---
title: Web Components 的服务端渲染路径
type: synthesis
category: frontend
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - web-components
  - ssr
  - lit
  - custom-elements
source_refs:
  - wiki/topics/frontend/Lit.md
  - wiki/topics/frontend/SSR.md
---
# Web Components 的服务端渲染路径

## 问题

Web Components 能不能像普通 SSR 框架那样先在服务端产出 HTML？如果能，代价是什么？

## 简答

能，但通常不是“天然支持”，而是通过 DOM 仿真实现一个服务端可执行环境，再提前注册 custom elements 并序列化结果。它更像一条可行但有额外成本的集成路线，而不是默认零成本能力。

## 综合结论

- 一条可行的实现路径是：在服务端用 `happy-dom` 一类 DOM 仿真环境补齐 `document`、`customElements`、`HTMLElement` 等全局对象，然后先执行组件注册，再把 HTML 丢进去渲染并序列化输出。
- 这说明 Web Components 的 SSR 并不是“不可能”，而是要先回答一个前提问题：你的组件实现是否足够依赖浏览器原生环境，还是能在受控的 DOM 仿真里运行。
- 结合现有 `[[wiki/topics/frontend/Lit|Lit]]` 和 `[[wiki/topics/frontend/SSR|SSR]]` 页面，可以得到一个更稳定的理解：
  - SSR 的目标仍然是首屏先给出可显示内容；
  - Web Components 的难点在于它们默认围绕浏览器运行时和 custom elements 生命周期组织；
  - 因此服务端渲染这类组件，往往要额外提供一个“像浏览器但不是真浏览器”的执行环境。
- 这条路径的价值在于：
  - 可以让 Web Components 体系也拿到首屏 HTML；
  - 对设计系统、静态展示组件和需要序列化 Shadow DOM 的场景尤其有吸引力。
- 但它的代价也很明确：
  - 需要额外维护 DOM 仿真环境；
  - 组件不能过度依赖浏览器独有 API；
  - 调试和运行时一致性要比传统 React/Vue SSR 更谨慎。

## 未决问题

- 这页还没有覆盖 hydration、事件恢复以及不同 Web Components 实现库的差异。
- 如果后续仓库里积累了更多例子，可以继续拆成 topic，例如专门记录 Lit 的 SSR 路线。

## 来源指针

- [[wiki/topics/frontend/Lit|Lit]]
- [[wiki/topics/frontend/SSR|SSR]]
