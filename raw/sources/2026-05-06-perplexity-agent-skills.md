# Designing, Refining, and Maintaining Agent Skills at Perplexity

- 来源：Perplexity Research
- 发布时间：2026-05-01 / 页面元数据发布时间 2026-05-06
- URL：https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity
- 读取时间：2026-05-06

## 来源事实摘录

文章是 Perplexity Agents team 用于设计、评审和维护 Agent Skills 的内部指南公开版。它强调：高质量 Skill 的开发直觉和传统软件开发不同，很多对代码有用的原则在 Skill 里会变成反模式。

## 核心观点

### Skill 不是普通软件，而是模型与环境的上下文工程

Perplexity 将 Skill 至少看作四件事：

1. **Directory**：Skill 不是单个 `SKILL.md`，而是包含 `SKILL.md`、`scripts/`、`references/`、`assets/`、`config.json` 等文件的目录。
2. **Format**：根 `SKILL.md` 需要 name 和 description，且 name 要和目录名对应。description 是路由触发器，不是功能说明。
3. **Invocable**：Skill 运行时按需加载，不总是放入上下文；Perplexity Computer 会调用 `load_skill`，把 Skill 目录复制到隔离 sandbox，递归加载 `depends:`，再剥离 frontmatter。
4. **Progressive**：Skill 有渐进式上下文成本：index 只加载 name/description；load 阶段加载 `SKILL.md`；runtime 阶段按需读取 scripts、references、assets、subskills 等文件。

### Zen of Skills 与 Zen of Python 相反

文章用 Python 之禅反向说明 Skill 写作原则：

- 代码里 simple is better than complex；Skill 里复杂性本身是特性，因为 Skill 是 folder，不是 file。
- 代码里 explicit is better than implicit；Skill 激活依赖隐式意图匹配和 progressive disclosure。
- 代码里 sparse is better than dense；Skill 里 context 昂贵，要最大化每 token 信息量。
- 代码里 special cases 不该破坏规则；Skill 里 gotchas 是最高价值内容。
- 如果实现很容易解释，代码里可能是好主意；Skill 里如果容易解释，模型往往已经知道，应删除。

### 什么时候需要 Skill

需要 Skill 的情况：

- 没有特殊上下文时 agent 会做错。
- 需要跨运行保持高度一致，降低非确定性。
- 知识是 durable 的，但不在训练数据中。
- 企业内部工作流、领域边界、审美品味、判断标准等无法用一句 prompt 稳定表达。

不需要 Skill 的情况：

- 只是列一串模型已经知道的命令，例如常规 git 操作。
- 重复系统提示词里已有的全局规则。
- 目标内容变化速度快于维护速度，例如频繁变化的远端 MCP 工具列表。

文章提出一个句子级测试：**如果没有这句话，agent 会不会做错？** 如果不会，就不该放进 Skill，因为每个 Skill 都是 token tax。

### 如何构建 Skill

Perplexity 的流程是：

0. **先写 evals**：包含真实用户查询、已知失败、相邻领域混淆；正例和负例都要有，负例尤其有价值。
1. **写 description**：这是最难的一行。description 是 routing trigger，不是文档。好的 description 描述用户什么时候会需要它，最好来自真实 query，目标 50 词以内，以 `Load when...` 开头，不要总结 workflow。
2. **写 body**：不要写模型已经知道的显然步骤。不要把人类 README 风格的逐条命令搬进 Skill；要写意图、边界、失败处理和 gotchas。
3. **用层级**：确定性逻辑放 `scripts/`，重文档放 `references/`，输出模板和 schema 放 `assets/`，首次配置放 `config.json`。条件性或分支性内容从 `SKILL.md` 拆出去。
4. **迭代**：在分支上用 hero query 和 evals 迭代；description 的小改动可能对路由产生大影响。
5. **发布**。

### 如何维护 Skill

维护重点是 gotchas flywheel 和 eval suites。

- Agent 某事失败：添加 gotcha。
- Skill 错误加载：收紧 description，添加 negative evals。
- Skill 该加载却没加载：增加关键词和 positive evals。
- 系统提示词变化：检查重复和冲突。

Skill 大体是 append-mostly 的，最有价值的部分通常是 gotchas，而不是不断扩写长指令。Perplexity 会跑多类 eval：Skill loading / file reads、progressive loading、端到端任务完成，并且要跨不同 orchestration model family 测试，因为 GPT、Claude Opus、Claude Sonnet 对 Skill 的行为会不同。

## 可迁移结论

- Skill 是上下文预算下的能力封装，不是文档仓库。
- description 是全局路由接口，每个词都有外溢风险。
- Skill 的新增会影响其他 Skill，存在 action at a distance。
- gotchas 和 negative examples 比泛泛说明更值钱。
- 好 Skill 需要 eval 驱动，不适合五分钟 one-shot 生成。
- 自生成 Skill 不可靠；模型未必能可靠写出自己受益的 procedural knowledge。
