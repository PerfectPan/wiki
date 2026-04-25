---
title: React Render Optimization
type: topic
category: frontend
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - react
  - performance
  - rendering
  - memoization
source_refs:
  - legacy-logseq-journals/2024_01_16.md
  - legacy-logseq-journals/2024_12_14.md
  - raw/sources/React.md
---
# React Render Optimization

## 摘要

React 渲染优化的关键不是“到处包 `memo`”，而是先识别状态更新会影响哪一段子树，再决定是调整状态位置、稳定引用，还是引入更细粒度的订阅方式。

## 关键点

- journal 里的核心观察是：组件内部一次 `setState` 会让该组件及其子树重新执行 render 逻辑。
- 如果某个子树本身很昂贵，而它又并不依赖那次状态变化，通常更有效的做法不是先上 `React.memo`，而是：
  - 把状态提到更合适的位置；
  - 让昂贵子树以稳定引用的方式透传；
  - 避免把不必要的变化传播进整棵子树。
- 这也是为什么“保持 Object Reference 稳定”在 React 性能里很重要：它不只是缓存优化，而是直接影响哪些子树会被重新计算。
- 后续 journal 还补了另一条线索：`react-scan` 这类工具能帮助观察真实的重渲染热点，比只凭直觉加 memo 更可靠。

## 相关页面

- [[React]]
- [[React Context 颗粒度与 Selector 路径]]

## 来源指针

- `legacy-logseq-journals/2024_01_16.md`
- `legacy-logseq-journals/2024_12_14.md`
- `raw/sources/React.md`
