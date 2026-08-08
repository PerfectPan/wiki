---
title: cmux
description: 记录 cmux 作为 macOS AI agent 终端编排器，如何通过 PATH shim + wrapper + env/socket 三层拦截接管 claude/codex/gemini/grok 等 agent 命令，而不包裹 shell 进程。
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

cmux 是一个 macOS 上的 AI agent 终端编排器（内嵌 ghostty 终端）。它的核心不是"包裹一层 shell 进程"，而是通过在 `PATH` 最前面插入同名 shim 来**拦截 agent 命令**（claude/codex/gemini/grok 等），由 wrapper 接管后用环境变量、Node require 钩子和 unix socket 把 agent 纳入自己的编排。原生 shell（zsh）本身不被改写，`~/.zshrc` 等启动文件保持干净。

## 关键点

- **PATH shim 拦截是入口。** cmux 为每个面板（panel）在 `$TMPDIR/cmux-cli-shims/<panel-id>/` 建临时目录并塞到 `PATH` 最前面，里面放 `claude`、`codex` 等**同名 shim 脚本**。在 shell 里敲 `claude`，命中的是这个 shim，而不是 `~/.local/bin/claude`；`command -v claude` 因此解析到 shim 路径而非真实 binary。

- **wrapper 接管，且带安全 fallback。** shim 的本质是定位 `cmux-claude-wrapper` 并 `exec` 它，把控制权交给 cmux。关键设计在末尾的 fallback：如果 wrapper 不存在，shim 会**把自己从 `PATH` 里摘掉**，再 `exec claude` 透传到真实命令——所以 cmux 自身出故障也不会把 agent 命令卡死。

- **env + socket 是注入通道。** wrapper 启动真实 agent（如 `CMUX_AGENT_LAUNCH_EXECUTABLE=~/.local/bin/claude`）时注入大量 `CMUX_*` 环境变量（panel/terminal/workspace 标识、`CMUX_SOCKET_PATH` 指向 `~/.local/state/cmux/cmux.sock`），并对 Node 程序通过 `NODE_OPTIONS=--require=.../restore-node-options.cjs` 装 require 钩子。事件通过 socket 回传给 cmux app 做编排。

- **shell 进程不被包裹。** 终端里跑的是原生 zsh，cmux 通过环境变量（`CMUX_SHELL_INTEGRATION=1`、`CMUX_LOAD_GHOSTTY_ZSH_INTEGRATION=1`）和内嵌 ghostty 的 shell integration 做 cwd/prompt 追踪，**不修改 `~/.zshrc` 等启动文件**。所以是"原生 zsh + cmux 注入的 env"，而非"cmux 包装的 shell"。

- **与 agent hooks 配置是两套路。** cmux 对 claude/codex 的编排**不依赖** settings 里的 `hooks` 字段（也因此与会被安装器写入、又可被删除的第三方 hooks 互不影响），而是靠 wrapper + `NODE_OPTIONS` 在运行时拦截。grok 是例外：cmux 主动写入 `~/.grok/hooks/cmux-session.json`，事件经 socket 转发。

## 局限与注意

- shim 目录在 `$TMPDIR` 下、路径含 session/panel id，随会话变化，不能写死引用。
- 编排能力依赖 `cmux.app` 在场；非 cmux 启动的 shell（如系统 Terminal、SSH）不受这套编排。
- fallback 设计保证了 cmux 故障时 agent 仍可运行，但也意味着"看似在 cmux 里"的命令可能在静默透传——排查时需用 `command -v` 确认实际命中 shim 还是真实 binary。
- 本文事实基于 2026-08-08 对本机 cmux 安装的直接观察，cmux 版本演进可能改变具体变量名与脚本细节。

## 相关页面

- [[Code Agent]]
- [[Agent]]
- [[wiki/syntheses/tooling/聚合型 Agent CLI 的架构设计观察|聚合型 Agent CLI 的架构设计观察]]

## 来源指针

- 本机 cmux.app（`/Applications/cmux.app`）安装的直接观察，2026-08-08
- [[raw/sources/2026-08-08-cmux-investigation|cmux 实现机制调查]]（env 变量、shim 脚本原文）
