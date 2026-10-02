---
title: Agent Harness 的设计取舍
description: 追踪主流 Agent Harness 在工程演进中的关键设计抉择：工具组合在沙箱还是上下文执行、单兵任务清单何时退役、多 Agent 状态共享走文件还是平台原语、中立运行时与云厂商一体化的边界。
type: topic
category: ai
created: 2026-10-01
updated: 2026-10-02
timestamp: 2026-10-02
tags:
  - agent
  - harness
  - mcp
  - claude-code
  - cloud-runtime
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

Harness 的基础架构（System Prompt、Tools、Agent Loop、Translation Layer）参见 [[agent-harness]]。本页聚焦一线框架（Claude Code、OpenAI、Pi、Tetral）在实际工程落地中的六个关键取舍：

| 维度 | 痛点 / 矛盾 | 主流做法 / 演进方向 | 代表案例 |
| --- | --- | --- | --- |
| **工具组合方式** | 每次调用都把海量数据塞回上下文 vs 用代码在沙箱里批量执行 | 移进代码沙箱用脚本编排，只向模型返回最终结果 | Pi Codemode、OpenAI PTC |
| **脚本执行环境** | 放在高权限主进程（不安全）vs 放在底层系统（缺接口）vs 独立沙箱 | 放在受控的轻量沙箱（能调内部工具，无系统破坏权限） | Pi JS/WASM、OpenAI 托管 V8 |
| **任务进度管理** | 强制每步打卡写 Todo vs 依赖模型自主规划 | 撤除个人备忘清单（`TodoWrite`）；保留团队协作看板（`Tasks`） | Claude Code |
| **多 Agent 状态存储** | 依托本地文件系统 vs 依赖云端平台会话原语 | 本地 CLI 偏好文件系统；云端平台偏好托管会话 | Claude Code vs OpenAI Agent Server |
| **框架生态路线** | 保持模型中立与开放协议 vs 使用云厂商全家桶 | 中立框架靠标准协议（MCP）维持开放；厂商主打全托管一体化 | Pi vs OpenAI Agents SDK |
| **云端执行宿主解耦** | 将 Harness 整体放进虚拟机沙箱导致容量绑定与恢复断裂 vs 解耦运行时 | 运行时只做无状态状态机推演，沙箱降级为按需外部资源，通过预写日志保证崩溃恢复 | Tetral（见 [[wiki/syntheses/ai/cloud-agent-runtime-scaling\|云端 Agent 的规模化架构]]） |

## 取舍一：工具组合——直接经由上下文传递还是代码沙箱批量执行

**传统做法（通过上下文单步传递）**：
框架把可用工具列表提供给模型，模型每调一次工具，框架就把完整的返回数据（哪怕有几万字 JSON）全部放进对话上下文。模型读完之后，再由模型决策发起下一次调用。
* **痛点**：大量中间数据占据上下文窗口，且每次调用都需要经过一次完整的模型推理与网络往返。更关键的是，模型无法直接写循环或并发逻辑来批量处理数据。
* 多数 MCP 工具最初也是按这种习惯设计的：把数据格式化为文本传回上下文，由模型在对话中筛选。

**进阶做法（代码沙箱 / 程序化工具调用）**：
让模型不再在对话中逐个接收原始数据，而是编写一段轻量脚本（如 JavaScript/Python），交给内置沙箱运行。脚本在后台并发调用多个工具，完成循环、过滤与聚合，仅将计算好的最终结果返回给上下文。
* **典型案例**：Pi 的 Codemode 与 OpenAI 的 Programmatic Tool Calling（参见 [[openai-programmatic-tool-calling]]）。
* **Codemode 与 MCP 的关系**：两者并不是替代关系。MCP 负责提供现成的外部接口能力（如读取 GitHub、Linear 的数据），而沙箱负责提供批量组合与并发调用的能力。例如需要检查 100 个 issue 时，沙箱开并发直接拉取并统计完毕，只给模型回传一行汇总报告，彻底解放上下文。

**适用边界**：对于最终代码写入、核心决策确认、权限审批等高影响操作，依然需要走模型直接确认与调用；只有中间查询、过滤与数据汇总才适合交给脚本沙箱。

## 取舍二：脚本沙箱放在哪——安全与功能的平衡

既然允许模型写脚本在沙箱里组合调用工具，这个沙箱应该部署在哪里？框架面临着权限隔离的三层划分：

