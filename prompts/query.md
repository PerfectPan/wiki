操作：query

你正在为这个 wiki 执行一次标准 query。

仓库根目录：`{{ROOT}}`

开始前必须先阅读：
- `{{AGENTS}}`
- `{{SCHEMA}}`
- `{{INDEX}}`

本次问题：
- `{{INPUT}}`

工作要求：
- 优先只读 wiki/ 回答
- 如果 `wiki/` 信息不足，再明确指出缺口，不要把猜测写成事实
- 如果回答形成了值得长期保留的综合结论，考虑沉淀为 `synthesis` 或 `comparison` 页面
- 只有当问题触发了实质知识更新时，才同步更新 `log.md`
- 所有写入都应走 branch + PR 审阅

输出目标：
- 先给出答案
- 再说明是否应该把这次回答沉淀进知识库
- 如果需要沉淀，指出建议写入的页面类型和文件路径

目标目录：
- topics：`{{TOPICS}}`
- syntheses：`{{SYNTHESES}}`
- comparisons：`{{COMPARISONS}}`
