---
title: Agent Harness 的设计取舍
description: 持续追踪 agent harness 当前实践中的设计取舍：工具组合放沙箱还是上下文、组合执行落在信任分层哪一层、补偿型脚手架何时退役、多 agent 共享状态走文件系统还是平台会话、中立 harness 与厂商平台化的边界。
type: topic
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
  - raw/sources/2026-09-29-you-said-no-mcp.md
  - https://earendil.com/posts/you-said-no-mcp/
  - raw/sources/2026-02-08-why-claude-code-dropped-todos-slash-commands.md
  - https://tonylee.im/en/blog/why-claude-code-dropped-todos-slash-commands/
  - raw/sources/2026-04-15-openai-agents-sdk-evolution.md
  - https://openai.com/zh-Hans-CN/index/the-next-evolution-of-the-agents-sdk/
  - raw/sources/2026-10-01-claude-code-task-tools-docs.md
  - https://code.claude.com/docs/en/agent-sdk/todo-tracking
  - https://code.claude.com/docs/en/tools-reference
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
resource:
  - raw/sources/2026-09-29-you-said-no-mcp.md
  - https://earendil.com/posts/you-said-no-mcp/
  - raw/sources/2026-02-08-why-claude-code-dropped-todos-slash-commands.md
  - https://tonylee.im/en/blog/why-claude-code-dropped-todos-slash-commands/
  - raw/sources/2026-04-15-openai-agents-sdk-evolution.md
  - https://openai.com/zh-Hans-CN/index/the-next-evolution-of-the-agents-sdk/
  - raw/sources/2026-10-01-claude-code-task-tools-docs.md
  - https://code.claude.com/docs/en/agent-sdk/todo-tracking
  - https://code.claude.com/docs/en/tools-reference
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# Agent Harness 的设计取舍

## 摘要

harness 的基础定义（system prompt、tools、agentic loop、translation layer）见 [[agent-harness]]。这页在它之下持续追踪一个更细的问题：**各家 harness 当下正在做哪些设计取舍，落点在哪**。

2026 年 2 月到 9 月的三份来源（Claude Code、OpenAI、Pi）给出五个正在被实践的维度：

| 维度 | 取舍两边 | 当前落点 | 主要来源 |
| --- | --- | --- | --- |
| 工具组合放哪 | 上下文接力 vs 代码沙箱 | 移进代码沙箱 | Pi、OpenAI |
| 组合执行放哪 | 并进 agent loop 或工具沙箱 vs 单独一层 | 受信侧受限沙箱（第三层） | Pi |
| 脚手架留不留 | 补偿模型短板 vs 拆除减负 | 补偿型随模型退役；协作型保留，但任务工具组按模型门控 | Claude Code |
| 多 agent 共享状态 | 文件系统协议 vs 平台会话原语 | 两条路线并行 | Claude Code、OpenAI |
| harness 归谁 | 用户可拥有的中立层 vs 厂商平台 | 并存且开始竞争 | Pi、OpenAI |

## 取舍一：工具组合——上下文接力还是代码沙箱

**上下文接力**是默认形态：工具逐个暴露给模型，模型逐个调用、逐个阅读返回，组合靠模型在上下文里完成。它的问题是 token 成本随组合深度上升，组合表达力受限于模型的注意力——没有循环、没有并发、没有中间变量暂存。按 Pi 文中的判断，当前多数 MCP server 就是按这个假设建的：为「把工具倒进上下文」的 harness 优化，返回纯文本省 token。

**代码沙箱**把组合移出上下文：模型生成一段 JS，在沙箱里用控制流、并发和中间状态编排工具调用，只把结构化结论带回。Pi 的 Codemode 与 OpenAI 的 Programmatic Tool Calling（[[openai-programmatic-tool-calling]]）是同一模式在 harness 侧与服务端的两个版本。Pi 的类比是 shell：CLI 之所以至今是 agent 最顺手的工具面，是因为 shell 天生就是组合引擎（bashisms）；Codemode 是把这套组合方式搬进 harness 受信侧，组合表达力从模型的注意力换成 JS 控制流。

