---
title: BMPI - 我是如何构建一个 AI 原生量化系统的
source_url: https://www.bmpi.dev/dev/ai-native-investment-system/
author: 马大伟
published: 2026-03-28
captured: 2026-06-21
type: source-note
---

# BMPI - 我是如何构建一个 AI 原生量化系统的

## 来源概览

文章记录作者构建策引（MyInvestPilot）的架构路径：从不让 AI 替用户做投资决策，到让 AI 把用户意图翻译成可执行、可验证、可复现的策略 DSL。它是 Agent Native 系统接口范式在量化领域的具体案例。

## 来源事实

- 策引选择的方向不是让 AI 直接给买卖结论，而是帮助用户理解自己跟随的策略结构。作者认为透明策略比黑盒答案更能支撑长期执行纪律。
- 作者试过让 AI 生成 Python 策略代码，但遇到三类核心问题：幻觉不存在的库、隐藏的前视偏差、实现不可复现；此外还需要沙盒隔离、资源限制和超时处理。
- 作者也考虑过让 AI 调用结构化 API，但策略逻辑一复杂，API 参数容易变成深层嵌套 JSON，表达力和演进成本都不理想。
- 最终方案是策略 DSL：AI 不写任意代码，只在预定义原语里组合策略；每个原语尽量正交，执行层形成 DAG。
- 原语系统覆盖技术指标、逻辑比较、延迟、连续状态确认、外部市场指标等能力。例如 EMA、GreaterThan、LessThan、Lag、Streak、VIX/SPX market indicators。
- 策略 DSL 不只是执行格式，也支撑解释层、可视化编辑器和一致性校验。完整链路是：自然语言 -> AI 翻译成 DSL -> 引擎执行 -> 解释层呈现给用户 -> 用户建立理解与信任。
- Schema 是唯一事实源。引擎 Schema 驱动 LLM 文档、prompt 和 few-shot 示例生成，避免 AI 说明书和执行代码漂移。
- 验证分层发生在前端、后端和语义层：前端用 AJV 做 JSON 结构校验，后端做运行时类型检查，语义层做 point-in-time、市场依赖等一致性检查。
- Prompt 演化从简单原语清单走向绝对禁止项和 few-shot 策略示例。作者观察到，告诉模型“不能怎么做”比只给正向引导更能降低常见错误。
- 架构上采用 Local / Remote 分工：Local Agent 像浏览器里的 CLI + ReAct Loop，处理用户模糊意图和本地工具编排；Remote Processor 处理长耗时回测、分析和队列任务。
- 作者保留 Python 代码路径处理高阶复杂状态场景，避免把 DSL 强行扩展成另一门复杂编程语言。

## 可沉淀观点

- 在严肃决策系统里，AI 更适合做翻译器和探索工具，不适合直接成为决策者。
- 对 Agent 友好的接口需要同时满足表达力、约束力、可复现性和可解释性；任意代码接口太宽，普通 API 参数又可能太窄。
- 文档与执行同源是 Agent 系统的基础设施问题，不是文档洁癖。一旦 prompt、Schema 和引擎漂移，Agent 会生成看似合理但无法执行的结构。
- DSL 不应覆盖所有场景。核心路径用 DSL 稳住 90% 常见需求，少数复杂状态逻辑保留代码路径，往往比追求全 DSL 更可维护。
- 对用户而言，系统目标不是单次给出答案，而是帮助人建立可理解、可执行、可长期坚持的决策框架。

## 来源指针

- https://www.bmpi.dev/dev/ai-native-investment-system/
- 相关对象：MyInvestPilot、策略原语、primitives_schema.json、llm-quickstart.txt
