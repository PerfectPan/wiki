#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLI="$ROOT/bin/wiki"
CLI_TS="$ROOT/bin/wiki.ts"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

assert_contains() {
  local haystack="$1"
  local needle="$2"
  if [[ "$haystack" != *"$needle"* ]]; then
    fail "expected output to contain: $needle"
  fi
}

[[ -f "$CLI_TS" ]] || fail "expected TypeScript CLI at $CLI_TS"
[[ ! -d "$ROOT/.codex/skills" ]] || fail "project-local skills should not exist"

if git -C "$ROOT" rev-parse --verify origin/main >/dev/null 2>&1; then
  changed_files="$(git -C "$ROOT" diff --name-only origin/main --)"
  if [[ "$changed_files" == "log.md" || "$changed_files" == *$'\nlog.md' || "$changed_files" == *$'\nlog.md\n'* || "$changed_files" == *'log.md'$'\n'* ]]; then
    fail "log.md is historical and must not be modified; put change notes in the PR body"
  fi
fi

agents_text="$(cat "$ROOT/AGENTS.md")"
assert_contains "$agents_text" "bin/wiki ingest"
assert_contains "$agents_text" "bin/wiki check"
assert_contains "$agents_text" ".agents/skills"

help_output="$("$CLI" help)"
assert_contains "$help_output" "ingest"
assert_contains "$help_output" "check"

# ingest 命令：抓取来源（本地文件不抓取，直接返回）
"$CLI" ingest deep-research-report.md >/dev/null

# check 命令：对合法页面应返回 0
check_output="$("$CLI" check wiki/topics/ai/MCP.md 2>&1)" || true
assert_contains "$check_output" "校验完成"

# check 命令：全量校验不应有 error（只有 warning）
full_check_output="$("$CLI" check 2>&1)" || true
assert_contains "$full_check_output" "0 个错误"

echo "PASS"
