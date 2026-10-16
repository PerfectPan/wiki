---
title: DDD
description: 系统梳理 DDD 核心心智模型、五型战略分型、值对象聚合机制与落地五大常见认知误区。
type: topic
category: architecture
created: 2026-04-12
updated: 2026-10-16
tags:
  - ddd
  - domain-driven-design
  - domain-model
  - aggregates
  - value-objects
  - architecture
source_refs:
  - raw/sources/ddd.md
  - https://zhuanlan.zhihu.com/p/585899317
  - https://en.wikipedia.org/wiki/Curry%E2%80%93Howard_correspondence
  - https://www.domainlanguage.com/ddd/reference/
  - https://martinfowler.com/bliki/AnemicDomainModel.html
  - https://dddcommunity.org/library/vernon_2011/
---

# DDD（领域驱动设计）

- 领域驱动设计，是一种自然萌生的软件设计潮流
- 软件里的代码模型，需要反映现实中的问题模型
- 软件迭代是领域模型跟代码模型不断同步的过程
- 软件内的模块依赖关系也应遵循领域之间的关系
- 柯里-霍华德同构给出了从知识到代码的转换方法
- 方法论流程：DomainDD -> TypeDD -> TestDD -> Impl
- 状态所有权决定领域形态：**“这份状态由谁来写”**是决定是否有聚合根与仓储的第一性原则

---

## 核心心智模型：状态所有权与全景五型战略分型

很多团队落地 DDD 感到痛苦的根源，在于试图用同一套“聚合根 + 实体 + 仓储”的战术模板套死全仓所有模块。在宏观架构上，一个系统中的概念天然由**状态所有权与生命周期**划分为 5 种不同形态：

| 类型 | 命名定义 | 典型场景 | 谁拥有写权限 | 状态存活周期 | 锁与互斥机制 | 领域模型形态 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A 型** | **外部事实投影**<br>(External Projection) | 外部日志读取与分析、环境探测 (sessions, discovery) | 外部第三方 Agent<br>(Claude Code/Codex) | 瞬时，随读随算，源变则报 `SourceChanged` | 无。本系统无权干预外部写入 | 纯数据只读快照 (VO) + 防腐层 ACL + 领域折叠计算服务 |
| **B 型** | **纯无状态计算**<br>(Pure Computation) | 费率算费、敏感词脱敏、共享内核 (cost, redact, catalog) | 无状态 | 无 | 无 | 纯原子值对象 + 纯数学/策略函数 |
| **C 型** | **宿主持有状态**<br>(Caller-held State) | 增量扫描状态机、生命周期演进 (UsageScanState) | 下游宿主应用 | 由宿主自己保存 | 宿主应用自己保证单写 | 状态快照 VO + 纯演进函数 `(state, input) -> state` |
| **D 型** | **进程内内存聚合**<br>(In-Memory Aggregate) | 交互会话状态机、执行计划、并发队列 (AcpSession, InstallPlan, Lane) | 本系统（单进程） | 单个执行生命周期 / 作用域 (Scope) | 单线程 + 闭包 Map / WeakMap 句柄防伪造 | 冻结类，状态变迁返回 `{ state, events }` |
| **E 型** | **持久化共享聚合**<br>(Persistent Aggregate) | 配置账本修改、跨进程执行锁互斥 (Ledger, Lease) | 本系统（多进程并发） | 本地磁盘 / 共享存储 | 内核级排他文件锁 (fcntl) + CAS 修订号 | 完整战术 DDD：Aggregate Root + Entity + Repository |

---

## 战术层：值对象（VO）到底是如何被“聚合”的？

在代码层面，将一揽子离散的 Value Objects 组织进一个业务模型，遵循严格的三个阶段：

