---
title: FAT 和 UNIX 文件系统
type: topic
category: systems
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - fat
  - unix
source_refs:
  - raw/sources/FAT 和 UNIX 文件系统.md
---
# FAT 和 UNIX 文件系统

- 数据结构课的假设：
	- 冯诺依曼计算机
	- Random Access Memory（RAM）
		- Word Addressing（例如 32 / 64 bit load / store）
		- 每条指令执行的代价是 O(1)
			- Memory Hierarchy 在苦苦支撑这个假设（cache-unfriendly 代码也会引起性能问题）
- 文件系统的假设：按块（例如 4KB）访问，在磁盘上构建 RAM 模型完全不切实际
- FAT
	- 性能
		- 小文件合适，大文件随机访问不行，4GB 的文件跳到末尾(4KB cluster)有 $2^{20}$ 次链表 next 的操作，缓存能部分解决这个问题
		- 在 FAT 时代，磁盘连续访问性能更加，但使用时间久的磁盘会产生碎片
	- 可靠性
		- 维护若干个 FAT 的副本防止元数据损坏
			- 额外的同步开销
		- 损坏的 cluster 在 FAT 中标记
- ext/UNIX 文件系统
- 文件系统的实现：
	- 自底向上实现数据结构
	- balloc / bfree
	- FAT / inside / …
	- 文件和目录文件
-

## Source Pointers

- `raw/sources/FAT 和 UNIX 文件系统.md`
