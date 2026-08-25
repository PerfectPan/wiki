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
- GitHub 仓库：`raw/sources/YYYY-MM-DD-仓库名.md`（分析报告）

阅读素材，理解核心内容。

## 第二步：判断页面类型

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

## 第三步：选择分类

从 SCHEMA.md 定义的一级分类中选一个：
frontend、ai、languages、systems、algorithms、architecture、tooling、product、career、life

每个页面只能选一个主分类。

## 第四步：写 frontmatter

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

## 第五步：写正文

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

## 第六步：写作规则

1. 原始事实和综合结论分开表达
2. 非平凡结论附带来源指针
3. 优先保留原始内容的措辞和结构（轻改原则）
4. 中文书写，保留清晰的英文术语
5. 不要改写或删除 raw/ 中的原始资料

## 第七步：更新导航

如果新增了页面，更新 `index.md` 中对应分类的列表。

## 第八步：校验

运行 `bin/wiki check <页面路径>` 确认 frontmatter 无误。

## 输出

- 判断这份来源应该影响哪些页面
- 必要时新增或更新知识页
- 为 PR 写出简短的变更摘要

目标目录：
- topics：`{{TOPICS}}`
- syntheses：`{{SYNTHESES}}`
- comparisons：`{{COMPARISONS}}`
