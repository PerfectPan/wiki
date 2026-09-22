#!/usr/bin/env bash
# 校验 PR 标题是否符合 Conventional Commits：type(scope): 描述
# 用法：
#   tests/pr-title.sh 'docs(systems): xxx'   # 直接传标题
#   PR_TITLE='docs: xxx' tests/pr-title.sh   # 或走环境变量（CI）
#   tests/pr-title.sh --self-test            # 内置正反用例自测

set -euo pipefail

PATTERN='^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test|synthesis)(\([a-z0-9-]+\))?!?: .+'

check_title() {
  local title="$1"
  if [[ -z "$title" ]]; then
    echo "::error::PR title is empty" >&2
    return 1
  fi
  if [[ "$title" == *"《"* || "$title" == *"》"* ]]; then
    echo "::error::PR title 不应包含书名号《》: $title" >&2
    return 1
  fi
  if [[ ! "$title" =~ $PATTERN ]]; then
    cat >&2 <<EOF
::error::PR title 不符合 Conventional Commits 规范: $title
要求格式: type(scope): 描述
  type  ∈ build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test|synthesis
  scope 可选，小写，如 (systems)、(bin)
 标题中不要使用书名号《》
示例: docs(systems): 新增 RPC 分层 synthesis
      fix(bin): 修复 ...
EOF
    return 1
  fi
}

if [[ "${1:-}" == "--self-test" ]]; then
  pass() { echo "ok: $1"; }
  fail_self() { echo "FAIL: $*" >&2; exit 1; }

  for good in \
    'docs(systems): 容器资源隔离' \
    'fix(bin): bin/wiki 在外层 package.json 下无法执行' \
    'synthesis: 判据页收录案例' \
    'docs: 补充 Git 认证说明' \
    'feat(skills)!: 重写 skill 入口'
  do
    check_title "$good" >/dev/null 2>&1 || fail_self "合法标题被拒: $good"
    pass "$good"
  done

  for bad in \
    '新增 synthesis：RPC 边界' \
    'docs(systems) 缺冒号' \
    'wip: 不支持的 type' \
    'docs(Systems): scope 大写' \
    'docs(systems): 标题带《书名号》'
  do
    if check_title "$bad" >/dev/null 2>&1; then
      fail_self "非法标题通过: $bad"
    fi
    echo "ok(拒绝): $bad"
  done
  echo "pr-title self-test passed"
  exit 0
fi

title="${1:-${PR_TITLE:-}}"
check_title "$title"
