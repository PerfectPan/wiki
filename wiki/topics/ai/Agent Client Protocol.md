---
title: Agent Client Protocol
description: Editor/Client 与 coding agent 之间的 JSON-RPC 协议：v1 prompt turn、v2 draft 的 session state 与 upsert，以及与 MCP 的边界
type: topic
category: ai
status: active
created: 2026-04-25
updated: 2026-08-06
timestamp: 2026-08-06
tags:
  - acp
  - code-agent
  - protocol
  - capability-negotiation
  - editor
source_refs:
  - raw/sources/2026-08-06-agent-client-protocol-v1-v2-research.md
  - https://agentclientprotocol.com/get-started/introduction
  - https://agentclientprotocol.com/get-started/architecture
  - https://agentclientprotocol.com/protocol/v1/overview
  - https://agentclientprotocol.com/protocol/v1/prompt-turn
  - https://agentclientprotocol.com/protocol/v2/migration
  - https://agentclientprotocol.com/announcements/acp-v2-draft
resource:
  - raw/sources/2026-08-06-agent-client-protocol-v1-v2-research.md
  - https://agentclientprotocol.com/protocol/v2/migration
  - https://agentclientprotocol.com/announcements/acp-v2-draft
---
# Agent Client Protocol

## 摘要

Agent Client Protocol（ACP）标准化 **code editor / IDE（Client）** 与 **coding agent（Agent）** 之间的通信，角色类似 LSP：Agent 实现一次 ACP 即可接入兼容 Client；Client 支持 ACP 即可接入生态中的 Agent。

协议基于 **JSON-RPC 2.0**（Methods + Notifications）。本地场景下 Client 按需拉起 Agent 子进程，经 **stdio** 通信。内容类型尽量复用 [[MCP]] 的 JSON 表示，并增加 coding UX 所需的 diff、plan、permission 等类型。默认面向用户的文本是 Markdown。

| 版本 | 状态 | 心智模型 |
| --- | --- | --- |
| **v1** | 稳定，生态主力 | **Prompt turn**：`session/prompt` 挂起整轮，响应携带 `stopReason` |
| **v2** | Draft（公告 2026-07-20） | **Session lifecycle**：prompt 只表示受理；结束靠 `state_update`；消息/tool/plan 按 ID upsert |

实现应 **v1/v2 并存**：按 `initialize` 协商版本；v2 用 feature flag 闸住，稳定前不要默认生产开启。一手调研见 `raw/sources/2026-08-06-agent-client-protocol-v1-v2-research.md`。

## ACP 不是什么

- **不是** Agent 框架（规划、记忆、多 Agent 编排不在协议范围）。
- **不是** [[MCP]]：MCP 连接工具与数据；ACP 连接 editor 与 coding agent。二者常同时出现——Client 经 `mcpServers` 把 MCP 配置交给 Agent。
- **不是** 模型 API（Chat Completions / Responses / Messages）。
- **默认不是零信任沙箱**：官方信任模型是“在 editor 里使用可信 agent”；仍有 permission，但会暴露本地文件与 MCP 访问。

## 基本架构

```mermaid
flowchart TB
  User[用户] --> Client[Client / Editor]
  Client -->|JSON-RPC over stdio| Agent[Agent 子进程]
  Client -->|mcpServers 配置| Agent
  Agent --> MCP1[MCP Server A]
  Agent --> MCP2[MCP Server B]
  Client -.->|可选 stdio MCP proxy| Agent
```

| 角色 | 典型形态 | 职责 |
| --- | --- | --- |
| **Client** | IDE、编辑器、agent UI | UX、会话展示、权限确认、cwd / MCP 配置 |
| **Agent** | coding agent 子进程（或远程 agent） | 推理与工具执行、流式 `session/update`；v2 中拥有 session 历史与 `messageId` |

设计原则：**MCP-friendly**、**UX-first**、**Trusted**。一条连接可多 concurrent session。约定：路径绝对；行号 1-based；属性 `camelCase`，判别值 `snake_case`。

## 信任与边界

```mermaid
flowchart LR
  User[用户] -->|确认 permission| Client
  Client -->|拉起进程、cwd、mcpServers| Agent
  Agent -->|request_permission| Client
  Agent --> FS[工作区 FS / Shell]
  Agent --> Ext[外部 MCP]
```

v2 删除 Client 侧 `fs/*` 与 `terminal/*` 执行面后，Client 若仍要暴露本地能力，官方推荐走 **MCP server**（与其它工具同等），而不是 ACP 上的私有执行 API。Agent-owned terminal 在 v2 仅为 **display-only**。

## v1：Prompt Turn

### 消息流

