---
title: 让AI主动管理自己的上下文
type: source
category: ai
status: captured
created: 2026-06-28
source_url: https://blog.xlab.app/p/6a966aeb/
author: 透明人
published: 2026-02-08
tags:
  - agent
  - context-management
  - session-tree
---

# 让AI主动管理自己的上下文

## 来源

- 原文：<https://blog.xlab.app/p/6a966aeb/>
- 作者：透明人
- 发布时间：2026-02-08
- Atom 源：<https://blog.xlab.app/atom.xml>

## 来源事实摘录

- 文章认为，当前主流上下文管理更多关注“如何找到内容放进上下文”，例如 RAG、MEM；对“如何清理上下文”的讨论较少。
- 现有清理方式多是在上下文窗口达到阈值后触发压缩，例如 Claude Code 的 compact。作者指出这通常是一次全量历史消息调用，成本高，也容易丢失信息。
- 作者引用 Kimi CLI 的 d-mail 思路：当模型发现自己做了低信息密度动作后，可以回到过去节点，并给过去的自己留一条压缩消息。
- 作者引用 Pi agent 的 session tree 设计：会话以树形式保存，每条消息是节点，支持分支和节点跳转。
- 作者把 session tree 类比为 Git 工作流：
  - 每条消息类似 commit；
  - 跳转类似 checkout；
  - 总结类似 merge request 之后的精简 commit；
  - session log 类似带标记的 git log。
- 作者提出让 agent 在对话中主动维护上下文骨架，形成“构建、感知、跳转”循环：
  - 构建：主动给关键节点打 tag；
  - 感知：查看上下文骨架、占用率、距离上次 tag 的步数；
  - 跳转：在骨架上 checkout，并带上一条 summary。
- 文章提出三个工具设计：
  - `context_tag`：标记关键上下文节点；
  - `context_log`：展示上下文骨架与占用仪表盘；
  - `context_checkout`：跳回某个节点，并带上总结消息。
- 作者进一步提出“无损的时间回溯”：不仅能回到过去，也能通过记录来源节点再回到未来分支。
- 文章认为，给 agent 一个结构化上下文，让 agent 自己编排和管理，可能在多线、长周期任务、个人助手、wide/deep research 中有价值。

## 初步判断

这篇文章的价值不在于某个具体插件，而在于把上下文压缩问题重新表述为 agent 可操作的上下文生命周期管理问题。它把 session tree、summary、tag、checkout、上下文占用提示和 skill 规则组合成一个较完整的工程模型，适合进一步沉淀为 AI agent 系统设计的综合页。
