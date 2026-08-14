---
title: Agent Native 系统接口设计
description: 综合 BMPI 两篇文章，沉淀 Agent Native 系统中 DSL、IR/DAG、验证契约和修复循环的设计范式。
type: synthesis
category: ai
created: 2026-06-21
updated: 2026-06-21
timestamp: 2026-06-21
tags:
  - agent
  - ai-native
  - dsl
  - validation
  - workflow
source_refs:
  - raw/sources/2026-06-21-bmpi-agent-native-system-paradigm.md
  - raw/sources/2026-06-21-bmpi-ai-native-investment-system.md
  - https://www.bmpi.dev/dev/agent-native-system-paradigm/
  - https://www.bmpi.dev/dev/ai-native-investment-system/
resource:
  - raw/sources/2026-06-21-bmpi-agent-native-system-paradigm.md
  - raw/sources/2026-06-21-bmpi-ai-native-investment-system.md
  - https://www.bmpi.dev/dev/agent-native-system-paradigm/
  - https://www.bmpi.dev/dev/ai-native-investment-system/
---

# Agent Native 系统接口设计

## 问题

复杂 AI 产品应该怎样设计软件接口，才能让 [[Agent]] 稳定地读取、编写、验证、执行和修复任务，而不是只把大模型接到聊天框或底层 API 上？

## 简答

Agent Native 系统的核心不是“让模型多做事”，而是为模型设计一层低熵、可验证、可修复的操作面。更稳的链路是：自然语言意图进入 Domain DSL，由业务引擎编译为 IR/DAG，再经过结构校验、语义校验、机器可读错误反馈和修复循环，最终交给确定性代码执行。

## 来源事实

BMPI 的两篇文章分别给了总纲和案例：

- 《Agent 时代的软件接口》从 Minecraft 建造和量化策略两个案例抽象出通用范式：`Intent -> Domain DSL -> IR/DAG -> Validation -> Repair Loop -> Execution`。
- 《我是如何构建一个 AI 原生量化系统的》展示了策引如何放弃 AI 直接写 Python 或调用复杂 API，转向策略原语 DSL、Schema 供应链、few-shot 示例和 Local / Remote 混合 Agent 架构。

这两个案例的共同点是：模型不直接接触底层执行面。量化系统不让模型直接写带前视偏差风险的 Python；Minecraft 建造系统不让模型直接生成低层方块坐标。模型只负责组合受控的领域原语，执行、排序、校验、计算和导出由确定性引擎处理。

## 综合结论

### 1. Agent 的接口不应等同于人类 API

传统 API 常面向人类开发者，假设调用方能理解文档、调试参数、处理边界。但 Agent 的失败模式不同：它容易在深层 JSON、隐式约束、坐标计算、状态维护和工具选择上累积小错。

因此 Agent 接口应该优先降低表达空间，而不是扩大能力边界：

- 任意代码接口表达力强，但幻觉、前视偏差、沙盒成本、不可复现性都高。
- 过细 API 参数看似类型安全，但复杂任务会退化成嵌套 JSON 迷宫。
- Domain DSL 是折中方案：保留领域表达力，同时把底层计算、权限、状态和执行细节收回引擎侧。

### 2. DSL 的好坏取决于原语是否足够小而正交

DSL 不是把自然语言换成 JSON。它真正有价值的地方，是把领域抽象成一组稳定原语。

在策引中，均线、比较、延迟、连续确认和外部市场指标被拆成可组合原语。模型只声明节点和依赖，不关心 Pandas 对齐、未来函数屏蔽和执行顺序。在 CraftDAG 中，模型只声明 RoomShell、Door、GableRoof、anchor、wall、offset 等组件语义，不直接计算方块坐标。

这类 DSL 的设计原则：

- 原语数量要少，但组合空间要大。
- 原语应表达领域语义，而不是底层实现细节。
- 约束要强到能拦截常见错误，但不能膨胀成另一门复杂通用语言。
- 真实复杂场景可以保留逃生口，例如策引保留 Python 路径处理少量复杂状态逻辑。

### 3. 业务引擎要像编译器，而不是像提示词模板

Agent 生成的 DSL 不能直接执行。它应该进入编译管线：

