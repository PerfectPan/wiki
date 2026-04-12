---
title: 系统调用和 Shell
type: topic
category: systems
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - shell
source_refs:
  - raw/sources/系统调用和 Shell.md
---
# 系统调用和 Shell

- [[Shell]] 就是操作系统 Kernel 外面包的一层壳，把「用户指令翻译成系统调用」的编程语言
- Graphical Shell - GUI
- 如何翻译？
	- parse command 成一棵命令树，然后用类似[[表达式求值]]的方式去执行命令
	- TODO parse 部分阅读整理
	- pipe 的实现：syscall pipe 创建管道，有一个读口，有一个写口，然后进行 fork，子进程把 stdout 关闭了，再对写口进行 dup 的系统调用，dup 的系统调用是复制最小数字的文件描述符，因此就把 stdout 的文件描述符指向了写口，然后再把读口写口都关闭了，执行左边的命令，然后再 fork 一个，类似的，把 stdin 关闭了，再对读口进行 dup 的系统调用，把 stdin 的文件描述符指向了读口，再把这个进程的读口写口都关闭了，执行右边的命令，然后再主进程把两个口都关闭了，再等待两个子进程都结束，就完成了 pipe。
		- 管道是操作系统资源，fork 的时候不会复制一份，文件描述符是复制指针
- 研究方向：
	- fish / zsh
	- 自动修复 / StackOverflow
	- Command palette of VSCode
	- …
- [[终端]]是 UNIX 操作系统中一类非常特别的设备：[[tty]]
- Ctrl+C 能够退出是因为[[终端]]存在信号机制，如果[[进程]]没有注册 Ctrl + C 的 handler 那么在终端里执行 Ctrl + C 的时候，对应进程就会被 kill 掉
- [[Job Control]]: [[setpgid]]
- 一个功能完整的 Shell 使用的操作系统对象和 API
	- session, process group, controlling terminal
	- 文件描述符: open, close, pipe, dup, read, write
	- 状态机管理: fork, execve, exit, wait, signal, kill, setpgid, getpgid
	- …

## Source Pointers

- `raw/sources/系统调用和 Shell.md`