```mermaid
sequenceDiagram
  participant C as Client
  participant A as Agent
  C->>A: initialize
  A-->>C: protocolVersion + agentCapabilities
  opt 需要登录
    C->>A: authenticate
  end
  C->>A: session/new 或 session/load
  loop Prompt Turn
    C->>A: session/prompt
    A-->>C: session/update
    A->>C: request_permission / fs/* / terminal/*
    C-->>A: 结果
    A-->>C: prompt result stopReason
  end
```

核心语义：`session/prompt` **在整轮期间保持 pending**；期间推送 `session/update`；最终响应用 `stopReason` 结束（`end_turn` | `max_tokens` | `max_turn_requests` | `refusal` | `cancelled`）。

### v1 能力要点

- **版本协商：** Client 发最新 `protocolVersion`；Agent 回支持版本；省略的 capability = 不支持；新能力优先靠 capability 加法，不靠涨 major。
- **Client 可选面：** `fs.readTextFile` / `fs.writeTextFile`、`terminal`、`elicitation` 等。
- **Agent 可选面：** `loadSession`、`promptCapabilities.*`、`mcpCapabilities.http|sse`、`sessionCapabilities.list|resume|close|delete`、`auth.logout` 等。
- **session/update 常见变体：** message chunks、`tool_call` / `tool_call_update`、`plan`、`usage_update`、`available_commands_update`、`current_mode_update`、`config_option_update`、`session_info_update`。
- **Diff：** `oldText` / `newText`；**Permission：** 以 `toolCall` 为中心。

### v1 张力（驱动 v2）

Turn 与后台更新、排队、多 Client 观察同一 session 难对齐；tool 创建/更新分裂；diff 难表达 delete/rename/binary；permission 文案污染 tool title；Client fs/terminal 实现参差。

## v2 Draft：Session lifecycle 与统一 upsert

**状态：** Draft。schema 分 `schema/v2/schema.json`（baseline）与 `schema.unstable.json`（opt-in）；**协商 `protocolVersion: 2` ≠ 开启全部 unstable 特性**。稳定前可能改；生产默认勿强切；**保留 v1**。

### 五大主题

1. **Beyond the turn：** prompt 响应 = 受理；进度/结束用 `state_update`；`session/update` 可随时发送。
2. **统一 upsert：** 按稳定 ID patch——省略不变、`null` 清空、有值替换、chunk 追加。
3. **Diff overhaul：** 结构化 `changes` + 可选 `git_patch`。
4. **Permission 解耦：** 必填 `title`、可选 `description`、可扩展 `subject`。
5. **默认前向兼容：** 开放 enum；`_` 前缀留给实现扩展。

### Prompt 生命周期

```mermaid
sequenceDiagram
  participant C as Client
  participant A as Agent
  C->>A: session/prompt
  A-->>C: result
  A-->>C: user_message + messageId
  A-->>C: state_update running
  A-->>C: chunks / tool_call_update / plan_update
  opt 等待用户
    A-->>C: state_update requires_action
    A->>C: session/request_permission
    C-->>A: selected 或 cancelled
    A-->>C: state_update running
  end
  A-->>C: state_update idle + stopReason
  Note over A,C: idle 时仍可有后台 update
```

| 前景信号 | v1 | v2 |
| --- | --- | --- |
| 已受理 | 隐含（request 挂起） | `session/prompt` → `{}` |
| 用户消息进历史 | 隐含 | `user_message` / chunks（Agent 生成 `messageId`） |
| 工作中 | prompt pending | `state_update: running` |
| 等用户 | 隐含 | `state_update: requires_action` |
| 结束 | prompt + `stopReason` | `idle` + `stopReason` |
| 取消确认 | prompt `cancelled` | idle + `cancelled` |

`stopReason` 取值集合与 v1 相同，仅位置迁移。**idle = 可接新 prompt**；后台 update 可不改变 state。Queueing / steering **尚未**由该 lifecycle 单独标准化。

### 迁移对照（压缩）

| 区域 | v1 | v2 |
| --- | --- | --- |
| 初始化 | `clientCapabilities` / `agentCapabilities`；info 可选 | 双向 `capabilities` + **必填** `info` |
| 支持标记 | bool 与 `{}` 混用 | **一律对象**；有/`{}`=支持 |
| Session 能力 | 分散可选 marker | `capabilities.session` 存在 ⇒ **基线方法必实现** |
| 认证 | `authenticate` / `logout` | `auth/login` / `auth/logout` |
| 加载会话 | `session/load` + `session/resume` | 仅 `session/resume` + 可选 `replayFrom` |
| 模式 | `session/set_mode`、`current_mode_update` | config options（`category: mode` 等） |
| Client fs/terminal | 可选执行面 | **删除**；本地能力走 MCP |
| Tool 通知 | `tool_call` + `tool_call_update` | 仅 `tool_call_update` + `tool_call_content_chunk` |
| Plan | `plan` 无 ID | `plan_update` + `planId` |
| Diff | `oldText`/`newText` | `changes` + 可选 `patch.git_patch` |
| MCP 配置 | stdio 可无 `type`；可有 SSE | 必填 `type`；**去掉 SSE** |

