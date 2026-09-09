---
title: Awesome Component Libraries
description: 组件库与动效参考的 curated 收录索引：推荐 / 可参考 / 偏薄 + raw 素材指针；判据与素材分离，不镜像全文。
type: topic
category: frontend
created: 2026-09-09
updated: 2026-09-09
timestamp: 2026-09-09
tags:
  - catalog
  - component-library
  - animation
  - reference
source_refs:
  - raw/sources/2026-09-09-rare-ui.md
  - raw/sources/2026-07-26-transitions-dev.md
  - raw/sources/2026-05-08-custom-scrollbar-library-source-review.md
  - wiki/syntheses/frontend/shadcn Registry 组件分发模式.md
  - wiki/comparisons/frontend/自定义滚动条库选型：OverlayScrollbars vs SimpleBar vs Perfect Scrollbar.md
  - https://www.rareui.com/
  - https://transitions.dev/
resource:
  - raw/sources/2026-09-09-rare-ui.md
  - raw/sources/2026-07-26-transitions-dev.md
  - raw/sources/2026-05-08-custom-scrollbar-library-source-review.md
  - wiki/syntheses/frontend/shadcn Registry 组件分发模式.md
  - wiki/comparisons/frontend/自定义滚动条库选型：OverlayScrollbars vs SimpleBar vs Perfect Scrollbar.md
  - https://www.rareui.com/
  - https://transitions.dev/
---

# Awesome Component Libraries

## 摘要

这是本 wiki 的**组件库 / 动效参考收录索引**（awesome 语义：curated list，不是 star 排行榜，不是全网镜像）。每个条目 = 一句话价值 + 分级 + 指针；素材与评审放在 `raw/sources/`，细节放在各对象自己的页面，本文不镜像全文。结构遵循 [[SCHEMA.md|SCHEMA]] 的「收录页约定」；同构先例见 [[Awesome Agent Skills]]（skill 领域）。

## 收录规则

每条候选至少要能回答：

1. **触发**：什么时候该来抄 / 参考它
2. **交付形态**：单文件（shadcn registry 式）/ npm 依赖、依赖栈（React? Motion? WebGL?）
3. **许可与归属**：能否商用；是否复刻作品、需要自查署名
4. **硬注意点**：SSR、WebGL、`prefers-reduced-motion`、是否跟随上游更新
5. **分级理由**：推荐 / 可参考 / 偏薄

流程：`候选 → raw 素材 / 评审 → 对照分级 → 本文加一行`。未过线的链接堆、摘录留在 `raw/sources/` 或进下面的候选池，不进索引。

判据说明：组件库领域暂无独立判据页，判据内联在本文「分级」；条目积累到约 8 个或出现分级争议时，按 SCHEMA 收录页约定拆成独立 synthesis 判据页，本文只留指针。

## 分级

| 档 | 含义 |
| --- | --- |
| **推荐** | 可直接抄进项目的成品质量高；文档（Props / 交互 / 安装）完整；许可明确可商用；或有范式价值 |
| **可参考** | 有真实可抄价值，但有短板：复刻归属需自查、依赖较重或需实测、文档偏薄 |
| **偏薄** | 只有链接 / 简介级信息，无 raw 素材或实测；默认不装，只作反例或起点 |

## 索引

### 推荐

| 库 | 一句话 | 指针 |
| --- | --- | --- |
| **Transitions.dev** | product UI 微交互的 CSS 动效菜谱（modal / dropdown / badge / skeleton 等 20+）；`t-*` 命名 + `prefers-reduced-motion`，写微交互时的观感与 snippet 参考 | [[wiki/topics/frontend/Transitions.dev|topic]] · `raw/sources/2026-07-26-transitions-dev.md` |

### 可参考

| 库 | 一句话 | 指针 |
| --- | --- | --- |
| **Rare UI** | React + Motion「稀有动效」组件库约 19 个（fluid orb / gooey nav / OTP input / gravity letters 等）；shadcn CLI 单文件分发、MIT；短板：多数为网上作品的复刻，商用前需按站内 Credits 自查归属，WebGL 组件需实测 | [官网](https://www.rareui.com/) · [components](https://www.rareui.com/components) · [GitHub](https://github.com/swamimalode07/rare-ui) · `raw/sources/2026-09-09-rare-ui.md` |
| **滚动条三件套** | OverlayScrollbars / SimpleBar / Perfect Scrollbar：横向选型已闭环，以 comparison 的取舍结论为准，本页只作召回入口 | [[wiki/comparisons/frontend/自定义滚动条库选型：OverlayScrollbars vs SimpleBar vs Perfect Scrollbar|comparison]] · `raw/sources/2026-05-08-custom-scrollbar-library-source-review.md` |

### 偏薄

（暂无挂名条目。）

## 明确不收

- 无 raw 素材、只有 star 数或营销页的链接（先补素材再谈收录）
- 纯 npm 重型框架组件库（MUI / Chakra 一类）——只当依赖使用时不构成收录；出现选型需求时走 comparison
- `raw/sources/Component Library.md`（旧 Logseq 遗留 4 行链接清单：ant-design/pro-editor、headlessui、fancycomponents）——未评审，停留在 raw

## 候选池（待 raw 评审，慢慢收录）

shadcn 生态动效组件站：Skiper UI、Aceternity UI、Magic UI、ReactBits、Animata、Origin UI、motion-primitives；旧清单遗留：ant-design/pro-editor、Headless UI、Fancy Components。

每项进索引前需补齐：raw 素材 → 对照分级 → 在 PR body 写明分级理由。

## 相关页面

- [[wiki/syntheses/frontend/shadcn Registry 组件分发模式|shadcn Registry 组件分发模式]] —— 本索引多数条目依赖的分发机制
- [[wiki/topics/frontend/Transitions.dev|Transitions.dev]]
- [[wiki/topics/design/界面质感细节|界面质感细节]] —— 动效组的「可抄成品」入口
- [[wiki/topics/ai/Awesome Agent Skills|Awesome Agent Skills]] —— 同构先例（skill 领域）
- [[SCHEMA.md|SCHEMA]] 收录页约定

## 来源指针

- `raw/sources/2026-09-09-rare-ui.md`（Rare UI 合并素材：官网首页 / 组件列表 / GitHub 元信息 / 两个组件页抽查）
- `raw/sources/2026-07-26-transitions-dev.md`
- `raw/sources/2026-05-08-custom-scrollbar-library-source-review.md`
- https://www.rareui.com/
- https://transitions.dev/
- [[wiki/syntheses/frontend/shadcn Registry 组件分发模式|shadcn Registry 组件分发模式]]
- [[wiki/comparisons/frontend/自定义滚动条库选型：OverlayScrollbars vs SimpleBar vs Perfect Scrollbar|自定义滚动条库选型]]
