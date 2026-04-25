---
title: MCP Client
type: topic
category: ai
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - mcp
  - client
  - tool-calling
  - xml
source_refs:
  - wiki/topics/ai/MCP.md
---
# MCP Client

## 摘要

MCP Client 是把模型输出接到工具执行链路上的一侧实现。它的职责不是“理解 MCP 是什么”，而是把模型意图解析成可执行的 tool 调用，再把执行结果喂回模型。

## 关键点

- 2025-03-29 的一条经验是一个很直接的实现心智模型：MCP Client 可以被看成“包一层 LLM function call”的执行器。
- 如果底层模型本身支持 function calling，client 可以直接把工具声明和调用结果接到模型 API。
- 如果模型本身不支持 function calling，也可以让模型产出约定格式的结构化文本，再由 client 先行 parse 后执行。XML 风格的协议就是一种可行做法，思路和很多代码生成工具用的自定义标记语言类似。
- 因此 MCP Client 的关键不是某一种特定语法，而是三件事：
  - 模型输出必须可被稳定解析；
  - 工具调用需要有明确的执行边界；
  - 执行结果要能重新进入模型上下文，形成闭环。

## 相关页面

- [[MCP]]
- [[mcp-remote]]

## 来源指针

- `wiki/topics/ai/MCP.md`
