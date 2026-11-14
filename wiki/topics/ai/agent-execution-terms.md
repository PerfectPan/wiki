---
title: Agent 执行术语：session、turn、run 与 step
description: 区分一轮用户交互、一次运行、一次模型迭代和消息，并对照 pi、DSH 与主流 Agent SDK 的命名。
type: topic
category: ai
created: 2026-11-14
updated: 2026-11-14
timestamp: 2026-11-14
tags:
  - agent
  - harness
  - terminology
source_refs:
  - https://github.com/earendil-works/pi/blob/e12dbfc9299049dc2e7a974612fec32001a7ba8a/packages/agent/README.md
  - https://github.com/deepseek-ai/deepseek-harness/blob/39163dd30f703a79079e2d2446545cff3c453738/docs/glossary.zh.md
  - https://openai.github.io/openai-agents-python/ref/run/
  - https://openai.github.io/openai-agents-python/running_agents/
  - https://developers.openai.com/cookbook/examples/agents_sdk/session_memory
  - https://code.claude.com/docs/en/agent-sdk/agent-loop
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
  - https://agentclientprotocol.com/protocol/v1/prompt-turn
  - https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling
  - https://github.com/open-telemetry/semantic-conventions-genai/issues/332
  - https://github.com/open-telemetry/semantic-conventions-genai/issues/418
  - https://github.com/weave-os/router/blob/424e57b678c05fe61ac8b73c063c1cad20557635/docs/SEMANTICS.md
resource:
  - https://github.com/earendil-works/pi/blob/e12dbfc9299049dc2e7a974612fec32001a7ba8a/packages/agent/README.md
  - https://github.com/deepseek-ai/deepseek-harness/blob/39163dd30f703a79079e2d2446545cff3c453738/docs/glossary.zh.md
  - https://openai.github.io/openai-agents-python/ref/run/
  - https://openai.github.io/openai-agents-python/running_agents/
  - https://developers.openai.com/cookbook/examples/agents_sdk/session_memory
  - https://code.claude.com/docs/en/agent-sdk/agent-loop
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
  - https://agentclientprotocol.com/protocol/v1/prompt-turn
  - https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling
  - https://github.com/open-telemetry/semantic-conventions-genai/issues/332
  - https://github.com/open-telemetry/semantic-conventions-genai/issues/418
  - https://github.com/weave-os/router/blob/424e57b678c05fe61ac8b73c063c1cad20557635/docs/SEMANTICS.md
---

# Agent 执行术语：session、turn、run 与 step

## 摘要

`turn` 在 Agent 系统中有多种粒度：一方的发言阶段、用户的一轮完整交互，或循环里的一次模型响应及工具执行。讨论上下文保留、执行上限和生命周期事件时，应先说明边界，再使用术语。OpenAI 的会话记忆示例按用户消息划分 turn，而其 Runner 的 `max_turns` 按模型调用计数；同一生态内也不能直接互换。[会话记忆示例][openai-memory]、[Runner 接口][openai-runner]

本页采用 **conversation turn（交互轮次）**、**run（一次运行）**、**step（执行步骤）** 区分这三层。这是本文的说明约定；描述具体框架时保留它自己的名称，并按下表解释。

## 术语表：本文的说明约定

| 术语 | 指什么 | 边界与容易混淆的地方 |
| --- | --- | --- |
| **Session / Conversation（会话）** | 保存交互历史及相关状态的容器，可以经历多轮交互和多次运行。 | 一次 run 结束后，会话通常仍可继续；会话也不等于当前模型实际接收的上下文。[OpenAI 对话管理][openai-conversations] |
| **Conversation turn（交互轮次）** | 从接纳一次用户请求，到 agent 完成本轮响应或因错误、取消等原因停止处理这一请求的交互过程。 | 可以包含多次模型请求和工具调用。执行中的插话是否并入当前轮，由产品规则决定；历史分组也可按“下一条用户消息之前”划分。[会话记忆示例][openai-memory] |
| **Run（一次运行）** | 运行时入口启动的一次执行生命周期，包含其调度的多个步骤，终态可能是完成、失败或取消。 | 由运行时定义开始、暂停、恢复与终止。它常对应一轮交互，但不能预设一一对应，例如 pi 可在同一次运行中接着消费 follow-up。[pi 生命周期与队列][pi-readme] |
| **Step / Iteration（执行步骤 / 循环迭代）** | 在本文讨论的模型与工具循环中，一次模型响应及其触发的工具执行和结果处理。 | 工具结果交给模型再次生成时进入下一步。一个步骤可以有零个、一个或多个工具调用；无工具的最终回答也算一步。[DSH 术语表][dsh-glossary]、[AI SDK 工具调用][ai-sdk] |
| **Model request（模型请求）** | 宿主向模型接口发起的一次逻辑生成请求。 | 它与工具执行是不同操作。统计时要说明是否把底层网络重试算作新的请求；服务端工具还可能在一次 API 请求内执行多次操作。[OpenTelemetry 术语讨论][otel-glossary]、[Claude 服务端工具][claude-server-tools] |
| **Message（消息）** | 交互记录中的内容单元，例如用户消息、assistant 消息、工具结果消息。 | 一次模型响应可能含文本、思考和工具调用。流式增量、内容块、SDK 发出的消息对象，不一定与协议消息一一对应。[pi 事件][pi-readme]、[Claude SDK 消息类型][claude-loop] |
| **Tool call / Tool result（工具调用 / 工具结果）** | assistant 提出的操作请求，以及执行程序返回的结果。 | 工具调用可作为 assistant 消息里的内容块，结果如何封装由协议决定。两个并行工具调用不代表两次模型请求或两个步骤。[AI SDK 工具调用][ai-sdk] |
| **Task / Goal（任务 / 目标）** | 希望完成的工作及其完成条件。 | 可能跨多轮交互、多次运行或多个 agent；停止运行和达成目标要分别判断。[DSH 目标与轮次][dsh-glossary] |

