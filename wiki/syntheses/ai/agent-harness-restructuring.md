---
title: Agent Harness 的职责重构：沙箱组合、脚手架拆除与平台化
description: 综合 Pi 接回 MCP 与 Codemode、Claude Code 用 Tasks/Skills 替换 TodoWrite/Slash Commands、OpenAI Agents SDK 平台化三篇来源，梳理 2026 年秋 agent harness 层的职责重新分配。
type: synthesis
category: ai
created: 2026-10-01
updated: 2026-10-01
timestamp: 2026-10-01
tags:
  - agent
  - harness
  - mcp
  - claude-code
source_refs:
  - raw/sources/2026-10-01-you-said-no-mcp.md
  - https://earendil.com/posts/you-said-no-mcp/
  - raw/sources/2026-10-01-why-claude-code-dropped-todos-slash-commands.md
  - https://tonylee.im/en/blog/why-claude-code-dropped-todos-slash-commands/
  - raw/sources/2026-10-01-openai-agents-sdk-evolution.md
  - https://openai.com/zh-Hans-CN/index/the-next-evolution-of-the-agents-sdk/
resource:
  - raw/sources/2026-10-01-you-said-no-mcp.md
  - https://earendil.com/posts/you-said-no-mcp/
  - raw/sources/2026-10-01-why-claude-code-dropped-todos-slash-commands.md
  - https://tonylee.im/en/blog/why-claude-code-dropped-todos-slash-commands/
  - raw/sources/2026-10-01-openai-agents-sdk-evolution.md
  - https://openai.com/zh-Hans-CN/index/the-next-evolution-of-the-agents-sdk/
---

# Agent Harness 的职责重构：沙箱组合、脚手架拆除与平台化

## 问题

2026 年秋，Pi、Claude Code、OpenAI Agents SDK 几乎同时调整了 harness 层的设计：Pi 收回「不支持 MCP」的宣言，把 MCP 挪进核心并配上 Codemode 沙箱；Claude Code 两天内用 Tasks 替换 TodoWrite、用 Skills 替换 Slash Commands；OpenAI 把 Agents SDK 升级为 Agent Server，并开始以厂商身份提供 Harness、Sandbox、Sessions 三个原语。这些变化合在一起，说明 agent harness 这个层的职责正在怎么变？

## 简答

harness 层不是单纯变厚或变薄，而是职责重新分配：**工具组合从「往上下文里堆工具」移进代码沙箱**（Pi Codemode、OpenAI Programmatic Tool Calling），组合沙箱落在 agent loop 与工具执行之间的信任分层上；**为模型短板做补偿的脚手架随模型变强被拆除**（Claude Code 的 unhobbling）；**协作与共享状态的抽象在增厚**（Tasks 依赖与跨会话共享、Skills 子 agent 与 context fork）；同时 **harness 本身开始被厂商平台化**（OpenAI 的三原语与 Codex CLI）。

## 来源事实

### Pi：把 MCP 从「拒绝」变成核心，配 Codemode 沙箱

