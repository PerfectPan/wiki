---
title: Provisional headers 调试路径
type: topic
category: systems
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - chrome
  - network
  - debugging
  - headers
source_refs: []
---
# Provisional headers 调试路径

## 摘要

Chrome DevTools 里看到 `Provisional headers are shown` 时，不要只盯 headers 本身，更应该回到“请求到底有没有真正发出去、底层连接发生了什么”去排查。

## 关键点

- 一个朴素但有效的排查路径是：
  - 用 `chrome://net-export/` 录制浏览器网络行为；
  - 再用 `lsof -i:{port}` 看本地 TCP 建连情况。
- 这说明这类问题的重点并不是“某个 header 看起来不对”，而是：
  - 浏览器是否真的发起了请求；
  - 请求在哪一层被拦住；
  - 底层连接是否已经建立。
- 更稳的工程心智是：当 DevTools 给出的只是 provisional 信息时，单看请求面板可能不够，需要切到浏览器网络日志和操作系统层面的连接视角一起看。

## 相关页面

- [[Chrome DevTools]]
- [[Computer Network]]
