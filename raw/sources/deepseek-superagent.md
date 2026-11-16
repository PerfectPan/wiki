<!--
source: https://x.com/DeepSeekHarness/status/2116857257245987236
type: tweet
author: DeepSeek Harness (Yujia Qiao et al.)
published: 2026-11-01
fetched: 2026-11-16
note: X article 2116829218935857152 + prototype repo deepseek-ai/dsh-superagent-prototype@8c32a9dc5d72c033816c6a8110b37f40cf94fba4
-->

# DeepSeek Super-agent 设计与原型 — 来源核查记录

## 访问元信息

- X 推文与长文：<https://x.com/DeepSeekHarness/status/2116857257245987236>（长文 ID `2116829218935857152`，标题 *Exploring Super-agent Design: Towards a More Autonomous Agent System*，作者 Yujia Qiao 及 DeepSeek Harness 团队，发布于 2026-11-01）。
- 原型仓库：<https://github.com/deepseek-ai/dsh-superagent-prototype>（MIT 许可，核查固定提交 `8c32a9dc5d72c033816c6a8110b37f40cf94fba4`）。
- 访问日期：2026-11-16。
- 边界声明：X 长文开头注明“探讨架构思路，并非 DeepSeek Harness 现有功能介绍”；原型仓库 `README.md` 注明该插件是从团队日常开发演化出的研究原型，经过整理后发布，部分长文讨论的设计（如跨设备 BYOM 守护进程、独立 Watchdog Session、投机执行等）属于未来方向，未在开源原型包中全部实现。

## X 长文核查位置与事实摘录

- **§1 Super-agent 定义与四个特征**：
  - 指出单任务能力受限于模型，而多任务并行受限于人的注意力（经验上一人同时只能盯 3–5 个活跃 session）。给本地单 session Agent 挂 CLI/MCP/外部连接器仍会因长操作阻塞、多任务上下文混杂、本机休眠断网而停摆。
  - 将脱离单次手动 session、跨会话保持上下文、并发推进多个复杂任务的智能体与系统架构称为 **Super-agent**，指出个人智能体（personal agents）与商业研发 Agent 在“常驻在线、并发响应环境事件”的约束下会收敛到相似设计。
  - 四个特征：**Continuous**（跨 IM、GitHub PR 评论等渠道保持同一 Agent 上下文连续）、**Productive**（并行推进多任务、前序命令未完即可接新指令）、**Proactive**（监听环境事件主动行动、无需处理时保持安静）、**Persistent**（常驻在线、直连真实工作环境、长程运行异常自愈）。
- **§2 Two-Level Architecture（两层架构）**：
  - 分析单 session（上下文连续但串行低吞吐、任务中间细节交错污染）与每事件开新 session（并发高但缺乏全局共享上下文、多会话分别回复用户造成混乱）的取舍。
  - **§2.1 Router Layer**：长生命周期全局路由层，承接所有人类交互、充当全局顺序点与协调记忆点；不亲自执行具体任务（可不挂 Bash 工具），通常可用较轻量的模型。采用单个长生命周期 LLM Session 时，上一轮推理期间到达的外部事件（Triggers）自动排队并在下一轮合并注入，利用 Prefill 阶段并行计算实现批处理（batching）。当单 Session 遇到吞吐上限时，可做多级过滤或水平分片（sharding），但分片越细共享上下文越少。
  - **§2.2 Worker Layer**：每个 Worker 拥有独立上下文与完整执行工具，专职单一任务，不直接与人交互，结果汇报给 Router 统一对外回复；Worker 内部可以是单会话、带子 Agent 或整个 Agent Team。