**Codemode 与 MCP 是互补而非替代**。Pi 把 MCP 接进核心时的判断：Pi 需要的和 MCP 需要的是同一个东西——一个解释器形式的沙箱。没有组合沙箱，MCP 只能被逐个倒进上下文（协议层已有结构化输出与发现机制，「难以组合」更多是 server 生态的用法惯性，不是协议缺陷）；没有 MCP，沙箱只有内置工具可组合，接不上 Linear、GitHub 这类外部生态。Pi 给 MCP 的定位「带智能工具发现的 OpenAPI」要放在这个语境读：[[mcp]] 页的协议时间线（无状态化解决部署与路由）之外，这是 harness 侧使用效率的线索。MCP 进核心而非扩展的技术原因也在组合这层：deferred tool loading、codemode-only 工具需要 harness 的 tool loadout 元数据做分流，普通 MCP 扩展拿不到这种元数据。

Linear + Jev 的例子是这条组合链的完整形态：MCP 供给工具面（拉 167 个 issue 的评论），Codemode 供给组合引擎（四个并行 worker、`store()` 暂存中间结果、只把统计带回），整条流水线「不浪费任何 context」。

**限定**：[[openai-programmatic-tool-calling]] 页已有的边界仍然成立——语义判断、审批、高影响写入和最终引用默认走直接工具调用，不是所有阶段都值得程序化。

## 取舍二：组合执行的位置——信任分层的哪一层

Pi 文中对执行位置的说明：harness 执行工具分两侧——bash 运行的位置在不受信沙箱里，agent loop 运行的位置在受信环境里，两侧信任级别完全不同。Codemode 选了第三个位置：**受信侧的受限沙箱**。harness 的执行面因此是三层：

| 层 | 运行位置 | 信任与权限 | 例子 |
| --- | --- | --- | --- |
| Agent loop | harness 进程 | 受信：用户环境、完整权限、持有会话状态 | 模型请求循环、路由、持久化 |
| 组合沙箱 | harness 侧的隔离运行时 | 受信环境内受限执行：只能调用被暴露的工具和模型 | Pi Codemode（JS/WASM）、OpenAI PTC（托管 V8） |
| 工具执行 | 外部沙箱 | 不受信：假定代码与返回数据都可能出问题 | bash、MCP server、shell 工具 |

组合沙箱必须单独成层的逻辑：组合要同时拿到多个工具的中间结果，必须站在能调用所有工具的位置，也就是 agent loop 一侧；但它执行的是模型生成的代码，不能直接给 harness 的完整权限，所以用 JS/WASM 这类可分发、可隔离的运行时兜底。它比工具沙箱更可信（执行与状态都留在会话内），又比 harness 本身更受限（状态落在会话记录里，不落到文件系统）。

**信任位置决定状态位置**：Codemode 的状态保存在 session transcript 而不是文件系统，组合过程的中间结果因此成为一等会话状态——可审计、可随会话恢复（对照 [[persistent-agent-harness-design-patterns]] 的 tree 与 operation log 分离），而不是散落在临时文件里。OpenAI 是同一分层的两种产品化：PTC 的 V8 每次执行互相隔离，Sandbox 原语把不受信那一侧标准化成平台能力。

## 取舍三：补偿型脚手架——随模型退役还是保留

TodoWrite 原本补偿的是模型自管状态能力弱：长任务里模型容易丢线索，外部清单是一层外挂状态，每完成一步靠重读清单重新对齐「做到哪了、还剩什么」。这层外挂有三项持续成本——每次更新是一次工具调用往返，清单本身占用上下文，模型还要维护「内在计划」与「外部清单」两份状态并保持同步。Claude Code 的官方解释（2026-02，经 Tony Lee 转述）：Opus 4.5 能更长时间自主运行、更有效跟踪状态，小任务上外部清单从帮助变成开销。同步开销超过对齐收益时，工具退役。

**退役的只是补偿部分**：Tasks 留下并强化的恰好是非补偿的部分——任务依赖元数据、跨会话共享的 Task List（`CLAUDE_CODE_TASK_LIST_ID`）。这些是协作结构，模型再强也不会自己长出来。Slash Commands → Skills 是同构拆分：progressive disclosure 是「模型不会自己找上下文」的补偿，被 Skills 自动装配上下文取代；SKILL.MD 引用其他文件形成的多步上下文链是协作资产，留下了。

