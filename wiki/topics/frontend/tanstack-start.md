---
title: TanStack Start
description: TanStack Start 的 server function 调用约定、实验性 RSC 支持，以及 TanStack Router 状态如何接到 React
type: topic
category: frontend
created: 2026-10-14
updated: 2026-10-14
timestamp: 2026-10-14
tags:
  - tanstack
  - rsc
  - react
  - router
source_refs:
  - raw/sources/rsc-update-path-local-demos.md
resource:
  - raw/sources/rsc-update-path-local-demos.md
---
# TanStack Start

## 摘要

TanStack Start 是基于 TanStack Router 和 Vite 的全栈 React 框架。服务端逻辑通过 `createServerFn` 定义成 server function，客户端调用时发 HTTP 请求；路由组件默认在客户端渲染，RSC 是可选的实验性功能。以下内容基于 `@tanstack/react-start` 1.169.1、`@tanstack/router-core` 1.171.37、`@tanstack/react-router` 1.170.44。

## 关键点

### Server function

- `createServerFn({ method })` 定义函数，`.validator()` 校验参数，`.handler()` 写服务端逻辑。
- 客户端调用时请求 `/_serverFn/<base64>`，base64 编码的是 `{file, export}`，例如 export 为 `increment_createServerFn_handler`。
- 参数和返回值用 seroval 序列化，可以表达对象、引用等 JSON 表达不了的结构。返回值外层包成 `{ result: ... }`。

### 实验性 RSC

- 需要 `@vitejs/plugin-rsc`，并在 Vite 配置里写 `tanstackStart({ rsc: { enabled: true } })`。
- server function 返回 `renderServerComponent` 或 `createCompositeComponent` 的结果；后者可以留插槽，客户端用 `<CompositeComponent src={...}>` 渲染并把客户端组件作为 children 传进去。
- 响应类型是 `application/x-tss-framed`：seroval 外壳里嵌入 Flight 数据，插槽位置是 `ClientSlot` 占位。
- RSC 粒度是单个 server function 的返回值，不是整条路由。

### Router 状态如何接到 React

1. `router-core` 不直接依赖 React。React 版 `Router` 构造时 `super(options, getStoreFactory)`（`react-router/src/router.ts:117`）。
2. `getStoreFactory`（`react-router/src/routerStores.ts:13`）在客户端返回 `@tanstack/react-store` 的 `createAtom` 和 `batch`，服务端返回不带订阅的实现。core 用它 `createRouterStores`（`router-core/src/router.ts:1369`）。
3. 数据变化时 core 调 `router.stores.setMatches(...)`（`router-core/src/stores.ts:153`）写 atom，组件用 `useSelector` 订阅，底层是 `useSyncExternalStoreWithSelector`（`react-store/src/useSelector.ts:60`）。
4. `Transitioner.tsx:31` 把 `router.startTransition` 换成 `React.startTransition`，所以提交 match 的那次写入发生在 React transition 里。

`router.invalidate()` 到 `setMatches` 的完整调用链见 [[wiki/syntheses/frontend/rsc-update-path-next-vs-tanstack|RSC 交互后的更新链路]]。

### 限制

- RSC 支持标为 experimental，API 和响应格式可能随版本变化。
- 源码行号只对应上述版本。

## 相关页面

- [[wiki/topics/frontend/rsc|RSC]]
- [[wiki/syntheses/frontend/rsc-update-path-next-vs-tanstack|RSC 交互后的更新链路：Next 与 TanStack Start]]

## 来源指针

- `raw/sources/rsc-update-path-local-demos.md`
