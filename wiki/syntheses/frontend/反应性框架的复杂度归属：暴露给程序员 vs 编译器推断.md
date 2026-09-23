---
title: 反应性框架的复杂度归属：暴露给程序员 vs 编译器推断
description: 从 Solid 2 与 Octane 作者的正面交锋中提炼——复杂度应显式暴露给程序员（运行时可检视）还是交给编译器推断，以及多准则打分的重复计数陷阱与 agent 时代的新变量
type: synthesis
category: frontend
created: 2026-09-23
updated: 2026-09-23
timestamp: 2026-09-23
tags:
  - reactivity
  - signals
  - compiler
  - react
source_refs:
  - raw/sources/2026-09-23-solid-2-vs-octane.md
  - https://gist.github.com/aleclarson/0f4266d63fd83c7a5ea5512441bbea0c
resource:
  - raw/sources/2026-09-23-solid-2-vs-octane.md
  - https://gist.github.com/aleclarson/0f4266d63fd83c7a5ea5512441bbea0c
---

# 反应性框架的复杂度归属：暴露给程序员 vs 编译器推断

## 问题

2026 年 8 月，aleclarson 发了一篇 gist，让 ChatGPT 用 9 条「Renderer DX Pillars」对比两个下一代渲染器：Octane（Dominic Gannaway / trueadm，前 React 核心团队，Inferno / Prepack / Ripple 的作者）和 Solid 2（Ryan Carniato / ryansolid）。原帖判了 7:2，结果两位框架作者本人下场在评论区交锋了四天。

这页回答：这场争论的核心分歧到底是什么？哪些结论超出了两个框架本身、值得作为通用判断沉淀？

## 简答

核心分歧是**复杂度归属**：Solid 2 把依赖关系（包括异步）做成运行时真实存在、可检视的图，复杂度显式暴露给程序员；Octane 让你写普通代码，由编译器推断并恢复依赖、缓存、并发信息。争论沉淀出的最锋利结论是：**被推断掉的复杂度不会消失，只是从「随时可检视」变成「出事才现形」——而「系统对应用的知识能否存活到运行时」这个性质，会随应用变复杂而复利。**

## 来源事实

按时间顺序列关键事实，判断见下一节。

- **原帖（aleclarson）**：9 条 pillars 判 Solid 2 以 7:2 胜出；Octane 仅赢「组件书写体验」（`count * 2` 就是普通代码，不用 `() => count() * 2`）和「生态互操作」。作者的直觉轨迹图：小应用两者接近，应用越复杂、状态关系越多，Solid 的优势越大——因为「Solid 的抽象更接近被建模的问题本身」。
- **trueadm 首轮反驳（08-14）**：9 条里有 4 条（state architecture、reactive reasoning、derived state、architectural scaling）实际是同一个偏好——「细粒度图是不是应用的基本架构」——的四次重复计数。React 的组件/hook 模型已被超大规模验证；Octane 应用不需要把领域状态放组件里：`useSyncExternalStore` 是一等防 tearing 边界，Zustand、Jotai、Redux、MobX、Valtio、TanStack Store、Alien Signals 都有绑定。他对中心问题的回答：编译器「主要是把组件模型写起来更爽更便宜，不会偷偷把 hooks 变成全局 Solid 式图」。
- **aleclarson 让步并重述问题（08-14）**：接受重复计数的批评，撤回「architectural scaling」作为独立支柱；把中心问题从「哪个架构能 scale」改成：**「哪些复杂度你想暴露给程序员，哪些复杂度你想让编译器推断？」**
- **ryansolid 回应（08-17，声明由 Fable 代笔）**：
  - 「暴露的复杂度是可检视的复杂度。被推断的复杂度不会消失，只是变成不可见的，直到它出错——那时『为什么更新了』的答案住在你没写过的地方。」Solid 的依赖图是运行时数据结构：可以走任意节点的 sources/observers、走 ownership 树、订阅诊断流；「从闭包词法捕获了什么来推导依赖，是对运行时问题的构建期回答」。
  - Octane 的并行是编译器**证明**独立之后才并行：其文档自己写明循环被排除、有依赖的创建不 hoist、编译器看不出的 promise 形态运行时回退串行。「Warm less = slower but never wrong 是正确的工程决定——但这意味着并行性是一个优化，其适用性取决于代码形态可不可证明，而不是一个可以依赖的语义。」
  - Solid 2 的 colorless async：每个响应式读取同一个契约——可能未就绪、pending 经派生传播、`isPending`/`latest` 有原子性保证（`[isPending(x), x()]` 一起观察是原子的）。同步信号换异步信号，下游零改动。
  - 外部 store 是**知识边界**：因果链穿不过去，框架的 async/pending/transition 语义停在快照边界；`useSyncExternalStore` 防 tearing 的方式恰恰是把观测粗化成快照。「React 的 scale 故事是两套响应式系统在接缝处缝合，最难的协调问题恰好都住在接缝上。『用第二套响应式系统解决组件引力』恰恰证明细粒度响应式状态才是真正 scale 的东西——问题只是它是原生的还是外挂的。」
  - GC 类比反转：GC 赢得通用内存管理，是因为运行时拥有活跃对象图——可达性是静态分析**证明不可恢复**的运行时性质；escape analysis、region inference 最后都成了运行时系统之上的优化而非替代；唯一真正成功的静态方案 Rust 需要一门更严格的新语言，而且对借用药检查不了的情况仍然让步给运行时（`Rc`、`RefCell`、`Arc` 全是运行时机制）。
