---
title: Agent Harness
description: Agent harness 是为 AI 模型提供运行环境的软件层，由 system prompt、tools、agentic loop 和 translation layer 四个组件构成，是用户保留自主权和模型选择权的关键。
type: topic
category: ai
created: 2026-08-20
updated: 2026-08-20
timestamp: 2026-08-20
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

代表性的开源 harness 包括 Pi、OpenClaw、OpenCode、Hermes 等。

## 相关页面

- [[Agent]]
- [[Code Agent]]
- [[wiki/syntheses/ai/Agent Harness 演进范式|Agent Harness 演进范式]]
- [[wiki/syntheses/ai/Agent 团队的角色分工与协作模式|Agent 团队的角色分工与协作模式]]

## 来源指针

- `raw/sources/2026-08-20-what-is-a-harness.md`
- https://earendil.com/posts/what-is-a-harness/
