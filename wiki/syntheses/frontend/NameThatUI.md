---
title: NameThatUI 是什么、什么时候用
description: namethatui.com 元素词典的使用判断：它是 UI 元素的"视觉词典"，价值在每个词条自带 agent prompt；适合写实现 prompt 前查正式名，不替代团队术语规范。
type: synthesis
category: frontend
status: seed
created: 2026-08-13
updated: 2026-08-13
timestamp: 2026-08-13
tags:
  - ui
  - design-systems
  - terminology
  - reference
  - agent-prompts
source_refs:
  - raw/sources/2026-08-13-namethatui.md
  - https://namethatui.com/
  - https://namethatui.com/methodology
  - https://namethatui.com/vs
resource:
  - raw/sources/2026-08-13-namethatui.md
  - https://namethatui.com/
  - https://namethatui.com/methodology
  - https://namethatui.com/vs
---

# NameThatUI 是什么、什么时候用

## 问题

[NameThatUI](https://namethatui.com/) 这个站解决什么问题、值不值得收进参考清单？

## 简答

它是 UI 元素的"视觉词典"：用大白话描述界面上那个东西（"the gray text inside the box that disappears when you type"），返回正式名称、代码符号和可直接粘贴给 coding agent 的 prompt。值得收，但定位是**参考站**，不是术语规范。

## 综合结论

- **核心机制**：76 个词条（Web 44 + macOS 32），每个词条把一个 UI 元素拆成 anatomy（每部分给正式名和代码符号，如 toast viewport = `Toaster`、消息本体 = `role="status"`），并给出别名和口语说法映射（"If you called it…"）。方法论上对照三层权威来源：平台 HIG 的用户可见名、框架文档的代码符号、WAI-ARIA/APG/WCAG 的可访问角色；命名冲突时不假装存在通用名，而是把平台名挂在术语上（macOS Sheet ≠ Web Sheet）。
- **真正的差异点是 agent prompt**：每个词条自带 "Prompt — paste into your agent"（含行为约束，如 toast 要在 hover/键盘聚焦时暂停自动消失计时）和 "Debug prompt"（列经典失败模式，如缺 `aria-live` 导致屏幕阅读器不播报）。它服务的是"用精确术语写实现 prompt"的工作流，而不只是查词典。
- **适用场景**：
  - 给 agent 写 UI 实现 prompt 前，查正式名和现成 prompt；
  - 评审 / 设计系统对齐时统一叫法（[/vs](https://namethatui.com/vs) 收了 18 组易混词：Popover vs Dropdown vs Tooltip、Switch vs Checkbox vs Radio、Skeleton vs Empty State 等）；
  - macOS 原生开发查 AppKit/SwiftUI 符号，另有 [/translate](https://namethatui.com/translate) 的 60+ 元素对照表。
- **与 [[wiki/topics/frontend/Transitions.dev|Transitions.dev]] 互补**：一个管"叫什么"，一个管"怎么动"，都挂在 frontend 参考清单里。
- **局限**：词条覆盖仍少，冷门控件可能查不到；macOS 部分对纯 web 项目用处小；它是参考而非规范，团队术语仍以自己的设计系统为准，用它补充别名和可访问性符号。
- **姊妹站**：/styles（Name That Vibe）是 UI 设计风格图鉴，解决"这个界面是什么风"，沉淀为 [[UI 设计风格]]。

## 未决问题

- 词条量增长后（有 RSS 可订阅），是否值得把高频术语对照沉淀成本库自己的 synthesis，而不是每次外链。
- 团队设计系统命名与站内术语冲突时的取舍，还没有单独的 comparison 页。

## 来源指针

- `raw/sources/2026-08-13-namethatui.md`
- https://namethatui.com/
- https://namethatui.com/methodology
- https://namethatui.com/vs
