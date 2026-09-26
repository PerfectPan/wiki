---
title: Awesome Prompts
description: 经判据审过的提示词薄索引：推荐 / 可参考 / 偏薄；正文存在 prompts/，这里只留一句话与指针
type: topic
category: ai
created: 2026-09-22
updated: 2026-09-22
timestamp: 2026-09-22
tags:
  - catalog
  - prompt
  - agent
source_refs:
  - wiki/topics/ai/Prompt.md
  - prompts/README.md
  - raw/sources/2026-09-22-lenny-world-class-designer.md
  - raw/sources/Prompt.md
  - https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world
resource:
  - wiki/topics/ai/Prompt.md
  - prompts/README.md
  - raw/sources/2026-09-22-lenny-world-class-designer.md
  - raw/sources/Prompt.md
  - https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world
---
# Awesome Prompts

## 摘要

这是本 wiki 的**提示词收录索引**，不是判据正文，也不是提示词仓库。

- **原文**在 `prompts/<id>.md`，一条一个文件，正文原样复制；用 `bin/wiki prompts show <id>` 直接打印。
- **判据**在 [[Prompt]]：什么提示词值得留存、推荐 / 可参考 / 偏薄各自的标准。
- **本页**只收「过线或有教学价值」的条目：一句话价值 + 分级 + 指针，方便在 GitHub 上浏览。

机器召回走 `bin/wiki prompts list --tag <tag>`（或 `--json`），本页是人读的那一层；`bin/wiki prompts check` 会提醒本页是否漏收。

## 收录规则

每条候选至少能回答：

1. **触发**：什么时候该用它（场景，不是功能广告）
2. **原文位置**：原文在哪（`raw/sources/` 的素材 + `prompts/<id>.md` 的逐字副本）
3. **硬 gotcha**：套用它时模型会稳定踩的坑
4. **怎么判断有没有用**：可观察的验收信号（哪怕弱，但不能为零）
5. **分级理由**：推荐 / 可参考 / 偏薄

流程：`候选 → raw 素材（原文）→ prompts/<id>.md（逐字副本 + 元数据）→ 对照判据分级 → 本页加一行 → PR`。

## 分级

三档标准由 [[Prompt]] 定义，本页只按档分组：

| 级 | 含义（简） |
| --- | --- |
| **推荐** | 结构完整、边界清楚、有失败模式说明，可长期复用 |
| **可参考** | 思路值得借，但要按自己的场景补齐取值、边界或验收 |
| **偏薄** | 只有口号或人格设定，缺产物约定；仅作反例或起点 |

## 索引

### 推荐

| 提示词 | 一句话价值 | 指针 |
| --- | --- | --- |
| **seed-string** | 让模型先用 shell 生成随机串再据此定配色、版式、字体，把它从不属于自己的「最可能 token」路径上推开；直接说「完全随机」没用，模型会把随机演成另一套默认 | [[prompts/seed-string\|原文]] · [[raw/sources/2026-09-22-lenny-world-class-designer.md\|素材]] |
| **design-critic-subagent** | 截图交给全新上下文的 critic（不带代码与历史），让它对标顶级工作室的执行并打 0–10 分；把「够不够好」从自评变成外部判决，实现者用便宜模型、critic 用强模型 | [[prompts/design-critic-subagent\|原文]] · [[raw/sources/2026-09-22-lenny-world-class-designer.md\|素材]] |
| **design-direction-hunt** | 先用 AI 列表式铺开点子 → 自己挑几条并说清喜欢/讨厌什么 → 再让 AI 把方向写成可执行 prompt；跳过中间那步，拿到的还是人人可得的东西 | [[prompts/design-direction-hunt\|原文]] · [[raw/sources/2026-09-22-lenny-world-class-designer.md\|素材]] |
| **dial-back-restraint** | 收尾时逐条点名要删的东西（渐变、发光、多余容器、自造控件换系统原生化）；模型只会加不会减，多数 AI 味来自没人让它删 | [[prompts/dial-back-restraint\|原文]] · [[raw/sources/2026-09-22-lenny-world-class-designer.md\|素材]] |

### 可参考

| 提示词 | 一句话价值 | 指针 |
| --- | --- | --- |
| **ambitious-direction-examples** | 把具体灵感（像素游戏静帧感、等距 3D 城市、激进非对称）写进 prompt，比「好看一点」有效得多；但方向得来自你自己的品味，照抄示例仍会趋同 | [[prompts/ambitious-direction-examples\|原文]] |
| **image-generation-pass** | 让 agent 调图像模型替代渐变和基础形状；含三条接入路径，以及把 key 放进 gitignored 文件并在 AGENTS.md 写明「仅供开发、不得随产品发布」的用法 | [[prompts/image-generation-pass\|原文]] |
| **video-loop-chroma-key** | 用纯色背景渲染循环视频再 chroma key 或 matting 抠掉背景，得到能叠在 UI 上的动效；玻璃折射要先把页面背景渲进去再抠 | [[prompts/video-loop-chroma-key\|原文]] |
| **keyframe-transition-scrub** | 用上一段视频的末帧作为下一段的起始帧接续，实现随滚动 scrub 的状态切换；依赖物理与一致性强的视频模型 | [[prompts/keyframe-transition-scrub\|原文]] |
| **plan-first** | 要求 agent 先读仓库约定与相似实现、有歧义先提问，再输出带文件树（NEW / UPDATE / DELETE）和逐文件改动说明的计划，最后才动代码 | [[prompts/plan-first\|原文]] · [[raw/sources/Prompt.md\|原始素材]] |

### 偏薄

| 提示词 | 一句话价值 | 指针 |
| --- | --- | --- |
| **negative-random-ask** | 反例：要求「完全随机」之后，配色、结构和同一个陶器隐喻仍在重复——模型的随机是被预测出来的随机 | [[prompts/negative-random-ask\|原文]] |

## 明确不收

- 只有人格、文风或「你是世界顶级 XX」设定的提示词，没有产物约定
- 说不清什么时候该用的提示词（没有触发场景）
- 来源不可追溯的复制粘贴，尤其是二手转述、丢失原始出处的
- 依赖私有密钥、账号或付费额度但没写清成本和授权边界的链路（写清了可以收）
- 单纯的「提示词技巧清单」摘录：先放 `raw/sources/`，整理出原文与边界再入库

## 相关页面

- [[Prompt]] — 唯一判据源（收录标准与三档定义）
- [[AI Slop]] — 「AI 味」的语义层归纳，多数提示词的靶子
- [[Claude 5 时代的上下文工程]] — 提示词之外的另一半：上下文组织
- [[Awesome Agent Skills]] — 提示词升级成带脚本、manifest、QA 的 skill
- [[Awesome Component Libraries]]

## 来源指针

- `raw/sources/2026-09-22-lenny-world-class-designer.md`
- `raw/sources/Prompt.md`
- `prompts/README.md`
- https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world
