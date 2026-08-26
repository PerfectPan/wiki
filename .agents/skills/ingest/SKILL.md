---
name: ingest
description: 将文章、网页、仓库、推文线程或视频素材整理为可审阅的 Wiki 页面；当用户要求把新来源沉淀进本仓库时使用。
---

操作：ingest

你正在为这个 wiki 执行一次标准 ingest。

仓库根目录：`{{ROOT}}`

开始前必须先阅读：
- `{{AGENTS}}`
- `{{SCHEMA}}`
- `{{INDEX}}`

本次输入：
- 来源：`{{INPUT}}`

## 第一步：定位素材

来源已经被抓取并存入 `raw/sources/`。找到对应的文件：
- 博客/文档：`raw/sources/YYYY-MM-DD-主题.md`（Markdown）和 `.html`（原始）
- GitHub 仓库：`raw/sources/YYYY-MM-DD-仓库名.md`（目录结构 + 关键文件）
- X 推文线程：`raw/sources/YYYY-MM-DD-主题.md`（线程全文）
- YouTube 视频：`raw/sources/YYYY-MM-DD-主题.md`（字幕转录）

阅读素材，理解核心内容。

## 第二步：分析素材

在写 wiki 页面之前，先分析素材：

### 博客/文档

1. **提取核心论点**：文章主要在说什么？作者的核心主张是什么？
2. **识别关键概念**：有哪些新概念、术语、方法论？给出明确定义
3. **梳理论证结构**：作者如何展开论证？有哪些论据和例子？
4. **判断价值**：哪些内容值得沉淀到 wiki？是事实、观点还是方法论？

**要求**：不能只做表面概括。要引用文章中的具体段落和论述来支撑你的理解。

### GitHub 仓库

**不能只看目录结构和 README。必须深入阅读核心代码。**

分析步骤：

1. **理解项目定位**：从 README 了解项目解决什么问题
2. **识别核心模块**：根据目录结构判断哪些是核心模块（如 src/core、src/harness、src/memory 等）
3. **深入阅读核心代码**：
   - 找接口定义（如 `*.interface.ts`、`types.ts`、基类）
   - 找核心编排逻辑（如 orchestrator、engine、main loop）
   - 找关键设计模式（抽象层、策略模式、插件架构等）
4. **理解架构设计**：
   - 模块之间如何交互
   - 核心数据流是什么
   - 扩展点在哪里
5. **提炼值得记录的设计**：
   - 有哪些独特的架构决策
   - 解决了什么问题
   - 可以借鉴的设计模式

**禁止**：只基于目录结构和 README 做表面分析。必须引用具体的代码文件和接口来支撑结论。

### X 推文线程

1. **识别主题**：这个线程在讨论什么？
2. **提取观点**：作者的核心观点是什么？
3. **判断价值**：是否值得沉淀为 wiki 页面？

### YouTube 视频

1. **理解主题**：视频讲了什么？
2. **提取关键点**：有哪些核心观点、方法论？
3. **判断价值**：是否值得沉淀？

分析完成后，判断这份素材应该写成什么类型的页面。

## 第三步：判断页面类型

根据内容性质决定放到哪个目录：

| 类型 | 目录 | 回答的问题 | 适用场景 |
| --- | --- | --- | --- |
| topic | `wiki/topics/<category>/` | 这是什么？ | 概念、工具、技术的定义和基本说明 |
| synthesis | `wiki/syntheses/<category>/` | 综合后的理解是什么？ | 多来源整合、方法论、设计模式提炼 |
| comparison | `wiki/comparisons/<category>/` | 该怎么选？ | 选型、对比、取舍 |

判断原则：
- 如果是解释一个概念"是什么" → topic
- 如果是从一个或多个来源提炼出方法论/设计模式 → synthesis
- 如果是在多个选项之间做选择 → comparison

## 第四步：选择分类

从 SCHEMA.md 定义的一级分类中选一个：
frontend、ai、languages、systems、algorithms、architecture、tooling、product、career、life

每个页面只能选一个主分类。

## 第五步：写 frontmatter

必填字段：
```yaml
---
title: 页面标题
description: 一句话说明这页解决什么问题
type: topic | synthesis | comparison
category: <一级分类>
created: YYYY-MM-DD
updated: YYYY-MM-DD
timestamp: YYYY-MM-DD
tags:
  - tag1
  - tag2
source_refs:
  - raw/sources/YYYY-MM-DD-主题.md
  - https://原始URL
resource:
  - raw/sources/YYYY-MM-DD-主题.md
  - https://原始URL
---
```

规则：
- `description`：面向人和 agent 的一句话摘要，必须写
- `tags`：1-5 个英文小写短词，表达横向主题
- `source_refs` 和 `resource`：指向 raw/sources 里的素材和原始 URL
- `created`/`updated`/`timestamp`：用今天的日期

## 第六步：写正文

### topic 页面结构

```markdown
# 标题

## 摘要

用一小段话定义这个主题。

## 关键点

- 要点 1
- 要点 2
- ...

## 相关页面

- [[相关页面]]

## 来源指针

- raw/sources/...
- https://...
```

### synthesis 页面结构

```markdown
# 标题

## 问题

这页在回答什么问题？

## 简答

一句话回答。

## 来源事实

客观列出素材中的关键事实。

## 综合结论

展开说明综合后的理解，分点论述。

## 对个人/项目的启发

提炼可操作的启发。

## 相关页面

- [[相关页面]]

## 来源指针

- raw/sources/...
- https://...
```

### comparison 页面结构

```markdown
# 标题

## 当前结论

目前的推荐结论是什么？

## 备选项

- 方案 A
- 方案 B

## 取舍分析

| 方案 | 优势 | 风险 | 适用场景 |
| --- | --- | --- | --- |
| A | ... | ... | ... |

## 推荐理由

写清楚当前选择及原因。

## 来源指针

- raw/sources/...
- https://...
```

## 第七步：写作规则

1. 原始事实和综合结论分开表达
2. 非平凡结论附带来源指针
3. 优先保留原始内容的措辞和结构（轻改原则）
4. 中文书写，保留清晰的英文术语
5. 不要改写或删除 raw/ 中的原始资料

## 第八步：更新导航

如果新增了页面，更新 `index.md` 中对应分类的列表。

## 第九步：校验

运行 `bin/wiki check <页面路径>` 确认 frontmatter 无误。

## 输出

- 判断这份来源应该影响哪些页面
- 必要时新增或更新知识页
- 在 PR body 中写清楚本次知识变更摘要、受影响页面和来源指针

目标目录：
- topics：`{{TOPICS}}`
- syntheses：`{{SYNTHESES}}`
- comparisons：`{{COMPARISONS}}`
