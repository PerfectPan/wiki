# 2026-08-03 大模型 101 对话摘录

来源：本机 agent 闲聊会话（opencode），围绕 coding agent 用量、计费与 API 协议的问答整理。

## 覆盖问题

1. Token / M / B / 亿 的数量级换算
2. ccusage compact 模式会隐藏 cache 列；total ≈ input + output + cacheCreation + cacheRead
3. Agent 为何极高 cache hit（上下文反复重传）
4. Coding Plan 套餐额度 vs API 按量：重度用户套餐往往不够
5. Claude / OpenAI Codex / GLM / Kimi / DeepSeek 的 API 单价横向对比（时点 2026-08 前后）
6. DeepSeek-V4-Flash-0731 正式版 agent 能力与价格定位
7. Chat Completions vs Responses API vs Anthropic Messages：协议差什么、工具是否本地执行、多步含义
8. 各厂支持的 API 风格与 Claude Code / Codex / OpenCode 默认插头

## 官方价格与发布指针（对话当时查阅）

- https://docs.z.ai/guides/overview/pricing
- https://docs.z.ai/devpack/overview
- https://docs.z.ai/devpack/notice/usage-revision.md
- https://platform.claude.com/docs/en/about-claude/pricing
- https://platform.openai.com/docs/pricing
- https://platform.kimi.ai/docs/pricing/chat-k3
- https://platform.kimi.ai/docs/pricing/chat-k27-code
- https://api-docs.deepseek.com/quick_start/pricing
- https://api-docs.deepseek.com/updates
- https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731

## 说明

本文件是 raw 事实层摘录与指针，不代替 `wiki/` 中的综合与主题页。价格与模型榜单会过期，以官方文档为准。
