---
title: Lody 在 ACP 之上的协议扩展
description: 分析 LodyAI 如何在标准 Agent Client Protocol 之上扩展产品侧语义，以及驱动扩展的具体场景与设计取舍
type: synthesis
category: ai
created: 2026-10-02
updated: 2026-10-02
timestamp: 2026-10-02
tags:
  - acp
  - code-agent
  - protocol-design
source_refs:
  - raw/sources/2026-09-30-lody-acp-extension-research.md
  - https://github.com/LodyAI
  - https://github.com/LodyAI/acp-extension-core
  - https://github.com/LodyAI/Lody
resource:
  - raw/sources/2026-09-30-lody-acp-extension-research.md
  - https://github.com/LodyAI
  - https://github.com/LodyAI/acp-extension-core
  - https://github.com/LodyAI/Lody
---

# Lody 在 ACP 之上的协议扩展

## 问题

相较标准 Agent Client Protocol（ACP，由 Zed 提出的编辑器与 coding agent 间 JSON-RPC 通信标准），Lody 到底扩展了什么？在标准 ACP 消息集合无法覆盖的具体场景中，Lody 为何做出这些扩展以及背后的设计取舍是什么？

## 简答

Lody 将所有扩展集中在 `acp-extension-core` 纯类型合约库中，保持标准协议骨架（会话连接、权限申请、工具调用、模式切换）不变，仅在产品侧语义上进行扩展：通过三层扩展策略（标准消息优先、`_meta.lody.*` 搭便车、`_lody/...` 命名空间自定义 RPC）补齐中途插话、长期目标、子 agent 可观测、用量记账与限流、移动端提问等标准 ACP 尚未覆盖的产品功能。

## 来源事实

以下事实来自 `raw/sources/2026-09-30-lody-acp-extension-research.md` 以及只读仓库 `LodyAI/acp-extension-core`：

### 1. 合约库定位与三层扩展策略

扩展全部集中在 `acp-extension-core`（一个 836 行 TypeScript 的纯类型合约库，仅包含 4 个极轻量运行时辅助函数，旨在受内容安全策略 CSP 限制的浏览器渲染进程中运行）。扩展策略分为严格的三层（`acp-extension-core/README.md:28-43`）：

1. **第一层：标准 ACP 能承载的一律使用标准消息**。例如 plan mode 完全复用标准 config 机制（`README.md:259-264`，"no separate Plan RPC"），通过标准 `session/set_config_option` 设置布尔配置项；`elicitation/create`、`session/fork` 同理。
2. **第二层：`_meta.lody.*` 元数据搭便车**。在标准消息的元数据字段 `_meta.lody` 下附加产品属性。聚合类型 `LodySessionMeta`（`src/session.ts:161-176`）覆盖 `worktreeProject`、`forkAtTurn`、`steer`、`goalControl`、`toolName`、`activity`、`task`、`goal`、`notice`、`titleSource`、`messagePhase`、`usageScopeId` 以及提问增强（`noteFor`）等。
3. **第三层：`_lody/...` 自定义 JSON-RPC 命名空间**。仅限标准 ACP 完全没有对应物的交互动作（`src/methods.ts:3-15`），包含 7 个请求方法与 4 个通知方法：
   - 请求方法：`_lody/session/steer`、`_lody/session/goal`、`_lody/session/history/read`、`_lody/rate_limits/get`、`_lody/subagents/list`、`_lody/subagents/cancel`、`_lody/subagents/output`。
   - 通知方法：`_lody/subagents/event`、`_lody/session/usage_update`、`_lody/rate_limits/update`、`_lody/session/steer_applied`。

### 2. 双边版本化能力协商

在客户端与 agent 建立连接初始化（`InitializeRequest` / `InitializeResponse`）时，所有可选扩展能力在 `capabilities._meta.lody` 下使用整数版本号声明（`src/capabilities.ts:11-15, 58-72`）。Agent 侧提供 12 个能力标记（如 `subagentEvents`、`steering`、`goal`、`usage`、`rateLimits` 等），Client 侧提供 2 个能力标记（`subagentEvents`、`elicitation`）。双方独立 opt-in，主版本不匹配即拒绝（如测试用例通过 `@ts-expect-error` 锁死拒绝未协商的 v2 版本）。

### 3. 仅有的四个运行时抽象

