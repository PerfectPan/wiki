---
title: 自定义滚动条库源码审阅记录
source_type: conversation-and-source-review
created: 2026-05-08
tags: [frontend, scrollbar, ui-library]
---

# 自定义滚动条库源码审阅记录

## 背景

这份 raw 记录来自一次关于 Web 自定义滚动条库的选型讨论。讨论对象包括：

- OverlayScrollbars
- SimpleBar
- Perfect Scrollbar
- 原生 CSS scrollbar

先前基于文档和包信息形成过初步判断，随后补充拉取源码进行核对。

## 已审阅源码

### OverlayScrollbars

- 仓库：`https://github.com/KingSora/OverlayScrollbars.git`
- 本地审阅版本：`dfa8196`
- 关键文件：
  - `packages/overlayscrollbars/src/overlayscrollbars.ts`
  - `packages/overlayscrollbars/src/setups/structureSetup/structureSetup.elements.ts`
  - `packages/overlayscrollbars/src/setups/observersSetup/observersSetup.ts`
  - `packages/overlayscrollbars/src/setups/scrollbarsSetup/scrollbarsSetup.ts`
  - `packages/overlayscrollbars/src/plugins/scrollbarsHidingPlugin/scrollbarsHidingPlugin.ts`
  - `packages/overlayscrollbars-react/src/useOverlayScrollbars.ts`

源码事实：

- 保留原生滚动元素，滚动仍由 DOM 的 `scrollTop / scrollLeft` 和 `scroll` 事件驱动。
- 构造或识别 `host / padding / viewport / content / scrollOffsetElement / scrollEventElement` 等结构。
- 使用 `MutationObserver`、`ResizeObserver`、debounce 和 update hints 处理内容、尺寸、方向和可见性变化。
- 隐藏原生滚动条由独立 `ScrollbarsHidingPlugin` 负责，通过 viewport margin、padding、width 等计算处理。
- React 包主要负责生命周期、options/events 更新、销毁和 defer 初始化。

### SimpleBar

- 仓库：`https://github.com/Grsmto/simplebar.git`
- 本地审阅版本：`dfbb9de`
- 关键文件：
  - `packages/simplebar-core/src/index.ts`
  - `packages/simplebar/src/index.ts`
  - `packages/simplebar-react/index.tsx`

源码事实：

- 保留原生滚动，实际滚动容器是 `contentWrapperEl`。
- DOM 结构相对固定，包括 `wrapper / mask / offset / content-wrapper / content / placeholder / track / scrollbar`。
- 使用 `ResizeObserver` 观察宿主和内容，使用 `MutationObserver` 观察内容子树变化。
- `recalculate()` 负责计算溢出、placeholder 尺寸、thumb 尺寸和原生滚动条隐藏偏移。
- 滚动时用 `requestAnimationFrame` 更新 scrollbar handle 位置。
- React 包预渲染 SimpleBar DOM 结构，再创建 `SimpleBarCore` 实例。

### Perfect Scrollbar

- 仓库：`https://github.com/mdbootstrap/perfect-scrollbar.git`
- 本地审阅版本：`07acbff`
- 关键文件：
  - `src/index.js`
  - `src/update-geometry.js`
  - `src/process-scroll-diff.js`
  - `src/handlers/mouse-wheel.js`
  - `src/handlers/touch.js`
  - `src/handlers/drag-thumb.js`
  - `src/handlers/keyboard.js`

源码事实：

- 底层仍操作宿主元素的 `scrollTop / scrollLeft`，但主动接管更多输入事件。
- 初始化时直接向宿主元素 append X/Y rail 和 thumb。
- `updateGeometry()` 通过容器尺寸、内容尺寸、滚动偏移计算 thumb 尺寸与位置。
- wheel、touch、keyboard、drag、click rail 等 handler 会直接修改 `scrollTop / scrollLeft`，然后调用 `updateGeometry()`。
- touch handler 内部还有基于 interval 的 swipe easing。

## 初步结论

- OverlayScrollbars 更像“滚动容器增强系统”：结构化 setup、observer 更新、插件化隐藏策略和较完整的复杂布局支持。
- SimpleBar 更像“固定 DOM 结构的滚动条替换组件”：保留原生滚动，结构和计算更直接，适合普通容器。
- Perfect Scrollbar 更像“老式 JS 滚动同步器”：保留 DOM scroll，但对输入事件接管更重，几何计算和事件处理更手工。

## 注意

这份 raw 是源码审阅摘要，不是完整源码摘录。长期结论已整理到 comparison 页面。