- **trueadm 二轮（08-17）**：编译器不许静默猜测——显式依赖数组今天仍是权威（需要时可显式给出）；分析不能安全推断的地方要有清晰契约、保守结果或可操作的报错。设计标准一句话版：**每条限制都要换来一个有用的保证；每个被删掉的 API 都要有更好的方式表达它的正当用途。**`"use strong"`：编译期硬阻断、无 override（不是可以忽略的 linter）；跨模块编译用 TS 原生类型证明跨多层组件的 props 不变。承认 Octane 还缺「把编译器决定了什么和运行时发生了什么连起来」——正是 ryansolid 指出的缺口。agent 时代让更严格的语言约束变得可行：「agent 能拿着一个精确的编译器诊断完成大重构，这让拒绝『局部方便但全局难推理』的模式变得实际。」
- **ryansolid 二轮（08-17）**：时间线考据——colorless 模型 2023-08 落在他们 signals repo，早于 runes 公布；Svelte 5 的 `$derived` 里写 `await` 仍是显式 color。agents 论证是双向的：agent 也让「上手 API 熟悉度」不再值钱；而且「agent 调试一个运行中的应用时，问的是运行时问题：为什么这个还在 pending、这个 transition 在等什么、这个为什么更新了两次。诊断信息解释的是编译器没能证明什么；它不解释应用刚刚做了什么。」
- **ryansolid 三轮（08-18，"This time no AI"）**：他反对十多年的不是 React 的实现，是 React 的**模型**；类比 immediate mode vs retained mode。「编译器是最后一阶段的优化——你得先知道自己在构建什么。Svelte 是教科书案例：他们有编译器，然后发现模型不完整。」Solid 十年不换模型的记录源于此。
- **trueadm 收尾（08-18）**：「社区已经没有接纳新框架的胃口了。」某前 Google 资深工程师的原话：对 Ripple 感兴奋但不会离开 React，因为「让 agent 修 React 的性能问题，最后基本都能修好」，迁移路径不值。signals 在 Octane 里也扮演重要角色（官方推荐 Alien Signals 或 Jotai/Zustand）；`"use strong"` 会检测 `useState` 的问题用法并把人推向 signals、状态机或 context。

## 综合结论

