---
title: Makefile
type: topic
category: tooling
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - makefile
source_refs:
  - raw/sources/Makefile.md
---
# Makefile

- 一行行执行，主要是一个构建工具
- 理论上可以编译任何项目，可以利用这个自己搭建一个工作流，但是实际上用得最多的还是 C / C++ 项目
- ```Makefile
  targets: prerequisites
    # 任意 shell 命令，可以有多条，如果 @ 开头，实际执行的时候不会打印这行命令
    # 每一行的命令是在一个单独的子 shell 进程中执行的
    command
  ```
- 伪目标，make 执行的时候目标都是会生成一个 targets，如果有时候我们只想执行一些自动化的动作，比如清理中间产物，那就可以用这个语法，它会无视本地项目里是否有这个 targets
	- ```makefile
	  .PHONY: clean
	  clean:
	  	rm -rf *.o test
	  ```
- make -nB 只输出执行的命令，不会实际执行
- 一般来说 make xxx 会让 make 命令去找文件里的 xxx 目标然后执行，如果没有输入这个参数的话会执行解析下来的第一个 targets，如果有多个相同的会合并
- make 命令工作流程：
	- 首先会在当前目录下面寻找 Makefile 文件
	- 寻找到 Makefile 文件之后，他会在文件当中寻找到一个编译目标
	- 然后 Make 会解析编译目标的依赖，如果这个依赖是其他的编译目标 A 的话，那么 Make 会先完成它依赖的编译目标 A 的命令，如果它依赖的编译目标 A 也存在依赖 B 的话，make 就会去执行依赖的 B 的编译命令，如此的递归下去，知道有所得依赖目标都存在了，才会完成第一个编译目标的编译，这个也很好理解，只有依赖文件都存在了我们才能够完成正确的编译过程
- 函数的调用 $(<function> <arguments>)
	- 字符串：subst, strip, findstring, filter, filter-out, sort,word
	- 文件名：dir, notdir, suffix, basename, addsuffix,addprefix, join, wildcard
	- 其他：foreach, call, origin
- 用 include 来引入其他的 makefile

## Source Pointers

- `raw/sources/Makefile.md`