为了保证在无 Node.js 环境的客户端界面与受限渲染进程中运行，合约库仅保留四个运行时逻辑：
- `supportsLodySubagentEvents()`：双边能力探测与版本匹配检查。
- `SessionUsageAccumulator`（`src/usage.ts:80-134`）：按操作标识单调合并的用量记账账本，生成的快照独立脱钩（使用 `structuredClone`），进程重启即切换新的 `usageScopeId`。
- `LodySubagentEmitter`（`src/subagent-emitter.ts:9-94`）：将底层原生 agent 标识映射为不透明的单次运行 `runId`，丢弃终止后的迟到输出，并将断开连接的运行标记为 `unknown` 与 `outputIncomplete: true`。
- 5 个针对不可信边界的手写格式校验函数（`src/subagent-events.ts:67-130`）。

### 4. 驱动扩展的五个具体场景案例

#### 案例 1：中途插话（Steering）
- **场景**：Agent 正在根据之前的提示词长程执行命令或编写代码，用户在终端或手机上发现其方向走偏，需要实时插入调整指令，而无需强行中断整个会话。
- **标准 ACP 空洞**：在 ACP v1 中，一个 `session/prompt` 严格对应一个 turn，且该请求是挂起阻塞的；在当前 turn 完成之前，协议上客户端没有第二条合法消息可向该会话注入输入，缺少向进行中 turn 注入新指令的调用约定。
- **Lody 的补法**：引入请求方法 `_lody/session/steer`（`src/session.ts:93-101`），入参携带 `steerId` 和注入内容。Agent 明确返回 `outcome: "injected" | "failed"`（遵循 inject-or-refuse 原则，不存在默默丢弃状态）。随后当注入内容实际合入上下文并被模型消费时，Agent 异步发出 `_lody/session/steer_applied` 通知作为生效回执。
- **设计取舍**：区分“指令已送达并被 Agent 接纳（injected）”与“指令已真正进入模型推理上下文（steer_applied）”。两阶段设计避免了客户端向用户虚假承诺中途调整已立即生效。

#### 案例 2：长期目标控制（Goal）
- **场景**：用户设定一个长程目标（如“排查登录重定向异常并补全测试”），可能跨越数十个交互轮次与多次自主重试；用户可能需要随时暂停、查看进度或清空目标。
- **标准 ACP 空洞**：ACP v1 的核心约束是客户端只能通过自身发起的 prompt 来拥有和驱动正在运行的工作（`README.md:206-231` 原话："ACP v1 gives a client exactly one way to own running work — its own prompt"）。如果通过独立的 RPC 请求触发目标启动，Agent 将不得不自主启动一段“没有任何客户端 prompt 关联的无主 turn”，这破坏了 ACP v1 的会话归属模型；但若完全依赖 prompt，当活跃目标驱动 Agent 保持忙碌时，客户端又无法发出新的 prompt 来执行暂停。
- **Lody 的补法**：被所有权模型拆分为方向相反的两条传输通道：
  1. **启动与恢复（`set` / `resume`）**：启动新工作的动作必须附带在 `session/prompt` 的 `_meta.lody.goalControl` 元数据中发出（ACP v1 中客户端拥有运行中工作的唯一方式是自己的 prompt）。该 prompt 在底层执行动作后，持续保持打开状态以承载该目标所驱动的各轮 turn，确保每一轮 turn 均有对应的客户端 prompt 归属。
  2. **暂停与清空（`pause` / `clear`）**：主要靠独立的请求方法 `_lody/session/goal`（`src/session.ts:64-70`）发出。因为活跃目标会让 prompt 保持打开，客户端无法再发 prompt，独立请求是唯一可达通道，且该请求绝不启动新 turn（must not start a turn）；同时随 prompt 元数据发送此类 status-only 动作也是允许的（例如在会话未运行时控制目标）。
- **设计取舍**：根据操作是否“启动新工作”与会话繁忙状态分流，既维持了 ACP v1 prompt-turn 的所有权约定，又保证了暂停与清空在 prompt 进行中的可达性。

