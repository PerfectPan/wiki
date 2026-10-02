---
title: 云端 Agent 运行时与系统架构边界
description: 梳理从沙箱宿主单体到云原生可持久化 Agent 运行时的演化路径，提炼纯计算运行时、预写执行、按需资源调度与对抗审查的工程范式。
type: synthesis
category: ai
created: 2026-10-02
updated: 2026-10-02
timestamp: 2026-10-02
tags:
  - agent
  - cloud-native
  - architecture
  - durability
  - scaling
source_refs:
  - raw/sources/2026-09-06-the-next-scaling-problem.md
  - https://tetral.ai/blog/the-next-scaling-problem/
resource:
  - raw/sources/2026-09-06-the-next-scaling-problem.md
  - https://tetral.ai/blog/the-next-scaling-problem/
---

# 云端 Agent 运行时与系统架构边界

## 问题

当 Agent 从本地 CLI（如 Claude Code、Codex）走向大规模云端托管服务时，瓶颈不再只是模型推理本身，而是外围系统的扩展性：如何解耦 Agent 状态与高开销的虚拟机沙箱？如何在无状态容器节点频繁崩溃或轮转时保证长程任务不丢状态、外部副作用不重复执行？多 Agent 并行扩展时，如何保证产物可靠沉淀而不是产生不可控的幻觉分歧？

## 简答

将 Agent 体系从「沙箱为宿主」重构为「可持久化计算中枢」：
1. **职责分离**：计算机与虚拟机是受控的外部按需资源，而非 Agent 本身的生存空间；
2. **预写执行（Write-Ahead Execution）**：将不可变的副作用操作声明与事务状态持久化前置于物理调用，杜绝失效重试导致的重复执行；
3. **分层状态模型**：Thread 承载单任务内上下文隔离，Session 承载跨任务独立生命周期，Workspace 承载长期共享资产；
4. **对抗审查沉淀机制**：多 Agent 协作不能仅依赖无约束的聊天会话，必须通过独立审查通道与人类确认，将经过验证的产物合并入共享版本库。

## 来源事实

在 Tetral 的系统设计与演进经验（Yang Li，2026-09）中，指出了传统云端 Agent 实现的多项限制与替代方案：

1. **沙箱不等于容量单元**：早期方案（如 Anoma 运行在 E2B 内）将完整 Agent 循环打包在单个沙箱虚拟机内，使得 Agent 容量直接与沙箱调度与资源生命周期绑定。沙箱生命周期的高频启停（Churn）给编排系统（如 Kubernetes Pod 或虚拟机调度器）带来巨大压力。
2. **状态与计算外置**：Tetral 将计算抽象为纯函数式 Reducer，所有会话时序和转移动作交由 Bridge 写入 PostgreSQL。计算 Pod 可被随意替换，恢复时仅需拉取提交记录即可重建检查点。
3. **外部副作用必须前置持久化**：借鉴 WAL 原理，在调用外部接口或执行环境前，先在数据库登记幂等声明（Receipt）。如果计算节点崩溃，未提交的提案作废，已提交的根据回执恢复，避免外部副作用被执行多次。
4. **凭据零泄露**：模型网关（Gateway）负责代理请求与刷新 OAuth 令牌，明文 API Key 从不进入计算 Pod 或执行沙箱。
5. **对话膨胀与审查机制**：无约束的会话漫游在多 Agent 协同中会导致 token 浪费且产物合并率极低。可靠的模式是各个 Agent 基于共享基线独立工作，互相提交对抗性质疑，最终由人工核准合入目标版本。

## 综合结论

### 1. 计算机是资源，不是宿主

在传统开发认知中，Agent 类似部署在某台机器上的进程，围绕这台机器的文件系统和 Shell 运行。但在云端，这种模式导致沙箱管理成本高昂、跨会话恢复困难且调试极度依赖私有环境访问。

解耦后的标准边界应为：
- **Runtime（运行时）**：轻量级计算进程，仅负责解析输入、调用 Reducer 状态机、派发能力声明；
- **Computer（计算环境）**：与模型网关、MCP 服务同等的外部资源。仅在产生文件改动或脚本编译需求时按需拉起，用完即释放或重置；
- **Workspace（工作区）**：跨环境保留的稳定事实层（代码仓库、持久化记忆、文档资产）。

