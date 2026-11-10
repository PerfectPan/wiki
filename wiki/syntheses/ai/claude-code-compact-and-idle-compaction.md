---
title: Claude Code compact 与 idle compaction 的成本机制
description: /compact 本质是一轮什么请求、缓存冷热时分别怎么计费，以及 idle compaction 如何在 1 小时缓存过期前自动压缩长会话来对冲全价重读。
type: synthesis
category: ai
created: 2026-11-10
updated: 2026-11-10
timestamp: 2026-11-10
tags:
  - claude-code
  - prompt-caching
  - compaction
  - billing
source_refs:
  - raw/sources/claude-code-prompt-caching-docs.md
  - raw/sources/claude-code-idle-compaction.md
  - raw/sources/claude-code-idle-compaction-dsebastien.md
  - raw/sources/claude-prompt-caching-pricing.md
  - https://code.claude.com/docs/en/prompt-caching
resource:
  - raw/sources/claude-code-prompt-caching-docs.md
  - raw/sources/claude-code-idle-compaction.md
  - raw/sources/claude-code-idle-compaction-dsebastien.md
  - raw/sources/claude-prompt-caching-pricing.md
  - https://code.claude.com/docs/en/prompt-caching
---
# Claude Code compact 与 idle compaction 的成本机制

## 问题

这页回答三个连在一起的问题：

1. 手动 `/compact` 到底怎么收费？它是不是一轮独立的模型请求？
2. 「缓存快过期前提前压缩一下」是不是真的省钱？
3. Claude Code 有没有内置自动做这件事的机制，怎么开关？

## 简答

`/compact` 没有独立计费通道，它就是一轮单独的模型请求：输入是完整对话历史加一条摘要指令，输出是摘要，历史随后被摘要替换。缓存热的时候，这轮请求的长历史走缓存读取价，成本主要是摘要输出；缓存过期后再压缩，整段历史按未缓存输入全价处理，是 compact 最贵的情形。Claude Code v2.1.283 起内置了 **idle compaction（闲置压缩）**：在 1 小时 TTL 的缓存过期前几分钟自动压缩长会话，等于把「提前 compact」这个手动策略产品化了。

## 来源事实

### compact 请求的结构与缓存分层

以下事实来自 Claude Code 官方 prompt caching 文档（`raw/sources/claude-code-prompt-caching-docs.md`）：

- Claude Code 的请求前缀分三层：system prompt、项目上下文（`CLAUDE.md`、auto memory、rules）、对话历史。compact 按设计只让对话历史层失效，前两层可以继续命中缓存。
- 生成摘要时，Claude Code 发一个独立请求，重复发送 system prompt、工具定义和待压缩的历史，末尾加摘要指令。缓存热时这个请求从前缀缓存读取，所以一次会话中途的 `/compact` 成本远低于上下文体量暗示的价格，时间主要花在生成摘要上。
- 闲置时间超过缓存寿命后，没有缓存可读，摘要请求把整段历史当未缓存输入重新处理。官方明确说明：恢复旧会话时执行 compact 成本最高。
- compact 之后的下一轮只为短得多的摘要重建对话层缓存，因此那一轮并不是慢点。
- compact 请求本身不属于主对话的 TTL 桶：subagent、workflow、compaction、会话标题等请求默认都是 5 分钟 TTL，只有订阅额度内的主对话是 1 小时。
- 两个相邻机制的区别：`/recap` 只把摘要作为命令输出追加，不替换历史，缓存前缀保持不变；`/rewind` 把对话截断回更早的轮次，剩余历史正好是当时建缓存的前缀，下一轮直接命中旧缓存，不会像 compact 那样新建前缀。

### idle compaction 的触发条件

以下事实来自 turboai 对 v2.1.314 的梳理（`raw/sources/claude-code-idle-compaction.md`），每个条件必须同时满足：

