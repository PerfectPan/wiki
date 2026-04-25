---
title: Agent Client Protocol
type: topic
category: ai
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - code-agent
  - protocol
  - capability-negotiation
  - editor
source_refs:
  - legacy-logseq-journals/2025_09_14.md
  - https://agentclientprotocol.com/overview/introduction
---
# Agent Client Protocol

## 摘要

Agent Client Protocol 是面向 editor / client 与 code agent 之间的协议约定，目标是让双方用明确的能力协商和边界行为来完成集成，而不是靠私有耦合。

## 关键点

- journal 对它的核心观察很准确：这类协议的价值不只是“能连起来”，而是把两边的边界行为显式写清楚，减少隐藏假设。
- 记录里摘出的初始化规则很关键：
  - `initialize` 里声明的 capability 都是可选的；
  - 新 capability 的引入不应被视为 breaking change；
  - 对端没声明的 capability，应该按“不支持”处理。
- 这类设计意味着协议更偏向渐进扩展，而不是强行要求所有 client 和 agent 一次性升级到同一能力集合。
- 对 code agent 生态来说，这种协议层的可协商性很重要，因为 editor、agent、tool runner 的演化速度通常不同步。

## 相关页面

- [[Code Agent]]
- [[Agent]]

## 来源指针

- `legacy-logseq-journals/2025_09_14.md`
- [Agent Client Protocol](https://agentclientprotocol.com/overview/introduction)
