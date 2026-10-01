---
title: LodyAI 组织 ACP 协议扩展调研报告
date: 2026-09-30
topic: Lody ACP extension
sources:
  - https://github.com/LodyAI
  - https://github.com/LodyAI/acp-extension-core
  - https://github.com/LodyAI/Lody
  - https://www.npmjs.com/package/@lodyai/acp-extension-core
---

# LodyAI 组织 ACP 协议扩展调研报告

> 调研日期：2026-09-30。调研对象：github.com/LodyAI 全部公开仓库。
> 本地仅保留 `acp-extension-core`（扩展协议的定义所在）；其余仓库的 `file:line` 引用请对照 GitHub 上的 LodyAI/Lody、LodyAI/acp-extension-{claude,codex,kimi,grok,pi,dsh} 等仓库。
> `acp-extension-core/` 内的引用可直接跳转。

## TL;DR

LodyAI 是产品 **Lody**（"Share coding agents with your team on phone and desktop"，⭐1151）背后的团队。组织里所谓 "ACP 协议扩展" 是一套**多适配器同步演进的协议家族**：

- **`acp-extension-core`** 是心脏：一个刻意保持 type-only 的纯合约库，定义了 Lody 在标准 ACP（Agent Client Protocol，Zed 提出的编辑器↔agent JSON-RPC 协议）之上叠加的私有语义——三层递进：标准消息原样用 → 标准消息加 `_meta.lody.*` 字段 → ACP 完全无对应物时才开 `_lody/...` 自定义 JSON-RPC 命名空间（7 个请求 + 4 个通知）。
- **6 个真实适配器**各自把一个 coding agent 接进 ACP：`claude`/`codex` 是 Zed 官方适配器的深度 fork（859/597 commits，最活跃）；`kimi` 是 MoonshotAI/kimi-code 整个 monorepo 的 fork；`grok` 是官方 Grok CLI 之上的纯 JS 双向代理；`pi` 对接 Pi CLI 的 RPC 模式；`dsh` 是 DeepSeek Harness 的 Cordis 进程内插件。
- **`devin`/`omp` 是空壳占位仓**（git ls-remote 无任何 ref，仅 9/29、9/30 建仓时的描述）。
- 主仓库 **Lody**（Electron 39 + React 19 桌面 + Capacitor 移动壳 + `npx lody` CLI daemon）以 git submodule + pnpm workspace 消费这套适配器，并为 5 个 "managed runtime" 维护带 sha256 校验的二进制分发清单，从 `api.lody.ai` 下载。Agent 全部跑在用户自己的机器上，云端（Convex + Loro Streams CRDT）只做同步与 Machine RPC 中继。
- 整个家族演进高度同步：2026-08-21/22 所有适配器同日 "adopt unified Lody ACP extensions" 切到 core，随后 9 月又同步三轮（sessionTitle → usage scopes → subagentEvents）。主要开发者 Leon Zhao (leeeon233)、Zixuan Chen，commit 尾标显示高度 AI 辅助开发（gpt-5.6 / claude-opus-5）。

---

## 1. 组织全景

