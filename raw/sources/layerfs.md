# LayerFS：源码阅读与运行记录

- 访问日期：2026-10-19 至 2026-10-21。
- 仓库：<https://github.com/Ephemeral-AI-Lab/layerfs>（`main` 克隆的 git remote 已核对）。GitHub API（2026-10-22）：约 1.5k star，MIT，仓库创建于 2026-08-10。
- 版本：
  - `v0.1.6` 源码包（无 git 元数据，`Cargo.toml` 的 `workspace.package.version = "0.1.6"`，`rust-version = "1.85"`）：本页实现细节的依据。
  - `main` 固定提交 `16e622e27278396c2cb822b0b0cc75ad03a7102c`（2026-10-17 20:58 +0800，「Merge dsh-demo-conversion: recorded runs as Live dsh demos (#347)」）：只看了 `core/crates/` 的划分和 `dsh/README.md`。
- 范围：顺着写入、提交、分叉的关键路径读代码，没有逐行通读；读了 `v0.1.6` 的 README、`explanation-zh.md`、`docs/versioned/0.1.6/quickstart.md`。

## 核查位置（v0.1.6）

- `crates/layerfs-layerstack-store/sql/schema/v10.sql`：`scope_allocator`、`object_packs`、`metadata_value_groups`、`objects`（`object_id` 32 字节，`canonical_length` ≤ 16777216）、`commits`（`commit_id` 33 字节，`root_id`、`parent_commit_id`、`base_layer_id`）、`branches`（`base_layer_id`、`head_commit_id`，名称只允许小写字母数字和 `._-`）、`layer_stacks`（`head_layer_id`）、`layers`、`workspace_stages`。
- `crates/layerfs-content/src/file/cdc/gear.rs` 第 7–11 行：`MINIMUM_CHUNK_BYTES = 8_192`、`TARGET_CHUNK_BYTES = 16_384`、`MAXIMUM_CHUNK_BYTES = 32_768`、`NORMALIZATION_SHIFT = 2`；第 262 行起是 `GEAR` 表。
- `crates/layerfs-content/src/object/digest.rs` 第 6–7 行：`OBJECT_DOMAIN = b"layerfs/object/v2\0"`、`CONTENT_DOMAIN = b"layerfs/content-bytes/v1\0"`，`blake3::Hasher` 先写域前缀。
- `crates/layerfs-layerstack-store/src/branch.rs` 第 9 行起 `fork_branch`：从 Layer 分叉时 `head_commit_id: None`；从 Commit 分叉时先 `branch_contains_commit` 校验。
- `crates/layerfs-layerstack-store/src/workspace.rs`：`prepare_reconciliation`（三方合并，约第 125–165 行）；`commit_reconciliation` 第 176 行比较 `head_commit_id` 与 `expected_head`，不符返回 `CommitHeadMoved`；`commit_candidate` 根与 Layer 都没变时返回 `UpToDate`，约第 300 行 `CommitId::derive(built.root_id, expected.head_commit_id, new_base_layer_id)`。
- `TransactionBehavior::Immediate` 出现在 `src/schema.rs`、`src/branch.rs`、`src/workspace.rs`。
- `crates/layerfs-workspace/src/container.rs` 第 111–114 行：`--device /dev/fuse`、`--cap-add SYS_ADMIN`；`docker.rs` 第 14 行检查 `test -c /dev/fuse`。
- `crates/layerfs-fuse/Cargo.toml`：`fuser = "=0.18.0"`。`src/local_spool.rs` 文件头注释：改动数据放在 `/snapshots/<workspace-id>/` 的分段文件，按约定可丢，从不 `fsync`，常驻缓存窗口有界并用 `POSIX_FADV_DONTNEED` 释放。`src/filesystem.rs` 的 `fsync` 回调转给 `port.fsync_async`。
- `crates/layerfs-sdk/src` 公开方法：`initialize_layerstack`、`fork_branch`、`create_workspace_session`、`exec_workspace_session`、`commit_workspace_session`、`end_workspace_session`、`add_layer`、`diff`、`analyze_dedup`、`workspace_conflicts`、`resolve_workspace_conflict` 等。
- README：Developer Preview 警告；「一个 `Client` 绑定一个 SQLite Store」；`end` 不会隐式提交；限制列表（无跨机同步、Workspace backing 不 fsync、0.1.6 与 0.1.5 组件不能混用、共享 `mmap` 脏页不被捕获、单构建线程导致 6 项测试慢 1.50–1.65 倍、`namespace-100000` 冷启动目标被豁免、存储未达 600 MB 目标、CLI JSON 不是稳定接口）；路线图 0.2.0 计划可移植投影，Later 阶段研究存储导出、导入和同步。
- `main`：`core/crates/` 共 13 个 crate（`layerfs-api`、`-bridge`、`-content`、`-daemon`、`-fuse`、`-history`、`-overlay`、`-persistence`、`-project`、`-sandbox`、`-storage`、`-telemetry`、`-workspace`）；`dsh/README.md` 描述 `dsh-layerfs` 插件包（宿主插件、客户端插件、agent 预设、mock 模型），写明不改 dsh 代码；`sdk/js` 目录存在。

## 运行记录

- 环境：另一个 bot 使用的 Linux 电脑，没有 Docker，因此只测了 `--projection materialize`，没有测容器 FUSE。
- 编译：`cargo build --locked --release -p layerfs-cli` 需要先装 `libsqlite3-dev`（快速上手文档没写），编译约 49 秒。
- 测试项目：`calc.py` 的 `add` 故意写成 `a - b`，加一个测试脚本。
- 结果：
  - 从 L0 分出 `try-a`、`try-b`，均立即完成。
  - `try-a`：Workspace 1 用 `sed` 修复后提交为 Commit 1；Workspace 2 跑测试输出 `TEST PASS`，提交为 Commit 2，父提交为 Commit 1。
  - `try-b`：改成 `a*b`，测试失败，`workspace end --discard` 后没有留下记录，Branch 头仍为空。
  - `layerstack add <try-a>` 生成 L1，`diff` 显示 `calc.py` 改动。
- 遇到的问题：`workspace end` 后立即创建新 Workspace 偶发 connection reset，等一两秒重试成功；CLI 把 stdout 打成字节数组；测试生成的 `__pycache__` 被提交；项目太小，`monitor analyze-dedup` 看不出节省量。
- 没有做的：容器 FUSE、多 Workspace 共享底座的空间测量、并发提交冲突、崩溃恢复、性能基准复现。

## 配图核对

- `raw/assets/layerfs-architecture.png`（1386×869）：matplotlib `plt.xkcd()` 手绘风格，逐项核对了 crate 名、`gear.rs` 的 8K/16K/32K、`digest.rs` 的 BLAKE3、`container.rs` 的 `/dev/fuse` 与 `SYS_ADMIN`、`v10.sql` 的表名、`TransactionBehavior::Immediate`、`expected_head` 冲突检查和 `UpToDate`。
- `raw/assets/layerfs-two-branch-bug-fix-flow.png`（1638×1027）：按「两个方案修同一个 bug」的示例流程画，是概念示意，不是实际运行截图；编号 ①–⑥ 与 topic 页的步骤对应。

## 同类方案的核实范围

- Turso AgentFS 的仓库 <https://github.com/tursodatabase/agentfs/> 与原理文章 <https://turso.tech/blog/agentfs-overlay> 在 2026-10 调研时打开核实过（`agentfs run claude`、SQLite + FUSE + 写时复制、TS / Python / Rust SDK）。
- topic 页同类方案表里 git worktree、Docker / OverlayFS、ZFS / Btrfs 快照、E2B / Modal 各行按一般了解写，没有逐项核实最新功能。
- 「为什么用 SQLite」「为什么先集成 DeepSeek Harness」是推断，README 没有给出原因。
