---
title: Agent Orchestration Platform
description: 企业级多人 Agent 编排平台是运行在单一 Agent Harness 之上的平台层，提供多租户、Scope 隔离、权限审批、多端接入、沙箱执行和多 Harness 路由等能力，代表产品有 QM、Raft、Orca。
type: topic
category: ai
created: 2026-08-26
updated: 2026-08-26
timestamp: 2026-08-26
tags:
  - agent
  - orchestration
  - multi-agent
  - platform
source_refs:
  - raw/sources/2026-08-26-yc-qm-agent-harness.md
  - raw/sources/2026-08-26-qm.md
  - https://qm.ycombinator.com/
  - https://github.com/yc-software/qm
resource:
  - raw/sources/2026-08-26-yc-qm-agent-harness.md
  - raw/sources/2026-08-26-qm.md
  - https://qm.ycombinator.com/
  - https://github.com/yc-software/qm
---

# Agent Orchestration Platform

## 摘要

企业级多人 Agent 编排平台（Agent Orchestration Platform）是运行在单一 Agent Harness 之上的平台层。它不直接实现 Agent 的运行循环，而是为多个 Agent 和多个用户提供协作、治理和执行环境。

## 与 Agent Harness 的边界

| 层 | 职责 | 代表 |
| --- | --- | --- |
| **Agent Harness** | 单个 Agent 的运行循环：system prompt、tools、agentic loop、translation layer | Pi、Claude Code、OpenCode、Codex |
| **编排平台** | 多 Agent、多用户的协作与治理：多租户、权限、安全、多端接入、沙箱、多 Harness 路由 | QM、Raft、Orca |

关系：编排平台通过路由层调用具体的 Harness，Harness 负责单 Agent 的实际执行。

## 核心能力

### 1. 多租户与 Scope 隔离

每个用户、项目、频道都有独立的 Scope，包含独立的 memory、files、keychain、permissions、sandbox。不同 Scope 之间的数据和权限隔离。

### 2. 权限与安全审批

- **Security Posture**：Strict（每次工具调用需审批）/ Auto（分类器筛选）/ Dangerous（无筛选）
- **Command Policy**：预声明的审批规则和硬拒绝（如递归删除、破坏性 SQL）
- **Audit**：所有操作可审计

### 3. 多端接入

支持 Slack、Web、Crons、Webhooks 等多种触发方式，让 Agent 可以在不同场景下被调用。

### 4. 沙箱执行

每个 Scope 的代码执行在独立的沙箱中（Docker、Fly、AWS MicroVM 等），避免互相影响和安全风险。

### 5. 多 Harness 路由

同一平台可以驱动多种 Harness（Pi、Claude Code、OpenCode、Codex），根据任务类型或用户偏好选择合适的 Harness。

## 代表产品

### QM（YC）

YC 开源的多人 Agent 编排平台。架构特点：
- Headless core + 可选插件（web UI、admin、Slack）
- Scope 隔离：每人/房间独立的 memory、files、keychain、sandbox
- 多 Harness 支持：Pi、OpenCode、Codex、Claude Code
- 安全模型：posture + command policy + security screening
- 部署目录独立于 core

### Raft

Botiverse 的多 Agent 协作平台。核心是托管的协作控制面（频道、DM、线程、任务、身份），Agent 运行在连接的本地 Computer 或外部 runtime 上。

### Orca

MIT 开源的 local-first Agent 开发环境。围绕代码仓库、Git worktree、终端、diff 审查组织多个 coding agent。

## 相关页面

- [[Agent Harness]]
- [[Agent]]
- [[Code Agent]]
- [[wiki/comparisons/product/Raft vs Orca：多 Agent 协作与本地执行|Raft vs Orca]]

## 来源指针

- `raw/sources/2026-08-26-yc-qm-agent-harness.md`
- `raw/sources/2026-08-26-qm.md`
- https://qm.ycombinator.com/
- https://github.com/yc-software/qm