| 仓库 | 角色 | 语言/规模 | 活跃度（截至 2026-09-30） |
|---|---|---|---|
| `Lody` | 主产品（桌面/移动/CLI） | TS，pnpm monorepo | v0.100.0，持续日更 |
| `acp-extension-core` | 全家族共享的 ACP 扩展**合约库** | TS，836 行，几乎零运行时 | 24 commits，08-20 公开，npm 0.1.9 |
| `acp-extension-claude` | Claude Code 适配器（fork 自 `agentclientprotocol/claude-agent-acp`） | TS，`acp-agent.ts` 单文件 11241 行 | 859 commits（含上游历史） |
| `acp-extension-codex` | Codex CLI 适配器（fork 自 `agentclientprotocol/codex-acp`） | TS，`CodexAcpServer` 3933 行 | 597 commits（含上游历史） |
| `acp-extension-kimi` | Kimi Code 适配器（fork 自 `MoonshotAI/kimi-code` 整仓） | TS monorepo，acp-server 6.7k src + 5.7k test | 1620 commits（约 1200 为上游），自有改动 08-12 起 |
| `acp-extension-grok` | xAI 官方 Grok CLI 的纯 JS 双向代理 | JS，2.1k src + 2.5k test | 26 commits，08-10 → 09-29 |
| `acp-extension-pi` | Earendil Works Pi CLI 的 RPC 适配器 | TS，3.0k src + 2.2k test | 8 commits（09-07 曾推倒重来做 RPC 版） |
| `acp-extension-dsh` | DeepSeek Harness 的 Cordis 插件 | TS，5.5k src | 32 commits，08-14 → 09-27 |
| `acp-extension-devin` | **空壳占位**（"devin acp for lody"） | — | 零 commit，09-29 建仓 |
| `acp-extension-omp` | **空壳占位**（"Oh my Pi adapter for Lody"） | — | 零 commit，09-30 建仓 |
| `.github` | 组织级配置（未 clone） | — | — |

## 2. acp-extension-core：协议扩展的设计核心

定位不是适配器框架，而是 **"Provider-neutral contracts for Lody capabilities that are not part of ACP"**（`acp-extension-core/README.md:1-3`）。连接管理、JSON-RPC、会话生命周期、权限请求全部留给官方 `@agentclientprotocol/sdk`（ACP TS SDK 迁到独立 org 后的新包名，core 仅 0.1.9 起以 *纯类型* 方式依赖 ^1.4.0，见 `package.json:26-31`）。

### 2.1 三层扩展策略（`README.md:28-43`）

1. **标准 ACP 能承载的一律用标准消息**。例：plan mode 完全复用标准 config 机制（`plan-mode.ts:1-21`，"no separate Plan RPC"）；elicitation、session/fork 同理。
2. **Lody 语义放标准消息的 `_meta.lody.<feature>`**。聚合类型 `LodySessionMeta`（`session.ts:161-176`）覆盖：`worktreeProject`（声明逻辑项目根，cwd 可能是 worktree）、`forkAtTurn`、`steer`、`goalControl`（goal 的 set/resume 必须"搭"在 prompt 元数据上，因为 ACP v1 只有客户端 prompt 能拥有运行中的工作）、`toolName`（canonical 工具身份，配合 `LODY_TOOL_NAMES`）、`activity`（compaction/retry）、`task`（后台/定时任务）、`goal`、`notice`、`titleSource`、`messagePhase` 等。
3. **ACP 完全没有对应物才开 `_lody/...` 命名空间**（`methods.ts:3-15`）：

| 类别 | 方法 | 语义 |
|---|---|---|
| 请求 | `_lody/session/steer` | 中途向进行中 turn 注入指令（inject-or-refuse，配 `steer_applied` 回执） |
| 请求 | `_lody/session/goal` | 长期目标控制（set/pause/resume/clear） |
| 请求 | `_lody/rate_limits/get` | 主动查询限流快照 |
| 请求 | `_lody/session/history/read` | 触发原生历史回读 |
| 请求 | `_lody/subagents/{list,cancel,output}` | 原生 subagent 任务管理三件套 |
| 通知 | `_lody/subagents/event` | subagent 执行事件流 |
| 通知 | `_lody/session/usage_update` | 用量记账推送（累计口径） |
| 通知 | `_lody/rate_limits/update`、`_lody/session/steer_applied` | 限流推送 / steer 生效回执 |

### 2.2 版本化能力协商

所有可选能力在 `InitializeRequest/Response` 的 `capabilities._meta.lody` 下以**整数 version** 广播（`capabilities.ts:11-15, 58-72`）：agent 侧 12 个能力键（subagentEvents、sessionTitle、usage、rateLimits、forkAtTurn、steering、tasks、subagents、goal、compaction、sessionHistory、worktreeProject），client 侧 2 个（subagentEvents、elicitation）。双边独立 opt-in，version 不匹配即拒绝（`subagent-events.ts:63-66`，测试明确 v2 被拒）。

