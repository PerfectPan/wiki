---
title: JavaScript Runtime
type: topic
category: languages
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - javascript
  - runtime
source_refs:
  - raw/sources/JavaScript Runtime.md
---
# JavaScript Runtime

- 标准：https://wintercg.org/
- 轻量 / 自主可控（V8 + WhatWG 标准的实现，赋予了开发团队很高的自由度）/ 开发同构（API 互操作性强）
- Worker 运行时，为业务代码提供了在 IDC 场景、边缘场景、CDN 场景之间平滑迁移的可能性，极大的拓宽了服务架构的想像空间。有了 Worker，我们完全可以做到，同一个 web 项目的同一份代码，既能部署在 IDC，又能部署在边缘，还能部署在 CDN。
- [[Node]] 包兼容性是问题，很多库强依赖 Node 的能力
- 标准的请求触发方式还比较单一
- 社区的一些实现：
	- https://tryandromeda.dev/
-

## Source Pointers

- `raw/sources/JavaScript Runtime.md`
