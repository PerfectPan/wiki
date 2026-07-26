---
title: Claude 5 上下文工程新规则
description: Thariq 在 X Article 中总结 Claude 5 时代系统提示词、CLAUDE.md、Skills、工具接口与参考物的设计变化
created: 2026-07-25
updated: 2026-07-25
source_refs:
  - https://x.com/trq212/status/2080710971228918066
---

# Claude 5 上下文工程新规则

## 来源

- 作者：Thariq（`@trq212`，Claude Code 团队）
- 标题：The new rules of context engineering for Claude 5 models
- 发布日期：2026-07-25
- 链接：<https://x.com/trq212/status/2080710971228918066>

## 来源事实

- 作者把 prompt 视为完整上下文的一小部分；系统提示词、Skills、`CLAUDE.md`、memory 和其他来源共同构成 context engineering。
- 团队称，面向 Claude Opus 5 和 Claude Fable 5 等新模型，他们删除了 Claude Code 系统提示词的 80% 以上，在内部 coding evaluations 上没有观察到可测损失。
- 团队在内部使用记录中发现，同一次请求可能同时收到“按需补文档”和“不要添加注释”等冲突信息。新模型通常仍能推断用户意图，但需要额外处理这些重叠约束。
- 文章总结了六组变化：
  1. 从给出大量规则，转向让模型结合周边上下文判断；
  2. 从给工具调用示例，转向设计表达力更好的接口；
  3. 从一次性前置所有信息，转向渐进式披露；
  4. 从跨层重复指令，转向简洁且职责明确的工具描述；
  5. 从把记忆塞进 `CLAUDE.md`，转向自动记忆；
  6. 从简单 Markdown 规格，转向代码、测试、HTML artifact、rubric 等高保真参考物。
- Claude Code 把验证和代码审查等非全程必需的信息拆进独立 Skills，并使用 deferred loading，让工具定义在需要时才进入上下文。
- 对 `CLAUDE.md` 的建议是保持轻量：简述仓库用途，主要记录无法从仓库结构直接推断的 gotchas；更详细的验证方法等内容应拆成按需加载的 Skill。
- 对 Skills 的建议是把它们视为帮助 Claude 按需找到信息的轻量指南，重点编码个人、团队或产品特有的观点、知识与实践；长 Skill 应通过多文件结构实现渐进式披露。
- 对 references 的建议是优先提供高保真材料。文章认为，代码、测试套件和 HTML mockup 往往比文字描述或截图更明确。
- 文章提到 Claude Code 的 `/doctor` 可用于检查和精简 Skills 与 `CLAUDE.md`。

## 备注

“删除 80% 以上系统提示词且评测无损”是作者披露的内部结果。原文没有给出评测集、统计细节或外部复现实验，因此更适合视为产品团队的一手经验，而不是可直接泛化到所有模型和 Agent 系统的定律。
