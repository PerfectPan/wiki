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

## 用词检查

使用具体的动作和对象解释行为，保留更清晰的英文技术术语。描述字段与请求响应时使用“接口定义”，描述双方交互要求时使用“调用约定”；“契约测试”等正式术语保留。

`bin/wiki check-jargon` 按 `bin/jargon-rules.json` 报告需修改的词项、位置和建议，不自动替换。原始引用和技术标识按 `bin/README.md` 的规则保留；需要上下文判断的表达仍由人工审阅。

## 建议使用的 frontmatter

新页面建议带上这组最小 frontmatter：

```yaml
---
title: 页面标题
description: 一句话说明这页解决什么问题，便于 agent 先扫 frontmatter
type: topic
category: frontend
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
- `tags`：细粒度英文主题，推荐 1 到 5 个
- `source_refs`：支持本页内容的相对路径、页面名或 URL
- `resource`：OKF-compatible 字段，导出时默认镜像 `source_refs`
- `resource_type`：可选字段。只有当页面描述真实外部资源时才填写，例如 `API Endpoint`、`Automation Job`、`Metric`、`BigQuery Table`
- `timestamp`：OKF-compatible 字段，导出时默认使用 `updated`

## OKF 兼容约定

这个 wiki 的主格式仍然是 Obsidian-compatible Markdown，但新页面应逐步兼容 Open Knowledge Format。

兼容目标：

1. 保留现有 `category`、`source_refs` 等治理字段，不为了兼容 OKF 丢掉本仓库的审阅和来源约束。
2. 在 frontmatter 中补充 `description`，让 agent 可以在不读取全文的情况下初筛页面。
3. 内部 `type` 始终表示页面职责，只允许 `topic`、`synthesis`、`comparison`。不要把外部资源类型直接塞进内部 `type`。
4. 使用 `resource` 作为 OKF-compatible 来源字段。手写页面时可以让它与 `source_refs` 相同；未来导出工具可以自动从 `source_refs` 生成。
5. 如果页面描述真实外部资源，使用可选 `resource_type` 表达资源对象类型，例如 `API Endpoint`、`Automation Job`、`Metric`、`BigQuery Table`。
6. 使用 `timestamp` 作为 OKF-compatible 更新时间字段。手写页面时可以与 `updated` 相同；未来导出工具可以自动生成。
7. 仓库内部可以继续使用 `[[wikilink]]`，但 OKF 导出时应转换为标准 Markdown 链接。
8. `raw/sources/` 继续作为事实层，不因 OKF 兼容而把未成熟资料直接提升到 `wiki/`。

字段映射：

| Wiki 字段 | OKF-compatible 字段 | 说明 |
| --- | --- | --- |
| `title` | `title` | 保持一致 |
| `description` | `description` | 新增，一句话摘要 |
| `type` | `type` | 保持一致，取值仍受本仓库页面类型约束 |
| `tags` | `tags` | 保持一致 |
| `source_refs` | `resource` | `source_refs` 是内部来源字段，`resource` 是导出友好字段 |
| `updated` | `timestamp` | `updated` 是内部字段，`timestamp` 是导出友好字段 |
| `resource_type` | `type` 或扩展字段 | 仅在 resource mode 导出时映射为 OKF `type`；knowledge mode 下保留为扩展字段 |
| `category` | 扩展字段 | OKF 不强制，本仓库继续保留 |

导出模式：

- **knowledge mode**：面向普通知识库 Agent 和 RAG。导出时 `type` 保持为 `topic`、`synthesis`、`comparison`，`resource_type` 作为扩展字段保留。
- **resource mode**：面向资源目录或工具目录。若页面存在 `resource_type`，导出时可以令 OKF `type = resource_type`，并把内部页面职责保留为 `page_type`。

最小样板：

```yaml
---
title: 页面标题
description: 一句话说明这页解决什么问题
type: synthesis
category: ai
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

资源页样板：

