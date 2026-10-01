---
title: Agent Harness
description: Agent harness 是为 AI 模型提供运行环境的软件层，由 system prompt、tools、agentic loop 和 translation layer 四个组件构成，是用户保留自主权和模型选择权的关键。
type: topic
category: ai
created: 2026-08-20
updated: 2026-10-01
timestamp: 2026-10-01
tags:
  - agent
  - harness
  - agent-framework
source_refs:
  - raw/sources/2026-08-20-what-is-a-harness.md
  - https://earendil.com/posts/what-is-a-harness/
resource:
  - raw/sources/2026-08-20-what-is-a-harness.md
  - https://earendil.com/posts/what-is-a-harness/
---

# Agent Harness

## 摘要

Agent harness 是包裹在 AI 模型外层的运行环境软件。常用公式是 **Agent = Model + Harness**。和模型不同，harness 可以被用户拥有、修改和定制，因此是用户保留自主权和模型选择权的关键。

## 关键点

### 1. 类比：攀岩安全带

攀岩安全带的作用是：支撑和保护使用者、挂载工具、可适配不同地形。Agent harness 同理——它为模型提供运行环境、暴露工具、并可被用户定制。

### 2. 四个核心组件

| 组件 | 作用 |
| --- | --- |
| **System Prompt** | 模型的行为指令，类似新员工入职指南。随每次请求注入上下文。 |
| **Tools** | 模型可调用的能力（搜索、写代码、发邮件等）。Harness 只提供工具，不强制何时使用，由模型自主决定。 |
| **Agentic Loop** | 模型自主评估结果、决定是否继续调用工具的循环。这是 agent 和普通问答的核心区别。 |
| **Translation Layer** | 适配不同模型（Anthropic / OpenAI / 开源）的抽象层，让同一个 harness 可以切换底层模型。 |

### 3. 和模型的区别

- **模型**：训练得到的权重，用户无法修改，数据存在厂商服务器上。
- **Harness**：用户可以拥有、运行在本地、修改 system prompt、添加工具、切换模型。

### 4. 为什么 Harness 重要

Harness 是用户自主权的载体：

- **模型可替换**：通过 translation layer，可以在 Anthropic、OpenAI、开源模型之间切换，不被单一厂商锁定。
- **数据本地化**：会话数据留在本地，而不是存在 AI 实验室的服务器上。
- **可定制**：用户可以修改 system prompt、设计工作流、添加扩展。

代表性的开源 harness 包括 Pi、Claude Code、OpenCode、Codex、Hermes 等。

### 5. 当前的设计取舍

随着底层模型规划与执行能力的提升，Harness 的演化重点正在从「管理单步执行」转向「支撑多任务协同」：
- **精简单步干预**：早期为了防止模型遗忘步骤而设计的单步记录工具（如强制更新 `TodoWrite` 任务列表），随着新模型长程规划能力的增强而逐步停用；框架转而专注于提供支持多 Agent 协同和依赖关系的任务系统。
- **由代码完成中间数据处理**：组合调用多个工具时，不再把每次调用的完整原始数据都注入模型上下文，而是让模型生成一段脚本在沙箱中批量执行过滤与聚合，仅将最终结果返回给上下文。
- **状态存储与生态分化**：多 Agent 协作状态是依托本地文件系统还是云端托管会话，以及选用跨模型的中立 Harness 还是云厂商全家桶，正在成为两条平行的工程路线。

具体维度的案例与技术细节见 [[agent-harness-design-tradeoffs]]。

### 6. 与上层编排平台的边界

Harness 负责**单个 Agent** 的运行循环。像 QM、Raft、Orca 这类产品属于更上层的 **Agent Orchestration Platform**，提供多租户、Scope 隔离、权限审批、多端接入、沙箱执行和多 Harness 路由等能力。详见 [[agent-orchestration-platform]]。

## 相关页面

- [[agent]]
- [[code-agent]]
- [[wiki/syntheses/ai/agent-harness-evolution-paradigm|Agent Harness 演进范式]]
- [[wiki/topics/ai/agent-harness-design-tradeoffs|Agent Harness 的设计取舍]]
- [[wiki/syntheses/ai/agent-team-roles-and-collaboration|Agent 团队的角色分工与协作模式]]

## 来源指针

- `raw/sources/2026-08-20-what-is-a-harness.md`
- https://earendil.com/posts/what-is-a-harness/
