---
title: Agent 循环工作流的控制边界
description: 结合 loop 分类与产出、注意力双目标，设计 agent 自动化的触发、停止、验收、并行协作和资源边界。
type: synthesis
category: ai
created: 2026-07-08
updated: 2026-10-13
timestamp: 2026-10-13
tags:
  - agent
  - workflow
  - orchestration
  - evaluation
source_refs:
  - https://threadnavigator.com/thread/2074208949205881033/
  - https://x.com/claudedevs/status/2074208949205881033
  - raw/sources/loopx.md
  - https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/apps/presentation/site/public/blog/zh/from-one-shot-agents-to-long-horizon-control/index.html
  - https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/docs/product/foundations/project-level-reward-model.md
  - https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/docs/development/control-plane-course/00-concept-primer.md
resource:
  - https://threadnavigator.com/thread/2074208949205881033/
  - https://x.com/claudedevs/status/2074208949205881033
  - raw/sources/loopx.md
  - https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/apps/presentation/site/public/blog/zh/from-one-shot-agents-to-long-horizon-control/index.html
  - https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/docs/product/foundations/project-level-reward-model.md
  - https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/docs/development/control-plane-course/00-concept-primer.md
---
# Agent 循环工作流的控制边界

## 问题

Agent loop 不只是“让模型多跑几轮”。如果没有明确触发条件、停止条件、验收方式和成本边界，循环会把 agent 的不确定性放大成 token 消耗、权限风险和低质量重复劳动。

## 简答

Agent loop 的设计重点是决定把哪一块控制权交出去：检查、停止条件、触发器，还是整条例行工作流。越往后自动化程度越高，越需要把完成证据、最大轮数、权限边界、验证手段和模型成本写成显式协议。

判断自动化有没有收益，还要同时看**经过验证的有效产出**和**获得这些产出所需的人的注意力**。减少持续盯守，把人的投入留给目标、质量标准和必要授权，是比单纯增加运行时间或 Agent 数量更具体的设计目标。[双目标与产出因素][loopx-objective]、[人的判断与协作负担][loopx-attention]

## 来源事实

### Loop 的控制权分类

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

### 长程工作的产出与注意力

LoopX 的公开文章提出“最大化 Agent 产出，最小化人的注意力投入”，并列出四个产出因素：**模型能力、有效并行度、时间利用率、目标对齐程度**。文章要求观察每单位算力和人类注意力换来了多少经过验证的产出，并以“无干预跑稳，有干预跑好”描述技术目标：缺少新事实时等待，路线失效时重新规划，验收满足后停止，人的反馈进入下一轮状态。[公开文章第 1 节][loopx-objective]

另一个产品文档写出 `project_reward = f(quantity, quality, token_cost, user_attention_cost)`：交付数量、质量、模型或执行预算消耗、人的指导投入共同用于项目复盘。这是**另一个观察项目价值的视角**，不能与上述四个产出因素混成一组变量。文档明确它不是模型训练奖励函数，也不替代任务 benchmark；它没有给出可计算的函数形式或权重。质量证据不足时，文档建议先用粗粒度标签。[产品价值模型][loopx-reward]

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

## 用双目标检查一次循环

以下是把公开框架用于工程设计的检查方法。四个因素提供优化方向，**没有定义四因素乘积，也不是经过实测标定的产出定律**。不能由此推导运行更久、并行更多或消耗更多 token 就一定增加收益。

以“把公开 issue 推进为可审阅修复 PR”为例，可以逐项检查：

| 产出因素 | 工程含义 | 实际检查问题 |
| --- | --- | --- |
| 模型能力 | 模型能完成所需的理解与推理；落地时还需检查 Agent-loop 的工具调用与验证能力 | 能复现问题并提供验证证据吗？当前失败来自模型判断，还是工具与执行循环缺少支持？ |
| 有效并行度 | 工作与验收边界可分离，并行结果能可靠交接 | 复现、定位和独立审查能分别推进吗？新增 Agent 节省的等待，是否被冲突处理、结果整合与人工 review 抵消？ |
| 时间利用率 | 有可推进的工作时持续执行，等待期间按条件恢复 | CI 没有新结果时能退避吗？还有独立任务可做吗？验收通过或预算耗尽时会停止吗？ |
| 目标对齐程度 | 每轮工作仍服务于原目标与验收标准，纠正后的方向能被后续轮次使用 | PR 修改的是原问题吗？用户更新的验收条件能否跨 session 保留？任务清单做完是否真的意味着目标完成？ |

四因素的名称来自[公开文章][loopx-objective]。将模型能力与 Agent-loop 执行能力一并检查，是本文的工程化解释；[概念导读][loopx-primer]区分模型执行与持久状态，并要求反馈保留权限和证据边界。[并行协作的讨论][loopx-parallel]还强调优先在验收边界可分离的地方并行，紧密耦合的修改可能更适合一个 Worker。

