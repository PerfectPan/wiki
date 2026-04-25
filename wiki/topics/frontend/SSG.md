---
title: SSG
type: topic
category: frontend
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - ssg
source_refs:
  - raw/sources/SSG.md
---
# SSG

- renderToString 就可以，如果有交互的话，还是需要 hydration 的
- 我理解如果是纯静态的话（不包含事件的）是可以不用 hydration 的，因为 SSR 本质上也是 html 的那棵树再重建然后水合，如果没有交互的话根本不需要引入 react

## Source Pointers

- `raw/sources/SSG.md`
