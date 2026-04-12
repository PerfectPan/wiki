---
title: useRef
type: topic
category: frontend
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - react
  - useref
  - hooks
source_refs:
  - raw/sources/useRef.md
---
# useRef

- 用 ref 去记录一些跟渲染无关的变量，因为它非响应式，修改不会引起 rerender
- This is because the `ref` object has a *stable identity:* React guarantees [you’ll always get the same object](https://beta.reactjs.org/reference/react/useRef#returns) from the same `useRef` call on every render. It never changes, so it will never by itself cause the Effect to re-run. Therefore, it does not matter whether you include it or not.

## Source Pointers

- `raw/sources/useRef.md`