### 2. 状态机持久化的两种实现范式

面对计算节点失效与长时间运行任务，当前云端架构存在两条分水岭路线：

| 维度 | 工作流编排引擎路线（如 Cursor + Temporal） | 事务数据库 + 纯 Reducer 路线（如 Tetral / Pi） |
| --- | --- | --- |
| **状态恢复机制** | 依靠 Temporal Event History 完整重放工作流代码中的事件流 | 依靠 PostgreSQL / SQLite 事件表，直接重建最新检查点由纯函数 Reducer 派生状态 |
| **外部副作用防护** | 依靠工作流 Activity 层的重试与幂等控制 | 依靠预写声明（Write-Ahead Declaration）与数据库原子事务提交回执 |
| **消息投影设计** | 对话流与内部执行事件通常作为两条物理链路维护 | 事件流（session_events）与模型上下文视图（session_messages）统一在同一事务权威下投影 |
| **系统复杂度** | 引入分布式工作流集群，运维开销较大 | 架构集中于关系型数据库事务与轻量队列，逻辑高度内聚 |

### 3. 多 Agent 扩展的二维隔离框架

Agent 系统要真正扩展，必须在空间与时间两个维度解耦：

```text
Workspace（全局共享资源：Git 仓库、长期记忆、权限策略）
  ├── Session A（功能开发：独立根上下文、独立生命周期与计费）
  │     ├── Thread 0（主编排逻辑）
  │     ├── Thread 1（子 Agent：单元测试生成，fork_turns 独立上下文）
  │     └── Thread 2（子 Agent：安全审查）
  └── Session B（文档维护：独立根上下文与触发频率）
```

- **Thread 级扩展**：用于解决单个任务内部的并行处理。子 Thread 拥有独立的时序事件队列，父子通信通过异步 Inbox 传递，互不污染彼此的上下文窗口。
- **Session 级扩展**：用于解决不同领域职责（如编码、代码审查、知识归档）的分离，各自采用不同的 Agent 版本配置与权限限制，通过工作区最终产物产生连接。

### 4. 验证驱动的产物合并原则

多 Agent 系统不能依赖多方在同一聊天频道内的“讨论”。自由讨论会带来记忆发散和不确定性累积。
稳健的工作流遵循**「提议-对抗审查-人工确认-合入基线」**：
- 候选 Agent 独立产出成果；
- 审查 Agent 针对成果的论据与测试覆盖进行主动质疑与边界探查（审查指令由平台系统注入，与待审查内容隔离以防 Prompt 注入）；
- 最终审查通过的产物经人工核准后更新至工作区公共版本，作为后续任务信任的基准。

## 对个人/项目的启发

1. **Agent 业务系统设计避坑**：不要让业务容器长久占用昂贵的远程沙箱。应将业务核心做成无状态服务，通过调用轻量沙箱服务（如 Daytona、Docker）动态执行具体指令。
2. **长任务可靠性保障**：在编写需要调用第三方 API（如发邮件、转账、触发构建）的 Agent 工具时，必须实现两阶段提交逻辑：先记录操作意图及唯一 ID，拿到落盘凭据后再行发起网络调用，避免重试导致双重支付或重复触发。
3. **防注入审查独立化**：当引入 AI 进行权限审批或安全判定时，审查逻辑必须运行在隔离的上下文线程中，切忌将未经脱敏的用户输入或外部网页数据直接作为审查指令的上下文，必须严格将“判定规则”与“证据材料”在提示词结构中拆开。

## 相关页面

- [[wiki/topics/ai/tetral|Tetral]]
- [[wiki/topics/ai/agent-harness|Agent Harness]]
- [[wiki/syntheses/ai/persistent-agent-harness-design-patterns|持久化 Agent Harness 的设计模式]]
- [[wiki/topics/ai/agent-orchestration-platform|Agent Orchestration Platform]]
- [[wiki/syntheses/ai/agent-loop-control-boundaries|Agent 循环工作流的控制边界]]

## 来源指针

- `raw/sources/2026-09-06-the-next-scaling-problem.md`
- https://tetral.ai/blog/the-next-scaling-problem/
