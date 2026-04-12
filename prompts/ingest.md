操作：ingest

你正在为这个 wiki 执行一次标准 ingest。

仓库根目录：`{{ROOT}}`

开始前必须先阅读：
- `{{AGENTS}}`
- `{{SCHEMA}}`
- `{{INDEX}}`
- `{{LOG}}`

本次输入：
- 来源：`{{INPUT}}`

工作要求：
- 优先把来源整理进 `wiki/topics/`、`wiki/syntheses/` 或 `wiki/comparisons/`
- 不要改写或删除 `raw/` 中的原始资料
- 如果导航发生变化，更新 `index.md`
- 在 `log.md` 追加本次知识变更记录
- 所有非微小改动都应走 branch + PR 审阅

输出目标：
- 判断这份来源应该影响哪些页面
- 必要时新增或更新知识页
- 为 PR 写出简短的变更摘要

目标目录：
- topics：`{{TOPICS}}`
- syntheses：`{{SYNTHESES}}`
- comparisons：`{{COMPARISONS}}`

