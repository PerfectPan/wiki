---
title: 云端 Agent 的规模化架构：把 runtime 移出沙箱
description: 分析云端 Agent 在多会话并发伸缩时将运行环境与沙箱容器解耦的架构设计，包括职责切分、写前执行、持久化投递与状态恢复边界。
type: synthesis
category: ai
created: 2026-10-02
updated: 2026-10-02
timestamp: 2026-10-02
tags:
  - agent
  - cloud
  - scaling
  - sandbox
  - architecture
source_refs:
  - raw/sources/2026-10-02-the-next-scaling-problem.md
  - https://tetral.ai/blog/the-next-scaling-problem/
resource:
  - raw/sources/2026-10-02-the-next-scaling-problem.md
  - https://tetral.ai/blog/the-next-scaling-problem/
---

# 云端 Agent 的规模化架构：把 runtime 移出沙箱

## 问题

将本地单机 Agent（如 Claude Code、Codex CLI）迁移至云端服务时，如果把「一个沙箱容器」当作「一个 Agent 的容量单位」，在应对高并发多会话时会面临沙箱频繁创建销毁、状态与环境强绑定、凭据泄露风险以及难以弹性扩缩容等架构瓶颈。云端 Agent 的运行环境应当如何设计职责边界与持久化机制，才能兼顾多会话伸缩、故障恢复与安全性？

## 简答

将 Agent 抽象为无状态且可替换的计算单元（Runtime），并将身份、状态、凭据和物理计算环境全部外置到进程之外。核心原则是「计算机只是 Agent 按需调用的资源，而不是 Agent 驻留的宿主」；通过在数据库中提交转换记录先于外部操作派发的「写前执行」（Write-Ahead Execution）协议、原子入队的持久化投递机制，以及独立于执行环境的权限检查，使运行实例能够随时崩溃或替换，而会话状态与执行链路始终保持一致。

## 综合结论

### 1. 从「沙箱等于容量单位」到「计算资源解耦」

在早期云端 Agent 实践（例如将 Agent 循环直接运行在 E2B 或轻量虚拟机中）中，普遍做法是将整个 Agent 进程部署在隔离沙箱内，依赖沙箱的文件系统保存上下文。这种架构在规模化时存在明显结构性错配：

1. **伸缩曲线脱节**：Agent 核心逻辑（提示词组装、模型调用、状态转移）是长生命周期、相对稳定的服务，可以在多个会话间复用；而执行工具命令的沙箱环境是短生命周期、突发且高频创建销毁的一次性资源。将二者绑死会导致 Kubernetes Pod 或虚拟机调度器面临极高的调度颠簸（churn）与冷启动瓶颈。
2. **调试与数据边界混杂**：会话历史、Trace 日志与用户私有代码混合在同一个沙箱环境中。排查运行时故障需要访问存有用户敏感资产的容器，违背最小特权原则。
3. **凭据无法物理隔离**：若 Agent 跑在沙箱中，访问模型 API 的密钥或外部 OAuth 令牌通常必须注入沙箱，导致任何被沙箱内任意代码执行（RCE）攻破的环节都会直接泄露平台凭据。

因此，解耦的核心分界是：**计算机（Computer）是 Agent 调用的外部资源，而不是 Agent 住的地方**。沙箱退化为与模型 API、MCP 服务器并列的可插拔资源服务，按需懒分配并独立调度。

### 2. Runtime 的职责边界切分

将 Agent 视为一个可随时替换的计算单元后，凡是所有者不同、生命周期不同、伸缩模式不同的职责，全部移出 Runtime 进程：

- **Gateway（接入网关）**：负责屏蔽模型供应商请求格式差异、维护外部长连接与流式响应协议、管理敏感凭据（如 API 密钥与 OAuth 令牌自动刷新）。Gateway 无会话状态，纯粹按请求伸缩；明文凭据绝不进入 Runtime 或沙箱。
- **Bridge 与 PostgreSQL（状态与事务控制）**：PostgreSQL 作为全局权威事实源；Bridge 充当数据库边界的看护服务，统一负责在事务中检查会话归属、时序递增、提交状态转换并返回带唯一标识的回执。Runtime 自身不直连数据库，避免将业务运行时与存储实现细节绑定。
- **Queue（持久化作业队列）**：负责跨进程与跨节点的工作投递，管理任务租约、按目标线程保序、重试、超时以及死信。
- **Sandbox Service（计算机资源池）**：管理底层隔离环境（如 Daytona 驱动的虚拟机或轻量容器）的生命周期。Runtime 仅向系统声明「当前执行需要一次计算机操作」，由 Sandbox Service 负责懒加载、环境激活、文件挂载与命令执行。
- **Runtime（纯计算核心）**：Runtime 实例仅运行一个不含网络和数据库直接 I/O 的纯函数状态机（Reducer）。它从 Bridge 拉取已提交的事实，推导下一步动作（发起模型调用、派发工具、等待外部输入或结束），并将动作声明交由 Bridge 记录。

