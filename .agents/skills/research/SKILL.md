---
name: research
description: 围绕主题开展深度调研并沉淀为可审阅的 Wiki 页面；当问题需要引入新来源、综合证据与形成长期结论时使用。
---

操作：research

你正在为这个 wiki 执行一次深度调研，并准备把结论沉淀为可审阅的 wiki 页面。

开始前必须先阅读：
- `AGENTS.md`
- `SCHEMA.md`
- `index.md`

工作要求：
- 写页面或选择配图前，先读 [页面类型与写作参考](../ingest/references/page-writing.md)，配图按其中的「配图选择与核对」执行
- 先明确调研对象、对比对象、源码快照或资料日期；对时效性强的信息使用当前可核验来源
- 区分原始事实、源码/文档证据、综合判断和推断；不要把猜测写成事实
- 优先使用官方文档、源码、release note、仓库文件、规范和一手资料；网页调研要记录来源链接
- 如果涉及实现调研，必须阅读关键入口、领域模型、数据流、存储边界、扩展点、运行时边界和测试/验证入口
- 如果涉及对比调研，必须说明每个对象的所有权、运行位置、核心 loop、数据治理、扩展性、成本和锁定风险
- 不要新增项目内 `.codex/skills` 或本地 skill；本仓库的 agent 工作流统一沉淀在 `bin/wiki` 和 `prompts/`

深度验收项：
- 涉及系统实现或运行机制时，按需补充系统架构图、核心数据流/生命周期图，以及扩展面或边界图（具体规范见 [配图选择与核对](../ingest/references/page-writing.md#配图选择与核对)）
- 对比类调研涉及架构或执行链路差异时，补充双方架构差异图
- 包含证据矩阵，至少覆盖：结论、证据来源、证据位置、置信度或限制
- 按 [验证记录与使用限制](../ingest/references/page-writing.md#验证记录与使用限制) 区分知识正文、raw 证据和 PR 验收；有尚未决定的具体选择时再设置相应小节，不留占位内容。

输出目标：
- 判断应新增或更新 `wiki/topics/`、`wiki/syntheses/` 还是 `wiki/comparisons/` 页面
- 新页面应带 `SCHEMA.md` 约定的 frontmatter，并在单独打开时自洽
- 如果导航发生变化，更新 `index.md`
- 把日期、受影响页面、来源和验证结果写进 PR body
- 为 PR 写出简短摘要，说明调研范围、来源、图表、验证方式和剩余风险

验证要求：
- 运行 `bin/wiki check` 与 `bin/wiki check-jargon --base origin/main`
- 运行 `git diff --check`
- 运行 `bash tests/wiki-cli.sh`
- 对新增 Mermaid fence 做成对与语法检查（注意 `sequenceDiagram` 禁用未转义 `;` 等规则，见 `../ingest/references/page-writing.md#配图选择与核对`）；生成图片须逐张读图核对文字与箭头
- 创建或修改 PR 前运行 `PR_TITLE="..." PR_BODY="..." node tests/pr-metadata.mjs` 预检 PR 标题与正文格式

目标目录：
- topics：`wiki/topics/`
- syntheses：`wiki/syntheses/`
- comparisons：`wiki/comparisons/`
