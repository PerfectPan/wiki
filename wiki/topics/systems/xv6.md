---
title: xv6
type: topic
category: systems
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - xv6
source_refs:
  - raw/sources/xv6.md
---
# xv6

- https://zhuanlan.zhihu.com/p/501901665
- https://zhuanlan.zhihu.com/p/567525198
- 用户程序是通过mkfs/mkfs直接写进fs.img里的，运行是通过exec从文件系统里读到内存里。因此想调试，应该就只能等pc跳过去之后，在gdb里手动看汇编 - 解决办法 https://www.cnblogs.com/KatyuMarisaBlog/p/13727565.html（或许还是 gdb 调试更方便些？）
- https://stackoverflow.com/questions/72759791/why-does-gdb-do-not-show-all-risc-v-csrs-when-debugging-bare-metal-program-runni
- VSCode 调试配置
	- ```json
	  // xv6-riscv/.vscode/launch.json
	  {
	      "version": "0.2.0",
	      "configurations": [
	          {
	              "name": "xv6debug",
	              "type": "cppdbg",
	              "request": "launch",
	              "program": "${workspaceFolder}/kernel/kernel",
	              "stopAtEntry": true,
	              "cwd": "${workspaceFolder}",
	              "miDebuggerServerAddress": "127.0.0.1:26000", //见.gdbinit 中 target remote xxxx:xx
	              "miDebuggerPath": "/usr/bin/gdb-multiarch", // which gdb-multiarch
	              "MIMode": "gdb",
	              "preLaunchTask": "xv6build"
	          }
	      ]
	  }
	  ```
	- ```json
	  // xv6-riscv/.vscode/tasks.json
	  {
	      "version": "2.0.0",
	      "tasks": [
	          {
	              "label": "xv6build",
	              "type": "shell",
	              "isBackground": true,
	              "command": "make qemu-gdb",
	              "problemMatcher": [
	                  {
	                      "pattern": [
	                          {
	                              "regexp": ".",
	                              "file": 1,
	                              "location": 2,
	                              "message": 3
	                          }
	                      ],
	                      "background": {
	                          "beginsPattern": ".*Now run 'gdb' in another window.",
	                          "endsPattern": "." // // 要对应编译成功后,一句echo的内容. 此处对应 Makefile Line:170
	                      }
	                  }
	              ]
	          }
	      ]
	  }

	  ```
	- ```json
	  // xv6-riscv/.vscode/c_cpp_properties.json 智能提示
	  {
	      "configurations": [
	          {
	              "name": "Linux",
	              // "includePath": [],
	              // "defines": [],
	              // "compilerPath": "/usr/bin/riscv64-linux-gnu-gcc",
	              // "cStandard": "gnu17",
	              // "intelliSenseMode": "${default}",
	              "compileCommands": "${workspaceFolder}/.vscode/compile_commands.json"
	              // "configurationProvider": "ms-vscode.makefile-tools"
	          }
	      ],
	      "version": 4
	  }
	  ```

## Source Pointers

- `raw/sources/xv6.md`