| 层次 | 所在环境 | 权限与安全性 | 典型功能 |
| --- | --- | --- | --- |
| **Agent 主循环** | Harness 宿主进程 | **完全受信**：持有用户完整环境、敏感密钥与主状态 | 对话请求、模型路由、持久化存储 |
| **组合沙箱** | Harness 内部轻量隔离环境 | **受控执行**：只能调用框架开放的安全工具，无法越权搞破坏 | Pi Codemode（JS/WASM）、OpenAI PTC（托管 V8） |
| **外部工具执行** | 底层独立环境 / 容器 | **默认不可信**：防止执行恶意系统命令或污染环境 | 本地 Bash 终端、外部 MCP 服务进程 |

如果直接在主循环里 `eval` 模型写的脚本，模型写错命令（如误删文件）会威胁宿主安全；如果把脚本直接扔到底层 Bash 容器里，它又无法直接调用 Harness 的内置接口。因此，Pi 与 OpenAI 都不约而同选择了**受限沙箱**方案：用隔离的轻量引擎（如 V8/WASM）运行脚本，既能安全编排所有已注册工具，又不会对宿主系统造成破坏。

## 取舍三：任务进度管理——从强制列 Todo 到依赖模型自主规划

在 Agent 演进过程中，框架给模型配置的任务记录工具发生了清晰分化：

### 1. 撤除个人备忘清单（`TodoWrite` 退役）
在早期模型（如 Claude 3 时代），由于模型长程记忆和规划能力较弱，容易做着做着就忘掉后续步骤。框架通常会注入 `TodoWrite` 工具，强制模型每一步都打卡更新清单。
* **代价**：随着新模型（如 Opus 4.5、Sonnet 5）自身规划能力的大幅提升，这种强制打卡变成了负担——每次更新都会增加一次网络往返延迟，消耗上千 token，还会分散模型的思考精力。
* **现状**：Claude Code 在较新的模型上默认关闭了 `TodoWrite` 工具（仅对老模型保留），直接交给模型在内部自主规划，让模型干活更快、更少分心。

### 2. 保留并强化团队协作看板（`Tasks` 系统）
撤除单 Agent 的个人 Todo 并不意味着任务系统没有价值，而是把职责切分得更清楚：

| 特性 | 个人备忘清单（`TodoWrite`） | 团队协作任务系统（`Tasks`） |
| --- | --- | --- |
| **解决的问题** | 弥补弱模型自己的记忆力和注意力不足 | 解决多个 Agent、主从进程或人与 Agent 之间的状态同步 |
| **操作方式** | 每次调用必须重写全量数组，只在当前会话可见 | 按 Task ID 增量更新，包含依赖关系（Blocker）与状态生命周期 |
| **消费者** | 只有模型自己看 | 其它 Sub-agent、并行会话认领任务，人类实时查看任务进度 |
| **演进方向** | 随模型变聪明而退役（非必需） | 随多 Agent 并行协作的深入而持续强化（基础设施） |

**实践启示**：在为 Agent 框架设计功能时，必须分清哪些工具只是帮弱模型记事的临时辅助（随着模型升级应及时撤除），哪些是真正的多实体协作基础设施（需要长期保留和沉淀）。

## 取舍四：多 Agent 状态共享——本地文件系统还是云端平台会话

当多个 Agent 协作（如主 Agent 派发子 Agent）时，中间成果与任务进度存放在哪里？业界出现了两条鲜明路线：

1. **本地文件系统路线（Claude Code 等工具）**：
   * 把任务元数据、协作清单直接保存在本地磁盘的文件目录中。
   * **优势**：极度简洁透明，人和 Git 都能直接查看和编辑，不依赖外部后端服务，多会话通过统一的环境变量（如 `CLAUDE_CODE_TASK_LIST_ID`）直接挂载同一组文件。
2. **云端托管会话路线（OpenAI Agent Server 等）**：
   * 将多 Agent 状态、检查点与运行历史保存在云端统一的 Sessions 服务中。
   * **优势**：长任务随时可以在后台挂起，数天后随时跨设备恢复继续执行；中间数据自带审计与回放能力，但与厂商的云服务深度绑定。

这两条路线分别代表了“本地优先/开发者自控”与“全托管云平台”的不同取向，短期内将长期并存。

## 取舍六：云端多租户执行——沙箱绑定还是运行时解耦

在将 Harness 迁移至云端多租户架构时，业界出现了两种截然不同的宿主设计：

