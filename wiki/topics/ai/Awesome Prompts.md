---
title: Awesome Prompts
description: 经判据审过的提示词薄索引：推荐 / 可参考 / 偏薄，链到原文与判据页，不镜像全文
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
  - raw/sources/2026-09-22-lenny-world-class-designer.md
  - raw/sources/Prompt.md
  - https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world
resource:
  - wiki/topics/ai/Prompt.md
  - raw/sources/2026-09-22-lenny-world-class-designer.md
  - raw/sources/Prompt.md
  - https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world
---
# Awesome Prompts

## 摘要

这是本 wiki 的**提示词收录索引**，不是判据正文，也不是提示词全文仓库。

- **判据**在 [[Prompt]]：什么时候算一条值得留存的提示词、推荐 / 可参考 / 偏薄是什么标准。
- **本页**只收「过线或有教学价值」的条目：一句话价值 + 分级 + 指针。
- **提示词原文**存在 `raw/sources/` 的素材里（文章、笔记），本页只给指针，不复制全文。

命名用 Awesome，语义是 **curated list**：能被召回的清单，不是提示词大全。

## 收录规则

每条候选至少能回答：

1. **触发**：什么时候该用它（场景，不是功能广告）
2. **原文位置**：提示词原文在哪份素材能整段复制
3. **硬 gotcha**：套用它时模型会稳定踩的坑
4. **怎么判断有没有用**：可观察的验收信号（哪怕弱，但不能为零）
5. **分级理由**：推荐 / 可参考 / 偏薄

流程：`候选 → raw 素材（原文）→ 对照判据分级 → 本页加一行`。同一条提示词只保留一份素材，多次抓取合并。

## 分级

三档的具体标准由 [[Prompt]] 定义，本页只按档分组：

| 级 | 含义（简） |
| --- | --- |
| **推荐** | 结构完整、边界清楚、有失败模式说明，可长期复用 |
| **可参考** | 思路值得借，但要按自己的场景补齐取值、边界或验收 |
| **偏薄** | 只有口号或人格设定，缺产物约定；仅作反例或起点 |

## 索引

### 推荐

| 提示词 | 一句话价值 | 指针 |
| --- | --- | --- |
| **Seed string（随机种子）** | 让模型先用 shell 生成随机串再据此定配色、版式、字体，把它从不属于自己的「最可能 token」路径上推开；直接说「随机一点」没用，模型只会换一套同样保守的默认 | [[raw/sources/2026-09-22-lenny-world-class-designer.md\|原文 · Technique 1]] |
| **设计批评者子代理循环** | 截图交给全新上下文的 critic（不带代码与历史），让它对标「顶级工作室会怎么做」并打 0–10 分；把「够不够好」从自评变成外部评判，且实现者用便宜模型、critic 用强模型 | [[raw/sources/2026-09-22-lenny-world-class-designer.md\|原文 · Technique 3]] |
| **「帮我找 prompt 点子」三步法** | 先要宽泛点子清单 → 自己挑几个并说明真实反应（喜欢/讨厌什么）→ 让模型写成可执行的 POC prompt；跳过中间两步直接采用 AI 的点子，得到的还是人人可得的东西 | [[raw/sources/2026-09-22-lenny-world-class-designer.md\|原文 · Technique 2]] |
| **做减法收尾** | 收尾时逐条点名要删的东西（渐变、发光、多余容器、自造控件换系统原生化）；模型只会加不会减，多数 AI 味来自没人让它删 | [[raw/sources/2026-09-22-lenny-world-class-designer.md\|原文 · Technique 6]] |

### 可参考

| 提示词 | 一句话价值 | 指针 |
| --- | --- | --- |
| **更野心勃勃的方向描述** | 把具体灵感（像素游戏截图感、等距 3D 城市、激进非对称）写进 prompt，比「好看一点」有效得多；但方向得来自你自己的品味，否则只是换个套路 | [[raw/sources/2026-09-22-lenny-world-class-designer.md\|原文 · Technique 2]] |
| **图像生成补质感** | 让 agent 调图像模型替代渐变和基础形状；文中给了三条接入路径，以及把 key 放进 gitignored 文件并在 AGENTS.md 写明「仅供开发、不得随产品发布」的用法 | [[raw/sources/2026-09-22-lenny-world-class-designer.md\|原文 · Technique 4]] |
| **视频循环片 + 抠背景** | 用纯色背景渲染循环视频再 chroma key 或 matting 抠掉背景，得到能叠在 UI 上的动效；玻璃类折射要先把页面背景渲进去再抠 | [[raw/sources/2026-09-22-lenny-world-class-designer.md\|原文 · Technique 5]] |
| **关键帧插值做滚动转场** | 用上一段视频的末帧作为下一段的起始帧接续，实现随滚动 scrub 的状态切换；依赖具体视频模型的物理与一致性 | [[raw/sources/2026-09-22-lenny-world-class-designer.md\|原文 · Technique 5]] |
| **计划模式提示词（Plan-first）** | 要求 agent 先读仓库约定与相似实现、有歧义先提问，再输出带文件树（NEW / UPDATE / DELETE）和逐文件改动说明的计划，最后才动代码 | [[Prompt]] · [[raw/sources/Prompt.md\|原始素材]] |

### 偏薄

（暂无挂名条目。只在反例里引用，不单独占行。）

## 明确不收

- 只有人格、文风或「你是世界顶级 XX」设定的提示词，没有产物约定
- 说不清什么时候该用的提示词（没有触发场景）
- 来源不可追溯的复制粘贴，尤其是二手转述、丢失原始出处的
- 依赖私有密钥、账号或付费额度但没写清成本和授权边界的链路（写清了可以收）
- 单纯的「提示词技巧清单」摘录：先放 `raw/sources/`，整理出原文与边界再上表

## 相关页面

- [[Prompt]] — 唯一判据源（收录标准与三档定义）
- [[AI Slop]] — 「AI 味」的语义层归纳，多数提示词的靶子
- [[Claude 5 时代的上下文工程]] — 提示词之外的另一半：上下文组织
- [[Awesome Agent Skills]] — 成体系的提示词升级形态（带脚本、manifest、QA 的 skill）
- [[Awesome Component Libraries]]

## 来源指针

- `raw/sources/2026-09-22-lenny-world-class-designer.md`
- `raw/sources/Prompt.md`
- https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world