`round` 和 `exchange` 也要看具体系统：Weave 把一次用户—agent 交互叫 round，把双方各自的发言阶段叫 turn；DSH 的 Round 是外层策略迭代，exchange 则是以真人输入划分、可包含多个 turn 的交互段。[Weave 术语约定][weave]、[DSH 循环层级][dsh-glossary]

## 用同一段执行过程对照

下面假设没有中途插话、自动续行或失败恢复，并使用 pi 的消息表示：工具调用放在 assistant 消息内，工具结果单独成为消息。

```text
Session：修改配置文件
└─ Conversation turn 1：用户要求修改端口
   ├─ user：把端口改成 8080
   └─ Run A
      ├─ Step 1：assistant 调用 read_file → toolResult 返回文件内容
      ├─ Step 2：assistant 调用 edit_file → toolResult 返回修改结果
      └─ Step 3：assistant 给出最终回答
```

这段过程有 **1 个交互轮次、1 次运行、3 个执行步骤、3 次逻辑模型请求、2 个工具调用、6 条消息**。其中 6 条消息只统计图中的 1 条 user、3 条 assistant、2 条 toolResult，不计系统与工具声明消息；流式片段也不额外计为消息。按 pi 的事件命名，它会产生 **3 组 `turn_start` / `turn_end`**。按 DSH 的命名，正常情况下是 **1 个 turn、3 个 step**。[pi 事件序列][pi-readme]、[DSH 循环层级][dsh-glossary]

## 框架与协议的实际用法

| 框架 / 场景 | 原生术语和边界 | 对应本文哪一层 |
| --- | --- | --- |
| **pi agent loop** | `turn_start` 到 `turn_end`：一次模型响应加其工具执行；`agent_start` 到 `agent_end` 覆盖整次循环运行。 | pi turn ≈ step；完整执行称 run。[pi README][pi-readme] |
| **DeepSeek Harness（DSH）** | turn 处理已接纳输入，直到模型及工具停止工作或终止策略介入；一个 turn 包含零个或多个 step。自动目标和通知也可以触发 turn。 | step 与本文相同；turn 是一次输入处理周期，不限于真人发起。[DSH 术语表][dsh-glossary] |
| **OpenAI Agents SDK Runner** | `max_turns` 的 turn 是一次模型调用，包含它引发的工具调用；run 推进这些调用直至最终输出等结束条件。 | turn 接近 step；run 是一次运行。[Runner 接口][openai-runner] |
| **OpenAI 会话记忆示例** | turn 是一条用户消息及其后续内容，直到下一条用户消息之前；示例的 `max_turns` 用于保留历史。 | 按用户消息划分的交互轮次；不是 Runner 的执行次数上限。[会话记忆示例][openai-memory] |
| **Claude Agent SDK** | turn 是循环的一次迭代，先生成输出，再执行其中的工具；最终无工具回答也计一个 turn。 | turn 接近 step。不要用输出的 AssistantMessage 对象数量代替 turn 数。[Turns and messages][claude-loop] |
| **Vercel AI SDK** | step 收集本次生成的文本、工具调用和结果；拿结果发起下一次生成时进入下一步。 | step 与本文相同。[Tool Calling][ai-sdk] |
| **ACP v1（Agent Client Protocol，agent 与客户端的交互协议）** | `session/prompt` 在整轮处理期间保持 pending，最终响应携带 `stopReason`。 | 协议层的完整 prompt 生命周期。[Prompt Turn][acp-turn] |
| **Weave Router** | round 包含用户和 agent 的交互；user turn / agent turn 区分双方，agent turn 内可有多个 step / action。 | 单方发言阶段也叫 turn，单次上游请求称 step / action。[术语与旧命名说明][weave] |

