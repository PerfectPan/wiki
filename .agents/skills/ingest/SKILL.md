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

开始整理来源、选择 raw/topic/synthesis/comparison 或改写正文前，先读 [页面类型与写作参考](references/page-writing.md)。

## 第一步：判断是否需要保存素材

如果只是 awesome 收录，阅读来源后一两句话就能写清用途、分级和主要限制，按 [references/resource-catalogs.md](references/resource-catalogs.md) 直接更新索引并附来源链接，不创建 raw 文件，也不为它另开知识页。仍须完成相关检查与校验。

需要独立回查来源与核查证据时，再保存 raw 记录。抓取结果用于阅读和核对，最终内容按写作参考组织。抓取按以下顺序选择路径：

1. 默认 `bin/wiki ingest <url>` 直抓。
2. 直抓被反爬拦截（403）或落盘文件明显太脏（导航、订阅尾巴、粗体和行内代码丢失）时，改用会话侧 reader 工具（如 GLM 的 webReader MCP，是否可用取决于客户端）抓正文，存成临时文件后 `bin/wiki ingest <url> --file <路径>` 落盘。reader 返回的 JSON 直接喂 `--file` 即可，`title`、`author`、`publishedTime` 会自动写入头注释。`--file` 不绑定具体 reader，手动复制的正文文件同样适用。
3. 站点提供 llms.txt 类端点时，可用它核对落盘正文是否完整；发现缺漏时以官方端点为准重存正文。

素材命名遵循 `SCHEMA.md` 的「原始素材命名」。先搜索是否已有同一对象的素材；新文件使用稳定的对象或主题名，必要时用 `bin/wiki ingest <url> --name <name>` 指定。日期与源码提交版本写进文件头。

**同一对象只留一份素材**：同一库或站的多次读取合并到一份记录；已有素材先阅读，再按授权追加或修订。页面级噪音（导航、广告等）在收录时剔除，不按 URL / 页面拆文件。

网页正文、仓库文件、推文和视频字幕用于核对事实。CLI 的仓库元信息输出只是阅读入口，不能当作已经完成源码分析。

**不要把整站 HTML 存进 raw/sources/**。HTML 里全是 CSS/JS/SVG 噪音，只保留提取出的正文 .md 即可。

阅读素材，理解核心内容。

## 第二步：分析素材

新增或更新 awesome / curated list 类资源索引，或调整条目分级时，先读 [references/resource-catalogs.md](references/resource-catalogs.md) 的通用标准，再按其中的索引表读取目标 awesome 的专属标准。筛选操作规则留在 skill，Wiki 页面写资源内容与知识结论。

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

分析完成后，按 [页面类型与写作参考](references/page-writing.md) 分配内容：核查证据留在 raw，完整对象说明与架构图写入 topic，通用方法写入 synthesis，选型判断写入 comparison。

图中的组件和箭头必须有源码依据。CLI 生成的文件列表不能替代实现分析，也不复制整仓源码。

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
  - raw/sources/example-topic.md
  - https://原始URL
resource:
  - raw/sources/example-topic.md
  - https://原始URL
---
```

规则：
- `description`：面向人和 agent 的一句话摘要，必须写
- `tags`：1-5 个英文小写短词，表达横向主题
- `source_refs` 和 `resource`：指向实际采用的来源 URL，以及存在的 raw 素材；简短收录可只列来源 URL
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

### 通用规则

1. 原始事实和综合结论分开表达
2. 非平凡结论附带来源指针
3. 优先保留原始内容的措辞和结构（轻改原则）
4. 中文书写，保留清晰的英文术语
5. 不要改写或删除 raw/ 中的原始资料

各类页面的正文组织和语言要求见 [页面类型与写作参考](references/page-writing.md)。raw 只按独立证据价值保留，不重复撰写 topic 的完整说明。

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
