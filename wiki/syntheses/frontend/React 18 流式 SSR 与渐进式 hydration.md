---
title: React 18 流式 SSR 与渐进式 hydration
type: synthesis
category: frontend
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - react
  - ssr
  - hydration
  - suspense
  - streaming
source_refs:
  - /Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2024_05_02.md
  - wiki/topics/frontend/SSR.md
  - wiki/topics/frontend/RSC.md
  - wiki/comparisons/frontend/SSR vs SSG vs RSC.md
---
# React 18 流式 SSR 与渐进式 hydration

## 问题

React 18 相比传统 SSR，到底改进了什么？它为什么能让页面在没有完成整页 hydration 之前就开始可交互？

## 简答

关键变化不在于“还是不是 SSR”，而在于把传输和 hydration 都拆成了更小的边界。服务端可以按 `Suspense` 边界流式输出 HTML，客户端也不必等整页代码都 ready 才统一 hydration，而是可以按优先级逐步接管页面。

## 综合结论

- journal 里的这条总结补上了传统 SSR 与 React 18 的差别：
  - 传统 SSR 更像一个大批处理：服务端先渲染整页 HTML，客户端再下载整页代码，最后做完整 hydration；
  - React 18 则允许服务端先把已完成的部分输出出来，再把慢的部分作为 `Suspense` 边界延后传输。
- 这种变化带来的不是“SSR 被替换”，而是 SSR 的颗粒度变细了。页面不再是“整页 ready / 整页 not ready”，而是不同区域可以按边界逐步完成。
- 更重要的是 hydration 也不再必须整页同步完成：
  - 某些区域的客户端代码 ready 了，就可以先接管；
  - 用户真正交互到某个未 hydration 的区域时，React 可以优先处理那一块。
- 这和当前仓库里已有的 `SSR` / `RSC` 页形成了一个更完整的层次：
  - `SSR` 回答首屏 HTML 为什么能更早到达；
  - `RSC` 回答哪些逻辑可以留在服务端，以及客户端要消费什么协议；
  - 这页则回答 React 18 如何把“HTML 交付”和“客户端接管”进一步拆细。
- 因此，React 18 的实际价值不是简单地“更快”，而是它把“等待整页完成”改成了“先让有意义的部分尽快可见、可用”。

## 未决问题

- 这条总结仍然偏 React 机制层，还没有把框架侧实现差异拆开，例如 Next.js、Waku 等在 streaming 和 hydration 调度上的不同细节。
- 当前仓库还没有单独拆出 `Suspense` 在服务端 streaming 中的工程实践页，后续可以继续补。

## 来源指针

- `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2024_05_02.md`
- `wiki/topics/frontend/SSR.md`
- `wiki/topics/frontend/RSC.md`
- `wiki/comparisons/frontend/SSR vs SSG vs RSC.md`
