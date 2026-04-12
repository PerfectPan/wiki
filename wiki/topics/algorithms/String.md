---
title: String
type: topic
category: algorithms
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - string
source_refs:
  - raw/sources/String.md
---
# String

- $S[i]$: 表示字符串 $S$ 第 $i$ 个位置的字母，下标从 1 开始
- $\rm{Prefix}_S[i]$: 表示字符串 $S$ 的长度为 $i$ 的前缀，$$\rm{Prefix}_S[i]=S[1,i]$$
- $\rm{Suffix}_S[i]$: 表示字符串 $S$ 的长度为 $i$ 的前缀，$$\rm{Suffix}_S[i]=S[|S|-i+1,i]$$
- Border：如果字符串 $S$ 的同长度的前缀和后缀完全相同，即 $$\rm{Prefix}[i]=\rm{Suffix}[i]$$，则称此前缀（后缀）为一个 Border
	- 特殊地，字符串本身也可以是它的 Border，具体是不是根据语境判断
	- 不具有二分性
	- 传递性：$S$ 的 Border 的 Border 也是 $S$ 的 Border
	- 周期定理：若 $p,q$ 均为串 $S$ 的周期，则 $(p,q)$ 也为 $S$ 的周期
	- 一个串的 Border 数量是 $O(N)$ 个，但他们组成了 $O(\rm{log}N)$ 个等差数列
- 周期：对于字符串 $S$ 和正整数 $p$，如果有 $$S[i]=S[i-p]$$，对于 $p<i\le |S|$成立，则称 $p$ 为字符串 $S$ 的一个周期
	- 特殊地，$$p=|S|$$ 一定是 $S$ 的周期
- 循环节：若字符串 $S$ 的周期 $p$ 满足 $$p\mid|S|$$，则称 $p$ 为 $S$ 的一个循环节
	- 特殊地，$$p=|S|$$ 一定是 $S$ 的循环节
- $p$ 是 $S$ 的周期等价于 $$|S|-p$$ 是 $S$ 的 Border
- [[KMP]]
- [[Hash]]
- 判定两个串的字典序等价于求解两个串的最长公共前缀（LCP）
	- 后缀数组 SA，复杂度 $$O(n\rm logn)$$
	- LCP 满足二分性，问题转化为判断两个子串是否相等，可以用 [[Hash]] 解决，时间复杂度 $$O(n\rm log n)$$
- [[Trie]]
- [[Border Tree]]
-

## Source Pointers

- `raw/sources/String.md`

