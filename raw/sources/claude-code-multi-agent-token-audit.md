# Claude Code 多 agent 任务的 token 账单复盘

- 记录日期：2026-10-08
- 场景：用 Claude Code（Opus 5.5，1M 上下文）当协调者，派多个 subagent 写代码、派 reviewer subagent 审查，完成一个公开 TypeScript monorepo 的多阶段开发，约一天。
- 数据来源：本机 `~/.claude/projects/<项目>/<会话 id>.jsonl`（主会话）和同名目录下 `subagents/agent-*.jsonl`（subagent）里每次请求记录的 `message.usage`；会话结束时 `/cost` 的汇总；官方文档与价格页。
- 本文件是对话中统计结果的摘录，不是 transcript 副本。

## `/cost` 汇总

```text
Total cost:            $742.04
claude-opus-5-5:  1.2m input, 6.5m output, 1.9b cache read, 43.3m cache write, 63 web search ($740.62)
claude-haiku-4-5: 392.9k input, 17.4k output, 0 cache read, 751.5k cache write ($1.42)
Prompt cache (main): 2059 requests · 99% of input tokens from cache · 10 misses
```

## 按价格拆分

Opus 5.5 价格（每百万 token）：输入 $4，输出 $20，读缓存 $0.20，5 分钟写缓存 $5，1 小时写缓存 $8。读缓存是输入价的 5%，不是其他模型常见的 10%。

| 项目 | 用量 | 花费 | 占比 |
| --- | --- | --- | --- |
| 读缓存 | 1.9B | 约 $378 | 51% |
| 写缓存 | 43.3M（subagent 5 分钟档 39.8M，主会话 1 小时档约 3.5M） | 约 $227 | 31% |
| 输出（含 thinking） | 6.5M | $130 | 18% |
| 输入、搜索、Haiku | — | 约 $7 | 1% |

## transcript 统计

- 去重：同一次请求的流式输出会写成多行，每行带相同的 `usage`。按 `message.id` + `requestId` 去重后原始 token 为 1.92B；不去重会算成 3.46B。
- 输出被低估：transcript 里记录的 `output_tokens` 合计约 0.7M，`/cost` 是 6.5M。按 transcript 统计输出会严重偏低，输出以 `/cost` 为准。
- 请求数与上下文：5,679 次请求，平均每次上下文 338k。粗算若每次上下文不超过 200k，同样的请求约 0.98B，是实际的一半。
- 命中率：读缓存 ÷（读缓存 + 写缓存 + 未缓存输入）= 97.8%（主会话 99.1%，subagent 97.4%）。命中率很高，账单仍然大，因为花费约等于上下文大小乘以请求次数。
- TTL：`usage.cache_creation` 里分 `ephemeral_5m_input_tokens` 和 `ephemeral_1h_input_tokens` 两档。主会话的写入全部是 1 小时档；这台机器上所有 subagent 的写入（157M）全部是 5 分钟档，1 小时档为 0。
- 整段重写：一次请求写入超过 100k、读取不到写入的 30%，视为缓存过期后的整段重写。subagent 因此花了约 $130，主会话约 $18，合计约占总额 20%。间隔 5～60 分钟后发生的 56 次 subagent 重写里，52 次发生在协调者用 SendMessage 叫回闲置 subagent 时，4 次发生在单个工具运行超过 5 分钟后。主会话的 3 次大重写前都有 107～135 分钟空档，其中两次前一条是额度用完的报错记录。
- 后续轮次：同一个 subagent 被叫回做的后续轮次（修 review 问题、rebase、补发报告、额度恢复后继续）输入侧花费 $298，比各自第一轮的 $203 还多；后续轮次开始时上下文多在 400k～900k。
- 按角色（输入侧 $603）：写代码的 subagent $390，主会话 $102，reviewer $74，subagent 再派的调研 agent $37。
- 反事实估算：若 subagent 全用 1 小时缓存，省下的重写减去更高的写入单价，净省约 $50；只给 reviewer 用 1 小时缓存，净省约 $12。

## 官方文档要点

[How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching)：

- TTL 按请求分两类。主会话（交互轮次、`-p`、Agent SDK）在订阅额度内默认 1 小时；使用 usage credits、API key 或云厂商时默认 5 分钟。subagent、workflow、in-process teammate、fork、压缩、生成标题等其他请求一律默认 5 分钟。
- 可以自己指定：主会话用 `promptCacheTtl` 或 `CLAUDE_CODE_PROMPT_CACHE_TTL`；其他请求用 `subagentPromptCacheTtl` 或 `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL`（v2.1.242 起）；单个 subagent 可在定义文件 frontmatter 写 `experimental: { cacheTtl: 1h }`（v2.1.248 起）。取值只能是 `5m` 或 `1h`。
- 优先级：`FORCE_PROMPT_CACHING_5M=1` → 该类请求的环境变量 → 该类请求的设置 → subagent frontmatter → `ENABLE_PROMPT_CACHING_1H=1` → 默认值。
- 每次读取会重新计时；只有闲置超过 TTL 才会过期。
- 验证方法：看响应 `usage.cache_creation` 的两个字段。

[Claude Opus 5.5 价格](https://platform.claude.com/docs/en/about-claude/pricing)：输入 $4、输出 $20、读缓存 $0.20、5 分钟写入 $5、1 小时写入 $8（每百万 token）。

订阅额度：官方没有公布读缓存、写缓存在 5 小时和每周额度里的换算方式。文档说明超额改用 usage credits 后主会话会降到 5 分钟缓存，并提示长时间闲置的大会话恢复时会消耗大量额度。

## 社区数据（未经官方确认）

- [anthropics/claude-code#74318](https://github.com/anthropics/claude-code/issues/74318)：把所有 subagent 改为 1 小时缓存后总花费上升 8.6%，因为大多数缓存复用发生在上一次请求后几十秒内。
- [anthropics/claude-code#99808](https://github.com/anthropics/claude-code/issues/99808)：约 3% 的 subagent 轮次与上一轮间隔超过 5 分钟，却占 subagent 缓存写入的约 78%。
