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

# bin/wiki.ts 是 ESM，而仓库本身没有构建步骤，模块类型完全依赖根 package.json 的
# type 字段（Node 会向上找最近的 package.json，找不到就按 CommonJS 解析 .ts）。
if ! grep -q '"type"[[:space:]]*:[[:space:]]*"module"' "$ROOT/package.json"; then
  fail 'root package.json must declare "type": "module" for bin/wiki.ts'
fi

# 回归：仓库被放在含 package.json{"type":"commonjs"} 的目录下时，CLI 仍必须能执行。
# 仓库自己没有 type 字段的时候，这里会命中外层 package.json，
# bin/wiki 会报 "Cannot use import statement outside a module" 而彻底跑不起来。
# 原仓库只能靠 cwd 在仓库内跑才正常，所以 CI 的干净检出复现不到。
ancestor_probe="$(mktemp -d)"
mkdir -p "$ancestor_probe/project"
cp -R "$ROOT/bin" "$ancestor_probe/project/bin"
cp "$ROOT/package.json" "$ancestor_probe/project/package.json"
printf '{"type":"commonjs"}' >"$ancestor_probe/package.json"
probe_output="$("$ancestor_probe/project/bin/wiki" help 2>&1)" \
  || fail "CLI failed when an ancestor package.json declares type=commonjs: $probe_output"
assert_contains "$probe_output" "check"
rm -rf "$ancestor_probe"

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

# PR 标题 lint：内置正反用例自测
bash "$ROOT/tests/pr-title.sh" --self-test >/dev/null

# prompts 命令
help_output="$("$CLI" help)"
assert_contains "$help_output" "prompts"

prompts_list="$("$CLI" prompts list)"
assert_contains "$prompts_list" "seed-string"
assert_contains "$prompts_list" "推荐"

prompts_tagged="$("$CLI" prompts list --tag design)"
assert_contains "$prompts_tagged" "seed-string"
if [[ "$prompts_tagged" == *"plan-first"* ]]; then
  fail "prompts list --tag design 不应包含 plan-first"
fi

prompts_json="$("$CLI" prompts list --tag design --json)"
assert_contains "$prompts_json" '"id": "seed-string"'

prompts_show="$("$CLI" prompts show seed-string)"
assert_contains "$prompts_show" "random alphanumeric string"
if [[ "$prompts_show" == *'```'* ]]; then
  fail "prompts show 不应带代码块包装，应直接打印原文"
fi

prompts_search="$("$CLI" prompts search 随机)"
assert_contains "$prompts_search" "negative-random-ask"

prompts_check="$("$CLI" prompts check 2>&1)" || fail "prompts check 不应失败: $prompts_check"
assert_contains "$prompts_check" "0 个错误"

prompt_file_check="$("$CLI" check prompts/seed-string.md 2>&1)" || true
assert_contains "$prompt_file_check" "校验完成"

# 坏提示词必须被拦下：在临时仓库里跑，不动真实 prompts/
prompt_probe="$(mktemp -d)"
mkdir -p "$prompt_probe/project/prompts" "$prompt_probe/project/wiki/topics/ai"
cp -R "$ROOT/bin" "$prompt_probe/project/bin"
cp "$ROOT/package.json" "$prompt_probe/project/package.json"
printf '# Awesome Prompts\n' >"$prompt_probe/project/wiki/topics/ai/Awesome Prompts.md"
probe_cli="$prompt_probe/project/bin/wiki"

write_prompt() { # <文件名> <id> <level> <正文>
  printf -- '---\nid: %s\ntitle: t\nscene: s\nlevel: %s\ntags:\n  - t\nsource: x\nadded: 2026-09-22\n---\n\n%s\n' \
    "$2" "$3" "$4" >"$prompt_probe/project/prompts/$1"
}

write_prompt good.md good 推荐 hello
"$probe_cli" prompts check >/dev/null 2>&1 || fail "合法提示词应通过 prompts check"

write_prompt bad-id.md other 推荐 hello
"$probe_cli" prompts check >/dev/null 2>&1 && fail "id 与文件名不一致时 prompts check 应失败"
rm "$prompt_probe/project/prompts/bad-id.md"

write_prompt bad-level.md bad-level 一般 hello
"$probe_cli" prompts check >/dev/null 2>&1 && fail "level 非法时 prompts check 应失败"
rm "$prompt_probe/project/prompts/bad-level.md"

write_prompt empty.md empty 推荐 ""
"$probe_cli" prompts check >/dev/null 2>&1 && fail "正文为空时 prompts check 应失败"
rm -rf "$prompt_probe"

echo "PASS"
