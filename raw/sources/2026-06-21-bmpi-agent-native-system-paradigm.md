---
title: BMPI - Agent 时代的软件接口
source_url: https://www.bmpi.dev/dev/agent-native-system-paradigm/
author: 马大伟
published: 2026-06-14
captured: 2026-06-21
type: source-note
---

# BMPI - Agent 时代的软件接口

## 来源概览

文章通过 MyInvestPilot（策引）和 MinePilot / CraftDAG 两个案例，提出一套面向 Agent 的系统接口范式。作者认为，把大模型接进聊天框或底层 API 都不足以支撑复杂任务；更稳的路径是为 Agent 设计领域 DSL、IR/DAG、验证契约和修复循环。

## 来源事实

- 文章从 Minecraft Agent 实验出发：让大模型在游戏内实时控制 Bot 建房，会遇到环境感知、路径规划、空间坐标维护、动作执行等稳定性问题。
- 作者从直接控制 Bot 转向外部生成建筑蓝图，并进一步发现 `.schem` 这种低层体素格式仍然太靠近方块坐标，模型直接生成容易产生墙体、屋顶、楼梯等结构错误。
- 作者把量化系统策引里的策略原语经验迁移到 Minecraft 建造系统：放弃让模型直接写底层 Python 或方块坐标，改为让模型组合受控领域原语。
- 在策引中，模型组合 EMA、GreaterThan、LessThan、Lag、Streak 等策略原语；底层 Pandas 计算、数据对齐、未来函数屏蔽由引擎负责。
- 在 CraftDAG 中，模型生成 `ComponentPlan` 这类组件级 DSL，例如房间壳体、门、屋顶、锚点、墙面、偏移、屋檐等高层语义；引擎再降级到几何包围盒和体素坐标。
- 作者把业务引擎视为编译器：自然语言意图先进入 Domain DSL，再编译为 IR/DAG，经过静态分析、依赖解析、拓扑排序和目标表示生成。
- 验证错误需要面向机器，而不只是面向人。错误反馈应包含 stage、code、path、repairHint 等字段，让模型能局部修复，而不是重写整份 JSON。
- 作者强调事前契约和事后报错同样重要：LLM 编写契约、JSON Schema、few-shot 示例、机器可读开发文档都属于 Agent 使用系统前必须读取的接口面。
- 理想架构是混合 Agent：Local Agent / Orchestrator 负责处理用户意图和模糊性，Remote Engine / Processor 负责队列、状态机、编译、验证和确定性计算。
- 这套范式的适用前提是领域结构明确、可抽象稳定原语、中间状态可验证、错误可定位、最终结果可执行或模拟，并且人仍能审查结果。

## 可沉淀观点

- Agent Native 的关键不是聊天入口，而是给 Agent 提供可读、可写、可验证、可修复的 workflow surface。
- Domain DSL 的价值是收拢底层控制权，把模型从坐标、数组、Pandas 对齐等低层细节中解放出来，让它只表达领域结构。
- IR/DAG 让系统获得静态分析、依赖追踪、局部重算和确定性执行能力，是拦截 Agent 幻觉的基础。
- Validation 不等于真实正确。它只能把错误空间缩小到系统可管理范围，不能替代投资有效性、审美质量或业务判断。
- 合理的最终形态是 dual interface：人通过 UI 表达意图、审查结果、做决策；Agent 通过 DSL、工具和验证契约操作系统。

## 来源指针

- https://www.bmpi.dev/dev/agent-native-system-paradigm/
- 相关案例：MyInvestPilot、MinePilot、CraftDAG
