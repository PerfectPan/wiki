# 变更记录

这个文件是追加式记录，用来登记有意义的知识库变更。

## 记录模板

```md
## 2026-04-12

- 摘要：
- 页面：
  - [[页面名]]
- 来源：
  - raw/sources/example.md
- 备注：
```

## 2026-04-12

- 摘要：初始化适用于 Obsidian + agent + PR 审阅工作流的治理与 schema 文件。
- 页面：
  - [[AGENTS]]
  - [[SCHEMA]]
  - [[index]]
- 来源：
  - [[deep-research-report]]
- 备注：从操作模型中移除了 `drafts/` 和 `inbox/`，后续统一通过 branch 和 PR 审阅。

## 2026-04-12

- 摘要：移除了项目内 skill，把工作流入口统一收敛到 `bin/wiki` 和 `AGENTS.md`。
- 页面：
  - [[AGENTS]]
  - [[log]]
- 来源：
  - [[AGENTS]]
- 备注：仓库不再依赖 `.codex/skills/`，后续 agent 统一通过 CLI 入口工作。

## 2026-04-12

- 摘要：为迁移流程补充英文分类规则，并明确迁移默认遵循轻改原则。
- 页面：
  - [[AGENTS]]
  - [[SCHEMA]]
  - [[log]]
- 来源：
  - [[deep-research-report]]
- 备注：后续页面将按分类子目录落到 `topics`、`syntheses`、`comparisons` 中，内容优先保持原样。

## 2026-04-12

- 摘要：冻结当前一级分类，并补充 `tags` 的使用规则。
- 页面：
  - [[AGENTS]]
  - [[SCHEMA]]
  - [[log]]
- 来源：
  - [[AGENTS]]
  - [[SCHEMA]]
- 备注：后续迁移优先用 `tags` 表达细粒度主题，避免 taxonomy 膨胀。
