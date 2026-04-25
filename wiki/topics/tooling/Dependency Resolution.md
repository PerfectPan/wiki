---
title: Dependency Resolution
type: topic
category: tooling
status: seed
created: 2026-04-22
updated: 2026-04-22
tags:
  - dependency-resolution
  - package-manager
  - sat
  - algorithm
source_refs:
  - /Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2024_05_29.md
  - https://borretti.me/article/dependency-resolution-made-simple
  - https://github.com/dart-lang/pub/blob/master/doc/solver.md
---
# Dependency Resolution

## 摘要

依赖解析是在包管理器里为一组包选择兼容版本的过程。一个常见思路是把“版本选择是否满足约束”规约成更底层的约束求解问题，再由统一求解器处理。

## 关键点

- journal 里的原始记录把这篇文章的核心抓得比较准：作者把包管理器里的依赖版本选择问题规约成一组命题，再转化为 SAT 风格的问题来求解。
- 这种思路的价值不只在于“能不能直接照搬”，而在于它提供了一个通用做法：
  - 先把包、版本、约束和冲突形式化；
  - 再把它们映射到一个更底层、可统一求解的问题。
- 原始记录也指出了一个现实差异：文中假设“一个包最多只安装一次”，但现代前端包管理器往往允许多版本并存，因此真实工程里的约束模型通常会更弱，也更复杂。
- 这意味着文章最值得迁移的不是具体实现，而是“先规约、再求解”的建模方法。
- Dart `pub` 的 resolver 文档可以作为后续对照材料，用来理解工业实现会在这个抽象思路上加哪些现实约束。

## 相关页面

- [[Algorithm]]
- [[Yarn]]
- [[Monorepo]]

## 来源指针

- `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2024_05_29.md`
- [Dependency Resolution Made Simple](https://borretti.me/article/dependency-resolution-made-simple)
- [Dart pub solver](https://github.com/dart-lang/pub/blob/master/doc/solver.md)