### 2.3 仅有的 4 个运行时抽象

core 几乎是 type-only，理由是"要在 CSP 受限的浏览器渲染进程里跑"（`subagent-events.ts:84-86`）。运行时部分只有：

- `supportsLodySubagentEvents()` —— 能力探测；
- `SessionUsageAccumulator`（`usage.ts:80-134`）—— 按 operationId 单调合并的记账账本，快照 detached（structuredClone）、进程重启即新 scope；
- `LodySubagentEmitter`（`subagent-emitter.ts:9-94`）—— nativeId→不透明 runId 映射、迟到 output 丢弃、disconnect 全部置 `unknown`；
- 5 个手写 wire 校验守卫（`subagent-events.ts:67-130`）。

### 2.4 测试锁死的设计不变量

版本化只做加法、绝不重释 v1（elicitation fixture 用 `@ts-expect-error` 锁死 v2）；usage 记账单调幂等、"通知投递不是 exactly-once 账本"；subagent 快照"宁可 unknown 不可撒谎"（commit 原词 *truthful*）；畸形载荷在不可信边界上封闭校验。

### 2.5 演进时间线

npm 上 0.0.1 早至 **2026-01-17**（私有形态存在大半年）；git 公开史 2026-08-20 起（自更大的 Lody 私有 monorepo 拆出，残留 "maintain Kimi as a builtin runtime" commit）。关键版本：0.1.1 独立布尔 plan mode（09-08）→ 0.1.2 worktreeProject → 0.1.3/4 goal 双通道拆分 → 0.1.5 首个运行时类 usage 账本 → 0.1.6 elicitation answerNotes → 0.1.7 自动会话标题 → 0.1.8 重启安全 usageScopeId → **0.1.9（09-27）最大一次：subagent 事件合约 + emitter + 引入 ACP SDK 类型依赖**。

## 3. 六个真实适配器：四种架构拓扑

| | 底层 agent | 拓扑 | core 依赖 | ACP SDK |
|---|---|---|---|---|
| claude | `@anthropic-ai/claude-agent-sdk` 0.3.284（固定） | 官方 SDK 常驻进程，每 session 一个 query 流 | 0.1.9 | 自装 |
| codex | `@openai/codex` 0.159.2（npm 捆二进制） | spawn `codex app-server` 子进程，JSON-RPC | 0.1.9 | 自装 |
| kimi | Kimi Code CLI（fork 整个 monorepo） | **in-process**：acp-server 经内存 transport 直连 agent-core-v2 引擎 | 0.1.9 | ^1.3.0 |
| grok | `@xai-official/grok` 1.0.40 | **子进程双向代理**：spawn `grok agent stdio`，NDJSON 逐条翻译 | 0.1.9（唯一运行时依赖） | **无**（手写 JSON-RPC） |
| pi | `@earendil-works/pi-coding-agent` 0.87.0（pin） | **子进程 RPC**：`pi --mode rpc`，LF-JSON envelope | 0.1.9 | 1.3.0 |
| dsh | DeepSeek Harness 0.1.5-rc.2 | **in-process 插件**：Cordis plugin 寄生 Harness 进程 | 0.1.9 | 1.3.0 |

### 3.1 claude / codex：官方适配器的深度 fork

- upstream 分别是 `agentclientprotocol/claude-agent-acp`（Zed 血统，2025-08 起）和 `codex-acp`。fork 中转痕迹：2026-07 经 `loro-dev` 组织，08-20 前后迁入 LodyAI。
- **fork 策略成熟**：定期 merge upstream 保留 git 双亲（claude 09-29 刚合入 upstream 0.84.0，冲突以已导入 0.79 为基线，见 `docs/UPSTREAM_SYNC.md`）；非 Lody 客户端（如 Zed）拿到的字段与上游**逐字节一致**，用录制回放快照回归（`src/tests/acp-scenarios/origin-main/zed`）。
- 除 `_lody/*` 外还实现 JetBrains AIR 扩展（`_meta.jetbrains.air.*`：diffPatch、asyncTasks、nativeSubagentSessions 等），继承自上游。
- 发布：claude 走 release-please + OIDC trusted publishing（公网 npm 停在 0.54.3/2026-07-01，之后转内部分发）；codex 手动 version-bump → 发 npm → 联动 dispatch 私有 `LodyAI/registry` 的 update-versions workflow，另用 bun 打六平台单文件二进制。

