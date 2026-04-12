---
name: wiki-lint
description: 在这个仓库里执行 wiki lint 工作流。用于巡检重复页面、缺失来源、孤立页面和导航遗漏；先阅读 AGENTS.md 和 SCHEMA.md，再运行 `bin/wiki lint`。
---

# Wiki Lint

1. 先阅读仓库根目录下的 `AGENTS.md`、`SCHEMA.md`、`index.md`、`log.md`。
2. 运行 `bin/wiki lint`，把输出当作本次工作的操作提示词。
3. 先找问题，再决定是否修复。
4. 如果产出修复，保持小范围并走 branch + PR 审阅。
