---
title: CSS
type: topic
category: frontend
status: seed
created: 2026-04-12
updated: 2026-04-25
tags:
  - css
  - tailwind
source_refs:
  - raw/sources/CSS.md
---
# CSS

- 现代 CSS 使用例子：https://dev.37signals.com/modern-css-patterns-and-techniques-in-campfire/
- 颜色：
	- https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl
- [[Tailwind]]
- Tutorial:
	- 介绍 grid 的，感觉挺好的：https://ishadeed.com/article/css-grid-area/

## 工程结论

- 对 portal 类组件，不要依赖父选择器嵌套出来的样式作用域。portal 节点脱离原来的 DOM 层级后，父元素 class 不会跟过去，这类样式要提到顶层，或改成直接命中 portal 根节点的选择器。
- 某些 CSS transition 依赖浏览器先把元素放进渲染树。如果你在同一轮脚本里既让元素可见、又立刻移除初始隐藏类，过渡可能直接跳到终态；这时读取 `offsetWidth`、`getBoundingClientRect()` 一类布局信息会强制触发 reflow，让过渡按预期生效。
- flex 容器里的子项如果看起来“明明设置了 `flex-shrink: 1` 还是不缩”，常见原因不是 shrink 失效，而是自动最小尺寸在生效。此时把子项的 `min-width` 显式设为 `0`，或通过 `overflow: hidden` 改写最小尺寸约束，往往才是正确修复方式。

## Source Pointers

- `raw/sources/CSS.md`
