---
title: 文件系统 API
type: topic
category: systems
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - api
source_refs:
  - raw/sources/文件系统 API.md
---
# 文件系统 API

- 让所有应用都共享硬盘不是一个很好的设计，相当于一张白纸给全班人去写，有个人一不小心写错了就把别人的写覆盖了
- 文件系统：设计目标
	- 提供合理的 API 使多个应用程序能够共享数据
	- 提供一个的隔离，使恶意/出错程序的伤害不能任意扩大
- 存储设备（字节序列）的虚拟化
	- 磁盘（I/O 设备）= 一个可以读/写的字节序列
	- 虚拟磁盘（文件）= 一个可以读/写的动态字节序列
		- 命名管理
			- 虚拟磁盘的名称、检索和便利
		- 数据管理
			- std:vector<char>(随机读写/resize)
- [[UNIX]]允许任意目录挂载一个设备代表的目录树
	- 可以把设备挂载到任何想要的位置
	- Linux 安装时的 mount point
		- /，/home，/var 可以是独立的磁盘设备
- Linux mount 工具可以自动检测文件系统
- 目录管理：创建 / 删除 / 遍历
	- mkdir
	- rmdir
	- getdents
- 硬链接允许一个文件被多个目录引用，目录仅存储指向文件数据的指针，不允许链接不存在的文件
- 软连接是在文件里存储一个「跳转提示」
	- 可以跨文件、可以链接目录
	- 指向位置当前不存在也没关系
- 进程的当前目录：pwd，如果你在 shell 里执行了一堆命令改路径啥的，但是最后回来 pwd 还是没有变
	- chdir 系统调用修改
-

## Source Pointers

- `raw/sources/文件系统 API.md`

