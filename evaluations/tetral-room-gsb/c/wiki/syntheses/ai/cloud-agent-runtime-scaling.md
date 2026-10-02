---
title: 云端 Agent 的规模化架构：把 runtime 移出沙箱
description: 云端 Agent 规模化时为什么不能以沙箱为容量单元；把 agent runtime 变成可替换的无状态计算单元、把状态和凭据移到数据库与网关之后，需要哪些协议支撑。
type: synthesis
category: ai
created: 2026-10-02
updated: 2026-10-02
timestamp: 2026-10-02
tags:
  - agent
  - harness
  - cloud
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

把本地 coding agent 搬上云时，最直接的做法是让整个 agent loop 住在一个虚拟机沙箱里（Manus 和 E2B 的路线）。这一页回答：为什么这个架构在规模化时会出问题，正确的容量单元和职责边界应该怎么划，以及把状态移出进程后需要补上哪些协议。

## 简答

沙箱是隔离的、突发的、用完即弃的，而 agent 是稳定的、可被许多任务复用的共享服务，两者的伸缩曲线不同，不应该绑在一起。把 agent 抽象成一个 runtime——一个只负责「加载线程状态、跑纯函数 reducer、声明下一个动作」的可替换计算单元——把状态放进事务数据库、把凭据和外部连接放进网关、把沙箱降级为按需分配的执行资源，就能让执行、身份和历史各自独立地失败、变更和伸缩。代价是必须补上写前提交、持久投递、授权边界这套协议，否则可替换的 runtime 无法安全推进线程。

## 来源事实

