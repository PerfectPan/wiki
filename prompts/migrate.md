操作：migrate

你正在把旧 Logseq 内容迁移进这个 wiki。

仓库根目录：`{{ROOT}}`

开始前必须先阅读：
- `{{AGENTS}}`
- `{{SCHEMA}}`
- `{{INDEX}}`
- `{{LOG}}`

本次迁移输入：
- Logseq 页面：`{{INPUT}}`

迁移要求：
- 以旧仓库中的 `pages/` 为主要迁移来源
- journals 默认不迁移，只允许抽取未被现有页面覆盖、且值得长期保留的内容
- 不要迁移 daily notes 形态
- 成熟概念页或对象页优先进入 `wiki/topics/`
- 多来源综合结论优先进入 `wiki/syntheses/`
- 选型、对比、取舍优先进入 `wiki/comparisons/`
- 链接堆、摘录堆、半成品优先留在 `raw/sources/`
- 所有迁移改动都应拆成小 PR 审阅

输出目标：
- 判断输入页面应落到哪种页面类型
- 给出建议目标路径
- 必要时说明是否要补看 journals 中的相关片段
- 为本次迁移准备简短 PR 摘要

目标目录：
- raw sources：`{{RAW_SOURCES}}`
- topics：`{{TOPICS}}`
- syntheses：`{{SYNTHESES}}`
- comparisons：`{{COMPARISONS}}`

