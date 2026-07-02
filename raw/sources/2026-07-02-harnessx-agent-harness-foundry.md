# 2026-07-02 HarnessX 论文调研

## 来源

- arXiv abstract: https://arxiv.org/abs/2606.14249
- arXiv PDF: https://arxiv.org/pdf/2606.14249
- DOI: https://doi.org/10.48550/arXiv.2606.14249

## 来源事实

- 论文标题为《HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry》，提交于 2026-06-12。
- 论文把 agent harness 定义为模型外层的运行时接口，包括 prompts、tools、memory、control flow，以及模型如何观察、推理、行动的中介机制。
- 论文认为当前 agent harness 主要有三类问题：
  - 手工构造且静态，换模型或任务时需要重新搭脚手架；
  - prompt、tool wrapper、retry policy、memory 等常混在同一路径中，难以组合和复用；
  - harness 改进和模型训练割裂，执行 trajectory 很少被系统性转化为 harness update 或模型训练信号。
- HarnessX 的三块核心：
  - Harness Composition：把 harness 作为一等对象，拆成 typed processors，挂到 task/model/tool lifecycle hooks 上，并通过 substitution algebra 组合。
  - Harness Adaptation：AEGIS 是 trace-driven 的多 agent harness evolution engine，包含 Digester、Planner、Evolver、Critic / gating。
  - Harness-Model Co-Evolution：把 harness 演化产生的 trajectory 作为模型强化学习信号，使用 cross-harness GRPO 和 mixed-policy replay buffer。
- AEGIS 把 symbolic harness adaptation 映射到 RL 问题，指出 reward hacking、catastrophic forgetting、under-exploration 也会出现在 harness 规则和 prompt/tool/control edits 中。
- 实验覆盖 ALFWorld、GAIA、WebShop、tau^3-Bench、SWE-bench Verified，任务 agent 包括 Claude Sonnet 4.6、GPT-5.4、Qwen3.5-9B。
- 论文报告 15 个 model-benchmark 配置中 14 个提升，平均提升 +14.5%，最高 +44.0%。
- 表 4 的关键结果包括：
  - ALFWorld：Qwen3.5-9B 从 53.0 到 97.0，+44.0；GPT-5.4 从 76.9 到 97.8，+20.9；Sonnet 4.6 从 83.6 到 94.8，+11.2。
  - WebShop：三个模型提升 +13.0 到 +18.0。
  - GAIA：Sonnet 4.6 +9.7，Qwen3.5-9B +17.1，GPT-5.4 单 harness stagnates。
  - SWE-bench Verified：Sonnet 4.6 +10.9，GPT-5.4 +18.2，Qwen3.5-9B +18.2。
  - tau^3-Bench 平均：Sonnet +5.4，GPT-5.4 +14.5，Qwen3.5-9B +1.1。
- 论文称 variant isolation 可以缓解 heterogeneous task set 上单一 harness 的相互干扰；co-evolution 在 GAIA 和 WebShop 上比 harness-only 额外增加约 +4.7%。
- 论文限制：
  - 所有 reported gains 都在 adaptation set 上测，没有 held-out evaluation，有 selection bias 和 overfitting 风险；
  - 实验都在 discrete text action space，没有验证 continuous action space；
  - AEGIS 依赖强 meta-agent，开源模型作为 meta-agent 尚未验证；
  - co-evolution 假设能同时控制 harness evolution 和 model training，现实组织里不总成立；
  - SWE-bench Verified 只用了 55-task subsample，tau^3-Bench 只评估 Retail、Airline、Telecom 三个域；
  - 完整代码尚未开源，论文称 future release。

## 初步判断

- 这篇论文的价值不在于具体数字本身，而在于把 agent harness 从手工 prompt/tool glue 升级为可组合、可观测、可演化、可训练反馈的系统接口。
- 它和 Agent Native 系统接口设计、结构化输出可靠性、Agent-native CLI 产物协议属于同一类思想：把模型外部的运行时边界做成低熵、可验证、可回放、可修复的工程层。
- 实验结果需要保守看待，因为没有 held-out set，且 benchmark 子集有限；但“弱模型更吃 harness 红利”这个方向对个人 agent 系统和自动化产品有启发。