1. **多准则打分会因「重复计数」产生假压倒性。** 9 条 pillars 里有 4 条其实是同一偏好的不同投影，于是 7:2 的悬殊比分很大程度是评估器自己的 artifact，不是对象的真实差距。任何 scored rubric（框架选型、工具评审、模型评测）都应先做维度相关性归并，再谈打分。本案例的难得之处在于：作者被指出后当场认账并重新表述了问题。
2. **被推断掉的复杂度不会消失，只是从「可检视」变成「出事才现形」。** 这是全篇最锋利的一句：「Exposed complexity is inspectable complexity.」构建期推断是对运行时问题的构建期回答。评估一切「编译器帮你搞定」类方案（React Compiler、_AUTO_、各种魔法化优化）的第一判据应当是：**它失败的时候，我能不能看到它失败了、为什么。**
3. **GC 的历史给出了「静态 vs 运行时」之争的稳定均衡形态。** 运行时拥有图、静态分析做优化不做替代——这是内存管理打完的仗。唯一纯静态的成功（Rust）付出了一门新语言的代价，且仍把不可证明的情况让回运行时。映射过来：编译器路线的终局很可能是「更严格的新语言/新模式」（`"use strong"` 正在走这条路），而一旦如此，「React 知识直接迁移」的卖点就不再成立——两条路线最终要在「语义住在运行时的指定图里，还是住在编译器的分析里」正面竞争。
4. **外部 store 边界是知识边界，不只是工程边界。** React 生态的 scale 方案（领域状态放 Zustand/MobX，组件做订阅边界）确实可行且被验证，但因果链和 async/pending 语义在快照边界断掉。同一个事实有两种读法：「外挂证明组件模型不设限」或「外挂恰恰说明原生细粒度才是终局」。分歧点在接缝处：最难的问题恰好都住在两套系统的缝合线上。
5. **Agent 同时削弱两边的传统卖点，但方向不对称。** 被削弱的：「上手熟悉度」的价值（agent 学新模型无怨言）、「人写代码的手感」。被强化的：「编译期硬约束」的可行性（agent 能消化精确诊断的大重构）。但 agent 调试运行中的应用时问的是运行时问题——所以**运行时可检视性在 agent 时代的价值是上升而非下降**。同时有个务实反例：trueadm 亲眼见到 agent 直接在编译产物里插 `console.log` 修好了 bug，根本不在乎源码和产物不一致——「源码可读性」对 agent 的意义可能被高估。
6. **AI 正在改变框架迁移的经济学，且方向不利于新框架。** agent 降低了「留在旧框架持续打补丁」的边际成本，让它低于「迁移到更好模型」的一次性成本。社区对新框架失去胃口不是审美疲劳，而是理性计算变了。新框架的卖点必须变成：「好到迁移路径 watertight」，或者「好到用户的 agent 会主动建议迁移」——trueadm 原话：「or at least their agent will tell them they should.」

## 对个人/项目的启发

- 评估框架/工具/模型时，先把评估维度做相关性归并再打分；本页事实层的 7:2 就是现成的反面教材。
- 选「编译器魔法」类方案时，把「出问题时我能看到什么」作为第一判据，而不是「写起来顺不顺手」。
- 给 agent 用的系统，优先提供两种能力：精确的、可操作的诊断（agent 能照着修）；运行时可查询的状态（agent 调试时问的是运行时问题）。这两点分别对应 Octane 和 Solid 各自押注的方向。
- API/产品契约设计可以直接抄 trueadm 的标准：每条限制都要换来一个有用的保证；每个被删掉的 API 都要有更好的方式表达它的正当用途。
- 做技术判断时警惕「用第二套系统补第一套系统的洞」：它既可以是务实的胜利，也可能是把根本问题推迟到接缝处，两种读法要对等摆出来再下结论。

## 相关页面

- [[前端框架的四个时代]]——这场争论所处的模型谱系位置
- [[Code Agent 结构约定的可验证边界]]——编译器诊断 + agent 可修复性的同族问题
- [[State Management]]——外部 store 与响应式图的边界在实践中的形态

## 来源指针

- raw/sources/2026-09-23-solid-2-vs-octane.md（原帖 + 8 条评论全文，2026-08-14 ~ 08-18）
- https://gist.github.com/aleclarson/0f4266d63fd83c7a5ea5512441bbea0c
- 评论中引用的一手材料：Octane 的 [suspense 并行计划](https://github.com/octanejs/octane/blob/main/docs/suspense-parallel-use-plan.md) 与 [bindings 状态](https://github.com/octanejs/octane/blob/main/docs/bindings-status.md)；创作者观点摘要见[作者另一篇 gist](https://gist.github.com/aleclarson/829c10aa7d287944ef75e1c2a90bef06)
