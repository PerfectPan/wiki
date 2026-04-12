# 知识库治理与迁移实施计划

> **给 Claude：** 必须使用 `superpowers:executing-plans` 按任务逐步执行这份计划。

**目标：** 建立适用于文件优先 wiki 的治理文档、核心目录结构和迁移规则，并统一采用 branch + PR 代替草稿目录审阅。

**架构：** 这个知识库保持 Obsidian 兼容，长期知识放在 `wiki/`，原始输入放在 `raw/`，操作规则由 `AGENTS.md` 和 `SCHEMA.md` 约束。Logseq 迁移按主题逐步推进，并通过小 PR 审阅。

**技术栈：** Markdown、Obsidian 兼容 wikilinks、Git branch/PR 工作流

---

### 任务 1：定义 agent 操作规则

**文件：**
- 新建：`AGENTS.md`
- 参考：`deep-research-report.md`

**步骤 1：编写规则**

写清楚 branch + PR 审阅模式、`raw/` 不可变约束、页面类型职责，以及 Logseq 迁移边界。

**步骤 2：核对规则是否匹配工作流**

确认文件明确写到：
- 不使用 `drafts/`
- 不使用 `inbox/`
- `journals` 默认不迁移
- 按主题拆小 PR

**步骤 3：提交**

```bash
git add AGENTS.md
git commit -m "docs: define wiki agent workflow"
```

### 任务 2：定义页面 schema

**文件：**
- 新建：`SCHEMA.md`
- 新建：`index.md`
- 新建：`log.md`

**步骤 1：写最小 schema**

定义三类页面：
- `topic`
- `synthesis`
- `comparison`

并补上最小 frontmatter 建议和页面模板。

**步骤 2：补上导航和日志**

创建 `index.md` 和 `log.md`，给后续迁移提供稳定入口。

**步骤 3：提交**

```bash
git add SCHEMA.md index.md log.md
git commit -m "docs: define wiki schema and navigation"
```

### 任务 3：创建长期目录结构

**文件：**
- 新建：`raw/sources/.gitkeep`
- 新建：`raw/assets/.gitkeep`
- 新建：`wiki/topics/.gitkeep`
- 新建：`wiki/syntheses/.gitkeep`
- 新建：`wiki/comparisons/.gitkeep`

**步骤 1：创建可追踪目录**

创建 schema 所需的 raw 和 wiki 子目录。

**步骤 2：验证结构**

执行：

```bash
find . -maxdepth 3 -type f | sort
```

预期：
- 根目录治理文件存在
- raw 和 wiki 子目录存在

**步骤 3：提交**

```bash
git add raw wiki
git commit -m "chore: scaffold wiki directories"
```

### 任务 4：准备迁移判断规则

**文件：**
- 修改：`AGENTS.md`
- 修改：`SCHEMA.md`
- 参考：旧 Logseq 仓库

**步骤 1：定义提升规则**

写清楚旧笔记怎么映射：
- 成熟概念页或对象页 -> `wiki/topics/`
- 多来源综合页 -> `wiki/syntheses/`
- 选型和取舍页 -> `wiki/comparisons/`
- 暂未成形的残留内容 -> `raw/sources/`

**步骤 2：定义 journal 策略**

明确说明 journals 不作为 daily notes 迁移，只抽取缺失的长期知识。

**步骤 3：提交**

```bash
git add AGENTS.md SCHEMA.md
git commit -m "docs: define migration heuristics"
```

### 任务 5：执行第一批迁移

**文件：**
- 新建或修改：`wiki/topics/...`
- 新建或修改：`wiki/syntheses/...`
- 新建或修改：`wiki/comparisons/...`
- 修改：`index.md`
- 修改：`log.md`

**步骤 1：选一个聚焦主题**

例如：
- React / RSC
- MCP / Agent tooling
- Software design

**步骤 2：只迁一小批**

把一组相关 Logseq 页面迁入新结构，保证 PR 可以在一次审阅中看完。

**步骤 3：更新导航和日志**

把新页面链接加入 `index.md`，并在 `log.md` 中登记这次迁移。

**步骤 4：提交**

```bash
git add wiki index.md log.md
git commit -m "docs: migrate first wiki topic batch"
```
