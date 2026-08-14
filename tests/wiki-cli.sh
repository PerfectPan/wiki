#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLI="$ROOT/bin/wiki"
CLI_JS="$ROOT/bin/wiki.js"

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

[[ -f "$CLI_JS" ]] || fail "expected CLI at $CLI_JS"
[[ ! -d "$ROOT/.codex/skills" ]] || fail "project-local skills should not exist"

if git -C "$ROOT" rev-parse --verify origin/main >/dev/null 2>&1; then
  changed_files="$(git -C "$ROOT" diff --name-only origin/main --)"
  if [[ "$changed_files" == "log.md" || "$changed_files" == *$'\nlog.md' || "$changed_files" == *$'\nlog.md\n'* || "$changed_files" == *'log.md'$'\n'* ]]; then
    fail "log.md is historical and must not be modified; put change notes in the PR body"
  fi
fi

agents_text="$(cat "$ROOT/AGENTS.md")"
assert_contains "$agents_text" "bin/wiki ingest <source>"
assert_contains "$agents_text" "bin/wiki query <question>"
assert_contains "$agents_text" "bin/wiki research <topic>"
assert_contains "$agents_text" "bin/wiki lint"
assert_contains "$agents_text" "bin/wiki migrate <logseq-page>"
assert_contains "$agents_text" "bin/wiki check"

help_output="$("$CLI" help)"
assert_contains "$help_output" "ingest"
assert_contains "$help_output" "query"
assert_contains "$help_output" "research"
assert_contains "$help_output" "lint"
assert_contains "$help_output" "migrate"
assert_contains "$help_output" "check"

ingest_output="$("$CLI" ingest deep-research-report.md)"
assert_contains "$ingest_output" "操作：ingest"
assert_contains "$ingest_output" "AGENTS.md"
assert_contains "$ingest_output" "SCHEMA.md"
assert_contains "$ingest_output" "PR body"

query_output="$("$CLI" query "什么是 vault")"
assert_contains "$query_output" "操作：query"
assert_contains "$query_output" "优先只读 wiki/"
assert_contains "$query_output" "synthesis"

research_output="$("$CLI" research "OpenDesign vs Claude Design")"
assert_contains "$research_output" "操作：research"
assert_contains "$research_output" "系统架构图"
assert_contains "$research_output" "核心数据流"
assert_contains "$research_output" "扩展面"
assert_contains "$research_output" "证据矩阵"
assert_contains "$research_output" "PR"

lint_output="$("$CLI" lint)"
assert_contains "$lint_output" "操作：lint"
assert_contains "$lint_output" "重复页面"
assert_contains "$lint_output" "来源指针"

migrate_output="$("$CLI" migrate '/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/pages/Logseq.md')"
assert_contains "$migrate_output" "操作：migrate"
assert_contains "$migrate_output" "journals 默认不迁移"
assert_contains "$migrate_output" "topics"

# check 命令：对合法页面应返回 0
check_output="$("$CLI" check wiki/topics/ai/MCP.md 2>&1)" || true
assert_contains "$check_output" "校验完成"

# check 命令：全量校验不应有 error（只有 warning）
full_check_output="$("$CLI" check 2>&1)" || true
assert_contains "$full_check_output" "0 个错误"

echo "PASS"