| 条件 | 默认值 | 调整方式 |
| --- | --- | --- |
| 功能被 Anthropic 远程开关打开 | 默认关，远程放量 | 本地无法强制开启 |
| auto-compaction 未关闭 | 开 | `DISABLE_AUTO_COMPACT`、`DISABLE_COMPACT`、`autoCompactEnabled` |
| idle compaction 未被本地阻止 | 未阻止 | `"idleCompaction": false`（v2.1.290+） |
| 会话使用 1 小时 TTL 缓存 | 订阅额度内的主对话默认是；API key、Bedrock、Vertex、Foundry 默认 5 分钟 | `promptCacheTtl`、`CLAUDE_CODE_PROMPT_CACHE_TTL`、`ENABLE_PROMPT_CACHING_1H` |
| 缓存仍热且前缀未变 | — | 缓存已过期或历史被改过则跳过 |
| 对话大小 | ≥ 200,000 token | `CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS`，低于 100,000 的值会被抬到 100,000 |
| 闲置时长 | 1 小时的 90%，约 54 分钟 | 远程配置，限制在 50%–95%（约 30–57 分钟） |
| 没有在途请求、未接近用量上限 | — | 不满足则跳过 |

5 分钟 TTL 的会话永远不会触发 idle compaction。触发时界面提示 `Compacted while idle, before the prompt cache expired`。v2.1.300 增加第二种模式 compact-on-return：闲置时在后台预写摘要，用户回来发下一条消息时才套用，依赖 `precomputeCompactionEnabled`；`"idleCompaction": false` 会同时关掉两种模式。

版本时间线：

| 版本 | 时间 | 变化 |
| --- | --- | --- |
| v2.1.283 | 2026-09-25 | idle compaction 上线，当时只能靠关闭全部 auto-compaction 来阻止 |
| v2.1.290 | 2026-10-05 | 新增 `idleCompaction` 设置和 `CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS`，发布说明未提及 |
| v2.1.299 | 2026-10-14 | 发布说明首次记录该功能 |
| v2.1.300 | 2026-10-14 | 新增 compact-on-return 模式 |
| v2.1.302 | 2026-10-16 | `/config` 出现 Idle compaction 开关，提示信息附带关闭方法 |
| v2.1.314 | 2026-10-30 | 扩展到 VS Code、Claude Desktop Code 标签页，以及使用 1 小时缓存的 Bedrock、Vertex、Foundry 和网关 |

### 缓存单价背景

缓存读写的具体单价见 [[token-usage-and-billing]]，这里只列推导需要的倍数：5 分钟档写入价是标准输入价的 1.25 倍，1 小时档是 2 倍；缓存读取价多数模型是输入价的 0.1 倍，Opus 5.5、Sonnet 5.5 一档为 0.05 倍。也就是说，同一段长历史，缓存热时读一遍和过期后全价重写一遍，输入成本可以相差 20 倍以上。

## 综合结论

### 1. compact 的账单 = 一次缓存读取（或全价输入）+ 一笔摘要输出

把 compact 当普通 turn 看就不会算错账：

- **缓存热时手动 compact**：长历史按缓存读取价计费（输入价的 0.05–0.1 倍），加上几千 token 的摘要输出。这是 compact 最便宜的形态。
- **缓存过期后 compact（典型场景是恢复旧会话）**：整段历史按未缓存输入全价处理，还要付缓存写入溢价重建缓存。官方文档把这称为 compact 最贵的情形。
- **compact 之后的对话**：历史已被短摘要替换，下一轮只为摘要重建缓存，重建成本很小。

### 2. idle compaction 省钱的本质是「用一轮便宜 turn 换掉一轮昂贵 turn」

以一个 300K token 的会话闲置超过 1 小时为例，对比两条路径：

- 没有 idle compaction：缓存过期，用户回来发一句「继续」，300K token 全部按全价输入重新处理并重建缓存，这是一轮昂贵的 turn。
- 有 idle compaction：第 54 分钟自动发起一轮 compact，300K 历史走缓存读取价，外加摘要输出费；缓存随后正常过期也无所谓，因为用户回来时全价输入的对象只剩短摘要。

