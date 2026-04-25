---
title: Polyfill
type: topic
category: frontend
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - polyfill
  - shim
  - compatibility
  - browser
source_refs:
  - legacy-logseq-journals/2022_10_31.md
---
# Polyfill

## 摘要

Polyfill 是一类用来在旧环境里补实现新能力的兼容层。更宽泛地说，它属于 `shim` 的一种特例。

## 关键点

- journal 里给出的关系很清楚：
  - `shim` 是对某个 API 调用做拦截、抽象或兼容的通用做法；
  - `polyfill` 是其中一类更具体的实现，通常是为了让旧浏览器或旧运行时具备新规范能力。
- 这意味着并不是所有 shim 都是 polyfill，但大部分浏览器兼容层讨论里的 polyfill，确实都可以被看作 shim。
- 工程上最重要的区分不是名词，而是目标：
  - 如果你是在补缺失能力，更像 polyfill；
  - 如果你是在重写、包裹或拦截既有接口，更像 shim。

## 相关页面

- [[ES Module 加载与 Import Maps]]

## 来源指针

- `legacy-logseq-journals/2022_10_31.md`