- **§3 Event-Driven Triggers（事件驱动触发）**：
  - **§3.1 Event Filtering**：借鉴计算机系统 Fast Path / Slow Path，先由确定性代码策略（Fast Path：按事件源、群组、用户/机器人白名单等规则设为“仅响应显式请求 / 作为候选事件 / 忽略”）过滤海量噪音，再由大模型语义策略（Slow Path：基于提示词判断候选事件是否行动）研判。
  - **§3.2 Event Routing（Subscription & Pass-through）**：同一 GitHub PR、IM 话题或邮件串的连续事件组成 **Thread**。Router 为 Thread 首个事件创建 Worker 后，Worker 直接订阅该 Thread；后续事件走代码直通（Subscribed Fast Path）送达 Worker，无需 Router 再次工具调用转发；超出任务范围时 Worker 可取消订阅或退回 Router。Thread 与 Worker 为多对多订阅，共享同一环境的多个 Worker 可通过收到相同 Thread 事件自行发现并消解冲突。
  - **§3.3 Context Organization（Inline & Spill 与 Chain of Recall）**：将上下文窗口视为缓存。**Inline** 按时空局部性直接注入当前对象 ID、摘要（如前 50 字符）、关联对象 ID 及相邻 IM/评论；**Spill** 对超长内容设上限截断并留读取指针。系统为 Trigger、Thread、Worker Session 分配唯一 ID 并内联下一跳关联 ID 形成引用图，使 Router 可按需多跳召回历史上下文（**Chain of Recall**）。
  - **§3.4 Acting Ahead（投机执行 Speculative Execution）**：根据环境信号在后台提前行动（如收到会议邀请邮件先查日历冲突并起草回复；研发群有人报 bug 时按“静默复现与修复”策略后台尝试复现和提 PR，确认简单可修才投递结果，否则全程静默）。
- **§4 Full-Duplex Multi-Channel Interaction（全双工多渠道交互）**：
  - **§4.1 Full-Duplex**：将耗时同步 `run()` 拆为异步 `start()`（立即返回 `"Started"`）和 `stop()`，后台工具完成后作为新事件消息送回会话，实现异步 ReAct 循环（文中注明 DeepSeek Harness 已实现该机制但默认未开启）。
  - **§4.2 Multi-Channel**：按渠道定制回复规范——IM 渠道保持轻量、仅在需决策或确认时通知（验证过的一条有效规则是单条回复不超过 100 词）；GitHub、邮件与文档等异步渠道输出高信息密度结构化内容。
- **§5 Separating Compute, State and Environments（计算、状态与环境两级解耦）**：
  - **§5.1 计算与状态分离**：Agent Loop 运行在无状态弹性云容器中，Session 状态存入数据库。
  - **§5.2 计算与执行环境分离**：对比 Anthropic《Decoupling the brain from the hands》（Managed Agents，侧重云端按需沙箱与客户 VPC），提出支持 **BYOM（Bring Your Own Machine）**——在用户日常使用的个人电脑或开发机上运行无状态轻量守护进程（daemon），仅负责执行命令和返回结果，保留本地未提交修改、内网服务依赖和凭据；设备间歇在线重连时云端 Agent 自动启动并完成待在该设备执行的任务。
- **§6 Watchdog（外部独立控制循环）**：
  - 针对进程未崩溃但模型陷入死循环或偏离目标的异常，在主系统之外运行由定时消息驱动的独立 **Watchdog Session**（自身也是带完整工具的 Agent 会话），监控基础设施故障与各 Worker 的实质进展，支持维护者用自然语言询问故障原因并在线增删提示词或调整触发规则。
- **§7 Preliminary Experiments（初步实验数据，文中注明使用合成负载与简化环境，结果仅供参考）**：
  - **§7.1 消融实验**：约 300 条群聊与 GitHub CI 消息（其中约 20 条工作请求），用耗时模拟工具代替实际编码，每种设计跑 5 次（消息间隔与工作时长按 1/4 缩放，模型调用时间不缩放）：
    - `Super-agent`：任务完成时间 p50 / p95 = **12.4 / 15.7 分钟**，每次运行总 cache-read tokens = **23.2M**。
    - `Super-agent without Pass-through`：p50 / p95 = **12.6 / 15.5 分钟**，总 cache-read tokens = **31.8M**（Router 决策次数增加约 30%，cache-read tokens 增加约 37%）。
    - `Single Session with Subagent tool, neutral prompt`：5 次运行均未调用 subagent，全部阻塞在主会话，p50 / p95 = **20.4 / 29.5 分钟**，总 cache-read tokens = **6.1M**。
    - `Single Session with Subagent tool, delegation prompt`：5 次中有 4 次委派、1 次自判任务小而亲自执行形成长尾，p50 / p95 = **13.8 / 29.0 分钟**，总 cache-read tokens = **10.8M**。
  - **§7.2 Router 层批处理压测**：Router 调真实模型、Worker 用 mock 模型，需决策的 Trigger 到达率从约 1/min 提升至约 40/min 时，平均批大小从 **1.0** 升至 **2.8**，单次请求耗时仅从 **2.5 s** 升至 **3.9 s**，单决策分摊推理耗时从 **6.4 s** 降至 **1.6 s**。
