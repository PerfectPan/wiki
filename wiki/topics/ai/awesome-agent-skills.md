---
title: Awesome Agent Skills
description: 按推荐、可参考、偏薄收录 Agent skill，附用途、来源与相关分析。
type: topic
category: ai
created: 2026-08-06
updated: 2026-10-07
timestamp: 2026-10-07
tags:
  - skills
  - agent
  - awesome
  - catalog
source_refs:
  - wiki/syntheses/ai/skill-engineering-artifact-protocol.md
  - raw/sources/2026-08-06-bento-slides-skill-review.md
  - raw/sources/2026-05-12-ai-cli-skill-review.md
  - raw/sources/2026-05-06-codex-pet-skill-article.md
  - raw/sources/2026-09-01-mono-color-skill-review.md
  - raw/sources/2026-09-01-hallmark-skill-review.md
  - raw/sources/2026-09-22-handdraw-style-prompter-review.md
  - raw/sources/2026-09-22-hand-drawn-explainer-video-nikola-review.md
resource:
  - wiki/syntheses/ai/skill-engineering-artifact-protocol.md
  - raw/sources/2026-08-06-bento-slides-skill-review.md
  - raw/sources/2026-05-12-ai-cli-skill-review.md
  - raw/sources/2026-05-06-codex-pet-skill-article.md
  - raw/sources/2026-09-01-mono-color-skill-review.md
  - raw/sources/2026-09-01-hallmark-skill-review.md
  - raw/sources/2026-09-22-handdraw-style-prompter-review.md
  - raw/sources/2026-09-22-hand-drawn-explainer-video-nikola-review.md
---
# Awesome Agent Skills

## 摘要

这里收录具有使用或学习价值的外部 Agent skill，每项保留用途、分级和来源。理解 skill 的设计方法，可阅读 [[skill-engineering-artifact-protocol|Skill 的交付内容与结果检查]]。

## 分级

| 级 | 含义 |
| --- | --- |
| **推荐** | 交付内容和结果检查清楚，包含值得借鉴的具体做法 |
| **可参考** | 有明确用途，但执行限制、结果检查等说明不完整 |
| **偏薄** | 只适合作为起点或反例，不建议直接安装 |

## 索引

### 推荐

| Skill | 一句话 | 指针 |
| --- | --- | --- |
| **bento-slides** | 只改 `#bento-doc` JSON 做单文件 deck；强制内容→chart/morph/state 映射，反 bullet 墙 | 产品 [[bento]] · [SKILL.md](https://github.com/nyblnet/bento/blob/main/plugins/bento-slides/skills/bento-slides/SKILL.md) · [[raw/sources/2026-08-06-bento-slides-skill-review.md\|评审]] |
| **hatch-pet**（范式锚点） | 图像生成收成可加载资产流水线：manifest、确定性编译、QA、局部 repair | [[skill-engineering-artifact-protocol]] · [[raw/sources/2026-05-06-codex-pet-skill-article.md\|来源]] |
| **mono-color** | 生成单墨/双色印刷风图像：把色板、布局、排版等取值写进 JSON 目录，交付前过 20 项 checklist，"不抄参考"变成 10 个结构变量至少改 4 个；evals 带断言进 CI | [SKILL.md](https://github.com/yanliudesign/mono-color-skill/blob/main/SKILL.md) · [[raw/sources/2026-09-01-mono-color-skill-review.md\|评审]] |
| **hallmark** | 反 AI-slop 建页：先选页面结构（21 种，不重复最近 3 个），交付前过 58 项检查；`study` 只提取结构不抄像素，`audit` 只诊断不改 | [SKILL.md](https://github.com/nutlope/hallmark/blob/main/skills/hallmark/SKILL.md) · [[raw/sources/2026-09-01-hallmark-skill-review.md\|评审]] · [[ai-slop]] |
| **handdraw-style-prompter** | 274 个风格编号 + 118 条排版图型出中英双语提示词；模型能力清单决定要不要垫图，未知一律兜底，参考图带「只抽画风、不沿用主体」隔离声明，378 行脚本校验数据与资产不变量 | [SKILL.md](https://github.com/yang0/handraw-style/blob/master/skills/handdraw-style-prompter/SKILL.md) · [[raw/sources/2026-09-22-handdraw-style-prompter-review.md\|评审]] |
| **hand-drawn-explainer-video-nikola** | 中文手绘讲解视频：两条不可混称的路线（逐笔落墨 / 程序动画），交付真实 MP4 + SRT + 时间轴 + 可编辑工程；13 条含反例的 evals，验收要求看边界帧并声明自动检查管不了语义 | [SKILL.md](https://github.com/hi-nikola/hand-drawn-explainer-video-nikola/blob/main/SKILL.md) · [[raw/sources/2026-09-22-hand-drawn-explainer-video-nikola-review.md\|评审]] · [[hand-drawn-style-explainer-video-constraints]] |

### 可参考

| Skill | 一句话 | 指针 |
| --- | --- | --- |
| **ai-cli** | 工具边界与 `-o` 防二进制污染 stdout 有 gotcha；默认协议 / 成本 / 失败 / 负例仍薄 | [[ai-cli]] · [[raw/sources/2026-05-12-ai-cli-skill-review.md\|评审]] |

### 偏薄

（暂无单独挂名条目。判据页用 ai-cli 说明「可用但不老练」时，可下沉到本级。）

## 相关页面

- [[skill-engineering-artifact-protocol]] — Skill 设计方法与案例
- [[hand-drawn-style-explainer-video-constraints]] — 两个手绘类案例的域内综合
- [[ai-slop]] — hallmark 反模式的语义层归纳
- [[bento]] — bento-slides 背后的单文件 slides 产品
- [[code-agent]]
- [[ai-cli]]
- [[agent-native-generative-cli-artifact-protocol]]

## 来源指针

- `raw/sources/2026-09-01-hallmark-skill-review.md`
- `raw/sources/2026-09-01-mono-color-skill-review.md`
- `raw/sources/2026-08-06-bento-slides-skill-review.md`
- `raw/sources/2026-05-12-ai-cli-skill-review.md`
- `raw/sources/2026-05-06-codex-pet-skill-article.md`
- `raw/sources/2026-09-22-handdraw-style-prompter-review.md`
- `raw/sources/2026-09-22-hand-drawn-explainer-video-nikola-review.md`
- https://github.com/nyblnet/bento
- https://github.com/yanliudesign/mono-color-skill
- https://github.com/nutlope/hallmark
- https://github.com/yang0/handraw-style
- https://github.com/hi-nikola/hand-drawn-explainer-video-nikola
