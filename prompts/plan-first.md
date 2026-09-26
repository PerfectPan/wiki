---
id: plan-first
title: 计划模式（Plan-first）
scene: 让 agent 动大改动之前先交计划，避免它边想边改、顺手改到别的模块时
level: 可参考
tags:
  - agent
  - code
  - workflow
source: raw/sources/Prompt.md
source_note: 仓库内既有素材（原样保留），非本次外部来源
notes:
  - 正文照 `raw/sources/Prompt.md` 原样复制，其中 `\`\`\`` 是素材里带反斜杠的转义写法，真正使用时换成普通三反引号
  - 素材里还有 `http://AGENTS[.]md` 这种被「防链接化」过的写法，同样保持原样
  - 缺正例/负例和一个明确的验收信号，所以没有放进推荐档
added: 2026-09-22
---

````text
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
````
