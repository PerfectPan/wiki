# dottxt.ai 与 LLM 结构化输出讨论摘录

- 日期：2026-05-17 至 2026-05-18
- 类型：对话整理
- 主题：dottxt.ai、constrained decoding、结构化输出、OpenAI JSON Schema、商业化边界
- 外部来源：
  - https://dottxt.ai/
  - https://docs.dottxt.ai/api/overview.md
  - https://docs.dottxt.ai/api/models.md

## 原始问题链

用户围绕 dottxt.ai 连续追问：

1. `https://dottxt.ai/ 这网站干啥的`
2. `他咋保证的？`
3. `还是没懂，他能控制 LLM 输出？`
4. `他咋做到的？LLM 不是部署在厂家那边吗？`
5. `他是自己把开源模型套了一下？`
6. `那怎么感觉这个东西没什么壁垒`
7. `那他咋商业化的 以及我要用的话怎么用`
8. `对啊 openai 不是都支持 json schema 输出了么`
9. `他怎么收费的啊 没看到呢`

## 来源事实

- dottxt.ai 官网主张是面向生产 LLM 的结构化输出能力，核心关键词包括 structured outputs、reliable agent infrastructure、NoBadOutputs。
- 其技术方向属于 constrained decoding：在模型每一步生成 token 时，根据 JSON Schema、regex 或 grammar 之类的约束，屏蔽非法 token，只允许模型在合法候选内继续生成。
- 如果推理栈可控，例如自托管开源模型、vLLM、SGLang、TensorRT-LLM，约束解码层可以插入生成循环，直接控制 token 采样空间。
- 如果模型完全由 OpenAI、Anthropic、Google 等闭源 API 托管，第三方通常拿不到 logits，也无法在外部真正介入每一步 token 生成，只能使用厂商开放的 JSON mode、Structured Outputs、function calling 或生成后校验重试。
- dottxt 文档暴露了 API、模型目录和 OpenAI-compatible 接入方式，但当时未看到清晰公开 pricing 页面。官网与文档更像 early access / B2B / 开发者 API 阶段。

## 综合判断

- constrained decoding 能保证输出结构合法，但不能保证事实正确、业务判断正确或工具调用时机正确。
- dottxt 的价值不在“让模型更聪明”，而在“把模型输出关进可验证协议里”。
- 对普通应用开发，OpenAI/Gemini 等厂商自带的 schema / structured output 通常已经够用。
- dottxt 这类工具更适合以下场景：
  - 自托管开源模型；
  - 大批量结构化抽取；
  - 私有化部署；
  - 推理服务商或 Agent 平台；
  - 对输出协议稳定性、吞吐和成本有强要求的企业系统。
- 单看 constrained decoding 原理，壁垒不厚；长期壁垒主要来自复杂 schema 支持、tokenizer/grammar 对齐、高并发性能、streaming、推理框架深度集成和生态位置。
