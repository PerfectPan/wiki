---
title: Border Tree
type: topic
category: algorithms
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - border
  - tree
source_refs:
  - raw/sources/Border Tree.md
---
# Border Tree

- 对于一个字符串 $S$, $$n = |S|$$，它的 Border 树共有 $n+1$ 个节点：0, 1, 2, ..., n
- 0 是这棵有向树的根，对于其他每个点 $$1\le i\le n$$，父节点为 $$next[i]$$
- 性质：
	- 每个前缀 $$Prefix[i]$$ 的所有 Border：节点 $i$ 到根的链
	- 哪些前缀有长度为 $x$ 的 Border：$x$ 的子树
	- 求两个前缀的公共 Border 等价于求 [[LCA]]
-

## Source Pointers

- `raw/sources/Border Tree.md`
