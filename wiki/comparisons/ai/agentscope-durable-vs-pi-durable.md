---
title: AgentScope Durable vs Pi Durable
description: 对照微信长文中的 AgentScope Durable（及 AgentCore 托管方向）与 wiki 已有的 Pi Durable：数据模型近乎同构，但产品与宿主不同；澄清 Document 与 Task 的分工，不将二者视为同一代码库
type: comparison
category: ai
created: 2026-11-04
updated: 2026-11-06
timestamp: 2026-11-06
tags:
  - agent
  - durability
  - recovery
  - agentscope
  - pi-durable
source_refs:
  - wiki/topics/ai/agentscope-durable.md
  - wiki/topics/ai/pi-durable.md
  - raw/sources/agentscope-durable.md
  - raw/sources/2026-10-02-pi-durable.md
  - https://mp.weixin.qq.com/s/z8JHkCyOVVKrXpKH-vy6tw
resource:
  - wiki/topics/ai/agentscope-durable.md
  - wiki/topics/ai/pi-durable.md
  - raw/sources/agentscope-durable.md
  - raw/sources/2026-10-02-pi-durable.md
  - https://mp.weixin.qq.com/s/z8JHkCyOVVKrXpKH-vy6tw
---

# AgentScope Durable vs Pi Durable

## 一段话结论

两者解决的是同一类问题：**仅保存对话历史不足以恢复任务，需要把任务进度、工具意图和结果变为可提交、可调度的状态。** 数据模型名词几乎一一对应（Conversation / Entry / Document / Task / Submission / Commit），工具恢复同样采用「先持久化调用意图，再依据 safe / unsafe 策略决定能否重放」，邮件类例子也都依赖外部幂等。差别在产品与宿主：[[wiki/topics/ai/agentscope-durable|AgentScope Durable]] 在文中基于 AgentScope HarnessAgent 实现，并接入阿里云 AgentCore（Session Store、Brain–Hands）；[[wiki/topics/ai/pi-durable|Pi Durable]] 是 npm 包 `@earendil-works/pi-durable`，在库内提供 Session 与调度，进程内独占存储与唤醒由宿主负责。**概念相近不等于同一代码库**；本文未做源码同源考证。

## 备选项各自是什么

| | AgentScope Durable（据微信长文） | Pi Durable（据已沉淀 topic / 固定 commit） |
| --- | --- | --- |
| 定位 | AgentScope 的 Durable 执行内核 + Session 提交协议；文中结合 AgentCore 托管方向 | `@earendil-works/pi-durable` 进程内执行库（1.0.0，Experimental） |
| 状态机实现 | HarnessAgent + 任务调度器 + Storage | Harness / Session + TaskScheduler + Storage |
| 宿主 / 平台 | 文中强调 AgentCore：共享 Session Store、唤醒、Brain–Hands、Environment | 宿主负责进程生命周期、鉴权、存储独占；库不提供分布式所有权 |
| 证据形态 | 公众号概念文；未审计 AgentScope 源码 | README / spec / 源码与测试（固定 `9b3c19da…`） |

## 共享概念（近乎同构）

| 概念 | 两边各自怎么说 | 共同意图 |
| --- | --- | --- |
| Conversation | 对话范围 | 组织 transcript |
| Entry | 不可变会话记录 | 用户/助手/工具结果只追加 |
| Document | 可事务更新的结构化状态（类型 + 版本；基线/增量） | 计划、回执、运行配置等可变事实 |
| Task | 阶段 + checkpoint + 终态 | 用状态机代替调用栈 |
| Submission | 输入受理与处理结果 | 「已接收」≠「已回答」；`requestId` 去重 |
| Commit | Entry / Document / Task 等同批原子提交 | 避免「完成了但没结果」或「有结果但任务没推进」 |
| 工具意图 | call 先保存意图 → 事务外执行 → 提交结果；恢复走 execute | 将意图与结果之间的缺口显式建模 |
| safe / unsafe | 双方策略均为 safe 才重跑，否则 interrupted | 框架不自动把外部写操作变成幂等 |
| 五封邮件类例子 | 文中核心例子 | Pi Durable 测试里也有按 key 去重的转账/副作用示范 |

**Document ≠ Task。** 不存在单一的「task document」对象；业务事实保存在 Document，执行进度保存在 Task，二者常在同一次 Commit 中一起更新。两者为什么不能合并、工具结果分别存储在何处、Task 是否按工具建模，见 AgentScope 主题页的 [[wiki/topics/ai/agentscope-durable#Document 与 Task：事实和进度是两类数据|Document 与 Task 分工]]一节；配图也在该页。可运行的恢复测试对照见本页「差异与取舍」中 Pi Durable 一行。

## 差异与取舍

| 如果需要 | 更贴近哪边的叙述 | 因为 | 代价 / 注意 |
| --- | --- | --- | --- |
| 理解「会话恢复 vs 任务恢复」与 Document/Task 分工 | AgentScope 长文 + 本 wiki topic | 以邮件例子完整说明意图与结果之间的恢复缺口 | 证据为文章，未核对源码 |
| 对照可运行的库 API、测试与存储后端行为 | Pi Durable topic | 有固定 commit、测试用例与 SQLite/JSONL 边界 | 单进程独占；外部幂等仍由业务保证 |
| 云上托管、统一 Session Store、推理与工具生命周期分离 | AgentScope 文中的 AgentCore / Brain–Hands 方向 | 由平台回答状态存储位置与恢复执行者 | 文中多为架构方向；落地需另查产品文档 |
| 自建宿主（本地进程、自选 Storage、自管唤醒） | Pi Durable | 库边界清楚：不提供对象路由与分布式锁 | 多实例协调需自行实现 |

## 避免过度推断

1. 不应仅因概念名称对应，就断言「AgentScope 派生自 Pi」或「Pi 就是 AgentScope」——没有证据。
2. 不应将 AgentCore 的节点恢复直接等同于文中细粒度的 Task 阶段；原文区分了「已有的托管节点恢复」与「深入执行内核的阶段 / 工具交接」。
3. 不应将「可安全重放」理解为端到端 exactly-once；二者均将外部动作确认交由业务系统负责。
4. Pi Durable 页中的存储刷盘、`close` 时挂起等限制来自其源码审计；AgentScope 侧没有对等审计，不能将 Pi 的限制直接套用到 AgentScope。

## 相关页面

- [[wiki/topics/ai/agentscope-durable|AgentScope Durable]]
- [[wiki/topics/ai/pi-durable|Pi Durable]]
- [[wiki/topics/ai/agent-harness|Agent Harness]]
- [[wiki/syntheses/ai/agent-harness-runtime-architecture|Agent Harness 运行时架构与演进]]

## 来源指针

- [[raw/sources/agentscope-durable.md]]、[微信原文](https://mp.weixin.qq.com/s/z8JHkCyOVVKrXpKH-vy6tw)
- [[raw/sources/2026-10-02-pi-durable.md]]、[[wiki/topics/ai/pi-durable|Pi Durable topic]]
