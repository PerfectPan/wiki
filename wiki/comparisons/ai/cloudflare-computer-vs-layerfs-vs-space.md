---
title: Cloudflare Computer vs LayerFS vs Perplexity SPACE
description: 三个 agent 执行环境到底各管哪一层：SPACE 管整台 microVM，Cloudflare Computer 管一个可换运行时的持久工作区，LayerFS 管可大量分叉的文件历史；按隔离、存储、分块、分叉、持久性和成熟度对比，最后按需求给选择
type: comparison
category: ai
created: 2026-10-22
updated: 2026-10-22
timestamp: 2026-10-22
tags:
  - agent
  - sandbox
  - filesystem
  - microvm
source_refs:
  - wiki/topics/ai/cloudflare-computer.md
  - wiki/topics/ai/layerfs.md
  - wiki/topics/ai/perplexity-space.md
  - raw/sources/cloudflare-computer.md
  - raw/sources/layerfs.md
  - raw/sources/perplexity-space.md
resource:
  - wiki/topics/ai/cloudflare-computer.md
  - wiki/topics/ai/layerfs.md
  - wiki/topics/ai/perplexity-space.md
  - raw/sources/cloudflare-computer.md
  - raw/sources/layerfs.md
  - raw/sources/perplexity-space.md
---
# Cloudflare Computer vs LayerFS vs Perplexity SPACE

## 一段话结论

这三个不是同一层的东西：[[wiki/topics/ai/perplexity-space|SPACE]] 管整台机器，每个沙箱一台 Firecracker microVM；[[wiki/topics/ai/cloudflare-computer|Cloudflare Computer]] 管一个一直在的工作区，运行时可以换；[[wiki/topics/ai/layerfs|LayerFS]] 管文件历史，能大量分叉、随时回退。跑不可信代码选 SPACE，在 Cloudflare 上要长期工作区选 Cloudflare Computer，要大量分叉试错看 LayerFS（还是开发预览版），少量并行只改源码用 git worktree。三者能叠：外面 SPACE 或 Cloudflare Computer，里面 LayerFS 管文件（按职责推的，没见过实际这么用的项目）。

![米色底手绘风格示意图：上中下三层，机器层是 Perplexity SPACE，工作区层是 Cloudflare Computer，文件历史层是 LayerFS；右侧说明三者可以叠着用](../../../raw/assets/agent-workspace-layers.png)

## 对比表

| | Perplexity SPACE | Cloudflare Computer | LayerFS |
| --- | --- | --- | --- |
| 管哪一层 | 整台 microVM | 持久工作区（一个虚拟文件系统） | 文件历史（Layer / Branch / Commit） |
| 隔离 | Firecracker + jailer，KVM | V8 isolate（Worker）或容器内 FUSE | 容器内 FUSE，或物化成普通目录 |
| 文件存哪 | 宿主上的 ext4 镜像（btrfs 子卷），快照传 S3 | Durable Object 的 SQLite | 单个 SQLite |
| 分块 / 哈希 | 块设备，不做内容寻址 | 固定 512 KiB，SHA-256 | FastCDC 8/16/32 KiB，BLAKE3 |
| 分叉 / 快照 | 整台挂起（内存差量 + 磁盘）、整机 fork | 没有，按 `rev` 增量同步 | 每次工具调用一个 Commit，零拷贝分叉 |
| 去重 | btrfs 写时复制，相对模板 `btrfs send -p` | 同一工作区内按哈希共享块 | 跨分支块级 |
| 多机 | 支持（Kubernetes 或 direct 适配器） | Cloudflare 全球网络，一个工作区一个 DO | 只能单机 |
| 什么时候算落盘 | 挂起、停止、快照时；客户机 `fsync` 只到宿主页缓存 | 写进 DO 就算；容器里的改动要等命令结束拉回 DO | 提交时；Workspace 改动不 `fsync`，不保证断电安全 |
| 成熟度 | 刚开源；`57c7c0c`（2026-10-18），Rust，Apache-2.0 | 核心 Stable，容器后端和同步协议 Experimental；`7415a44`（0.5.1，npm 已到 0.6.0），TS，MIT | `v0.1.6` 开发预览，`main` 在重写；Rust，MIT |

