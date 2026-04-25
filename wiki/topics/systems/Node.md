---
title: Node
type: topic
category: systems
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - node
source_refs:
  - raw/sources/Node.md
---
# Node

- Shell Wrapper：
	- https://github.com/sindresorhus/execa
		- 基于 node 的 child_process 包裹，很轻量，也支持 streaming 等需求，使用起来会比直接用 child_process 更方便
- 鉴权方案：
	- https://authjs.dev/
- ESM 环境下已经没有内置的 `__dirname`
	- 常见替代方式是先通过 `fileURLToPath(import.meta.url)` 得到 `__filename`，再用 `dirname(__filename)` 推出目录
-

## Source Pointers

- `raw/sources/Node.md`
