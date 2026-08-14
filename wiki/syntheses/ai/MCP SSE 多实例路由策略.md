---
title: MCP SSE 多实例路由策略
description: 旧版有状态 MCP SSE 在多实例部署中的路由问题，以及 2026-07-28 无状态核心如何消除协议级 session
type: synthesis
category: ai
created: 2026-04-25
updated: 2026-07-29
timestamp: 2026-07-29
tags:
  - mcp
  - sse
  - gateway
  - routing
  - distributed-system
source_refs:
  - wiki/topics/ai/MCP.md
  - https://modelcontextprotocol.io/specification/2026-07-28
  - https://blog.modelcontextprotocol.io/posts/2026-07-28/
resource:
  - wiki/topics/ai/MCP.md
  - https://modelcontextprotocol.io/specification/2026-07-28
  - https://blog.modelcontextprotocol.io/posts/2026-07-28/
---
# MCP SSE 多实例路由策略

## 问题

当 MCP 使用 SSE transport，而且服务端是多实例部署时，为什么会出现路由和连接归属问题？通常有哪些解决思路？

## 简答

在 2026-07-28 之前，因为 SSE 长连接和后续 HTTP 消息未必会命中同一个实例，而 MCP SSE transport 又带有协议会话状态，多实例部署必须保证后续请求回到持有 session 的实例，或把映射状态外置。2026-07-28 规范移除了握手、`Mcp-Session-Id` 和协议级 session，使任意请求可以落到任意实例；旧方案因此主要保留为迁移背景。

## 综合结论

- 这个问题可以拆成两层：MCP 的 SSE transport 不是简单“一条 SSE 把所有东西都收完”，而是长连接负责接收，后续发送往往仍走 HTTP 请求。
- 一旦服务端是多实例，两个问题马上出现：
  - 建立 SSE 长连接的实例，未必是后续 POST 请求命中的实例；
  - 某个实例重启、扩缩容或下线时，会话状态如何接管。
- 这类问题本质上是在处理“有状态连接如何在分布式环境里被定位和续接”。
- 这里可以落成两类稳定思路：
  - 方式 1：尽量让实例无状态，或者让客户端自行和更多实例建立可恢复连接；
  - 方式 2：把 session -> instance 的映射状态中心化存储，再由网关或代理层把请求转发给正确实例。
- 以文中记录的 Higress 思路为例，就是把 session 关系放到中心化位置，再在发现目标 session 不在本机时转发到对应实例。
- 进一步的工程化结论是：如果 SSE 本身承担了大量长连接，最好把它从普通业务网关里拆出来，形成更稳定、变化更少的一层协议网关，减少每次业务发布带来的大面积重连。

## 2026-07-28 后的结论

- 新版 MCP 的默认路线不再是维护 session -> instance 映射，而是让每个请求自描述、独立路由。
- 服务端若确实需要跨调用状态，应显式返回业务 handle，并要求后续工具调用把 handle 作为参数带回；不要把状态隐藏在 transport session 中。
- 中途确认、补参数和 server-to-client 交互由 MRTR 承载：服务端返回 `input_required`，客户端收集输入后重试原调用，不需要一直占用双向流。
- 长任务状态进入 Tasks 扩展，通过持久句柄和轮询管理；它与协议核心的无状态性不冲突。
- 旧 HTTP + SSE transport 已弃用但有至少 12 个月兼容期。迁移期内仍运行旧 server 时，本页记录的 sticky routing、中心化映射和连接层隔离仍然适用。

## 未决问题

- 现有 server 中有多少把业务状态错误地绑定在 `Mcp-Session-Id` 上，仍需通过真实迁移案例验证。
- MRTR、Tasks 和显式 handle 在失败恢复、幂等和超时语义上的最佳实践仍会继续演化。

## 来源指针

- `wiki/topics/ai/MCP.md`
- <https://modelcontextprotocol.io/specification/2026-07-28>
- <https://blog.modelcontextprotocol.io/posts/2026-07-28/>
