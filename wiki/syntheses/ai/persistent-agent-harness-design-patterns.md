---
title: 持久化 Agent Harness 的设计模式
description: 保留 Pi harness-v2 的历史设计，并用 Pi Durable 1.0.0 收窄意图记录、并发隔离与恢复保证的适用范围
type: synthesis
category: ai
created: 2026-08-20
updated: 2026-10-02
timestamp: 2026-10-02
tags:
  - agent
  - harness
  - durability
  - recovery
  - storage
source_refs:
  - raw/sources/2026-08-20-pi-harness-v2-design.md
  - https://github.com/earendil-works/pi/blob/harness-v2/j4/packages/agent/docs/harness-v2.md
  - raw/sources/2026-10-02-pi-durable.md
  - https://github.com/earendil-works/pi/blob/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/durable/docs/spec.md
resource:
  - raw/sources/2026-08-20-pi-harness-v2-design.md
  - https://github.com/earendil-works/pi/blob/harness-v2/j4/packages/agent/docs/harness-v2.md
  - raw/sources/2026-10-02-pi-durable.md
  - https://github.com/earendil-works/pi/blob/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/durable/docs/spec.md
---

# 持久化 Agent Harness 的设计模式

## 问题

Pi 的早期 harness-v2 如何组织崩溃恢复与多执行流？其中哪些设计仍可借鉴，哪些不能当成当前实现或通用可靠性保证？

## 简答

旧设计的三个重点是 **intent record 与 result entry**、**lane 隔离执行位置**、**对话树与操作日志分离**。这些适合用于理解恢复时需要记录什么，但意图存在而结果缺失，只说明本地结果未知，不能证明外部副作用没有发生。

