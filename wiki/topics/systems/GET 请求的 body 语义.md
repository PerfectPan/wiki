---
title: GET 请求的 body 语义
type: topic
category: systems
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - http
  - get
  - request-body
  - semantics
source_refs: []
---
# GET 请求的 body 语义

## 摘要

HTTP 并没有为 `GET` 请求的 body 赋予明确语义，因此它既不是标准鼓励的常规做法，也不是协议层完全禁止的行为。

## 关键点

- 核心在于：协议没有强行为 `GET` body 指定业务语义。
- 这意味着“能不能发”与“应不应该依赖它”是两回事：
  - 某些实现从技术上允许你发送 body；
  - 但很多客户端、网关、缓存层、浏览器和框架不会把它当作稳定约定来支持。
- 不同实现的态度并不一致：
  - 有的直接禁止；
  - 有的不建议；
  - 有的技术上可行但不保证行为一致。
- 所以在工程实践里，更稳的判断不是“协议没禁止就能用”，而是：如果你的接口语义依赖 body，就不该再坚持 `GET`。

## 相关页面

- [[HTTP]]