### 3.2 kimi：fork 整仓，自研面其实很薄

GitHub fork 元数据确认为 `MoonshotAI/kimi-code`（7740 ⭐）的 fork。上游**官方就原生带 ACP server**（`packages/acp-server`，2026-06 上游实现）；LodyAI 的工作（08-12 起约 23 个自有 commit）集中在把该 ACP server 接到 acp-extension-core 契约上 + 少量深入引擎的改动（fork-at-turn 的 `forkTurnSlice.ts`、托管 OAuth）。当前基于上游 Kimi 2.0.2，持续合并上游。

### 3.3 grok：契约工程化的典范

根目录 `runtime-manifest.json` 是"**私有 wire contract 钉子**"：`officialRuntime` 块钉死适配的官方 Grok 版本（1.0.40，最低 1.0.34），`privateWireContract` 块枚举适配器依赖的每一个 Grok 私有方法名（`x.ai/yolo_mode_changed`、`x.ai/session/fork`、`x.ai/billing` 等），代码里只以 `contract.<key>` 引用——升级官方 runtime 时改 manifest + 翻译逻辑即可，且"依赖了哪些非标准方法"集中可审查。注意与主仓 `Lody/apps/cli/src/agent/grok-runtime-manifest.json`（六平台二进制 sha256 下载清单）是两回事。测试 2517 行 / 80 用例纯函数协议测试；短板是无 TS、认证后的真实执行未验证。

### 3.4 pi：最年轻的适配器

spawn Pi 子进程跑 `--mode rpc`；适配器额外打包一个 extension 注入 Pi 提供 questionnaire/todo/subagent/MCP 四个 packaged tools。`native/` 是仅 Windows 的 46 行 C++ Job Object addon——spawn Pi 前把当前进程加进 `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`，适配器一退出 OS 自动杀整棵进程树（Unix 靠 detached + 协作清理，属接受的 V1 限制）。8 个 commit，09-12 曾推倒 SDK 方案重做 RPC 版。

### 3.5 dsh = DeepSeek Harness

Cordis 插件三件套（`apply/inject/name`）寄生在 Harness 进程内。`presets/` 四个**中文描述**的 agent 预设（standard / ptc / minimal / cordis），PTC 模式 = 用 TypeScript 程序编排工具调用。usage 按 DeepSeek 官方价目表估算 USD（README 写死 2026-09-13 核对的分时价格）。风险点：上游是 0.1.5-rc.2。

## 4. 主产品 Lody 如何消费这套体系

- **架构**：pnpm monorepo = `apps/cli`（npm 包 `lody`，daemon，**agent 真正运行的地方**）+ `apps/electron`（Electron 39 + React 19）+ `packages/components`（桌面/Web/移动共享 UI，移动端是 Capacitor 壳，App Store/Google Play 已上架但闭源）。协同栈是 Loro 全家桶（CRDT）+ Convex（组织/账号）+ better-auth。
- **7 个适配器以 git submodule 挂进 `packages/`**（`.gitmodules:1-21`），其中 claude/codex/grok/dsh 四个被构建成 CLI 内嵌入口（`apps/cli/src/*-acp-entry.ts`），kimi/pi 排除在根依赖图外、只消费其单独打包的 managed-runtime 制品。
- **launch 三分法**（`apps/cli/src/agent/setting.ts`，类型 `builtin | registry | custom`）：
  - *builtin*：8 种（codex/claude/grok/kimi/pi 五个 managed runtime + deepseek/dimcode/bub）。managed runtime 从 `https://api.lody.ai/api/runtimes/...` 下载带 sha256 校验、断点续传的 tar.zst（`managed-agent-runtime.ts:675`），版本漂移检查错误信息指向 operator 的 `pnpm mirror:agent-runtimes`；
  - *registry*：构建期镜像 **Zed 官方 ACP Registry**（`cdn.agentclientprotocol.com/registry/v1`），生成 `REGISTRY_ACP_AGENTS`——排除 claude/codex/grok/pi（自家维护），本地覆盖 11 个条目（kimi、opencode、goose、cursor-agent 等），支持 npx/uvx/binary 下载（Devin 走 binary，有 `specs/devin-acp-runtime.md`，呼应空壳 devin 仓）；
  - *custom*：用户一行 launch command。
