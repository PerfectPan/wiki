操作：research

你正在为这个 wiki 执行一次深度调研，并准备把结论沉淀为可审阅的 wiki 页面。

仓库根目录：`{{ROOT}}`

开始前必须先阅读：
- `{{AGENTS}}`
- `{{SCHEMA}}`
- `{{INDEX}}`
- `{{LOG}}`

本次调研主题：
- `{{INPUT}}`

工作要求：
- 先明确调研对象、对比对象、源码快照或资料日期；对时效性强的信息使用当前可核验来源
- 区分原始事实、源码/文档证据、综合判断和推断；不要把猜测写成事实
- 优先使用官方文档、源码、release note、仓库文件、规范和一手资料；网页调研要记录来源链接
- 如果涉及实现调研，必须阅读关键入口、领域模型、数据流、存储边界、扩展点、运行时边界和测试/验证入口
- 如果涉及对比调研，必须说明每个对象的所有权、运行位置、核心 loop、数据治理、扩展性、成本和锁定风险
- 不要新增项目内 `.codex/skills` 或本地 skill；本仓库的 agent 工作流统一沉淀在 `bin/wiki` 和 `prompts/`

深度验收项：
- 必须包含系统架构图；优先使用兼容 Obsidian 和 GitHub 的 Mermaid
- 必须包含核心数据流、执行链路或生命周期图
- 必须包含扩展面、边界或 trust model 图
- 对比类调研必须包含双方架构差异图
- 必须包含证据矩阵，至少覆盖：结论、证据来源、证据位置、置信度或限制
- 必须包含“当前张力 / 风险 / 未决问题”，说明哪些判断可能随版本或产品策略变化

输出目标：
- 判断应新增或更新 `wiki/topics/`、`wiki/syntheses/` 还是 `wiki/comparisons/` 页面
- 新页面应带 `SCHEMA.md` 约定的 frontmatter，并在单独打开时自洽
- 如果导航发生变化，更新 `index.md`
- 在 `log.md` 追加本次知识变更记录，包含日期、页面和来源指针
- 为 PR 写出简短摘要，说明调研范围、来源、图表、验证方式和剩余风险

验证要求：
- 运行 `git diff --check`
- 运行 `bash tests/wiki-cli.sh`
- 对新增 Mermaid fence 做成对检查；如果无法渲染，至少确认 Markdown fence 没有破坏页面结构

目标目录：
- topics：`{{TOPICS}}`
- syntheses：`{{SYNTHESES}}`
- comparisons：`{{COMPARISONS}}`
