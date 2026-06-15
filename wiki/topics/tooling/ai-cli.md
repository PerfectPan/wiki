---
title: ai-cli
type: topic
category: tooling
status: seed
created: 2026-05-12
updated: 2026-05-12
tags:
  - ai
  - cli
  - ai-sdk
  - agent-tools
source_refs:
  - https://github.com/vercel-labs/ai-cli
  - raw/sources/2026-05-12-ai-cli-skill-review.md
---
# ai-cli

## 摘要

`vercel-labs/ai-cli` 是一个极简的 AI 生成 CLI，核心不是做交互式 terminal agent，而是把文本、图片和视频生成能力封装成 Unix 管道友好的原子命令。它通过 Vercel AI SDK 与 AI Gateway 统一访问模型，并把生成物以文件、stdout 或 JSON metadata 的形式交付，适合被脚本、cron 或 agent 工作流调用。

## 关键点

- **产品边界很窄。** 核心命令是 `ai text`、`ai image`、`ai video`、`ai models`，不处理 memory、tools、权限、长任务状态或自主 agent 行为。
- **价值在可组合性。** `stdin` / `stdout`、`-o` 文件输出和 `--json` metadata 让它更像自动化流水线中的生成物工具，而不是面向人类聊天的应用。
- **动态模型发现。** 它从 Vercel AI Gateway 拉取模型列表，避免在 CLI 中维护静态模型表；代价是对 Gateway 可用性和模型元数据质量有依赖。
- **多模态路由有工程含量。** 普通 image model 走 `generateImage`；但 `language + image-generation` 类型模型需要走 `generateText`、多模态 messages 和 provider options，再从 `result.files` 中提取图片。这说明“生成图片”能力不一定暴露在 image API 下。
- **多模型比较是基础能力。** `-m` 支持多个模型，`-n` 支持每个模型生成多个结果；但这也会放大成本、失败率和结果筛选负担。
- **适合作为 agent 的底层工具。** 它不是“大脑”，更像负责生成文本、图片、视频的“手”。真正的系统价值来自上层如何做选题、调度、验收、发布和复盘。

## 局限

- 当前项目仍偏早期，版本和参数还在变化，已有 breaking changes。
- 强依赖 Vercel AI Gateway；多 provider 支持仍在演进中。
- 失败处理偏基础：有超时和部分失败 exit code，但缺少 retries、backoff、rate limit 感知和成本预算。
- 对 agent 来说，图片和视频生成必须优先使用 `-o <path-or-dir> --json`，避免二进制 stdout 污染上下文。
- 仓库 `package.json` 声明 Apache-2.0，但审阅时未看到独立 `LICENSE` 文件；企业采用时需要补核验。

## 启发

`ai-cli` 的启发不在于商业护城河，而在于产品形态：把 AI 生成能力拆成稳定、可组合、可脚本化的 CLI 原子能力。对于 agent 工作流，生成能力最好不是一次性的 prompt wrapper，而是有明确输入、输出、产物路径和失败语义的工具。

这类工具本身不一定赚钱，但可以成为内容自动化、情报服务、素材生产和批处理工作流的底层零件。

## 相关页面

- [[wiki/syntheses/ai/Skill 工程化的产物协议范式|Skill 工程化的产物协议范式]]

## 来源指针

- https://github.com/vercel-labs/ai-cli
- `raw/sources/2026-05-12-ai-cli-skill-review.md`
