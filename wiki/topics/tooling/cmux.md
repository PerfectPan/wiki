---
title: cmux
description: 记录 cmux 作为 macOS AI agent 终端编排器，如何通过 PATH shim 拦截 agent 命令，再由 wrapper 用命令行参数动态注入各 agent 自带的 hooks（不写配置文件）把 claude/codex/grok 纳入编排。
type: topic
category: tooling
status: seed
created: 2026-08-08
updated: 2026-08-08
timestamp: 2026-08-08
tags:
  - agent
  - terminal
  - wrapper
  - claude-code
  - cli
source_refs:
  - raw/sources/2026-08-08-cmux-investigation.md
resource:
  - raw/sources/2026-08-08-cmux-investigation.md
---
# cmux

## 摘要

cmux 是一个 macOS 上的 AI agent 终端编排器（内嵌 ghostty 终端）。它通过在 `PATH` 最前面插入同名 shim 来**拦截 agent 命令**（claude/codex/grok 等），由 wrapper 接管后，**用命令行动态注入各 agent 自带的 hooks 机制**（claude 用 `--settings`，codex 用 `--enable hooks` + `-c hooks.X=...`），让 SessionStart/Stop/PreToolUse 等事件回调 cmux。整个过程不修改用户的配置文件，与用户已有的 hooks 并存。原生 shell（zsh）不被改写。

## 关键点

- **PATH shim 拦截是入口。** cmux 为每个面板（panel）在 `$TMPDIR/cmux-cli-shims/<panel-id>/` 建临时目录并塞到 `PATH` 最前面，里面放 `claude`、`codex` 等**同名 shim 脚本**。shell 里敲 `claude` 命中的是这个 shim，而非 `~/.local/bin/claude`；`command -v claude` 因此解析到 shim 路径。

- **wrapper 接管，且带安全 fallback。** shim 定位 `cmux-claude-wrapper` / `cmux-codex-wrapper` 并 `exec`。关键设计在 fallback：wrapper 缺失、或不在 cmux 环境（无 `CMUX_SURFACE_ID`）、或 socket 不可达时，直接透传真实命令，cmux 故障也不会把 agent 卡死（claude shim 还有"把自己从 PATH 摘掉再透传"的兜底）。

- **接入靠"动态注入各 agent 的 hooks"，不是进程内拦截。** wrapper 不 patch 模块、不改配置文件，而是在**启动命令行上注入 hooks**：
  - **claude**：wrapper 构造一份 hooks JSON（SessionStart/Stop/SessionEnd/Notification/UserPromptSubmit/PreToolUse/PostToolUse/PermissionRequest/SubagentStop，每个 command 调 `cmux hooks claude <event>`），通过 `claude --session-id <uuid> --settings <hooks-json>` 注入。`--settings` 与用户 `settings.json` 叠加；若用户也传 `--settings`，wrapper 用内联 node 脚本把两者 deep-merge 成单一 `--settings`，确保两边 hooks 都跑、且不依赖 CLI 对多个 `--settings` 的优先级。
  - **codex**：wrapper 调 `cmux hooks codex inject-args` 拿到一组参数（`--enable hooks`、`--dangerously-bypass-hook-trust`、`-c hooks.<event>=<cmux-cmd>`），prepend 到 codex 命令行注入。hook 是 fire-and-forget（后台 + 30s watchdog + 立即 `echo '{}'`），因为 codex 同步阻塞跑 hooks，否则每次启动卡 ~35s。
  - 所以 cmux **重度依赖** claude/codex 自带的 hooks 机制，只是每次启动**动态注入、不落盘**——既不污染 `~/.claude/settings.json` / `~/.codex/hooks.json`，又天然和用户已有 hooks 并存。

- **`NODE_OPTIONS=--require` 只是还原环境，不是拦截。** cmux 给 claude 临时加了 `--max-old-space-size=4096`（内存）和 `--require restore-node-options.cjs`；那个 9 行的 cjs 在 Node 启动最早期把 `NODE_OPTIONS` 恢复成用户原始值，防止 cmux 的修改泄漏到 claude 的子进程。它**不 patch 任何模块、不拦截任何 API**。codex 不是 Node 程序，没有这层。

- **shell 进程不被包裹。** 终端里跑的是原生 zsh，cmux 通过环境变量（`CMUX_SHELL_INTEGRATION=1`、`CMUX_LOAD_GHOSTTY_ZSH_INTEGRATION=1`）和内嵌 ghostty 的 shell integration 做 cwd/prompt 追踪，**不修改 `~/.zshrc`**。

- **事件回传走 socket。** hooks 命令（`cmux hooks claude/codex <event>`）通过 `CMUX_SOCKET_PATH`（`~/.local/state/cmux/cmux.sock`）把事件回传给 cmux app 做编排/通知。grok 因是原生 Mach-O 二进制（非 Node、且 cmux 选择走它的 hooks 配置），由 cmux 写 `~/.grok/hooks/cmux-session.json` 走同样机制。

## 局限与注意

- shim 目录在 `$TMPDIR` 下、路径含 session/panel id，随会话变化，不能写死引用。
- 编排依赖 `cmux.app` 在场 + socket 可达；非 cmux 启动的 shell（系统 Terminal、SSH）不受编排。
- wrapper 的 hook 注入是 per-invocation 的，agent 自身的 settings/hooks 配置仍是事实来源之一，cmux 与之 merge 而非覆盖。
- 本文机制基于 2026-08-08 对本机 `cmux.app` 的直接代码阅读（`cmux-claude-wrapper` ~1060 行、`cmux-codex-wrapper` ~290 行、`restore-node-options.cjs` 9 行），cmux 版本演进可能改变细节。

## 相关页面

- [[Code Agent]]
- [[Agent]]
- [[wiki/syntheses/tooling/聚合型 Agent CLI 的架构设计观察|聚合型 Agent CLI 的架构设计观察]]

## 来源指针

- 本机 cmux.app（`/Applications/cmux.app`）的 wrapper 脚本原文阅读，2026-08-08
- [[raw/sources/2026-08-08-cmux-investigation|cmux 实现机制调查]]（env 变量、shim 与 wrapper 关键片段）
