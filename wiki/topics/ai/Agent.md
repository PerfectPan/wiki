---
title: Agent
type: topic
category: ai
status: active
created: 2026-04-12
updated: 2026-04-25
tags:
  - agent
  - coding-agent
  - agent-framework
source_refs:
  - raw/sources/Agent.md
  - https://github.com/Aider-AI/aider
  - https://github.com/agno-agi/agno
---
# Agent

## 摘要

Agent 指的是能基于当前上下文自主决定下一步动作，并通过工具调用或环境反馈继续推进任务的执行体。

## 关键点

- 和普通问答式 AI 相比，agent 的区别不在于“模型更强”，而在于它会把观察、决策、执行、再观察串成循环。
- 2024-12-24 的一条观察里把一个关键边界说得很清楚：如果流程本身已经能被人稳定写出来，那更接近 workflow；只有当下一步依赖模型持续判断时，才更像 agent。
- 工程上常见的 agent 既可以是通用执行体，也可以是更窄的 [[Code Agent]]。
- 现有记录里的两个入口分别代表不同层级：
  - `aider` 更像直接可用的 coding agent；
  - `agno` 更像搭 agent 的框架层。

## 相关页面

- [[Code Agent]]
- [[Workflow vs Agent]]
- [[Agent Client Protocol]]

## 来源指针

- `raw/sources/Agent.md`
- https://github.com/Aider-AI/aider
- https://github.com/agno-agi/agno
