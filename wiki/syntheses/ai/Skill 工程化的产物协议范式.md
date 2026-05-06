---
title: Skill 工程化的产物协议范式
type: synthesis
category: ai
status: seed
created: 2026-05-06
updated: 2026-05-06
tags:
  - agent
  - skills
  - workflow
  - qa
  - provenance
source_refs:
  - raw/sources/2026-05-06-codex-pet-skill-article.md
  - https://mp.weixin.qq.com/s/uH71k1yAoF6xjsOYmVAJBg
---
# Skill 工程化的产物协议范式

## 问题

一个真正有工程价值的 Agent Skill，和普通 prompt wrapper 或轻量 workflow 的区别在哪里？

## 简答

成熟 Skill 的核心不是“让模型换一种说法”，而是先定义可消费的产物协议，再用 manifest 外部化任务状态，用脚本处理确定性编译，用 provenance 约束来源，用 QA 区分结构正确与语义正确，最后通过局部 repair 收敛失败。模型负责生成候选，不应直接拥有最终提交权。

## 综合结论

`hatch-pet` 的启发不在于 Codex 宠物本身，而在于它把一个看似主观的图像生成任务，改造成了可审计的资产流水线。用户输入只是 intent，最终交付却是 Codex app 能加载的 `pet.json` 与 `spritesheet.webp`。中间经过 request、job manifest、生成候选、来源记录、确定性编译、QA、局部修复和打包。

这说明 Skill 的价值边界应当从“提示模型怎么做”上移到“定义产物如何被验证和消费”。如果一个 Skill 只包含人格设定或几段 instructions，它最多是 prompt 模板；如果它定义了产物契约、状态机、工具边界、验收标准和失败修复路径，它才开始接近工程组件。

`hatch-pet` 展示了几条可迁移原则：

- **模型输出是生产材料，不是最终成果。** 图像模型可以生成 base pet 和 row strips，但只有经过记录、抽帧、拼 atlas、验证和打包后，才成为可加载资产。
- **关键状态必须外部化。** 长任务不能靠模型上下文记忆进度，`imagegen-jobs.json` 这类 manifest 才能承载依赖、输入、输出、来源、hash、派生规则和完成状态。
- **并行不等于共享提交权。** 子代理可以生成候选和写 QA note，但不能修改 manifest、record、finalize、repair 或 package；父代理作为 control plane 统一提交 truth。
- **确定性脚本应承担编译器角色。** 抽帧、透明背景检查、尺寸校验、hash 校验、spritesheet 组装和打包都不该让模型自由发挥。
- **QA 要分结构层和语义层。** schema、尺寸、alpha、帧数、空 cell 可以自动验证；身份一致性、状态语义和视觉质量仍需要视觉检查。
- **repair 优于 retry。** 失败时重开最小失败范围，保留已通过部分，比整套重跑更稳定、更便宜，也更符合生产系统的维护方式。

这套范式也能迁移到代码、UI、文档、知识库、数据处理和自动化运营任务。凡是输出物要长期复用，就应该问：

1. 最终产物的消费协议是什么？
2. 哪些步骤是模型生成，哪些步骤必须确定性执行？
3. 任务状态是否写在外部 manifest 中？
4. 来源、hash、依赖和完成状态是否可审计？
5. QA 是否同时覆盖结构正确和语义正确？
6. 失败后能否局部 repair，而不是只能整体 retry？

## 和 workflow 的关系

传统 workflow 擅长确定性链路，适合触发器、节点、固定分支和清晰输入输出。但当任务需要上下文理解、动态决策、候选筛选、多代理协作和局部修复时，画死节点图会越来越重。

Skill 更适合承载“半结构化生产流程”：协议和边界是硬的，执行路径可以由 Agent 根据状态选择。也就是说，成熟 Skill 不是 workflow 的反面，而是把 workflow 的确定性部分收进脚本和 manifest，把不确定的语义判断留给模型。

## 对 AgentOS / control plane 的启发

这篇文章最值得保留的判断是：Agent 系统的稳定性不靠更多 prompt，而靠协议、manifest、provenance、编译器、QA 和 repair。

可以把成熟 Skill 抽象成一条生产链：

```text
intent
-> request
-> job manifest
-> generated candidates
-> recorded provenance
-> compiled artifact
-> QA result
-> targeted repair
-> packaged asset
```

这条链路把模型关进工程边界里。创意层可以开放，协议层必须收紧；worker 可以并行，提交权必须集中；结构可以自动验，语义要单独看；失败可以重试，但更应该能定位和修复。

## 未决问题

- `hatch-pet` 依赖图像生成质量，Skill 只能降低漂移，不能彻底消除视觉不一致。
- 这种范式会增加脚本、manifest 和 QA 成本，不适合一次性小任务。
- 子代理并行会增加 token 和额度消耗，只有任务天然可并行且产物需要严格验收时才划算。
- `/goal` 这类目标驱动机制如果和 manifest / QA 结合，可能成为长任务持续推进的控制环，但仍需要明确完成证据和停止条件。

## 来源指针

- `raw/sources/2026-05-06-codex-pet-skill-article.md`
- https://mp.weixin.qq.com/s/uH71k1yAoF6xjsOYmVAJBg
