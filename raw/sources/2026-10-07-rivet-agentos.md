# Rivet agentOS 文档核对

- 访问日期：2026-10-07。
- 输入：<https://rivet.dev/agentos/docs/>。
- 范围：官方文档阅读记录；未运行 SDK、故障恢复测试或隔离测试。
- 以下是改写后的事实笔记，不是原文快照；不保存导航和宣传指标。

## 核对位置

| 来源 | 位置 | 核对到的事实 |
| --- | --- | --- |
| [Architecture](https://rivet.dev/agentos/docs/architecture/) | The big picture / Anatomy of a Linux VM | client 配置 VM；sidecar 持有虚拟内核；executor 运行 guest；JS 使用 V8，shell/coreutils 使用 WASM。 |
| [Embedded quickstart](https://rivet.dev/agentos/docs/quickstart-embedded/) | Choosing between Actors and embedded | embedded 不依赖 Rivet Actors，身份、持久化和生命周期由应用管理；Actor 模式自动注入 SQLite。 |
| [Persistence & Sleep](https://rivet.dev/agentos/docs/persistence/) | What persists / Reading durable state after sleep | `/home/agentos`、会话目录和已完成历史保留；进程、shell、未完成流式增量和 VM 内 cron 定义不保留；唤醒创建新 VM，adapter 按需恢复。 |
| [Sessions & Persistence](https://rivet.dev/agentos/docs/architecture/sessions-persistence/) | Session event log / Trusted plaintext storage | 完整用户输入先提交再发送；已提交事件再发布；投递不确定的 prompt 不会自动重发；运行数据库可能明文保存环境变量、MCP 凭据和工具内容。 |
| [Security Model](https://rivet.dev/agentos/docs/security-model/) | Trust model / The security boundary | 安全边界是可信 sidecar 与不可信 executor；client 配置被视为可信输入；产品处于 beta，安全审查仍在进行。 |
| [Custom Host Functions](https://rivet.dev/agentos/docs/host-functions/) | Getting started / Security | Zod 输入定义生成 CLI 和 guest JS 调用入口；`execute()` 在宿主环境执行，需要宿主约束其权限。 |
| [Limitations](https://rivet.dev/agentos/docs/limitations/) | Software registry / Lightweight Linux kernel | 不支持任意 Linux 二进制、apt/yum、Docker、inotify/fs.watch 或 GPU；完整 Linux 工作负载需外部 sandbox。 |

## 判断与待验证项

文档描述的是运行环境与恢复能力，不能据此推断已实现长期知识提炼、过期事实纠正或跨 agent 语义召回。能写文件只提供了实现 memory 的存储条件。

采用前应在目标 adapter 上验证 sleep/wake、进程中断、权限请求恢复、prompt 投递不确定时的处理，以及外部 sandbox 挂载后的文件一致性。性能宣传和安全性均未独立复现。
