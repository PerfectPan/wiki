---
title: Code Agent
type: topic
category: ai
status: active
created: 2026-04-12
updated: 2026-07-01
tags:
  - code-agent
  - agent
  - agents-md
  - workflow
  - tool-boundary
source_refs:
  - raw/sources/Code Agent.md
  - raw/sources/2026-05-31-vercel-ai-cli-research.md
  - raw/sources/2026-07-01-openseek-shell-git-policy.md
---
# Code Agent

## 摘要

Code agent 是把大语言模型放进真实工程工作流里的执行体：它不只是回答问题，而是要读仓库约束、规划改动、操作文件和命令，并在审阅边界内完成任务。

## 关键点

- `AGENTS.md` 这类仓库内指令文件的价值，不是补充一点风格说明，而是把 agent 的权限边界、输出语言、改动方式和 Git 流程变成机器可遵守的局部协议。
- code agent 和普通聊天式 AI 的差别，在于它需要同时处理代码语义、仓库治理和执行副作用，因此“先读规则再动手”是工作流的一部分，不只是礼貌。
- 2025-03-01 的一条经验是一个很实用的经验：AI 在改代码时容易顺手删注释、擅自重构。对 code agent 来说，这意味着需要更强的范围控制、最小 diff 和显式意图确认。
- 如果两边都定义了协议边界，code agent 的行为会更稳定。`AGENTS.md` 约束的是仓库侧行为，[[Agent Client Protocol]] 这类协议约束的是 editor / client 与 agent 之间如何协商能力。
- code agent 不只需要调用 SDK 或 MCP，也经常依赖 CLI 作为执行边界。稳定的 agent-native CLI 应该把文件产物、JSON metadata、stdout/stderr 分离、并发控制和失败语义做成明确协议，而不是让 agent 从自然语言输出里猜结果。参见 [[Agent-native 生成型 CLI 的产物协议]]。
- 大仓里的结构约定也应尽量机器可验证。像 `konsistent` 这类结构 linter 可以把 provider、adapter、plugin、harness 等重复结构的文件、导出、导入和继承约束变成 CI 检查，降低 agent 只凭样例模仿时的漂移。参见 [[Code Agent 结构约定的可验证边界]]。
- shell 和 Git 不是单纯“开或关”的能力。更稳的做法是把源文件修改权收敛到结构化编辑工具，把 shell 定位为分析和验证通道，并对 Git 这类会写源文件的 CLI 按写入来源、可恢复性和重配置风险分类。参见 [[Coding Agent Shell 与 Git 权限边界]]。
- OpenSeek 这类项目说明，code agent 的可靠性不只取决于模型，还取决于 session event log、runtime steering、typed tool protocol 和 eval harness 是否形成闭环。参见 [[OpenSeek 项目架构总览]]。

## 典型约束

- 语言和写作策略：对话语言、工程文档语言、代码注释语言可能分别被约束。
- 变更安全：是否允许自动提交、是否需要先确认、是否只能做最小 diff。
- Git / PR 规则：是否允许直接 push、PR 描述格式、是否必须走 branch + PR。
- 命令执行边界：是否偏好非交互命令、是否要求 timeout、是否禁止危险命令。

## 相关页面

- [[Agent]]
- [[Agent Client Protocol]]
- [[Code Agent 结构约定的可验证边界]]
- [[Agent-native 生成型 CLI 的产物协议]]
- [[OpenSeek 项目架构总览]]
- [[Coding Agent Shell 与 Git 权限边界]]
- [[Workflow vs Agent]]

## 来源指针

- `raw/sources/Code Agent.md`
- `raw/sources/2026-05-31-vercel-ai-cli-research.md`
- `raw/sources/2026-07-01-openseek-shell-git-policy.md`
