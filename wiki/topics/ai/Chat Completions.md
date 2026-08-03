---
title: Chat Completions
description: OpenAI 风格的 /v1/chat/completions：messages 对话、tool_calls，以及作为事实标准的兼容生态。
type: topic
category: ai
status: seed
created: 2026-08-03
updated: 2026-08-03
timestamp: 2026-08-03
tags:
  - llm
  - api
  - openai
  - tool-calling
source_refs:
  - raw/sources/2026-08-03-llm-101-conversation.md
resource:
  - raw/sources/2026-08-03-llm-101-conversation.md
---
# Chat Completions

## 摘要

Chat Completions 是目前最通用的 LLM HTTP 协议形态：用 `messages` 表达对话，用 `tools` / `tool_calls` 表达函数调用。多数第三方模型与 OpenCode、Cline 一类客户端默认兼容这一套。

## 关键点

- 典型端点：`POST /v1/chat/completions`。
- 请求核心：`model`、`messages[]`、`tools`、`tool_choice`、流式 `stream`。
- 系统提示常见两种写法：`messages` 里 `role: system`，或网关映射到其它字段。
- 助手一轮回复挂在一条 assistant message 上：
  - 正文：`content`（string 或 multimodal parts）
  - 工具：`tool_calls[]`（可并行多个）
- 工具结果：另开 `role: "tool"`（或兼容实现的等价角色），带 `tool_call_id`。
- **多步 agent 不是协议替你跑完**，而是客户端 `while` 循环：调 API → 本地执行工具 → 把结果写回 messages → 再调 API。
- 思考 / reasoning 在 Completions 时代多为私有字段或标签（如 `reasoning_content`、`<think>`），没有统一 item 类型。
- 生态地位：DeepSeek、Kimi、GLM、Groq 等「OpenAI 兼容」通常首先兼容的是 Completions。

## 相关页面

- [[Responses API]]
- [[Anthropic Messages API]]
- [[LLM API 协议选型]]
- [[Code Agent]]
- [[大模型 101]]

## 来源指针

- `raw/sources/2026-08-03-llm-101-conversation.md`
