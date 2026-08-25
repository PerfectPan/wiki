# [Lv. MAX](/)
[← 返回](/)用 Claude Code 将三万行 Go 项目移植到 Rust：Agent Team 实践与 Harness 效率优化
2026-04-12 · 14 min
## [背景](#背景)
[mihomo](https://github.com/MetaCubeX/mihomo)（Clash Meta）是一个用 Go 编写的规则代理内核，支持 Shadowsocks、Trojan、VLESS 等多种协议，被广泛部署在路由器和 VPS 上。我决定用 Rust 重写它，不是出于 "用 Rust 重写一切" 的执念，而是有实际需求：更小的二进制体积、更低的内存占用、以及 Rust 类型系统在网络协议实现中带来的安全保障。
最终产物 [mihomo-rust](https://github.com/madeye/mihomo-rust) 包含 11 个 workspace crate、31,000+ 行 Rust 代码、40 份技术规格文档、2 份架构决策记录（ADR），以及覆盖单元测试、集成测试、端到端 TProxy 测试的完整 CI 管线。从第一个 commit 到 M1 里程碑基本完成，整个过程高度依赖 Claude Code 的 Agent Team 机制。
这篇文章不会说 "AI 好厉害"。它只记录实际工程中的做法：哪些有效，哪些踩坑，以及怎么调 harness 配置让 Claude Code 在大型项目里真正可用。
## [Agent Team：四个角色的分工](#agent-team四个角色的分工)
Claude Code 的 Agent Team 允许你在一个会话中运行多个专业化 agent，各自承担不同职责。在 mihomo-rust 项目中，我使用了四个角色：

| 角色 | 模型 | 职责 |
| --- | --- | --- |
| PM（项目经理） | Sonnet | 拥有路线图、排列优先级、撰写里程碑退出标准、维护 roadmap.md |
| Architect（架构师） | Opus | 编写差距分析报告、ADR、做架构决策、审查技术方案 |
| Engineer（工程师） | Sonnet | 实现代码、编写测试、处理 CI 修复 |
| QA | Haiku | 编写测试计划、审查测试覆盖率、维护 CI 状态报告 |

### [为什么这样分配模型](#为什么这样分配模型)
Opus 放在 Architect 角色上，因为架构决策需要最强的推理能力。比如决定 gRPC transport 是手写 "gun" 帧还是引入 tonic（最终选择手写，因为上游 Go 代码本身就没有 protobuf schema，引入 tonic 会增加约 30 个依赖和 2MB 二进制体积）。
Sonnet 用于 PM 和 Engineer，因为这两个角色的工作更偏向结构化执行：PM 按固定模板填充路线图表格，Engineer 按 spec 实现代码。Haiku 用于 QA。测试计划是高度模板化的工作，用最快最便宜的模型即可。
### [角色之间的信息流](#角色之间的信息流)
四个 agent 并不是各自为战。它们通过文件系统共享状态：

```
docs/vision.md ← PM 拥有，定义目标和非目标
docs/gap-analysis.md ← Architect 产出，PM 消费
docs/roadmap.md ← PM 拥有，引用 Architect 的分析
docs/adr/*.md ← Architect 拥有，不可协商的架构决策
docs/specs/*.md ← PM 拥有格式，Architect 审查技术内容
docs/specs/*-test-plan.md ← QA 产出
docs/ci-status.md ← QA 拥有

```
关键原则：**ADR 决定架构（不可协商），spec 填充细节（可讨论），测试计划验证 spec**。这种分层避免了 agent 之间的决策循环。
## [里程碑驱动的开发节奏](#里程碑驱动的开发节奏)
项目分为四个里程碑：
- M0（正确性修复）：10 个小项，修复安全漏洞、接线遗漏、CI 缺口。比如 REST API 的 Bearer 认证一直是 #[allow(dead_code)]，GEOIP 规则解析直接返回错误
- M1（用户可用）：协议、传输层、规则、DNS、API 的全面补齐
- M2（性能优化）：基准测试、分配器审计、feature flag 精简
- M3（运维成熟）：热重载、OpenTelemetry、配置校验
M0 和 M1 并行推进。M0 的项都是小范围修复，Engineer 可以在等待 M1 spec 评审时穿插完成。
### [一个具体的例子：Transport Layer 的开发过程](#一个具体的例子transport-layer-的开发过程)
Transport Layer（M1.A）是 M1 的前置依赖。VLESS 协议需要可复用的 TLS/WebSocket/gRPC 传输层，否则每个新协议都要复制粘贴 TLS 握手代码。
开发过程如下：
1. Architect 编写 ADR-0001，确定 mihomo-transport 作为独立 leaf crate，定义 Transport trait 接口，决定用 Box<dyn Stream> trait object 而非泛型（因为运行时需要根据 YAML 配置动态组合传输层链）
1. PM 将 ADR 翻译为路线图中的四个有序任务（A-1 到 A-4），标注依赖关系。"VMess 在 A-2 完成后解锁"
1. Engineer 按序实现：先建 crate 骨架和 TLS 层，迁移 Trojan；然后 WebSocket 层，迁移 v2ray-plugin；然后手写 gRPC gun 帧；最后 HTTP/2 和 HTTPUpgrade
1. QA 在每一步验证集成测试仍然通过：trojan_integration 和 v2ray_plugin_integration 不能因迁移而中断
这个流程看起来重：四个角色处理一个 crate 的创建。但正是这套结构保证了几件事：gRPC 没有引入不必要的依赖（Architect 决策）、构建顺序没有被打乱（PM 管控）、迁移过程中测试一直是绿的（QA 验证）。
## [CLAUDE.md：Harness 效率的核心杠杆](#claudemdharness-效率的核心杠杆)
CLAUDE.md 是 Claude Code 在每次会话开始时自动加载的指导文件。这是提高 harness 效率的关键：写得好，agent 不需要每次都重新探索项目结构。
mihomo-rust 的 CLAUDE.md 只有 101 行，但信息密度很高：

```
## Build Commands
cargo build --release
cargo test --lib
cargo test --test rules_test # 78 rule matching tests
cargo test --test trojan_integration # embedded mock server
cargo test --test shadowsocks_integration # requires ssserver

## Architecture
Listeners → Tunnel (routing) ←→ DNS Resolver
 |
 Rule Matching
 |
 Proxy Adapters / Groups → Remote Server

REST API (Axum) → Runtime control

## Key Patterns
- ProxyAdapter trait — all protocols implement this
- Rule trait — all rule types implement this
- Tunnel — Arc-shared routing engine

```
### [怎么写 CLAUDE.md](#怎么写-claudemd)
只写不能从代码推断的信息。** 不要列出每个文件的路径，agent 可以用 Glob 找到。要写的是：哪些 trait 是架构骨架、哪些测试需要外部依赖（ssserver）、构建命令有什么特殊参数。
写清楚扩展点。** "如何添加新协议" 和 "如何添加新规则类型" 各三行，告诉 agent 需要改哪三个文件。这比写一整段架构描述更有效，agent 需要的是 actionable 的指令。
不要写过时的信息。** CLAUDE.md 不是变更日志。如果某个决策已经落实到代码里（比如 fake-ip 已经被移除），就不需要在 CLAUDE.md 里再解释为什么移除。
## [Memory 系统：跨会话的经验积累](#memory-系统跨会话的经验积累)
Claude Code 的 Memory 系统允许在会话之间持久化信息。mihomo-rust 项目积累了 7 条 memory，全部是 `feedback` 类型，即对 agent 行为的纠正或确认。
几条有代表性的：
### ["不要在 router 上加 CatchPanic"](#不要在-router-上加-catchpanic)

```
prohibits adding CatchPanic or panic-absorbing middleware to axum router.
Task #26 requires panics in spawned tokio tasks to abort the process
so failures are detectable.

```
这条 memory 来自一次实际事件：Engineer agent 试图在 Axum router 上加 `tower::catch_panic` 来 "提高健壮性"。但 QA 的测试计划要求 panic 必须导致进程终止，soak test 才能检测到失败。保存这条 memory 后，后续会话中 Engineer 不再犯同样的错误。
### ["tokio::time::pause() 不虚拟化系统调用"](#tokiotimepause-不虚拟化系统调用)

```
tokio::time::pause()/advance() only affects sleep/Instant futures,
not kernel syscalls like TcpStream::peek(), read(), recv().

```
这条是 Engineer 在写 sniffer 测试时踩的坑。`tokio::time::pause()` 看起来可以用来加速超时测试，但它只影响 tokio 自己的定时器，不影响实际的 socket IO。这个知识点保存后，在后续编写 boring-tls 测试时直接规避了同样的陷阱。
### ["里程碑完成时必须重启所有 teammate"](#里程碑完成时必须重启所有-teammate)

```
Mandatory shutdown and respawn all four teammates at milestone completion.
Respawn with model assignment: architect=opus, pm/engineer=sonnet, qa=haiku.
Do not clear mid-milestone or if any state isn't saved.

```
这是最重要的一条操作规范。Agent Team 的上下文窗口有限。经历一整个里程碑的讨论后，上下文中堆满了过时的中间状态。在里程碑边界处 "重启" 所有 agent，让它们从干净的状态重新读取文件系统中的文档，比带着旧上下文继续工作更高效。
## [上游分歧策略：ADR-0002 的实践价值](#上游分歧策略adr-0002-的实践价值)
移植项目最棘手的问题之一是：上游的 bug 要不要复制？
ADR-0002 定义了一个简单的二分类法：
- Class A（安全/隐私/路由意图）：硬错误，拒绝加载。用户读配置文件时会误以为自己得到了 X，实际上得到的 Y 更不安全
- Class B（性能/兼容性）：警告一次，继续运行。流量到达正确目的地，只是走了更慢的路径
具体案例：

| 场景 | 上游行为 | mihomo-rust | 分类 |
| --- | --- | --- | --- |
| VMess cipher: zero | 接受，明文传输 | 解析时报错 | A |
| alterId > 0 | 运行废弃的 MD5 密钥推导 | 警告并强制为 0 | B |
| sniffer peek IO 错误 | 静默跳过 | 记日志，保留原始 metadata | A |
| default-nameserver 包含 tls:// | 接受，运行时 bootstrap 死循环 | 加载时报错 | A |

这个分类法的价值在于：它让 Engineer agent 在实现过程中遇到 spec 未预见的边界情况时，有一个明确的默认规则。"不确定时选 Class A（硬错误），在 PR 描述中标注"。这比每次都暂停来请求 Architect 决策高效得多。
对 QA 来说，测试用例中引用分歧分类（`Class A per ADR-0002: upstream accepts, we reject`）让审查者一眼就能判断测试的意图。
## [Spec 驱动开发：40 份文档的实际作用](#spec-驱动开发40-份文档的实际作用)
项目产出了 40 份 spec 文档和对应的测试计划。数量看起来多，但在 agent team 的协作模式下，spec 是协调四个 agent 的关键工具。
每份 spec 的固定结构：
1. YAML schema：配置文件中的字段定义
1. Struct shapes：Rust 结构体的字段和类型
1. Error types：所有错误情况的枚举
1. Divergences table：与上游的分歧，引用 ADR-0002 分类
1. Test plan：测试矩阵（独立文件）
spec 比直接告诉 Engineer "去实现 VLESS" 更高效，因为 spec 是 agent 之间的接口协议。Architect 在 spec 的 struct shapes 部分定义类型签名，Engineer 实现它们，QA 根据 spec 的 error types 生成测试用例。没有 spec，每个 agent 都要自己去读上游 Go 代码来理解应该怎么做，结果是三个 agent 对同一个问题产生三种理解。
一个具体的数字：transport-layer.md 这份 spec 覆盖了 M1.A 的全部四个子任务，因为 ADR-0001 已经确定了架构。spec 只需要填充 YAML schema、struct shapes 和 per-layer 测试，大约 200 行。而 Engineer 根据这 200 行 spec 产出了整个 `mihomo-transport` crate 的代码。
## [效率优化：踩过的坑和学到的经验](#效率优化踩过的坑和学到的经验)
### [1. 上下文窗口是最稀缺的资源](#_1-上下文窗口是最稀缺的资源)
Agent team 中每个 agent 都有独立的上下文窗口。长时间运行的会话会导致上下文被早期的探索、失败尝试和中间状态填满。解决方案：
- 在 CLAUDE.md 中写清楚关键信息，让 agent 不需要每次都重新探索
- 里程碑边界处重启所有 agent
- 用文件系统（docs/、specs/）而不是上下文窗口来传递状态
### [2. 文档是给 Agent 写的，不只是给人写的](#_2-文档是给-agent-写的不只是给人写的)
传统软件项目中，文档是写给下一个读代码的人看的。在 agent team 模式下，文档同时也是 agent 的 "system prompt"。它们通过读取 `docs/` 来理解项目状态和决策历史。
这意味着文档的写法需要调整：
- 用表格代替散文。 Agent 解析表格比理解段落高效
- 引用要精确。 "参见 ADR-0001" 比 "参见之前的架构讨论" 好，因为 agent 可以直接定位文件
- 状态要明确。 每个工作项标注 "completed / in-progress / blocked"，而不是 "我们之前讨论过这个"
### ************[3. Memory 要精简且可操作](#_3-memory-要精简且可操作)
Memory 系统的陷阱是存太多信息。mihomo-rust 只保存了 7 条 memory，全部是 feedback 类型，即 "不要做 X" 或 "做 Y 时注意 Z" 的规则。
不保存的东西：
- 代码模式和约定（从代码本身可以推断）
- Git 历史（git log 更权威）
- 调试方案（修复已经在代码里了）
- 临时任务状态（用 task 系统而非 memory）
### [4. 测试是验证 Agent 工作质量的唯一可靠手段](#_4-测试是验证-agent-工作质量的唯一可靠手段)
Agent 生成的代码看起来可能是正确的，但 "看起来正确" 不等于 "运行正确"。
mihomo-rust 的 CI 管线包含：
- 100+ 单元测试
- 82 个 API 集成测试
- 78 个规则匹配测试
- 5 个协议级集成测试（Trojan、Shadowsocks、v2ray-plugin、VLESS、boring-tls）
- Docker 化的 TProxy 端到端测试
- MSRV 校验（确保声称的最低 Rust 版本是真的）
每次 Engineer agent 提交代码后，跑完整测试套件是不可跳过的步骤。在 ECH/uTLS 的开发中，31 个测试用例（包括 C13-C15 的真实 BoringSSL 服务器端到端握手）是判断 "这个 feature 可以合并" 的唯一标准。
### [5. 让 Agent 管理自己的状态文档](#_5-让-agent-管理自己的状态文档)
ECH/uTLS feature 的开发展示了一种有效模式：PM agent 维护一份 `ech-utls-status.md`，记录 16 个 task 的状态、每个 task 的 owner、完成的 commit hash、以及关键决策（为什么选择 boring 而不是 rustls 做 ECH backend、为什么 `random` profile 在 `TlsLayer::new` 时解析而不是每次连接时）。
这份状态文档既是 agent 团队的协作界面，也是人类审查时的速查表。
## [数字与成本](#数字与成本)
一些客观数据：

| 指标 | 数值 |
| --- | --- |
| 总 Rust 代码量 | 31,178 行（117 个源文件） |
| Workspace crate 数 | 11 |
| 最大 crate | mihomo-proxy（9,797 行，27 文件） |
| Git commits | 106 |
| Claude 直接 commit | 10 |
| Spec 文档 | 40 份（最大 695 行） |
| ADR | 2 份 |
| 测试函数 | 619 个（408 同步 + 211 异步） |
| 集成测试套件 | 24 个 |
| CI jobs | 5（lint、test、tproxy、msrv、macos） |
| Cargo 依赖 | 375 个 |
| 开发跨度 | ~4 周（2026-02-21 至 2026-04-12） |
| 单日最高 commit | 27（2026-04-08，M0 sweep + 6 specs） |

Claude 直接 commit 只有 10 个（主要是 CI 修复和 simple-obfs 插件），并不意味着 Claude 只贡献了 10 个 commit 的工作量。大部分 commit 的作者是我，但代码是在 Claude Code 会话中协作完成的：我审查、修改、然后以自己的名义提交。Claude 的贡献更多体现在编写 spec、生成代码初稿、执行重构、维护文档。
## [总结：什么时候值得用 Agent Team](#总结什么时候值得用-agent-team)
Agent Team 不是万能方案。以下场景值得使用：
- 项目规模大到一个上下文窗口装不下。 mihomo-rust 有 11 个 crate、31K 行代码、40 份文档。单个 agent 无法同时 hold 住全局架构和局部实现细节
- 需要不同层次的决策。 架构决策（用不用 tonic）、项目管理决策（M1 先做什么）、实现决策（这个 struct 的字段类型）需要不同的思维模式
- 有明确的文档驱动流程。 Agent team 的协作基于文件系统。如果你的团队没有写 spec 的习惯，agent team 的效率会大打折扣
- 需要在里程碑之间保持一致性。 Memory 系统和文档保证了跨会话的知识不丢失
不值得使用的场景：
- 小型项目（< 5K 行），单个 agent 足够
- 探索性原型开发，结构化流程是负担
- 没有测试基础设施的项目。你无法验证 agent 产出的质量
Claude Code 解决的不是 "AI 能不能写代码"，而是 "AI 写的代码怎么工程化地验证和集成"。Agent Team + CLAUDE.md + Memory + Spec 驱动开发组成了一套完整的 harness，让 AI 辅助从 "试试看能不能跑" 变成可重复、可审查、可扩展的工程流程。
- 背景
- Agent Team：四个角色的分工
- 为什么这样分配模型
- 角色之间的信息流
- 里程碑驱动的开发节奏
- 一个具体的例子：Transport Layer 的开发过程
- CLAUDE.md：Harness 效率的核心杠杆
- 怎么写 CLAUDE.md
- Memory 系统：跨会话的经验积累
- "不要在 router 上加 CatchPanic"
- "tokio::time::pause() 不虚拟化系统调用"
- "里程碑完成时必须重启所有 teammate"
- 上游分歧策略：ADR-0002 的实践价值
- Spec 驱动开发：40 份文档的实际作用
- 效率优化：踩过的坑和学到的经验
- 1. 上下文窗口是最稀缺的资源
- 2. 文档是给 Agent 写的，不只是给人写的
- 3. Memory 要精简且可操作
- 4. 测试是验证 Agent 工作质量的唯一可靠手段
- 5. 让 Agent 管理自己的状态文档
- 数字与成本
- 总结：什么时候值得用 Agent Team
分享 right © 2026 by [Max Lv](//github.com/madeye)
