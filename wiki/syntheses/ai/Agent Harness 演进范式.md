---
title: Agent Harness 演进范式
description: 基于 HarnessX 论文，沉淀 agent harness 如何从静态脚手架演进为可组合、可观测、可演化的运行时接口。
type: synthesis
category: ai
status: seed
created: 2026-07-02
updated: 2026-07-02
timestamp: 2026-07-02
tags:
  - agent
  - harness
  - evaluation
  - rl
source_refs:
  - raw/sources/2026-07-02-harnessx-agent-harness-foundry.md
  - https://arxiv.org/abs/2606.14249
  - https://arxiv.org/pdf/2606.14249
resource:
  - raw/sources/2026-07-02-harnessx-agent-harness-foundry.md
  - https://arxiv.org/abs/2606.14249
  - https://arxiv.org/pdf/2606.14249
---

# Agent Harness 演进范式

## 问题

Agent 系统的能力提升，除了换更强模型，还能不能通过改进模型外层的运行时 harness 获得复利？

## 简答

可以，但前提是把 harness 当成一等工程对象，而不是 prompt、tools、memory、retry policy 和 control flow 的临时胶水。HarnessX 的核心启发是：agent harness 应该可组合、可观测、可演化，并且执行 trace 不应只用于 debug，还应转化为 harness update 和模型训练信号。

## 来源事实

HarnessX 论文把 agent harness 定义为模型与环境之间的运行时中介：它决定任务如何表达、工具如何暴露、记忆如何读写、控制流如何推进、模型输出如何变成行动。

论文提出三层机制：

- **Harness Composition**：把 harness 拆成 typed processors，挂到 task/model/tool lifecycle hooks 上，通过 substitution algebra 做组合与替换。
- **Harness Adaptation / AEGIS**：用 Digester、Planner、Evolver、Critic / gating 组成 trace-driven harness evolution loop。
- **Harness-Model Co-Evolution**：把 harness 演化 trajectory 作为强化学习信号，用 cross-harness GRPO 让模型吸收不同 harness 版本中的有效策略。

实验覆盖 ALFWorld、GAIA、WebShop、tau^3-Bench、SWE-bench Verified，论文报告平均提升 +14.5%，最高 +44.0%。但它也明确承认没有 held-out evaluation，所有结果都在 adaptation set 上测，且 SWE-bench Verified 只用了 55-task subsample。

## 综合结论

### 1. Harness 是 Agent 产品的真实接口层

很多 agent 产品表面上是“模型 + 工具”，实际稳定性主要取决于 harness：任务如何进入上下文、工具调用前后怎么改写、失败怎么重试、历史怎么裁剪、trace 怎么记录、评估怎么回放。

因此 harness 不应该只是散落在应用代码里的 glue logic。更稳的设计是把它拆成明确组件：

- context processor：任务、历史、用户输入如何进入模型；
- tool processor：工具输入、权限、结果、失败如何处理；
- memory processor：什么进入长期或短期记忆；
- control processor：何时继续、停止、重试、切换策略；
- evaluation processor：如何判定一轮执行是否真的变好。

这和 [[Agent Native 系统接口设计]] 的 DSL / IR / validation 思路是同一类工程选择：模型外部需要一个低熵、可验证的操作面。

### 2. Trace 是 harness 演化的原材料，不只是日志

HarnessX 最有价值的地方，是把执行轨迹视为持续改进的输入。一次失败不只是“这个任务没过”，而是可以拆成：

- 证据没拿到；
- 工具返回格式不稳定；
- prompt 误导了搜索策略；
- memory 引入旧偏见；
- retry policy 过早停止；
- evaluator 被格式漏洞欺骗。

如果 trace 足够结构化，系统就可以把这些失败聚类，再选择改 prompt、改工具、改 processor、改 config，或者直接拒绝本轮改动。没有 trace，所谓 harness 演化只会退化成拍脑袋调 prompt。

