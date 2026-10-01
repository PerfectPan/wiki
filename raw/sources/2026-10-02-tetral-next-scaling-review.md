# Tetral《The Next Scaling Problem》素材评审

基本信息：作者 Yang Li（Tetral 作者），发布 2026-09-06，抓取 2026-10-02。原文 https://tetral.ai/blog/the-next-scaling-problem/ ，正文已存 `raw/sources/2026-10-02-the-next-scaling-problem.md`。正文完整（58,682 bytes，reader 预抓落盘），开头含少量站内导航尾巴，引用标题时写《The Next Scaling Problem》。

定位：alpha 产品的架构宣言。描述的是作者声称的设计，不是已验证的生产系统。作者自己承认的局限（见文末）必须与机制描述分开表达。

## 文章在回答什么问题

把 agent 运行时从沙箱里拉出来之后，一个云 agent 系统怎么组织，才能让 agent 工作比任何单个进程或计算机活得更久？

## 演化动机（作者的两代产品经历）

- 第一代产品 Anoma：整个 agent loop 放进 E2B 沙箱，沙箱成为容量单位。结果要不断把职责搬出沙箱才能用：调试依赖能访问含私有用户数据的环境，API key 要单独网关代理，还要自己管沙箱 fleet 的供给、复用、回收。
- 第二代 Tetral 的判断：agent 是稳定的共享服务，容量可跨多项工作复用；沙箱 fleet 是隔离、突发、可弃的。两条 scaling 曲线不同，必须分离。沙箱变成与模型、内存、文件、凭证、工具并列的一种资源。
- 中间考虑过 Kubernetes（pod 不适合高频创建销毁的沙箱，Modal 后来也记录了同样的调度瓶颈）和 EC2+Firecracker 自建（等于做沙箱提供商）。

## Runtime 边界

判据：agent 的身份、状态、资源都放在进程外，运行时才是可替换的计算单元。每个有不同 owner、生命周期或 scaling 模式的职责都要移出。移出的五项职责：

1. Gateway：provider 格式、凭证、出站连接、流式协议；不保存会话状态，可独立扩缩。
2. Bridge + PostgreSQL：PostgreSQL 是唯一事实来源和事务权威；Bridge 拥有数据库协议，提交转移前检查 ownership 和顺序。与 Cursor 用 Temporal 重放工作流的恢复边界不同，Tetral 把恢复权威集中在 PostgreSQL。
3. Queue：排序、租约、重试、取消、死信。
4. Sandbox Service：计算机的激活、执行、替换。
5. Public API + Event Stream：都不在执行路径上。

核心概念定义：
- session：一项持续的 agent 工作，配置 agent 版本和所选资源。
- thread：session 内一条独立有序的执行路径，actor 式串行边界；session 以 root thread 开始，可为 subagent 开 child thread。
- reducer：纯函数，从已提交的输入和结果重建状态，返回下一个合法转移（调模型、路由工具调用、等待输入或结束），自身不做任何数据库或网络 I/O。

运行时 pod 只是可替换的计算宿主，可以热持有多个 session 和 thread，但不拥有它们；声明被接受前不能派发外部操作。

## Write-ahead execution（先写后执行）

- 解决的问题：pod 消失后，接替者无法从进程内存判断操作是没开始、进行中还是已完成；乱猜会漏做或重复外部副作用。
- 规则借自 WAL：授权一个操作的转移必须先提交，再派发。派发前向 Bridge 提交带稳定身份的不可变声明；Bridge 校验 ownership 和顺序后在一个事务里提交转移和回执；稳定身份是幂等键，重试返回已有回执，换内容复用同一身份会被拒绝。
- Bash 例子（必须保留）：输入先提交才进上下文；`span.model_request_start` 记录精确上下文边界；模型返回 Bash 调用后，Bridge 先提交 `agent.tool_use` 才能路由；Bridge 先在一个事务里登记 sandbox execution 和 Queue job；worker 执行命令并把原始结果存为已完成未消费；之后 Bridge 在另一个事务里追加 `agent.tool_result`、更新 `session_messages`、把沙箱结果标为已消费、记录幂等回执。
- 三表存储模型（源自 OpenCode v2 的事件表 + session 投影，扩展了排序和回执）：`session_events` 事件日志；`session_messages` 模型上下文投影（一条 assistant 消息在一次模型请求中累积文本、工具调用和结果）；`session_bridge_operations` 幂等回执。compaction 只决定下次模型请求加载什么，不删除更早的执行历史。
- 边界：协议不能让任意外部系统变成事务性的；它给每个副作用一个已提交的身份和 owner，让重试收敛到同一操作。开放请求期间 pod 丢失，请求记为 `runtime_pod_lost`，不恢复丢失的 provider 流。