来源：Earendil 2026-09-29 博客 [“You Said No MCP!”](https://earendil.com/posts/you-said-no-mcp/)。

- Pi 曾在官网和实践访谈中公开宣称不支持 MCP（含 Mario Zechner 的《what if you don't need MCP》），现在 MCP 已进入核心功能。此前社区存在 `pi-mcp-adapter` 扩展。
- 进入核心的理由有两层：MCP 这一年本身变了；更关键的是改造所需的架构改动「普遍有用」——同样的改动让 Jev 这类模型更容易在 Pi 内使用。Pi 与 MCP 的共同需求是「一个解释器形式的沙箱」。
- MCP 最大的遗留问题是**难以组合**（hard to compose）。很多 MCP server 仍为「把工具倒进上下文」的 harness 而建，为省 token 返回纯文本。Pi 现在把 MCP 定位为「带智能工具发现的 OpenAPI」：工具应返回结构化数据、靠文档描述被发现。
- CLI 之所以好用，是因为 agent 用高效的 shell 组合方式把工具接起来；MCP 没有理由做不到——Pi 的 MCP 就建立在把工具暴露给 JavaScript 沙箱之上，Codex 等其他 harness 也是这么做的。
- harness 执行工具的位置分两侧：bash 运行的一侧（不受信沙箱）与 harness agent loop 运行的一侧（受信环境），两侧信任级别完全不同。
- **Codemode**：运行在 harness 侧（受信侧）的 JavaScript 沙箱，用于编排和组合工具调用；状态保存在 session transcript 里而不是文件系统；JS 可以作为 WASM 二进制分发并提供合理隔离。配置 MCP 时自动加载。
- MCP 进核心而不是扩展的直接原因：新模型支持 deferred tool loading、mid-conversation system messages、reasoning level 变化，工具需要元数据标记「只给 LLM」「只给 Codemode」或「deferred」，普通 MCP 扩展拿不到 Pi 的工具元数据。
- 策略表态：「影响一件事的最好方式是拥抱它」，想参与塑造 MCP server 与使用模式在小型 harness 里的形态，而不是在场边旁观。
- 示例：在 Pi 里用 Codemode 组合 Linear MCP 与 Jev 分类器，四个并行 worker 分析 167 个 open issue 的评论情绪，中间结果不进入模型上下文，「不浪费任何 context」。

### Claude Code：TodoWrite → Tasks，Slash Commands → Skills

来源：Tony Lee 2026-02-08 博客（02-18 更新），基于 Anthropic 官方变更的解读。

- Anthropic 两天内完成两项替换，官方说明都是「既有功能、行为不变」：Todos 变 Tasks，Slash Commands 变 Skills。
- TodoWrite 退役的官方解释：Opus 4.5 能更长时间自主运行、更有效跟踪自身状态，小任务不再需要外部清单——模型已经能自己规划，外部清单从帮助变成开销。
- Slash Commands 的 progressive disclosure 设计（按需加载上下文）随模型变强不再最优：Skills 自动读取相关文件装配上下文，SKILL.MD 可引用其他文件形成多步上下文链，从模型视角不需要单独的语法和工具。
- 作者把共同模式称为 **unhobbling**：随模型能力提升，拆除为模型局限性做补偿的脚手架。
- 同时两套抽象显著变强：Tasks 增加任务间依赖与阻塞的元数据、基于文件系统的多会话协调、共享 Task List 的跨会话自动同步（`CLAUDE_CODE_TASK_LIST_ID`）；Skills 增加 `agent:` 配置（加载技能生成子 agent）、`context: fork`（克隆完整当前上下文给子 agent）、调用方控制（用户 / 模型 / 两者）。
- 作者结论：简单任务直接交给模型并删掉工具；复杂协作围绕共享状态与上下文隔离建结构。未来 agent 系统的重点不在单个 agent 的能力，而在设计多个 agent 如何切分与合并状态。

### OpenAI：Agents SDK 升级为 Agent Server，厂商提供 harness 原语

来源：OpenAI 2026-09-30 官方博客 [Agents SDK 的全新演进](https://openai.com/zh-Hans-CN/index/the-next-evolution-of-the-agents-sdk/)。

- Agents SDK 从编排框架演进为 Agent Server：`singleDeploy: true` 让同一份代码本地和云端同一方式运行；云端提供 playground、统一 traces（本地日志自动同步）。
- 三个新原语：
  - **Sandbox**：Agent Server 内置的安全沙箱，运行自定义工具与 MCP 工具，提供完全系统访问的同时逻辑隔离网络 / 文件系统 / 进程，内置提示注入防护。早期数据：appsec bug 减少 45%，漏洞修复速度提升 2.5 倍。
  - **Sessions**：长任务的检查点与恢复，几天后可继续；与 Chat 后端会话融合为统一会话 API。
  - **Harness**（alpha）：agent 运行的容器，为每个会话提供隔离的沙箱化环境，内置工具和 MCP server 在会话内可用，把 agent 当完整应用而非请求处理函数；`agent.as_harness()` API。
- 新 Codex CLI 完全基于 Agents SDK 构建，原生支持 MCP server 与中间件，可从 CLI 无缝迁移到云端。
- Sandbox、Sessions、Harness、Chat 正在收敛为统一 API，几个月内推出 beta。

## 综合结论

### 1. 工具组合的职责从上下文移进代码沙箱

三家里有两家把「组合工具」从模型上下文移进了代码执行环境。Pi 的 Codemode 运行在 harness 受信侧，用 JS 编排工具调用，中间结果留在沙箱、只把结构化结论带回；OpenAI 的 Programmatic Tool Calling 是同一模式的服务端版本（见 [[openai-programmatic-tool-calling]]）。Pi 点破的动机是：MCP server 为「把工具倒进上下文」的 harness 而建、返回纯文本省 token，这让工具难以组合；把工具暴露给沙箱后，agent 可以像用 shell 管道（bashisms）一样组合它们。

CLI 之所以至今仍是 agent 最顺手的工具面，正是因为 shell 天生就是组合引擎。Codemode 本质上是把 shell 这套久经考验的组合方式搬进了 harness 受信侧：中间结果不再流经模型上下文，组合的表达力从模型的注意力换成 JS 控制流。

### 2. Agent loop 与工具执行的信任分层

Pi 文里对 Codemode 位置的解释值得单独拿出来：harness 执行工具分两侧——bash 运行的位置在不受信沙箱里，agent loop 运行的位置在受信环境里，两侧信任级别完全不同。Codemode 是第三种东西：**受信侧的受限沙箱**。harness 的执行面由此分成三层：

| 层 | 运行位置 | 信任与权限 | 例子 |
| --- | --- | --- | --- |
| Agent loop | harness 进程 | 受信：用户环境、完整权限、持有会话状态 | 模型请求循环、路由、持久化 |
| 组合沙箱 | harness 侧的隔离运行时 | 受信环境内受限执行：只能调用被暴露的工具和模型 | Pi Codemode（JS/WASM）、OpenAI PTC（托管 V8） |
| 工具执行 | 外部沙箱 | 不受信：假定代码与返回数据都可能出问题 | bash、MCP server、shell 工具 |

组合沙箱必须单独成层，而不是并进另外两层。组合逻辑要同时拿到多个工具的中间结果，所以它必须站在能调用所有工具的位置，也就是 agent loop 一侧；但它执行的又是模型生成的代码，不能直接给它 harness 的完整权限，所以需要 JS/WASM 这类可分发、可隔离的运行时兜底。它比工具沙箱更可信（执行与状态都留在会话内），又比 harness 本身更受限（状态落在会话记录里，不落到文件系统）。

信任位置直接决定状态位置：Codemode 的状态保存在 session transcript 而不是文件系统，组合过程的中间结果因此成为一等会话状态——可审计、可随会话恢复（对照 [[persistent-agent-harness-design-patterns]] 的 tree 与 operation log 分离），而不是散落在临时文件里。OpenAI 侧是同一分层的两种产品化：PTC 的 V8 每次执行互相隔离，Sandbox 原语则把不受信那一侧标准化成平台能力。

### 3. Codemode 与 MCP 互相成全：协议供给工具面，沙箱供给组合引擎

Pi 把 MCP 接进核心的动机，文章说得直白：Pi 需要的和 MCP 需要的是同一个东西——一个解释器形式的沙箱。两者互补，缺谁都不完整：

- **没有组合沙箱的 MCP**：工具被逐个倒进上下文，模型逐个调用、逐个阅读返回，组合靠模型在上下文里接力。这正是当前多数 MCP server 的设计假设——为「把工具倒进上下文」的 harness 而建，返回纯文本省 token。
- **没有 MCP 的 Codemode**：只能组合 harness 内置工具，接不上 Linear、GitHub 这类外部生态。沙箱有引擎，没有燃料。

因此 MCP「难以组合」这个最大遗留问题的归属变了：协议层已有结构化输出与发现机制，问题更多在 server 生态的用法惯性。Pi 的应对是拥抱并塑造——用 Codemode 从 harness 侧示范另一种用法（工具返回结构化数据、被程序组合），把自己变成协议用法演化的参与者。它给 MCP 的定位「带智能工具发现的 OpenAPI」也要放在这个语境里读：这是 [[mcp]] 页协议时间线（无状态化解决部署与路由，2026-07-28 版）之外的另一条线索——「工具返回结构化数据、可被程序组合」解决的是 harness 侧的使用效率，两条线索合起来才是 MCP 的完整定位。

进核心而非做成扩展，技术原因同样落在组合这层：新模型支持 deferred tool loading、mid-conversation system messages 和 reasoning level 切换，工具需要元数据标记「给 LLM」「只给 Codemode」「deferred」，普通 MCP 扩展拿不到 Pi 的 tool loadout，做不了这种分流。

Linear + Jev 的例子是这条组合链的完整形态：MCP 供给工具面（拉 167 个 issue 的评论），Codemode 供给组合引擎（四个并行 worker、`store()` 暂存中间结果、只把统计带回），整条流水线「不浪费任何 context」。

### 4. Unhobbling：补偿型脚手架有半衰期

Claude Code 的两个替换给出了一条维护原则：harness 里为模型短板做补偿的机制会随模型变强从「帮助」变成「开销」，应该被拆除。这与 [[claude-5-context-engineering]] 观察到的「堆规则、堆示例的约束失效」是同一现象的两面：模型能力上移后，靠外挂结构弥补能力的做法贬值。

TodoWrite 退役值得拆开看它补偿的是什么。早期模型自管状态能力弱，长任务容易丢线索，外部清单是一层外挂状态：模型每完成一步，靠重读清单重新对齐「做到哪了、还剩什么」。这层外挂有三项持续成本——每次更新是一次工具调用往返，清单本身占用上下文，模型还要维护「内在计划」与「外部清单」两份状态并保持同步。模型能力越过某个点后（官方解释：Opus 4.5 能更长时间自主运行、更有效跟踪状态），同步开销超过对齐收益，工具从辅助变成拖累。

但退役的只是补偿部分，清单这个概念没有被扔掉——Tasks 留下并强化的恰好是非补偿的部分：任务依赖元数据、跨会话共享。这些是协作结构，模型再强也不会自己长出来。Slash Commands → Skills 是同构的拆分：progressive disclosure 是「模型不会自己找上下文」的补偿，被 Skills 自动装配取代；而 SKILL.MD 引用其他文件形成的多步上下文链不是补偿，是协作资产。

两个限定仍然成立。其一，unhobbling 的前提是绑定最新强模型——对弱模型，外部清单仍是净收益，[[agent-harness-evolution-paradigm]] 里 HarnessX 的 inverse-scaling 结论（弱模型从 harness 改进中获益更大）正说明补偿型脚手架对弱模型有真实价值。其二，「Anthropic 官方称这为 unhobbling」是博主的转述，工程事实（两个工具被替换、新抽象变强）比叙事标签更可靠。

对 harness 维护者的具体含义：每加一个「帮模型绕过短板」的机制，都应记录它补偿的是什么短板、模型能力达到什么水平时可以退役。没有退出条件的补偿型脚手架会累积成模型不需要时也不肯走的遗产。

### 5. 拆掉的对面是协作层增厚

Claude Code 拆掉了简单任务的外挂，却给复杂协作加了三层结构：任务依赖成为元数据、Task List 通过文件系统跨会话共享、Skills 能 fork 上下文生成子 agent。结合 [[agent-team-roles-and-collaboration]] 已有的「文件系统是 agent 间的通信协议」，方向一致且更具体了：跨会话共享状态不必发明新协议，任务清单落在文件系统上、由 harness 同步，就是多 agent 协作的最小骨架。

三家在这点上不冲突：OpenAI 的 Sessions 解决的是同一问题的另一面（长任务跨执行的状态保持），Pi harness-v2 的 lanes 解决的是并行执行隔离（见 [[persistent-agent-harness-design-patterns]]）。多 agent 的状态切分、共享与合并，正在取代单 agent 能力成为 harness 设计的主要变量。

### 6. Harness 开始被平台化，中立 harness 的价值主张受到检验

OpenAI 把 Harness、Sandbox、Sessions 变成厂商原语，Codex CLI 直接构建其上——harness 从「用户拥有的软件层」变成「平台提供的服务」。这与 [[agent-harness]] 的核心主张直接相关：translation layer 让用户保留模型选择权，而厂商的 model-native harness 天然为自家模型优化，选择权被收回厂商侧。

Pi 的应对值得记录：不是回避协议生态，而是把 MCP 接进核心、参与塑造协议在小型 harness 里的用法。对开源中立 harness，协议层（MCP、Agent Client Protocol）是和厂商 harness 竞争时少数可以对齐的外部界面；放弃协议等于放弃话语权。

### 7. 状态与执行环境的分离正在成为共识

OpenAI Sessions（检查点、恢复、与 Chat 会话融合）和 Pi harness-v2（intent record、tree 与 operation log 分离、lanes）在解决同一个问题：长任务崩溃后的状态恢复与并行执行。区别在形态——前者是平台原语，后者是自研 harness 的内部设计。随着厂商把这类能力产品化，自研 harness 里「自己发明持久化规则」的部分会缩小，剩给独立 harness 的差异化空间在工具组合层、协议中立性和可定制性。

## 对个人 agent 系统的启发

- **组合优先在沙箱做**：与其在提示词里教模型逐个调用工具并阅读全部中间结果，不如把工具暴露给一个代码执行环境，让组合逻辑、并发和中间结果都留在沙箱里。Pi Codemode 和 OpenAI PTC 是现成参照；沙箱放在 harness 受信侧、状态落在会话记录里，中间结果才可审计、可恢复。
- **给补偿型脚手架记账**：每次为绕过模型短板增加机制时，写下它补偿的短板和退役条件；升级模型后逐项复查。
- **跨会话协作用文件系统**：共享任务清单、状态文件是多个会话 / 子 agent 协作的最小可行协议，不要为此引入新的通信机制。
- **关注平台化的边界**：使用厂商 harness（Agent Server、Codex）时明确哪些能力会被锁在厂商侧；需要模型选择权和工作流可控性的部分，留在中立 harness。

## 保留判断

- unhobbling 是二手解读框架而非可验证的工程结论；TodoWrite 退役对使用弱模型的用户可能是退化，本文只确认「替换发生了、新抽象变强了」这两个事实。
- OpenAI Harness 处于 alpha，`agent.as_harness()` 等接口形态可能变化；安全数据（-45% appsec bug、2.5x 修复速度）来自 OpenAI 自述的早期信号，无外部验证。
- 三篇来源均有立场：Pi 是 harness 厂商（为拥抱 MCP 的决定辩护），OpenAI 是平台方（为平台化叙事推广），Tony Lee 是基于 changelog 的推断。事实与叙事在来源事实一节已尽量分开。

## 相关页面

- [[wiki/topics/ai/agent-harness|Agent Harness]]
- [[agent-harness-evolution-paradigm]]
- [[persistent-agent-harness-design-patterns]]
- [[openai-programmatic-tool-calling]]
- [[mcp]]
- [[claude-5-context-engineering]]
- [[agent-team-roles-and-collaboration]]

## 来源指针

- `raw/sources/2026-10-01-you-said-no-mcp.md` / [You Said No MCP! — Earendil](https://earendil.com/posts/you-said-no-mcp/)
- `raw/sources/2026-10-01-why-claude-code-dropped-todos-slash-commands.md` / [Why Claude Code Dropped Todos and Slash Commands — Tony Lee](https://tonylee.im/en/blog/why-claude-code-dropped-todos-slash-commands/)
- `raw/sources/2026-10-01-openai-agents-sdk-evolution.md` / [Agents SDK 的全新演进 — OpenAI](https://openai.com/zh-Hans-CN/index/the-next-evolution-of-the-agents-sdk/)
