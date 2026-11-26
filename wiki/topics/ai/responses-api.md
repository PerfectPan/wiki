---
title: Responses API
description: OpenAI Responses API 的输出条目、工具回传、会话续接，以及请求级指令和历史消息的区别。
type: topic
category: ai
created: 2026-08-03
updated: 2026-11-18
timestamp: 2026-11-18
tags:
  - llm
  - api
  - openai
  - agent
  - codex
source_refs:
  - raw/sources/2026-08-03-llm-101-conversation.md
  - https://developers.openai.com/api/reference/resources/responses/methods/create
  - https://developers.openai.com/api/docs/guides/latest-model
---
# Responses API

## 摘要

Responses API 是 OpenAI 面向 agent 产品线的主协议之一：一次调用对应一个带生命周期的 `response` 对象，输出是异构 `output[]` item，而不是单条 `message` 上堆字段。它不改变「本地执行工具」的基本分工，但让多类型块、续聊和托管工具更标准化。

## 关键点

- 典型端点：`POST /v1/responses`。
- 返回是 **Response 资源**，有 `id`、`status`（例如 `completed`、`in_progress`、`incomplete`）及输出条目。
- **`output[]` 多类型 item**（协议核心）：
  - `message`：给用户看的话
  - `reasoning`：思考块（一等类型）
  - `function_call` / `function_call_output`：工具调用与结果
  - 以及 web_search、code_interpreter 等 **内置/托管工具** 相关 item
- **`previous_response_id`**：指向上一条 Response，由服务端续接其上下文。客户端也可以按顺序重传所需的历史条目。
- 输入侧常用 `input`（字符串或 input item 数组）+ 顶层 `instructions`，形状不同于纯 `messages[]`。
- 流式更偏 **item 事件**（块开始/增量/结束），而不是只往一个 `delta.content` 里挤所有类型。
- **工具默认仍在客户端执行**（读盘、改仓库、跑命令）。托管工具只覆盖平台提供的那一类；coding agent 的本地副作用不因此上云。
- 「多步」指协议能清晰描述一轮任务中的多种步骤块，以及跨 turn 续跑；**不是**「以前只能一步、现在才能 agent」。Completions 时代客户端 while + 多 `tool_calls` 已经能多步。
- 产品动机：统一 agent 能力、对齐 Codex/ChatGPT 新链路、减少私有字段补丁；对终端用户写代码体感往往接近零。
- 其它厂支持情况：OpenAI 原生；DeepSeek V4-Flash 等强调兼容以便接 Codex；多数模型厂仍以 Completions 为主。

## 请求级指令与会话历史

顶层 `instructions` 是 `POST /v1/responses` 的可选字段，API 将它作为一条 system 或 developer 指令插入本次模型上下文。同一个会话的不同请求可以各自提供、替换或省略这个字段。用 `previous_response_id` 续接时，上一份请求的顶层 `instructions` 不会自动传下去。需要跨请求持续生效的规则可作为 `input` 中的 `developer` 消息保存到历史。[Responses 接口定义](https://developers.openai.com/api/reference/resources/responses/methods/create)

例如，第一份请求要求查询订单，只在本次生成中要求模型先调用工具：

```json
{
  "model": "gpt-6.2-astra",
  "input": "订单 A123 发货了吗？",
  "instructions": "先调用 get_order_status 查询订单。",
  "tools": [
    {
      "type": "function",
      "name": "get_order_status",
      "description": "按订单号查询发货状态",
      "parameters": {
        "type": "object",
        "properties": { "order_id": { "type": "string" } },
        "required": ["order_id"],
        "additionalProperties": false
      }
    }
  ]
}
```

应用执行返回的 `function_call`，取第一份响应的 `id` 和工具调用的 `call_id` 发下一份请求。下面的 ID 是示例：

```json
{
  "model": "gpt-6.2-astra",
  "previous_response_id": "resp_example",
  "input": [
    {
      "type": "function_call_output",
      "call_id": "call_example",
      "output": "{\"status\":\"shipped\"}"
    }
  ],
  "instructions": "用一句话向用户说明查询结果。"
}
```

用户只问了一次，应用发了两次模型请求。第二次仍读到原来的问题和工具调用，顶层指令是这次传入的「用一句话向用户说明查询结果」。平台在同一次请求内执行的托管工具继续使用该请求的指令。历史输入仍计入用量，命中的部分按缓存读取价计费。[函数调用](https://developers.openai.com/api/docs/guides/function-calling) · [会话状态](https://developers.openai.com/api/docs/guides/conversation-state)

GPT‑6.2 把顶层 `instructions` 放到整个 `input` 之后。更换临时指令时，之前的历史仍有机会命中缓存。这条临时指令本身按普通输入计费。固定规则放在 `input` 开头的 `developer` 消息里，才可以跟随稳定前缀一起缓存。位置与续接规则分别由接口定义，具体的缓存匹配和费用见 [[kv-cache-vs-request-cache]]。[提示缓存的前缀匹配](https://developers.openai.com/api/docs/guides/prompt-caching#how-prefix-matching-works)

## 相关页面

- [[chat-completions]]
- [[anthropic-messages-api]]
- [[chat-completions-vs-messages-vs-responses]]
- [[code-agent]]
- [[llm-101]]
- [[agent-execution-terms]]