两个工具的机械对比（官方 tools-reference 与 todo-tracking 文档，2026-10 查证）：

| | TodoWrite | Tasks（TaskCreate / TaskGet / TaskUpdate / TaskList） |
| --- | --- | --- |
| 工具形态 | 单工具，一次调用重写整张清单 | 四个工具：建 / 查 / 改 / 列，按任务 ID 增量更新 |
| 数据模型 | 条目数组，状态 pending / in_progress / completed | 任务带 subject 与状态生命周期（completed 或 deleted 收尾），依赖与阻塞由 TaskUpdate 维护 |
| 清单归属 | 会话内的自我对齐清单，只在本会话存在 | 共享任务清单：多会话、子 agent、agent teams 队友都可读写，`CLAUDE_CODE_TASK_LIST_ID` 让多个实例共享同一清单 |
| 消费者 | 只有模型自己 | 模型之外的协调载体：其他会话认领工作、人查看进度 |
| 默认状态 | 仍存在但默认关闭，`CLAUDE_CODE_ENABLE_TASKS=0` 可切回 | 有这组工具的会话里的默认 |

**门控比博客知道的走得更远**：changelog 显示 v2.1.233 起 TodoWrite 与 Task 工具组在 Opus 4.8、Sonnet 5、Fable 5、Mythos 5 及更新模型上整体不再提供；v2.1.268 收敛为现行规则——默认只提供给 Claude 3.x、Opus 4.0–4.7、Sonnet 4.0–4.6、Haiku 4.5，其余模型需 `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` 或 allowedTools 显式启用。官方给的理由与本页的补偿逻辑同向：「新模型无需书面清单即可跟踪多步工作，工具定义与提醒占用上下文」。两个例外值得注意：后台会话与云端会话在所有模型上保留这组工具；子 agent 仅当主会话有这组工具时才有，没有 Task 工具的 agent teams 队友改用消息而非共享任务清单协调。

**限定**：这条取舍的前提是绑定最新强模型。[[agent-harness-evolution-paradigm]] 里 HarnessX 的 inverse-scaling 结论（弱模型从 harness 改进中获益更大）说明对弱模型外部清单仍是净收益；「协作层保留」也要按门控来读——协作工具的价值没有变，但交互式会话里「谁默认拥有它」成了模型能力的函数。对 harness 维护者的操作含义：每个补偿型机制都记录它补偿的短板和退役条件——没有退出条件的补偿层会累积成模型不需要时也不肯走的遗产。

## 取舍四：多 agent 共享状态——文件系统还是平台原语

Claude Code 的落点是**文件系统**：Tasks 的依赖与阻塞存为任务间元数据，多个 session 和子 agent 通过文件系统协调，共享 Task List 的会话自动同步；Skills 侧 `agent:` 生成加载技能的子 agent、`context: fork` 克隆完整当前上下文给子 agent。这与 [[agent-team-roles-and-collaboration]] 的「文件系统是 agent 间的通信协议」同一方向，且更具体：跨会话共享状态不必发明新协议，任务清单落在文件系统上、由 harness 同步。

OpenAI 的落点是**平台会话**：Sessions 提供长任务的检查点与恢复（几天后可继续），并与 Chat 后端会话融合为统一 API。Pi 的 harness-v2 用 lanes + append-only tree 解决同类问题（[[persistent-agent-harness-design-patterns]]）。

三条路线解决的是同一问题——多 agent / 多会话的状态切分、共享与合并。文件系统路线不引入新协议、对用户可读可改；平台会话路线把恢复与审计做成默认能力。当前看不出收敛，更像是本地优先 harness 与平台 harness 各自的自然选择。

## 取舍五：中立 harness 还是厂商 harness

