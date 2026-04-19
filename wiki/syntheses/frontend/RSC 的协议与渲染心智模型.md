---
title: RSC 的协议与渲染心智模型
type: synthesis
category: frontend
status: seed
created: 2026-04-19
updated: 2026-04-19
tags:
  - react
  - rsc
  - ssr
  - ssg
  - rendering
source_refs:
  - wiki/topics/frontend/RSC.md
  - wiki/topics/frontend/SSR.md
  - wiki/topics/frontend/SSG.md
  - wiki/topics/frontend/Waku.md
  - wiki/topics/frontend/React.md
  - raw/sources/RSC.md
  - raw/sources/SSR.md
  - raw/sources/SSG.md
  - raw/sources/Waku.md
---
# RSC 的协议与渲染心智模型

## 问题

RSC 到底在服务端和客户端之间传了什么？它和 SSR、SSG 的关系应该怎么理解？

## 简答

RSC 传的不是最终 HTML，而是“服务端组件的 UI 描述 + 客户端组件引用”的协议结果；SSR 负责把页面先渲染成 HTML，SSG 负责把这类结果提前固化到构建产物里。三者不是互斥关系，而是经常组合出现。

## 综合结论

- 从 `RSC.md` 的记录看，RSC 的核心不是“把 React 直接渲染成 HTML”，而是先把组件树拆成两类：
  - Server Component 变成可流式传输的 UI 描述；
  - Client Component 变成模块引用，等到浏览器端再真正消费。
- 因此，RSC 更像一套协议和边界划分机制，而不是传统意义上的首屏策略。它解决的是“哪些代码必须进浏览器、哪些可以留在服务端”。
- `SSR.md` 里强调的则是另一件事：首屏 HTML 先到浏览器，再做 hydration。这个过程可以改善 SEO 和首屏感知，但并不会自动减少客户端 JS 体积，因为同一份 UI 逻辑仍要在两端跑。
- `SSG.md` 对应的是构建时机而不是协议形态：如果页面是静态稳定的，就可以提前把 HTML 甚至相关 payload 产出来，运行时直接分发。
- `Waku.md` 很适合把三者放在同一个构建心智里理解：
  - `buildServerBundle` 更接近 RSC 服务端部分；
  - `buildSsrBundle` 负责 SSR 的 HTML 渲染；
  - `buildClientBundle` 负责客户端代码，并且在静态页面场景下可以把 RSC payload 一并预埋，形成接近 SSG 的产物。
- 所以比较稳的心智模型是：
  - RSC：决定哪些组件留在服务端，以及客户端消费什么协议；
  - SSR：决定首屏是否由服务端先给 HTML；
  - SSG：决定这些结果是在请求时算，还是在构建时先算好。
- 这也解释了为什么 RSC 常常需要和 SSR 一起讨论，但不能简单说“RSC 取代 SSR”。RSC 更像“减少不必要客户端 JS 的边界工具”，SSR 更像“优化首屏交付形态的渲染策略”。

## 未决问题

- `RSC.md` 里对客户端组件嵌套、流式上屏时机仍有实验性疑问，还没有形成更稳定的框架无关结论。
- `Waku.md` 里也保留了多个 TODO，例如动态路由在 SSG 场景下的兜底方式。
- 当前仓库还缺一页真正聚焦 “hydrate / payload / HTML” 三层关系的图解页，后续可以单独补。

## 来源指针

- `wiki/topics/frontend/RSC.md`
- `wiki/topics/frontend/SSR.md`
- `wiki/topics/frontend/SSG.md`
- `wiki/topics/frontend/Waku.md`
- `wiki/topics/frontend/React.md`
- `raw/sources/RSC.md`
- `raw/sources/SSR.md`
- `raw/sources/SSG.md`
- `raw/sources/Waku.md`
