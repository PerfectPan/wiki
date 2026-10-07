---
title: Awesome Component Libraries
description: 收录组件库、视觉效果库和 CSS 参考站，按推荐、可参考、偏薄分级，附用途与来源。
type: topic
category: frontend
created: 2026-09-09
updated: 2026-10-07
timestamp: 2026-10-07
tags:
  - catalog
  - component-library
  - animation
  - css
  - reference
source_refs:
  - https://animejs.com/
  - wiki/topics/frontend/animejs.md
  - https://www.itshover.com/icons
  - raw/sources/its-hover.md
  - https://corne.rs/
  - https://modern-css.com/
  - raw/sources/2026-09-09-rare-ui.md
  - raw/sources/2026-07-26-transitions-dev.md
  - raw/sources/2026-05-08-custom-scrollbar-library-source-review.md
  - wiki/syntheses/frontend/shadcn-registry-component-distribution.md
  - wiki/comparisons/frontend/overlayscrollbars-vs-simplebar-vs-perfect-scrollbar.md
  - https://www.rareui.com/
  - https://transitions.dev/
resource:
  - https://animejs.com/
  - wiki/topics/frontend/animejs.md
  - https://www.itshover.com/icons
  - raw/sources/its-hover.md
  - https://corne.rs/
  - https://modern-css.com/
  - raw/sources/2026-09-09-rare-ui.md
  - raw/sources/2026-07-26-transitions-dev.md
  - raw/sources/2026-05-08-custom-scrollbar-library-source-review.md
  - wiki/syntheses/frontend/shadcn-registry-component-distribution.md
  - wiki/comparisons/frontend/overlayscrollbars-vs-simplebar-vs-perfect-scrollbar.md
  - https://www.rareui.com/
  - https://transitions.dev/
---

# Awesome Component Libraries

## 摘要

这里收录写界面时可用的组件库、视觉效果库和 CSS 参考站。每项只写用途、分级和来源。

## 分级

| 档 | 含义 |
| --- | --- |
| **推荐** | 可直接抄进项目的成品质量高；文档（Props / 交互 / 安装）完整；许可明确可商用；或有范式价值 |
| **可参考** | 有真实可抄价值，但有短板：复刻归属需自查、依赖较重或需实测、文档偏薄 |
| **偏薄** | 只有链接 / 简介级信息，缺少进一步分析或实测；默认不装，只作反例或起点 |

## 索引

### 推荐

| 库 | 一句话 | 指针 |
| --- | --- | --- |
| **Anime.js** | 用 JavaScript 编排元素、SVG 和对象动画，时间线与滚动等工具文档完整，采用 MIT 许可；与 Motion 的接口关系见主题页，尚未做项目实测。 | [[wiki/topics/frontend/animejs\|topic]] · [官网](https://animejs.com/) |
| **Transitions.dev** | product UI 微交互的 CSS 动效菜谱（modal / dropdown / badge / skeleton 等 20+）；`t-*` 命名 + `prefers-reduced-motion`，写微交互时的观感与 snippet 参考 | [[wiki/topics/frontend/transitions-dev|topic]] · `raw/sources/2026-07-26-transitions-dev.md` |

### 可参考

| 库 | 一句话 | 指针 |
| --- | --- | --- |
| **Its Hover** | 基于 React + Motion、可经 shadcn CLI 复制的动效图标，抽查组件需补焦点触发与减少动态效果，并核对 Apache-2.0 / MIT 声明差异。 | [图标](https://www.itshover.com/icons) · [[raw/sources/its-hover\|源码核查]] |
| **Lisse（corne.rs）** | 为 React、Vue、Svelte 等界面提供平滑圆角、边框和阴影，适合卡片与按钮；需检查布局和超出圆角区域的内容，尚未实测。 | [官网](https://corne.rs/) · [文档](https://github.com/JaceThings/Lisse/wiki) · [使用限制](https://github.com/JaceThings/Lisse/wiki/Limitations) |
| **Modern CSS** | 用新旧代码对照帮助查找更简短的 CSS 写法，采用前需核对目标浏览器、布局适用性与复用许可。 | [官网](https://modern-css.com/) · [居中示例](https://modern-css.com/centering-elements-without-the-transform-hack/) |
| **Rare UI** | React + Motion「稀有动效」组件库约 19 个（fluid orb / gooey nav / OTP input / gravity letters 等）；shadcn CLI 单文件分发、MIT；短板：多数为网上作品的复刻，商用前需按站内 Credits 自查归属，WebGL 组件需实测 | [官网](https://www.rareui.com/) · [components](https://www.rareui.com/components) · [GitHub](https://github.com/swamimalode07/rare-ui) · `raw/sources/2026-09-09-rare-ui.md` |
| **滚动条三件套** | OverlayScrollbars / SimpleBar / Perfect Scrollbar：横向选型已闭环，以 comparison 的取舍结论为准，本页只作召回入口 | [[wiki/comparisons/frontend/overlayscrollbars-vs-simplebar-vs-perfect-scrollbar|comparison]] · `raw/sources/2026-05-08-custom-scrollbar-library-source-review.md` |

### 偏薄

（暂无挂名条目。）

## 相关页面

- [[wiki/topics/frontend/animejs|Anime.js]] —— 与 Motion 的接口关系。
- [[wiki/syntheses/frontend/shadcn-registry-component-distribution|shadcn Registry 组件分发模式]] —— 本索引多数条目依赖的分发机制
- [[wiki/topics/frontend/transitions-dev|Transitions.dev]]
- [[wiki/topics/design/interface-polish-details|界面质感细节]] —— 动效组的「可抄成品」入口

## 来源指针

- [Anime.js](https://animejs.com/)、[[wiki/topics/frontend/animejs|接口与接入依据]]。
- [Its Hover](https://www.itshover.com/icons)、[[raw/sources/its-hover|组件与许可核查]]。
- [Lisse](https://corne.rs/)：[文档](https://github.com/JaceThings/Lisse/wiki)、[使用限制](https://github.com/JaceThings/Lisse/wiki/Limitations)。
- [Modern CSS](https://modern-css.com/)：[居中示例](https://modern-css.com/centering-elements-without-the-transform-hack/)。

- `raw/sources/2026-09-09-rare-ui.md`（Rare UI 合并素材：官网首页 / 组件列表 / GitHub 元信息 / 两个组件页抽查）
- `raw/sources/2026-07-26-transitions-dev.md`
- `raw/sources/2026-05-08-custom-scrollbar-library-source-review.md`
- https://www.rareui.com/
- https://transitions.dev/
- [[wiki/syntheses/frontend/shadcn-registry-component-distribution|shadcn Registry 组件分发模式]]
- [[wiki/comparisons/frontend/overlayscrollbars-vs-simplebar-vs-perfect-scrollbar|自定义滚动条库选型]]