[[agent-harness]] 的核心主张是 translation layer 带来用户自主权：换模型、数据本地、可定制。OpenAI 2026-04 的动作把张力摆上台面：Agents SDK 演进为 Agent Server（`singleDeploy` 让同一代码本地与云端运行），Harness / Sandbox / Sessions 成为厂商原语，Codex CLI 直接构建其上——harness 从「用户拥有的软件层」变成「平台提供的服务」，而厂商 harness 天然为自家模型优化。

Pi 的应对值得记录：不是回避协议生态，而是把 MCP 接进核心、参与塑造它在小型 harness 里的用法（「影响一件事的最好方式是拥抱它」）。对中立 harness，协议层（MCP、[[agent-client-protocol]]）是少数能与厂商 harness 对齐的外部界面；放弃协议等于放弃话语权。

## 实践启发

- **组合优先在沙箱做**：与其在提示词里教模型逐个调用工具并阅读全部中间结果，不如把工具暴露给代码执行环境，让组合逻辑、并发和中间结果留在沙箱里；沙箱放受信侧、状态落会话记录，中间结果才可审计、可恢复。
- **给补偿型脚手架记账**：记录每个机制补偿的短板与退役条件，模型升级后逐项复查。
- **跨会话协作用文件系统**：共享任务清单、状态文件是多个会话 / 子 agent 协作的最小可行协议，不为此引入新通信机制。
- **明确平台化边界**：使用厂商 harness（Agent Server、Codex）时确认哪些能力被锁在厂商侧；需要模型选择权和工作流可控性的部分，留在中立 harness。

## 时间线

| 时间 | 事件 | 来源 |
| --- | --- | --- |
| 2026-02-08（02-18 更新） | Claude Code 用 Tasks 替换 TodoWrite、用 Skills 替换 Slash Commands | Tony Lee 对官方变更的解读 |
| 2026-04-15 | OpenAI 宣布 Agents SDK 演进为 Agent Server，新增 Harness / Sandbox / Sessions 原语与 Codex CLI | OpenAI 官方 |
| 2026-09-29 | Pi 把 MCP 接入核心，介绍 Codemode 沙箱 | Earendil 官方 |

## 保留判断

- 「unhobbling」最初是二手解读，但官方文档后来给出同向理由（新模型无需书面清单、工具定义占上下文）；Tony Lee 文中未见于官方文档的细节，引用前以官方 tools-reference / env-vars 为准。
- OpenAI Harness 处于 alpha，`agent.as_harness()` 等接口形态可能变化；appsec bug 减少 45%、修复速度 2.5 倍是 OpenAI 自述的早期信号，无外部验证。
- 三份来源均有立场：Pi 是 harness 厂商（为拥抱 MCP 的决定辩护），OpenAI 是平台方（推广平台化），Tony Lee 是基于 changelog 的推断。
- OpenAI 原文直连返回 403，raw 素材是 web reader 提取的重构版而非逐字副本，关键 API 示例保留原文。

## 相关页面

- [[wiki/topics/ai/agent-harness|Agent Harness]]
- [[agent-harness-evolution-paradigm]]
- [[persistent-agent-harness-design-patterns]]
- [[openai-programmatic-tool-calling]]
- [[mcp]]
- [[claude-5-context-engineering]]
- [[agent-team-roles-and-collaboration]]

## 来源指针

- `raw/sources/2026-09-29-you-said-no-mcp.md` / [You Said No MCP! — Earendil，2026-09-29](https://earendil.com/posts/you-said-no-mcp/)
- `raw/sources/2026-02-08-why-claude-code-dropped-todos-slash-commands.md` / [Why Claude Code Dropped Todos and Slash Commands — Tony Lee，2026-02-08](https://tonylee.im/en/blog/why-claude-code-dropped-todos-slash-commands/)
- `raw/sources/2026-04-15-openai-agents-sdk-evolution.md` / [Agents SDK 的全新演进 — OpenAI，2026-04-15](https://openai.com/zh-Hans-CN/index/the-next-evolution-of-the-agents-sdk/)
- `raw/sources/2026-10-01-claude-code-task-tools-docs.md` / [Track todos — Claude Code 官方文档](https://code.claude.com/docs/en/agent-sdk/todo-tracking)、[Tools reference（task-tool availability）](https://code.claude.com/docs/en/tools-reference)、[CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
