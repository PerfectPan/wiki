---
title: KV Cache 与请求缓存的边界
description: 区分 KV Cache、Prompt Cache、请求缓存和普通结果缓存的作用范围、缓存对象和成本边界。
type: synthesis
category: ai
created: 2026-05-24
updated: 2026-05-24
timestamp: 2026-05-24
tags:
  - llm
  - inference
  - cache
  - transformer
source_refs:
  - raw/sources/2026-05-24-kv-cache-request-cache-conversation.md
  - https://x.com/_avichawla/status/2034902650534187503
resource:
  - raw/sources/2026-05-24-kv-cache-request-cache-conversation.md
  - https://x.com/_avichawla/status/2034902650534187503
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

## 未决问题

- 这页还没有展开不同推理框架如何实现 Prefix Cache。
- 后续可以补充 vLLM PagedAttention、DeepSeek MLA、GQA/MQA 的具体内存计算方式。

## 来源指针

- `raw/sources/2026-05-24-kv-cache-request-cache-conversation.md`
- `https://x.com/_avichawla/status/2034902650534187503`
