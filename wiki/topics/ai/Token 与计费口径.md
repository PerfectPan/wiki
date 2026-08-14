---
title: Token 与计费口径
description: Token、M/B 数量级、input/output/cache 分项，以及 ccusage 一类本地统计工具该怎么读。
type: topic
category: ai
created: 2026-08-03
updated: 2026-08-03
timestamp: 2026-08-03
tags:
  - llm
  - token
  - billing
  - cache
  - ccusage
source_refs:
  - raw/sources/2026-08-03-llm-101-conversation.md
resource:
  - raw/sources/2026-08-03-llm-101-conversation.md
---
# Token 与计费口径

## 摘要

Token 是模型计费与上下文长度的基本单位。读用量报表时，必须分清 input、output、cache write、cache read，以及 total 是否把 cache 算进去；单位 M/B 与中文「万/亿」也常被混用。

## 关键点

- 粗算：英文约 0.75–1 token/词，中文约 1.5–2 token/字；精确数以各厂 tokenizer 为准。
- 数量级：`1M = 100 万`，`100M = 1 亿`，`1B = 1000M = 10 亿`。
- 计费常见四项：
  - **Input（cache miss）**：新送进模型的未命中前缀
  - **Cache creation / cache write**：写入前缀缓存（部分厂商单独计价，常 ≥ input）
  - **Cache read / cache hit**：命中已有前缀（单价通常远低于 input，常见约 0.1×）
  - **Output**：模型生成（含 thinking 时往往很贵）
- Coding agent 场景下，**cache read 常占 total 的绝大部分**（长会话反复重传 system、工具定义、历史与仓库上下文）。
- `ccusage` 等工具在 **compact 模式**下可能只显示 Input/Output，**隐藏 cache 列**；完整 JSON 里通常有 `cacheReadTokens`、`cacheCreationTokens`、`totalTokens`。
- 经验公式（以 ccusage JSON 为例）：

```text
totalTokens ≈ inputTokens + outputTokens + cacheCreationTokens + cacheReadTokens
```

- **total 很大 ≠ 按 input 全价付完**。高 cache hit 时账单主要由少量 miss input、cache write 与 output 决定。
- 订阅套餐（按 prompt / credits 封顶）与 API 按量是两套账；套餐文档里的「约 xxM tokens/周」是假设条件（模型、cache 率、高峰系数）下的估算，不能和本地 total 直接等同。

## 相关页面

- [[KV Cache 与请求缓存的边界]]
- [[Code Agent]]
- [[大模型 101]]
- [[LLM API 协议选型]]

## 来源指针

- `raw/sources/2026-08-03-llm-101-conversation.md`
