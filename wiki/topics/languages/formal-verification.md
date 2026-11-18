---
title: 形式化验证
description: 用数学模型或定理证明确保程序满足规约的方法，包括定理证明、TLA+ 模型检验、符号执行与 Proof Assistant。
type: topic
category: languages
created: 2026-11-18
updated: 2026-11-18
timestamp: 2026-11-18
tags:
  - formal-verification
  - tla-plus
  - lean
  - programming-languages
source_refs:
  - raw/sources/nju-se-software-quality-2.md
---

# 形式化验证

软件测试只能证明 Bug 存在，无法穷举所有路径来证明“没有 Bug”。形式化验证（Formal Verification）的目标是把程序的规约（Specification）和行为写成精确的数学对象，通过**穷举状态空间**、**求解路径方程**或**公理化推导证明**，在逻辑意义上保证程序满足给定性质（如永不崩溃、内存不越界、并发协议不死锁）。

## 四条主要技术路线

| 路线 | 代表工具 / 案例 | 核心做法 | 代价与限制 |
| --- | --- | --- | --- |
| **定理证明（Hoare 逻辑）** | `{P} C {Q}`、循环不变式 | 从前置条件出发，用公理规则推导程序终止后必满足后置条件 | 对带指针的数据结构或复杂算法，人工构造循环不变式难度极高 |
| **Model-Based** | TLA+（如 2PC 共识建模） | 抽取出几十到数百状态的简化状态机模型，穷举所有路径验证不变量 | 模型正确不代表代码正确，需通过 Refinement Mapping 衔接真实代码 |
| **Path-Based** | KLEE（符号执行） | 把程序指令与分支条件列成数学方程，交给 SMT 求解器解出可行路径 | 依赖中间表示（如 LLVM IR）建模，容易遭遇路径爆炸 |
| **Proof-Based** | CompCert、seL4、Lean / Coq | 直接对真实代码或编译器写出机器可检验的数学证明 | 传统模式成本极高（seL4 耗费 25 人年、20 万行证明脚本） |

## Model-Based 与 Refinement Mapping

真实程序状态空间太大，直接穷举会引发状态爆炸。TLA+ 的做法是只对核心逻辑建立极简状态机模型（例如把自动售货机抽象成余额状态的有限跳转，或把分布式事务抽象成提交/中止），在几十到几百个状态内用 BFS/DFS 暴力验证不存在坏状态。

要解决“模型对了，但代码没按模型跑”的落差，需要 **Refinement Mapping（精化映射）**：

- **模型对模型**：定义一个映射函数，证明低层细化协议（如包含网络重传的两阶段提交 `TwoPhase.tla`）每走一步，映射上去要么是高层规约（`TCommit.tla`）的一步合法迁移，要么保持高层状态不变（空步）。
- **模型对真实代码（工程落地）**：
  1. **Trace Validation**：让真实代码在关键状态迁移处输出结构化日志，把运行轨迹按映射规则翻译回 TLA+ 变量，检查这条真实轨迹是否落在模型允许的路径内。
  2. **Model-Based Testing**：从验证过的模型中采样出极端并发交错序列，翻译成真实代码的测试用例或故障注入脚本。

## Proof Assistant、Curry-Howard 同构与 AI 拐点

1. **确定性的裁判机制**：在 Lean / Coq 等 Proof Assistant 中，每一步推导都必须显式声明所用的公理或规则，由内核逐字核对，杜绝跳步。这种“非对即错”的严格反馈非常适合用于训练强化学习模型，使生成数万行证明脚本从极稀缺的人类脑力劳动转化为算力成本。
2. **Curry-Howard 同构（命题即类型，证明即程序）**：在 Lean 4 中，证明“对任意输入 `x` 存在满足性质 `P` 的输出 `y`”等价于写出一个构造函数；归纳证明的结构与递归函数一一对应。开发者可以在同一门语言里同时写可执行函数（`def`）与性质证明（`theorem`）。
3. **编译与证明擦除（Proof Erasure）**：Lean 4 编译器会先校验 `theorem` 成立，随后在生成 C 代码并编译为原生二进制时把证明项全部擦除，只保留计算逻辑。这也让 **Proof-Carrying Code**（代码自带可在编译期校验的证明，验证不过则拒绝编译）重新具备了工程可行性。

## 边界：`Intent → Spec` 依然没有银弹

即使 AI 大幅压低了 `Impl ↔ Spec` 的证明成本，形式化验证依然无法解决软件工程最上游的困难——**Autoformalization（把模糊人类意图翻译成精确规约）**：

- 依赖主观体验的需求（如动画是否自然舒适、系统是否符合预期）难以写成无歧义的数学公式。
- 模型在形式化目标时可能出现“偷偷弱化定理条件再将其证出”的偏差，因此仍需要可执行的软件测试来反向校验形式化定义是否符合原意。

## 相关页面与来源

- [[wiki/topics/architecture/software-engineering|软件工程]]
- [[wiki/topics/languages/lambda-calculus|Lambda 演算]]
- [nju-se-software-quality-2.md](raw/sources/nju-se-software-quality-2.md)
