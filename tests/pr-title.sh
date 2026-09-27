#!/usr/bin/env bash
# Kept for callers that only validate a Conventional Commits title.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ "${1:-}" == "--self-test" ]]; then
  exec node "$ROOT/tests/pr-metadata.mjs" --self-test
fi
exec node "$ROOT/tests/pr-metadata.mjs" --title "${1:-${PR_TITLE:-}}"
