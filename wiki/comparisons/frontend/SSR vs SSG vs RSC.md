---
title: SSR vs SSG vs RSC
type: comparison
category: frontend
status: seed
created: 2026-04-19
updated: 2026-04-19
tags:
  - ssr
  - ssg
  - rsc
  - react
  - rendering
source_refs:
  - wiki/topics/frontend/SSR.md
  - wiki/topics/frontend/SSG.md
  - wiki/topics/frontend/RSC.md
  - wiki/topics/frontend/Waku.md
  - wiki/topics/frontend/React.md
  - raw/sources/SSR.md
  - raw/sources/SSG.md
  - raw/sources/RSC.md
---
# SSR vs SSG vs RSC

## 当前结论

这三者不该被当成同一层级的互斥选项。`SSR` 和 `SSG` 更像“什么时候把结果算出来”，`RSC` 更像“哪些组件逻辑可以留在服务端”。如果目标是 React 应用的长期演进，通常不是三选一，而是先判断页面是否静态，再判断是否需要首屏 HTML，最后才判断 RSC 是否值得引入来减少客户端 JS。

## 备选项

- SSR：请求时在服务端先产出 HTML，再在客户端 hydration。
- SSG：构建时把页面或相关 payload 预先生成，运行时直接分发。
- RSC：把部分组件保留在服务端，以协议形式把结果传给客户端消费。

## 取舍分析

| 方案 | 优势 | 风险 | 适用场景 |
| --- | --- | --- | --- |
| SSR | SEO 友好、首屏 HTML 更早到达、适合动态数据和渐进接入。 | 服务器压力更大，TTFB 可能变差，交互复杂时客户端 JS 仍然很重。 | 动态页面、首屏内容重要、又不能提前静态化的场景。 |
| SSG | 运行时最简单，静态页面可以提前生成并缓存，分发成本低。 | 动态路由、实时数据、权限相关页面不适合强行静态化。 | 文档、营销页、稳定内容页，或者能接受构建时生成的页面。 |
| RSC | 能把一部分组件逻辑留在服务端，减少客户端 JS，并支持更细粒度的流式返回。 | 心智和工具链更复杂，协议、边界、构建集成都更重；通常仍需和 SSR/SSG 组合。 | React 应用中对 JS 体积、流式数据返回和服务端边界很敏感的场景。 |

## 推荐理由

1. 先用 `SSG` 处理稳定页面，因为它最便宜，也最接近“预先算好”。
2. 静态化做不到、但又需要首屏 HTML 时，用 `SSR`；它解决的是交付时机问题，而不是天然减少 JS。
3. 当真正的问题变成“哪些组件根本不该进浏览器”时，再引入 `RSC`。它更像服务端边界优化，而不是单独的首屏策略。
4. 从 `Waku.md` 的构建记录看，现实框架经常同时包含三套产物，这说明工程上通常是组合，而不是纯粹替代。

## 来源指针

- `wiki/topics/frontend/SSR.md`
- `wiki/topics/frontend/SSG.md`
- `wiki/topics/frontend/RSC.md`
- `wiki/topics/frontend/Waku.md`
- `wiki/topics/frontend/React.md`
- `raw/sources/SSR.md`
- `raw/sources/SSG.md`
- `raw/sources/RSC.md`
