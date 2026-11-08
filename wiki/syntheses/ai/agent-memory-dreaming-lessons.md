---
title: Agent Memory 的记忆选择、纠错与验证
description: 从 Anthropic 的记忆实验提炼保存规则、回查原始记录和评估 wiki 收益的方法
type: synthesis
category: ai
created: 2026-11-08
updated: 2026-11-08
timestamp: 2026-11-08
tags:
  - agent
  - memory
  - evaluation
  - context-engineering
source_refs:
  - raw/sources/anthropic-components-of-agent-memory.md
  - https://www.anthropic.com/research/components-of-agent-memory
resource:
  - raw/sources/anthropic-components-of-agent-memory.md
  - https://www.anthropic.com/research/components-of-agent-memory
---

# Agent Memory 的记忆选择、纠错与验证

## 问题与简答

智能体已经有日志、搜索和笔记，为什么还需要离线整理记忆？

记忆的目标是让未来少走弯路，而不是保存更多文字。Anthropic 将离线检查日志、纠正笔记和维护知识结构的过程称为 dreaming。它有价值的前提是能减少重复错误或检索成本，而不是把摘要写得更长。

本文基于 [Components of agent memory][article] 提炼方法。下文把文章报告的观察与设计建议分开。具体设置及未复现范围见 [[raw/sources/anthropic-components-of-agent-memory|阅读证据]]。存储、修订与撤回接口的设计见 [[wiki/syntheses/ai/agent-memory-implementation|如何实现 Agent Memory]]，这里不重复展开。

## 1. 记住推导结果，而不只是可重新读取的状态

**文章观察：** 在 Pokémon 实验中，较早模型大量保存战斗、物品和位置。许多状态下一轮就能从屏幕读到，还会不断过时。另一个模型主要保存目标、策略与经过检验的规则，维护的文件少得多。见原文 “Claude has learned to judge salience”。

**设计建议：** 编程任务中，当前文件列表可以重新扫描，当前分支可以重新查询。更值得跨会话保留的是无法直接从这些状态看出的原因，例如：

- 为什么某个依赖不能升级，以及复查条件是什么。
- 哪条失败路径已经重现，怎样验证修复。
- 某个决定适用于哪个项目，哪些场景不能沿用。

判断一条记忆是否值得写入，可以先问：不保存它，下次需要重新推导什么？这不是“越少记越好”，任务进度仍可能需要保存用于交接。

也不要把上述建议固化为“只记录失败”。原文 “Steering Claude to write memory” 中，这条限制削弱了 Opus 5 和 Opus 4.7 从记忆获得的增益。成功经验和已验证的正面规则同样可能值得保留。

## 2. 记忆是预测，不是永久成立的事实

**文章观察：** 写下一条规则，是预测未来还会遇到相关模式。CL-Bench 中，只保存未经检验的猜测，与检验假设后保存规则，是不同的学习行为。文章也指出环境变化会让记忆过时。见 “Memory can be a prediction about what the future will need” 与结尾讨论。

**设计建议：** 对会影响后续决策的记忆，记录来源、验证状态和适用条件。例如“这个命令不能并行运行”要说明在哪个版本、通过什么现象或测试得到，而不是从一次失败推成所有项目的禁令。没有验证的假设仍可保存，但不能在召回后悄悄变成确定规则。

## 3. 离线整理应回查证据，不只是再次总结

**文章观察：** Mt. Moon 案例的关键不是写出更好的摘要，而是对照会话记录，发现 PokéCenter 方位笔记错误并更正。错误记忆让模型反复走回旧路。见 “Dreaming can correct memory”。

**设计建议：** 保留原始记录的可回查位置，将笔记和 wiki 作为可修订的内容。整理时先问“这条规则的证据是否支持它”，再决定保留、修改或删除。只对旧摘要继续总结，没有增加独立依据，还可能让错误更难被发现。

