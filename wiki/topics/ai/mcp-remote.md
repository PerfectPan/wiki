---
title: mcp-remote
type: topic
category: ai
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - mcp
  - remote
  - proxy
  - oauth
source_refs:
  - https://www.npmjs.com/package/mcp-remote
---
# mcp-remote

## 摘要

`mcp-remote` 是一个把远端 MCP Server 代理成本地 stdio MCP Server 的桥接工具，适合那些原本只支持 stdio server 的 MCP 客户端。

## 关键点

- 它本质上是在本地起一个 stdio server，再和远端 server 之间建立另一层远程通信，把请求转发过去。
- 这种桥接方案的意义不是重新定义 MCP，而是把“客户端只会 stdio”这一现实限制兼容掉。
- 另一个实际价值是：它可以同时兼容认证场景，因此不只是简单的协议转码，而是把“远端可访问 + 本地可消费”这条链打通。

## 相关页面

- [[MCP]]
- [[OAuth]]

## 来源指针

- [mcp-remote](https://www.npmjs.com/package/mcp-remote)
