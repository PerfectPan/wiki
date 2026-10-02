---
title: Tetral 如何把 Agent 运行时移出沙箱
description: 分析 Tetral 在云端服务中把运行时移出沙箱的架构设想，梳理基于 PostgreSQL 的 write-ahead execution 记录机制、按需分配计算机与凭证授权解耦，并记录作者自述的系统局限。
type: synthesis
category: ai
created: 2026-10-02
updated: 2026-10-02
timestamp: 2026-10-02
tags:
  - agent
  - cloud
  - runtime
  - scaling
source_refs:
  - raw/sources/2026-10-02-the-next-scaling-problem.md
  - https://tetral.ai/blog/the-next-scaling-problem/
resource:
  - raw/sources/2026-10-02-the-next-scaling-problem.md
  - https://tetral.ai/blog/the-next-scaling-problem/
---

# Tetral 如何把 Agent 运行时移出沙箱

## 问题

把 Agent 运行时从单机沙箱中拆出之后，云端系统应该如何组织执行边界、持久化状态与外部计算资源，才能让长期 Agent 工作的生命周期脱离单个进程或虚拟机的限制？

## 简答

作者在自己的云端服务中选择把运行时与沙箱分开，理由是沙箱属于突发、易失的隔离环境，而 Agent 状态需要长期保留。Tetral 设想的架构是将运行时做成无状态的计算 Pod，将沙箱降为按需调用的外部工具，并在向外部派发操作前先向 PostgreSQL 提交调用声明（write-ahead execution），配合凭证与授权审查分离来应对进程崩溃。但作者明确说明该系统目前只是运行在个人 k3s 集群上的 alpha 原型，多节点持续恢复和背压等机制尚未经过生产验证。

## 核心机制与实现细节

作者围绕四个核心问题展开架构设计（对应原文第 1 至 9 节）：

### 1. 为什么把运行时移出沙箱？（原文第 1-3 节）

在第一代产品（Anoma）中，作者把整个 Agent 循环放进 E2B 虚拟机沙箱中，导致调试必须进入存有用户私有数据的虚拟机、模型 API Key 需要单独做代理网关，团队还要自行管理沙箱的创建、复用和回收。

在第二代设计（Tetral）中，作者将沙箱与 Agent 拆开：Agent 是长期的共享服务，沙箱则是临时、易失的执行环境。系统将身份、状态和关联资源全部移出进程，划分出五项职责：
- **Gateway**：处理不同供应商的模型接口转换、注入凭证并维护流式连接，不存会话状态，独立扩缩。
- **Bridge + PostgreSQL**：PostgreSQL 作为唯一的事实来源与状态记录点；Bridge 在写入数据库前检查任务所有权与操作顺序。与 Cursor 依赖 Temporal 重放工作流不同，Tetral 将恢复逻辑交给 PostgreSQL 记录。
- **Queue**：负责消息排序、租约、重试和死信。
- **Sandbox Service**：负责虚拟机的激活、执行命令与销毁替换。
- **Public API**：处理外部请求，不在核心执行路径上。

系统内的概念定义为：`session`（配置和资源固定的持续任务）、`thread`（串行有序上下文路径）、`reducer`（纯函数，仅根据已提交的输入和事件计算下一步操作，不直接读写网络或数据库）。

### 2. 运行时重启时如何避免重复执行或遗漏操作？（原文第 4-5 节）

为了防止 Pod 崩溃或重启后无法判断外部操作是否已执行，系统借鉴数据库 WAL 思路，采用 **write-ahead execution**：任何操作必须先由 Bridge 写入数据库确认，然后才向外部系统派发。

数据保存在三张表中：
- `session_events`：不可变事件日志，按序记录所有输入、工具调用与结果。
- `session_messages`：面向模型的对话投影，压缩（compaction）只影响下一次传给模型的上下文范围，不删除早期的事件记录。
- `session_bridge_operations`：记录操作的幂等回执，用相同身份重试直接返回已有结果，更换内容复用同一身份则会被拒绝。

