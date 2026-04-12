---
title: Hash
type: topic
category: algorithms
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - include
source_refs:
  - raw/sources/Hash.md
---
# Hash

- 多项式 Hash：将字符串看作是某个进制下（Base）下的数字串
	- $$\begin{align*}H(S)&=\sum_{i=1}^{i\le |S|=n} S[i]*Base^{n-i} \\ &= S[1] * Base^n+S[2]*Base^n-1+\cdots +S[n]*Base^0 \end{align*}$$
	- 优点：字符串和 Hash 值一一对应，不会发生 Hash 冲突（Base 要比字符集大）
	- 缺点：数字范围过大，难以用原始数据结构存储和比较（如果用高精度，那么和直接比较串没有区别了）
- 多项式取模 Hash：为了解决多项式 Hash 的缺点，在效率和冲突率之间的折衷，将多项式 Hash 值对一个较大的质数取模
- 生日悖论：
	- 有 $n$ 个人，每个人的生日可以认为是 [1, 365] 范围内的随机整数
	- 若 $n > 365$，则一定有两个人的生日相同
	- 若 $n \le 365$，则没有人生日相同的概率为：$$\frac{A(365,n)}{365^n}$$
	- 当 $n=23$ 时，上述结果为 0.46。即有超过 50% 的概率有人生日相同
	- 这指引我们当随机检验次数超过 $$\sqrt{Mod}$$ 时，就有较大概率错误
	- 因此，在多项式取模 Hash 中使用的模数最好超过 Hash 检验次数的平方
- Hash 模数：
	- 优秀的 Hash 模数首先应该满足：足够大
	- 自然溢出：$$2^{64}$$，容易构造 Hash 冲突
	- 优秀的 Hash 模数还应该是一个质数：选取 $$10^9-10^{10}$$ 范围的大质数作为模数（乘法不会溢出，也保证范围在 int），但也有广为人知的方法构造冲突
	- 双模：进行多次不同质数的单模。在不泄漏模数的前提下，没有已知方法可以构造冲突
- 子串 Hash：$$H(S[l,r])=F(r)-F(l-1)*Base^{r-l+1}$$
	- $$F(i)=H(Prefix[i])$$
- ```cpp
  #include <random>
  mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());

  int rnd(int x, int y) {
      return uniform_int_distribution<int>(x, y)(rng);
  }

  int MOD = 998244353 + rnd(0, 1e9), BASE = 233 + rnd(0, 1e3);

  struct HashSeq {
      vector<long long> P, H;

      HashSeq() {}

      HashSeq(string &s) {
          int n = s.size();
          P.resize(n + 1);
          P[0] = 1;
          for (int i = 1; i <= n; i++) P[i] = P[i - 1] * BASE % MOD;
          H.resize(n + 1);
          H[0] = 0;
          for (int i = 1; i <= n; i++) H[i] = (H[i - 1] * BASE + s[i - 1]) % MOD;
      }

      long long query(int l, int r) {
          return (H[r] - H[l - 1] * P[r - l + 1] % MOD + MOD) % MOD;
      }
  };
  ```

## Source Pointers

- `raw/sources/Hash.md`