这些关系只比较执行粒度，不表示不同框架的队列、取消、重试和恢复行为相同。

## 社区分歧如何影响阅读

OpenTelemetry 的 [#332][otel-turn] 最初按完整用户交互描述 turn，作者在[后续评论][otel-redefinition]中改成一次 agent 推理循环。另一位参与者又[指出][otel-question]，术语表里描述这个单位的名称是 iteration，要求先确定 turn 的边界。

其 [#418 术语表提案][otel-glossary]把 run / turn 作为较大单位、iteration 作为内部循环，并明确属于非规范性讨论。这些材料能说明用法存在分歧，不能作为已经统一的行业标准，也不能据此判断哪种叫法占多数。

## 写文档和读代码时的约定

1. **首次写“轮”时说明计数对象。** 使用“交互轮次”“模型请求次数”“执行步骤数”，或明确写“pi turn”。不要只写“最多 10 轮”。
2. **区分运行结束和任务完成。** pi 的 `agent_end` 是最后一个循环事件，取消和错误也会结束运行；等待中的事件监听器处理完毕后才会空闲。业务成功仍需检查结果和验收条件。[pi 生命周期][pi-readme]
3. **不强行把 run 和用户交互一一对应。** pi 的 steering 会在运行中注入输入，follow-up 可让同一次 run 继续处理下一项请求；DSH 的自动输入也可开启新的 turn。[pi 队列][pi-readme]、[DSH 交互段][dsh-glossary]
4. **裁剪历史时说明分组方法。** “保留最近 N 个用户轮次”和“保留最近 N 个模型步骤”保留的内容不同；先确定分组，再遵守所用模型协议的消息与工具结果配对要求。[会话记忆示例][openai-memory]、[Claude 工具结果格式][claude-tool-results]

## 相关页面

- [[wiki/topics/ai/agent|Agent]]
- [[wiki/topics/ai/agent-harness|Agent Harness]]
- [[wiki/topics/ai/agent-client-protocol|Agent Client Protocol]]
- [[wiki/topics/ai/agent-memory|Agent Memory]]
- [[wiki/syntheses/ai/agent-loop-control-boundaries|Agent 循环工作流的控制边界]]

## 来源指针

- [pi：事件序列、生命周期与输入队列][pi-readme]，源码快照 `e12dbfc9299049dc2e7a974612fec32001a7ba8a`。
- [DSH：目标与循环层级术语][dsh-glossary]，源码快照 `39163dd30f703a79079e2d2446545cff3c453738`。
- [OpenAI Agents SDK Runner][openai-runner]、[会话管理][openai-conversations]、[会话记忆示例][openai-memory]。
- [Claude Agent SDK：Turns and messages][claude-loop]、[服务端工具][claude-server-tools]、[工具结果格式][claude-tool-results]。
- [Vercel AI SDK：Tool Calling][ai-sdk]。
- [ACP v1：Prompt Turn][acp-turn]。
- [OpenTelemetry #332：turn 的计数与定义讨论][otel-turn]、[#418：非规范性术语表提案][otel-glossary]。
- [Weave Router：术语层级与旧命名][weave]，源码快照 `424e57b678c05fe61ac8b73c063c1cad20557635`。

[pi-readme]: https://github.com/earendil-works/pi/blob/e12dbfc9299049dc2e7a974612fec32001a7ba8a/packages/agent/README.md#event-flow
[dsh-glossary]: https://github.com/deepseek-ai/deepseek-harness/blob/39163dd30f703a79079e2d2446545cff3c453738/docs/glossary.zh.md#循环层级
[openai-runner]: https://openai.github.io/openai-agents-python/ref/run/
[openai-conversations]: https://openai.github.io/openai-agents-python/running_agents/#conversationschat-threads
[openai-memory]: https://developers.openai.com/cookbook/examples/agents_sdk/session_memory
[claude-loop]: https://code.claude.com/docs/en/agent-sdk/agent-loop#turns-and-messages
[claude-server-tools]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools
[claude-tool-results]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
[ai-sdk]: https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling
[acp-turn]: https://agentclientprotocol.com/protocol/v1/prompt-turn
[otel-turn]: https://github.com/open-telemetry/semantic-conventions-genai/issues/332
[otel-redefinition]: https://github.com/open-telemetry/semantic-conventions-genai/issues/332#issuecomment-4767960518
[otel-question]: https://github.com/open-telemetry/semantic-conventions-genai/issues/332#issuecomment-6452836851
[otel-glossary]: https://github.com/open-telemetry/semantic-conventions-genai/issues/418
[weave]: https://github.com/weave-os/router/blob/424e57b678c05fe61ac8b73c063c1cad20557635/docs/SEMANTICS.md#terms
