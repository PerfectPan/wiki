---
title: Transitions.dev
description: Product UI 动效菜谱参考站；写动画时查阅，不作为全局 agent skill 常驻。
type: topic
category: frontend
status: seed
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

[Transitions.dev](https://transitions.dev/) 是一套可交互的 product UI transition 菜谱站（约 20+ 种：modal、dropdown、badge、tabs、skeleton、accordion 等）。主用法是打开网站看观感、复制 CSS；它也提供 agent skill，但本库选择 **当参考站沉淀，不当全局常驻 skill**。

## 何时打开

- 做微交互：notification badge、dropdown / modal 开合、icon swap、success check
- 做 loading / 状态反馈：skeleton、shimmer text、error shake
- 做分段控件或面板：sliding tabs、panel reveal、accordion
- 想对照「业界常见动效长什么样」再落到自己的 token / Tailwind 体系

## 何时不依赖它

| 需求 | 看哪里 |
| --- | --- |
| 布局状态切换怎么动画、为什么用 transform | [[wiki/syntheses/frontend/FLIP 布局动画的心智模型\|FLIP 布局动画的心智模型]] |
| 动效观感 / 时序是否对 | 浏览器实测（例如 verifying-animation-timing 一类流程） |
| 整体 UI 方向与打磨 | frontend-design / impeccable 等设计 skill，而不是抄 `t-*` 菜谱 |

## 与 agent skill 的边界

- **默认**：不把 `transitions-dev` 写进跨机 skill manifest，不在每台机器、每个 agent 常驻安装。
- **临时**：某次任务需要 agent 直接套菜谱时，可 `npx skills add Jakubantalik/transitions.dev`，用完可卸。
- **原因**：本库日常以内容站 / 工具向 UI 为主，全量常驻 skill 噪音大于收益；菜谱站本身可外链查阅，不必再复制一份进 agent 目录。

## 使用注意

- 站点 snippet 使用 `t-*` 与自有 CSS 变量，接入项目时通常要改成现有 design token / Tailwind 语义，不要整包硬贴。
- 复制时保留 `prefers-reduced-motion` 分支。
- 不要把「有过渡」当成默认目标；没有信息价值的动效应省略。

## Related Pages

- [[wiki/syntheses/frontend/FLIP 布局动画的心智模型|FLIP 布局动画的心智模型]]
- [[wiki/topics/frontend/CSS|CSS]]

## Source Pointers

- `raw/sources/2026-07-26-transitions-dev.md`
- https://transitions.dev/
- https://transitions.dev/skill.html
- https://github.com/Jakubantalik/transitions.dev
