---
title: Tetral 与 agent-native cloud 架构
description: Tetral 如何把 agent runtime 从 sandbox 中拆出来，用 PostgreSQL 状态、write-ahead execution 和独立授权边界构建可扩展的 cloud agent 系统。
type: topic
category: ai
created: 2026-10-02
updated: 2026-10-02
timestamp: 2026-10-02
tags:
  - agent
  - cloud-agents
  - scaling
  - durable-execution
  - sandbox
source_refs:
  - raw/sources/2026-10-02-the-next-scaling-problem.md
  - https://tetral.ai/blog/the-next-scaling-problem/
resource:
  - raw/sources/2026-10-02-the-next-scaling-problem.md
  - https://tetral.ai/blog/the-next-scaling-problem/
---

# Tetral 与 agent-native cloud 架构

## 摘要

Tetral 是 Yang Li 开发的开源（MIT）agent-native cloud 系统，当前为 alpha，跑在个人 k3s 集群上。它的核心主张是：cloud agent 的扩展瓶颈不在模型，而在系统结构——agent runtime 必须从 sandbox 中拆出来变成可替换的稳定服务，sandbox 降级为一种可丢弃的执行资源。原话："A computer should be something the agent calls, not somewhere the agent lives."（计算机应该是 agent 调用的对象，而不是 agent 居住的地方。）

## 关键点

### 1. 教训：sandbox 不该是容量的单位

作者的第一个产品 Anoma 把整个 agent loop 放进 E2B sandbox（照搬 Manus 的做法），结果 sandbox 成了 agent 容量的单位，扩展 agent 等于扩展 sandbox：

- 更多用户意味着更多 sandbox 要创建、复用、回收，受制于 provider 的生命周期约束
- session 历史和 trace 留在 sandbox 里，调试依赖接触含用户私有数据的环境
- API key 要放在 sandbox 外，得单独建一个 gateway 代理模型请求

结论：agent 是稳定的、可跨任务复用的共享服务；sandbox 是隔离的、突发的、一次性的。两者的扩展曲线不同，必须分开。Kubernetes pod 和 Firecracker microVM 都被评估过，前者不适合高频创建销毁的 sandbox（Modal 后来也公开了同样的结论），后者等于自建 sandbox provider——两条路都把 sandbox 供应留成了独立的基建问题。

### 2. 运行时边界：把不同生命周期的职责拉出 runtime

判定标准：凡是 owner、生命周期或扩展模式不同的职责，都移出 runtime。拆出来的组件：

| 组件 | 职责 |
| --- | --- |
| **Gateway** | provider 格式、凭证、出站连接、流式协议；对 runtime 暴露统一的请求和流接口；不保留 session 状态，可独立扩容 |
| **Bridge** | PostgreSQL 状态边界的唯一入口；校验所有权和顺序后提交状态转换 |
| **Queue** | 投递与执行任务：排序、租约、重试、取消、死信 |
| **Sandbox Service** | computer（执行环境）的生命周期与执行 |
| **Public API / Event Stream** | SDK 入口和事件导出，不在执行路径上 |

留在 runtime 里的是对 session 和 thread 的计算：session 是一段持续的 agent 工作，thread 是 session 内一条独立排序的执行路径（actor 式串行边界），子 agent 跑在子 thread 里。核心是一个纯 reducer：从已提交的输入和结果重建状态，返回下一个合法转换，不做任何数据库或网络 I/O。runtime pod 只是可替换的算力宿主，不拥有任何 session。

与 Cursor 的路线对比：Cursor 用 Temporal 做 durable execution，worker 重放 workflow 代码恢复控制流；Tetral 把恢复边界放在 PostgreSQL——替换的 runtime 从已提交记录重建 thread checkpoint，再问纯 reducer 要下一步。

### 3. Write-ahead execution：先记录，再执行

可替换 runtime 的核心难题：pod 消失后，接替者无法从进程内存判断一个操作是没开始、进行中还是已完成。猜错要么漏做要么重复执行外部副作用。

解法借用了数据库 WAL 的排序规则：**凡是能推进 thread 或产生外部义务的转换，必须先提交再派发**。派发前 runtime 向 Bridge 提交一份带稳定身份的 declaration；Bridge 在一个事务里提交转换和回执；收到确认后才允许派发操作。稳定身份是幂等键——重试同一声明返回已有回执，用同一身份提交不同内容会被拒绝。

文章用一次产生 Bash 调用的模型 turn 完整走了一遍协议：输入先提交再进上下文 → `span.model_request_start` 记录精确上下文边界 → 模型返回 Bash 调用后先提交 `agent.tool_use` 再路由 → sandbox 执行结果先落库（completed but not consumed）→ Bridge 在一个事务里追加 `agent.tool_result`、更新 `session_messages` 投影、标记结果已消费、记录幂等回执 → reducer 才能依赖结果算下一步。