- **客户端侧扩展消费**：`initialize` 时广播 `clientCapabilities._meta.lody = { elicitation: {version:1, answerNotes:true}, subagentEvents: {version:1} }`（`agent-client.ts:1950-1956`）；34 个文件引用 acp-extension-core；另留 `_acp_ext:*`、`_claude/taskLifecycle` 等 legacy 兼容层。
- **"Share with team"**：agent 全跑在用户机器的 daemon 上；云端只做 Convex 权限/通知 + Loro Streams CRDT 同步 + Machine RPC 中继（`session/dispatch-turn`、`session/steer`、`machine/acp-authenticate` 等，秘密走 ECDH-P256-AES-256-GCM 信封）；机器可共享给团队、活会话可 handoff（非只读快照）、另有静态分享链接。daemon 还内置名为 `lody` 的 MCP server 让 agent 互相编排（委托链深度上限 32）。

## 5. 值得借鉴的设计决策

1. **扩展协议的三层克制**：能上标准就上标准、meta 字段次之、自定义 RPC 最后——并且用一份集中合约库 + 整数版本协商把"私有扩展"做成可审计、可增量演进的东西。
2. **type-only 合约包**：让同一份契约同时跑在 Node 适配器和浏览器渲染进程（CSP 受限）里。
3. **fail-closed 一以贯之**：权限决策集不完整即 cancel；steer 无确证即拒绝并保持 unknown；subagent 快照宁可 unknown 不可撒谎；turn 结束无 result 显式标 failed（"never invented success"）。
4. **fork 与上游共存**：定期 merge 保留双亲 + "非自家客户端逐字节兼容上游"的录制回放回归 + wire contract manifest 集中声明私有依赖。
5. **版本纪律**：合约只做加法、v1 永不重释、未来版本必须显式协商，测试用 `@ts-expect-error` 锁死。
6. **多仓同步演进**：同一批人在 8+ 仓库同步落同一个契约变更（08-21 统一切 core、09-24/26/27 三轮同步迭代），靠 core 锁版本（全部钉 0.1.9）保证一致。

## 6. 风险与不确定

- claude/codex 公网 npm 停更于 2026-07（转 Lody 内部分发），外部使用者拿不到最新版。
- grok 适配器"认证后的真实执行未验证"（README 自述）；dsh 依赖 rc 版上游。
- devin/omp 空壳，落地时间未知；`.github` 未调研（组织配置）。
- 移动端/Web/云端闭源，本报告对"共享"机制的理解来自开源桌面/CLI 侧代码与 site-docs。

## 7. 来源

- 本地 clone：`~/Workspace/oss/lodyai/{Lody,acp-extension-*}`（2026-09-30 clone，HEAD 见各仓 git log）
- GitHub API：orgs/LodyAI/repos 元数据（fork 父仓、创建/推送时间、描述）
- npm registry：`acp-extension-core`、`acp-extension-claude`、`acp-extension-codex` 发布史
- 关键文件入口：`acp-extension-core/README.md`（扩展策略总纲）、`acp-extension-core/src/methods.ts`（`_lody/*` 清单）、`Lody/apps/cli/src/agent/README.md`（主仓集成层索引）、`Lody/apps/cli/src/agent/managed-agent-runtime.ts`（runtime 分发）、`acp-extension-grok/runtime-manifest.json`（wire contract）
