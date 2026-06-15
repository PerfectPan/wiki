---
title: LLM 结构化输出的可靠性边界
type: synthesis
category: ai
status: seed
created: 2026-05-18
updated: 2026-05-18
tags:
  - llm
  - structured-output
  - constrained-decoding
  - inference
  - agent
source_refs:
  - raw/sources/2026-05-18-dottxt-structured-outputs-conversation.md
  - https://dottxt.ai/
  - https://docs.dottxt.ai/api/overview.md
  - https://docs.dottxt.ai/api/models.md
---
# LLM 结构化输出的可靠性边界

## 问题

LLM 结构化输出工具能“保证”什么？像 dottxt.ai 这类 constrained decoding 工具，和 OpenAI / Gemini 自带的 JSON Schema、Structured Outputs 有什么区别？

## 简答

结构化输出工具主要保证**形式可靠性**，不是保证事实可靠性。constrained decoding 的核心是在生成过程中限制下一步 token 的合法集合，让模型只能在 JSON Schema、regex 或 grammar 允许的空间里继续生成。它能减少解析失败、字段缺失和格式漂移，但不能保证内容真实、业务判断正确，或工具调用时机正确。

## 来源事实

dottxt.ai 的定位是生产 LLM 的结构化输出基础设施。它强调 structured outputs、reliable agent infrastructure、NoBadOutputs，并提供 API、模型目录和 OpenAI-compatible 的接入方式。

这类系统真正能“控制输出”的前提，是它能进入推理层：模型每生成一个 token 前，推理服务会先得到候选 token 的概率分布；约束解码层根据当前 schema / grammar 状态，把非法 token mask 掉，只允许模型在合法 token 里选择。

如果模型部署在自托管推理栈里，例如开源模型配合 vLLM、SGLang、TensorRT-LLM，这个控制点是可用的。如果模型完全由 OpenAI、Anthropic、Google 等闭源 API 托管，外部服务通常拿不到 logits，也无法直接插入 token 生成循环，只能使用厂商自身提供的 JSON mode、Structured Outputs、function calling，或退化为生成后校验与重试。

## 综合结论

constrained decoding 解决的是“模型输出能不能被程序稳定消费”的问题。它不是让模型更聪明，而是把模型的表达限制在可验证协议里。

这对 Agent 和自动化系统很关键。因为生产系统里最常见的失败并不总是模型完全答错，而是模型输出了一个人类能看懂、机器不能稳定解析的半结构文本：JSON 少逗号、字段名漂移、枚举值不在约定内、函数参数缺字段、数组层级错位。约束解码把这些失败从“生成后补救”前移到了“生成中禁止”。

但边界也很清楚：

- 它能保证 `age` 是数字，不能保证年龄没编。
- 它能保证 `status` 只能是约定枚举，不能保证状态判断正确。
- 它能保证工具参数符合 schema，不能保证这个工具本来就该被调用。
- 它能降低解析失败率，不能替代事实校验、权限判断、业务规则校验和人工验收。

所以结构化输出更像类型系统或协议层，而不是事实验证系统。

## 和厂商 Structured Outputs 的关系

对普通应用开发，优先使用模型厂商自带的结构化输出能力通常更现实：

- 接入成本低；
- 不需要维护推理服务；
- 能直接和当前模型能力、上下文窗口、计费体系绑定；
- 对表单抽取、简单分类、工具参数生成已经够用。

第三方 constrained decoding 工具的价值更偏底层基础设施，适合以下场景：

- 自托管开源模型，希望在本地或私有云保证输出协议；
- 大批量结构化抽取，对失败重试成本敏感；
- 推理服务商或 Agent 平台，需要把结构化输出作为基础能力提供；
- 企业私有化部署，不能或不想依赖闭源厂商的 schema 能力；
- 需要在 vLLM / SGLang / TensorRT-LLM 等推理栈里深度集成。

换句话说，OpenAI / Gemini 的 schema 能力更像“成品模型 API 的一部分”；dottxt 这类工具更像“可控推理栈里的可靠输出层”。

## 壁垒判断

单看 constrained decoding 的原理，壁垒不厚：把规则编译成状态机，在每一步生成前 mask 非法 token。这个思路不神秘，也容易被大模型厂商吸收。

真正的壁垒在工程细节和生态位置：

- JSON Schema、regex、CFG grammar 的复杂兼容；
- tokenizer 与 grammar 状态的边界处理；
- 字符串转义、多语言文本、嵌套数组、optional 字段等脏细节；
- streaming 输出下的状态推进；
- 高并发、批量推理和吞吐损耗控制；
- 与 vLLM、SGLang、TensorRT-LLM 等推理框架的集成深度；
- 是否能成为自托管模型和推理服务商的默认组件。

如果只卖“JSON 不出错”，空间容易被厂商原生能力挤压。如果能卡进开源推理生态和企业私有化链路，它才可能从单点工具变成基础设施组件。

## 使用建议

当前选型可以按层次判断：

1. **普通业务应用**：先用 OpenAI / Gemini / Claude 等厂商自带 schema、JSON mode 或 function calling。
2. **输出失败成本高但仍用闭源 API**：在厂商 schema 基础上增加业务校验、重试、兜底和人工审核。
3. **自托管模型或大批量抽取**：再考虑 dottxt 这类 constrained decoding 层，重点评估吞吐、schema 支持范围、失败率和运维成本。
4. **Agent 平台或推理服务商**：把结构化输出视为协议能力，而不是 prompt 技巧；它应该和工具权限、状态机、日志、评估、回放一起设计。

## 未决问题

- dottxt.ai 当时未看到公开透明的 pricing，商业化状态更像 early access / B2B / 开发者 API 阶段。
- 厂商原生 Structured Outputs 的能力会持续增强，第三方工具需要靠自托管生态、性能和集成深度保持位置。
- 结构化输出降低的是协议失败，不是语义失败；用于高风险业务时仍需要独立校验和审计。

## 来源指针

- `raw/sources/2026-05-18-dottxt-structured-outputs-conversation.md`
- https://dottxt.ai/
- https://docs.dottxt.ai/api/overview.md
- https://docs.dottxt.ai/api/models.md
