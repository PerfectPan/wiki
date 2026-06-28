---
title: Open Knowledge Format 与 Agent 可读知识库
description: 分析 Google Cloud OKF v0.1 对文件优先、Agent 可读个人 wiki 的意义，以及本仓库为何应做 OKF-compatible 而不是 OKF-only。
type: synthesis
category: ai
status: seed
created: 2026-06-15
updated: 2026-06-15
timestamp: 2026-06-15
tags:
  - okf
  - agent
  - wiki
  - knowledge-base
  - markdown
source_refs:
  - raw/sources/2026-06-15-google-cloud-open-knowledge-format.md
  - raw/sources/2026-06-15-okf-type-resource-type-conversation.md
  - https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/
  - https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf
  - https://raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/main/okf/SPEC.md
resource:
  - raw/sources/2026-06-15-google-cloud-open-knowledge-format.md
  - raw/sources/2026-06-15-okf-type-resource-type-conversation.md
  - https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/
  - https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf
  - https://raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/main/okf/SPEC.md
---
# Open Knowledge Format 与 Agent 可读知识库

## 问题

Google Cloud 发布的 Open Knowledge Format 对这个文件优先、Agent 协作维护的个人 wiki 有什么长期价值？它意味着我们应该把 wiki 改成 OKF，还是只做 OKF-compatible？

## 简答

OKF 的价值不在于 Google Cloud 本身，而在于它把过去一年反复出现的 LLM wiki / agent-readable repository 模式规格化了：Markdown 文件、YAML frontmatter、普通链接、Git 版本历史。这个仓库不需要改成纯 OKF；更稳的路线是保留现有 raw/wiki 分层和 PR 审阅治理，同时提供一层 OKF-compatible 字段与未来导出能力。

## 来源事实

Google Cloud 在 2026-06-12 发布 OKF v0.1 draft。它把一个 knowledge bundle 定义为一组 Markdown 文件，每个 concept 是一个文件，路径就是 concept identity。

OKF 的最小结构很薄：

- concept 文档必须是 UTF-8 Markdown；
- 文件顶部使用 YAML frontmatter；
- `type` 是唯一必需字段；
- consumer 会用 `type` 做 routing、filtering 和 presentation；
- 推荐字段包括 `title`、`description`、`resource`、`tags`、`timestamp`；
- concept 之间使用标准 Markdown 链接；
- `index.md` 和 `log.md` 都是可选保留文件；
- Git repository 是推荐分发方式之一，因为它天然提供历史、署名和 diff。

OKF 明确不做几件事：不定义固定 taxonomy，不替代 Avro / Protobuf / OpenAPI 等领域 schema，不要求中心服务，不要求 SDK，也不绑定特定云、模型或 agent 框架。

## 综合判断

OKF 证明了一件事：给 Agent 用的知识库，最稳的底座不一定是先上向量库或知识图谱，而是先把知识变成可读、可 diff、可链接、可审阅的文件。

这和本仓库当前方向一致。`raw/sources/` 保留事实层，`wiki/` 保留整理后的知识层，`SCHEMA.md` 定义页面约束，`index.md` 做导航，Git/PR 承担审阅和变更记录。与 OKF 相比，本仓库多了一层治理：不是所有 Markdown 都直接等价为知识，只有经过判断的内容才进入 `wiki/`。

因此不应把 OKF 当作要全盘迁移的新格式。更准确的定位是：

- **内部格式**：继续服务 Obsidian、中文写作、raw/wiki 分层和 PR 审阅。
- **兼容字段**：在 frontmatter 中逐步补充 `description`、`resource`、`timestamp`。
- **导出格式**：未来通过 `export-okf` 把 wikilink 转成标准 Markdown link，把 `source_refs` 映射成 `resource`，输出 OKF bundle。

## 对本仓库的启发

### `type` 是消费侧路由字段

OKF 里的 `type` 不是普通标签。它是 consumer 读 bundle 时最先看的路由字段：不同 type 可以走不同展示模板、不同读取策略、不同筛选入口。