- 解析领域计划；
- 降级为 IR/DAG；
- 建立节点依赖；
- 做拓扑排序；
- 进行静态分析和语义校验；
- 生成目标表示或执行计划。

IR/DAG 的价值在于把模型意图变成系统可以推理和审计的结构。它可以追踪量化信号依赖，检查是否偷看未来数据；也可以计算建筑组件依赖、材料清单和局部重算范围。

这说明 Agent Native 产品里的“业务引擎”不只是后端服务，更接近一个领域编译器。

### 4. 验证契约要同时覆盖事前和事后

稳定的 Agent 系统需要两类契约：

- 事前契约：Schema、LLM authoring contract、llm.txt、quickstart、few-shot 示例、绝对禁止项。
- 事后契约：结构化错误、错误阶段、错误码、JSON path、repair hint、重试策略。

如果系统只返回 `Invalid plan`，模型只能猜测并重写整份计划。更好的做法是返回机器可读错误，让模型知道哪个节点、哪个字段、哪个阶段出了问题，以及推荐修复方向。

这类验证契约和 [[LLM 结构化输出的可靠性边界]] 相关：结构化输出能保证形式可靠，但业务正确性仍要靠领域校验、状态机、权限和审计补足。

### 5. 概率层和确定性层必须硬切开

两篇文章都反复强调一个边界：模型适合处理模糊意图、自然语言解释、候选方案生成和错误文本翻译；队列、状态机、回测计算、拓扑排序、数据对齐、几何计算这些必须由确定性代码负责。

更稳的分工是：

- Local Agent / Orchestrator：靠近用户，处理模糊性、对话、路由、本地工具和确认表单。
- Remote Engine / Processor：接收结构化 Job，执行耗时任务、验证、编译、回测和计算。

这和 [[Workflow vs Agent]] 的边界一致：能被流程和状态机稳定表达的部分，不应交给模型自由决定；只有下一步动作本身需要持续判断时，才上升为 Agent。

## 适用边界

这套范式适合：

- 有明确领域结构；
- 能抽象出稳定原语；
- 中间状态可以验证；
- 最终结果可以执行、模拟或回测；
- 错误可以定位和局部修复；
- 人类仍能审查结果并承担最终判断。

它不适合：

- 完全开放、没有验证标准的创意任务；
- 领域原语还不稳定的早期探索；
- 结果无法模拟、无法回放、无法审计的高风险任务；
- 为了追求纯 DSL 而把 DSL 膨胀成另一门复杂编程语言。

Validation 也不等于真实正确。投资策略通过回测不代表未来有效，建筑蓝图通过编译不代表审美优秀。验证契约的作用是收窄错误空间，而不是替代人类判断。

## 对 wiki 和个人自动化产品的启发

对个人自动化、情报服务和知识库协作来说，可以借鉴这条原则：

> 先把关键链路变成 Agent 可操作的结构化协议，再让模型参与生成、修复和解释。

例如：

- 情报简报：信源、主题、时间窗、可信度、摘要结构和投递格式应先结构化；模型负责摘要和解释，不负责偷偷改流程。
- wiki 协作：来源层、综合页、索引、PR body 和校验清单应形成固定协议；模型负责整理和链接，不直接绕过审阅写入主干。
- 内容生成：选题、素材、草稿、审核、发布应分阶段，每阶段有明确产物和状态，不让模型直接从一句话跳到外部发布。

真正可复用的 Agent Native 系统，不是“聊天框 + 工具调用”，而是“领域协议 + 编译验证 + 修复循环 + 人类审查”。

## 相关页面

- [[Agent]]
- [[Workflow vs Agent]]
- [[LLM 结构化输出的可靠性边界]]
- [[Agent Harness 演进范式]]
- [[Agent-native 生成型 CLI 的产物协议]]

## 来源指针

- `raw/sources/2026-06-21-bmpi-agent-native-system-paradigm.md`
- `raw/sources/2026-06-21-bmpi-ai-native-investment-system.md`
- https://www.bmpi.dev/dev/agent-native-system-paradigm/
- https://www.bmpi.dev/dev/ai-native-investment-system/
