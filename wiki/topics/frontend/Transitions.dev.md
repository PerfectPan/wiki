---
title: Transitions.dev
description: Product UI 动效菜谱参考站；写动画时查阅、复制 CSS。
type: topic
category: frontend
created: 2026-07-26
updated: 2026-07-26
timestamp: 2026-07-26
tags:
  - animation
  - motion
  - css
  - ux
  - reference
source_refs:
  - raw/sources/2026-07-26-transitions-dev.md
  - https://transitions.dev/
  - https://transitions.dev/skill.html
  - https://github.com/Jakubantalik/transitions.dev
resource:
  - raw/sources/2026-07-26-transitions-dev.md
  - https://transitions.dev/
  - https://transitions.dev/skill.html
  - https://github.com/Jakubantalik/transitions.dev
---

# Transitions.dev

## 摘要

[Transitions.dev](https://transitions.dev/) 是一套可交互的 product UI transition 菜谱站（约 20+ 种：modal、dropdown、badge、tabs、skeleton、accordion 等）。主用法是打开网站看观感、复制 CSS；入口挂在 [[wiki/topics/frontend/CSS|CSS]] 的参考清单里。

## 何时打开

- 做微交互：notification badge、dropdown / modal 开合、icon swap、success check
- 做 loading / 状态反馈：skeleton、shimmer text、error shake
- 做分段控件或面板：sliding tabs、panel reveal、accordion
- 想对照「业界常见动效长什么样」再落到自己的 token / Tailwind 体系

## 何时不依赖它

- 布局状态切换的心智与性能模型（为什么用 transform 做补偿）——需要单独的布局动画笔记，不在本站覆盖范围。
- 动效观感 / 时序是否对——浏览器实测，而不是再抄一份 snippet。
- 整体 UI 方向与打磨——frontend-design / impeccable 一类设计 skill，而不是默认套 `t-*` 菜谱。

## 使用注意

- 站点 snippet 使用 `t-*` 与自有 CSS 变量，接入项目时通常要改成现有 design token / Tailwind 语义，不要整包硬贴。
- 复制时保留 `prefers-reduced-motion` 分支。
- 不要把「有过渡」当成默认目标；没有信息价值的动效应省略。

## Related Pages

- [[wiki/topics/frontend/CSS|CSS]]

## Source Pointers

- `raw/sources/2026-07-26-transitions-dev.md`
- https://transitions.dev/
- https://transitions.dev/skill.html
- https://github.com/Jakubantalik/transitions.dev
