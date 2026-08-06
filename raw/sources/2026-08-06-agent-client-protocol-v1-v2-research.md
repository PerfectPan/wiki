---
title: Agent Client Protocol v1 / v2 draft research
date: 2026-08-06
topic: Agent Client Protocol
sources:
  - https://agentclientprotocol.com/llms.txt
  - https://agentclientprotocol.com/get-started/introduction.md
  - https://agentclientprotocol.com/get-started/architecture.md
  - https://agentclientprotocol.com/protocol/v1/overview.md
  - https://agentclientprotocol.com/protocol/v1/initialization.md
  - https://agentclientprotocol.com/protocol/v1/prompt-turn.md
  - https://agentclientprotocol.com/protocol/v1/session-setup.md
  - https://agentclientprotocol.com/protocol/v1/tool-calls.md
  - https://agentclientprotocol.com/protocol/v1/transports.md
  - https://agentclientprotocol.com/protocol/v2/overview.md
  - https://agentclientprotocol.com/protocol/v2/migration.md
  - https://agentclientprotocol.com/protocol/v2/prompt-lifecycle.md
  - https://agentclientprotocol.com/announcements/acp-v2-draft.md
  - https://agentclientprotocol.com/rfds/v2/overview.md
  - https://agentclientprotocol.com/rfds/v2/prompt.md
  - https://agentclientprotocol.com/rfds/streamable-http-websocket-transport.md
---

# Agent Client Protocol v1 / v2 draft research

## 调研范围与日期

- **Access date:** 2026-08-06
- **Primary site:** https://agentclientprotocol.com（优先 `.md` URL，索引见 `llms.txt`）
- **范围：** ACP v1 稳定协议核心（定位、架构、initialize、session、prompt turn、tool calls、transport）+ ACP v2 Draft（overview、migration、prompt lifecycle、announcement、v2 RFD collection、remote transport RFD 标题/状态）
- **未深入：** 完整 JSON Schema 逐字段、各语言 SDK 实现细节、v1 已 stabilize 的次要 RFD（elicitation、session list 等仅在对照中出现）
- **方法：** 仅依据官方文档/RFD 事实；推断单独标注

## 协议定位（是什么 / 不是什么）

### 是什么（docs 事实）