**Bash 命令执行的具体链路**：
1. 外部输入写入数据库后记录 `span.model_request_start`，划定模型上下文边界。
2. 模型返回 Bash 调用后，Bridge 先向数据库提交 `agent.tool_use`，随后才路由该调用。
3. Bridge 在一个数据库事务中同时登记沙箱执行记录和对应的 Queue 任务。
4. 沙箱 worker 取出任务执行命令，并将原始结果保存为已完成但未消费。
5. Bridge 发起单个事务：向 `session_events` 追加 `agent.tool_result`、更新 `session_messages`、把沙箱结果标为已消费，并写入幂等回执。
6. 模型请求结束时记录 `span.model_request_end`。

若在模型流式输出或执行中 Pod 丢失，请求标记为 `runtime_pod_lost` 终止，系统不会强行恢复断开的流。

在消息投递（durable delivery）方面，Public API 在一个事务中写入输入事件、Inbox 记录和 Queue 任务后立即返回 200。为了避免分布式租约超时导致的脑裂，系统结合 binding generation 与 Kubernetes Pod UID 作为 fencing token；只有 Kubernetes API 确认旧 Pod 已经销毁，Bridge 才会把已接受的投递收回并重新放回 Queue。

### 3. 计算机如何作为外部资源按需调度？（原文第 7 节）

原文指出："A computer should be something the agent calls, not somewhere the agent lives."（计算机应当是 Agent 调用的外部资源，而不是 Agent 驻留的环境。）

以 execution #42 的冷启动为例：
1. Worker 派发执行时发现沙箱未激活，便将该逻辑执行挂起在对应的激活任务（activation A7）上，状态设为 `waiting_activation`。
2. Sandbox Service 在派发前将执行绑定到当前的具体计算机实例，防止旧 Worker 错发指令到新实例。
3. 激活完成后，该执行以新的 generation 重新回到 Queue，并发的多次调用共享同一次激活。
4. 执行完成后结果由 Sandbox Service 暂存，等待运行时通过 Bridge 结算，Pod 崩溃不会导致命令重新执行。

作者说明当前实现采用 Daytona 虚拟机，这属于现阶段的工程选择，未来针对文件读写可使用虚拟文件系统，轻量任务可使用临时容器。

### 4. 凭证隔离与授权审查如何分离？（原文第 6、9 节）

系统将“是否有权限调用外部服务”与“具体某个操作是否被允许执行”分开处理：
- **凭证隔离**：运行时 Pod 不持有长期 API Key 或 OAuth Token。向 Gateway 发送请求时，Gateway 校验 Kubernetes workload identity 与短期 Bridge token；OAuth 在 Gateway 边界通过行锁刷新，明文凭证不写入日志或沙箱。
- **授权审查（`approve_for_me` 流程）**：
  1. Tool Gate 依据静态规则初筛，若需审查，提案保持为 proposal 状态，不产生公开的 `agent.tool_use`、不派发沙箱任务。
  2. 计算哈希绑定审查对象：`review_id = H(workspace, session, thread, request, tool_call, tool, action, policy)`，修改命令或策略都会生成新的审查 ID。
  3. 审查者作为内部 thread 运行，输入的审查材料视为待检证据而非指令（防止提示词注入），平台的提示词指令与被审查的材料分开。持久的审查主线程（reviewer trunk）串行审查；并发审查时从主线程最新状态克隆临时副本线程（sidecar threads）并行评估，完成后销毁副本。
  4. 审查输出必须包含风险级别、用户授权判断与 allow/deny 结果，格式异常直接按审查失败拒绝，不默认放行。
  5. 审查决定先写入 PostgreSQL，经 Tool Gate 二次核验通过后，才正式提交公开的 `agent.tool_use`。
  6. 若 Pod 在提案后、授权前丢失，请求直接以 `runtime_pod_lost` 终止，未决提案作废不补执行，防止孤立未决状态转为误放行。

## 扩展趋势与协作判断（作者观点，原文第 10-13 节）

