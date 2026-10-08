---
title: Token 与计费统计标准
description: Token、M/B 数量级、input/output/cache 分项，缓存保留时间与计价，以及 ccusage、Claude Code transcript 一类本地统计该怎么读。
type: topic
category: ai
created: 2026-08-03
updated: 2026-10-08
timestamp: 2026-10-08
tags:
  - llm
  - token
  - billing
  - cache
  - ccusage
source_refs:
  - raw/sources/2026-08-03-llm-101-conversation.md
  - raw/sources/claude-code-multi-agent-token-audit.md
  - https://code.claude.com/docs/en/prompt-caching
  - https://platform.claude.com/docs/en/about-claude/pricing
resource:
  - raw/sources/2026-08-03-llm-101-conversation.md
  - raw/sources/claude-code-multi-agent-token-audit.md
  - https://code.claude.com/docs/en/prompt-caching
  - https://platform.claude.com/docs/en/about-claude/pricing
---
# Token 与计费统计标准

## 摘要

Token 是模型计费与上下文长度的基本单位。读用量报表时，要分清 input、output、cache write、cache read，以及 total 是否把 cache 算进去；单位 M/B 与中文「万/亿」也常被混用。Agent 场景下，每次模型请求都会把整个上下文重新送一遍，花费约等于上下文大小乘以请求次数；缓存命中率高只说明单价低，不说明总价低。

## 关键点

### 单位与分项

- 粗算：英文约 0.75–1 token/词，中文约 1.5–2 token/字；精确数以各厂 tokenizer 为准。
- 数量级：`1M = 100 万`，`100M = 1 亿`，`1B = 1000M = 10 亿`。
- 计费常见四项：
  - **Input（cache miss）**：新送进模型、没有命中缓存的部分
  - **Cache write / cache creation**：把前缀写入缓存。Anthropic 按缓存保留时间（TTL）分两档：5 分钟档为输入价的 1.25 倍，1 小时档为 2 倍
  - **Cache read / cache hit**：命中已有前缀。单价按模型而定：多数 Claude 模型为输入价的 0.1 倍，Opus 5.5 为 0.05 倍（$0.20/M）
  - **Output**：模型生成，thinking 按 output 计费
- `ccusage` 等工具在 **compact 模式**下可能只显示 Input/Output，**隐藏 cache 列**；完整 JSON 里通常有 `cacheReadTokens`、`cacheCreationTokens`、`totalTokens`。
- 经验公式（以 ccusage JSON 为例）：

```text
totalTokens ≈ inputTokens + outputTokens + cacheCreationTokens + cacheReadTokens
```

### 读缓存量大时仍是账单大头

- 每次请求都重读整个上下文，所以 cache read 常占 total 的 95% 以上。单价低不代表可以忽略：一次 Opus 5.5 多 agent 开发任务中，命中率 97.8%，账单 $742 里读缓存仍占 51%，写缓存 31%，输出 18%，未缓存输入不到 1%。
- 命中率 = cache read ÷（cache read + cache write + 未缓存 input）。它衡量前缀有没有被复用，不衡量花了多少。降低总价要靠缩小每次请求的上下文、减少请求次数，以及避免缓存过期后的整段重写。

### 缓存保留时间（TTL）

- 缓存在闲置超过 TTL 后过期；每次读取会重新计时，所以连续工作的会话不会过期。
- 过期后的下一次请求要按写入价把整个上下文重写一遍。Opus 5.5 上 5 分钟档的重写相当于同样内容读 25 次；上下文越大，过期一次越贵。
- TTL 越长不一定越省：1 小时档的每一笔写入都更贵，只有闲置 5～60 分钟后还会接着用的上下文才划算。
- Claude Code 的默认值：主会话在订阅额度内用 1 小时，用 usage credits、API key 或云厂商时用 5 分钟；subagent、workflow、teammate、fork 一律 5 分钟。可用 `promptCacheTtl`、`subagentPromptCacheTtl` 或 subagent frontmatter 的 `experimental.cacheTtl` 修改，详见 [官方文档](https://code.claude.com/docs/en/prompt-caching)。
- 每次响应的 `usage.cache_creation` 分 `ephemeral_5m_input_tokens` 和 `ephemeral_1h_input_tokens` 两档，用来确认一次请求实际用了哪个 TTL。

### 从 Claude Code transcript 统计

- 主会话在 `~/.claude/projects/<项目>/<会话 id>.jsonl`，subagent 在同名目录下的 `subagents/agent-*.jsonl`，每条 assistant 记录带 `message.usage`。
- 同一次请求的流式输出会写成多行、带相同的 usage，统计前按 `message.id` + `requestId` 去重，否则会多算近一倍。
- transcript 里的 `output_tokens` 明显偏低（一次实测 0.7M，`/cost` 为 6.5M），输出量和金额以 `/cost` 为准；input、cache read、cache write 与 `/cost` 一致。

### 订阅与按量

- **total 很大 ≠ 按 input 全价付完**，按价格拆分后再判断花在哪里。
- 订阅套餐（按 prompt / credits 封顶）与 API 按量是两套账；套餐文档里的「约 xxM tokens/周」是假设条件（模型、cache 率、高峰系数）下的估算，不能和本地 total 直接等同。官方没有公布 cache read、cache write 在订阅额度里的换算方式。

## 相关页面

- [[kv-cache-vs-request-cache]]
- [[model-usage-and-gotchas]]
- [[code-agent]]
- [[llm-101]]
- [[chat-completions-vs-messages-vs-responses]]

## 来源指针

- `raw/sources/2026-08-03-llm-101-conversation.md`
- `raw/sources/claude-code-multi-agent-token-audit.md`（多 agent 任务的账单拆分与 transcript 统计）
- [How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching)
- [Claude 价格](https://platform.claude.com/docs/en/about-claude/pricing)
