---
title: useRef
description: 解释 useRef 在跨渲染周期保持对象引用稳定、且修改不触发重渲染的特性。
type: topic
category: frontend
created: 2026-04-12
updated: 2026-04-19
tags:
  - react
  - useref
  - hooks
source_refs:
  - raw/sources/use-ref.md
  - https://beta.reactjs.org/reference/react/useRef#returns
---
# useRef

- 用 ref 去记录一些跟渲染无关的变量，因为它非响应式，修改不会引起 rerender
- This is because the `ref` object has a *stable identity:* React guarantees [you’ll always get the same object](https://beta.reactjs.org/reference/react/useRef#returns) from the same `useRef` call on every render. It never changes, so it will never by itself cause the Effect to re-run. Therefore, it does not matter whether you include it or not.

## Source Pointers

- `raw/sources/use-ref.md`
- https://beta.reactjs.org/reference/react/useRef#returns
