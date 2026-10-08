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

### 一次请求里的读、写和普通输入

请求按缓存断点（`cache_control`）分成三段：

```text
[ 已缓存的前缀 ][ 新内容，到最后一个缓存断点为止 ][ 断点之后的内容 ]
   cache_read        cache_creation（写缓存）          input_tokens（普通输入）
```

- 读缓存是从开头起与已缓存内容完全一致的最长前缀；写缓存是命中部分之后、到最后一个断点为止的内容，写入后下一次请求即可命中；断点之后的内容按普通输入计费，不进缓存。
- Claude Code 每轮都把新内容写进缓存，普通输入很少：一次多 agent 任务里写缓存 43.3M，普通输入只有 1.2M。
- 模型的回复会被计费不止一次：生成时按 output 计费，下一轮作为历史送回时按写入价写进缓存，之后每轮按读取价重读。工具结果也是送进去时写一次，之后每轮重读。
- 前缀从某处对不上时（缓存过期、切换模型、工具定义变化、压缩对话），从那里开始的内容全部重写。
- 短于模型最小可缓存长度的前缀不会被缓存（Opus 5.5 为 512 token），按普通输入计费。

### 为什么每轮都写缓存

一段内容在之后每轮请求里都会被再送一遍。设它之后还会被送 n 次，按输入价的倍数算：

| | 走缓存（Opus 5.5，5 分钟档） | 不走缓存 |
| --- | --- | --- |
| 第一次 | 写入 1.25 | 1 |
| 之后每次 | 读取 0.05 | 1 |
| 合计 | 1.25 + 0.05n | 1 + n |

n = 1 时已是 1.30 对 2.0。Agent 会话动辄几十到几百轮，早期内容被重读几百次，缓存便宜几十倍：上面那次任务的 1.9B 读缓存实际约 $380，按普通输入算约 $7,600。`DISABLE_PROMPT_CACHING` 只适合排查问题。

走缓存吃亏只有两种情况：写入后再也没被读（例如会话最后一轮的新内容，只多付 25%），以及写入后还没被读就过期（先付写入价，之后整段重写）。前者量很小，后者就是闲置后再叫回大上下文 agent 的代价。

### 完整计价公式

以输入单价 `P_in`、输出单价 `P_out` 为基准，缓存的读和写分开计价，写入再按 TTL 分档：

```text
费用 = 未缓存输入 × P_in
     + 5 分钟档写入 × 1.25 × P_in
     + 1 小时档写入 × 2 × P_in
     + 读缓存 × r × P_in          （r：多数 Claude 模型 0.1，Opus 5.5 为 0.05）
     + 输出（含 thinking）× P_out
```

- **读**：每次请求里已经在缓存中的前缀，即此前积累的整个上下文，按 `r × P_in` 计。
- **写**：每次请求新增的部分（新的工具结果、回复）写入一次，按写入价计；缓存过期后的那次请求要把整个上下文重写一遍，同样按写入价计。
- 单次请求约等于 `P_in × (r × 已缓存上下文 + 写入倍数 × 新写入) + P_out × 输出`。整段重写与读一遍的价格比是写入倍数 ÷ r，Opus 5.5 的 5 分钟档为 1.25 ÷ 0.05 = 25。
- `/cost` 只给写缓存的总量，5 分钟档和 1 小时档的拆分要从 transcript 的 `usage.cache_creation` 汇总。

Opus 5.5（`P_in` = $4/M，`P_out` = $20/M）一次多 agent 任务的实算：

| 项目 | 用量 | 单价（每百万） | 花费 |
| --- | --- | --- | --- |
| 未缓存输入 | 1.2M | $4 | $4.8 |
| 5 分钟档写入（subagent） | 39.8M | $5 | $199 |
| 1 小时档写入（主会话） | 3.5M | $8 | $28 |
| 读缓存 | 1.9B | $0.20 | $380 |
| 输出 | 6.5M | $20 | $130 |
| 合计 | | | 约 $742，与 `/cost` 一致 |

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