#### 案例 3：子 Agent 可观测性（Subagent Observability）
- **场景**：主 Agent 在执行复杂任务时启动了子 Agent（Subagent）并行检索或编写子模块，客户端需要向用户呈现子 Agent 的实时思考、执行步骤和进度。
- **标准 ACP 空洞**：标准 ACP 仅将子 Agent 视作普通的 `tool_call`。在工具调用返回之前，客户端与用户只能看到工具处于等待状态的加载图标，内部完全不透明。
- **Lody 的补法**：双边协商 `subagentEvents` 能力后，通过通知方法 `_lody/subagents/event` 实时推送事件流（文本、思考、工具调用、计划更新）；配合三个管理方法 `_lody/subagents/{list,cancel,output}` 实现列表查看、手动取消和日志回读。
- **设计取舍**：采用显式的弱保证设计（`README.md:15-17` 原话："no sequence numbers, replay guarantees, or cross-reconnect deduplication"）。由于真实网络可能经由移动端或 CRDT 协同中继，无法保证严格有序重放。合约明确规定观测数据丢失时状态直接置为 `unknown` 且标记 `outputIncomplete: true`，宁可暴露数据不完整，也不伪造执行结果，同时明确该事件丢失不代表 Agent 实际执行失败。

#### 案例 4：用量记账与限流（Usage & Rate Limits）
- **场景**：团队共享和多端协同场景下，需要对各模型 Token 消耗、估算费用进行累计记账，并展示各个模型窗口的限流配额状态。
- **标准 ACP 空洞**：标准 ACP 的 `usage_update` 通知仅反映当前会话对模型上下文窗口的占用比例（用于提示上下文裁剪），不包含面向财务统计的绝对 Token 统计、费用核算和配额窗口。
- **Lody 的补法**：定义通知方法 `_lody/session/usage_update`，区分单次操作增量 `delta` 与按模型累计值 `modelUsage`；提供 `_lody/rate_limits/get` 与 `_lody/rate_limits/update` 处理并发配额窗口。
- **设计取舍**：
  1. 坚持未提供费用不等于免费（`README.md:192` 原话："Missing cost means unknown, not free"），缺少数据时显式保持未决状态。
  2. 针对 Agent 进程重启后内存累计值丢失的问题，引入 `_meta.lody.usageScopeId`（`README.md:186-190`）。每次进程拉起均生成独立唯一的 scope 标识，客户端分别累计各个 scope 的用量再求和，避免新进程从零开始上报冲掉历史账本。

#### 案例 5：移动端提问增强（Elicitation Enhancement）
- **场景**：Agent 遇到歧义向用户发起单选提问（如选择重构方案），用户在移动端操作，既希望点击选择预设方案，又需要随手附带一句补充说明（如“注意保持对外公开接口稳定”），或者当用户长时间离线时自动超时避免阻断无人值守任务。
- **标准 ACP 空洞**：标准 ACP 的 `elicitation/create` 基于标准 JSON Schema 询问表单。在标准交互中，自定义输入通常是作为“完全替代既有预设选项”的互斥操作（customAnswerFor），无法表达“选中该选项并附带补充说明”的组合输入。
- **Lody 的补法**：保持对标准 `elicitation/create` 调用的完全复用（`README.md:115`："Both use standard ACP `elicitation/create`; no new RPC is needed"）。在 Schema 属性定义中附加 `_meta.lody.elicitation: { noteFor: "approach" }`，让补充说明字段与主选项解耦关联；同时在元数据中提供 `autoResolveAfterSeconds` 倒计时机制，超时自动裁决以防止移动端用户未及时查看导致任务死锁。
- **设计取舍**：完全不增加新 RPC，使用标准 JSON Schema 扩展字段；老客户端由于不认识该元数据，仍可将主选项与备注当作普通表单字段正常提交，保持向前兼容。

### 5. 反例对照：标准能力不扩展

在设计扩展时，Lody 保持了严格的克制界限：
- **规划模式（Plan Mode）完全不扩展**：虽然也是交互模式切换，但并未设立专门的 Plan RPC，而是将其作为名为 `plan_mode` 的布尔值配置项（`README.md:259-264`），复用标准 ACP 的 `session/set_config_option` 进行通知和切换。
- **历史分叉（Session Fork）不新设 RPC**：完全复用标准的 `session/fork` 请求，仅在元数据中追加 `_meta.lody.forkAtTurn` 声明从特定的交互轮次开始切出新分支。

## 综合结论

### 1. 讨论观点与判断

在 2026-09-30 的技术讨论中，形成并确认了以下判断：
- **讨论观点 1**：Lody 扩展的核心本质是补充**产品侧语义**（中途插话、长期目标、多端协同下的子任务监控、用量与限流、移动端交互体验），而标准 ACP 的核心骨架（会话连接、权限管控、工具执行流、配置项机制）被完全保留和复用。
- **讨论观点 2**：判断一个能力是否应当开辟新的 JSON-RPC 方法，唯一判据是“标准 ACP 消息是否完全缺乏该物理动作的表达能力”。凡是状态切换、参数变更或附带信息，一律通过标准机制（配置项或 `_meta`）承载。

