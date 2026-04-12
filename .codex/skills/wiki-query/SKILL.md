---
name: wiki-query
description: 在这个仓库里执行 wiki query 工作流。用于围绕现有 wiki 回答问题，并在必要时把高价值回答沉淀为 synthesis 或 comparison 页面；先阅读 AGENTS.md 和 SCHEMA.md，再运行 `bin/wiki query "<question>"`。
---

# Wiki Query

1. 先阅读仓库根目录下的 `AGENTS.md`、`SCHEMA.md`、`index.md`。
2. 运行 `bin/wiki query "<question>"`，把输出当作本次工作的操作提示词。
3. 优先只基于 `wiki/` 回答。
4. 如果形成了值得长期保留的新结论，再落入知识库并走 branch + PR 审阅。
