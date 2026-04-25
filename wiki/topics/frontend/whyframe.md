---
title: whyframe
type: topic
category: frontend
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - iframe
  - isolation
  - compilation
  - component
source_refs: []
---
# whyframe

## 摘要

whyframe 的核心思路是把需要 iframe 隔离的组件在编译期拆出来，而不是运行时动态拼装。这让“组件运行在 iframe 里”从一个运行时技巧，变成了一个构建期约束。

## 关键点

- 它的本质是：
  - 用 `<iframe>` 做隔离；
  - 但不是运行时把现有组件塞进去；
  - 而是编译时把 iframe 内的源码剥离出来，生成独立的虚拟入口和根文件。
- 这意味着它更像“构建工具层的 iframe 隔离方案”，而不是单纯的组件 API。
- 好处是隔离边界清晰；代价是动态能力会受限，因为很多内容在构建期就已经决定好了。
