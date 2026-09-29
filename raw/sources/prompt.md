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
- https://github.com/anthropics/prompt-eng-interactive-tutorial Anthropics 的教程，需要 api key
-