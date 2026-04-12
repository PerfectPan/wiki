---
title: Trie
type: topic
category: algorithms
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - trie
source_refs:
  - raw/sources/Trie.md
---
# Trie

- 字典：一个字符串的集合
- 字典串：在字典里的串
- Trie 是一棵有根树，每个点至多有 $$|\Sigma|$$ 个后继边，每条边上有一个字符
- 每个点表示一个前缀：从根到这个点的边上的字符顺次连接形成的字符串
- 每个点还有一个终止标记：是否这个点代表的字符串是一个字典串
- 支持向 Trie 插入新字典串，删除字典串，查询某字符串是否是字典串
- 支持可持久化
- 0-1 Trie：即对字符集只有 2 的字典串构建的 Trie，常来解决 01 二进制串相关的字典序或者计数问题
	- 最大区间异或和：
		- 求出异或前缀和，每个区间的异或和就可以表示成两个前缀和的异或
		- 问题转化为 $n+1$ 个数字中选两个做异或运算的最大值
		- 将数字插入 01 Trie 中，枚举 $x$，从高到低考虑 $x$ 的每一个二进制位 $bit$，在 01 Trie 上寻找 $y$：从根出发，如果有 $!bit$ 边，则走 $!bit$ 边，否则只能走 $bit$ 边，这样贪心的找
- https://leetcode.cn/problems/extra-characters-in-a-string/
	- 连续查询一个字符串每个位置为结尾的子串是否在字典里可以用 Trie 来优化查询，而不是直接用哈希表

## Source Pointers

- `raw/sources/Trie.md`

