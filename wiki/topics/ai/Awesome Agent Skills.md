---
title: Awesome Agent Skills
description: 经判据审过的 Agent Skill 薄索引：推荐 / 可参考 / 偏薄，链到评审与范式页，不镜像全文
type: topic
category: ai
created: 2026-08-06
updated: 2026-09-01
timestamp: 2026-09-01
tags:
  - skills
  - agent
  - awesome
  - catalog
source_refs:
  - wiki/syntheses/ai/Skill 工程化的产物协议范式.md
  - raw/sources/2026-08-06-bento-slides-skill-review.md
  - raw/sources/2026-05-12-ai-cli-skill-review.md
  - raw/sources/2026-05-06-codex-pet-skill-article.md
  - raw/sources/2026-09-01-mono-color-skill-review.md
  - raw/sources/2026-09-01-hallmark-skill-review.md
resource:
  - wiki/syntheses/ai/Skill 工程化的产物协议范式.md
  - raw/sources/2026-08-06-bento-slides-skill-review.md
  - raw/sources/2026-05-12-ai-cli-skill-review.md
  - raw/sources/2026-05-06-codex-pet-skill-article.md
  - raw/sources/2026-09-01-mono-color-skill-review.md
  - raw/sources/2026-09-01-hallmark-skill-review.md
---
# Awesome Agent Skills

## 摘要

这是本 wiki 的 **Skill 收录索引**，不是判据正文，也不是全网镜像。

- **判据**只在 [[Skill 工程化的产物协议范式]]：产物协议、路由 description、gotcha、QA、manifest、负例等。
- **本页**只收「过线或有教学价值」的条目：一句话价值 + 分级 + 指针。
- 未过判据的链接堆、摘录 → `raw/sources/`，不进本表。

命名用 Awesome，语义是 **curated list**，不是 star 排行榜。

## 收录规则

每条候选至少能回答：

1. **触发**：何时该加载（description 场景，不是功能广告）
2. **产物协议**：最终交什么、谁消费
3. **硬 gotcha**：模型会稳定踩的坑
4. **验收**：结构 / 语义怎么验（可弱，但不能为零）
5. **分级理由**：推荐 / 可参考 / 偏薄

流程：`候选 → raw 评审笔记 → 对照判据分级 → 本页加一行`。产品本身另开 topic 时与 Skill 条目解耦。

### 分级

| 级 | 含义 |
| --- | --- |
| **推荐** | 强产物契约 + 高价值 gotcha；可当工程范例或长期安装 |
| **可参考** | 有真实约束，但缺默认协议 / QA / 负例中的多项 |
| **偏薄** | 基本是 README 摘要；仅作反例或起点，默认不装 |

## 索引

### 推荐

| Skill | 一句话 | 指针 |
| --- | --- | --- |
| **bento-slides** | 只改 `#bento-doc` JSON 做单文件 deck；强制内容→chart/morph/state 映射，反 bullet 墙 | 产品 [[Bento]] · [SKILL.md](https://github.com/nyblnet/bento/blob/main/plugins/bento-slides/skills/bento-slides/SKILL.md) · [[raw/sources/2026-08-06-bento-slides-skill-review.md\|评审]] |
| **hatch-pet**（范式锚点） | 图像生成收成可加载资产流水线：manifest、确定性编译、QA、局部 repair | [[Skill 工程化的产物协议范式]] · [[raw/sources/2026-05-06-codex-pet-skill-article.md\|来源]] |
| **mono-color** | 视觉系统约束型：design-system catalog 约束取值（catalog wins）+ 可枚举 Quality Gate + 原创性防火墙（≥4 结构变量）；evals 带 assertions 进 CI | [SKILL.md](https://github.com/yanliudesign/mono-color-skill/blob/main/SKILL.md) · [[raw/sources/2026-09-01-mono-color-skill-review.md\|评审]] |
| **hallmark** | 反 AI-slop 建页：宏结构优先（21 种，拒绝重复最近 3 个）+ 58 道交付门禁 + study 提结构不提像素；audit 把 QA 做成动词 | [SKILL.md](https://github.com/nutlope/hallmark/blob/main/skills/hallmark/SKILL.md) · [[raw/sources/2026-09-01-hallmark-skill-review.md\|评审]] · [[AI Slop]] |

### 可参考

| Skill | 一句话 | 指针 |
| --- | --- | --- |
| **ai-cli** | 工具边界与 `-o` 防二进制污染 stdout 有 gotcha；默认协议 / 成本 / 失败 / 负例仍薄 | [[ai-cli]] · [[raw/sources/2026-05-12-ai-cli-skill-review.md\|评审]] |

### 偏薄

（暂无单独挂名条目。判据页用 ai-cli 说明「可用但不老练」时，可下沉到本级。）

## 明确不收

- 仅人格 / 文风、无产物契约的 prompt 包
- 无 description 路由、无 gotcha 的命令备忘
- 未写 raw 评审、只有 star 数或营销页的链接
- 本仓库自己的 agent 工作流（统一走 `bin/wiki`，不进 Skill 市场镜像）

## 相关页面

- [[Skill 工程化的产物协议范式]] — 唯一判据源
- [[AI Slop]] — hallmark 反模式的语义层归纳
- [[Bento]] — bento-slides 背后的单文件 slides 产品
- [[Code Agent]]
- [[ai-cli]]
- [[Agent-native 生成型 CLI 的产物协议]]

## 来源指针

- `raw/sources/2026-09-01-hallmark-skill-review.md`
- `raw/sources/2026-09-01-mono-color-skill-review.md`
- `raw/sources/2026-08-06-bento-slides-skill-review.md`
- `raw/sources/2026-05-12-ai-cli-skill-review.md`
- `raw/sources/2026-05-06-codex-pet-skill-article.md`
- https://github.com/nyblnet/bento
- https://github.com/yanliudesign/mono-color-skill
- https://github.com/nutlope/hallmark
