# Cloudflare Computer：源码阅读记录

- 访问日期：2026-10-21。
- 仓库：<https://github.com/cloudflare/computer>（git remote 已核对）。
- 固定提交：`7415a446b394a733b462917cc6660f2ebb2fd027`（2026-10-15 14:57 +0100，「computer: Keep long-running isolate JavaScript alive (#237)」）。此提交下各包 `package.json` 版本为 0.5.1。
- npm：`@cloudflare/computer` latest = 0.6.0，registry 记录的发布时间 2026-10-20T21:18:08Z（北京时间 10-21 05:18）；0.5.1 发布于 2026-10-13。0.6.0 的改动没有读。
- 官方文章：<https://blog.cloudflare.com/cloudflare-computer/>（2026-08-03）。
- GitHub API（2026-10-22）：约 9.7k star，MIT，仓库创建于 2026-06-05。
- 范围：读 README、`packages/computer/README.md`、`packages/computerd/README.md` 与下列源码；没有部署 Worker、Durable Object 或容器，没有运行测试。README 说明 `docs/` 是面向未来的规格，本次结论以源码为准。

## 核查位置

- `packages/dofs/src/schema/core.ts`：`SCHEMA_VERSION = 10`，`ROOT_INODE = 1`；`vfs_nodes`、`vfs_dirents`（`WITHOUT ROWID`，主键 `(parent_inode, name)`）、`vfs_blobs`、`vfs_blob_bytes`、`vfs_chunks`（`WITHOUT ROWID`，主键 `(inode, idx)`）及索引。文件头注释逐条记录了 v2–v10 每次升级的原因。
- `packages/dofs/src/schema/sync.ts`：`vfs_manifests`、`vfs_changes`（只有 `delete` 一种 op，带 `prior` 指纹）、`_vfs_watermark`（按 `(k, backend)`）、`_vfs_fetch_cursor`、`_vfs_push_cursor`、`_vfs_sync_operations`（`capturing` / `pending` / `failed` / `lost`，`mode` 为 `entries` / `pack`）、`_vfs_sync_skips`、`_vfs_mounts`。
- `packages/dofs/src/rev.ts`：`incrementRev()` 用 `UPDATE vfs_meta SET v = v + 1 WHERE k = 'rev' RETURNING v`，注释要求在 `transactionSync` 内调用。
- `packages/dofs/src/fs/writeFile.ts`：第 29 行 `CHUNK_SIZE = 512 * 1024`；`sha256()` 用 `node:crypto` 的 `createHash("sha256")`（约第 135–143 行）；约第 405–417 行校验除最后一块外每块必须满 512 KiB。
- `packages/rpc/src/interface.ts`：`SyncRPC`（`push`、`fetchChanges`、`watermarks`、`readEntry`、`hasObjects`、`fetchObjects`、`pushObjects`）、`ShellRPC`、`WorkspaceRPC`。
- `packages/rpc/src/sync-driver.ts`：`pullOnce`、`pushOnce`、`tick()`（先拉后推，注释说明回环抑制）、`reconcileWatermarks()`（注释说明容器重启清空内存库时需要重置游标）。
- `packages/rpc/src/sync-engine.ts`：文件头注释说明每次 `next()` 只完成一个块，游标和操作行持久化，DO 被驱逐后可以从持久状态恢复。
- `packages/computer/src/workspace.ts`：`#pushForExec` / `#pushForExecDefault`（约第 1215–1255 行，命令前 `pushOnce`）、`#pullForExec` / `#pullResolved`（约第 713–735、1211 行，命令后 `pullOnce`），`handle.sync === "none"` 时跳过。
- `packages/computer/src/backends/worker-shell/worker-shell.ts`：文件头注释说明 `env.LOADER`、`WorkspaceServiceProxy`、`env.HOST.getWorkspace()`、`ShellWorker` 入口与 `sync: "none"`。
- `packages/computerd/src/cli/computerd.ts`：`/api` capnweb 端点；约第 671 行读 `COMPUTERD_DB`。
- `packages/computerd/src/fuse/store.ts`：`COMPUTERD_DB` 为空或 `memory` 时用内存，绝对路径时落盘。
- `packages/computerd/src/fuse/driver.ts`：`MAX_FILE_BYTES = 256 * 1024 * 1024`。
- `packages/computerd/src/fuse/passthrough.ts`：注释说明 `fuse-native` 绑定 libfuse 2.9，不是内核 `FOPEN_PASSTHROUGH`；忽略路径用 `pwrite` 直写宿主盘，跳过 VFS、SQLite、变更包和拉取。
- `packages/computerd/README.md` 第 126 行起：`MOUNT_IGNORE`、`MOUNT_IGNORE_PATH`。
- `packages/computer/README.md` 状态表与后端表：Stable / Experimental / Deprecated 的划分，`scheduling_policy: "durable_object"`，Worker shell 需要 `experimental` 标志。
- 在 `packages/computer/src` 检索 `fork|snapshot`（排除测试）：命中 `runtime/runtime.ts`、`stub.ts` 的「客户端创建时快照后端信息」注释，以及容器生命周期文件里的快照恢复字段，没有工作区分叉或快照 API。

## 验证记录

- 只读源码和 README，没有运行。同步时机、重连对账、断点续传均来自代码与注释，没有在真实 DO 或容器上验证。
- 配图 `raw/assets/cloudflare-computer-architecture.png`（1386×869）由另一个 bot 在 2026-10 用 matplotlib 的 `plt.xkcd()` 手绘风格绘制（字体 Noto Sans CJK SC），本次逐项核对了框内的文件名、表名、`CHUNK_SIZE`、SHA-256、`pushOnce` / `pullOnce`、`_vfs_sync_operations`、`passthrough.ts` 与上述源码一致。