协议不能让任意外部系统变成事务性的。它保证的是：每个副作用有已提交的身份和 owner，重试收敛到同一操作；结果不明时不许悄悄推进 thread。

这与 Pi harness-v2 的 intent record 是同一思想家族（副作用前先声明意图），见 [[wiki/syntheses/ai/persistent-agent-harness-design-patterns|持久化 Agent Harness 的设计模式]]。

### 4. 存储模型：事件日志 + 上下文投影 + 回执

存储设计借鉴 OpenCode v2 的 event table 与 session-message projection 分离：

| 表 | 职责 |
| --- | --- |
| `session_events` | 事件日志：有序执行历史（输入、请求边界、工具调用、结果、中断、收尾） |
| `session_messages` | 模型上下文投影：可加载进模型上下文的内容；compaction 后从新摘要检查点加载，但不删除早先的执行历史 |
| `session_bridge_operations` | 每份幂等声明的回执 |

三者合称 session log——逻辑执行记录，不是一张物理表也不只是对话转录。系统不存可变的状态机快照；冷加载时 Bridge 返回已提交的消息、边界和未完成工作，runtime 据此构建 checkpoint，reducer 判断 thread 在等请求、等工具还是可以继续。保留下来的历史后续可做可检索上下文，而不是让一份摘要扛全部过去。

### 5. Durable delivery：投递与执行分离

write-ahead 协议保证 thread 安全推进，但不保证已接受的输入能到达 thread。投递用 outbox 模式：一个 PostgreSQL 事务里同时追加输入事件、创建目标 thread 的 Inbox 条目、创建指向该条目的 Queue job。事务提交后 Public API 即返回 200，投递异步继续。

- `pg_notify` 唤醒 Job Runner；通知丢了由轮询兜底，消息本体一直在 PostgreSQL 里
- 同一 thread 的普通输入保序，后到的不能越过正在投递/重试的；其他 thread 并发推进；interrupt 单独处理不排队
- 到达 runtime 分两步收尾：Bridge 先记 Inbox 为 accepted，Job Runner 再确认 Queue job
- 防脑裂：超时不证明旧 runtime 已停；用 binding generation + pod UID 做 fencing token，Bridge 只在 Kubernetes 确认原 pod 已消失后才把已接受的投递还给 Queue

### 6. 模型调用：凭证不进 runtime

请求不带 API key 或 OAuth token。Gateway 校验 pod 的 Kubernetes workload identity 和短期 Bridge token（证明它仍拥有该 session/thread），被替换的 pod 无法再为旧 thread 刷新 token 或调用模型。凭证选中但缺失/吊销/不可解密时直接拒绝，不静默回退；OAuth 刷新也在 Gateway 边界完成，明文凭证不进 runtime、Bridge、session log 或 sandbox。请求经 Vercel AI SDK 转换成统一的 `ProviderStreamEvent` gRPC 流。MCP 工具走同样的边界：runtime 只拿工具名、描述和 schema，连接与凭证由 connector 持有。

### 7. Computer 是一种资源，懒分配

多数能力不需要计算机：模型和 web 请求归 Gateway，MCP 调用归 connector，记忆操作走 Bridge。只有 shell 和文件系统工具需要执行环境。computer 懒分配——Bash 声明和 Queue job 可以先于任何 computer 存在；worker 接到任务时检查 session 的 computer，可用就执行，否则触发 activation（复用/启动/创建/替换，加一个 materialization job 准备文件和访问权），并发调用共享同一次 activation。执行前把任务绑定到确切的当前 computer，防陈旧 worker 把命令发给新实例。当前实现是每 session 一个 Daytona computer，但这个映射不是抽象本身：文件访问可以走虚拟文件系统，小任务用轻量容器，平台特定工作用对应系统的机器。

### 8. 两个扩展维度：thread 与 session

一个有序上下文不能同时向两个方向推进（并发模型请求会读到同一边界、产出竞争的下一状态），并行需要独立的执行路径：

- **workspace** 持有长生命周期资源（文件、记忆）
- **session** 是一个持续任务：自己的配置、历史、生命周期、所选资源
- **thread** 是 session 内一条有序上下文和执行路径

