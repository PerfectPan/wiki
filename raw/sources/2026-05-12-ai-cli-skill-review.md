---
title: ai-cli 仓库与 Skill 设计审阅记录
source_type: conversation + repository review
created: 2026-05-12
source_refs:
  - https://github.com/vercel-labs/ai-cli
  - https://github.com/vercel-labs/ai-cli/blob/main/skills/ai-cli/SKILL.md
---

# ai-cli 仓库与 Skill 设计审阅记录

## 背景

基于一次对 `vercel-labs/ai-cli` 的仓库审阅，重点讨论了它作为 terminal AI generation CLI 的产品边界、源码结构，以及其中 `skills/ai-cli/SKILL.md` 是否算一个好 Skill。

## 仓库事实摘要

- `ai-cli` 是一个极简 CLI，不是交互式 terminal agent。
- 核心命令是 `ai text`、`ai image`、`ai video`、`ai models`。
- 主要依赖 Vercel AI SDK 与 AI Gateway，通过统一模型入口生成文本、图片和视频。
- CLI 的工程价值在于 Unix 管道友好、生成物可落盘、支持 `--json` 结构化 metadata、多模型对比，以及适合被 agent 当作底层原子工具调用。
- 源码里比较有含量的一点是：它区分普通 image model 与 `language + image-generation` 模型。后者虽然输出图片，但需要通过 `generateText` + multimodal messages + `responseModalities` 调用，再从 `result.files` 中提取图片。

## 对 ai-cli Skill 的评价

`skills/ai-cli/SKILL.md` 合格但偏薄：

- 优点：边界清楚，说明何时使用；示例直接；明确提醒 agent 生成图片/视频时应使用 `-o`，避免二进制污染上下文。
- 不足：缺少失败处理、超时策略、exit code 使用、`--json` 默认工作流、多模型结果筛选、成本和速率限制提醒。
- 判断：它更像 README 摘要型 Skill，能帮助 agent 知道工具存在；但还不是工程操作型 Skill，不能充分约束 agent 稳定、低成本、可恢复地使用工具。

## 提炼出的判断

一个好 Skill 不只是介绍命令，而要把模型容易做错的地方变成操作协议：什么时候加载、默认怎么执行、哪些参数会放大成本、失败怎么收敛、产物怎么交付、何时不要使用。
