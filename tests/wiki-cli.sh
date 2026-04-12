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

agents_text="$(cat "$ROOT/AGENTS.md")"
assert_contains "$agents_text" "bin/wiki ingest <source>"
assert_contains "$agents_text" "bin/wiki query <question>"
assert_contains "$agents_text" "bin/wiki lint"
assert_contains "$agents_text" "bin/wiki migrate <logseq-page>"

help_output="$("$CLI" help)"
assert_contains "$help_output" "ingest"
assert_contains "$help_output" "query"
assert_contains "$help_output" "lint"
assert_contains "$help_output" "migrate"

ingest_output="$("$CLI" ingest deep-research-report.md)"
assert_contains "$ingest_output" "操作：ingest"
assert_contains "$ingest_output" "AGENTS.md"
assert_contains "$ingest_output" "SCHEMA.md"
assert_contains "$ingest_output" "log.md"

query_output="$("$CLI" query "什么是 vault")"
assert_contains "$query_output" "操作：query"
assert_contains "$query_output" "优先只读 wiki/"
assert_contains "$query_output" "synthesis"

lint_output="$("$CLI" lint)"
assert_contains "$lint_output" "操作：lint"
assert_contains "$lint_output" "重复页面"
assert_contains "$lint_output" "来源指针"

migrate_output="$("$CLI" migrate '/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/pages/Logseq.md')"
assert_contains "$migrate_output" "操作：migrate"
assert_contains "$migrate_output" "journals 默认不迁移"
assert_contains "$migrate_output" "topics"

echo "PASS"
