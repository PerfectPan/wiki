---
title: RSC 与 CSS-in-JS 的兼容性约束
type: synthesis
category: frontend
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - rsc
  - react
  - css-in-js
  - styling
source_refs:
  - legacy-logseq-journals/2024_04_16.md
  - wiki/topics/frontend/RSC.md
  - wiki/topics/frontend/CSS.md
---
# RSC 与 CSS-in-JS 的兼容性约束

## 问题

为什么 React Server Components 往往和运行时 CSS-in-JS 不那么合拍，而更偏向编译时样式方案？

## 简答

因为 RSC 压缩了客户端运行时能力，很多依赖 React context、运行时插入样式或组件执行阶段收集信息的 CSS-in-JS 机制都失去了落点。越依赖编译时提取、静态类名和构建期产物的样式方案，越容易与 RSC 协作。

## 综合结论

- 现有 `[[wiki/topics/frontend/RSC|RSC]]` 页已经说明了 RSC 的核心边界：服务端组件并不是普通的客户端 React 组件，它们经过协议化传输，再由客户端恢复和拼装。
- journal 进一步给出的高价值结论是：RSC 不能自由使用 `useContext` 这类客户端运行时特性，这会直接影响依赖运行时上下文和样式注入的 CSS-in-JS 方案。
- 这意味着两类样式路线的兼容性会明显分化：
  - 运行时 CSS-in-JS：典型问题是依赖组件执行期、context 或浏览器端注入样式，和 RSC 的执行边界天然有摩擦；
  - 编译时样式方案：更接近“提前产出 class name 和静态资源”，对 RSC 更友好。
- 从工程决策上看，这页最值得沉淀的不是“某个库行不行”，而是一个更稳的判断标准：
  - 如果样式方案要求组件运行时去决定最终样式结构，就要仔细检查它在 RSC 下的可用性；
  - 如果样式方案主要在构建期工作，最终只给 React 组件留下 class name 或静态结果，通常更容易兼容。
- 所以 journal 里“社区都在往编译时路线走”的观察，本质上不是风格偏好，而是对 RSC 运行边界的适配结果。

## 未决问题

- 这页目前总结的是方向性约束，还没有逐个梳理具体库在 RSC 下的支持差异。
- 如果后续仓库里积累了更多案例，可以继续补成一页 comparison，例如“运行时 CSS-in-JS vs 编译时样式方案”。

## 来源指针

- `legacy-logseq-journals/2024_04_16.md`
- [[wiki/topics/frontend/RSC|RSC]]
- [[wiki/topics/frontend/CSS|CSS]]
