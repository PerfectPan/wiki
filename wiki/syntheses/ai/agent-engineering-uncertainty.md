---
title: Agent 工程中的不确定性与验收设计
description: 从测试、调试、操作边界和版本管理说明 Agent 工程需要补充哪些质量控制，并区分来源观点与实践建议。
type: synthesis
category: ai
created: 2026-10-21
updated: 2026-10-21
timestamp: 2026-10-21
tags:
  - agent
  - evaluation
  - observability
  - reliability
source_refs:
  - raw/sources/kimmking-agent-engineering.md
  - https://www.zhihu.com/question/2024177621341075284/answer/2095217865989399922
  - wiki/comparisons/ai/workflow-vs-agent.md
  - wiki/syntheses/ai/llm-structured-output-reliability.md
resource:
  - raw/sources/kimmking-agent-engineering.md
  - https://www.zhihu.com/question/2024177621341075284/answer/2095217865989399922
  - wiki/comparisons/ai/workflow-vs-agent.md
  - wiki/syntheses/ai/llm-structured-output-reliability.md
---

# Agent 工程中的不确定性与验收设计

Agent 工程需要在已有软件工程方法之上，增加对模型效果波动的评测和对模型动作的执行校验。模型可以提出不同解法，程序仍要检查权限、输入和操作结果。本文根据 kimmking 的[知乎回答](https://www.zhihu.com/question/2024177621341075284/answer/2095217865989399922)整理，并结合库内页面给出实践建议。

## 原回答的主要判断

作者用模型输出的不确定性串起四项工程变化：

| 环节 | 作者强调的问题 | 对应做法 |
| --- | --- | --- |
| 测试与验收 | 输出可能有多种可接受形式 | 建立评测样例、评分标准和人工抽检 |
| 调试 | 同一次失败可能无法稳定重现 | 保存输入输出及上下文，追踪每次调用 |
| 操作边界 | 模型可能提出不合适的动作 | 用代码实现明确规则，在执行前校验并拒绝越界操作 |
| 发布 | 模型、提示词和检索配置都可能改变效果 | 记录配置组合，随变更评估效果 |

作者同时强调分层、版本管理、灰度发布和监控仍然适用。上述内容是经验判断，回答没有给出实验或统计资料；具体段落位置见[[raw/sources/kimmking-agent-engineering|来源核查记录]]。

## 用一个项目维护任务理解这些变化

假设 Agent 要根据故障描述修改代码、运行检查并创建拉取请求（PR）。以下是编者提出的例子和实施建议，不是原回答里的案例。

### 1. 把功能断言与效果评测分开

先约定交付物：故障被修复、相关检查通过、没有改动无关文件，并且 PR 说明能解释修改原因。模型不必每次生成同一份补丁，但每份补丁都要满足这些要求。

对能明确判断的行为保留精确测试，例如工具参数是否合法、无权限时是否拒绝写入。对修复是否合理、说明是否准确等问题，使用代表性任务、明确评分标准和人工复核。对容易波动的任务重复执行，记录成功与失败，避免把一次成功当成稳定能力。

这也限定了原文对测试的概括：Agent 测试不必全部变成主观评分。[[wiki/syntheses/ai/llm-structured-output-reliability|结构化输出的可靠性边界]]已经区分了格式合法、内容正确和动作适当这几件事。

### 2. 保存失败时的可观察证据

调查失败时，需要知道 Agent 看到了什么、调用了什么、实际产生了什么结果。这个例子中可记录任务标识、代码版本、模型及提示词版本、检索到的材料、工具参数、工具返回值和最终补丁。

这些记录有助于区分上下文缺失、模型判断错误和工具执行失败，但不能保证重跑会得到同一个补丁。记录范围也应受脱敏、访问权限和保留期限约束，不把原文关于完整日志的建议理解为无条件保存凭据、私人数据或模型内部思维过程。

### 3. 让执行程序负责操作边界

模型负责提出修改方案，工具执行层检查可写目录、允许的命令和操作授权。创建 PR、合并或部署分别按各自的授权条件执行，不能仅凭模型说任务需要就开放操作。

固定的检查步骤可以由程序编排，只有需要结合上下文选择下一步的部分才交给模型。这里沿用[[wiki/comparisons/ai/workflow-vs-agent|Workflow vs Agent]]对决策权的区分；模型生成了合法参数，也不等于该动作已经获得授权。

### 4. 把效果变化关联到具体版本

一次评测应能对应代码、模型、提示词、检索配置和评测集版本。更换模型或修改提示词后，用同一组代表性任务检查回归，再决定是否扩大使用范围。

联合记录版本是为了找到效果变化的原因，并能恢复先前的配置组合；这不要求每次把所有组件一起升级。对这个项目维护 Agent，补丁质量下降时应能查出究竟改了哪一项，而不是只保留应用版本号。

## 使用这些判断的限制

- 不把传统软件等同于绝对确定、Agent 等同于完全不可复现。更实用的划分是：哪些行为有明确规则，哪些结果需要效果评测，哪些失败依赖当时的环境和上下文才能解释。这是本文对原文概括的限定。
- 原文把模型和提示词工作估为约三成，其余工程工作估为约七成，但没有交代样本和统计方法。可以据此提醒团队预留评测、监控和降级工作，不能直接拿这个比例做排期基准。

## 相关页面

- [[wiki/comparisons/ai/workflow-vs-agent|Workflow vs Agent]]：哪些步骤由程序决定，哪些交给模型判断。
- [[wiki/syntheses/ai/llm-structured-output-reliability|LLM 结构化输出的可靠性边界]]：格式约束不能替代业务判断和权限检查。
- [[wiki/topics/ai/agent-harness|Agent Harness]]：承载模型调用、工具执行和运行控制的工程系统。

## 来源指针

- [kimmking：开发Agent和传统软件工程有哪些区别？](https://www.zhihu.com/question/2024177621341075284/answer/2095217865989399922)，发布于 2026-10-18，访问于 2026-10-21。
- [[raw/sources/kimmking-agent-engineering|来源核查记录]]：段落位置、可确认内容与证据限制。
- [[wiki/comparisons/ai/workflow-vs-agent|Workflow vs Agent]]。
- [[wiki/syntheses/ai/llm-structured-output-reliability|LLM 结构化输出的可靠性边界]]。