1. **沙箱即 Agent 模式（早期云端 Agent）**：
   * 将包含模型交互、Prompt 装配与工具调用的完整 Agent 循环直接打包运行在虚拟机沙箱（如 E2B）内部。
   * **代价**：沙箱的创建和销毁属于重型、高频操作，极易导致编排系统调度出现瓶颈；且会话状态受困于沙箱生命周期，节点宕机时上下文完全丢失，排障还必须直接接触包含用户私有数据的沙箱。同时，为发起推理请求，API 凭据不得不直接注入到非受信的沙箱内部。
2. **运行时与沙箱解耦模式（如 Tetral）**：
   * 把 Harness 拆分为两部分：负责纯状态机推演与请求装配的「无状态运行时（Runtime）」，以及提供操作系统执行环境的「外部沙箱服务（Sandbox Service）」。
   * **机制**：计算机成为 Agent 调用的外部资源，而非运行宿主；运行时不持有任何数据库事务和外部调用，所有推进和工具调用在发出前必须通过预写日志（WAL）提交到独立的事务服务（Bridge）与事实存储（PostgreSQL）；凭据则由独立的模型网关在代理请求时动态注入。
   * **收益**：沙箱按需延迟分配，不再与会话生命周期强绑定；运行时成为随时可替换的轻量计算节点，崩溃后替补节点可依据提交的事件流精准恢复上下文继续执行。详细分析见 [[wiki/syntheses/ai/cloud-agent-runtime-scaling|云端 Agent 的规模化架构：把 runtime 移出沙箱]]。

## 取舍七：中立 Harness 还是厂商一体化全家桶

Harness 的最初价值在于通过适配层（Translation Layer）赋予用户选择权——可以自由切换 Claude、OpenAI、DeepSeek 等各类模型，保持本地工作流的独立性。

但随着云厂商（如 OpenAI Agent Server、Codex CLI）把 Harness、沙箱和多 Agent 会话统统打包成一体化云端产品，用户在获得极佳开箱体验的同时，也面临着生态锁定的风险。
像 Pi 等中立框架的应对策略是**拥抱并推动开放协议（如 MCP）**：通过打通标准工具协议，让中立 Harness 既能对接庞大的开源生态，又能保留灵活更换底层模型的核心自由。

## 实践启发

1. **避免在上下文里逐条拼装数据**：需要批量查询或处理大量数据时，优先提供代码沙箱让脚本在内部完成过滤与计算，只把处理后的最终结果返给模型上下文。
2. **警惕过度辅助变成性能累赘**：为模型增加辅助机制（如打卡清单、强制格式）时，要想清楚它到底是在帮模型还是在束缚模型；模型能力提升后，及时评估并清理过时的辅助开销。
3. **协作状态优先复用简单载体**：如果是本地运行的多 Agent 任务，使用本地文件系统或任务状态文件作为协作媒介最易维护，无需过早引入复杂的中心化通信协议。
4. **守住工作流的控制权**：根据业务需要明确边界——需要极致开箱体验的使用平台全托管能力，需要随时切换模型和保证数据隐私的核心链路，保留在中立 Harness 架构中。

## 时间线

| 时间 | 事件 | 来源与背景 |
| --- | --- | --- |
| 2026-02-08 | Claude Code 用 Tasks 替换 TodoWrite、用 Skills 替换 Slash Commands | 模型自主能力提升后撤除多余的单兵辅助工具（Tony Lee 转述官方说明） |
| 2026-04-15 | OpenAI 宣布 Agents SDK 演进为 Agent Server，引入托管 Harness/Sandbox/Sessions | 厂商发力平台一体化，将运行时标准化为云端基础设施 |
| 2026-09-06 | Tetral 提出把 runtime 移出沙箱架构 | 将计算机降级为按需外部资源，采用预写日志保障无状态运行时的高频替换与容灾 |
| 2026-09-29 | Pi 框架把 MCP 接入核心，并推出 Codemode 沙箱 | 探索中立框架下通过受限代码沙箱安全编排标准协议工具 |

## 相关页面

- [[wiki/topics/ai/agent-harness|Agent Harness]]
- [[wiki/syntheses/ai/cloud-agent-runtime-scaling|云端 Agent 的规模化架构：把 runtime 移出沙箱]]
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
- `raw/sources/2026-10-01-claude-code-task-tools-docs.md` / [Track todos — Claude Code 官方文档](https://code.claude.com/docs/en/agent-sdk/todo-tracking)、[Tools reference](https://code.claude.com/docs/en/tools-reference)、[CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- `raw/sources/2026-10-02-the-next-scaling-problem.md` / [The Next Scaling Problem — Tetral，2026-09-06](https://tetral.ai/blog/the-next-scaling-problem/)