### 3. 写前执行协议（Write-Ahead Execution）与恢复边界

无状态计算实例带来的核心挑战是：当承载 Runtime 的容器或节点意外崩溃消失时，接替的新实例如何确认某个外部操作（如执行 Shell 命令或扣费操作）是未开始、进行中还是已完成？

该系统借鉴了数据库的预写式日志（WAL）机制，实施**写前执行**调用约定：

1. **不可变声明与幂等标识**：Runtime 在派发任何可能推动线程前进或产生外部副作用的操作之前，必须先向 Bridge 提交一个不可变的意图声明，并附带稳定的幂等标识符（Idempotency Key）。
2. **单事务原子提交**：Bridge 校验会话所有权与时序，在 PostgreSQL 的单一事务中同时持久化状态转换记录和对应回执。只有收到数据库提交确认后，Runtime 才被允许实际调度外部操作。若网络抖动导致确认丢失，Runtime 使用相同标识重试只会获取既有回执，不会重复触发。
3. **基于事实重建，不存易变快照**：
   - 存储模型分为两层：`session_events` 记录严格有序的全局执行日志（输入接收、请求边界、工具调用、工具返回、中断信号等）；`session_messages` 则是面向模型上下文的投影，随执行过程累积。当上下文过长触发摘要压缩（Compaction）后，后续模型加载从最新的检查点开始，但历史事件日志完整保留，可供未来检索。
   - 崩溃恢复时不恢复已丢失进程的内存快照，而是由替补 Runtime 通过 Bridge 重新拉取已提交的上下文与未决任务，重新经由 Reducer 确认状态。

这一设计与 Cursor 依托 Temporal 工作流引擎的持久化执行（Durable Execution）路线形成对照：Temporal 依靠重放代码事件历史来恢复工作流的程序控制流；而此处选择将单一事务型关系数据库（PostgreSQL）作为系统的状态恢复边界。

### 4. 消息投递保证与隔离边界（Outbox 与 Fencing Token）

为保证外部输入在没有可用 Runtime Pod 时不丢失，系统采用发件箱模式（Transactional Outbox）实现原子入队：

1. **原子写入**：用户的输入消息、对应的线程收件箱（Inbox）记录以及指向该记录的 Queue 待处理任务，在同一个 PostgreSQL 事务中提交。提交成功后接口立即向客户端返回成功，后续投递异步执行。
2. **保序与中断**：推进同一上下文的输入严格保持有序，后续普通消息不能越过正在投递或重试的前序消息；其他线程则并发独立执行。会话级的全局变更会形成隔离屏障（Barrier），而中断（Interrupt）信号通过单独通道分发优先送达，无需排在普通待处理消息后。
3. **隔离防重（Fencing Token）**：当节点响应超时时，无法直接断定原 Runtime 已经停止执行。系统将 Kubernetes 的 Pod UID 与 Binding Generation 作为隔离凭据（Fencing Token）。Bridge 仅在底层集群确认原 Pod 已经销毁后，才允许将超时任务重新放回队列由其他节点认领，杜绝双写脑裂。

### 5. 并发模型：Workspace、Session 与 Thread

系统划分了三层概念以支持并发执行：

- **Workspace（工作区）**：定义静态资产与长期资源，如文件、仓库、记忆库和环境配置。
- **Session（会话）**：代表一个持续运行的具体任务目标，绑定特定 Agent 版本与选定的资源实例。各 Session 共享 Workspace 但不共享执行历史。
- **Thread（线程）**：Session 内部的单一有序执行序列与上下文边界。一个 Session 默认由一个根线程承载，支持派生子线程运行子 Agent。

子 Agent 并发派生设计借鉴了 Codex 的多 Agent 模型，并在底层映射为独立子线程：
- 父线程调用派生指令时，通过 `fork_turns` 参数显式定义上下文继承范围（`none` 不继承、`all` 继承全部、或保留最近 N 轮），生成不可变的初始上下文，避免无节制膨胀。
- 父子线程上下文物理隔离，彼此不能直接读写对方的上下文；跨线程通信全部通过持久化收件箱投递，经由严格的事务提交与消息队列保序流转。

### 6. 独立授权与审批机制（Tool Gate 与 approve_for_me）