Google 给的例子偏数据资产和运维知识，例如 `BigQuery Table`、`BigQuery Dataset`、`API Endpoint`、`Metric`、`Playbook`、`Reference`。这些 type 回答的是“这个 concept 是什么种类的对象”。

本仓库当前的 `type` 回答的是“这个页面承担什么知识职责”：

- `topic`：解释一个概念或对象；
- `synthesis`：沉淀综合理解；
- `comparison`：记录选型和取舍。

这和 OKF 不冲突，但含义更偏 wiki 页面角色，而不是业务资产类型。消费时可以这样用：

- 只想找定义，筛 `type=topic`；
- 想找结论和方法论，筛 `type=synthesis`；
- 想做技术选型，筛 `type=comparison`；
- 再用 `category` 和 `tags` 过滤具体领域，例如 `category=ai`、`tags=agent`。

如果未来要导出给更通用的数据目录或企业知识平台，可以在页面上增加可选 `resource_type` 字段，由导出层映射成 OKF 的资产类型；但内部不必现在就把 `type` 改成 `BigQuery Table` 这类资产类型。对个人 wiki 来说，页面职责比资产 taxonomy 更稳定。

### 本仓库的映射决策

本轮讨论把映射规则收敛为两层：

- 内部 `type` 固定为页面职责：`topic`、`synthesis`、`comparison`。
- 可选 `resource_type` 表示真实外部资源类型：例如 `BigQuery Table`、`API Endpoint`、`Metric`、`Automation Job`。
- `resource` 指向真实资源或来源文件，不承载页面职责。
- knowledge mode 导出时，OKF `type` 保留内部页面职责，适合知识库 Agent 和 RAG。
- resource mode 导出时，若存在 `resource_type`，OKF `type` 可以映射为 `resource_type`，同时用 `page_type` 保留内部页面职责。

这个规则避免了两个风险：一是把内部 `type` 放飞成无限枚举，导致 wiki 页面模板失稳；二是完全忽略 OKF 的资源目录能力，把 OKF 误读成普通 Markdown 文档格式。

第一，`description` 很重要。它不是给人看的装饰字段，而是给 agent 快速判断页面相关性的索引摘要。没有它，agent 必须打开正文才能知道一页是否值得读。

第二，标准 Markdown link 是对外互操作的底线。仓库内部可以继续使用 Obsidian wikilink，但导出给其他 agent 或工具时，应转换成 bundle-relative Markdown link。

第三，`log.md` 不是必需的。OKF 允许 `log.md`，但也推荐 Git 作为分发形态。本仓库已经用 Git/PR 审阅，继续维护手写 `log.md` 会重复记录职责。因此删除 `log.md` 并把变更摘要放进 PR body，是更贴近当前工作流的选择。

第四，OKF 的低约束既是优点也是风险。它统一了最低可交换格式，但不保证页面质量、来源可信度、结论成熟度或分类一致性。本仓库仍需要 `SCHEMA.md`、source pointer、状态字段和 PR review 作为质量层。

## 风险与边界

- OKF v0.1 仍是 draft，生态是否采用还未验证。
- `type` 没有中心注册，长期可能出现语义碎片化。
- `resource` 更适合描述具体资产；对抽象 synthesis 页面，它只能指向来源资料，而不是唯一底层资产。
- 纯 OKF 不区分 raw fact layer 与 synthesized knowledge layer，这一点本仓库不应放弃。

## 相关页面

- [[wiki/syntheses/ai/Agent 驱动 Wiki 的维护流程|Agent 驱动 Wiki 的维护流程]]
- [[SCHEMA]]

## 来源指针

- `raw/sources/2026-06-15-google-cloud-open-knowledge-format.md`
- `raw/sources/2026-06-15-okf-type-resource-type-conversation.md`
- https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/
- https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf
- https://raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/main/okf/SPEC.md
