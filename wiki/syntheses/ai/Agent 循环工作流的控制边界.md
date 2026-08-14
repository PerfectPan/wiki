---
title: Agent 循环工作流的控制边界
description: 从 ClaudeDevs 的 loop 分类中抽象出 agent 自动化的触发、停止、验收和成本控制模型。
type: synthesis
category: ai
created: 2026-07-08
updated: 2026-07-08
timestamp: 2026-07-08
tags:
  - agent
  - workflow
  - orchestration
  - evaluation
source_refs:
  - https://threadnavigator.com/thread/2074208949205881033/
  - https://x.com/claudedevs/status/2074208949205881033
resource:
  - https://threadnavigator.com/thread/2074208949205881033/
  - https://x.com/claudedevs/status/2074208949205881033
---
# Agent 循环工作流的控制边界

## 问题

Agent loop 不只是“让模型多跑几轮”。如果没有明确触发条件、停止条件、验收方式和成本边界，循环会把 agent 的不确定性放大成 token 消耗、权限风险和低质量重复劳动。

## 简答

Agent loop 的设计重点是决定把哪一块控制权交出去：检查、停止条件、触发器，还是整条例行工作流。越往后自动化程度越高，越需要把完成证据、最大轮数、权限边界、验证手段和模型成本写成显式协议。

## 来源事实

ClaudeDevs 将 loop 定义为：agent 重复执行工作循环，直到满足停止条件。文章按触发方式、停止方式、Claude Code primitive 和适用任务，把 loop 分为四类：

| Loop 类型 | 交出去的控制权 | 触发方式 | 停止条件 | 典型 primitive |
| --- | --- | --- | --- | --- |
| Turn-based | 检查 | 用户 prompt | Agent 判断完成或需要更多上下文 | 普通对话 + verification skill |
| Goal-based | 停止条件 | 手动 prompt | 目标达成或达到最大轮数 | `/goal` |
| Time-based | 触发器 | 时间间隔 | 用户取消、PR 合并、队列清空等 | `/loop`、`/schedule` |
| Proactive | 实时 prompt | 事件或计划任务 | 单个任务达标；例行任务持续运行直到关闭 | `/schedule` + `/goal` + dynamic workflows + auto mode |

文章还强调两条工程前提：

- 质量取决于 loop 外围系统：干净代码库、可达文档、可量化 verification skill，以及独立 review agent。
- 成本控制要靠边界：选合适模型和 primitive、设置明确 done/stop 条件、先小范围试跑、确定性工作交给脚本、不要过密轮询，并通过用量工具观察 skill、subagent 和 workflow 的消耗。

## 综合结论

Agent loop 可以理解为一组逐步上升的自动化交接层：

1. **Turn-based loop：把检查流程结构化。**
   人仍然掌握推进节奏，但可以把“怎么验收”写进 skill，让 agent 自己启动服务、跑测试、看浏览器、检查日志和截图。这里的重点不是延长 agent 工作时间，而是减少人类重复检查。

2. **Goal-based loop：把停止条件外置。**
   `/goal` 的价值在于阻止 agent 过早判断“差不多完成了”。目标应尽量是确定性或可量化的，例如测试数、性能分数、lint 状态、覆盖率阈值、候选数量。没有清晰验收标准的任务，不适合直接升为 goal loop。

3. **Time-based loop：把触发器交给时间。**
   定时 loop 适合输入在外部系统中变化的工作，例如 PR review、CI 状态、消息汇总、队列巡检。这里最容易出问题的是轮询频率和重复处理，所以要设计去重、空跑退出、最长运行时间和状态记录。

4. **Proactive loop：把整条例行工作流系统化。**
   这类 loop 已经接近自动化系统，不只是 prompt 技巧。它需要任务路由、权限策略、子代理并行、审查 agent、状态存储、失败恢复和成本监控。适用场景必须是“反复出现、输入清楚、验收可写、权限边界可控”的工作流。

## 设计检查表

在把任务升级成 loop 前，先问四个问题：

- **触发是否清楚？** 是用户手动触发、目标触发、时间触发，还是外部事件触发？
- **完成证据是什么？** 是测试通过、分数达标、队列清空、PR 合并，还是人工确认？
- **停止边界在哪里？** 最大轮数、最大耗时、最大 token、最大子任务数、失败次数上限分别是多少？
- **谁负责验证？** 主 agent 自检、verification skill、脚本、浏览器、CI、review agent，还是人类？

如果这四项写不清楚，loop 只会把一次模糊任务变成多轮模糊任务。

## 对现有 agent 系统的启发

- 定时简报、RSS 筛选、PR 修复、wiki 维护都不应只写“每隔多久做一次”，还要写清楚空跑条件、去重状态、投递目标、失败告警和完成证据。
- Skill 的价值不只是让 agent 知道工具怎么用，更重要的是把验收流程、失败处理和退出条件写成可重复协议。
- 多 agent 并行适合探索空间大、可独立验证的任务；如果每个分支都需要昂贵语义判断，fan-out 会迅速变成成本问题。
- 对外部动作和长期例行任务，auto mode 必须和权限边界绑定。能自动执行不等于应该自动提交、发布或对外回复。
- 复杂 loop 最好使用第二个 agent 做审查。主 agent 自己推进、自己验收，容易把中间推理当成完成证据。

## 风险和未决问题

- 文章主要基于 Claude Code primitive；迁移到其他 coding agent 或个人助手系统时，需要重新映射对应的 goal、schedule、workflow 和 usage 能力。
- `/goal` 的 evaluator 本身也可能误判，尤其是目标含糊或依赖主观质量时。
- 定时 loop 如果没有持久状态，很容易重复处理同一批输入，或在外部系统异常时反复空耗。
- Proactive loop 的权限风险高于普通 coding loop，尤其是涉及发消息、合并 PR、发布内容、交易或真实账户操作时。
- 成本控制不能只靠“少跑几轮”，还要能观测每个 skill、subagent、MCP、workflow 的消耗来源。

## 相关页面

- [[wiki/topics/ai/Agent|Agent]]
- [[wiki/topics/ai/Code Agent|Code Agent]]
- [[wiki/comparisons/ai/Workflow vs Agent|Workflow vs Agent]]
- [[wiki/syntheses/ai/Skill 工程化的产物协议范式|Skill 工程化的产物协议范式]]
- [[wiki/syntheses/ai/Agent 主动上下文管理|Agent 主动上下文管理]]
- [[wiki/syntheses/ai/Agent Native 系统接口设计|Agent Native 系统接口设计]]

## 来源指针

- ClaudeDevs, “Getting started with loops”, 2026-07-06: https://threadnavigator.com/thread/2074208949205881033/
- Original X thread: https://x.com/claudedevs/status/2074208949205881033
