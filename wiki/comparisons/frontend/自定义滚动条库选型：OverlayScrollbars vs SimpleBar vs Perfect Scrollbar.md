---
title: 自定义滚动条库选型：OverlayScrollbars vs SimpleBar vs Perfect Scrollbar
type: comparison
category: frontend
status: seed
created: 2026-05-08
updated: 2026-05-08
tags: [scrollbar, ui-library, performance, accessibility]
source_refs:
  - raw/sources/2026-05-08-custom-scrollbar-library-source-review.md
  - https://github.com/KingSora/OverlayScrollbars
  - https://github.com/Grsmto/simplebar
  - https://github.com/mdbootstrap/perfect-scrollbar
---

# 自定义滚动条库选型：OverlayScrollbars vs SimpleBar vs Perfect Scrollbar

## 当前结论

如果只是简单美化滚动条，优先使用原生 CSS scrollbar。只有当产品需要统一跨浏览器视觉、稳定处理复杂滚动容器，才值得引入自定义滚动条库。

在三个库里：

- **OverlayScrollbars** 适合复杂 Web App、AI 聊天界面、Dashboard、长期维护的后台系统。
- **SimpleBar** 适合普通滚动容器和较轻量的视觉统一需求。
- **Perfect Scrollbar** 更适合历史项目延续；新项目不应优先选择。

一句话：**OverlayScrollbars 是“滚动容器增强系统”；SimpleBar 是“固定结构的滚动条替换组件”；Perfect Scrollbar 是“老式 JS 滚动同步器”。**

## 备选项

- 原生 CSS scrollbar
- OverlayScrollbars
- SimpleBar
- Perfect Scrollbar

## 源码事实

### OverlayScrollbars

源码显示 OverlayScrollbars 保留原生滚动，不重写滚动系统。它会构造或识别一组滚动容器结构：`host / padding / viewport / content / scrollOffsetElement / scrollEventElement`。

它的核心不是“画一个 scrollbar”，而是围绕滚动容器做完整增强：

- `structureSetup` 管理 DOM 包装与滚动元素关系。
- `observersSetup` 使用 `MutationObserver`、`ResizeObserver`、debounce 和 update hints 管理变化。
- `scrollbarsSetup` 管理自定义 scrollbar UI、auto hide、drag、click scroll、pointer 交互。
- `ScrollbarsHidingPlugin` 单独负责隐藏原生滚动条，通过 viewport margin、padding、width 等方式处理，而不是简单 `overflow: hidden`。

这套结构解释了它为什么比 SimpleBar 重：它处理的不是单个滚动条，而是一整套滚动容器状态机。

### SimpleBar

SimpleBar 也保留原生滚动，实际滚动容器是 `contentWrapperEl`。它的 DOM 结构相对固定：`wrapper / mask / offset / content-wrapper / content / placeholder / track / scrollbar`。

它的核心路径比较直接：

- 初始化时准备固定 DOM 包装。
- `ResizeObserver` 监听容器和内容尺寸。
- `MutationObserver` 监听内容子树变化。
- `recalculate()` 计算溢出、placeholder、thumb 尺寸和隐藏原生滚动条所需偏移。
- 滚动时用 `requestAnimationFrame` 更新 thumb 位置。

所以 SimpleBar 更像一个轻量、固定结构的滚动条替换组件。它适合普通容器，但复杂布局和边界适配能力不如 OverlayScrollbars。

### Perfect Scrollbar

Perfect Scrollbar 底层仍操作宿主元素的 `scrollTop / scrollLeft`，但它主动接管更多输入事件：wheel、touch、keyboard、drag thumb、click rail。

它的核心是手工几何同步：

- 初始化时向宿主 append X/Y rail 和 thumb。
- `updateGeometry()` 通过 `containerWidth / contentWidth / scrollTop / scrollLeft` 计算 thumb 尺寸和位置。
- 各类 handler 直接修改 `scrollTop / scrollLeft`，然后调用 `updateGeometry()`。
- touch handler 里还有基于 interval 的 swipe easing。

这类实现能工作，但更像早期自定义滚动条方案。现代复杂 UI 下，它的事件接管和几何同步更容易形成维护成本。

## 取舍分析

| 方案 | 优势 | 风险 | 适用场景 |
| --- | --- | --- | --- |
| 原生 CSS scrollbar | 零运行时、无额外 DOM、维护成本最低 | 跨浏览器一致性和控制力有限 | 简单官网、轻量页面、只需轻微美化 |
| OverlayScrollbars | 工程化完整，Observer 更新体系和复杂布局支持更强 | DOM 包装和监听器更多，API 与调试复杂度更高 | 后台系统、聊天窗口、Dashboard、复杂滚动容器 |
| SimpleBar | 接入简单，保留原生滚动，结构清楚 | 固定结构能力有限，复杂边界不如 OverlayScrollbars | 普通侧栏、列表、面板、轻量后台 |
| Perfect Scrollbar | 老项目常见，事件覆盖较全 | 事件接管更重，几何同步老派，现代维护风险较高 | 已有历史项目延续，不建议新项目首选 |

## 推荐理由

### 新项目默认策略

1. 先判断是否真的需要自定义滚动条。
2. 如果只是为了“好看一点”，先用原生 CSS scrollbar。
3. 如果是普通滚动容器，优先 SimpleBar。
4. 如果是复杂 Web App 的关键滚动区域，优先 OverlayScrollbars。
5. 新项目一般不要优先选择 Perfect Scrollbar。

### OverlayScrollbars 适合的场景

- AI 聊天消息区
- 长侧边栏 / 文件树 / 菜单区
- 日志面板 / 代码窗口
- 表格容器 / Dashboard 卡片
- 桌面感强、需要统一 scrollbar 视觉的 Web App

它的价值在于“复杂滚动容器治理”，不是单纯装饰。

### SimpleBar 适合的场景

- 普通后台侧栏
- 简单长列表
- 弹窗 / 抽屉内容区
- 对功能深度要求不高，但希望视觉统一的容器

它比 OverlayScrollbars 更轻，但不要期待它覆盖所有复杂布局。

### Perfect Scrollbar 的定位

如果历史项目已经用了 Perfect Scrollbar，可以继续维护；但新项目选型时，它通常不是最优解。它对 wheel、touch、keyboard 等输入事件接管更多，`updateGeometry()` 手工同步也更老派，长期风险高于前两个。

## 落地原则

- 不要全站无脑接管滚动条。
- 优先只在 1 到 3 个高价值局部容器使用。
- body 级滚动谨慎使用，尤其要测试路由切换、锚点跳转、滚动恢复和移动端软键盘。
- 虚拟列表场景必须确认 ref 挂载、滚动监听目标、高度测量和 DOM wrapper 是否冲突。
- 可访问性不能只看文档承诺，至少测试 Tab、PageUp/PageDown、Home/End、focus ring 和屏幕阅读器区域识别。

## 相关页面

- [[wiki/topics/frontend/CSS|CSS]]
- [[wiki/syntheses/frontend/交互式 UI 的可访问性基线|交互式 UI 的可访问性基线]]
- [[wiki/topics/frontend/React Render Optimization|React Render Optimization]]

## 来源指针

- `raw/sources/2026-05-08-custom-scrollbar-library-source-review.md`
- OverlayScrollbars 源码：`https://github.com/KingSora/OverlayScrollbars`
- SimpleBar 源码：`https://github.com/Grsmto/simplebar`
- Perfect Scrollbar 源码：`https://github.com/mdbootstrap/perfect-scrollbar`