thread 共享 session 不共享上下文；session 共享 workspace 不共享执行历史。子 agent 控制模型改编自 Codex 的 multi-agent 设计；`fork_turns` 显式选择子 thread 的起始上下文（`none` / `all` / 最近 N turns），runtime 解析成不可变的起始上下文。spawn 前先在一个事务里提交 `spawn_agent`、父子关系、上下文、指令和投递 job，重试返回同一个子 thread。父子通信走与普通输入相同的有序投递路径，谁也不能直接写对方的上下文。职责边界：同属一个任务的并行路径用子 thread；需要独立 root agent、独立凭证和生命周期的（实现、文档、审计、知识维护）用独立 session。

### 9. 授权是与凭证隔离分开的决策

凭证隔离管的是"能不能用某个能力"，授权管的是"这个提议的动作可不可以用"。授权决策必须在执行之前、且在提议它的 agent 之外。

`approve_for_me` 模式的流程：模型提议的 Bash 命令先过确定性的 tool gate（session 审批模式 + 工具目录 + 工具策略）；需要独立审查时，提议获得一个稳定 review 身份——`review_id = H(workspace, session, thread, request, tool_call, tool, action, policy)`，命令或策略变了就是不同的 review。reviewer 是一个内部 thread，用和其他 agent 工作相同的 runtime 机制；它收到的输入是证据不是指令（被审查材料可能含 prompt injection，平台侧的 reviewer 策略与审查材料分离）。reviewer 只返回风险等级、可见的用户授权、allow/deny 和理由；输出格式错按审查失败处理，不是放行。决定先提交 PostgreSQL，再过第二次 tool gate；deny 记录被拒的工具结果但不执行；runtime 在授权完成前消失则请求以 `runtime_pod_lost` 关闭，提议不重建不执行——**在这个边界上故意牺牲恢复能力，防止孤儿决定变成许可**。

### 10. 下一个扩展问题：模型之外的容量

agent 工作能超越任何进程和计算机之后，扩展不再只是加 runtime 容量——authority、identity、history、资源消耗都在同步增长，最短的那块板成为下一个瓶颈：

- **编译与验证**：更长 horizons 和更多并行路径意味着更多 runtime 转换、测试、构建循环。作者的开发服务器上一条 Tetral 集成路径要七八分钟，全量验证约半小时。编译和验证可能先于推理成为限制（例证：Bun 从 Zig 迁到 Rust、TypeScript 的 Go 原生移植）。
- **执行环境**：突发创建、挂载/恢复延迟、高 churn 调度和启动时间同样重要；sandbox 对多数操作太重，完整计算机不该是默认边界（actor system 是设计空间里的另一个点）。
- **存储**：session 事件、工具结果、日志要进有序 session 历史；代码、文档、构建产物要回到可被其他环境加载的仓库/对象存储/workspace 文件。
- **模型作为更大的交付单元**：采样参数在新模型上陆续废弃，agent 接口转向 effort、tools、skills、MCP、context、policy、orchestration——被配置的"产品"越来越是包含模型的 agent 系统，而非 surrounded by 产品特定基建的裸模型端点。

### 11. 协作观：对抗性审查先于综合

引用 Anthropic 的多 agent 研究指出：协调的 swarm 和独立并行 agent 的 token/结果比可能相近，更大的共享编码 swarm 合并的工作占比反而更低。Tetral 的押注是**综合之前的对抗性审查**：工作进入共享 workspace 前，其他 agent 必须挑战其结论和证据而不只是同意；人决定接受什么。被接受的成果成为后续探索的地基，未经检验的错误会向下游传播。同一任务跑不同 agent 版本，其轨迹可对比成评估数据；被拒的工具调用、被推翻的审查、失败验证和人工纠错都是具体的失败样本。

### 12. 现状与限制

alpha，个人 k3s 集群，未经过生产验证。已知缺口：runtime 调度不感知容量；backpressure 未打通准入、Queue 压力和扩容；多节点持续恢复未验证；runtime 滚动升级会打断进行中的 turn（没有优雅排水）。产品方向是 hosted agent system service：产品团队定义自己的工具、reviewer、thread 策略、资源、模型和界面，不用先重建连续性、身份、授权、恢复和资源调度。

## 相关页面

- [[wiki/topics/ai/agent-harness|Agent Harness]]
- [[wiki/syntheses/ai/persistent-agent-harness-design-patterns|持久化 Agent Harness 的设计模式]]
- [[wiki/syntheses/ai/agent-harness-evolution-paradigm|Agent Harness 演进范式]]
- [[wiki/syntheses/ai/agent-native-system-interface-design|Agent Native 系统接口设计]]
- [[wiki/syntheses/ai/auditable-local-agent-memory-architecture|可审计的本地 Agent 记忆架构]]

## 来源指针

- `raw/sources/2026-10-02-the-next-scaling-problem.md`
- https://tetral.ai/blog/the-next-scaling-problem/
