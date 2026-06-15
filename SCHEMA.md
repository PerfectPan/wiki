# Wiki 结构约定

这个文件定义了知识库页面的最小结构。目标是让 agent 的输出足够稳定，但不要把写作流程变成负担。

## 全局规则

1. 文件名应当可读，并尽量与页面标题一致。
2. 新的知识页面只能放在 `wiki/topics/`、`wiki/syntheses/` 或 `wiki/comparisons/` 下。
3. 每个页面都应当在 Obsidian 中单独打开时仍然容易理解。
4. 优先通过页面链接建立关系，而不是在不同页面中重复解释同一件事。
5. 任何包含结论、建议或判断的页面，都应附带来源指针。
6. 新页面应带一个英文 `category` 字段，并按分类子目录存放。
7. `tags` 用来表达细粒度主题，不用来替代一级分类。

## 建议使用的 frontmatter

新页面建议带上这组最小 frontmatter：

```yaml
---
title: 页面标题
description: 一句话说明这页解决什么问题，便于 agent 先扫 frontmatter
type: topic
category: frontend
status: seed
created: 2026-04-12
updated: 2026-04-12
tags: []
source_refs: []
resource: []
timestamp: 2026-04-12
---
```

字段约定：

- `type`：`topic`、`synthesis` 或 `comparison`
- `description`：面向人和 agent 的一句话摘要。新页面应优先补上，避免 agent 必须打开正文才能判断页面是否相关
- `category`：英文一级分类，例如 `frontend`、`ai`、`systems`
- `status`：`seed`、`active` 或 `evergreen`
- `tags`：细粒度英文主题，推荐 1 到 5 个
- `source_refs`：支持本页内容的相对路径、页面名或 URL
- `resource`：OKF-compatible 字段，导出时默认镜像 `source_refs`
- `timestamp`：OKF-compatible 字段，导出时默认使用 `updated`

## OKF 兼容约定

这个 wiki 的主格式仍然是 Obsidian-compatible Markdown，但新页面应逐步兼容 Open Knowledge Format。

兼容目标：

1. 保留现有 `category`、`status`、`source_refs` 等治理字段，不为了兼容 OKF 丢掉本仓库的审阅和来源约束。
2. 在 frontmatter 中补充 `description`，让 agent 可以在不读取全文的情况下初筛页面。
3. 使用 `resource` 作为 OKF-compatible 来源字段。手写页面时可以让它与 `source_refs` 相同；未来导出工具可以自动从 `source_refs` 生成。
4. 使用 `timestamp` 作为 OKF-compatible 更新时间字段。手写页面时可以与 `updated` 相同；未来导出工具可以自动生成。
5. 仓库内部可以继续使用 `[[wikilink]]`，但 OKF 导出时应转换为标准 Markdown 链接。
6. `raw/sources/` 继续作为事实层，不因 OKF 兼容而把未成熟资料直接提升到 `wiki/`。

字段映射：

| Wiki 字段 | OKF-compatible 字段 | 说明 |
| --- | --- | --- |
| `title` | `title` | 保持一致 |
| `description` | `description` | 新增，一句话摘要 |
| `type` | `type` | 保持一致，取值仍受本仓库页面类型约束 |
| `tags` | `tags` | 保持一致 |
| `source_refs` | `resource` | `source_refs` 是内部来源字段，`resource` 是导出友好字段 |
| `updated` | `timestamp` | `updated` 是内部字段，`timestamp` 是导出友好字段 |
| `category` | 扩展字段 | OKF 不强制，本仓库继续保留 |
| `status` | 扩展字段 | OKF 不强制，本仓库继续保留 |

最小样板：

```yaml
---
title: 页面标题
description: 一句话说明这页解决什么问题
type: synthesis
category: ai
status: seed
created: 2026-06-15
updated: 2026-06-15
timestamp: 2026-06-15
tags:
  - agent
source_refs:
  - raw/sources/example.md
resource:
  - raw/sources/example.md
---
```

分类与 tag 的分工：

- `category` 解决“这页放哪儿”
- `tags` 解决“这页还和哪些主题相关”
- 目录只保留一个主分类，交叉语义通过 `tags` 和页面链接表达

分类治理：

1. 当前一级分类默认冻结，不随迁移过程随意扩张。
2. 更细粒度主题优先放进 `tags`，例如 `react`、`rsc`、`mcp`、`typescript`。
3. 只有当一个主题持续形成稳定页面簇，并且放进现有分类明显别扭时，才考虑升级为新的一级分类。

## 页面类型

### 1. 主题页面

路径：`wiki/topics/<category>/`

用于稳定主题页，既包括概念，也包括具体对象。主题页回答“这是什么？”，并且应该可以长期持续演化。

建议结构：

```md
# 页面标题

## 摘要

用一小段话定义这个主题。

## 关键点

- 要点 1
- 要点 2

## 相关页面

- [[相关页面]]

## 来源指针

- 来源 1
```

示例：

- `React`
- `MCP`
- `Rolldown`
- `Software Design`

### 2. 综合页面

路径：`wiki/syntheses/<category>/`

用于把多份笔记或多份资料整合为更高层次的理解。综合页面回答“目前综合后的理解是什么？”

建议结构：

```md
# 页面标题

## 问题

这页在回答什么问题？

## 简答

一句话回答。

## 综合结论

展开说明综合后的理解。

## 未决问题

- 问题 1

## 来源指针

- 来源 1
```

示例：

- `RSC 的序列化心智模型`
- `Agent 驱动 Wiki 的维护流程`

### 3. 对比页面

路径：`wiki/comparisons/<category>/`

用于记录选择、取舍和决策。对比页面回答“应该怎么选？”

建议结构：

```md
# 页面标题

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

- 来源 1
```

示例：

- `Obsidian vs Logseq`
- `RSC vs SSR`

## 原始材料规则

- `raw/sources/` 存放原始资料和迁移后的残留材料。
- `raw/assets/` 存放被页面引用的附件。
- 不要强行把 raw 材料改写成 wiki 页面，除非它已经达到可以被提升的程度。

## 迁移判断规则

- 成熟的概念页或对象页，提升到 `wiki/topics/`
- 多来源整合出的结论，提升到 `wiki/syntheses/`
- 选型、对比、决策类内容，提升到 `wiki/comparisons/`
- 暂时不成形的残留内容，留在 `raw/sources/`
- 页面落库时必须选择一个英文一级分类，并进入对应的分类子目录