### 2. 作者解释：为何 Lody 的扩展实践值得关注

从协议工程与 Agent 系统设计的角度，本总结提炼出以下四项机制特征：

- **UI 只依赖统一接口定义，不按厂商写特化分支**：适配器把各家 agent 的非标准行为翻译进 `acp-extension-core` 统一接口定义，UI 消费端只依赖这份类型定义，不针对具体模型厂商做分支处理。
- **遵循协议物理约束（所有权驱动通道分离）**：在 Goal 机制中表现尤为典型——协议架构师没有凭空发明统一的“目标管理 RPC”，而是顺应了 ACP v1 中“只有客户端 prompt 才能拥有执行 turn”的硬性约束，将控制动作精细拆解为元数据通道与独立带外通道。
- **面向不可靠链路的容错约定**：在移动端中继与分布式协同场景中，不假定网络传输是顺序且无损的。在子 Agent 事件流中主动放弃序列号和重放保障，通过明确定义 `unknown` 状态防止界面渲染虚假事实。
- **非破坏性渐进演进**：通过整数版本号在 `initialize` 阶段进行严格能力握手，所有新增字段只做加法且永不重释旧语义，保证了适配器在接入标准客户端（如 Zed）时仍可逐字节还原标准行为。

## 对个人/项目的启发

1. **协议扩展的层级纪律**：在已有通用协议（如 LSP、MCP、ACP）上构建垂直产品时，应严格划分“原生承载”、“元数据增强（搭便车）”与“独立命令空间”。优先利用已有生命周期，避免过早发明自定义 RPC。
2. **多端协同必须考虑无主 turn 约束**：设计 Agent 与客户端之间的控制调用约定，必须明确谁对长任务具有归属权。在任务控制不可达时，需要评估带外 RPC 与带内提示词流的协同方式。
3. **真实网络下的状态坦诚**：分布式或弱网环境下，不要在协议层做出难以兑现的绝对有序承诺。将“未知 / 缺失（unknown / incomplete）”作为一等状态显式建模，优于强行保证一致性导致的界面假死或误判。

## 未决问题

- **ACP 官方规范演进的吸收不确定性**：ACP v2 草案已经开始针对会话状态解耦、排队与中途插话（steering）进行铺路，`_lody/*` 命名空间下的部分私有扩展将来是否会被 ACP 官方标准吸收或产生命名冲突，目前尚未确定。
- **占位适配器的落地节奏**：LodyAI 组织内的 `devin` 与 `omp` 适配器仓库目前仍为纯空壳状态，其实际接入协议的形态尚未落地。
- **闭源协同端的实现细节**：Lody 的移动端、Web 端与云端（Convex + Loro CRDT）属于闭源实现，当前对团队共享与权限中继机制的理解主要来自开源 CLI daemon 和桌面端实现。
- **部分适配器分发渠道停更**：`acp-extension-claude` 与 `acp-extension-codex` 在公网 npm 上的发布停留在 2026-07（已转为 Lody 内部分发），外部开发者难以直接获取经过实战验证的最新适配器发布包。

## 相关页面

- [[wiki/topics/ai/agent-client-protocol|Agent Client Protocol]]
- [[wiki/topics/ai/mcp|MCP]]
- [[wiki/syntheses/ai/agent-harness-evolution-paradigm|Agent Harness 演进范式]]

## 来源指针

- 仓库内素材：[[raw/sources/2026-09-30-lody-acp-extension-research.md]]
- [LodyAI 组织主页](https://github.com/LodyAI)
- [Lody 主产品仓库](https://github.com/LodyAI/Lody)
- [acp-extension-core 扩展合约仓库](https://github.com/LodyAI/acp-extension-core)
  - `README.md:28-43`（三层扩展策略）
  - `README.md:115-141`（提问增强与 noteFor）
  - `README.md:186-202`（用量记账与 scopeId）
  - `README.md:206-231`（Goal 目标控制双通道）
  - `README.md:259-264`（Plan mode 配置项）
  - `src/methods.ts:3-15`（自定义方法清单）
  - `src/session.ts:64-106`（Goal 与 Steer 接口定义）
  - `src/session.ts:161-176`（LodySessionMeta 元数据聚合）
  - `src/capabilities.ts:11-15, 58-72`（版本化能力协商）