作者对 Agent 系统的演进趋势作出了以下分析与推测（非既成事实）：
- **系统瓶颈转移**：模型能力增强会带来更多状态流转、虚拟机调用、网络请求与外部副作用，周边系统的最短板会成为瓶颈。
- **编译与验证耗时**：作者引用 TypeScript 的原生 Go 移植早期版本声称运行速度约快十倍且占用更少内存，而 Bun 从 Zig 迁至 Rust 则重在降低内存使用、提升吞吐和解决内存安全问题；作者提到在其本地机器上单条集成测试需 7-8 分钟、全量验证需约半小时，认为代码编译与测试验证可能先于模型推理成为限制迭代的瓶颈。
- **沙箱非默认边界**：沙箱过重，轻量 actor 系统是另一可选方向；Agent 产生的高频写入会促使底层存储调整（如 OpenAI 的 PG 扩展、Cursor 基于对象存储 WAL 的 Git host）。
- **模型交付单元扩大**：随着 `temperature` 等采样参数在近期模型中逐渐弃用，配置转向推理深度（effort）、工具集成、MCP 和多 Agent 编排，模型正在被封装进更大的系统中。
- **对抗式审查先于合并**：简单增加 Agent 数量或通信并不改善协作（Anthropic 研究显示更大规模共享编码群组的代码合并率反而下降）。作者主张由独立 Agent 主动对抗质疑证据，最终由人类决定是否合并，未经验证的错误被阻断在 session 内部。

## 系统局限与实现约束（作者声明，原文第 14 节）

该架构目前只是一个 alpha 原型，作者在文末承认了以下具体的工程局限：
1. **运行环境**：目前仅运行在作者个人的 k3s 集群上，尚未验证持续的多节点故障恢复。
2. **调度无容量感知**：运行时 Pod 的分配和调度尚未结合节点资源容量。
3. **背压未闭环**：请求准入控制、Queue 积压压力与底层计算节点的弹性扩缩容尚未联动打通。
4. **缺乏平滑停机**：系统重新发布更新时会直接中断正在处理中的 turn，尚未实现优雅排水（drain）。
5. **规划中的功能尚未落地**：代码模式（Code Mode，在隔离 JavaScript 环境中组合调用 MCP 工具）目前仅为设计规划（planned）；沙箱环境当前绑定于 Daytona。

## 综合结论

Tetral 的工程思路在于把 Agent 的长期状态与临时计算环境解耦：PostgreSQL 集中保存事件、投影与回执等持久化记录，reducer 仍在运行时 Pod 中纯内存计算下一个状态转移。系统采用 write-ahead execution 原则，要求在派发外部操作前必须先提交调用声明，并在操作完成后把结果提交入库，reducer 才能依赖该结果推进下一步。这种机制让无状态 Pod 在崩溃时可以重新从数据库构建 checkpoint 并继续运行。同时，系统把沙箱降级为按需调用的资源，并通过独立的审查线程控制操作权限。但正如作者所指出的，该系统在多节点环境下的容灾稳定性、调度容量感知与背压机制仍未得到验证，其实际生产表现还有待后续检验。

## 未决问题

- 在高并发海量工具调用的长任务中，三表模型频繁的行锁事务与事件追加是否会成为 PostgreSQL 的写入瓶颈？
- 编译、构建与集成测试等重型计算资源如何在按需冷启动时延与常驻成本之间取得平衡？
- Code Mode 规划中的受限 JavaScript 执行沙箱与直接调用外部 MCP 服务之间，其边界与权限粒度如何定义？

## 来源指针

- [raw/sources/2026-10-02-the-next-scaling-problem.md](../../../raw/sources/2026-10-02-the-next-scaling-problem.md)（原文抓取存档）
- [The Next Scaling Problem - Tetral Blog](https://tetral.ai/blog/the-next-scaling-problem/)
- 相关页面：[[wiki/topics/ai/agent-harness|Agent Harness]]、[[wiki/topics/ai/agent-harness-design-tradeoffs|Agent Harness 的设计取舍]]、[[wiki/syntheses/ai/persistent-agent-harness-design-patterns|持久化 Agent Harness 的设计模式]]、[[wiki/syntheses/ai/agent-loop-control-boundaries|Agent 循环工作流的控制边界]]
