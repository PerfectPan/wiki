---
title: Rolldown
type: topic
category: tooling
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - rolldown
source_refs:
  - raw/sources/Rolldown.md
---
# Rolldown

- `RD_LOG=debug ../../packages/rolldown/bin/cli.js`
- just 就是类似 makefile 的东西，可以管理命令
- `cargo test -p rolldown --test esbuild` 测试 rolldown/esbuild 下的测试用例，可以再细化到单个测试用例
	- `cargo test -p rolldown --test esbuild -- test_tests__esbuild__splitting__hybrid_esm_and_cjs_issue617__config_json` __ 表示进入新的文件夹
-

## Source Pointers

- `raw/sources/Rolldown.md`
