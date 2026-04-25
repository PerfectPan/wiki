---
title: KMP
type: topic
category: algorithms
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - kmp
source_refs:
  - raw/sources/KMP.md
---
# KMP

- $\rm{next}[i]=\rm{Prefix[i]}$ 的非平凡最大 Border
- $\rm{next}[1] = 0$
- ![CleanShot 2023-10-18 at 22.50.11@2x.png](../../../raw/assets/CleanShot_2023-10-18_at_22.50.11@2x_1697640619385_0.png)
- $\rm{Prefix}[i]$ 的所有 Border 去掉最后一个字母一定是 $$\rm{Prefix}[i-1]$$ 的 Border，反过来推不出来，一般这时候可以遍历后者去检验合法性来求
- ![CleanShot 2023-10-18 at 23.22.34@2x.png](../../../raw/assets/CleanShot_2023-10-18_at_23.22.34@2x_1697642560323_0.png)
	- 求出 $T$ 的 Border，然后匹配 $S$ 的时候失配就跳 Border 继续匹配

## Source Pointers

- `raw/sources/KMP.md`
