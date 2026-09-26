---
title: Prompt
description: Prompt 的用途、教程与本仓库保存的提示词素材
type: topic
category: ai
created: 2026-04-12
updated: 2026-09-26
timestamp: 2026-09-26
tags:
  - prompt
  - prompt-engineering
  - workflow
source_refs:
  - raw/sources/Prompt.md
  - https://github.com/anthropics/prompt-eng-interactive-tutorial
  - prompts/README.md
  - raw/sources/2026-09-22-lenny-world-class-designer.md
resource:
  - raw/sources/Prompt.md
  - https://github.com/anthropics/prompt-eng-interactive-tutorial
  - prompts/README.md
  - raw/sources/2026-09-22-lenny-world-class-designer.md
---
# Prompt

## 摘要

Prompt 是提供给模型的输入，可以包含任务指令、上下文、示例和输出要求。

本仓库将可复查的来源放在 `raw/sources/`，提取的提示词放在 `prompts/`。例如 [[prompts/plan-first|Plan first]] 要求 agent 先提出代码修改计划；该副本保留了原素材的格式错误，使用前需要处理，详见文件中的 `notes`。

## 本仓库的提示词记录

每个文件记录用途、来源和使用条件，格式与查找方式见 [[prompts/README|prompts README]]。说明使用英文或中文取决于提示词本身的语言，不要求统一翻译。

当前 PR 使用三个分类值：

| 值 | 原有分类意图 |
| --- | --- |
| `recommended` | 整理者认为说明较完整、值得尝试 |
| `reference` | 需要结合具体任务调整的参考示例 |
| `limited` | 存在明显限制或作为反例保留 |

这些值不是测试结果，也不能跨模型和任务保证效果。仅凭文本是否包含失败案例或详细步骤，无法证明一条提示词更好。分级是否值得继续维护，仍是提示词库设计中的待定问题。

## 教程与来源

- [Anthropic Prompt Engineering Interactive Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)
- [[raw/sources/Prompt|原有 Prompt 素材]]
- [[raw/sources/2026-09-22-lenny-world-class-designer|设计提示词文章存档]]
