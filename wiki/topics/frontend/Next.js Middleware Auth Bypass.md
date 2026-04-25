---
title: Next.js Middleware Auth Bypass
type: topic
category: frontend
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - nextjs
  - middleware
  - security
  - auth
source_refs:
  - /Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2025_03_24.md
---
# Next.js Middleware Auth Bypass

## 摘要

一类 Next.js middleware 绕过问题：框架为了避免 middleware 自己递归调用自己，会使用内部头部来记录调用链深度；如果这个头部可以被外部请求伪造，依赖 middleware 做鉴权的逻辑就可能被整体跳过。

## 关键点

- journal 里的记录指出，Next.js 会用一个内部头部来标识 middleware 调用链。
- 一旦外部请求能够带上这个头部，并伪造成“已经递归调用多次”的状态，middleware 的后续逻辑就可能被直接绕过。
- 如果鉴权、重定向或访问控制放在 middleware 中，这种绕过会直接影响整条保护链。
- 记录里还提到一个重要边界：部署在 Vercel 上时，由于网关层能拦截非法头部，这类问题的暴露面会小一些；但自托管或不同部署环境下，不能默认享受这层保护。

## 相关页面

- [[Software Design]]
- [[OAuth]]

## 来源指针

- `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2025_03_24.md`
