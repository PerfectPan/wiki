# Quotio 源码核查记录

- 来源：https://www.quotio.dev/；https://github.com/nguyenphutrong/quotio
- 访问日期：2026-10-07
- 源码提交：`71f427f7488e592406104d98936ff142000383d7`（当日默认分支快照，不等同于已发布安装包）
- 范围：macOS 额度界面到 Rust 后端、Claude / Codex / Antigravity 采集、数据模型、缓存和凭据边界。

## 证据矩阵

| 结论 | 固定版本位置 | 观察事实 | 置信度或限制 |
| --- | --- | --- | --- |
| macOS 使用本机 Rust 后端 | [CompositionRoot.swift](https://github.com/nguyenphutrong/quotio/blob/71f427f7488e592406104d98936ff142000383d7/apps/macos/Quotio/App/CompositionRoot.swift#L85-L110) | 创建 QuotioCLIBackend 与 QuotioCLIServerProcess | 已读装配，未启动应用 |
| 本机端口与认证 | [QuotioCLIServerProcess.swift](https://github.com/nguyenphutrong/quotio/blob/71f427f7488e592406104d98936ff142000383d7/Packages/QuotioCore/Sources/QuotioInfrastructure/QuotioCLI/QuotioCLIServerProcess.swift#L80-L173) | 启动 serve --manage --listen 127.0.0.1:0，生成 token 并经父子进程管道初始化 | 仅对应当前 macOS 本机路径 |
| 界面刷新与状态读取 | [QuotioCLIBackend.swift](https://github.com/nguyenphutrong/quotio/blob/71f427f7488e592406104d98936ff142000383d7/Packages/QuotioCore/Sources/QuotioInfrastructure/QuotioCLI/QuotioCLIBackend.swift#L486-L565) | POST v2/refresh，轮询 v2/operations，再 loadSnapshot | 已读调用链，未运行 |
| 界面三秒读取不等于上游三秒采集 | [QuotaFeatureController.swift](https://github.com/nguyenphutrong/quotio/blob/71f427f7488e592406104d98936ff142000383d7/Packages/QuotioCore/Sources/QuotioPresentation/Quota/QuotaFeatureController.swift#L309-L320) | startObservingHost 每三秒 bootstrap；后端另有调度 | 与 schedule 条目一起核对 |
| 后端独立定时刷新 | [server.rs](https://github.com/nguyenphutrong/quotio/blob/71f427f7488e592406104d98936ff142000383d7/apps/cli/src/server.rs#L1137-L1172) | 恢复缓存，按 refresh_interval 决定是否刷新并等待下一轮 | 配置为零时不定时采集 |
| Claude 额度取自 OAuth usage | [oauth_primary.rs](https://github.com/nguyenphutrong/quotio/blob/71f427f7488e592406104d98936ff142000383d7/apps/cli/src/providers/catalog/oauth_primary.rs#L294-L423) | claude_window / claude_windows / fetch_claude_at 解析 utilization、resets_at | 未请求线上接口；凭据读取另见同文件 246–283 行 |
| Codex 本机协议读限额 | [codex.rs](https://github.com/nguyenphutrong/quotio/blob/71f427f7488e592406104d98936ff142000383d7/apps/cli/src/providers/codex.rs#L258-L408) | connect 启动 app-server；fetch 使用 account/rateLimits/read 并核对前后身份 | 与 OAuth HTTP 路径分开记录 |
| Codex HTTP 读限额 | [codex_api.rs](https://github.com/nguyenphutrong/quotio/blob/71f427f7488e592406104d98936ff142000383d7/apps/cli/src/providers/codex_api.rs#L1-L207) | translated_window / parse / fetch_at 转换 used_percent 与时间窗口 | credits 作为独立指标 |
| Antigravity 回退有条件 | [antigravity.rs](https://github.com/nguyenphutrong/quotio/blob/71f427f7488e592406104d98936ff142000383d7/apps/cli/src/providers/antigravity.rs#L374-L479) | 先 summary，再按错误类型进入模型或 quota 接口 | 未验证所有账号类型 |
| 额度状态与窗口独立 | [domain.rs](https://github.com/nguyenphutrong/quotio/blob/71f427f7488e592406104d98936ff142000383d7/apps/cli/src/domain.rs#L40-L153) | Quota::from_used/from_remaining，QuotaWindow 的单位、来源与 fetched_at | 核心类型支持 Unknown；各解析器也可能省略缺失窗口或返回错误 |
| 账号隔离与失败保留 | [cache.rs](https://github.com/nguyenphutrong/quotio/blob/71f427f7488e592406104d98936ff142000383d7/apps/cli/src/cache.rs#L196-L391) | one 在前后核对身份；失败可返回旧窗口并记录 last_failure | 不能声称失败后所有账号一律保留缓存 |
| 旧值显式标记 stale | [snapshot.rs](https://github.com/nguyenphutrong/quotio/blob/71f427f7488e592406104d98936ff142000383d7/apps/cli/src/contract/snapshot.rs#L273-L377) | observation 根据 failure、fetched_at 与 TTL 设置 freshness | 不代表服务商数据实时更新 |
| 凭据存储因平台而异 | [vault.rs](https://github.com/nguyenphutrong/quotio/blob/71f427f7488e592406104d98936ff142000383d7/apps/cli/src/accounts/vault.rs#L269-L323) | system_with_mode 在 macOS 选择 Keychain，在 Linux 选择 EncryptedFile | 只读存储选择，未进行安全审计 |
| 新增服务商的实现接口 | [mod.rs](https://github.com/nguyenphutrong/quotio/blob/71f427f7488e592406104d98936ff142000383d7/apps/cli/src/providers/mod.rs#L62-L88) | ProviderAdapter 包含 fetch、cache_identity 和 cacheable | 仍需配合目录注册和账号支持 |
| 缓存恢复测试存在 | [cache.rs](https://github.com/nguyenphutrong/quotio/blob/71f427f7488e592406104d98936ff142000383d7/apps/cli/tests/cache.rs#L171-L225) | 恢复已缓存的健康、过期、失败账号，并验证重试 | 已读测试代码，未测试 |
| 快照语义测试存在 | [contract.rs](https://github.com/nguyenphutrong/quotio/blob/71f427f7488e592406104d98936ff142000383d7/apps/cli/tests/contract.rs#L257-L343) | snapshot_selects_healthy_sources_and_preserves_quota_semantics | 已读测试代码，未测试 |

## 未测试项

本次未安装或运行 macOS 应用、Rust CLI 或上游测试，未读取本机账号凭据，未请求真实额度接口，也未验证服务商线上接口是否仍接受源码中的请求。远程共享、代理路由、自动切换和计费对账不在本次核查范围。
