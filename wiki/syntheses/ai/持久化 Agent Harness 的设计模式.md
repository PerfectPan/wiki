---
title: 持久化 Agent Harness 的设计模式
description: 从 Pi harness-v2 设计文档中提炼 agent harness 的持久化与恢复模式：intent record + result entry 的无事务持久性、lane 的并行隔离、append-only tree 与 operation log 的状态分离。
type: synthesis
category: ai
created: 2026-08-20
updated: 2026-08-20
timestamp: 2026-08-20
tags:
  - agent
  - harness
  - durability
  - recovery
  - storage
source_refs:
  - raw/sources/2026-08-20-pi-harness-v2-design.md
  - https://github.com/earendil-works/pi/blob/harness-v2/j4/packages/agent/docs/harness-v2.md
resource:
  - raw/sources/2026-08-20-pi-harness-v2-design.md
  - https://github.com/earendil-works/pi/blob/harness-v2/j4/packages/agent/docs/harness-v2.md
---

# 持久化 Agent Harness 的设计模式

## 问题

Agent harness 如何在崩溃后可靠恢复？如何支持多个并行的执行流而不引入复杂的事务机制？如何把对话状态和执行状态分离，使得恢复逻辑清晰可推理？

## 简答

核心是三个设计选择：**intent record + result entry 的无事务持久性**、**lane 的并行隔离**、**append-only tree 与 operation log 的状态分离**。每次执行副作用前先写 intent record 声明意图和预分配 id，执行后用该 id 写 result entry；崩溃后通过"intent 有没有对应的 result"判断状态，不需要多对象原子事务。

## 来源事实

Pi 的 harness-v2 设计文档定义了一个持久化 agent harness，支持崩溃恢复、多 lane 并行执行、三种存储后端（Memory/JSONL/SQLite）。

### Session 的四部分状态

| 部分 | 说明 | 特性 |
| --- | --- | --- |
| **Tree** | 对话树（消息、模型输出、工具结果） | append-only，所有 lane 共享，只增不改 |
| **Lanes** | 执行位置 | 每个 lane 指向树中的一个 entry，类似 git branch |
| **Lane operation logs** | 操作日志 | 每个 lane 一条，记录执行过程，实现持久性 |
| **Global facts** | 会话级键值 | 会话名、entry 标签，latest-wins |

关键分离：**Tree 是对话内容，operation log 是执行过程**。删除所有 operation log，对话仍然完整有效。

### 持久性规则

> Before an effect: write an intent record that names what will happen and the ids it will produce. After the effect: append the result as an entry with exactly those ids.

三种主要 intent record：

| Intent Record | 写入时机 | 内容 |
| --- | --- | --- |
| `operation_started` | 操作被接受时 | 操作类型（run/compaction/navigation）、初始消息、预分配结果 id |
| `step_attempt` | 每个可重试步骤前 | 第几次尝试、结果 entry 的预分配 id |
| `tool_started` | 工具执行前 | 工具名、参数、结果 id、是否可安全重放 |

**不需要事务**：每条记录单独持久化。崩溃后，有 intent 没有 result → 未完成，重试或合成结果；两者都有 → 已完成。

### Lanes：并行执行的隔离单元

- 每个 lane 是对话树中的一个位置，类似 git branch + worktree
- 每个 lane 最多一个操作（run/compaction/navigation）
- lanes 并行执行，互不干扰
- 例子：Slack 频道是 session，每个 thread 是 lane；子 agent 跑在父 session 的第二个 lane

### Recovery

打开 session 时每个 lane 独立恢复：

1. 查找未完成的 operation（0=idle，1=suspended，2=corruption）
2. 读取该 operation 的所有 records
3. 还原状态：进行到哪一步、哪些 tool call 未完成、是否有 deferred handle
4. 从断点继续：重试未完成的 step、重新执行 safe 的 tool、redeem deferred handle

### Hooks

拦截点：`before_run`、`before_tool`、`after_tool`、`before_compaction`、`before_navigation`、`transform_context`、`before_request`。

关键语义：hook 的输出在执行前持久化（如 `before_tool` 的 effective args 存在 `tool_started` record 里），崩溃后不重复运行已持久化的 hook。

### Storage

三种后端：Memory（测试）、JSONL（兼容 v3）、SQLite（生产）。

JSONL 设计：每个 session 一个文件，每行一个 mutation，原子单位是一行。崩溃导致的残缺尾行直接截断。

## 综合结论

### 1. Intent record 是"无事务持久性"的关键

传统数据库用事务保证"要么全做要么全不做"。Harness 用更简单的方式：**先声明意图，再写结果**。意图记录里预分配了结果的 id，所以"意图有没有对应的结果"就是状态判断的全部依据。

这避免了多对象原子写入的复杂性，也让恢复逻辑变成纯粹的"检查 intent 和 result 的配对关系"。

### 2. 对话状态和执行状态必须分离

Tree（对话）和 operation log（执行）是两种不同性质的状态：

- Tree 是用户可见的对话内容，append-only，不可变
- Operation log 是 harness 的执行元数据，用于恢复，不进入模型上下文

分离的好处：
- 恢复时只需读 operation log，不需要扫描整个对话树
- 对话树保持简单（只增不改），执行状态可以复杂
- 模型永远看不到 operation log，避免干扰

### 3. Lane 是"并行但隔离"的执行单元

多 lane 并行不需要复杂的并发控制，因为：
- 每个 lane 最多一个操作，不存在 lane 内并发
- lane 之间共享对话树，但树是 append-only 的，追加不需要锁
- 每个 lane 有自己的 operation log，互不干扰

这类似 git 的多 branch 模型：branch 之间共享历史，但各自独立推进。

### 4. 持久性的粒度是"副作用"

不是每个操作都需要 intent record，只有产生副作用的操作才需要：
- 模型请求 → `step_attempt`
- 工具执行 → `tool_started`
- 操作开始 → `operation_started`

纯计算、内存操作不需要持久化，因为崩溃后可以重新计算。

## 对个人 agent 系统的启发

- **持久化的核心是"声明意图"，不是"事务"**：在执行副作用前先记录要做什么，比实现原子事务简单得多。
- **对话和执行要分离**：对话内容（用户看到的）和执行元数据（用于恢复的）应该分开存储。
- **并行执行靠隔离，不靠锁**：每个执行流有自己的状态，共享不可变数据，避免并发问题。
- **恢复逻辑应该是纯粹的状态检查**：通过"intent 有没有 result"判断，而不是复杂的状态机。

## 相关页面

- [[wiki/topics/ai/Agent Harness|Agent Harness]]
- [[wiki/syntheses/ai/Agent Harness 演进范式|Agent Harness 演进范式]]
- [[wiki/syntheses/ai/Agent 团队的角色分工与协作模式|Agent 团队的角色分工与协作模式]]
- [[wiki/syntheses/ai/Agent 循环工作流的控制边界|Agent 循环工作流的控制边界]]

## 来源指针

- `raw/sources/2026-08-20-pi-harness-v2-design.md`
- https://github.com/earendil-works/pi/blob/harness-v2/j4/packages/agent/docs/harness-v2.md
