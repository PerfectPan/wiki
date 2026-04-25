---
title: 浏览器 Fetch Streaming 的读取边界
type: synthesis
category: frontend
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - fetch
  - streaming
  - response-body
  - utf8
  - browser
source_refs:
  - legacy-logseq-journals/2023_11_23.md
  - wiki/syntheses/frontend/React 18 流式 SSR 与渐进式 hydration.md
---
# 浏览器 Fetch Streaming 的读取边界

## 问题

浏览器侧的 `fetch` 到底在什么意义上支持 streaming？`.json()`、`.text()` 和底层流读取的边界在哪里？

## 简答

`fetch` 的 `Response.body` 天然可以流式读取，但 `.json()`、`.text()`、`.arrayBuffer()` 这些高级 API 通常会先把数据整体收完再交给你。要真正利用 streaming，就得直接消费底层流，而不是只调用这些便利方法。

## 综合结论

- journal 里的观察非常关键：浏览器侧不是“只有服务端 streaming 才能流式处理”，而是 `fetch` 本身就给了你底层流接口。
- 真正的区别在于你用哪一层 API：
  - `.json()` / `.text()` / `.arrayBuffer()` 更像一次性读完后的语法糖；
  - 直接读 `Response.body`，才会看到浏览器分块接收字节流的真实过程。
- 这也解释了为什么 streaming UI、RSC payload 和聊天式增量输出都依赖底层流，而不是建立在 `.json()` 之上。
- journal 里关于 UTF-8 字节的实验也很有价值：浏览器收到的是字节块，而不是“天然已经分好字符的字符串”。
- 因此更稳的心智模型是：
  - HTTP 报文按字节流到达；
  - 浏览器可把这些字节暴露为可读流；
  - 你是否能做真正 streaming，取决于你是不是绕过了会整体缓冲的便利 API。

## 未决问题

- 当前仓库还没有把 `ReadableStream`、字符解码、增量 parser 和 UI 刷新节奏放在一页里讲清楚。
- 如果后续继续积累流式 UI 实践，可以把“字节流 -> 文本块 -> 结构化数据 -> 视图更新”单独拆一页。

## 来源指针

- `legacy-logseq-journals/2023_11_23.md`
- `wiki/syntheses/frontend/React 18 流式 SSR 与渐进式 hydration.md`