### 3. Harness 演化也会有 RL 式病灶

论文把 symbolic harness adaptation 映射到 RL，并指出三类病灶：

- reward hacking：harness 改动让 benchmark 过了，但不是因为真实能力提升；
- catastrophic forgetting：连续叠加规则后，之前能做对的任务被破坏；
- under-exploration：系统只反复微调同一类改动，找不到更有效的工具或控制流变更。

这点很实在。很多 agent 系统一旦开始“自动改自己”，最危险的不是改不动，而是看似提升、实则把评估器和历史样本摸透了。Critic、change manifest、seesaw constraint、variant isolation 这些机制，本质上是在给自我演化加刹车。

### 4. 弱模型更吃 harness 红利，但也有能力地板

论文报告的一个重要现象是 inverse-scaling：弱模型从 harness evolution 中拿到更大提升。例如 ALFWorld 上 Qwen3.5-9B 提升 +44.0，而 Sonnet 4.6 提升 +11.2。

这对个人 agent 系统很有启发：在预算有限、不能总上最大模型时，好的 harness 可以补一部分能力差距。尤其是工具重发、预算调整、检索路径替换、错误保护、任务拆解这些结构性改动，往往比单纯换 prompt 更有效。

但 SWE-bench 的结果也说明有能力地板。对仓库级代码修改，弱模型即使得到 prompt / processor / config 支持，也可能无法执行复杂修复。Harness 可以降低错误率，但不能把不具备基础能力的模型直接抬成强 coder。

### 5. Co-evolution 好听，但现实门槛高

HarnessX 进一步提出 harness-model co-evolution：harness 改进产生 trajectory，模型再通过 cross-harness GRPO 学这些轨迹，训练后的模型反过来支持下一轮 harness 演化。

工程上这很漂亮，但现实约束很硬：

- 需要同时控制 harness 和模型训练；
- 需要共享 replay buffer；
- 需要能负担 rollout、训练和评估成本；
- 需要组织上让产品工程、模型训练、评估团队同步。

多数团队短期更现实的路径，是先做 harness-only evolution：结构化 trace、failure clustering、手动或半自动 change manifest、CI / benchmark gating。等这些基础设施稳定后，再考虑模型训练闭环。

## 对 OpenClaw / 个人自动化的启发

对 OpenClaw 这类个人 agent 系统，HarnessX 的启发不是照搬 AEGIS，而是先把运行时接口打磨成可演化对象：

- 每次任务保存结构化 trace：输入、工具调用、失败、修复、最终产物。
- 对常见任务建立 benchmark-like replay set，例如新闻简报、wiki PR、代码调研、小红书自动化。
- 把 prompt、工具包装、记忆策略、投递策略、重试策略拆成可替换 processors。
- 每次改动写 change manifest，说明改了什么、预期改善什么、风险是什么。
- gating 不只看本次任务成功，也要回放旧任务，防止为一个场景破坏另一个场景。
- 对异质任务保留 variant isolation，不要让新闻、代码、社媒、wiki 共用一套越来越臃肿的 harness。

这比“让 agent 自己越来越聪明”更现实。真正能复利的是 trace、评估集、可替换 harness、回放和审查流程。

## 保留判断

这篇值得沉淀，但实验数字要保守引用。它没有 held-out evaluation，报告的是 adaptation set 上的 peak / end-of-run 表现，存在过拟合和选择偏差。长期价值在方法论：agent 的 runtime interface 可以像软件系统一样被组合、观测、演化和回放，而不是每次靠人工改 prompt。

## 相关页面

- [[Agent]]
- [[Code Agent]]
- [[Agent Native 系统接口设计]]
- [[Agent-native 生成型 CLI 的产物协议]]
- [[LLM 结构化输出的可靠性边界]]

## 来源指针

- `raw/sources/2026-07-02-harnessx-agent-harness-foundry.md`
- https://arxiv.org/abs/2606.14249
- https://arxiv.org/pdf/2606.14249
