---
title: Anthropic Messages API
description: Claude 原生 /v1/messages：独立 system、content 类型块、tool_use/tool_result，以及与 OpenAI Chat 的字段差异。
type: topic
category: ai
status: seed
created: 2026-08-03
updated: 2026-08-03
timestamp: 2026-08-03
tags:
  - llm
  - api
  - anthropic
  - claude
  - tool-calling
source_refs:
  - raw/sources/2026-08-03-llm-101-conversation.md
resource:
  - raw/sources/2026-08-03-llm-101-conversation.md
---
# Anthropic Messages API

## 摘要

Anthropic Messages 是 Claude 官方对话与工具协议。思想仍是「messages + 客户端跑工具」，但 JSON 形状、鉴权头、工具结果角色和 thinking 表达与 OpenAI Chat Completions 不通用。

## 关键点

- 典型端点：`POST /v1/messages`；头需要 `x-api-key` 与 `anthropic-version`（Bearer 体系不兼容）。
- **`system` 在顶层**，一般不放进 `messages[].role = system`。
- `messages` 角色主要是 **user / assistant**；几乎总是 **`content` 块数组**，而不是纯字符串。
- 工具定义字段更接近：`name` + `input_schema`（而非 OpenAI 的 `function.parameters` 包一层）。
- 模型调工具：assistant `content` 里出现 `type: "tool_use"` 块；`stop_reason` 常为 `tool_use`。
- 回传工具结果：**user 消息**里放 `type: "tool_result"`，用 `tool_use_id` 关联——**没有** OpenAI 的 `role: "tool"`。
- Thinking 在 Messages 体系里更一等：请求侧 thinking 参数，响应侧 `thinking` 内容块。
- 流式事件模型不同：`content_block_start` / `delta` / `stop` 等，与 OpenAI SSE 形状不通用。
- Claude Code 默认走 Messages 语义；因此 z.ai Coding Plan、DeepSeek 等会提供 **`/anthropic` 兼容端点**，让 CC 只改 base_url/key 即可。

## 与 Chat Completions 对照（工具一轮）

| 步骤 | Chat Completions | Anthropic Messages |
| --- | --- | --- |
| 模型要调工具 | `message.tool_calls[]` | `content[]` 中 `tool_use` |
| 你返回结果 | `role: tool` | `role: user` + `tool_result` |
| 系统提示 | 常在 messages 内 | 顶层 `system` |
| 停因字段 | `finish_reason` | `stop_reason` |

## 相关页面

- [[Chat Completions]]
- [[Responses API]]
- [[LLM API 协议选型]]
- [[Code Agent]]
- [[大模型 101]]

## 来源指针

- `raw/sources/2026-08-03-llm-101-conversation.md`