日志也不等于外部世界的真相。记录中可能包含模型误判、错误工具结果或过时信息，回查时仍需分辨是谁观察到了什么。

## 4. Wiki 帮助搜索，不应取代搜索

文章在约 350,000 个文件、420M token 的内部资料上构建 wiki，用 25 道问题评估。随着构建会话从 2 次增加到 128 次，图 10 报告：

| 使用方式 | 满足评分标准的比例 |
| --- | --- |
| 仅搜索 | 53% |
| wiki 加搜索 | 从 54% 到 61% |
| 仅 wiki | 从 13% 到 48% |

wiki 加搜索还节省了每题约 20,000 token。这里的指标不是所有问题的通用正确率，也不包含构建 wiki 的全部成本。见 “Dreaming can build new memory representations”。

**设计建议：** Wiki 适合帮助智能体知道已有知识在哪里、跨文档关系是什么，再回到来源核对。需要跨文档推理的任务可能获益更多；单份文档就能直接检索的问题，不一定需要额外 wiki。若 wiki 比原文更大，却没有减少查找和推理成本，就应考虑删减或改变组织方式。

## 5. 先检查写入方式，再怀疑模型能力

**文章观察：** 合同任务从约 72% 提升至 100%，伴随三项修改：明确条款的重要性、每份合同由一个智能体写独立页面、逐字保留条款而非概括进共享表。旧方式会发生相互覆盖。见 “Dreaming can focus memory on a specific goal”。

**设计建议：** 记忆遗漏不一定是模型不会记，也可能是文件被覆盖、多个任务修改同一区域，或摘要抹掉了关键条件。优先把写入对象拆开，明确谁负责哪份内容，再汇总索引。若必须多人改同一对象，则需要版本检查等并发控制。

上述实验同时改变多个因素，只能说明整组改动在该任务有效，不能证明任何一项改动独自解释了全部提升。

## 6. 用同一模型验证收益，算上维护成本

**证据边界：** Sonnet 3.7 与 Fable 5 的 Pokémon 对比既换了模型，各自也只展示一次运行。它不能证明少记文件导致更强。CL-Bench 的同模型无状态与有记忆对比，更接近回答“记忆在这项任务上是否有帮助”，但仍不能直接推广到所有工作。

**设计建议：** 在自己的任务上固定模型、工具和预算，比较：

1. 没有跨会话记忆。
2. 只有原始记录搜索。
3. 搜索加可修订笔记或 wiki。
4. 在相同基础上加入离线整理。

同时记录任务成功率、重复错误、召回内容是否过时、前台 token 与延迟，以及后台整理成本。条件允许时重复运行，不能只挑一次成功演示。

## 对文件优先 Wiki 的启发

下面是工程建议，不是文章已经验证的完整实现：

- **原始记录可追溯。** 每个关键判断能找到来源位置，必要时重建笔记与索引。
- **常驻索引保持短。** 只预先加载稳定约定和导航，其余内容按需读取，避免错误在每次会话中重复出现。
- **经验规则要验证。** 保留检查方法与适用范围，区分假设和已验证规则。
- **过时内容能纠正。** 按风险、变化频率和访问情况决定复查优先级，不必每次扫描全部记忆。

先用这些条件检查现有 Wiki，再决定是否增加自动 dreaming。增加一轮模型调用，本身并不等于完成了维护。

## 相关页面与来源

- [[wiki/syntheses/ai/agent-memory-implementation|如何实现 Agent Memory]]
- [[wiki/syntheses/ai/auditable-local-agent-memory-architecture|可审计的本地 Agent 记忆架构]]
- [[wiki/comparisons/ai/agent-memory-approaches|Agent 记忆方案对比]]
- [[raw/sources/anthropic-components-of-agent-memory|文章阅读证据]]
- [Anthropic · Components of agent memory][article]

[article]: https://www.anthropic.com/research/components-of-agent-memory
