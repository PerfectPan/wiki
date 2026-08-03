---
title: LLM API 协议选型
description: Chat Completions、Anthropic Messages、Responses 三种主流插头怎么选，以及和 Claude Code / Codex / OpenCode 的对应关系。
type: comparison
category: ai
status: seed
created: 2026-08-03
updated: 2026-08-03
timestamp: 2026-08-03
tags:
  - llm
  - api
  - openai
  - anthropic
  - agent
source_refs:
  - raw/sources/2026-08-03-llm-101-conversation.md
resource:
  - raw/sources/2026-08-03-llm-101-conversation.md
---
# LLM API 协议选型

## 决策问题

接模型或写 agent 时，该用 OpenAI Chat Completions、Anthropic Messages，还是 OpenAI Responses？

## 简短结论

- **默认选 Chat Completions**：生态最大，自己写调用或接 OpenCode/Cline 最省事。
- **跑 Claude Code / Claude 原生能力**：选 **Anthropic Messages**（或厂商标了 `/anthropic` 的兼容端点）。
- **接 Codex 新链路 / OpenAI 托管工具产品线**：才需要认真做 **Responses**。
- 三者都能做多步 tool loop；差别主要在 **JSON 形状、续聊、托管工具和官方产品对齐**，不是「会不会 agent」。

## 对比表

| 维度 | Chat Completions | Anthropic Messages | Responses |
| --- | --- | --- | --- |
| 谁主推 | OpenAI 兼容生态事实标准 | Anthropic / Claude | OpenAI agent / Codex 新线 |
| 对话容器 | `messages[]` | `messages[]` + 顶层 `system` | `input` + response 资源 |
| 多类型怎么放 | message 上挂 `content`/`tool_calls`/私有 reasoning | `content[]` 类型块 | `output[]` 异构 item |
| 工具结果角色 | `role: tool` | user + `tool_result` | function_call_output 等 item |
| 续聊 | 客户端重传全历史 | 客户端重传全历史 | 可 `previous_response_id` |
| 状态机 | 弱 | 弱（靠 stop_reason） | response `status` 一等 |
| 托管工具 | 弱/旁路 | 有限 | 主协议内更完整 |
| 本地 coding 工具 | 客户端执行 | 客户端执行 | 客户端执行（同） |

## 客户端默认插头

| 客户端 | 默认协议口味 |
| --- | --- |
| OpenCode / Cline / 多数 | Chat Completions |
| Claude Code | Anthropic Messages |
| Codex | 越来越 Responses（Completions 仍可能经适配） |

## 厂商侧常见策略

- **只做 Completions**：覆盖最广的第三方接入。
- **Completions + `/anthropic`**：同时伺候 OpenCode 与 Claude Code（GLM Coding Plan、DeepSeek 等）。
- **再补 Responses**：为了进 Codex / OpenAI 新示例，不是让终端用户手写代码突然变强。

## 不该有的预期

- 换 Responses ≠ 工具改由云端改你的仓库。
- 换 Responses ≠ 以前不能并行 tool call。
- 协议新 ≠ 模型更强；模型能力与价格要单独比。

## 相关页面

- [[Chat Completions]]
- [[Anthropic Messages API]]
- [[Responses API]]
- [[Code Agent]]
- [[大模型 101]]

## 来源指针

- `raw/sources/2026-08-03-llm-101-conversation.md`
