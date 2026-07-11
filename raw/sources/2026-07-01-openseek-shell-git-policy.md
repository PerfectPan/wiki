---
title: openseek shell/git policy source review
type: source
created: 2026-07-01
source_refs:
  - https://github.com/moonbitlang/openseek
  - https://github.com/moonbitlang/openseek/pull/273
---

# openseek shell/git policy source review

## Source scope

- Repository: `moonbitlang/openseek`
- Repository description: DeepSeek-backed MoonBit coding agent.
- Primary language: MoonBit.
- Review date: 2026-07-01.
- Main source snapshot: `42141d0` (`fix(shell): strengthen block message + clustered-f / pathspec-from-file clobber`), pushed after PR #273 merged.
- Main PR: #273, `feat(shell/sandbox): relax git via a default-deny trust allowlist`, merged on 2026-06-30.
- Local validation limit: source and test review only. The `moon` CLI was not available in the review environment, so project tests were not re-run locally.

## Repository shape

`openseek` is a small MoonBit foundation for a DeepSeek-backed coding agent. The repository separates:

- `deepseek` and `deepseek/client`: model data structures, JSON encoding/decoding, and HTTP transport.
- `agent_session`: append-only typed conversation state and DeepSeek message projection.
- `agent_runtime`: loop-scoped runtime state, event queue, steering queue, and task scope.
- `agent_tool`: model-facing local tool boundary and concrete built-in tools.
- `agent`: the native agent loop and local tool dispatch.
- `cmd/openseek` and `cmd/tui`: CLI and terminal UI entry points.
- `eval/*` and `testkit/*`: deterministic harnesses and filesystem fixtures.

The standard tool registry includes `shell`, `read`, `edit`, `multi_edit`, `write`, and `finish`.

## PR #273 source facts

PR #273 changed the shell sandbox behavior for Git. Before this PR, the project had a large heuristic engine for detecting Git writes. The PR replaced it with a smaller internal package:

- `agent_tool/shell/internal/git_policy/git_policy.mbt`
- `agent_tool/shell/internal/git_policy/git_policy_test.mbt`
- `agent_tool/shell/sandbox.mbt`
- `agent_tool/shell/sandbox_wbtest.mbt`
- `agent_tool/shell/shell_test.mbt`
- `agent_tool/shell/README.mbt.md`

The final diff from the pre-PR baseline to `42141d0` was:

- 9 files changed.
- 771 insertions.
- 1445 deletions.
- New focused `git_policy` package.
- Large reduction inside `sandbox.mbt` and sandbox tests.

The PR body reports `moon check`, `moon fmt`, `moon info`, and 112/112 relevant tests passing in CI. This review did not independently re-run those commands.

## Implemented policy

The policy has two distinct layers:

1. Runtime sandbox launch decision.
   - On macOS, commands normally run under `/usr/bin/sandbox-exec` with MoonBit source and manifests read-only.
   - Narrow, recoverable Git worktree operations can run as trusted source writes.
   - Everything else remains source-read-only where sandbox enforcement is available.

2. Static pre-block.
   - Cross-platform guard before execution.
   - Blocks Git commands that mutate source in ways not recoverable from Git's object store, or commands that can reconfigure Git to write from another source.
   - This matters because Linux and Windows do not get the same `sandbox-exec` enforcement.

Trusted recoverable Git subcommands:

- `checkout`
- `switch`
- `restore`
- `reset`
- `stash`
- `rm`

Explicitly excluded or blocked:

- `apply`, `am`, `update-index`, `read-tree`, `fast-import`
- `mv`
- non-dry-run `clean`
- object-store writers combined with reconfiguring options such as `-c`, `--config-env`, `--git-dir`, `--namespace`, `--exec-path`, `-C`, `--work-tree`
- object-store writers combined with custom environment such as `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_*`, or `env ... git`
- `checkout`, `switch`, and `restore` forms that can clobber untracked files from another tree, including force/source/overlay/side-pick forms and positional tree-ish before `--` or `--pathspec-from-file`

Allowed exceptions:

- read-only patch validation such as `git apply --check` and `git apply --stat`
- dry-run `git clean -n`
- read-only Git commands such as `git status` and `git diff`, though they do not get trusted source-write classification

## Important implementation observations

- `git_policy.mbt` is pure command-line grammar and classification. It has no filesystem, workspace, or shell-parse dependency.
- `sandbox.mbt` owns workspace glue, runtime sandbox launching, direct source-write pre-blocking, and trusted command classification.
- `trusted_git_command_class` grants trusted source write only when a parsed Git invocation is a recoverable object-store writer and has no custom environment or reconfiguring global options.
- `git_preblock_target` blocks unsafe Git independently of current working directory so `git -C <workspace> apply` cannot slip through from outside the workspace.
- The TooComplex text path still scans command text for unsafe Git operations when static argv cannot be trusted, including custom environment before the `git` word.
- The tool's block message is part of the policy. It tells the model not to work around the shell block with redirects, scripts, `sed`, `awk`, `git apply`, or stage-then-checkout tricks, and to use line-anchored `edit` or `multi_edit`.

## Residual risk acknowledged by the source

The policy is explicitly a guardrail, not a hard security boundary:

- A determined plumbing sequence can still seed Git's object store while `.git` is writable.
- Branch switching may overwrite git-ignored untracked source if the target branch tracks that path.
- The static pre-block is conservative but not a full shell security proof.
- Runtime sandbox enforcement is strongest on macOS because it depends on `sandbox-exec`.

## Reusable takeaway

The durable idea is not the exact Git allowlist. The reusable idea is to split agent shell permissions into:

- dedicated file-editing tools for source mutation,
- a general shell for analysis and validation,
- runtime enforcement where possible,
- cross-platform static pre-blocks where runtime enforcement is weaker,
- pure, testable policy classifiers,
- explicit model-facing guidance when an unsafe path is blocked.