## Durable delivery（可靠投递）

- outbox 式原子入队：一个 PostgreSQL 事务写输入事件 + 目标 thread 的 Inbox 记录 + 指向该记录的 Queue job。事务提交后 Public API 才返回 200，投递异步继续。
- Inbox 是接收侧记录：queued / delivering / accepted。`pg_notify` 只唤醒 Job Runner，不带内容、不持有投递状态；丢了由轮询兜底。
- 顺序：同一上下文的输入保序，后面的普通消息不能越过正在投递或重试的；session 级变更（如 interrupt）走单独通道。
- fencing：超时不能证明旧 runtime 停了；binding generation + pod UID 做 fencing token，只有 Kubernetes 确认绑定 pod 已消失，Bridge 才把已接受的投递退回 Queue。

## Calling the model / 凭证隔离

- 请求不带任何 API key 或 OAuth token；Gateway 验证 pod 的 K8s workload identity 和短期 Bridge token（证明它仍拥有该 session/thread）；被替换的 pod 无法再刷新 token。
- 凭证缺失、撤销、归档、不可解密一律拒绝，不静默回退；OAuth 刷新在 Gateway 边界锁行完成。明文凭证不进 runtime、Bridge、session log 或沙箱。
- MCP 工具同理：runtime 只拿到工具名、描述和 input schema，不拿服务器凭证；`agent.mcp_tool_use` 先提交，connector 注入凭证。

## Computers as resources

- 关键句（原样引用）："A computer should be something the agent calls, not somewhere the agent lives."
- 计算机按需懒分配，session 创建时不一定有沙箱。冷启动例子：execution #42 提交后 worker 发现计算机是冷的，把执行挂为 `waiting_activation`，激活完成后同一逻辑执行以新 generation 回到 Queue；并发调用共享同一激活。
- 现状：每个 session 懒分配一个 Daytona 计算机是当前实现，不是抽象本身；文件访问未来可用虚拟文件系统，小任务用轻量容器。

## 二维扩展与 subagent

- workspace（长生命周期资源）> session（独立任务）> thread（有序上下文和执行路径）。threads 共享 session 不共享上下文；sessions 共享 workspace 不共享执行历史。
- subagent 控制模型改编自 Codex 的 multi-agent 设计。`fork_turns`：none / all / 正整数（最近 N 轮），解析成 child 的精确不可变起始上下文。
- `spawn_agent` 先提交：一个事务建 child、存上下文和指令、写 Inbox、建投递 job，确认后才返回 child thread ID；重试同一调用返回同一 child。父子上下文独立，后续通信走有序输入（send_message、完成通知、wait_agent）。
- child thread 适合一个任务内的多条路径；实现、文档、审计、知识维护这类职责应该用独立 session（各自 root agent、上下文、版本、凭证、生命周期），从同一 workspace 选资源。

## 授权与审查分离（A separate decision）

- 区分：凭证隔离控制能否访问能力；授权决定某个 proposed action 能否使用它。这个决定在执行之前、在提议它的 agent 之外。
- `approve_for_me` 模式（review 模型灵感来自 Codex 的 auto approval reviewer）。流程：确定性 Tool Gate 首评 → 需要审查时 proposal 仍是 proposal（没有公开的 `agent.tool_use`、没有沙箱 job、没有外部副作用）→ review_id = H(workspace, session, thread, request, tool_call, tool, action, policy)，哈希绑定精确提案，改命令或策略即新 review → 审查者是内部 thread，输入是证据不是指令（防 prompt injection，平台策略与被审材料分离）→ 输出只有风险级别、上下文中的用户授权、allow/deny、理由；格式错即审查失败，不是许可 → 决定先提交 PostgreSQL 才返回 → Tool Gate 二评后才提交公开 `agent.tool_use`。
- 并行审查：热 reviewer thread 一次处理一个；重叠审查从其最新已提交状态复制临时 thread。
- 故意牺牲恢复性的边界：runtime 在 proposal 之后、授权完成前消失，请求以 `runtime_pod_lost` 关闭，proposal 既不重建也不执行——防止孤儿决定变成许可。
- 引用的例证：Claude Code auto mode（云边界统一策略）、OpenAI Hugging Face 事件（在行动 agent 内部识别风险不等于在其周围强制边界；作者同时声明这不意味着 LLM 审查者能防止该事件）。

