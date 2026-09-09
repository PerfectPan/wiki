---
title: Rare UI
description: 免费开源的动画 React 组件库（约 19 个）；单文件 + shadcn CLI 分发、基于 Motion，作为“稀有组件”的参考与复制源。
type: topic
category: frontend
created: 2026-09-09
updated: 2026-09-09
timestamp: 2026-09-09
tags:
  - react
  - motion
  - animation
  - shadcn
  - component-library
source_refs:
  - raw/sources/2026-09-09-rare-ui-home.md
  - raw/sources/2026-09-09-rare-ui-components.md
  - raw/sources/2026-09-09-rare-ui.md
  - raw/sources/2026-09-09-rare-ui-fluid-orb.md
  - raw/sources/2026-09-09-rare-ui-otp-input.md
  - https://www.rareui.com/
  - https://www.rareui.com/components
  - https://github.com/swamimalode07/rare-ui
resource:
  - raw/sources/2026-09-09-rare-ui-home.md
  - raw/sources/2026-09-09-rare-ui-components.md
  - raw/sources/2026-09-09-rare-ui.md
  - raw/sources/2026-09-09-rare-ui-fluid-orb.md
  - raw/sources/2026-09-09-rare-ui-otp-input.md
  - https://www.rareui.com/
  - https://www.rareui.com/components
  - https://github.com/swamimalode07/rare-ui
---

# Rare UI

## 摘要

[Rare UI](https://www.rareui.com/) 是一个免费开源的“稀有动画”React 组件库（GitHub: `swamimalode07/rare-ui`，MIT，收录时约 887 stars）。定位与 [[wiki/syntheses/frontend/shadcn Registry 组件分发模式|shadcn Registry]] 一致：每个组件是“你拥有的单文件，而不是安装的依赖”，通过 shadcn CLI 直接分发进项目，适合想要少见而有质感动效的产品页、portfolio 与 AI 类产品界面。

## 关键点

- **组件构成**：约 19 个组件，按类别展示：Display（Folder component、Code Block、Gravity Letters、GitHub activity、Step player、Animated counter）、AI kit（Fluid Orb、Grid Reveal、Matrix orb）、Navigation（Bounce sidebar、Hook Sidebar、Proximity Sidebar、Scroll Progress、Gooey nav）、Inputs（Duration Picker、OTP Input、Delete button）、Feedback（Emoji reaction、Notification bell）。
- **分发模式**：每个组件一个文件，用 `npx shadcn@latest add swamimalode07/rare-ui/<component>` 安装，可用任意包管理器；官方口径是“add it with the shadcn CLI, using any package manager you like”。
- **技术栈**：React + TypeScript；组件依赖 `motion`（OTP Input 页面明确标注 Dependencies: motion）；Fluid Orb 这类用 WebGL 实现“drifting fluid shading”流体质感；支持 `prefers-reduced-motion`（Ambient 类交互在 reduced-motion 下停在一帧静止画面）。
- **组件页结构**：每个组件页都有 Interaction Type（交互类型描述）、Props 表、Installation、用法 snippet、Source Code 查看入口和 Credits。Props 做得比较完整，例如 OTP Input 有 `length` / `value` / `onComplete` / `status(idle|success|error)` / `mask` 等受控与反馈状态。
- **来源与许可**：站点明确说明“大多数组件是对网上优秀作品的复刻/逆向工程并加料，不声称原创、会尽量署名”（如 Fluid Orb 灵感来自 ChatGPT voice mode）；GitHub 仓库为 MIT；站内许可条款为个人与商业免费可用、使用组件时署名被感谢但不强制、不要把组件当自己的 kit 转售。
- **收录判断**：它是“看观感 + 复制代码进自己项目”的参考型资源库，用法接近 [[wiki/topics/frontend/Transitions.dev|Transitions.dev]]，而不是传统意义上安装更新的 npm 依赖。

## 何时打开

- 需要产品里少见的装饰性/氛围动效：fluid orb（ChatGPT voice mode 风格）、gooey nav、gravity letters。
- 做 portfolio、landing page 或 AI 产品界面，想要“立刻能用的精致交互原语”，参考别人已打磨好的实现再落到自己的 token 体系。
- 想找一个交互状态齐全的输入类组件做参照（如带 caret 滑动 + 校验反馈的 OTP Input）。

## 使用注意

- **复制后自维护**：单文件拷贝进项目意味着不随上游更新，和 shadcn registry 模式的取舍一致，引用组件前先想清楚是否愿意自维护。
- **来源自查**：作者自述多数是复刻作品；对版权/署名敏感的产品场景，先顺着站内 Credits 找到原始灵感再决定是否使用。
- **依赖与运行环境**：组件依赖 `motion`，WebGL 组件（如 Fluid Orb）在 SSR、低端设备或弱 GPU 环境要先实测。
- **动效克制**：保留 `prefers-reduced-motion` 分支；不要为了“有动画”而堆动效，参考站的价值是让你先看观感再决定。

## 相关页面

- [[wiki/topics/frontend/Transitions.dev|Transitions.dev]]
- [[wiki/syntheses/frontend/shadcn Registry 组件分发模式|shadcn Registry 组件分发模式]]
- [[wiki/topics/frontend/React|React]]
- [[wiki/topics/frontend/CSS|CSS]]

## 来源指针

- `raw/sources/2026-09-09-rare-ui-home.md`（首页：定位、安装命令、组件数、评价）
- `raw/sources/2026-09-09-rare-ui-components.md`（组件列表页）
- `raw/sources/2026-09-09-rare-ui.md`（GitHub 仓库元信息：MIT、TypeScript、stars）
- `raw/sources/2026-09-09-rare-ui-fluid-orb.md`、`raw/sources/2026-09-09-rare-ui-otp-input.md`（代表性组件页）
- https://www.rareui.com/
- https://www.rareui.com/components
- https://github.com/swamimalode07/rare-ui