将凭据移出沙箱解决了访问权限控制（Capability Access），但并未解决单次操作的授权判定（Authorization Decision）。在云端环境中，任何外部工具调用在真正触发副作用前，必须通过独立的检查边界。

系统设计了与业务 Agent 隔离的审查机制：

1. **静态过滤与意图哈希**：当模型提出受控工具（如 Shell）调用时，Runtime 首先通过 Tool Gate。若判定需要审批，该提案会生成不可变哈希标识：
   `review_id = H(workspace, session, thread, request, tool_call, tool, action, policy)`
2. **独立审查线程**：审查逻辑运行在隔离的审查线程中，输入包括被审查动作、上下文证据与系统安全要求。平台审查规则与可能含有提示注入攻击的外部输入完全隔离。
3. **确定性优先**：审查判定结果必须先由 Bridge 写入 PostgreSQL 提交；随后 Runtime 带着已提交的判定结果再次通过 Tool Gate。只有判定允许，才会正式写入对外可见的 `agent.tool_use` 事件并派发给工作队列。若在审批完成前 Runtime 崩溃，该请求直接标记失败，**不确定的状态绝不转化为执行许可**。

### 7. 端到端流转实例：以 Bash 工具调用为例

以下梳理一次模型生成 Bash 命令到最终执行完成的完整生命周期：

```
[Runtime / Reducer]
  │ 1. 产出 Bash 提案 (未提交)
  ▼
[Tool Gate]
  │ 2. 命中审批策略，生成 review_id
  ▼
[Reviewer Thread]
  │ 3. 独立审查，输出 allow
  ▼
[Bridge / PostgreSQL]
  │ 4. 事务提交审批通过记录
  ▼
[Tool Gate]
  │ 5. 二次校验通过，提交 agent.tool_use 与 Queue 任务
  ▼
[Queue]
  │ 6. Sandbox Worker 认领任务
  ▼
[Sandbox Service]
  │ 7. 检查关联 Computer：
  │    - 若冷态：挂起任务至激活队列 (waiting_activation)，启动 Daytona 实例并挂载文件
  │    - 若热态：绑定当前计算机代次，执行 bash 脚本
  │ 8. 写入执行结果为待消费状态
  ▼
[Bridge / PostgreSQL]
  │ 9. 原子事务：追加 agent.tool_result、更新 session_messages、消费输出回执
  ▼
[Runtime / Reducer]
  │ 10. 确认收到确认回执，推动下一步规划
```

在此流程中，写前执行协议并不能使任意外部系统事务化。若 Runtime 实例在流式响应或工具执行过程中崩溃，已提交的工作可按既有记录安全恢复，重试请求经由幂等标识收敛到同一操作；对于未完成或中断的外部效果，系统依已提交的事实将其显式标记关闭（例如将未竟的模型请求标记为 `runtime_pod_lost`，审批中途崩溃则放弃提案），杜绝未经验证的操作静默推进线程。

## 未决问题

1. **持续多节点恢复尚未验证**：作者当前运行在个人 k3s 集群上，自认 sustained multi-node recovery 尚未得到充分验证，大规模集群下的 Pod 驱逐与故障转移表现仍待检验。
2. **缺乏容量感知与平滑排水**：调度器尚未感知 Runtime 与 Sandbox Worker 的实时资源压力；版本发布时对正在执行的长任务会产生中断，平滑排水（Graceful Draining）机制尚待完善。
3. **轻量计算单元的下沉抽象**：对只涉及轻微文件读写或无害检查的工具，调动完整容器沙箱依然过重。未来是否引入基于 Actor（如 Rivet）的极轻量执行单元，与重型沙箱形成梯级调度，仍属探索方向。
4. **编译与验证可能先于推理成为瓶颈**：随着代码生成规模增加，编译与测试验证可能先于模型推理成为整个系统的性能瓶颈。以作者的开发机为例，一条集成路径耗时约 7 至 8 分钟，全量验证则需约半小时，长程任务耗时受制于底层工程基建。

## 相关页面

- [[wiki/topics/ai/agent-harness|Agent Harness]]
- [[wiki/topics/ai/agent-harness-design-tradeoffs|Agent Harness 的设计取舍]]
- [[wiki/topics/ai/code-agent|Code Agent]]
- [[wiki/syntheses/ai/agent-loop-control-boundaries|Agent 循环工作流的控制边界]]
- [[wiki/topics/systems/sandbox|Sandbox]]

## 来源指针

- `raw/sources/2026-10-02-the-next-scaling-problem.md`
- [The Next Scaling Problem — Yang Li，2026-09-06，Tetral 博客](https://tetral.ai/blog/the-next-scaling-problem/)
