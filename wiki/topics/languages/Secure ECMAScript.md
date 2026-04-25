---
title: Secure ECMAScript
type: topic
category: languages
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - secure
  - ecmascript
source_refs:
  - raw/sources/Secure ECMAScript.md
---
# Secure ECMAScript

- 供应链攻击：
	- 安装时
		- --ignore-scripts（本地的也 ignore 了）
		- pnpm: onlyBuiltDependencies
			- https://github.com/pnpm/pnpm/issues/4001
			- 也有问题，可以同名然后指向一个 evil 的仓库地址或者 cdn 地址，需要在 pnpm install 的 hooks 里再写点代码来制造白名单，可以看上面这个 issue
		- npm/yarn: @lavamoat/allow-scripts
		- 或者都在 docker 里开发（一个虚拟化的环境）
	- 编译时
		- 执行恶意代码：
			- 最小权限原则
				- deno 提供进程级最小权限原则的实现
				- LavaMort 提供 npm 包级别最小权限原则的实现
		- 编译产物植入恶意代码：没有好的解决办法，只能靠人工审核和测试
			- 可重复构建：为编译工具提供虚假的时间、时区、语言、项目绝对路径
	- 运行时
- 基于能力的安全模型
	- apiKey，key 会指定你可以用的权限
- 基于对象能力的安全模型（不是特别理解）
- https://github.com/endojs/endo
- ShadowRealm 是运行在同一进程的，挂在全局上的一个对象，跨进程可以走 web worker，同一进程会比 iframe 轻量
- Compartment 相较于 ShadowRealm 可控制的会更多（模块依赖图，解析 specifier 可以自定义 hook），全局实例对象（Array，Function，Object，etc...）的 prototype 是共享的，实例还是隔离的，ShadowRealm 是隔离的，创建会比 ShadowRealm 更轻量一些
	- 和 lockdown 提案一起使用，防止原型链污染

## Source Pointers

- `raw/sources/Secure ECMAScript.md`