![手绘对比表：LayerFS、SPACE、Cloudflare Computer 在管理层次、隔离方式、存储、分块哈希、分叉粒度、去重、分布式、成熟度和适用场景上的差异](../../../raw/assets/agent-workspace-layer-comparison.png)

## 怎么选

- **跑不可信代码，要完整 Linux 和网络，自己部署**：SPACE。要 KVM、btrfs、特权宿主，还得运维 PostgreSQL + 控制器 + 节点服务。
- **E2B 代码想换自托管**：SPACE 的兼容层 ECW（兼容 E2B Python SDK；ECW 的 pause 即 SPACE 的 suspend）。
- **在 Cloudflare 上给每个用户或会话一个长期工作区**：Cloudflare Computer。绑定 Cloudflare，容器后端还是实验性的。
- **主要读写文件、跑 JS，不想起容器**：Cloudflare Computer 的 Worker 后端，直接经 Workers RPC 读写 DO。just-bash 不是真 bash，跑不了任意二进制。
- **MCTS、RL rollout 这类大量分叉、随时回退**：LayerFS。只能单机，不保证断电安全，调度层要自己接。
- **少量并行、只改源码**：git worktree。依赖要重装，只管 Git 跟踪的文件。

只读了文档和关键源码，只跑过 LayerFS 的物化模式（[[wiki/topics/ai/layerfs#实际运行结果|运行结果]]），没测性能。

## 名词

- **microVM / Firecracker**：精简的虚拟机，隔离边界是虚拟机而不是进程。
- **KVM**：Linux 的硬件虚拟化接口，SPACE 要求宿主有 `/dev/kvm`。
- **V8 isolate**：V8 里独立的 JS 运行时，有自己的堆，彼此拿不到对象引用。
- **容器**：用 namespace 和 cgroup 隔出来的进程，和宿主共享内核。
- **FUSE**：用户态文件系统，要 `/dev/fuse` 和 `SYS_ADMIN` 这类特权。
- **内容寻址分块**：用块内容的哈希当名字，相同的块只存一份。固定大小分块在中间插几个字节，后面的块全变；CDC 按内容找切点，只影响附近一两块。
- **零拷贝分叉**：LayerFS 分叉只加一行 Branch 记录，不复制文件数据。
- **写时复制（CoW）**：先共用一份数据，谁写谁复制改动的部分。
- **Durable Object（DO）**：Cloudflare 的单实例有状态对象，自带 SQLite，离开 Cloudflare 用不了。
- **fsync**：等数据真正落盘再返回；不调用，断电可能丢。

## 来源指针

- [[wiki/topics/ai/cloudflare-computer|Cloudflare Computer]]、[[wiki/topics/ai/layerfs|LayerFS]]、[[wiki/topics/ai/perplexity-space|Perplexity SPACE]]：各自的实现细节和源码位置
- `raw/sources/cloudflare-computer.md`、`raw/sources/layerfs.md`、`raw/sources/perplexity-space.md`：阅读范围、核查位置与验证记录
- [cloudflare/computer](https://github.com/cloudflare/computer)、[Ephemeral-AI-Lab/layerfs](https://github.com/Ephemeral-AI-Lab/layerfs)、[perplexityai/SPACE](https://github.com/perplexityai/SPACE)
- `raw/assets/agent-workspace-layers.png`：脚本（matplotlib）画的米色底手绘风格分层示意，不是各项目的官方素材
- `raw/assets/agent-workspace-layer-comparison.png`：按三页内容画的手绘风格对比表。图中 SPACE 的「fork/快照粒度」一栏只写了挂起，没写整机 fork，以本页表格为准
