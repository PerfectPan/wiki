---
title: openseek project architecture source review
type: source
created: 2026-07-01
source_refs:
  - https://github.com/moonbitlang/openseek
---

# openseek project architecture source review

## Source scope

- Repository: `moonbitlang/openseek`
- Review date: 2026-07-01
- Source snapshot: `42141d0`
- Repository description: DeepSeek-backed MoonBit coding agent.
- Primary language: MoonBit.
- Local static counts at review time: 75 `moon.pkg` package files and 212 `.mbt` files.
- Validation limit: the source was read locally, but upstream `moon` tests were not re-run because the `moon` CLI was not available in the review environment.

## Files and areas reviewed

- Project overview: `README.md`, `README.mbt.md`
- Model protocol: `deepseek/README.mbt.md`, `deepseek/deepseek.mbt`, `deepseek/client/README.mbt.md`
- Agent loop: `agent/README.mbt.md`, `agent/agent.mbt`
- Session model: `agent_session/README.mbt.md`, `agent_session/types.mbt`, `agent_session/projection.mbt`, `agent_session/store/store.mbt`, `agent_session/compact/compact.mbt`
- Runtime model: `agent_runtime/README.mbt.md`, `agent_runtime/runtime.mbt`
- Tool protocol: `agent_tool/README.mbt.md`, `agent_tool/agent_tool.mbt`, key tool READMEs
- CLI/TUI: `cmd/openseek/README.md`, `cmd/openseek/main.mbt`, `cmd/openseek/serve.mbt`, `cmd/tui/README.md`, `cmd/tui/engine_client.mbt`
- Evaluation: `eval/README.md`, `eval/tool_harness/README.mbt.md`, `eval/tool_harness/harness.mbt`, `eval/file_edit/README.md`, `eval/file_edit/harness/harness.mbt`, `eval/prompt_task/README.md`
- Adjacent subsystems: `agent_skill/README.mbt.md`, `agent_review/README.mbt.md`, `agent-improvement-guide.md`

## Project shape

`openseek` is not just a CLI wrapper around DeepSeek. It is a MoonBit agent stack with separable layers:

- pure DeepSeek request/response and tool-call protocol types;
- native HTTP client with streaming support and retry boundaries;
- immutable append-only session model;
- filesystem session store with JSONL event log;
- runtime event and steering queues;
- local tool registry and typed tool actions;
- agent loop that commits user, assistant, tool, runtime, summary, and terminal events;
- CLI, serve mode, TUI, review mode, best-of-N mode, and eval harnesses.

## Important source facts

- The `deepseek` package is pure and suitable for network-free request/response tests.
- The effectful HTTP client is isolated in `deepseek/client`.
- `agent` requires the caller to provide system prompt text; prompt ownership stays at the application layer.
- `Session` is immutable and append-only. Compaction appends `Summary` events instead of deleting raw events.
- `Session::chat_messages` repairs dangling tool calls with synthetic tool-error messages to keep replay protocol-valid.
- `AgentRuntime` separates lossy runtime events from lossless steering input.
- The standard tools include `shell`, `read`, `edit`, `multi_edit`, `write`, and `finish`.
- Tool failures are normal `ToolOutput(is_error=true)` responses sent back to the model for recovery.
- `finish` returns `Control(Finish(...))`, so ending the run is a host-loop transition, not merely another tool message.
- CLI runs record durable sessions by default; `--no-session` restores ephemeral behavior.
- TUI uses a long-lived `--serve` engine and JSONL command/event streams for prompt, steer, cancel, and compact operations.
- Eval support is multi-layered: deterministic tool harness, file-edit model eval, prompt-task eval, and roadmap notes for semantic CLI validation.

## Durable takeaways

- The project is best read as an agent runtime experiment, not a polished user-facing product.
- Its central design theme is turning model interaction into typed, replayable, testable protocol boundaries.
- The most reusable parts are not specific to DeepSeek or MoonBit: append-only session events, tool-result-as-recovery, runtime/steering separation, serve-mode JSONL control, and eval harness design.

