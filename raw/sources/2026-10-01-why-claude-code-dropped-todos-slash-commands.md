<!--
source: https://tonylee.im/en/blog/why-claude-code-dropped-todos-slash-commands/
type: blog
author: Tony Lee
published: 2026-02-08 (updated 2026-02-18)
fetched: 2026-10-01
note: page navigation, related-posts links and newsletter trailer removed at ingest
-->

# Why Claude Code Dropped Todos and Slash Commands

Anthropic replaced TodoWrite with Tasks and Slash Commands with Skills in two days. Both changes point in the same direction - unhobbling the model.
Over two days, Anthropic changed two things in Claude Code simultaneously. Todos became Tasks. Slash Commands became Skills. Both were framed as “existing features, same behavior” - easy to overlook. But the two changes point in exactly the same direction.
## Why TodoWrite Disappeared
Anthropic’s explanation is revealing: “Opus 4.5 runs autonomously for longer and tracks state more effectively. For small tasks, TodoWrite is no longer necessary.”
- The model already figures out what needs to be done on its own
- A separate to-do list becomes overhead rather than help
- The core move is unhobbling - removing constraints that limit what the model can do
The model was already capable. The tool was holding it back.
## Why Slash Commands Became Skills
The same logic applies here. Slash Commands were designed around progressive disclosure - load context only when needed. As the model got smarter, that approach stopped being optimal.
- Skills read related files automatically to assemble context
- A SKILL.MD file can reference other files, enabling multi-step context chains
- From the model’s perspective, there’s no reason to split this into a separate tool
## The Common Thread: Removing Scaffolding for Simple Work
Here’s the pattern across both changes:
- Todos: The model handles it on its own, so the tool is unnecessary
- Slash Commands: The model loads context on its own, so the special syntax is unnecessary
****
****

Both follow the same philosophy: as model capability increases, remove the scaffolding that was compensating for its limitations. Anthropic calls this “unhobbling” - taking off the chains.
## Yet Tasks and Skills Got More Powerful
Here’s the paradox. Tools for simple work disappeared, but the abstractions for complex work got significantly more sophisticated.
What Tasks added:
- Dependencies and blockers stored as metadata between tasks
- File-system-based coordination so multiple sessions and sub-agents can collaborate
- Updates in one session automatically reflected across all sessions sharing the same Task List
What Skills added:
- An agent: setting that creates a sub-agent with a skill loaded
- A context: fork option that clones the full current context into a separate sub-agent
- Fine-grained control over who can invoke a skill - user, model, or both

## A New Principle for Agent Design
The principle I read from these two changes:
- Simple tasks: Hand them to the model and remove the tools
- Complex collaboration: Build structures for shared state and context isolation
****
****

An environment variable like CLAUDE_CODE_TASK_LIST_ID=groceries claude lets multiple sessions share the same Task List. Combined with Skills’ sub-agent integration for splitting context, you can run multiple workstreams concurrently. This is the basic skeleton of multi-agent collaboration that Claude Code is proposing.
As models get smarter, simple scaffolding disappears and only the collaboration layer remains.
The future of agent systems isn’t about betting on a single agent’s capability. It’s about designing how multiple agents split and merge state. That’s what will matter most going forward.
