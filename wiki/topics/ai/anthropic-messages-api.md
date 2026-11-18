---
title: Anthropic Messages API
description: Claude Messages API 的顶层 system、会话中途系统消息、工具结果回传及当轮指令的作用范围。
type: topic
category: ai
created: 2026-08-03
updated: 2026-11-18
timestamp: 2026-11-18
tags:
  - llm
  - api
  - anthropic
  - claude
  - tool-calling
source_refs:
  - raw/sources/2026-08-03-llm-101-conversation.md
  - https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages
---
# Anthropic Messages API

## 摘要

Anthropic Messages 是 Claude 官方对话与工具协议。思想仍是「messages + 客户端跑工具」，但 JSON 形状、鉴权头、工具结果角色和 thinking 表达与 OpenAI Chat Completions 不通用。

## 关键点

- 典型端点：`POST /v1/messages`；头需要 `x-api-key` 与 `anthropic-version`（Bearer 体系不兼容）。
- **顶层 `system`** 放适用于整个会话的规则。支持的模型也接受 `messages` 中途插入的 `role: "system"` 消息。
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
| 系统提示 | 常在 messages 内 | 顶层 `system`，支持的模型也可在对话中追加 |
| 停因字段 | `finish_reason` | `stop_reason` |

## 中途追加与仅当轮生效的系统消息

Claude Opus 4.8 已支持在 `messages` 中途插入系统消息，后续模型的支持范围见官方列表。有内容的系统消息一般紧跟一条 `user` 消息，然后结束本次输入或接一条 `assistant` 消息。默认从插入点继续生效，后来的系统消息可以覆盖更早的规则。启用 `cache_control` 时，在断点之后追加消息会保留先前的缓存匹配资格。顶层 `system` 仍在会话开头，改它会让后续前缀失配。[中途系统消息与缓存](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages)

只在下一次生成中生效的提醒可用 `clear_at: "next_user_message"`，需要 `anthropic-beta: mid-conversation-system-clear-at-2026-08-21`。例如，应用先让 Claude 查订单，再把结果交回去：

```text
user       订单 A123 发货了吗？
system     先查订单，暂不回复用户。clear_at: next_user_message
assistant  tool_use: get_order_status
user       tool_result: 已发货
assistant  订单 A123 已发货。
```

回传结果的 `user` 消息会清除前面那条当轮指令，即使真人没有发新消息。应用重传历史时原样保留已清除的系统消息，API 从此不再把它呈现给模型，也不计它的输入 token。需要继续约束下一次生成时，在 `tool_result` 消息后追加新的当轮系统消息。服务端工具循环如果没有引入后续 `user` 消息，则不触发清除。[当轮系统消息](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages)

## 相关页面

- [[chat-completions]]
- [[responses-api]]
- [[chat-completions-vs-messages-vs-responses]]
- [[code-agent]]
- [[llm-101]]
- [[agent-execution-terms]]
