---
title: Responses API
description: OpenAI 新一代 agent 向协议：response 对象、output item 列表、previous_response_id 与托管工具。
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
  - agent
  - codex
source_refs:
  - raw/sources/2026-08-03-llm-101-conversation.md
resource:
  - raw/sources/2026-08-03-llm-101-conversation.md
---
# Responses API

## 摘要

Responses API 是 OpenAI 面向 agent 产品线的主协议之一：一次调用对应一个带生命周期的 `response` 对象，输出是异构 `output[]` item，而不是单条 `message` 上堆字段。它不改变「本地执行工具」的基本分工，但让多类型块、续聊和托管工具更标准化。

## 关键点

- 典型端点：`POST /v1/responses`。
- 返回是 **Response 资源**：有 `id`、`status`（如 completed / requires_action / in_progress），不是只有 `choices[0].message`。
- **`output[]` 多类型 item**（协议核心）：
  - `message`：给用户看的话
  - `reasoning`：思考块（一等类型）
  - `function_call` / `function_call_output`：工具调用与结果
  - 以及 web_search、code_interpreter 等 **内置/托管工具** 相关 item
- **`previous_response_id`**：服务端会话指针，可少传全量历史（客户端仍可选择自带上下文）。
- 输入侧常用 `input`（字符串或 input item 数组）+ 顶层 `instructions`，形状不同于纯 `messages[]`。
- 流式更偏 **item 事件**（块开始/增量/结束），而不是只往一个 `delta.content` 里挤所有类型。
- **工具默认仍在客户端执行**（读盘、改仓库、跑命令）。托管工具只覆盖平台提供的那一类；coding agent 的本地副作用不因此上云。
- 「多步」指协议能清晰描述一轮任务中的多种步骤块，以及跨 turn 续跑；**不是**「以前只能一步、现在才能 agent」。Completions 时代客户端 while + 多 `tool_calls` 已经能多步。
- 产品动机：统一 agent 能力、对齐 Codex/ChatGPT 新链路、减少私有字段补丁；对终端用户写代码体感往往接近零。
- 其它厂支持情况：OpenAI 原生；DeepSeek V4-Flash 等强调兼容以便接 Codex；多数模型厂仍以 Completions 为主。

## 相关页面

- [[Chat Completions]]
- [[Anthropic Messages API]]
- [[LLM API 协议选型]]
- [[Code Agent]]
- [[大模型 101]]

## 来源指针

- `raw/sources/2026-08-03-llm-101-conversation.md`
