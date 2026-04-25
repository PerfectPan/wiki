---
title: 同源 iframe 沙箱设计
type: synthesis
category: frontend
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - iframe
  - sandbox
  - security
  - isolation
source_refs: []
---
# 同源 iframe 沙箱设计

## 问题

如果业务场景要求在同源 iframe 里跑不可信或半可信代码，应该重点控制哪些边界？

## 简答

核心不是“有没有 iframe”，而是如何同时约束脚本执行、资源访问、DOM 挂载和路由跳转。即使使用同源 iframe，也必须额外补窗口代理、CSP、资源拦截和宿主边界控制，才能接近真正可用的沙箱。

## 综合结论

- 同源 iframe 的问题从来不是“能不能隔离”，而是“隔离粒度够不够细”。
- 这条材料把沙箱控制点拆成了四类：
  - 脚本：不安全脚本不可运行；
  - 资源：不安全资源不可请求；
  - DOM：不安全节点不能挂到宿主树；
  - 路由：不安全跳转不可逃逸。
- 这也解释了为什么只做 iframe 容器远远不够，实际还要配合：
  - `window` 代理；
  - 事件 / 视图对象改写；
  - CSP；
  - 对资源请求的额外拦截。
- 更稳的工程理解是：同源 iframe 沙箱并不是浏览器自带的完整隔离层，而是一个“你自己继续补边界”的基础设施。

## 未决问题

- 当前材料还没有把同源 iframe 和 cross-origin iframe、Worker、进程隔离放在一起比较。
- 如果后续继续沉淀沙箱系统内容，这页可以进一步连接到 `线程级隔离 vs 进程级隔离`。
