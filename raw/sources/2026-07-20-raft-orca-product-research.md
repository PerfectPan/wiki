# Raft 与 Orca 产品调研：一手来源取证清单

抓取日期：2026-07-20（Asia/Shanghai）
用途：为 [[wiki/topics/product/Raft|Raft]]、[[wiki/topics/product/Orca|Orca]] 与 [[wiki/comparisons/product/Raft vs Orca：多 Agent 协作与本地执行|Raft vs Orca：多 Agent 协作与本地执行]] 提供可追溯的一手来源清单。

> 这是调研时的原始取证记录，不是对外部页面的完整镜像或逐字副本。网页和产品能力会变化；引用页面应以此处的抓取日期和链接为准，并在重新调研时追加新记录，而非覆盖本文件。

## Raft

| 来源 | 调研时可核验的观察 | 不应由此直接推断 |
| --- | --- | --- |
| [Raft 中文官网与 FAQ](https://raft.build/zh-cn/) | Raft 自称为多 Agent 协作平台；页面将频道、私信、线程、任务和 @mention 描述为人和 Agent 的共享工作空间，并列出 Claude、Codex、Hermes 等 runtime。 | 不能仅凭营销页面推断企业安全控制、SLA 或私有部署已经可用。 |
| [Computers](https://docs.raft.build/features/server/computers/) | Computer 是连接到 Server 的机器；Raft Computer 是本地服务，负责连接、Agent 生命周期和消息收发。Computer 可为笔记本、桌面机或云 VM。 | 本地运行不等于 Agent 自动获得最小权限或工作内容完全不出机器。 |
| [Runtime](https://docs.raft.build/features/agents/runtime/) | Runtime 在接入的 Computer 上运行，使用用户现有的模型订阅/API；Raft 不代理该 runtime 到模型供应商的调用。 | 不应把 Raft 当作模型供应商或 runtime 沙箱。 |
| [External Agents](https://docs.raft.build/features/agents/external/) | 外部 Agent 经 CLI、device authorization 与 `RAFT_PROFILE` 接入；接入后可收发消息、认领任务和协作；该能力标为 Experimental，活动状态可能不准确。 | 不能将外部 Agent 的在线状态作为任务已完成的审计证据。 |
| [隐私政策 §9、§16](https://raft.build/zh-cn/privacy/) | 政策称服务器在美国；本地 workspace、终端输出和文件读写不由 Botiverse 存储；明确发往频道、DM、workspace record 的消息、附件、任务和元数据会被存储处理。 | “本地 workspace 不存储”不代表运行活动、显式发送的内容或其他供应商模型请求不涉及数据处理。 |
| [定价页](https://raft.build/zh-cn/#pricing) | Enterprise 中的私有部署、SSO 和高级访问控制在当时标为“即将推出”。 | 不应把页面中的路线图当成交付承诺。 |

## Orca

| 来源 | 调研时可核验的观察 | 不应由此直接推断 |
| --- | --- | --- |
| [Orca Docs：What is Orca?](https://www.onorca.dev/docs) | Orca 是桌面 ADE；一个任务对应一个 Git worktree、Agent terminal 与 browser tab；其定位为运行多个 AI coding agent，而不是模型或 Git 替代品。 | 不应把 worktree 隔离等同于容器、OS、网络或凭据隔离。 |
| [Supported agents](https://www.onorca.dev/docs/agents/supported) | Orca 运行用户已有的 CLI Agent，支持 Codex、Claude Code 和可自定义的 CLI Agent；部分受支持 CLI 的启动参数与权限模式可由设置控制。 | Agent 的模型能力、成本和行为仍取决于 CLI、模型供应商和宿主环境。 |
| [Remote Orca Servers](https://www.onorca.dev/docs/remote-servers) | `orca serve` 可在另一台机器上运行 runtime；Server 拥有 repo、worktree、terminal 与 Agent processes，客户端连接并控制这些状态；该功能为 Beta，pairing URL 应视为 secret。 | 自管 runtime 不代表已经具备完整企业多租户、统一身份、审计或权限控制面。 |
| [Enterprise](https://www.onorca.dev/enterprise) | Orca 提供面向团队 rollout、批准的 Agent/集成和组织级默认配置的 Enterprise 沟通入口，并称可 self-host。 | 不能据此推断其具有 Raft 式频道、DM、任务认领或长期 Agent 身份等协作原语。 |
| [Privacy & Telemetry](https://www.onorca.dev/docs/telemetry) | packaged build 的匿名遥测可关闭；文档称不上传代码、路径、prompt、Agent/terminal 输出、repo/branch 名，仍会发送匿名本地 ID、版本、OS/CPU 与事件类别至美国区域 PostHog。 | 需在目标版本、网络策略和部署方式中实际验证；文档不替代企业 DPA 或网络审计。 |
| [LICENSE](https://github.com/stablyai/orca/blob/main/LICENSE) | 公开仓库使用 MIT License。 | 开源许可不自动涵盖第三方 Agent CLI、模型 API、插件或部署基础设施。 |

## 调研边界

- 未注册或安装 Raft、Orca，未提交表单、未连接远程 Server，也未用真实凭据做现场运行测试。
- 未对官网客户、团队、性能、价格或安全营销主张做独立第三方验证。
- 结论页应把“官方称”与基于这些事实得出的安全/选型推论区分开。
