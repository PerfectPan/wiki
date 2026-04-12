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

## 2026-04-12

- 摘要：完成第一批迁移，优先落地成熟 topic 页面，并为迁移页面保留 raw 来源副本。
- 页面：
  - [[wiki/topics/architecture/Software Design|Software Design]]
  - [[wiki/topics/architecture/技术方案|技术方案]]
  - [[wiki/topics/ai/MCP|MCP]]
  - [[wiki/topics/product/Logseq|Logseq]]
  - [[raw/sources/RAG|RAG]]
- 来源：
  - `raw/sources/Software Design.md`
  - `raw/sources/技术方案.md`
  - `raw/sources/MCP.md`
  - `raw/sources/Logseq.md`
  - `raw/sources/RAG.md`
- 备注：这一批遵循轻改原则，正文尽量保持原样；`RAG` 暂时仍保留在 raw 层，后续再决定是否提升为 wiki 页面。

## 2026-04-12

- 摘要：补充迁移 `frontend` 第一组成熟页面，并将 `Ref`、`RSC` 相关图片一并纳入仓库。
- 页面：
  - [[wiki/topics/frontend/React|React]]
  - [[wiki/topics/frontend/RSC|RSC]]
  - [[wiki/topics/frontend/Ref|Ref]]
  - [[wiki/topics/frontend/useRef|useRef]]
  - [[wiki/topics/frontend/State Management|State Management]]
  - [[wiki/topics/frontend/zustand|zustand]]
  - [[wiki/topics/frontend/CSS|CSS]]
  - [[wiki/topics/frontend/SVG|SVG]]
  - [[wiki/topics/frontend/Component Library|Component Library]]
  - [[wiki/topics/frontend/Web Component|Web Component]]
  - [[wiki/topics/frontend/React Devtools|React Devtools]]
- 来源：
  - `raw/sources/React.md`
  - `raw/sources/RSC.md`
  - `raw/sources/Ref.md`
  - `raw/sources/useRef.md`
  - `raw/sources/State Management.md`
  - `raw/sources/zustand.md`
  - `raw/sources/CSS.md`
  - `raw/sources/SVG.md`
  - `raw/sources/Component Library.md`
  - `raw/sources/Web Component.md`
  - `raw/sources/React Devtools.md`
  - `raw/sources/React Render Optimization.md`
- 备注：正文保持轻改；`React Render Optimization` 当前仍为空页，只保留 raw 副本，未提升到 `wiki/`。

## 2026-04-12

- 摘要：继续迁移 `architecture` 与 `ai/product` 的成熟页面，补充设计、依赖注入、DDD、Agent、GPT、Code Agent 等主题。
- 页面：
  - [[wiki/topics/architecture/DDD|DDD]]
  - [[wiki/topics/architecture/Dependency Injection|Dependency Injection]]
  - [[wiki/topics/product/Design|Design]]
  - [[wiki/topics/ai/Agent|Agent]]
  - [[wiki/topics/ai/Code Agent|Code Agent]]
  - [[wiki/topics/ai/GPT|GPT]]
- 来源：
  - `raw/sources/DDD.md`
  - `raw/sources/Dependency Injection.md`
  - `raw/sources/Design.md`
  - `raw/sources/Agent.md`
  - `raw/sources/Code Agent.md`
  - `raw/sources/GPT.md`
- 备注：这批仍然遵循轻改原则，正文尽量保持原样，只补目录、frontmatter 和来源指针。

## 2026-04-12

- 摘要：完成旧 Logseq `pages/` 的全量迁移，所有页面都已进入 `wiki/topics/`，并保留 raw 来源副本。
- 页面：
  - `wiki/topics/*`
  - `raw/sources/*`
  - `raw/assets/*`
  - [[index]]
  - [[log]]
- 来源：
  - `raw/sources/`
  - `raw/assets/`
- 备注：本次全量迁移覆盖 `192/192` 个旧 `pages`；`journals/` 仍按既定规则未整体迁入。
