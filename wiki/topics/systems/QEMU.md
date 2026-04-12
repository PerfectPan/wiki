---
title: QEMU
type: topic
category: systems
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - qemu
source_refs:
  - raw/sources/QEMU.md
---
# QEMU

- qemu 提供了 monitor 选项能够观测当前模拟器的硬件行为，如果是 nographic 模式的话需要按下面步骤：
	- ```
	  -monitor telnet::45454,server,nowait -serial mon:stdio
	  ```
	- 另一个 shell 里起 [[Telnet]] 即可：`telnet localhost 45454`
	- 可以用 quit 命令去停止模拟
	- 直接 Ctrl + A 然后按 c 即可切换到 monitor，好像不用 monitor 选项，有时间看下为啥
- info mem 查看地址空间
- (Ctrl + A) + x 结束 qemu

## Source Pointers

- `raw/sources/QEMU.md`

