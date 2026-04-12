# Wiki 规则

这个仓库是一个文件优先、兼容 Obsidian 的 wiki。agent 可以参与维护，但所有非微小改动都必须通过分支和 PR 进行审阅。

## 目标

- 保持知识库脱离单一应用后仍然可读。
- 让 agent 承担重复性的整理工作。
- 让长期知识变更始终有可审阅的变更记录。

## 仓库结构

- `raw/sources/`：不可变的原始输入、迁移残留、素材文档、原始笔记
- `raw/assets/`：页面引用的图片和附件
- `wiki/topics/`：稳定主题页，同时容纳概念页和具体对象页
- `wiki/syntheses/`：多来源综合页，用来沉淀整合后的理解
- `wiki/comparisons/`：对比、选型、取舍页
- `index.md`：知识库总导航
- `log.md`：重要知识变更的追加式记录
- `SCHEMA.md`：页面类型和写作约定

## 工作流规则

1. 不使用 `drafts/` 和 `inbox/`。审阅统一通过分支和 PR 完成。
2. 不要做缺乏说明的大范围重写。所有改动都应保持聚焦和可审阅。
3. 把 `raw/` 视为追加式区域。除非用户明确要求，否则不要删除或重写原始资料。
4. 当 `wiki/` 下新增页面或对页面做了实质更新时，如果导航发生变化，也要同步更新 `index.md`。
5. 对有意义的知识变更，在 `log.md` 中追加一条简短记录，包含日期、受影响页面和来源指针。
6. 优先按主题或决策问题拆成小 PR，不要做超大迁移 PR。

## 标准入口

这个仓库不依赖项目内 skill。统一通过 `bin/wiki` 作为 agent 的标准入口。

- `bin/wiki ingest <source>`：为新来源生成标准 ingest 提示词
- `bin/wiki query <question>`：为知识问答生成标准 query 提示词
- `bin/wiki lint`：为巡检知识库生成标准 lint 提示词
- `bin/wiki migrate <logseq-page>`：为 Logseq 页面迁移生成标准 migrate 提示词

使用要求：

1. 在执行任意命令前，先阅读 `AGENTS.md`、`SCHEMA.md`，必要时补读 `index.md` 和 `log.md`。
2. `bin/wiki` 负责编译工作流提示词，不替代实际的审阅和页面修改。
3. agent 的写入仍然必须遵守 branch + PR 审阅规则。

## 迁移规则

1. 旧 Logseq 仓库中的 `pages/` 是主要迁移来源。
2. `journals/` 默认不迁移。只有当其中包含现有迁移页面未覆盖、且值得长期沉淀的内容时，才允许抽取。
3. 不要把 daily notes 作为 daily notes 迁入新库。
4. 尽量保留有价值的 `[[wikilinks]]`、代码块和图片引用。
5. 如果一个迁移笔记本质上只是链接堆、摘录堆或半成品，应先放入 `raw/sources/`，或者重写成合格的 wiki 页面后再合并。

## 分类规则

迁移后的页面统一使用英文分类。分类的目标是帮助导航和批量迁移，不是为了过度细分。

当前使用这一组一级分类：

- `frontend`：React、CSS、RSC、Web Components、状态管理、组件库、渲染层相关主题
- `ai`：LLM、GPT、MCP、Agent、RAG、Prompt、AI 工作流相关主题
- `languages`：TypeScript、JavaScript、Rust、Go、ClojureScript、ReScript、Zig 以及语言特性
- `systems`：操作系统、网络、编译器、运行时、文件系统、数据库等底层主题
- `algorithms`：数据结构、动态规划、图论、贪心、LeetCode、解题方法
- `architecture`：软件设计、设计模式、依赖注入、技术方案、系统设计
- `tooling`：npm、Yarn、Bundler、CLI、编辑器、DevTools、工程工具链
- `product`：SaaS、知识工具、开发者工具产品、产品观察、UX 参考
- `career`：招聘、面试、自由职业、职业发展
- `life`：读书摘录、金句、理财、生活、非工作类长期笔记

使用方式：

1. 每个迁移后的页面只选一个主分类。
2. 次级主题不要再发明第二层分类，交给 `tags` 或页面链接表达。
3. 如果页面无法归入上述分类，优先判断它是否应留在 `raw/sources/`，不要随手塞进 `misc`。
4. 同一个页面类型下，按分类子目录存放，例如：
   - `wiki/topics/frontend/...`
   - `wiki/syntheses/ai/...`
   - `wiki/comparisons/product/...`

分类治理：

1. 这组一级分类当前默认冻结，迁移过程中不要随意新增。
2. 只有同时满足以下条件时，才允许新增一级分类：
   - 已经积累出一批稳定页面，而不是零散主题
   - 放进现有分类会长期别扭
   - 它代表长期领域，而不是短期热点或单一技术名词
3. 像 `react`、`rsc`、`mcp`、`typescript`、`security`、`web3` 这类更细粒度主题，优先通过 `tags` 表达，而不是立刻升为一级分类。

## Tag 规则

1. `tags` 用来表达横向主题、技术名词、上下文和交叉语义，不用来代替主分类。
2. 每个页面可以没有 `tags`，但推荐保留 1 到 5 个高价值 tag。
3. `tags` 优先使用英文、小写、短词，例如 `react`、`rsc`、`mcp`、`performance`。
4. 当一个页面同时和多个主题相关时，目录只保留一个主分类，其余语义通过 `tags` 和页面链接表达。
5. 如果某个 tag 长期出现并形成稳定页面簇，再考虑是否升级为新的一级分类。

## 轻改原则

迁移默认遵循“轻改而非重写”：

1. 优先保留原始内容的措辞、段落顺序、bullet 结构、代码块和图片引用。
2. 允许做的编辑包括：补 frontmatter、补标题、补来源指针、修复明显坏链、移动到正确页面类型和分类目录。
3. 只有在页面明显属于半成品、重复页或结构严重混乱时，才允许重写。
4. 如果一页内容有价值但还不适合直接进入 `wiki/`，优先放进 `raw/sources/`，不要为了迁移完成率强行洗稿。

## 写作规则

1. 使用兼容 Obsidian 的纯 Markdown。
2. 文档默认使用中文书写；必要时保留更清晰的英文技术术语。
3. 原始事实和综合结论要分开表达。
4. 任何非平凡结论都应附带来源指针。
5. 如果一个页面无法明确归入其他类型，默认放到 `wiki/topics/`。

## 页面职责

- `wiki/topics/`：回答“这是什么？”
- `wiki/syntheses/`：回答“目前综合后的理解是什么？”
- `wiki/comparisons/`：回答“该怎么选？取舍是什么？”
