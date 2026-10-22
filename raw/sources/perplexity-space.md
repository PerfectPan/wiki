# Perplexity SPACE：文档与源码阅读记录

- 访问日期：2026-10-21。
- 仓库：<https://github.com/perplexityai/SPACE>（git remote 已核对）。GitHub API（2026-10-22）：约 1.8k star，Apache-2.0，仓库创建于 2026-10-01。
- 固定提交：`57c7c0c47a73373a974c5b542d180599795465da`（2026-10-18 15:08 UTC，「Bind the last substrate literals and forbid new ones with archcheck (#611)」）。
- 规模：仓库内 `.rs` 文件共约 98.2 万行（`wc -l`，含测试）。
- 范围：读 README、`docs/architecture.md`、`docs/space/design/guest-io.md`、`docs/snapshot-upload-streaming.md`、`docs/base-snapshots.md`、`docs/installation.md`、`docs/configuration.md` 的相关段落，以及下列源码；没有部署，没有创建沙箱。

## 核查位置

- `docs/architecture.md`：核心概念表；API 把期望状态写进 PostgreSQL，控制器和工作节点服务调和；direct 与 Kubernetes 两种适配器（`crates/libs/api/src/controllers/substrate/direct.rs`、`kubernetes/mod.rs`）；Running / Paused / Suspended / Deleted 保留内容表；默认 6 小时无活动自动挂起；服务职责表写明「btrfs copy-on-write supports root filesystem creation」；管理 token 与数据面连接 token 不能互换；ECW 的 pause 对应 suspend。
- `docs/space/design/guest-io.md`：根盘是 ext4 镜像、virtio 块设备、`Unsafe` 缓存模式（客户机 `fsync` 只到宿主页缓存）；限速器默认 10,000 次/秒、100 MiB/s、突发 30 秒；上传新建或覆盖时写临时文件再改名、不 sync，追加和原地写在确认前 `fsync`；停止前 `syncfs`（30 秒预算），挂起和暂停前必须 flush，删除不 flush；读取按 64 KiB 分块、经 vsock；没有宿主级 I/O 总量限制。
- `docs/snapshot-upload-streaming.md`：`vol/mgr` 的 zstd 编码直接接对象存储的分块上传，每块 64 MiB、每个对象最多 16 个并发分块、默认 1 GiB 共享预算；LUKS 产物 `snapshot.luks`、`cow.luks`；`SPACE_SNAPSHOT_STREAM_BTRFS_SEND=true` 时挂起保留只读 btrfs 源，再流式 `btrfs send`。
- `crates/libs/node/runtime/core/src/fc_api.rs` 第 81–87 行：注释说明有意使用 Diff 快照加脏页追踪，`CREATE_SNAPSHOT_TYPE = "Diff"`、`LOAD_SNAPSHOT_TRACK_DIRTY_PAGES = true`。
- `crates/libs/node/runtime/supervisor/src/service.rs` 约第 624 行：`launch::launch_via_jailer(launch::JailerLaunch { jailer_bin, .. })`。
- `crates/libs/template/mgr/src/volume.rs` 约第 1431–1451 行（模板摘要目录建成 btrfs 子卷，失败时退回普通目录）、约第 1734–1790 行（`btrfs send -p` 需要只读父子卷；非 btrfs 宿主仍走 reflink 加 Full 编码的路径，只是没有 btrfs send）。
- `crates/libs/spaced/guest/server/src/run.rs`：vsock 监听。
- `crates/libs/api/src/fork_operations.rs`：`FORK_PATH_TEMPLATE = "/sandboxes/{sandboxID}/fork"`、`DEFAULT_FORK_COUNT = 1`、`DEFAULT_FORK_HARD_DEADLINE_SECONDS = 240`、`fork_restore_activation_lease_seconds`；`docs/configuration.md` 第 98–99 行 `SPACE_SANDBOX_FORK_ENABLED`（默认 on）。路由在 `crates/libs/api/src/routes/e2b/fork.rs` 与同名目录。
- `docs/installation.md` 第 13 行：Linux x86_64 + KVM，需要 `/dev/kvm`、`/dev/net/tun`、loop 设备、btrfs 支持和允许特权容器的 Docker。

## 验证记录

- 只读文档和关键路径源码，没有部署 Kind 集群、没有创建或挂起沙箱、没有测上传和恢复。
- fork 的内部流程（是否先快照再恢复成新 VM）只从函数名和常量推断，没有读完实现。
- jailer 的隔离手段（chroot、cgroup、命名空间、降权）来自 Firecracker 的通用文档，SPACE 传给 jailer 的具体参数没有逐项核对。
- 配图 `raw/assets/perplexity-space-architecture.png`（1386×869）：matplotlib `plt.xkcd()` 手绘风格，核对了 crate 路径、`Unsafe`、限速器数值、`Diff` 快照、zstd + LUKS、btrfs send -p。图中没有画整机 fork。
- 对比图 `raw/assets/agent-workspace-layer-comparison.png`（1386×869）中 SPACE「fork/快照粒度」一栏只写挂起，没写整机 fork，以 topic 页正文为准。
