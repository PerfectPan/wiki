---
title: Workflow vs Agent
type: comparison
category: ai
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - agent
  - workflow
  - orchestration
  - llm
source_refs:
  - https://www.anthropic.com/research/building-effective-agents
---
# Workflow vs Agent

## 当前结论

如果任务步骤、分支和回路大致可预期，优先用 workflow；只有当“下一步做什么”本身需要交给模型持续判断时，才更适合 agent。

## 备选项

- Workflow：由人预先定义步骤、分支、并行和循环条件。
- Agent：让模型根据当前状态决定下一步动作，并通过反馈继续迭代。

## 取舍分析

| 方案 | 优势 | 风险 | 适用场景 |
| --- | --- | --- | --- |
| Workflow | 可预测、可审计、容易控成本和控范围 | 面对开放问题时容易僵硬，分支爆炸后维护成本高 | 固定流程、批处理、多步但结构稳定的任务 |
| Agent | 更能处理开放式问题，能根据中间结果调整下一步 | 更难控制范围、成本和副作用，调试与评估更复杂 | 搜索空间大、需要试探与反馈闭环的任务 |

## 推荐理由

- 2024-12-24 的一条观察已经给出一个很稳的区分：workflow 更接近确定性编排，像并行、循环等待、拆分子任务这类结构都由人预先规定。
- agent 则把“下一步做什么”交给模型，并通过反馈机制不断更新行动。
- 这不是“谁更高级”的问题，而是“决策权放在哪一层”的问题。能在流程层写死的，通常先不要上升成 agent。

## 来源指针

- [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