以下事实来自 Tetral 作者 Yang Li 2026-09-06 的文章（[The Next Scaling Problem](https://tetral.ai/blog/the-next-scaling-problem/)，素材见 `raw/sources/2026-10-02-the-next-scaling-problem.md`）。Tetral 本身是一个跑在个人 k3s 集群上的 alpha，不是经过生产验证的云服务。

架构演进的事实：

- 作者的第一个产品把整个 agent loop 放进 E2B 沙箱。结果是仍然要管理沙箱集群的分配、复用和回收；会话历史和 trace 留在沙箱里直到清理，调试依赖访问含用户私有数据的环境；API key 要放在沙箱外的网关代理。「我们不断把职责移出沙箱，才能让沙箱里的 agent 可用。」
- Kubernetes 的 pod 不适合高频创建销毁的沙箱（Modal 后来在百万级并发沙箱的场景记录了同样的不匹配：串行调度器和协调式 pod 生命周期成为瓶颈）；另一条路是 EC2 + Firecracker 自建沙箱服务，但那等于去做沙箱提供商，agent 容量仍受计算机数量限制。
- 结论：agent 是稳定共享服务，沙箱集群是突发可弃资源，两者必须分离。沙箱降级为与模型、内存、文件、凭据、工具并列的一种资源。「计算机应该是 agent 调用的东西，而不是 agent 居住的地方。」

runtime 边界的事实：

- 作者把 agent 定义为 runtime：一个持续运行的程序，解释模型输出并给 agent 受控的模型、网络、文件、工具、子 agent 和外部世界访问。Claude Code 和 Codex 在本地已经是这种 runtime。
- runtime 要成为可替换的计算单元，前提是身份、状态和资源都在进程之外。判据是：凡是拥有不同 owner、生命周期或伸缩模式的职责都要移出去。Tetral 移出的职责：Gateway（提供商格式、凭据、流式协议）、Bridge + PostgreSQL（状态与事务）、Queue（投递）、Sandbox Service（计算机生命周期）、Public API / Event Stream（产品面）。
- 剩下的计算是：session（一项持续任务）和 thread（session 内一条有序执行路径）。对每个活跃 thread，一个不做任何 I/O 的纯 reducer 根据已提交的输入和结果推导下一个合法转移；runtime 加载 thread、跑 reducer、声明下一个动作，不拥有任何线程，声明被接受前不能派发外部操作。

协议的事实：

- **写前执行（write-ahead execution）**：借 WAL 的排序规则——先记录转移，再执行它授权的操作。runtime 派发前向 Bridge 提交带稳定身份的不可变声明；Bridge 校验 ownership 和顺序后在一个事务里提交转移并返回回执；稳定身份是幂等键，重试同一声明返回已有回执。Pod 消失后，替代 runtime 从已提交事实重建 checkpoint，而不是恢复丢失的进程。
- **存储模型**：`session_events` 事件表保存有序执行历史，`session_messages` 是可加载进模型上下文的投影。这一分法来自 OpenCode v2 的事件表加 session-message 投影。压缩（compaction）只决定下一次模型请求加载什么，不抹除早先的执行历史。系统不存可变状态机快照，恢复完全靠这些记录。
- **持久投递**：outbox 模式——一个 PostgreSQL 事务同时追加输入事件、创建目标 thread 的 Inbox 条目、创建 Queue 任务。`pg_notify` 只是唤醒，丢了靠轮询兜底。绑定 generation 和 pod UID 作为 fencing token：只有 Kubernetes 确认原 pod 消失后，已接受的投递才回到 Queue 重新分配。
- **模型调用**：请求不带任何 API key 或 OAuth token；Gateway 用 Kubernetes workload identity 加短期 Bridge token 验证 pod 仍持有该 session/thread。OAuth 刷新在 Gateway 边界完成，明文凭据不进 runtime、Bridge、会话日志或沙箱。MCP 工具走同一边界：runtime 只拿到工具名、描述和 schema，凭据由 connector 注入远端请求。
- **计算机按需分配**：session 创建时不分配沙箱，只有 shell / 文件系统工具真正需要时才激活。一个已提交的 Bash 声明可以在没有可用计算机时先排队。
- **子 agent**：控制模型改编自 Codex 的 multi-agent 设计。父 thread 用 `spawn_agent` 创建子 thread，`fork_turns` 显式选择子线程的起始上下文（无父历史 / 全部 / 最近 N 轮）。spawn 声明先提交，一个事务里创建父子关系、存上下文和指令、放入 Inbox、创建投递任务；重试返回同一个子线程。父子后续通信全部走有序输入，互相不能直接写对方上下文。
- **授权是独立决策**：凭据隔离控制「能不能用某个能力」，授权决定「这一次提议的动作可不可以执行」。`approve_for_me` 模式下，工具提议先过确定性 tool gate，需要审查的提议由独立的 reviewer thread（用同一套 runtime 机制）评估，审查输入是证据不是指令（防注入：平台策略与被审材料分离），决策先提交 PostgreSQL 才返回。review_id 是对 workspace、session、thread、请求、tool call、工具、动作、策略的哈希，绑定唯一提案。审查未完成时 runtime 消失，请求以 `runtime_pod_lost` 关闭，提案不重建也不执行——在这个边界上故意牺牲恢复性，避免孤儿决策变成许可。

作者对趋势的判断（区别于已实现的事实）：

- 模型变强会让「系统」而不是模型先成为瓶颈：更多 runtime 转移、测试、计算机、文件、网络请求和外部效果，最短的那块容量是下一个规模化问题。作者的开发服务器上一次 Tetral 集成路径要七八分钟，完整验证约半小时——编译和验证可能在推理之前先成为限制。
- 被配置的产品越来越是「包含模型的 agent 系统」而不是裸模型端点（Claude API 对新模型废弃 temperature/top_k 等采样参数、OpenAI 的最新模型指南转向推理控制、托管工具和多 agent 执行，被引为同一方向的证据）。
- 多 agent 协作上，作者押注「合成前的对抗性审查」：工作进入共享 workspace 前必须被其他 agent 挑战结论和证据，再由人决定是否接受；共享对话不能替代已接受的产物。依据之一是 Anthropic 的多 agent 研究：协调蜂群和独立并行 agent 每单位结果消耗相近 token，更大的共享编码蜂群能合并的工作比例更小。

## 综合结论

结合本库已有的 [[wiki/topics/ai/agent-harness|Agent Harness]] 和 [[wiki/topics/ai/agent-harness-design-tradeoffs|Agent Harness 设计取舍]]，这篇文章补充了云端一侧的判断：

**1. 容量单元的选择是云端 harness 的第一决策，沙箱不是好的默认单元。**已有页面记录了工具组合应该移进代码沙箱（Pi Codemode、OpenAI PTC），那是「单次任务内在哪里跑脚本」的问题；这篇文章处理的是「agent 本体住在哪里」的问题。两个层面结论不同：脚本执行进沙箱，agent loop 出沙箱。判据是伸缩曲线：凡是和 agent 主循环生命周期不同的职责（沙箱、凭据、状态、投递），都应该移出可替换的计算边界。这与 Claude Code（本地文件系统协作状态）和 OpenAI Agent Server（云端托管会话）的分歧是同一问题在不同部署形态下的答案。

**2. 「无状态可替换 runtime」不是免费的设计，它用一套写协议换伸缩性。**runtime 一旦不拥有状态，每个外部效果都要回答「没开始 / 进行中 / 已完成」，这正是进程内存答不了的。Tetral 的答案是把 WAL 规则搬到 agent 层：先提交转移再执行操作，用幂等声明收窄重试语义。这条结论的可迁移部分是规则本身（记录线程可以做什么，再做；记录发生了什么，再依赖它），而不是具体的服务拆分——Gateway、Bridge、Queue、Sandbox Service 的拓扑是 Tetral 的实现选择，作者自己预期服务会合并、拆分或替换。

**3. 凭据和授权是两个边界，都要在执行路径上而不是 agent 内部。**Gateway 挡住凭据（runtime 和沙箱都拿不到明文密钥）解决访问控制；tool gate 加已提交的审查决策解决动作授权。把 LLM 审查放进云端边界的好处是策略对客户端和执行环境一致，且「审查者可以替换」——runtime 和执行服务不随审查策略演进变化。作者明确收窄了承诺：这套系统保证的是「被审查的动作在有记录的决策之前不可调度、不确定性永远不变成许可」，而不是审查者本身可靠。

**4. 子 agent 的上下文继承应该显式声明而不是隐式共享。**`fork_turns` 把「子 agent 拿多少父上下文」从隐式行为变成接口定义里的参数，父子后续通信走与用户输入相同的有序投递路径，没有第二条内容通道。这和 [[wiki/syntheses/ai/agent-team-roles-and-collaboration|Agent 团队的角色分工与协作模式]] 里观察到的「thread 之间不共享上下文、通过消息协作」一致，但补上了持久化语义：spawn、消息、完成通知都是先落库的声明。

**适用边界与证据强度**：以上判断的实现证据是一个人的 alpha 项目，作者自述的未解决问题包括 runtime 放置不感知容量、背压未连接准入与扩缩容、多节点持续恢复未演示、发布会中断进行中的轮次。写前执行、持久投递、fencing token 各自是分布式系统里被验证过的成熟技术（WAL、outbox、fencing），novel 的部分是它们在 agent loop 上的组合方式，这个组合尚未经过生产流量检验。「模型变强后系统先于推理成为瓶颈」「对抗性审查先于合成」是作者的判断加部分外部证据（Modal、Anthropic 研究、TypeScript/Bun 的工具链重构），不是本文的实测结论。

## 一个具体例子：一次 Bash 调用怎么穿过这套系统

以文中 Bash 执行 #42 为例，跟着一次工具调用走完全程：

1. 模型在模型请求中返回一个 Bash 调用。此时它只是提议：没有公开的 `agent.tool_use`，没有沙箱任务，没有外部效果。
2. 如果该工具策略要求审查（`always_ask`），提议先过 tool gate，由 reviewer thread 评估并给出 allow/deny；决策提交 PostgreSQL 后，runtime 第二次跑 gate，deny 则记录被拒绝的工具结果、不执行命令。
3. 审查通过后，runtime 提交 `agent.tool_use` 声明，Bridge 校验 ownership 和顺序后在一个事务里提交并返回回执。
4. Bridge 同时记录执行 #42 和它的第一个 Queue 任务。此时还没有任何计算机——计算机是懒分配的。
5. 一个执行 worker 租到任务 #42，发现该 session 的计算机是冷的：把这个执行挂到一次激活（activation A7）上，声明在 PostgreSQL 里保持 `waiting_activation`；并发的调用可以共享同一次激活，不会各起一台计算机。
6. 生命周期 worker 激活计算机后，同一逻辑执行以第二代（generation 2）回到 Queue；worker 执行 Bash，把原始结果存为「已完成、未消费」。runtime 失败不会取消这次计算机操作，也不需要重发命令。
7. 等待中的 runtime 通过 Bridge 拿到结果，提交 `agent.tool_result`——同一个事务里追加事件、更新 `session_messages` 投影、把沙箱结果标记为已消费、记录幂等回执。reducer 此后才能依赖这个结果算下一步。

任何一步之后 pod 消失，替代 runtime 都从 PostgreSQL 的已提交记录重建：没有提交的提议不重建（宁可不执行，不让孤儿决策变成许可），已提交的效果靠稳定身份重试收敛到同一操作。

## 未决问题

- 写前执行协议在 agent loop 上的性能代价：每步两个事务（声明 + 回执）加一次存储往返，对短任务的延迟影响文章未给数据。
- 「对抗性审查先于合成」目前是设计立场，文章引用的多 agent 研究证据（token 消耗相近、合并率下降）不支持也不否定它，需要产品内的对照数据。
- actor 式轻量计算（可休眠唤醒、不需要整台计算机）如何映射到 session/thread/resource worker，作者标为开放问题；「沙箱不应是每个操作的默认边界」到什么粒度替代（虚拟文件系统、轻量容器）尚无实现。
- Tetral 兼容 Anthropic Managed Agents API 的 fork 路线（中立 SDK + 自建底层）能否成立，取决于生态采用，文章无法回答。

## 相关页面

- [[wiki/topics/ai/agent-harness|Agent Harness]]
- [[wiki/topics/ai/agent-harness-design-tradeoffs|Agent Harness 设计取舍]]
- [[wiki/syntheses/ai/agent-team-roles-and-collaboration|Agent 团队的角色分工与协作模式]]
- [[wiki/syntheses/ai/persistent-agent-harness-design-patterns|持久化 Agent Harness 的设计模式]]
- [[wiki/topics/ai/mcp|MCP]]

## 来源指针

- `raw/sources/2026-10-02-the-next-scaling-problem.md` / [The Next Scaling Problem — Tetral（Yang Li），2026-09-06](https://tetral.ai/blog/the-next-scaling-problem/)
- 文中引用的关键外部来源：[Modal：扩展到百万并发沙箱](https://modal.com/blog/scaling-to-1-million-concurrent-sandboxes-in-seconds)、[Anthropic：Managed Agents](https://www.anthropic.com/engineering/managed-agents)、[Anthropic：multi-agent systems 研究](https://www.anthropic.com/research/multiagent-systems)、[Cursor：Cloud Agent Lessons（Temporal 路线）](https://cursor.com/blog/cloud-agent-lessons)