当前实现另见 [[wiki/topics/ai/pi-durable|Pi Durable]]。1.0.0 已改为 Conversation、Document、Task checkpoint 和 Session 原子提交；SQLite 使用事务，一个 Storage 要由一个进程独占。本文保留以下旧设计资料，不把“无需事务”“无需锁”推广成当前架构或一般规律。[当前设计说明 §4、§5.2](https://github.com/earendil-works/pi/blob/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/durable/docs/spec.md)

## 来源事实：历史 harness-v2 设计

本节记录 2026-08-20 阅读的 harness-v2 设计文档：它规划了崩溃恢复、多 lane 并行执行及 Memory/JSONL/SQLite 后端，不代表当前 `pi-durable` 的数据模型或验证结果。

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

旧设计尝试以单条记录持久化减少多对象原子写入需求。恢复时，有 intent 没有 result 表示结果尚未确认，必须结合工具的可重放性处理；两者都有才可读取已保存结果。这种记录方式本身不保证外部副作用只发生一次。

### Lanes：并行执行的隔离单元

- 每个 lane 是对话树中的一个位置，类似 git branch + worktree
- 每个 lane 最多一个操作（run/compaction/navigation）
- lanes 隔离执行位置和操作日志；工具若访问同一外部资源，仍可能互相影响
- 例子：Slack 频道是 session，每个 thread 是 lane；子 agent 跑在父 session 的第二个 lane

### Recovery

打开 session 时每个 lane 独立恢复：

1. 查找未完成的 operation（0=idle，1=suspended，2=corruption）
2. 读取该 operation 的所有 records
3. 还原状态：进行到哪一步、哪些 tool call 未完成、是否有 deferred handle
4. 从断点继续：重试未完成的 step、重新执行 safe 的 tool、redeem deferred handle

### Hooks

拦截点：`before_run`、`before_tool`、`after_tool`、`before_compaction`、`before_navigation`、`transform_context`、`before_request`。

旧设计将 `before_tool` 的 effective args 保存在 `tool_started` record，供恢复使用。不能据此推导任意 hook 只执行一次：当前实现中，工具意图之后恢复会复用参数，但模型的 `beforeRequest` 会随请求重发再次运行，具体取决于检查点边界。[当前工具实现](https://github.com/earendil-works/pi/blob/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/durable/src/harness/tool.ts)、[当前生成实现](https://github.com/earendil-works/pi/blob/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/durable/src/harness/generation.ts)

### Storage

三种后端：Memory（测试）、JSONL（兼容 v3）、SQLite（生产）。

JSONL 设计：每个 session 一个文件，每行一个 mutation，原子单位是一行。崩溃导致的残缺尾行直接截断。

## 综合结论

### 1. Intent record 记录恢复所需信息，不代替所有事务

**先声明意图，再写结果**能让恢复知道原来准备做什么。预分配结果 ID 有助于关联记录，但外部调用与本地存储之间仍存在失败窗口，需要安全重试、外部幂等 key、可查询回执或中断处理。

当前 Pi Durable 用原子 commit 同时推进任务和库内状态，并将外部副作用放在提交之外。这说明意图记录与事务可以配合使用。[当前设计说明 §5.2](https://github.com/earendil-works/pi/blob/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/durable/docs/spec.md)

### 2. 对话状态和执行状态必须分离

Tree（对话）和 operation log（执行）是两种不同性质的状态：

- Tree 是用户可见的对话内容，append-only，不可变
- Operation log 是 harness 的执行元数据，用于恢复，不进入模型上下文

分离的好处：
- 恢复时只需读 operation log，不需要扫描整个对话树
- 对话树保持简单（只增不改），执行状态可以复杂
- 模型永远看不到 operation log，避免干扰

### 3. Lane 是"并行但隔离"的执行单元

旧设计用 lane 减少执行流之间的状态耦合：
- 同一 lane 同时仅有一个 operation，状态变更仍需串行化
- lane 之间共享 append-only 对话树，但 append-only 本身不能证明追加无需序列化或所有权约束
- 每个 lane 有自己的 operation log，互不干扰

当前 Pi Durable 将多个任务的状态提交排入同一 Session 队列，并要求宿主保证单进程拥有 Storage；它不提供跨进程 owner 锁。执行隔离和存储并发控制需要分别设计。[当前 README Storage](https://github.com/earendil-works/pi/blob/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/durable/README.md#storage)

### 4. 持久性的粒度是"副作用"

旧设计对下面这些执行边界记录意图：
- 模型请求 → `step_attempt`
- 工具执行 → `tool_started`
- 操作开始 → `operation_started`

可重新计算的纯计算不必单独存储；但影响重试行为的输入、选择和标识应进入检查点。当前实现也持久化输入队列 Inbox、配置和取消标记，不能把持久化范围只理解为工具副作用。Session 的提交 Promise 队列本身只存在于进程内。

## 对个人 agent 系统的启发

- **同时设计意图、提交和外部结果**：记录准备做什么，用原子提交保持库内状态一致，再单独处理外部副作用的不确定结果。
- **对话和执行要分离**：对话内容（用户看到的）和执行元数据（用于恢复的）应该分开存储。
- **隔离执行状态仍需并发控制**：明确单写入者、提交序列化以及共享外部资源的协调方式。
- **恢复保证要分层说明**：输入去重、任务不重复收尾和外部业务只生效一次是不同保证。当前转账测试调用服务两次，单次生效依靠服务按 key 去重。[恢复测试](https://github.com/earendil-works/pi/blob/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/durable/test/harness-tasks-recovery.test.ts#L112)

## 相关页面

- [[wiki/topics/ai/pi-durable|Pi Durable：可恢复的 Agent 执行库]]
- [[wiki/topics/ai/agent-harness|Agent Harness]]
- [[wiki/syntheses/ai/agent-harness-evolution-paradigm|Agent Harness 演进范式]]
- [[wiki/syntheses/ai/agent-team-roles-and-collaboration|Agent 团队的角色分工与协作模式]]
- [[wiki/syntheses/ai/agent-loop-control-boundaries|Agent 循环工作流的控制边界]]

## 来源指针

- `raw/sources/2026-08-20-pi-harness-v2-design.md`
- https://github.com/earendil-works/pi/blob/harness-v2/j4/packages/agent/docs/harness-v2.md
- [[raw/sources/2026-10-02-pi-durable|Pi Durable 1.0.0 来源摘要]]
- https://github.com/earendil-works/pi/blob/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/durable/docs/spec.md
