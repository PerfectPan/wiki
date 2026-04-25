---
title: Code Agent
type: topic
category: ai
status: active
created: 2026-04-12
updated: 2026-04-25
tags:
  - code-agent
  - agent
  - agents-md
  - workflow
source_refs:
  - raw/sources/Code Agent.md
---
# Code Agent

## 摘要

Code agent 是把大语言模型放进真实工程工作流里的执行体：它不只是回答问题，而是要读仓库约束、规划改动、操作文件和命令，并在审阅边界内完成任务。

## 关键点

- `AGENTS.md` 这类仓库内指令文件的价值，不是补充一点风格说明，而是把 agent 的权限边界、输出语言、改动方式和 Git 流程变成机器可遵守的局部协议。
- code agent 和普通聊天式 AI 的差别，在于它需要同时处理代码语义、仓库治理和执行副作用，因此“先读规则再动手”是工作流的一部分，不只是礼貌。
- 2025-03-01 的一条经验是一个很实用的经验：AI 在改代码时容易顺手删注释、擅自重构。对 code agent 来说，这意味着需要更强的范围控制、最小 diff 和显式意图确认。
- 如果两边都定义了协议边界，code agent 的行为会更稳定。`AGENTS.md` 约束的是仓库侧行为，[[Agent Client Protocol]] 这类协议约束的是 editor / client 与 agent 之间如何协商能力。

## 典型约束

- 语言和写作策略：对话语言、工程文档语言、代码注释语言可能分别被约束。
- 变更安全：是否允许自动提交、是否需要先确认、是否只能做最小 diff。
- Git / PR 规则：是否允许直接 push、PR 描述格式、是否必须走 branch + PR。
- 命令执行边界：是否偏好非交互命令、是否要求 timeout、是否禁止危险命令。

## 相关页面

- [[Agent]]
- [[Agent Client Protocol]]
- [[Workflow vs Agent]]

## 来源指针

- `raw/sources/Code Agent.md`
