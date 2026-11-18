---
title: KV Cache 与请求缓存的边界
description: 区分单次生成的 KV Cache、跨请求的前缀缓存与结果缓存，并说明 GPT‑6.2 的匹配、计费与排查方式。
type: synthesis
category: ai
created: 2026-05-24
updated: 2026-11-18
timestamp: 2026-11-18
tags:
  - llm
  - inference
  - cache
  - transformer
source_refs:
  - raw/sources/2026-05-24-kv-cache-request-cache-conversation.md
  - https://x.com/_avichawla/status/2034902650534187503
  - https://developers.openai.com/api/docs/guides/prompt-caching
---
# KV Cache 与请求缓存的边界

## 问题

KV Cache、请求缓存、Prompt Cache 和普通结果缓存经常被混在一起。它们到底是不是一回事？为什么 KV Cache 会占显存，又为什么它会成为 LLM 推理服务的核心成本变量？

## 简答

KV Cache 是单次自回归生成过程里的推理中间状态缓存；请求缓存或 Prompt Cache 是跨请求复用相同 prompt 前缀的服务端优化；普通结果缓存则是缓存最终答案。三者都叫缓存，但缓存对象、作用范围和失效条件不同。

## 综合结论

KV Cache 的缓存对象不是最终回答，而是 Transformer attention 里历史 token 的 Key/Value 中间结果。

自回归 LLM 每次只生成下一个 token。生成新 token 时，模型需要让当前 token 关注前面所有历史 token。如果没有 KV Cache，每生成一步都要重新计算历史 token 的 K/V，重复计算会快速膨胀。KV Cache 把历史 K/V 保存下来，后续 decode 步骤只计算新 token，并复用已经保存的历史 K/V。

这解释了一个常见体验：第一 token 往往更慢，后续 token 连续输出更快。第一 token 之前的 prefill 阶段要处理完整 prompt 并建立缓存；缓存建立后，decode 阶段就可以沿着已有中间状态继续生成。

KV Cache 通常放在 GPU 显存里，不是因为“缓存只能放显存”，而是因为 attention 计算发生在 GPU 上，而且每一步都会高频读取历史 K/V。如果把这些中间结果放在主存里，再反复搬到 GPU，数据传输会抵消缓存带来的收益。

请求缓存、Prompt Cache 或 Prefix Cache 是另一层优化。它关注的是多次请求之间是否有完全相同或可复用的 prompt 前缀，例如系统提示词、工具说明、长上下文前缀。如果服务端支持并命中，它可以减少下一次请求的 prefill 成本。它可能复用底层 K/V 结果，但工程语义已经从“单次生成内部缓存”变成了“跨请求前缀复用”。

普通结果缓存又是另一回事。它缓存的是某个输入对应的最终输出，类似业务系统里的 HTTP 缓存、Redis 缓存或搜索结果缓存。它不解决 LLM 逐 token 生成过程中的重复 attention 计算。

## 边界表

| 缓存类型 | 缓存对象 | 作用范围 | 典型命中判断 | 主要收益 | 主要代价 |
| --- | --- | --- | --- | --- | --- |
| KV Cache | 历史 token 的 K/V 中间结果 | 单次请求内部 | 推理引擎内部默认使用，用户通常只能从后续 token 输出速度间接感知 | 减少 decode 重复计算 | 占用显存，随上下文长度和并发增长 |
| Prompt Cache / Prefix Cache | 重复 prompt 前缀的推理中间结果 | 跨请求 | API 返回 cached tokens / cache hit，或相同长前缀的 TTFT 明显下降 | 减少重复 prefill 成本 | 依赖前缀一致性、过期策略和服务端支持 |
| 结果缓存 | 最终答案或业务响应 | 跨请求 | 相同请求直接返回已有结果 | 延迟最低，成本最低 | 容易过期，不适合个性化或动态问题 |

## 工程含义

- 长上下文贵，不只是因为输入 token 多，还因为每层都要为历史 token 保存 K/V。
- 高并发难，不只是因为模型权重大，而是每个活跃请求都会带着自己的 KV Cache。
- GQA、MQA、PagedAttention、MLA 等优化方向，本质上都在减少或更有效管理 KV Cache 的显存压力。
- 线上推理成本不能只看模型参数量，还要看上下文长度、并发、首 token 延迟、decode 速度和缓存管理策略。
- 判断“缓存有没有命中”时，需要先问清楚是哪一种缓存：单次推理内部的 KV Cache、跨请求的前缀缓存，还是最终结果缓存。

