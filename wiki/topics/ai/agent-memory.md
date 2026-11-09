---
title: Agent Memory
description: 理解智能体如何跨会话保留经验，以及记忆选择、检索和纠错之间的关系
type: topic
category: ai
created: 2026-11-08
updated: 2026-11-08
timestamp: 2026-11-08
tags:
  - agent
  - memory
  - context-engineering
source_refs:
  - raw/sources/anthropic-components-of-agent-memory.md
  - https://www.anthropic.com/research/components-of-agent-memory
resource:
  - raw/sources/anthropic-components-of-agent-memory.md
  - https://www.anthropic.com/research/components-of-agent-memory
---

# Agent Memory

## 摘要

Agent Memory 是智能体将过去任务中的信息保存在当前会话之外，并在后续任务中取回、使用和修订的机制。本文讨论的是外部记忆：日志、笔记和知识页面等持久记录，而不是通过训练修改模型权重。

单会话上下文学习只利用当前输入中的信息，不保证会话结束后仍能使用。摘要或压缩可以减少文字，但若没有跨会话保存与取回，就还没有形成这里所说的记忆。反过来，记忆也不一定经过压缩，能够检索的原始日志就可以构成基础。后一点见 [[raw/sources/anthropic-components-of-agent-memory#Thinking backward, looking forward|文章结尾讨论]]；上述边界是本文为解释外部记忆采用的定义。

本页按记忆的生命周期组织：写入时记什么、以什么形式保存、离线怎样整理、需要时怎样取回，以及成效如何评估。字段、接口和操作层面的设计见 [[wiki/syntheses/ai/agent-memory-implementation|如何实现 Agent Memory]]。

## 记什么：记忆是对未来有用性的预测

一条记忆被写下，是因为预期未来还会遇到相关问题。价值不取决于保存了多少文字，而取决于它是否让后续任务少做重复推导、少犯已知错误。这个理解对应文章的 [[raw/sources/anthropic-components-of-agent-memory#Memory can be a prediction about what the future will need|记忆作为预测]]。

**在这个预测下，优先保存已经推导、验证过的规则、失败原因和决策依据，而不是下一轮就能重新读取的状态。**

容易重新读取的状态与难以重新推导的知识，保存价值不同。当前文件列表可以重新扫描，依赖不能升级的原因却可能需要重做调查。放到编程任务里，少记“刚改了哪些文件”，多记“为什么必须这样改，以及怎样验证”。项目决定的理由、已验证的操作规则、失败的复现条件和成功路径，都可能值得保留。任务进度也有交接价值，但临时状态不因此成为长期规则。这些是本文据此作出的判断，不是实验已经验证的通用筛选公式；保存对象的具体分类见 [[wiki/syntheses/ai/agent-memory-implementation|如何实现 Agent Memory]]。

文章中的三个案例从不同侧面说明“记什么”：

- **保存内容存在选择差异。** Pokémon 案例中，一个模型大量保存屏幕可见状态，另一个更偏向保存目标、策略和规则。这说明“记什么”值得关注，但两者使用不同模型，且各只展示一次运行，不能推断少记文件导致成绩更好。见 [[raw/sources/anthropic-components-of-agent-memory#Claude has learned to judge salience|记忆选择案例]]。
- **“只记录失败”不是好的筛选规则。** 文章在较强模型上观察到，这条限制反而削弱了记忆增益，成功经验同样可能有用。见 [[raw/sources/anthropic-components-of-agent-memory#Steering Claude to write memory|记忆指令实验]]。
- **未经检验的猜测不应直接当成规则保存。** CL-Bench 案例区分了留下未经检验的猜测，与检验假设后再保存规则两种做法。见 [[raw/sources/anthropic-components-of-agent-memory#Memory can be a prediction about what the future will need|假设检验案例]]。

预测可能出错。保存下来的推测不自动成为事实，过去正确的规则也可能因版本或环境变化而过时。因此，本文认为一条经验除了结论，还需要能辨认其来源、验证状态和适用范围，避免把一次观察扩展成所有场景的规则。依据见前述假设检验案例及 [[raw/sources/anthropic-components-of-agent-memory#Thinking backward, looking forward|过时与维护问题]]。

## 记忆的形式与层级：日志、笔记、Wiki 与常驻索引

这些记录不是互相替代的产品，而是承担不同作用的知识形式：

- 原始日志保存当时的消息、观察和工具结果，是追查结论怎么来的依据。日志也可能包含误判，不等于外部世界的真相。
- 笔记保存从经历中选出的结论、计划或经验，便于下一次使用，也因此带入了记录者的判断。
- Wiki 将分散笔记和资料组织成主题与关系，减少每次从头跨文档整理的工作。
- 常驻索引是每次会话预先加载的少量规则和导航，帮助智能体知道哪些知识存在、去哪里查。它不需要装下全部记忆。

这是本文对文章中不同记忆形式的归纳。一次任务结束后，日志可以被提炼成笔记，笔记与资料可以被组织进 Wiki，少量稳定内容或入口可以进入常驻索引。后续任务从入口定位相关内容，再检索和回查来源。整理发现错误时，修订的是已有记忆，而不是把旧结论继续当作依据。相关机制见 [[raw/sources/anthropic-components-of-agent-memory#Dreaming can build new memory representations|Wiki 构建]]和 [[raw/sources/anthropic-components-of-agent-memory#Dreaming can promote notes up the memory hierarchy|记忆层级]]。

常驻不意味着一定有用：预先加载会占用上下文，错误也会随每次会话进入模型，模型读到后仍可能不遵循。因此索引承担的是有限的导航和提醒作用，不是将所有知识强行装进当前上下文。

## 离线整理（dreaming）：回查证据并修订记忆

文章把离线检查日志、修订笔记和维护知识结构的过程称为 dreaming。它可以在当前任务之外完成，但增加一轮总结本身不等于纠错。

Mt. Moon 案例中，错误的 PokéCenter 方位笔记让模型反复走旧路线。离线整理对照会话记录发现错误并改写笔记，随后该运行抵达 Cerulean City。这个案例说明了回查来源如何纠错，不证明所有记忆错误都能自动修复。见 [[raw/sources/anthropic-components-of-agent-memory#Dreaming can correct memory|纠错案例]]。

本文据此认为，整理的关键问题是“证据是否支持这条结论”，而非“能否写出更短的摘要”。摘要套摘要没有增加独立依据，反而可能丢掉原本用于质疑结论的条件。来源本身仍须判断：日志里的模型猜测与工具观察不能不加区别地当作事实。维护还要付出计算成本，何时整理、何时复查过时内容没有统一答案。

## 怎样取回：记忆与搜索互补

搜索让智能体在需要时找到记录，Wiki 等记忆形式则提前组织知识，保留已经完成的关联与推导。搜索原始日志可以是记忆系统的一部分，因而“记忆还是搜索”并不是非此即彼的问题。

[Anthropic 记忆实验][anthropic-memory] 图 10 让 Opus 5 基于内部资料构建 Wiki，再用 25 道问题评估：仅搜索满足评分标准的比例为 53%，Wiki 加搜索在构建会话增多后达到 61%。这是特定评测中两种使用方式的比较，不是通用正确率。Wiki 加搜索每题约节省 20,000 token，但构建和维护 Wiki 的开销也必须计算。另一项以单份文档检索为主的任务没有显示明显增益。见 [[raw/sources/anthropic-components-of-agent-memory#Dreaming can build new memory representations|评测设置与边界]]。

据此，本文将 Wiki 的作用理解为复用知识组织，而非取代证据搜索。涉及跨文档关系的任务可能受益，直接查一份文档就能解决的问题未必需要额外整理。

## 成效评估的边界：模型能力与记忆系统分开看

记忆系统提供可复用的信息，模型仍要判断什么值得记、结论是否成立、何时检索以及怎样使用。保存成功不等于下次能找到，找到也不等于能正确执行。因此，换一个更强模型后的成绩不能全部算作记忆机制的收益，文件更少也不能直接作为质量指标。

前述 CL-Bench 中，同一模型在无状态与有记忆条件下的对比，比跨模型展示更接近回答“这项任务是否从记忆获益”。它仍只支持该任务条件下的结论，不能推广成所有工作的保证。具体设置见 [[raw/sources/anthropic-components-of-agent-memory#Memory can be a prediction about what the future will need|CL-Bench 记录]]。

本文据此认为，衡量记忆系统需要尽量固定模型、工具和预算，分清原始记录搜索、整理后的知识及离线维护各自带来的变化。最终看任务结果、重复错误和总成本，而非只看文件数或前台 token。

本文的实验证据全部来自上述 Anthropic 文章的指定版本，没有独立复现实验，也未核查网页最新版本；Pokémon 等案例多为单次运行，只能用来说明机制，不能当作通用结论。资料范围与逐条证据边界见 [[raw/sources/anthropic-components-of-agent-memory|阅读证据与资料范围]]。

## 相关页面

- [[wiki/syntheses/ai/agent-memory-implementation|如何实现 Agent Memory]]：采集、存储、修订、撤回和验收的实现方法。
- [[wiki/comparisons/ai/agent-memory-approaches|Agent 记忆方案对比]]

## 来源指针

- [Anthropic 记忆实验][anthropic-memory]
- [[raw/sources/anthropic-components-of-agent-memory|阅读证据与资料范围]]

[anthropic-memory]: https://www.anthropic.com/research/components-of-agent-memory
