---
name: wiki-ingest
description: 在这个仓库里执行 wiki ingest 工作流。用于把新来源、原始资料或迁移材料整理进 topics、syntheses、comparisons 页面；先阅读 AGENTS.md 和 SCHEMA.md，再运行 `bin/wiki ingest <source>`。
---

# Wiki Ingest

1. 先阅读仓库根目录下的 `AGENTS.md`、`SCHEMA.md`、`index.md`、`log.md`。
2. 运行 `bin/wiki ingest <source>`，把输出当作本次工作的操作提示词。
3. 按提示词执行页面更新。
4. 所有非微小改动都走 branch + PR 审阅。