- ACP = **Agent Client Protocol**：标准化 **code editors/IDEs** 与 **coding agents** 之间的通信。([introduction](https://agentclientprotocol.com/get-started/introduction.md))
- 类比 **LSP**：agent 实现一次 ACP → 任意兼容 editor；editor 支持 ACP → 接入整个 agent 生态。([introduction](https://agentclientprotocol.com/get-started/introduction.md))
- 假设用户主要待在 editor，按需调用 agent 完成具体任务。([introduction](https://agentclientprotocol.com/get-started/introduction.md))
- 消息编码：**JSON-RPC 2.0**；Methods（请求-响应）+ Notifications（单向）。([v1 overview](https://agentclientprotocol.com/protocol/v1/overview.md), [v2 overview](https://agentclientprotocol.com/protocol/v2/overview.md))
- 尽量复用 **MCP** 的 JSON 表示；为 agentic coding UX 增加自定义类型（如 diffs）。用户可读文本默认 **Markdown**（不必渲染 HTML）。([introduction](https://agentclientprotocol.com/get-started/introduction.md))
- 命名约定：ACP JSON 对象属性默认 `camelCase`；discriminator 字符串值默认 `snake_case`；JSON-RPC 信封字段遵循 JSON-RPC 2.0。([v1/v2 overview](https://agentclientprotocol.com/protocol/v1/overview.md))
- 路径 **MUST** 为绝对路径；行号 1-based。([v1/v2 overview](https://agentclientprotocol.com/protocol/v1/overview.md))

### 不是什么 / 边界

- **不是** LLM provider API、也不是替代 MCP 的 tool protocol；MCP 是 agent 连接外部 tools/data 的通道，ACP 是 editor↔agent 会话与 UX 协议。([architecture](https://agentclientprotocol.com/get-started/architecture.md), [session-setup MCP](https://agentclientprotocol.com/protocol/v1/session-setup.md))
- **不是** “仅本地”：定位 local + remote；但 full remote agent 支持 **WIP**（intro 明确）。([introduction](https://agentclientprotocol.com/get-started/introduction.md))
- **信任模型不是零信任沙箱默认：** “ACP works when you're using a code editor to talk to a model you trust”；editor 仍控制 tool call 权限，但会给 agent 本地文件与 MCP 访问。([architecture — Trusted](https://agentclientprotocol.com/get-started/architecture.md))

## 架构与信任模型

来源：[architecture](https://agentclientprotocol.com/get-started/architecture.md)

### 设计原则

1. **MCP-friendly：** JSON-RPC + 复用 MCP types，避免再发明 common data types。
2. **UX-first：** 解决与 AI agent 交互的 UX；足够表达 agent intent，不过度抽象。
3. **Trusted：** 信任模型见上；permission 仍在 client 侧可控。

### 运行时拓扑

- 用户连接 agent 时，editor **按需启动 agent 子进程**；通信默认 **stdin/stdout**。
- **一条连接可多个 concurrent sessions**（多条并行对话）。
- 大量使用 **JSON-RPC notifications** 做实时 UI 流式更新。
- **双向请求**：agent 可向 editor 发请求（例：tool call permission）。

### MCP 集成模式

- Client 把用户配置的 MCP server 配置在 prompt/session 路径传给 agent，**agent 直连 MCP**。
- Client 也可导出自己的 MCP tools：不在同一 socket 混跑 MCP+ACP；client 可提供 **stdio proxy** 把 MCP 请求隧道回 editor。

## v1 核心模型

### 典型消息流

来源：[v1 overview](https://agentclientprotocol.com/protocol/v1/overview.md)

1. **Initialization：** `initialize` →（可选）`authenticate`
2. **Session setup：** `session/new` 或（若支持）`session/load` / `session/resume`
3. **Prompt turn：** `session/prompt` → 多个 `session/update` →（可选）permission/fs/terminal →（可选）`session/cancel` → **`session/prompt` response 带 `stopReason` 结束 turn**

### Initialize（v1）

来源：[v1 initialization](https://agentclientprotocol.com/protocol/v1/initialization.md)

- Client **MUST** 调用 `initialize`，携带：
  - `protocolVersion`：单个整数，标识 **MAJOR** 版本；仅 breaking 时递增
  - `clientCapabilities`
  - **SHOULD** `clientInfo`（name / title / version）
- Agent 响应：选定 `protocolVersion`、`agentCapabilities`、**SHOULD** `agentInfo`、`authMethods`
- **版本协商：** Client 发自己支持的最新版本；Agent 若支持则回同版本，否则回自己最新；Client 若不支持 Agent 版本 **SHOULD** 断开并告知用户
- 省略的 capability = **UNSUPPORTED**（非 breaking 加能力靠 capability，不靠版本号）

#### v1 Client capabilities（摘要）

| Capability | 含义 |
| --- | --- |
| `fs.readTextFile` / `fs.writeTextFile` | 暴露 `fs/read_text_file` / `fs/write_text_file` |
| `terminal` | 全部 `terminal/*` |
| `elicitation` | `elicitation/create` 模式（form/url）；`{}` 不等于 form support（与 MCP 不同） |
| `session.configOptions.boolean` | 支持 boolean config options |

#### v1 Agent capabilities（摘要）

| Capability | 含义 |
| --- | --- |
| `loadSession` | `session/load` |
| `promptCapabilities.image/audio/embeddedContext` | prompt 内容类型；基线 MUST 支持 Text + ResourceLink |
| `mcpCapabilities.http` / `sse` | MCP 传输（sse 已被 MCP 废弃） |
| `auth.logout` | `logout` 方法 |
| `sessionCapabilities`：`delete` / `additionalDirectories` / `resume` / `close` / `list` 等 | 各 session 扩展方法 |

文档注：`session/load` 仍由顶层 `loadSession` 处理，“将在未来版本统一”。

### Session setup（v1）

来源：[v1 session-setup](https://agentclientprotocol.com/protocol/v1/session-setup.md)

| Method | 作用 | 门控 |
| --- | --- | --- |
| `session/new` | 创建会话；params：`cwd` + `mcpServers`（v1 中 mcpServers 在示例中为必填列表） | baseline |
| `session/load` | 恢复并 **replay 全历史** 为 `session/update` | `loadSession` |
| `session/resume` | 恢复 **不 replay** | `sessionCapabilities.resume` |
| `session/close` | 取消进行中工作并释放 active session 资源 | `sessionCapabilities.close` |
| `session/delete` | 从 history 删除（另文） | `session.delete` 类 capability |

- `sessionId`：opaque 会话 ID
- `cwd`：绝对路径；session 主工作目录；与 `additionalDirectories` 组成 effective root set
- MCP servers：stdio **MUST** 支持；http/sse 看 capability；stdio 配置无 `type` 字段（与 v2 对比）

### Prompt turn（v1）——响应即 turn 结束

来源：[v1 prompt-turn](https://agentclientprotocol.com/protocol/v1/prompt-turn.md)

1. Client → `session/prompt`（`sessionId` + `prompt: ContentBlock[]`）
2. Agent 处理 LLM；通过 `session/update` 流式输出
3. 无 pending tool calls 时，Agent **MUST** 用带 `stopReason` 的 **prompt response** 结束
4. Tool 路径：`tool_call` → 可选 `session/request_permission` → `tool_call_update`（in_progress/completed）→ 结果回 LLM → 循环
5. Cancel：Client `session/cancel` notification；Agent 最终 **prompt response** `stopReason: "cancelled"`

**StopReason（v1，在 prompt response）：** `end_turn` | `max_tokens` | `max_turn_requests` | `refusal` | `cancelled`

#### v1 `session/update` 变体（文档出现）

| `sessionUpdate` | 用途 |
| --- | --- |
| `user_message_chunk` | 用户消息块（load replay） |
| `agent_message_chunk` | agent 文本流；`messageId` **可选** |
| `agent_thought_chunk` | 思考流 |
| `plan` | 扁平 entries 列表（无 planId） |
| `tool_call` | 创建 tool call |
| `tool_call_update` | 更新 tool call（字段可选 patch 风格） |
| `usage_update` | `used`/`size` 必填 token；可选 `cost` |
| `available_commands_update` | slash commands |
| `current_mode_update` | session mode 变更 |
| `config_option_update` | config options |
| `session_info_update` | session 元信息 |

### Tool calls（v1）

来源：[v1 tool-calls](https://agentclientprotocol.com/protocol/v1/tool-calls.md)

- 创建：`sessionUpdate: "tool_call"`，字段含 `toolCallId`, `title`, `kind`, `status`, `content`, `locations`, `rawInput`, `rawOutput`
- 更新：`tool_call_update`，除 `toolCallId` 外可选
- **kind：** `read` | `edit` | `delete` | `move` | `search` | `execute` | `think` | `fetch` | `other`（默认）
- **status：** `pending` | `in_progress` | `completed` | `failed`
- **content 类型：** regular content / `diff`（`path`, `oldText`, `newText`）/ `terminal`（`terminalId` 引用 client `terminal/create`）
- **Permission：** `session/request_permission` params 含 `toolCall` + `options[]`（`optionId`, `name`, `kind`: allow_once/allow_always/reject_once/reject_always）；outcome `selected` 或 `cancelled`

### v1 Client surfaces（Agent → Client methods）

来源：[v1 overview](https://agentclientprotocol.com/protocol/v1/overview.md)

| 方向 | Method | 基线/可选 |
| --- | --- | --- |
| Client→Agent baseline | `initialize`, `authenticate`, `session/new`, `session/prompt` | baseline |
| Client→Agent optional | `session/load`, `logout`, `session/set_mode`, list/delete/resume/close 等 | capability |
| Client→Agent notif | `session/cancel` | baseline |
| Agent→Client baseline | `session/request_permission` | baseline |
| Agent→Client optional | `fs/*`, `terminal/*`, `elicitation/create` | capability |
| Agent→Client notif | `session/update`, `elicitation/complete` | |

### 扩展性（v1）

- `_meta` 自定义数据
- `_` 前缀自定义 methods
- initialize 时广告 custom capabilities

## v2 Draft 状态与设计目标

### Draft 状态（必须强调）

来源：[acp-v2-draft 公告](https://agentclientprotocol.com/announcements/acp-v2-draft.md)（Published: **2026-07-20**）、[migration](https://agentclientprotocol.com/protocol/v2/migration.md)

- **v2 整体为 Draft**：文档与 schema 已发布供 review/testing
- **“various pieces can, and will, change before stabilization”**
- 实现要求：
  1. 走 **version negotiation**（`protocolVersion: 2`）
  2. **再** 用 **feature flags** 门控；**不要默认生产开启** 直到接近 stabilize
- **不要丢弃 v1**：v1-only peers 会长期存在；推荐双版本并存
- Schema 发布形态：仓库 releases 中 `v2.0.0-alphaX` 与 v1 并列；另有 `schema/v2/schema.json`（stable v2 baseline）与 `schema/v2/schema.unstable.json`（opt-in draft layers）
- 协商 `protocolVersion: 2` **不** 自动包含 unstable 层特性；各自 capability/flag 门控

### 设计目标 / Big themes（出发点 Why → What）

来源：公告 + [rfds/v2/overview](https://agentclientprotocol.com/rfds/v2/overview.md) + [migration 开篇](https://agentclientprotocol.com/protocol/v2/migration.md) + [prompt RFD](https://agentclientprotocol.com/rfds/v2/prompt.md)

**Why（公告原意）：**

- v1 可用 RFD 快速加法，但 **部分 breaking** 才能解锁：更丰富的 session 状态、巩固有用模式、整体一致性。
- v2 = **consolidation**，故意不塞满 optional 新功能（那些继续 RFD）；聚焦改核心行为。
- Agent 工作更长、更多后台编排后，**turn 所有权绑在 pending `session/prompt`** 让 client（要保证交互模式）与 agent（要随时 update、idle 仍可后台推）都不爽。
- 需要清晰支持：queueing / steering、非用户发起工作的实时更新、多 client 观察、replay 时用户消息的权威插入点。

**What（主题）：**

1. **Moving beyond the turn** — prompt 响应 = 接受确认，不是 turn 结束；`session/update` 可随时流动；显式 idle/running/requires_action
2. **统一 upsert/patch + streaming** — message / tool call / plan / terminal 按 ID patch；omitted / null / value / chunks append
3. **Diff overhaul** — 结构化 file operations + 可选 `git_patch`
4. **更灵活 permission** — 独立 title/description + extensible `subject`
5. **Forward compatibility by default** — 开放 enum/tagged union；`_` 前缀扩展
6. **删除生态已迁移离开的 surface** — Client fs/terminal 执行 API、dedicated modes API、session/load 等
7. **Capability 重组** — 统一 `capabilities` + required `info`；object support markers；session baseline 方法集合

### Migration 文档的 “五条记忆点”

1. `session/prompt` response **不再结束 turn**；完成靠 `state_update`
2. Updates 是 **upserts**（三态 patch + chunks append）
3. Client **fs / terminal execution / session modes API 删除**；显示型 terminal 是 agent-owned
4. Capabilities 重组；session 基线方法必选
5. 一切可扩展（unknown enum values）

## v2 相对 v1 的 breaking / 语义变化

### 1. Prompt lifecycle（最大语义变化）

| 信号 | v1 | v2 |
| --- | --- | --- |
| Prompt 已接受 | 隐式（request 挂起） | `session/prompt` → `{}` 立即响应 |
| 用户消息进历史 | 隐式 = request 本身 | **必须** `user_message` 或 `user_message_chunk`（agent 拥有 `messageId`） |
| 前台工作中 | prompt 仍 pending | `state_update` `state: "running"` |
| 等待用户 | 隐式（permission pending） | `state_update` `state: "requires_action"` |
| 前台结束 | prompt response + `stopReason` | `state_update` `state: "idle"` + `stopReason` |
| 取消确认 | prompt response `cancelled` | idle `state_update` + `stopReason: "cancelled"` |

**StopReason 集合不变**（`end_turn` / `max_tokens` / `max_turn_requests` / `refusal` / `cancelled`），只是位置从 prompt response 移到 idle state_update。v2 允许 custom stop reason：`_` 前缀；无 `_` 的未知值留给未来 ACP。

**idle 语义：** 可接受新 prompt；**background 更新仍可继续**，不改变 state。([prompt-lifecycle](https://agentclientprotocol.com/protocol/v2/prompt-lifecycle.md), [migration](https://agentclientprotocol.com/protocol/v2/migration.md), [prompt RFD](https://agentclientprotocol.com/rfds/v2/prompt.md))

动机（RFD/公告）：queueing、multi-client 观察同一 session、agent 发起更新、background work、replay 一致性。

### 2. Initialize / capabilities

| 项 | v1 | v2 |
| --- | --- | --- |
| 能力字段名 | `clientCapabilities` / `agentCapabilities` | 双向统一 `capabilities` |
| 实现信息 | 可选 `clientInfo` / `agentInfo` | 双向 **required** `info` |
| 支持标记 | boolean 与 object 混用 | **一律 object**：`{}`=支持，省略/`null`=不支持 |
| Session 组 | 顶层 `loadSession`、`promptCapabilities`、`mcpCapabilities`、`sessionCapabilities.*` | 嵌套 `capabilities.session`；`prompt`→`session.prompt`，`mcp`→`session.mcp` |
| `capabilities.session` | N/A | **可选**；存在则承诺 baseline session methods |
| Client fs/terminal caps | 有 | **删除**；stable v2 无标准 Client capability 字段 |
| protocolVersion | `1` | `2` |

**v2 session baseline（广告 `capabilities.session` 即承诺）：**  
`session/new`, `session/list`, `session/resume`, `session/close`, `session/prompt`, `session/cancel`, `session/update`  
可选仍单独标记：`session.delete`, `session.additionalDirectories`, `session.prompt.*`, `session.mcp.*`

### 3. Authentication

| v1 | v2 |
| --- | --- |
| `authenticate` | `auth/login` |
| `logout`（`agentCapabilities.auth.logout` 门控） | `auth/logout`；**无 logout capability marker** |
| auth method `id` | `methodId`；**required** `type` discriminator（stable: `"agent"`） |
| — | 非空 `authMethods` ⇒ **MUST** 实现 login+logout；空/省略 ⇒ Client **MUST NOT** 调用 |

### 4. Session lifecycle methods

| v1 | v2 |
| --- | --- |
| `session/load`（replay） | **删除**；用 `session/resume` + `replayFrom: { "type": "start" }` |
| `session/resume`（无 replay，capability 门控） | **Required**；可选 `replayFrom`（省略/null = 不 replay） |
| `session/list` / `session/close` | **Required**（在 session capability 下） |
| `session/new` 的 `mcpServers` | 现为 **optional**（省略 ≡ `[]`） |
| 响应中的 `modes` | **删除** |
| `session/set_mode` + `current_mode_update` | **删除** → `session/set_config_option` + `config_option_update`；config `category: "mode"` 等 |
| config option `id` | `configId`；select group `group`→`groupId` |
| stable categories | `mode`, `model`, `model_config`, `thought_level` |

### 5. Messages

| v1 | v2 |
| --- | --- |
| `messageId` 可选 | **所有** message update/chunk **必填**；agent 生成 opaque string |
| 仅 chunks | 新增 whole-message upsert：`user_message`, `agent_message`, `agent_thought`（`content` **数组**） |
| — | 三态：omitted content=不变；`null` 或 `[]`=清空；concrete array=整段替换；chunks **append** |

### 6. Tool calls

| v1 | v2 |
| --- | --- |
| `tool_call` + `tool_call_update` | **仅** `tool_call_update`（首次未见 `toolCallId` = 创建） |
| — | 新增 `tool_call_content_chunk`（append 单个 ToolCallContent） |
| status 无 cancelled | status 增加 `cancelled`；enums 可扩展 |
| kind 集合 | 文档称 field set 与 kind 值 **unchanged**（仍可扩展） |

### 7. Terminals

| v1 | v2 |
| --- | --- |
| Client `terminal/*` 执行与控制 | **全部删除** |
| tool content `terminal` → Client 拥有的 terminal | Agent-owned **display-only** 引用 `terminalId` |
| — | `terminal_update` upsert（command/cwd/output snapshot/exitStatus） |
| — | `terminal_output_chunk`：独立 base64 字节 append |
| — | 无 input/resize/interrupt/kill/wait/release/execution 语义 |

### 8. Diffs

| v1 | v2 |
| --- | --- |
| `{ type, path, oldText, newText }` | `{ type: "diff", changes: [...], patch?: { format, text } }` |
| 难区分 delete vs empty | `operation: delete|add|modify|move|copy` |
| — | `fileType`: text/binary/directory/symlink；可选 mimeType |
| — | optional `patch.format: "git_patch"`（绝对路径；无 commit envelope） |
| — | **无** 机械映射回 oldText/newText |

### 9. Permissions

| v1 | v2 |
| --- | --- |
| params 以 `toolCall` 为中心 | **required** `title`；optional `description`；optional `subject` tagged union |
| 常把 prompt 文案塞进 tool title | title 不更新 tool 显示标题 |
| — | `subject.type: "tool_call"`（ToolCallUpdate upsert）或 `"command"`（command + abs cwd + 可选 toolCallId/terminalId） |
| options/outcome | 基本不变；未知 outcome **MUST NOT** 当 approval |
| — | pending 时 **SHOULD** `requires_action` |

### 10. Plans

| v1 | v2 |
| --- | --- |
| `sessionUpdate: "plan"` + entries | `plan_update` + `{ type: "items", planId, entries }` |
| 无 identity | `planId` 支持多 plan；同 id 替换 entries |
| — | status 可有 `cancelled`；priority/status 可扩展 |

### 11. MCP config

| v1 | v2 |
| --- | --- |
| stdio 无 `type` | **必须** `type`（stdio 为 `"stdio"`） |
| `type: "sse"` 可选 | **删除** SSE |
| mcpCaps http/sse | `session.mcp.stdio` + `session.mcp.http`；stdio 可 opt-out |
| args/env/headers 常必填空数组 | optional |

### 12. Content / slash commands / 命名

- Content block 五类型不变：`text`, `image`, `audio`, `resource_link`, `resource`；对齐最新 MCP（如 `resource_link.icons`）；type 可扩展
- Slash command `input`：v1 无 tag → v2 `type: "text"` tagged union
- ID 命名统一：domain-specific（`sessionId`, `messageId`, `toolCallId`, `planId`, `methodId`, `configId`…）禁止泛化 `id`
- 开放 enum：`_` 前缀 = 实现扩展；无 `_` 未知值 = 未来 ACP；receiver **SHOULD** preserve when proxying

### 13. 删除的 Client 执行面（迁移含义）

Client 若需给 agent 文件/未保存缓冲/命令执行能力：通过 session 的 **`mcpServers` 提供 MCP server**，与其他 tools 同等。Agent 侧删除双路径 capability 检查。文件变更用 diff content 报告。

## 方法与 session/update 对照表

### Methods

| Method | v1 | v2 |
| --- | --- | --- |
| `initialize` | 有（字段结构不同） | 有（`info`+`capabilities`） |
| `authenticate` | 有 | → `auth/login` |
| `logout` | 有（cap） | → `auth/logout`（随 authMethods） |
| `session/new` | 有 | 有（mcpServers optional） |
| `session/load` | 有（cap） | **移除** |
| `session/resume` | 有（cap） | **Required** + `replayFrom` |
| `session/list` | 有（cap） | **Required** |
| `session/close` | 有（cap） | **Required** |
| `session/delete` | 有（cap） | 仍 optional |
| `session/prompt` | 有；response=结束 | 有；response=接受 |
| `session/cancel` | 有 | 有；完成靠 state_update |
| `session/set_mode` | 有 | **移除** |
| `session/set_config_option` | 有 | 有 |
| `session/request_permission` | 有（toolCall 中心） | 有（title+subject） |
| `session/update` | 有 | 有（变体变） |
| `fs/*` | 有（cap） | **移除** |
| `terminal/*` | 有（cap） | **移除** |
| `$/cancel_request` | 有 | 有（unchanged per migration） |
| `elicitation/*` | 有 | 有（overview 仍列 optional） |

### `sessionUpdate` 变体

| Variant | v1 | v2 |
| --- | --- | --- |
| `user_message_chunk` | 有；messageId 可选 | 有；messageId **必填** |
| `agent_message_chunk` | 有 | 有；messageId 必填 |
| `agent_thought_chunk` | 有 | 有；messageId 必填 |
| `user_message` / `agent_message` / `agent_thought` | 无 | **新增** whole-message upsert |
| `state_update` | 无 | **新增** running/idle/requires_action |
| `tool_call` | 有 | **移除** |
| `tool_call_update` | 有 | 有（唯一 tool upsert） |
| `tool_call_content_chunk` | 无 | **新增** |
| `terminal_update` / `terminal_output_chunk` | 无 | **新增** |
| `plan` | 有 | → `plan_update` |
| `current_mode_update` | 有 | **移除**（→ config_option_update） |
| `available_commands_update` | 有 | 有（input tagged） |
| `config_option_update` | 有 | 有 |
| `session_info_update` | 有 | 有 |
| `usage_update` | 有 | 有 |

## 与 MCP 的关系

**事实（docs）：**

- ACP **复用 MCP JSON 表示** where possible（content blocks 等）。([introduction](https://agentclientprotocol.com/get-started/introduction.md), [architecture](https://agentclientprotocol.com/get-started/architecture.md))
- Session 创建/恢复时 Client 可传 `mcpServers`；Agent 连接这些 MCP 获取 tools/data。([session-setup](https://agentclientprotocol.com/protocol/v1/session-setup.md))
- 不在同一 socket 混跑 MCP 与 ACP；editor 可用 stdio proxy 暴露自身 MCP。([architecture](https://agentclientprotocol.com/get-started/architecture.md))
- v1：stdio MCP MUST；http/sse 可选（sse deprecated by MCP）。v2：显式 `session.mcp.stdio` / `http`；**移除 SSE**；配置必须带 `type`。([migration](https://agentclientprotocol.com/protocol/v2/migration.md))
- v2 删除 Client fs/terminal 后，**MCP 成为 Client 向 Agent 暴露本地能力的推荐路径**。([migration — Client file system and terminal](https://agentclientprotocol.com/protocol/v2/migration.md))
- llms.txt / RFD 索引另有 **MCP-over-ACP** RFD（`rfds/mcp-over-acp`）——本次未展开正文。
- v2 RFD overview “RFDs to be Written” 提到 MCP tool timeouts、更多 lifecycle methods 仍待写。([rfds/v2/overview](https://agentclientprotocol.com/rfds/v2/overview.md))

**推断（非 docs 原话）：** ACP 与 MCP 是互补层：MCP=tool/context 总线，ACP=editor agent 会话与权限/UX 编排。实现上 agent 往往同时是 ACP server 与 MCP client。

## Transport 现状

### stdio（v1 与 v2 主路径）

来源：[v1 transports](https://agentclientprotocol.com/protocol/v1/transports.md), [migration Transports](https://agentclientprotocol.com/protocol/v2/migration.md)

- Client 启 agent 子进程；newline-delimited JSON-RPC；消息 **MUST NOT** 内嵌 newline
- stderr 可日志；stdout **仅** ACP 消息
- Agents/clients **SHOULD** 支持 stdio
- **v2 明确 JSON-RPC 2.0 batch：** 一行可以是 batch array；可并发处理 batch 项；notification 不回复；非法 entry 用 `-32600`；**不要** batch 生命周期敏感消息：`initialize`, `auth/login`, `session/new`, `session/resume`, `session/prompt`

### Remote transport

- Intro：remote 可用 HTTP/WebSocket，但 full support **WIP**。([introduction](https://agentclientprotocol.com/get-started/introduction.md))
- v1 transports 页：Streamable HTTP 标注 *draft proposal in progress*
- **RFD：** [Streamable HTTP & WebSocket Transport](https://agentclientprotocol.com/rfds/streamable-http-websocket-transport.md)
  - 标题/状态要点：统一 `/acp`；Streamable HTTP（POST/GET/DELETE，HTTP/2，长连接 SSE：connection-scoped + per-session）+ WebSocket upgrade
  - Headers：`Acp-Connection-Id`, `Acp-Session-Id`；cookie 亲和
  - Migration 写明：**标准 remote transport 在独立 RFD，不是 core v2 protocol surface 的一部分**
  - RFD 自身把部分 durability 标为 v1 additive / v2 增强（message IDs、Last-Event-ID resume 等）——与 “remote 是否进 v2 core” 的 migration 表述需区分（见未决）
- 另有公告 *Transports Working Group*（llms.txt 索引）

### Custom transports

- 允许；须保持 JSON-RPC 消息格式与 lifecycle；应文档化连接模式。([v1 transports](https://agentclientprotocol.com/protocol/v1/transports.md))

## 实现注意事项（双版本、feature flag、三态 patch）

来源：[migration — Supporting v1 and v2](https://agentclientprotocol.com/protocol/v2/migration.md), [acp-v2-draft](https://agentclientprotocol.com/announcements/acp-v2-draft.md), [rfds/v2/overview SDK](https://agentclientprotocol.com/rfds/v2/overview.md)

1. **每连接恰好一个协商版本**（initialize 后）；共享应用逻辑 + 两套 thin protocol surface。
2. **v2 默认关闭 + feature flag**；unstable schema 特性再单独门控。
3. **三态字段建模：** omitted ≠ null ≠ concrete value。普通 optional/nullable 类型会抹掉协议语义（尤其 upsert `_meta`、content、terminal output）。
4. **Agent 拥有 session history 与 messageId**；Client 不能在协议层抢先分配 messageId（v2）。
5. **UI 驱动源切换：** v1 盯 prompt response；v2 盯 `state_update` + `user_message` ack。
6. **取消：** v2 在 cancel 后仍接受 updates，直到 idle+`cancelled`。
7. **未知 enum：** preserve + 安全降级；不要发明无 `_` 前缀的自定义值。
8. **未知 permission outcome：MUST NOT 当批准。**
9. **Diff：** Client 用 `changes` 建树；有 `patch.text` 再渲染；无 patch 时处理 binary/symlink。
10. **Terminal bytes：** 每 chunk 单独 base64 decode 再 append；勿先拼 base64 字符串；chunk 可切开 UTF-8/ANSI，解析器需跨 chunk 状态；后续 `terminal_update.output` snapshot **整段替换**。
11. **SDK：** v1/v2 schema、models、fixtures 完全分离；Rust schema **不做** cross-version 自动转换（RFD）。
12. **Schema codegen 名变更（无 wire 变）：** 如 `UpdateSessionNotification`、`LoginAuthRequest` 等。

### Agent 迁移清单（压缩）

见 migration “Migration checklist: Agents” 16 步：改 initialize → baseline methods → auth 改名 → prompt 立即 `{}` + state_update → 必填 messageId → 只发 tool_call_update → terminal display → 新 diff → 新 permission → plan_update → modes→config → resume+replayFrom → 删 fs/terminal 调用 → MCP type → slash input type → open enums + batch。

### Client 迁移清单（压缩）

改 initialize → 信 session baseline → UI 跟 state_update → messageId upsert → tool 首见创建 → terminal 显示 → 新 diff/permission/plan → resume 替代 load → 用 MCP 暴露本地能力 → cancel 等 idle cancelled → 容忍未知 update 类型。

## 未决 / 风险（明确标注推断）

| 项 | 类型 | 说明 |
| --- | --- | --- |
| v2 稳定时间表 | 未在已读 docs 给出具体 GA 日期 | 仅 Draft + “will change”；2026-07-20 公告 |
| Unstable vs stable v2 baseline 边界 | 文档有分层但需跟 schema | `schema.unstable.json` 特性列表本次未逐条核对 schema 文件 |
| Message queueing / steering | RFD 明确 **不是** prompt RFD 范围 | idle 不等于 queueing 已标准化 |
| Multi-client 同 session | 设计动机已写；完整一致性/冲突规则未在本次精读中展开 | |
| Remote transport vs v2 core | **文档张力：** migration 说 remote RFD **不是** core v2 surface；transport RFD 正文有 v1/v2 durability 分段 | 实现应以 “core v2 不含标准 HTTP” 为准，remote 跟 RFD/WG |
| MCP-over-ACP、proxy-chains 等 | 仅索引存在 | 未读正文 |
| v1 与 v2 文档并行演进 | v1 仍在 stabilize 新能力（llms.txt 大量 “stabilized” 公告） | 写 wiki 时注意引用日期与版本 |
| `loadSession` 顶层 cap 与 sessionCapabilities 不统一 | v1 initialization 自承 future unify | v2 用 resume+replayFrom 解决 |
| 生产双栈成本 | RFD “huge support issues” 自承 | SDK 仍在补 dual-version 表达 |
| 推断：editor 删除 fs/terminal 后短线 UX 回退 | 推断 | 依赖各 client 是否认真提供 MCP filesystem/terminal servers |

## 来源清单

| # | URL | 状态 (2026-08-06) |
| --- | --- | --- |
| 1 | https://agentclientprotocol.com/llms.txt | OK |
| 2 | https://agentclientprotocol.com/get-started/introduction.md | OK |
| 3 | https://agentclientprotocol.com/get-started/architecture.md | OK |
| 4 | https://agentclientprotocol.com/protocol/v1/overview.md | OK |
| 5 | https://agentclientprotocol.com/protocol/v1/initialization.md | OK |
| 6 | https://agentclientprotocol.com/protocol/v1/prompt-turn.md | OK |
| 7 | https://agentclientprotocol.com/protocol/v1/session-setup.md | OK |
| 8 | https://agentclientprotocol.com/protocol/v1/tool-calls.md | OK |
| 9 | https://agentclientprotocol.com/protocol/v2/overview.md | OK |
| 10 | https://agentclientprotocol.com/protocol/v2/migration.md | OK |
| 11 | https://agentclientprotocol.com/protocol/v2/prompt-lifecycle.md | OK |
| 12 | https://agentclientprotocol.com/announcements/acp-v2-draft.md | OK |
| 13 | https://agentclientprotocol.com/rfds/v2/overview.md | OK |
| 14 | https://agentclientprotocol.com/rfds/v2/prompt.md | OK |
| 15 | https://agentclientprotocol.com/protocol/v1/transports.md | OK（补充） |
| 16 | https://agentclientprotocol.com/rfds/streamable-http-websocket-transport.md | OK（补充 transport RFD） |

**Schema 链接（文档提及，本次未抓取正文）：**

- https://agentclientprotocol.com 站点内 `/protocol/v1/schema`、`/protocol/v2/schema`
- 仓库 releases：`schema/v2/schema.json`、`schema/v2/schema.unstable.json`、`v2.0.0-alphaX`
- OpenAPI 索引：https://agentclientprotocol.com/api-reference/openapi.json（llms.txt）

**v2 RFD collection 标题（overview 列出，正文未全读）：**  
New Prompt Lifecycle；Enum Variant Extension；Required Session Methods；Session Resume Replay；Client Filesystem and Terminal Execution Surface；Terminal Output；Plan Variants；Tool Call Updates；Diff File States；Permission Requests；Message Updates and Chunks；Remote Transports（streamable-http-websocket）。