净效果是用一轮「缓存读取 + 少量输出」的便宜请求，对冲掉一轮「长历史全价重读」的昂贵请求。会话越长、用户本来就会回来继续，差额越大。它不是免费机制：如果用户不再回来，这轮 compact 的花费就是纯支出，但因为触发点设在缓存过期前几分钟，损失有上限。

### 3. 省钱的对立面是上下文有损

压缩是有损操作，两份来源都强调了同一代价：摘要保留主干，会丢掉早期只提过一次的约束、被否决的方案、精确报错和文件内容。而且 idle compaction 发生在用户不在场时，没有人告诉摘要该重点保留什么。GitHub issue #98747 就是针对早期版本无法关闭该功能的投诉。

### 4. 「提前 compact 续缓存」这个直觉只在离开场景成立

活跃使用时每次缓存命中都会免费续期，TTL 只在闲置时倒计时，所以连续工作中不存在「缓存快过期」的问题，为续期而 compact 反而白白损失上下文并触发前缀重建。真正成立的场景是：知道自己要离开超过 TTL、且任务还没做完，趁缓存热先压缩，让过期后全价重读的对象从长历史换成短摘要——这正是 idle compaction 自动化的策略。

## 对个人/项目的启发

1. **连续干活时不要手动 compact 续缓存**，缓存会自动续期；把 compact 留在任务之间的自然停顿点，官方文档也是这个建议。
2. **默认保持 idle compaction 开启**：多数闲置会话恢复时只是一句「继续」，为长历史付全价不划算。
3. **细节敏感的长会话（深度调试、设计讨论）在离开前手动 `/compact focus on <关键事项>`**，自己指定摘要保留内容；或者直接在 `settings.json` 写 `"idleCompaction": false`（v2.1.290+），接受回来时的全价重读。
4. **折中做法是调高阈值**：设置 `CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS`（如 600000），只让超大会话被自动压缩。注意 `"idleCompaction": true` 不能强制开启，功能由远程开关控制，`true` 只是不阻止。
5. **API key 或云厂商用户**默认只有 5 分钟 TTL，不会触发 idle compaction；需要这个行为要显式设 `"promptCacheTtl": "1h"`，但 1 小时档写入价是 2 倍，只适合间隔 5–60 分钟还会回来的间歇式工作。
6. **想放弃某条探索路径时用 `/rewind` 而不是 `/compact`**：rewind 截断到的前缀本来就在缓存里，下一轮直接命中，不产生新摘要，也不丢截断点之前的上下文。
7. 验证缓存行为可以看响应 usage 里的 `cache_read_input_tokens`、`cache_creation_input_tokens`，1 小时和 5 分钟写入分别对应 `ephemeral_1h_input_tokens` 和 `ephemeral_5m_input_tokens`；账单各分项的定义见 [[token-usage-and-billing]]。

## 相关页面

- [[token-usage-and-billing]]：缓存读写单价、TTL 分档与 transcript 统计方法
- [[kv-cache-vs-request-cache]]：KV Cache 与请求缓存的边界
- [[agent-proactive-context-management]]：阈值式 compact 作为上下文治理兜底手段的局限
- [[claude-5-context-engineering]]：Claude Code 削减系统提示词与延迟加载的上下文工程
- [[code-agent]]

## 来源指针

- `raw/sources/claude-code-prompt-caching-docs.md`：[How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching)（官方文档，compact 请求结构、缓存分层、TTL 桶、idle compaction 开关）
- `raw/sources/claude-code-idle-compaction.md`：[Claude Code "Compacted while idle" guide](https://www.turboai.dev/blog/claude-code-idle-compaction-guide)（触发条件表、配置项、版本时间线）
- `raw/sources/claude-code-idle-compaction-dsebastien.md`：[Claude Code idle compaction - cheaper to resume, but from a summary](https://www.dsebastien.net/2026-10-16-claude-code-idle-compaction-cheaper-to-resume-but-from-a-summary/)（使用代价与配置建议）
- `raw/sources/claude-prompt-caching-pricing.md`：[Anthropic Claude Prompt Caching: Pricing, 5-Min vs 1-Hour TTL](https://www.respan.ai/articles/claude-prompt-caching)（缓存写入与读取的定价倍数）
