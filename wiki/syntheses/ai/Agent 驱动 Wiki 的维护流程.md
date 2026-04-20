---
title: Agent 驱动 Wiki 的维护流程
type: synthesis
category: ai
status: seed
created: 2026-04-19
updated: 2026-04-19
tags:
  - agent
  - wiki
  - workflow
  - mcp
  - prompt
source_refs:
  - AGENTS.md
  - SCHEMA.md
  - deep-research-report.md
  - wiki/topics/ai/Agent.md
  - wiki/topics/ai/Code Agent.md
  - wiki/topics/ai/MCP.md
  - wiki/topics/ai/Prompt.md
---
# Agent 驱动 Wiki 的维护流程

## 问题

在一个文件优先、可审阅的 wiki 里，agent 应该怎样参与维护，而不是只做一次性问答？

## 简答

可持续做法不是让 agent 直接改一切，而是把知识库分成 `raw`、`wiki`、`rules` 三层：`raw` 保留原始事实，`wiki` 沉淀可更新结论，`AGENTS.md` / `SCHEMA.md` 约束 agent 的写法与边界；agent 负责 ingest、query、lint 一类重复整理，人负责范围、判断和审阅。

## 综合结论

- 从仓库治理看，这个库已经把 agent 的职责限定得比较清楚：`raw/sources/` 是 append-only 的事实层，`wiki/` 是可整理的知识层，`index.md` 和 `log.md` 负责把改动变成可导航、可追踪的记录。
- 从 `deep-research-report.md` 的方法论看，agent 最适合承担三类工作：
  - ingest：读原始资料，补主题页、综合页、对比页，并同步索引与变更记录；
  - query：把已经问出来、且具有复用价值的答案沉淀回 `wiki/syntheses/` 或 `wiki/comparisons/`；
  - lint：定期找出重复页、过薄页、孤儿页、过时页和缺失页。
- 这个仓库与研究报告里的原型并不完全相同。报告里出现过 `drafts/` / `inbox/` 作为缓冲区，但当前仓库明确取消了这两个目录，改成 `branch + PR` 审阅。因此这里的质量闸门不是“起草区”，而是 Git 分支、diff 和 PR。
- 这意味着 agent 的最佳工作方式不是“直接当编辑器”，而是“先做高重复、高结构化的整理，再把结论变成可审阅的变更集”。本轮并行清理 topic，以及把对比/综合页落成 PR，就是这种工作方式的具体体现。
- 从知识类型看，agent 更适合处理：
  - frontmatter、来源指针、坏链、导航同步；
  - 多页之间的交叉整理；
  - 把问答结果沉淀成 synthesis / comparison。
- 人仍然应保留三类关键判断：
  - 这个改动是否值得进入长期知识层；
  - 当前结论是否足够稳；
  - 这次改动是否应以小 PR、还是像本轮这样按明确要求做并行大扫除。

## 未决问题

- 当前仓库虽然有 `bin/wiki ingest/query/lint`，但还没有把 lint 输出稳定收敛成一套长期 backlog 视图。
- `journals/` 仍未接入当前仓库，因此“从日记里抽长期结论”的流程还没有真正跑顺。
- 后续如果 `syntheses/` 和 `comparisons/` 继续增长，可能需要更明确的索引结构，而不只是把它们挂到 `index.md` 的尾部。

## 来源指针

- `AGENTS.md`
- `SCHEMA.md`
- `deep-research-report.md`
- `wiki/topics/ai/Agent.md`
- `wiki/topics/ai/Code Agent.md`
- `wiki/topics/ai/MCP.md`
- `wiki/topics/ai/Prompt.md`
