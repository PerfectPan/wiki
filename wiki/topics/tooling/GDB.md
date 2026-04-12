---
title: GDB
type: topic
category: tooling
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - gdb
source_refs:
  - raw/sources/GDB.md
---
# GDB

- starti - 开始执行程序，在第一条指令处会停下来
- info inferiors - 列出进程的信息
- layout asm - 展示汇编语言
	- 退出：Ctrl - X + A
- si - 执行下一条指令
- info registers - 查看寄存器
- info inferiors  - 打印进程/线程信息
- bt f - backtrace full 打印堆栈信息
- l - 展示当前运行的代码
- c - continue 继续执行
- b _start - 在 _start 处设置断点
- run(r) args - 运行并带有 args 参数
- watch *0x7c00 - 在硬件的这个地址上打上一个断点，如果这个地址上的值发生改变则程序执行停止
- ctrl + D - 退出程序
- set print pretty 1
- 其他工具：
	- https://sourceware.org/gdb/onlinedocs/gdb/Python.html#Python
	- https://www.gdbgui.com/
	- https://wizardforcel.gitbooks.io/100-gdb-tips/content/print-STL-container.html

## Source Pointers

- `raw/sources/GDB.md`

