---
title: Agent-native 生成型 CLI 的产物协议
type: synthesis
category: ai
created: 2026-05-31
updated: 2026-05-31
tags: [agent, cli, automation, artifacts]
source_refs:
  - raw/sources/2026-05-31-vercel-ai-cli-research.md
  - https://github.com/vercel-labs/ai-cli
  - https://www.npmjs.com/package/ai-cli
---

# Agent-native 生成型 CLI 的产物协议

## 问题

面向 agent 的文本、图片、视频生成 CLI，应该怎样设计命令边界和产物协议，才能稳定接入自动化工作流？

## 简答

这类 CLI 的核心不是“模型更多”，而是把生成能力包装成可组合、可解析、可追踪的产物节点。最低要求是：窄命令面、明确输入输出、文件产物优先、机器可读 metadata、stderr/stdout 分离、并发和失败语义清楚，并且 provider 只能是 adapter，不能成为系统边界。

## 协议原则

生成型 CLI 面向 agent 时，应该优先保证下面几件事：

- 命令面要窄。`text`、`image`、`video`、`models` 这类命令比大而全的 agent command 更稳。
- stdin/stdout 要可组合，但二进制产物不能默认污染 agent 上下文。
- 文件输出要是一等能力。图片、视频、长文本最好通过 `-o` 写入文件或目录。
- metadata 要机器可读。`--json` 应返回模型、耗时、文件路径、成功失败、错误信息等字段。
- 人类进度输出和机器输出要分离。进度、warning、preview 走 stderr；结构化结果走 stdout。
- 并发要可控，并且结果顺序要稳定，方便生成候选集和后续评分。
- exit code 要表达失败层次。全失败和部分失败不应混成同一种错误。
- provider 要 adapter 化。OpenAI、Vercel AI Gateway、OpenRouter、fal、Replicate 等可以作为后端，但不应绑死 CLI 协议。

## 源码案例：vercel-labs/ai-cli

`vercel-labs/ai-cli` 是一个合适的案例。它不是完整 agent 框架，而是一个窄范围的生成型 CLI：`ai text`、`ai image`、`ai video`、`ai models`。

它做对的地方包括：

- 参数在 CLI 边界收窄成可靠类型，业务层不处理半脏数据。
- stdin 有首包超时探测，降低 agent 环境里误等 stdin 卡死的概率。
- 并发生成使用固定 worker 数，并保持结果顺序稳定。
- `-o` 和 `--json` 让文件产物和结构化 metadata 成为自动化接口。
- 人类进度输出走 stderr，机器结果走 stdout，降低 agent 解析成本。
- 图片/视频 preview 是 best-effort，不阻塞主产物生成。
- 动态模型目录只缓存成功结果，失败不永久缓存，允许下一次重试。
- 模型能力和调用路径分离，能表达 language-image 这类跨能力模型。
- 测试重点落在发布包入口、参数解析、模型目录、二进制输入输出、并发和预览底层这些容易坏的边界模块。

它不宜照抄的地方也很清楚：

- 当前版本和 Vercel AI Gateway 绑定较深，生成调用走 `gateway()`、`gateway.image()`、`gateway.video()`。
- reference image / stdin 二进制缺少明显大小限制，自动化接入时需要外层约束。
- 默认模型写在源码里，模型变动时依赖发版或环境变量覆盖。
- 没有内建成本账本，不适合直接承载高频内容生成链路。
- 生成结果仍需要人工验收或独立评分，不应直接自动发布到外部平台。

## OpenClaw 接入形态

OpenClaw 如果要做类似能力，应该先封装自己的稳定协议，而不是直接把业务流程写死到某个 provider CLI 上。

建议的 wrapper 输入：

- 任务类型：`text`、`image`、`video`、`models`
- prompt / system prompt
- 参考文件或 stdin 内容
- model 或候选模型列表
- 输出目录
- 并发、超时、预算上限

建议的 wrapper 输出：

- exit code
- 成功/失败/部分失败状态
- 每个结果的 model、elapsed、file、error
- prompt hash 或 source pointer
- 估算成本或实际成本记录

建议的硬约束：

- 强制 `--json` 和 `-o`。
- 限制输入文件大小、输出目录、并发数和超时。
- 记录 prompt、模型、文件路径、耗时和失败原因。
- 生成结果进入人工验收、评分器或后处理，不直接对外发布。

## 适用场景

- 小红书图文、封面、插图、短视频草稿生成。
- 多模型文案比稿，生成候选集供筛选。
- 截图视觉理解，例如解释 UI 错误、提取图片信息。
- 情报服务里的配图、摘要、短报告初稿。
- agent workflow 中需要“生成一个文件产物”的低风险节点。

## 不适用场景

- 对成本严格敏感但没有成本账本的高频链路。
- 对可复现性要求高但缺少 seed / determinism 的图片生成流程。
- 不经人工验收直接对外发布的内容链路。
- 需要强 SLA 的生产链路，除非 provider 故障切换、重试和降级策略已经完善。

## 来源指针

- `raw/sources/2026-05-31-vercel-ai-cli-research.md`
- `https://github.com/vercel-labs/ai-cli`
- `https://www.npmjs.com/package/ai-cli`