```yaml
---
title: Search API
description: 搜索服务的 HTTP API 入口与调用边界
type: topic
category: tooling
created: 2026-06-15
updated: 2026-06-15
timestamp: 2026-06-15
tags:
  - api
  - search
resource_type: API Endpoint
resource:
  - https://example.com/api/search
source_refs:
  - raw/sources/search-api.md
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

## 收录页约定（curated list / awesome 类）

用于把一批同类外部对象（skill、组件库、参考站、工具……）收进 wiki，形成可召回、可维护的索引。收录页回答「我们收录了哪些 X、各是什么水平」，不回答「X 是什么」（那是对象 topic 页或清单行的职责），也不回答「该怎么选」（那是 comparison 的职责）。`type` 仍是 `topic`，按领域分类目录存放（如 `wiki/topics/frontend/`、`wiki/topics/ai/`）。

判断是否该用收录页：

- 有一批同领域对象需要持续维护，用一页做「索引 + 分级」比每个对象单独开页更划算；
- 单个对象不值得开 topic 页，但合起来值得一页（例如「动画组件库收藏」）；
- 已有多个 topic / comparison / 清单行分散引用同一批对象，需要一个聚合召回入口。

### 定位纪律

1. 收录页是 curated list，不是 star 排行榜，也不是全网镜像；只收「过线或有教学价值」的条目。
2. 判据与索引分离：领域判据只存在于该领域的唯一判据页（如 skill 领域见 `wiki/syntheses/ai/Skill 工程化的产物协议范式.md`），收录页只写「一句话价值 + 分级 + 指针」；不要在收录页里重建判据细则。
3. 未过判据的链接堆、摘录 → `raw/sources/`，不进收录页。
4. 对象若另开 topic / product 页，收录页条目与对象页解耦：收录页只留指针。
5. 素材合并：同一对象（一个库 / 站）在 `raw/sources/` 只保留一份合并素材（`YYYY-MM-DD-<对象>.md`），不按 URL / 页面拆多个文件；页面级噪音（testimonials、导航、广告）在收录时剔除，不整站搬运。

### Frontmatter 约定

```yaml
type: topic
description: 经 <判据页> 审过的 <领域> 薄索引：推荐 / 可参考 / 偏薄；链判据与素材，不镜像全文
tags:
  - catalog          # 必含：recall 时先查 catalog + 领域 tag
  - <领域 tag>        # 如 skills / component-library / tooling
source_refs:          # 判据页 + 各条目 raw 评审 + 对象来源
resource:             # 镜像 source_refs
```

- 命名统一为 `Awesome <领域>`（沿用 awesome 的 curated list 语义）或 `<领域> 收录索引`，方便按名字召回。
- 分级语义统一三档：**推荐 / 可参考 / 偏薄**；每档在该领域的具体含义由判据页定义，收录页只放三档各一张表。

### 结构模板（必要小节）

```md
# 标题

## 摘要        # 角色声明：这是索引，不是判据正文、不是镜像；指向判据页
## 收录规则    # 每条候选至少要回答的问题 + 流程：候选 → raw 评审 → 对照判据分级 → 加一行
## 分级        # 三档含义表（领域化，判据页定义）
## 索引        # 按档分组表格：| 对象 | 一句话价值 | 指针 |；指针必须可点，评审素材链 raw
## 明确不收    # 显式负例清单，防止后续重复评审同类候选
## 相关页面
## 来源指针
```

### 召回与更新约定

- 找「收录了哪些 X」：先查 `tags: catalog` + 领域 tag 的页面，不要逐个 topic 页翻。
- 收录页加条目、改分级 = 知识变更，走 branch + PR；PR body 说明该条目的判据与分级理由。
- 收录页新增对象若本身值得开页（topic / product），导航同步更新 `index.md`；纯索引行变更不需要。

样板页：`wiki/topics/ai/Awesome Agent Skills.md`（本约定的首个实例，2026-08 建立并沿用至今）。

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