```text
┌────────────────────────── 领域模型 (Entity / Projection Root) ──────────────────────────┐
│                                                                                          │
│  1. 【组合装配 (Composition)】：作为骨架持有不可变 VO                                      │
│     - 内部属性全由只读值对象搭积木拼装（如 sessionInfo, capabilities, events[], skipped[]） │
│                                                                                          │
│  2. 【跨 VO 规则守卫 (Invariants)】：在工厂/创建阶段把关一致性                              │
│     - 单个 VO 只能自保合法，跨 VO 的规则（如事件时序连续、工具调用与结果成对配对）          │
│       必须由工厂（Factory）在构造时统一建立并保证，而非交给零散的外部代码                 │
│                                                                                          │
│  3. 【行为合成 (Behavior Synthesis)】：消费持有的 VO，合成新的 VO                           │
│     - 业务方法以内部持有的 VO 为原料，经过领域折叠运算，输出衍生快照 VO（如 SessionSummary） │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 落地中的五大常见认知误区

1. **误区一：把“方法挂在对象上”误当成“聚合根”**  
   聚合根的核心使命是**划定写事务边界，在状态突变（Mutation）中强一致地守护业务不变量**。对于只读查询场景，没有命令和状态流转，强立聚合根属于概念空转。
2. **误区二：把“读取本地文件（如 .jsonl）”误当成“仓储（Repository）”**  
   外部第三方进程写入的文件，本系统没有回写权（No Save），格式由别人制定。在 DDD 中属于**防腐层（ACL）适配器**，绝不能被命名为拥有完整所有权的仓储。
3. **误区三：把“拥有唯一 ID”误当成“实体（Entity）”**  
   实体的核心在于**在多次状态修改中跨生命周期追踪“同一个东西”**。不可变的历史事件事实（Fact）即便带有全局 UUID，也是等价可互换的值语义。
4. **误区四：把“函数式纯数据 + 纯函数”误当成“贫血模型（Anemic Model）”**  
   Martin Fowler 批判的贫血模型是指业务规则外溢到了应用层。如果所有规则和算法 100% 封闭在领域层内（Policies & Services），这就是标准的**函数式充血（Functional Rich Domain）**。
5. **误区五：低估“DTO ↔ Entity 实例化”在密集日志 SDK 中的工程代价**  
   大日志场景下几万个事件对象逐行 `new Class` 会带来巨大的 V8 原型链内存膨胀与 GC 暂停；同时类方法无法被打包器 tree-shake。

---

## 兼顾清晰度与高性能的最佳工程实践：伴随对象模式（Companion Object）

在 TypeScript 中，利用“类型（Type）与值（Value）同名空间合并”特性，既能获得面向对象打点补全的内聚感，又能保留纯数据的零序列化损耗与极致轻量：

```typescript
// 1. 类型层面：纯数据契约（100% 序列化安全，零原型链负担）
export interface Transcript {
  readonly agent: CodingAgentId;
  readonly session: TranscriptSession;
  readonly events: readonly TranscriptEvent[];
}

// 2. 行为层面：同名伴随常量（收拢散落函数，提供 IDE 补全）
export const Transcript = {
  summarize(t: Transcript): SessionSummary {
    return foldTranscript(t);
  },
  prompts(t: Transcript, options?: SessionPromptsOptions): readonly SessionPrompt[] {
    return sessionPrompts(t, options);
  }
} as const;
```

---

## 延伸阅读与综合理解

- [[ddd-mental-models-and-anti-patterns|DDD 实践中的五大认知误区与全景分型范式]]：基于真实工业级系统演进，深度复盘只读强立聚合根、防腐层与仓储混淆、函数式充血等常见认知陷阱与战略五型判据。
- [[ddd-bounded-context-and-aggregate|限界上下文、聚合与仓储]]：系统梳理限界上下文语义边界、聚合一致性边界、facade 暴露机制、分层依赖方向以及聚合根与仓储的解耦协作关系。
- [[ddd-implementation-approaches|DDD 的实现方式与取舍]]：评估 Seedwork、框架、架构测试与 decider 等落地路径，厘清分布式仓储设计、前后端模型共用、Effect 定位以及基础库中的 DDD 取舍。

---

## Source Pointers

- `raw/sources/ddd.md`
- https://zhuanlan.zhihu.com/p/585899317
- https://en.wikipedia.org/wiki/Curry%E2%80%93Howard_correspondence
- Eric Evans, *Domain-Driven Design Reference: Definitions and Pattern Summaries* (2015)
- Vaughn Vernon, *Effective Aggregate Design* (2011)
- Martin Fowler, *Anemic Domain Model* (2003)
