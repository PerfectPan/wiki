---
title: Prompt
description: Prompt 是什么，以及本 wiki 提示词收录的判据与三档标准（索引见 Awesome Prompts）
type: topic
category: ai
created: 2026-04-12
updated: 2026-09-22
timestamp: 2026-09-22
tags:
  - prompt
  - prompt-engineering
  - workflow
source_refs:
  - raw/sources/Prompt.md
  - https://github.com/anthropics/prompt-eng-interactive-tutorial
  - wiki/topics/ai/Awesome Prompts.md
  - prompts/README.md
  - raw/sources/2026-09-22-lenny-world-class-designer.md
resource:
  - raw/sources/Prompt.md
  - https://github.com/anthropics/prompt-eng-interactive-tutorial
  - wiki/topics/ai/Awesome Prompts.md
  - prompts/README.md
  - raw/sources/2026-09-22-lenny-world-class-designer.md
---
# Prompt

## 摘要

Prompt 是用户交给模型的输入指令。在本 wiki 里，这页除了作为 Prompt 主题页，还兼作**提示词收录的判据页**：值得长期留存的提示词要满足下面几条，否之就只当素材放 `raw/sources/`。

过线的提示词存在 `prompts/`（一条一个文件，正文原样复制），索引在 [[Awesome Prompts]]，那里只写「一句话价值 + 分级 + 指针」。

## 提示词放在哪

| 位置 | 作用 |
| --- | --- |
| `prompts/<id>.md` | 提示词原文（逐字副本）+ 元数据（`scene` / `level` / `tags` / `source`） |
| `raw/sources/` | 来源素材（文章、笔记），即原文的出处 |
| [[Awesome Prompts]] | 人读的索引：一句话价值 + 分级 + 指针 |

命令（文件格式见 `prompts/README.md`）：

```text
bin/wiki prompts list [--tag <tag>] [--level <档>] [--json]   列出
bin/wiki prompts search <关键词>                              搜索（含正文）
bin/wiki prompts show <id>                                    打印原文
bin/wiki prompts check                                        校验所有提示词文件
```

## 收录判据

一条提示词值得长期留存，至少要能回答：

1. **什么时候用**：触发场景写得出来，而不是「感觉需要的时候」；
2. **产物形状**：它让模型交什么？输出格式、消费者、下游怎么接；
3. **硬 gotcha**：有至少一条模型会稳定犯的错或边界；只是复述常识和通用命令的不算；
4. **能判断有没有用**：有可观察的验收信号；只能是人工看图也行，但不能为零；
5. **来源可追溯**：原文在哪份素材能整段复制，不靠记忆复述。

## 分级

| 级 | 标准 |
| --- | --- |
| **推荐** | 1–5 全满足，且结构完整、边界清楚、写了失败模式；可以直接拿去用 |
| **可参考** | 满足 1、2、5，但缺默认取值 / gotcha / 验收中的多项，必须按自己的场景补齐 |
| **偏薄** | 只有人格、文风或口号；或纯技巧清单，没有原文与边界；只作反例或起点 |

审的时候把「模型已经知道的」和「只有踩过才知道的」分开：后者才是提示词真正的信息量。

## 示例：计划模式提示词（Plan-first）

要求 agent 先读仓库约定与相似实现、有歧义先提问，再输出带文件树的逐文件改动计划：

- ```markdown
  ## 1. Explore the Codebase

  * List relevant directories to show project structure.
  * Review http://AGENTS[.]md, http://CLAUDE[.]md, and files under `docs/` for context and conventions.
  * Check existing code for examples of similar implementations.

  ## 2. Ask Clarifying Questions

  If anything is ambiguous, ask questions before finalizing the plan.
  Examples:

  * "Which module should the new helper live in?"
  * "Should this endpoint return JSON or HTML?"

  ## 3. File Tree of Changes

  At the top of the plan, show a tree diagram of affected files.
  Use markers for status:

  * UPDATE = update
  * NEW = new file
  * DELETE = deletion

  Example:
  \`\`\`
  /src
   ├── services
   │    ├── UPDATE user.service.ts
   │    └── NEW payment.service.ts
   ├── utils
   │    └── DELETE legacy-helpers.ts
   └── UPDATE index.ts
  \`\`\`

  ## 4. File-by-File Change Plan

  For each file:

  * Show full path + action (update, new, delete).
  * Explain the exact changes in plain language.
  * Include a short code snippet for the main update.

  Example:

  * File: `src/services/user.service.ts` (UPDATE)

    * Add a method `getUserByEmail(email: string)` that looks up a user from an in-memory list.
    * Refactor `getUserById` to reuse shared lookup logic.

    \`\`\`
    const users = [
      { id: 1, email: "alice@example[.]com", name: "Alice" },
      { id: 2, email: "bob@example[.]com", name: "Bob" },
    ];

    export function getUserByEmail(email: string) {
      return users.find(u => http://u[.]email === email) || null;
    }

    export function getUserById(id: number) {
      return users.find(u => http://u[.]id === id) || null;
    }
    \`\`\`

  ## 5. Explanations & Context

  At the end of the plan, include:

  * Rationale for each change (why it's needed).
  * Dependencies or side effects to watch for.
  * Testing suggestions to validate correctness.
  ```
- Anthropics 的提示词工程教程：https://github.com/anthropics/prompt-eng-interactive-tutorial （需要 api key）

## 相关页面

- [[Awesome Prompts]] — 过线条目的薄索引
- `prompts/README.md` — 提示词文件格式与命令
- [[Claude 5 时代的上下文工程]] — 提示词之外的另一半：上下文怎么组织
- [[AI Slop]] — 「AI 味」的语义层归纳
- [[Awesome Agent Skills]] — 提示词升级成带脚本、manifest、QA 的 skill

## 来源指针

- `raw/sources/Prompt.md`
- https://github.com/anthropics/prompt-eng-interactive-tutorial