**Session 基线方法**（声明 `capabilities.session` 即承诺）：`session/new`、`session/list`、`session/resume`、`session/close`、`session/prompt`、`session/cancel`、`session/update`。`session/delete` 等仍可选。

### 扩展面

```mermaid
flowchart TB
  JR[JSON-RPC 2.0 / stdio] --> Upsert[ID upsert 与 chunk]
  JR --> State[state_update]
  Cap[capabilities.session] --> Baseline[基线 session 方法]
  Ext[_meta / _methods / _enums] --> JR
  Agent --> MCP[mcpServers]
  RemoteRFD[Remote transport RFD] -.->|非 core v2 surface| JR
```

stdio 仍是主路径；v2 明确 JSON-RPC **batch**，但不要 batch `initialize`、`auth/login`、`session/new|resume|prompt`。标准 HTTP/WebSocket 在独立 RFD 与 Transports WG，**不是** migration 所称的 core v2 surface。

## 与 MCP、Code Agent

| 层 | 连接 | 解决 |
| --- | --- | --- |
| [[MCP]] | Host ↔ 外部工具/数据 | 发现、调用、授权 |
| **ACP** | Editor ↔ Coding Agent | 会话、流式 UX、permission、diff/plan、能力协商 |
| [[Code Agent]] / `AGENTS.md` | 仓库 ↔ agent 行为 | 权限、流程、输出约定 |

## 实现要点

1. 每连接协商恰好一个 major 版本；共享业务逻辑 + 两套 thin protocol surface。
2. v2 与 unstable 特性分别 feature flag。
3. Upsert 必须区分 **omitted / null / concrete**（含 `_meta`、content、terminal output）。
4. v2 UI 跟 `state_update` 与 `user_message` ack，不要把 prompt 响应当 turn 结束。
5. Cancel 后仍接受 update，直到 idle + `cancelled`。
6. 未知 permission outcome **不得**当批准；未知 enum 尽量透传，勿占用无 `_` 前缀值。
7. Terminal：每 chunk 单独 base64 decode 再 append；后续 snapshot 整段替换。

## 证据矩阵

| 结论 | 证据位置 | 置信度 |
| --- | --- | --- |
| ACP 标准化 editor↔coding agent，类比 LSP | introduction | 高 |
| 本地 stdio 子进程、多 session、MCP-friendly / Trusted | architecture | 高 |
| v1 prompt turn：响应带 stopReason 结束 | v1 prompt-turn / overview | 高 |
| v2 Draft；双版本 + feature flag；勿默认生产开 | acp-v2-draft 公告、migration | 高 |
| prompt `{}` 仅受理；完成靠 state_update | migration、v2 prompt-lifecycle | 高 |
| 删除 Client fs/terminal；改走 MCP | migration | 高 |
| Diff → changes + 可选 git_patch | migration | 高 |
| Remote HTTP/WS 非 core v2 surface | migration Transports；transport RFD 并行 | 高（进度会变） |
| Queueing 未由 prompt lifecycle 标准化 | v2 prompt RFD 范围说明 | 高 |

完整 URL 与方法对照表见调研笔记。

## 当前张力 / 风险 / 未决

- v2 仍 Draft，无已读文档中的 GA 日期；字段可能变。
- 双栈与 SDK dual-version 表达成本高。
- 去掉 Client 执行面后，短期依赖各 Client 是否提供合格 MCP filesystem/terminal。
- Remote transport 与 “是否算 v2” 在 migration 与 transport RFD 表述上需区分：实现以 core 不含标准 HTTP 为准。
- Multi-client 同 session、排队/steering 多为设计动机，完整冲突规则未在本次精读展开。
- MCP-over-ACP 等 RFD 仅索引、未展开。
- Unstable schema 特性列表未逐条核对 schema 文件。

## 相关页面

- [[Code Agent]]
- [[Agent]]
- [[MCP]]
- [[MCP Client]]

## 来源指针

- 调研笔记：[[raw/sources/2026-08-06-agent-client-protocol-v1-v2-research.md]]
- [Introduction](https://agentclientprotocol.com/get-started/introduction)
- [Architecture](https://agentclientprotocol.com/get-started/architecture)
- [v1 Overview](https://agentclientprotocol.com/protocol/v1/overview) / [Prompt Turn](https://agentclientprotocol.com/protocol/v1/prompt-turn)
- [v2 Migration](https://agentclientprotocol.com/protocol/v2/migration) / [Prompt Lifecycle](https://agentclientprotocol.com/protocol/v2/prompt-lifecycle)
- [ACP v2 Draft 公告](https://agentclientprotocol.com/announcements/acp-v2-draft)
- [v2 RFD overview](https://agentclientprotocol.com/rfds/v2/overview) / [Prompt RFD](https://agentclientprotocol.com/rfds/v2/prompt)