- **§8 Open Problems（四个尚未收敛的方向）**：
  - 8.1 两层架构的扩展边界（何时以及如何对 Router 分片、Worker 间直接通信拓扑、跨月度长期记忆瓶颈）；
  - 8.2 无 Session 界面的交互与半途人工介入（如何在后台自主执行中随时接管或协同）；
  - 8.3 上下文共享边界与跨实例 A2A（Agent-to-Agent，如个人 Agent 与团队共享 Super-agent 之间跨权限边界协作）；
  - 8.4 安全与隐私（事件驱动扩大不可信输入面；云端 Agent Loop 若被攻破或遭受提示词注入会波及所连 BYOM 终端；凭据一旦进入模型上下文即有泄露风险，需让 Agent“使用凭据但看不见凭据”）。

## 原型仓库 `dsh-superagent-prototype`（`8c32a9dc`）核查位置

- `README.md` 与 `docs/000-philosophy.md`：核心原则为“占用最少的人类注意力，交付最大的价值”；仅在被允许的人直接请求或匹配团队编写的规则时行动；未请求的主动工作默认处于只记录不接单的观察模式。
- `docs/001-domain.md`：定义核心领域模型 `Source → Trigger → Thread → Eval (Gate + Assessment) → Decision → Ticket (Mandate) → Assignment (Executor) → Channel`，以及多对多 `Subscription` 扇出（Fan-out）与只加不路由的 `Correlation`；明确列出被拒绝的设计概念（如不建跨 Source 统一人物实体、不让 Ticket 状态直接绑死底层 DSH Session、不在策略变更时强行取消运行中 Ticket）。
- `docs/002-authorization.md`：区分 `explicit`（显式请求）与 `inferred`（推断候选）两类强度；定义 `off`、`observe`（默认，评估后记为 `would accept` 的 ignore）、`auto` 三种接单模式；定义 `Mandate` 的不可变性、策略版本追踪与恢复前重校验（`revalidate`）；定义 Executor 将超范围跟进消息退回主会话的 `handback` 机制。
- `docs/003-execution.md`：
  - 每个 Ticket 分配独立 `worker-<ticket id>` 会话与工作目录（通常通过 `prepare` 命令创建 `git worktree`）；
  - `dsh-superagent-worker` 与 `dsh-superagent-router` 预设在前台 shell 命令运行满 **5 秒**后自动移入后台作业（background job），避免阻塞下一步消息接收；后台作业在每轮结束后最多运行 30 分钟（移交人工审阅的服务除外）；
  - 并发槽位（`WorkerSlots`）为人类消息或状态查询预留 1 个额外槽位，防止新任务占满槽位导致人无法继续已有工单；
  - 环境变量（如 `DSH_SUPERAGENT_DIR`、`DSH_SUPERAGENT_BLOCKED_COMMANDS`）不含凭据，Worker 通过已配置账号的 `gh` 和 `lark-cli` 访问外部服务。
- `docs/007-architecture.md`：
  - `Runtime`（`src/app/runtime.ts`）加目录锁并打开单一 SQLite `Store`（`src/app/store.ts`）；
  - `Engine`（`src/core/engine.ts`）由 `Intake`、`Evals`、`Tickets`、`Assignments`、`Replies` 五个内部部分组成，所有命令在单一事务内修改聚合根，并将外部副作用写入持久化队列 `Effects`（`src/app/effects.ts`，包含 `assessment`、`launch`、`delivery`、`relay`、`notice`、`reply` 六类任务，在 `afterCommit` 后按指数退避重试执行）。

## 验证记录

- 已通过 API 获取 X 长文完整结构化正文、配图说明与实验表格数据，并读取 `deepseek-ai/dsh-superagent-prototype`（`8c32a9dc5d72c033816c6a8110b37f40cf94fba4`）的 `README.md` 及 `docs/000-philosophy.md` 至 `docs/008-cookbook.md`。
- 本次未在本地安装 DeepSeek Harness 运行 `dsh-superagent-prototype`，未复现长文中的合成负载消融实验与批处理压测。
- 整理页：[[wiki/topics/ai/personal-agent|Personal Agent 与 Super-agent]]、[[wiki/syntheses/ai/always-on-and-super-agent-architecture|常驻型 Agent（Always-on / Super-agent）的系统架构]]。
