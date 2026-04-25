---
title: MCP SSE 多实例路由策略
type: synthesis
category: ai
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - mcp
  - sse
  - gateway
  - routing
  - distributed-system
source_refs:
  - wiki/topics/ai/MCP.md
---
# MCP SSE 多实例路由策略

## 问题

当 MCP 使用 SSE transport，而且服务端是多实例部署时，为什么会出现路由和连接归属问题？通常有哪些解决思路？

## 简答

因为 SSE 长连接和后续 HTTP 消息未必会命中同一个实例，而 MCP SSE transport 又天然带有会话状态。多实例下的核心问题不是“能不能用 SSE”，而是“后续请求如何稳定回到持有该 session 的实例”，或者干脆把这类状态从实例里拿掉。

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

## 未决问题

- 当前记录已经有了不错的系统设计结论，但还没有和现有开源 MCP server / gateway 的真实代码结构做更多交叉验证。
- 后续如果仓库继续积累 MCP 部署实践，可以把“无状态化”与“中心化状态转移”做成一页 comparison。

## 来源指针

- `wiki/topics/ai/MCP.md`
