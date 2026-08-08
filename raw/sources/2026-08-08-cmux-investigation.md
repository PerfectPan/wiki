---
title: cmux 实现机制调查（2026-08-08）
date: 2026-08-08
topic: cmux
sources:
  - 本机 cmux.app（/Applications/cmux.app）直接观察
---

# cmux 实现机制调查（2026-08-08）

## 调查背景与方法

在排查本机 agent hooks（claude/codex/gemini/amp 接 SuperSet、grok 接 cmux）的过程中，确认 claude/codex 实际由 **cmux** 编排而非 SuperSet。本文记录对 cmux 实现机制的直接观察，作为 `wiki/topics/tooling/cmux.md` 的事实层。

方法：在一个 cmux 启动的 claude 会话内，检查 `PATH`、`command -v`、`$TMPDIR/cmux-cli-shims/` 下的 shim 脚本、`env | grep CMUX`。日期 2026-08-08。

## PATH 注入

`PATH` 最前面被插入了 session 临时 shim 目录：

```
PATH[0] = /var/folders/<id>/T/cmux-cli-shims/<panel-id>/
...
PATH[n] = /Applications/cmux.app/Contents/Resources/bin
```

`command -v claude` / `command -v codex` 解析到 shim 目录下的同名脚本，而非 `~/.local/bin/claude`。

## shim 目录内容

```
/var/folders/<id>/T/cmux-cli-shims/<panel-id>/
├── claude   (~1.5KB, bash 脚本)
└── codex    (~1.5KB, bash 脚本)
```

## claude shim 脚本原文（节选）

```bash
#!/usr/bin/env bash
cmux_wrapper="/Applications/cmux.app/Contents/Resources/bin/cmux-claude-wrapper"
# 1) 依次从 CMUX_BUNDLED_CLI_PATH 同目录、或 `command -v cmux` 同目录找 wrapper
...
export CMUX_CLAUDE_WRAPPER_SHIM="<tmpdir>/cmux-cli-shims/<panel-id>/claude"
export CMUX_CLAUDE_WRAPPER_SHIM_ROOT="<tmpdir>/cmux-cli-shims/<panel-id>"
if [[ -x "$cmux_wrapper" ]]; then
    exec "$cmux_wrapper" "$@"      # 2) 正常路径：交给 cmux wrapper
fi
# 3) fallback：遍历 PATH，跳过所有 cmux-cli-shims 目录，重建 PATH 后透传真实 claude
cmux_path_without_shim=""
IFS=:
for cmux_entry in ${PATH:-}; do
    if [[ "$cmux_entry" == */cmux-cli-shims/* ]]; then continue; fi
    ...
done
export PATH="$cmux_path_without_shim"
exec claude "$@"
```

要点：优先 `exec cmux-claude-wrapper`；wrapper 缺失则把自己从 PATH 摘掉再 `exec claude`（安全透传，cmux 故障也不卡死）。

## 关键 CMUX_* 环境变量（节选）

```
CMUX_BUNDLE_ID=com.cmuxterm.app
CMUX_BUNDLED_CLI_PATH=/Applications/cmux.app/Contents/Resources/bin/cmux
CMUX_SHELL_INTEGRATION=1
CMUX_SHELL_INTEGRATION_DIR=/Applications/cmux.app/Contents/Resources/shell-integration
CMUX_LOAD_GHOSTTY_ZSH_INTEGRATION=1
CMUX_PANEL_ID=<uuid>
CMUX_TERMINAL_LIFECYCLE_ID=<uuid>
CMUX_WORKSPACE_ID=<uuid>
CMUX_TAB_ID=<uuid>
CMUX_SOCKET_PATH=~/.local/state/cmux/cmux.sock
CMUX_PORT=9140
CMUX_AGENT_LAUNCH_KIND=claude
CMUX_AGENT_LAUNCH_EXECUTABLE=~/.local/bin/claude
CMUX_AGENT_LAUNCH_CWD=<cwd>
CMUX_CLAUDE_WRAPPER_SHIM=<tmpdir>/cmux-cli-shims/<panel-id>/claude
CMUX_CODEX_WRAPPER_SHIM=<tmpdir>/cmux-cli-shims/<panel-id>/codex
NODE_OPTIONS=--require=<tmpdir>/cmux-claude-node-options/restore-node-options.cjs --max-old-space-size=4096
GHOSTTY_RESOURCES_DIR=/Applications/cmux.app/Contents/Resources/ghostty
TERMINFO=/Applications/cmux.app/Contents/Resources/terminfo
```

（敏感能力字段如 `CMUX_SOCKET_CAPABILITY` 此处省略。）

## 机制小结

cmux 通过三层实现 agent 编排：

1. **PATH shim**：临时目录塞 PATH[0]，同名 shim 拦截 agent 命令。
2. **wrapper 接管**：shim `exec cmux-<agent>-wrapper`，带安全 fallback（摘 shim 后透传）。
3. **env + socket 注入**：wrapper 注入 `CMUX_*` 与 `NODE_OPTIONS` require 钩子，事件经 socket 回传。

shell 本体（zsh）不被改写，仅被注入 env + ghostty shell integration。

## 与 agent hooks 的关系（读 wrapper 代码后订正）

cmux **完全依赖**各 agent 自带的 hooks 机制，只是通过命令行参数**动态注入、不落盘**：

- **claude**：`cmux-claude-wrapper` 构造 hooks JSON（SessionStart/Stop/SessionEnd/Notification/UserPromptSubmit/PreToolUse/PostToolUse/PermissionRequest/SubagentStop），通过 `claude --session-id <uuid> --settings <hooks-json>` 注入。`--settings` 与用户 `settings.json` 叠加；用户额外传的 `--settings` 用 wrapper 内联的 node 脚本 deep-merge 成单一 `--settings`（hook 数组 concat、用户标量优先）。
- **codex**：`cmux-codex-wrapper` 调 `cmux hooks codex inject-args` 生成参数（`--enable hooks`、`--dangerously-bypass-hook-trust`、`-c hooks.<event>=<cmux-cmd>`），prepend 到 codex 命令行。hook 用 fire-and-forget（捕获 stdin 到临时文件 + nohup 后台 + 30s watchdog + 立即 `echo '{}'`），避免 codex 同步阻塞跑 hooks 导致每次启动卡 ~35s。
- **grok**：cmux 写 `~/.grok/hooks/cmux-session.json`（6 个事件：SessionStart/SessionEnd/Stop/UserPromptSubmit/Notification/PreToolUse），通过 socket 转发，受 `CMUX_GROK_HOOKS_DISABLED=1` 控制。

`NODE_OPTIONS=--require restore-node-options.cjs`（仅 claude）**不是拦截**——那 9 行脚本只把 `NODE_OPTIONS` 还原成用户原始值（`CMUX_ORIGINAL_NODE_OPTIONS`），防止 cmux 的 `--max-old-space-size=4096` 等泄漏到 claude 的子进程。它不 patch 模块、不拦截 API。

因此删除第三方（如 SuperSet）写入 settings 的 hooks 与 cmux 互不影响——cmux 走每次启动的命令行注入，不依赖 `~/.claude/settings.json` 或 `~/.codex/hooks.json` 里的内容。

> 注：初版调查曾据 `NODE_OPTIONS=--require` 的表象误判为"进程内 require 拦截、不靠 hooks"，阅读 `cmux-claude-wrapper`（~1060 行）与 `cmux-codex-wrapper`（~290 行）后订正为"命令行动态注入各 agent 自带的 hooks"。