## GPT‑6.2：指令位置、缓存断点与推理记录

假设两次独立请求都要总结同一份长文，第一次用中文，第二次用英文。6.2 把 Responses API 的顶层 `instructions` 移到了 `input` 后面：

```text
旧版    [用中文总结] [长文]
        [用英文总结] [长文]

GPT‑6.2 [长文] [用中文总结]
        [长文] [用英文总结]
```

提示缓存匹配的是模型实际接到的前缀。处理长文时，每个 token 的中间状态依赖前文。旧版两份请求在读到长文之前就发生了分歧，6.2 可以共享前面长文的计算。这个区别对独立请求和同会话的续接请求都成立。工具定义、顺序和输出格式等设置也可能改变前缀。[GPT‑6.2 变化](https://developers.openai.com/api/docs/guides/latest-model) · [缓存匹配与请求设置](https://developers.openai.com/api/docs/guides/prompt-caching#which-settings-affect-the-cached-prefix)

### 缓存断点与费用

断点标记一段可复用前缀的结尾。GPT‑5.5 已有按固定 token 间隔生成的自动断点。GPT‑5.6 起支持显式断点，自动模式也改为按合格消息的结尾选点。6.2 沿用这一机制，断点前需要至少 1,024 个可见输入 token。多轮 Agent 可以用自动模式延长前缀。重复处理不同文档时，可在固定规则后加 `prompt_cache_breakpoint: { "mode": "explicit" }`，并将 `prompt_cache_options.mode` 设为 `"explicit"`，这样每次的新文档按普通输入价处理。顶部的工具定义、规则和示例应保持一致，变化频繁的内容放在后面。[各代模型的缓存差异](https://developers.openai.com/api/docs/guides/prompt-caching#summary-of-model-differences)

以 GPT‑6.2 Astra / Sol 的普通输入单价为 1 倍，读缓存为 0.05 倍。写入默认的 30 分钟缓存为 1.25 倍，写入 12 小时缓存为 2.5 倍。两档都是最短保留时间，使用 `prompt_cache_options.ttl` 选择。从 GPT‑5.5 或更早版本迁移时，用该字段代替 `prompt_cache_retention`。如果固定前缀长 2,000 token，写入一次 30 分钟缓存并完整命中一次，前缀的两次总费用相当于 2,600 个普通输入 token，较两次普通输入省 35%。95% 的折扣只适用于命中部分的读取。[保留时间与费率](https://developers.openai.com/api/docs/guides/prompt-caching#cache-lifetime)

### 怎样判断哪里出了问题

| 想确认什么 | 看哪里 | 如何解释 |
| --- | --- | --- |
| 这次复用了多少前缀 | `usage.input_tokens_details.cached_tokens` 与 `cache_write_tokens` | 分别是按缓存读取和写入计费的 token 数。读取折扣与实际延迟分开测。 |
| 为什么突然少命中 | `prompt_cache_options.comparison_response_id` | 指定一条可对比的旧响应，诊断信息会尽力定位第一个差异。 |
| 旧推理条目是否被移除 | `input_transformations` 中的 `prefix_mismatch` | 在 6.2 中，改写早期消息或工具结果可能同时失去缓存与后续推理条目。缓存到期时，仍可用保存下来的推理条目续接。 |

所以维护长会话时，固定早期消息和工具定义，新增结果往后追加。需要调整推理强度时可追加 `configuration_update`，保留原来的顶层 `reasoning.effort`。顶层临时指令的作用范围见 [[responses-api#请求级指令与会话历史]]。[保持前缀不变](https://developers.openai.com/api/docs/guides/keep-prefix-unchanged) · [缓存诊断](https://developers.openai.com/api/docs/guides/prompt-caching/diagnostics)

## 还需要确认什么

- 这页还没有展开不同推理框架如何实现 Prefix Cache。
- 后续可以补充 vLLM PagedAttention、DeepSeek MLA、GQA/MQA 的具体内存计算方式。
