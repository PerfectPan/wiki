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
  - raw/sources/2026-10-07-lisse.md
  - raw/sources/2026-10-07-modern-css.md
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
  - raw/sources/2026-10-07-lisse.md
  - raw/sources/2026-10-07-modern-css.md
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

这里收录写界面时可用的组件库、视觉效果库和 CSS 参考站。每项只写用途、分级和来源；具体评审保存在原始资料中。

## 分级

| 档 | 含义 |
| --- | --- |
| 推荐 | 说明和许可清楚，有明确复用或学习价值。 |
| 可参考 | 有具体用途，但仍有接入或使用限制需要核对。 |
| 偏薄 | 仅在具有明确教学价值时保留，通常不建议直接采用。 |

## 索引

### 推荐

| 库 | 一句话 | 指针 |
| --- | --- | --- |
| **Transitions.dev** | product UI 微交互的 CSS 动效菜谱（modal / dropdown / badge / skeleton 等 20+）；`t-*` 命名 + `prefers-reduced-motion`，写微交互时的观感与 snippet 参考 | [[wiki/topics/frontend/transitions-dev|topic]] · `raw/sources/2026-07-26-transitions-dev.md` |

### 可参考

| 库 | 一句话 | 指针 |
| --- | --- | --- |
| **Lisse（corne.rs）** | 为 React、Vue、Svelte 等界面提供平滑圆角、边框和阴影，适合卡片与按钮；需检查布局和超出圆角区域的内容，尚未实测。 | [官网](https://corne.rs/) · [文档](https://github.com/JaceThings/Lisse/wiki) · [[raw/sources/2026-10-07-lisse\|评审素材]] |
| **Modern CSS** | 用新旧代码对照帮助查找更简短的 CSS 写法，采用前需核对目标浏览器、布局适用性与复用许可。 | [官网](https://modern-css.com/) · [[raw/sources/2026-10-07-modern-css\|评审素材]] |
| **Rare UI** | React + Motion「稀有动效」组件库约 19 个（fluid orb / gooey nav / OTP input / gravity letters 等）；shadcn CLI 单文件分发、MIT；短板：多数为网上作品的复刻，商用前需按站内 Credits 自查归属，WebGL 组件需实测 | [官网](https://www.rareui.com/) · [components](https://www.rareui.com/components) · [GitHub](https://github.com/swamimalode07/rare-ui) · `raw/sources/2026-09-09-rare-ui.md` |
| **滚动条三件套** | OverlayScrollbars / SimpleBar / Perfect Scrollbar：横向选型已闭环，以 comparison 的取舍结论为准，本页只作召回入口 | [[wiki/comparisons/frontend/overlayscrollbars-vs-simplebar-vs-perfect-scrollbar|comparison]] · `raw/sources/2026-05-08-custom-scrollbar-library-source-review.md` |

### 偏薄

（暂无挂名条目。）

## 相关页面

- [[wiki/syntheses/frontend/shadcn-registry-component-distribution|shadcn Registry 组件分发模式]] —— 本索引多数条目依赖的分发机制
- [[wiki/topics/frontend/transitions-dev|Transitions.dev]]
- [[wiki/topics/design/interface-polish-details|界面质感细节]] —— 动效组的「可抄成品」入口

## 来源指针

- [[raw/sources/2026-10-07-lisse|Lisse 评审素材]]
- [[raw/sources/2026-10-07-modern-css|Modern CSS 评审素材]]

- `raw/sources/2026-09-09-rare-ui.md`（Rare UI 合并素材：官网首页 / 组件列表 / GitHub 元信息 / 两个组件页抽查）
- `raw/sources/2026-07-26-transitions-dev.md`
- `raw/sources/2026-05-08-custom-scrollbar-library-source-review.md`
- https://www.rareui.com/
- https://transitions.dev/
- [[wiki/syntheses/frontend/shadcn-registry-component-distribution|shadcn Registry 组件分发模式]]
- [[wiki/comparisons/frontend/overlayscrollbars-vs-simplebar-vs-perfect-scrollbar|自定义滚动条库选型]]