### 减少盯守，保留关键决策

Minimize Human Attention 指减少获得产出所需的注意力投入。设计交互时，可检查以下问题：

- **什么变化值得打断人？** 重要交付、主要阻塞或路线选择是否清楚？能否合并重复汇报，让无变化的巡检保持安静？
- **人被要求判断什么？** 是否需要决定目标、质量标准、权限或风险？问题是否附带产物、证据和可选行动，还是只在要求人提醒 Agent 继续？
- **一次反馈能用多久？** 对目标和验收的纠正是否进入后续状态，避免每次新 session 都让人重新解释？
- **注意力负担是否转移了？** 虽然消息少了，人是否反而需要花更多时间找错误、协调 Agent 或重新验收？

这些问题综合自[交互与协作负担][loopx-attention]、[注意力成本定义][loopx-reward]和[反馈的状态边界][loopx-primer]。减少注意力投入不等于消除 Human Interaction（人机交互）；原文明确要求在需要判断时询问，并保留授权与验收。

### Token 另记资源预算

在上述 PR 例子中，可以分别记录通过验收的修复数量与质量、token 或执行时间、人的 review 与纠偏投入。token 表示资源消耗，不能与并行度拼成原文没有的成本公式。上游的 `token_cost` 也允许用运行分钟数或配额槽位作替代记录，因此记录时要注明单位与采集方式，并先在同一项目或宿主内比较。[预算指标与注意力成本][loopx-budget]

本文建议先固定一类任务、验收标准和预算，再小范围比较：新增并行或延长运行后，经过验证的产出是否增加、返工是否减少、人的总投入是否可承受。必要的授权与 review 仍须保留，单看 token 数、运行时长、消息数量或 Agent 数量都不足以说明收益。

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

- ClaudeDevs 的 loop 分类主要基于 Claude Code primitive；迁移到其他 coding agent 或个人助手系统时，需要重新映射对应的 goal、schedule、workflow 和 usage 能力。
- `/goal` 的 evaluator 本身也可能误判，尤其是目标含糊或依赖主观质量时。
- 定时 loop 如果没有持久状态，很容易重复处理同一批输入，或在外部系统异常时反复空耗。
- Proactive loop 的权限风险高于普通 coding loop，尤其是涉及发消息、合并 PR、发布内容、交易或真实账户操作时。
- 成本控制不能只靠“少跑几轮”，还要能观测每个 skill、subagent、MCP、workflow 的消耗来源。

## 相关页面

- [[wiki/topics/ai/agent|Agent]]
- [[wiki/topics/ai/code-agent|Code Agent]]
- [[wiki/comparisons/ai/workflow-vs-agent|Workflow vs Agent]]
- [[wiki/syntheses/ai/skill-engineering-artifact-protocol|Skill 工程化的产物协议范式]]
- [[wiki/syntheses/ai/agent-proactive-context-management|Agent 主动上下文管理]]
- [[wiki/syntheses/ai/agent-native-system-interface-design|Agent Native 系统接口设计]]
- [[wiki/syntheses/ai/agent-harness-runtime-architecture|Agent Harness 运行时架构与演进]]：工具调用、恢复和资源隔离的具体实现边界。

## 来源指针

- ClaudeDevs, “Getting started with loops”, 2026-07-06: https://threadnavigator.com/thread/2074208949205881033/
- Original X thread: https://x.com/claudedevs/status/2074208949205881033
- [[raw/sources/loopx|LoopX 双目标的公开来源核查]]：固定提交、证据位置与适用限制。
- [LoopX：从一次性 Agent 到长程控制面][loopx-objective]：双目标与四因素；[交互面与并行条件][loopx-attention]。
- [Project-Level Reward Model][loopx-reward]：用于产品复盘的价值维度，包含 token 与人的注意力投入。
- [概念导读][loopx-primer]：无人干预与有人干预的状态、权限和证据边界。

[loopx-objective]: https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/apps/presentation/site/public/blog/zh/from-one-shot-agents-to-long-horizon-control/index.html#L60-L66
[loopx-attention]: https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/apps/presentation/site/public/blog/zh/from-one-shot-agents-to-long-horizon-control/index.html#L210-L234
[loopx-parallel]: https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/apps/presentation/site/public/blog/zh/from-one-shot-agents-to-long-horizon-control/index.html#L224-L234
[loopx-reward]: https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/docs/product/foundations/project-level-reward-model.md#L11-L85
[loopx-budget]: https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/docs/product/foundations/project-level-reward-model.md#L59-L85
[loopx-primer]: https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/docs/development/control-plane-course/00-concept-primer.md#L3-L45