## 下一阶段 scaling 问题（作者判断）

- 能力更强的模型给周围系统带来更多工作：更多 runtime 转移、测试、计算机、文件、网络请求、存储轨迹、外部副作用；最短的那个容量成为下一个瓶颈。
- 编译验证可能先于推理成为瓶颈：引用 Bun 迁 Rust（省内存、提吞吐）、TypeScript 原生 Go 端口（大约十倍速、显著省内存）；作者自己的开发服务器上单条集成路径 7-8 分钟，全量验证约半小时。
- 沙箱不该是所有操作的默认边界；actor 系统（可睡眠唤醒的轻量可寻址计算）是设计空间中的另一点，如何映射到 Tetral 的 session/thread 仍开放。
- 存储边界：一次性执行环境的产出必须比环境活得久；session 日志、代码、构建产物各归其位；PostgreSQL 和 Git 存储在 agent 规模下需要新的实现（引 OpenAI 的 PG 扩展、Cursor 的对象存储 WAL Git host）。
- 模型正被装进更大的交付单元：temperature/top_k/top_p 对新模型弃用，配置面转向 effort、tools、skills、MCP、context、policy、orchestration；被配置的产品越来越是包含模型的 agent 系统。

## Durable participant 与 Work that compounds（作者判断）

- 有可寻址身份的 agent 可以跨终端、浏览器、GitHub、团队产品延续；外部动作可追溯到 agent 版本、session、thread、policy 和 review。例证：RoboBun（GitHub 上的公开 agent 身份）、Raft（多 agent workspace）、Claude Tag（Slack 频道异步 Claude）。
- 授权委托的例证：Cloudflare+Stripe 的 agent 开户/买域名/部署；Stripe 商户和金额绑定的支付凭证（不接触卡号）。用户/组织仍是 principal。
- 计划中的 Code Mode（受 OpenCode codemode 启发）：受 confined JavaScript 程序发现并组合允许的 MCP 工具。CLI 留给计算机原生工作，MCP 成为云原生能力的首选接口。注意：是 planned。
- 协作立场：加人或加通信不自动改善协作（引 Anthropic 多 agent 研究：coordinated swarm 和独立并行 agent 每结果 token 相近，更大的共享编码 swarm 合并比例更低）。主张对抗式审查先于合并：其他 agent 主动挑战结论和证据，人类决定采纳；被接受的工作成为后续探索的基础，未检查的错误会传播。workspace 保存被接受的成果，session log 保存每个候选是怎么产生的。
- 轨迹可复用为评估和对齐数据（rejected tool calls、被推翻的审查、失败验证、人工纠正），前提是来源链存活、私有数据清除、人类判断成败。

## 作者承认的局限（必须单独成节，不得写成已验证能力）

个人 k3s 集群上的 alpha，不是生产级云；runtime 放置不感知容量；背压未把 admission、Queue 压力和扩缩连起来；多节点持续恢复未验证；发布时会中断进行中的 turn（没有优雅排水）。三项保留的 bet：agent 是云原生的；必须扩展的是 agent 系统而不仅是模型；runtime 让 agent 保持计算中心，周围系统保存连续性和控制。MIT 开源。

## 收录建议

- 一个来源的架构方法论提炼，建议新增一个 synthesis 页，不为 Tetral 单开 topic 页。
- 建议路径 `wiki/syntheses/ai/tetral-cloud-agent-runtime-architecture.md`，category ai，tags 建议 agent / cloud / runtime / scaling。
- 可在相关处链接 [[wiki/syntheses/ai/persistent-agent-harness-design-patterns|持久化 Agent Harness 的设计模式]]、[[wiki/syntheses/ai/agent-loop-control-boundaries|Agent 循环工作流的控制边界]]。
- 事实层（作者声称的机制）与作者判断（下一代瓶颈、协作立场）分开表达；第三方事实（Modal、Cursor、Anthropic 研究）保留原链接。
