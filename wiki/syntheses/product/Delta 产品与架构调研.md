---
title: Delta 产品与架构调研
description: Zed 团队做的多人在场 agent 工作台：thread 把对话与工作副本绑成一个对象，底层自建 DeltaDB 用连续的 delta 取代 commit 快照；本页整理它的对象模型、数据流、扩展面与信任边界。
type: synthesis
category: product
created: 2026-09-17
updated: 2026-09-17
timestamp: 2026-09-17
tags:
  - code-agent
  - collaboration
  - version-control
  - trust-boundary
  - zed
source_refs:
  - raw/sources/2026-09-17-delta-dev.md
  - https://delta.dev/
  - https://delta.dev/docs/concepts/core-concepts
  - https://delta.dev/docs/concepts/delta-and-git
  - https://delta.dev/docs/privacy-and-security/agentic-safety
  - https://delta.dev/roadmap
  - https://delta.dev/pricing
resource:
  - raw/sources/2026-09-17-delta-dev.md
  - https://delta.dev/
  - https://delta.dev/docs/concepts/core-concepts
  - https://delta.dev/docs/concepts/delta-and-git
  - https://delta.dev/docs/privacy-and-security/agentic-safety
  - https://delta.dev/roadmap
  - https://delta.dev/pricing
---

# Delta 产品与架构调研

## 问题

Zed 团队为什么要再做一个 coding agent 产品？它和已经能改代码的 CLI agent 差在哪？它的对象模型、数据流、扩展面和信任边界分别是什么，代价是什么？

本页基于 2026-09-17 抓取的官方站点与 26 个文档页，以及一次对 `zed-industries` 公开仓库的核查。产品处于公开 beta、版本迭代极快（0.1.1 → 0.16.0 只用了三周多），任何具体行为都可能随后变化。

## 简答

Delta 的赌注不在模型能力，而在**工作单元的定义**。它把“与 agent 的对话”和“被 agent 改动的文件副本”绑成同一个对象（thread），于是回退对话能连带回退文件，评论能锚定在改动上，同事能实时看到同一份对话加文件。为了让这件事成立，它在 git 之外自建了 DeltaDB：不记录 commit 快照，而是把每一次改动、每一条消息、每一条评论都记成有身份的 delta，由各客户端各持一份副本并保持同步。

它换来的能力很具体：审阅与协作是原生的，而不是事后套一层 PR；代价同样具体：**目前没有权限系统、没有沙箱**，仓库内容会被自动执行，代码与历史全程进 Cloudflare，启动需要联网登录。

## 来源事实

### 一句话定位（官方原文）

- Delta app：“a multiplayer environment for coding with agents. The unit of work is a thread: the conversation with an agent and the checkout of the repository it works in, kept together as one shareable artifact.”
- DeltaDB：“Where Git captures a snapshot at each commit, DeltaDB records work as a stream of fine-grained deltas. Each delta has a stable identity, so a reference anchors to a change rather than a line number and survives as the code moves.”

### 对象模型

| 对象 | 定义 | 关键约束 |
| --- | --- | --- |
| thread | 与 agent 的对话，可独立存在，也可挂一到多个 project | 持久、可并行隔离、对话与文件一起回退、可共享 |
| project | 你打开的文件夹 | 必须是 Git 仓库的顶层目录；导入 Git 跟踪的文件（含已被 ignore 但被跟踪的）与未被 ignore 的未跟踪文件 |
| Delta worktree | thread 在某个 project 上的工作副本，历史记在 DeltaDB | 一个 thread 每个 project 一份；**不是** git worktree |
| checkout | worktree 在磁盘上的真实文件夹 | 每个参与者在各自机器上一份；终端与文件系统工具在它上面工作 |

默认配置被命名为 Isolated Workspace：agent 不在你的 project 目录里动手，改动要先带回来。

### DeltaDB 与 delta

- delta 记录“谁在什么位置改了共享状态的哪一部分”，类型包括文件编辑、文件树变化、消息、评论。它在工作发生的过程中**连续产生**，不需要 stage 或 commit。
- 每个连接的客户端持有一份数据库副本，Delta 保持副本同步；一份 worktree 有“DeltaDB 里的共享表示”和“磁盘上的 checkout”两种表示，两边保持同步。
- 与 git 的关系是**引导同步**（“Delta currently uses git as a way to bootstrap our syncing”），当前只支持配了 `origin` 的仓库。commits 仍留在 git，Delta 负责在机器之间搬运，不必绕道 origin。
- 每个托管 checkout 有**自己的 git 仓库**，agent 的 commit 落在那里；要回到你的仓库必须 push 到 `local` 或 `origin` 这类 remote。

### 执行位置的规则

- 每个参与者在自己的机器上有自己的 checkout，**turn 在发送者所在的环境里跑**，不在 thread owner 的机器上。
- 浏览器 turn 用 Delta 托管的模型，**没有 checkout、没有 shell**；要用本机的工具、凭据、进程就得在桌面端跑。
- 模型接法三种：自带 API key（Anthropic / OpenAI / OpenRouter / OpenCode Zen / OpenCode Go）、已有订阅（ChatGPT / GitHub Copilot / Grok）、随 Zed 计划的 hosted models。thread 可中途换模型。
- hosted model 的用量记在**发送者**账上，不记在 thread owner 头上。

### 协作与审阅

- 共享权限三档（受邀者 / 组织内 / 有链接者），默认 Private；链接共享被官方标注为敏感。
- 草稿是共享且可见的，本身就能当聊天用；一旦有人发送，会把末尾所有作者草稿一起提交，agent 一个 turn 回应全部。
- Review thread 是独立对话，包含 agent 生成的 change guide（按最能解释改动的顺序走查），产出 Approve / Request Changes 的 verdict 并回写父 thread；review agent 在分叉的 worktree 里工作，改动要靠 `Pull Changes` 拉回。
- `Land Changes` 会在专门的 subthread 里跑你项目自己的 landing workflow（由 skill 定义检查、合并策略与发布步骤），Delta 不预设 Git 流程。

### 扩展面

- `.agents/prepare`（或 `.delta/prepare`）：每次新建/重建托管 checkout 时执行的可执行脚本，用来装依赖、设缓存、链 hook。官方要求它快且可重复。
- `.agents/linked`：把 `.env` 之类本机文件在各 checkout 之间做硬链接共享。
- `.agents/skills/`、`~/.agents/skills/`：技能目录，`<name>/SKILL.md` + YAML frontmatter（`name`、`description`、可选 `user-invocable`、`disable-model-invocation`）；同名时项目技能优先。
- `AGENTS.md`、`profiles/*.toml`（subagent 的模型、thinking effort、`prompt`/`system_prompt`、`worktree = isolated | shared`）、`settings.json`、`~/.config/delta/.env`。
- Subagent 预算：每父 thread 4 个并发、整个进程 8 个；Worker/Reviewer 默认隔离副本、成功自动合并，Scout 直接用父 thread 的 checkout。

这套约定与 Zed 生态其它工具一致——本项目自己的 `.agents/skills/` 就是同一套布局，写好的技能不需要改就能被 Delta 读。

## 系统架构图

```mermaid
graph TB
  subgraph Machine["开发者机器（桌面端）"]
    App["Delta 桌面应用"]
    CO["checkout（真实文件夹）"]
    Agent["agent 进程<br/>在发送者的机器上运行"]
    MyRepo["你自己的 git 仓库"]
    Prepare[".agents/prepare 自动执行"]
  end

  subgraph Browser["浏览器（Delta Web）"]
    Web["Replicated worktree<br/>无 checkout、无 shell"]
  end

  subgraph Cloud["Zed Cloud（Cloudflare）"]
    Sync["同步与账号服务"]
    DO[("Durable Objects + SQLite<br/>thread / worktree deltas")]
    R2[("R2<br/>文件内容 / commit / checkpoints")]
    KV[("KV + D1<br/>thread / 仓库 / 协作者元数据")]
  end

  subgraph Providers["模型供应商"]
    Hosted["Zed hosted models"]
    BYO["自接 provider<br/>Anthropic / OpenAI / OpenRouter 等"]
  end

  App <--> Sync
  Web <--> Sync
  Sync --- DO
  Sync --- R2
  Sync --- KV
  Agent --> CO
  CO --> MyRepo
  Agent -.->|"直接读写共享表示"| Sync
  Prepare --> CO
  App --> Hosted
  App --> BYO
```

## 核心数据流

```mermaid
sequenceDiagram
  participant U as 发送者（桌面端）
  participant D as DeltaDB（本地副本 + Cloud）
  participant C as 协作者
  participant A as agent（发送者机器上）
  participant G as git remote（local / origin）

  C->>D: 起草草稿（实时可见，可当聊天）
  U->>D: 发送消息（末尾所有作者草稿一起提交）
  U->>A: 在发送者环境里启动一个 turn
  A->>D: 读 worktree 的共享文件表示
  A->>A: 编辑 / 跑命令（终端命令在 checkout 里）
  A->>D: 每次改动记录为 delta
  D->>C: 同步 delta（对话、评论、文件改动）
  C->>D: 行级评论 / 请求修改
  D->>A: 送回下一轮指令
  U->>G: Land（push 到 local，或推到 origin 走 PR）
  Note over U,G: 托管 checkout 有自己的 git 仓库<br/>agent 的 commit 不会自己出现在你的仓库里
```

## 扩展面与信任边界

```mermaid
flowchart LR
  subgraph Repo["仓库内容（不可信输入）"]
    P1[".agents/prepare"]
    P2[".envrc"]
    P3["AGENTS.md / .agents/skills/"]
  end

  subgraph Auto["Delta 当前的自动行为"]
    A1["挂载托管 checkout 时执行"]
    A2["经 direnv 加载，未批准也代为授权"]
    A3["直接变成 agent 指令"]
  end

  subgraph Boundary["信任边界（官方承认的缺口）"]
    B1["没有权限系统<br/>不询问就调用工具，含破坏性调用"]
    B2["没有沙箱<br/>agent 可访问整台设备"]
    B3["不询问就加载仓库配置"]
  end

  subgraph Out["离开设备的数据"]
    O1["对话 / 工具输出 / 读到的文件 → 模型供应商"]
    O2["文件内容 / commit / deltas → Cloudflare R2 与 Durable Objects"]
    O3["已识别密钥在离开设备前替换为 REDACTED"]
  end

  P1 --> A1
  P2 --> A2
  P3 --> A3
  A1 --> B1
  A2 --> B2
  A3 --> B3
  B1 --> Out
```

## 综合结论

**1. 真正的变量是工作单元，不是 agent 能力。** 主流 CLI agent 的单位是“一次会话 + 一个工作目录”，会话结束后对话留在模型侧、改动留在 git 里，两者之间只有一条时间线能对齐。Delta 让 thread 同时持有对话与工作副本，于是三类此前很难做到的操作变成默认能力：整体回退、就地评论、实时共享。

**2. DeltaDB 是在为“引用”找稳定锚点。** 官方那句 “a reference anchors to a change rather than a line number and survives as the code moves” 说的是同一件在别处反复被讨论的事：行号是脆弱的标识。[[Coding Agent 编辑工具]] 里各家 patch 格式去掉行号、改用上下文匹配，是同一个问题在编辑层的解法；Delta 把它下沉到版本控制层，好让评论、对话与改动能长期指向同一个东西。

**3. 多人在场的规则定义得比能力更细。** 谁在跑（发送者的机器）、谁付钱（发送者）、谁能看见草稿（所有参与者）、谁能改权限（owner），文档都给了明确答案，也坦白了“没有只发给协作者的通道”。这套规则是产品的主体，模型反而是可换的部件。

**4. 与本地 CLI agent 的位置差异。**

| 维度 | 本地 CLI agent | Delta |
| --- | --- | --- |
| 工作单元 | 会话 + 工作目录 | thread（对话 + 工作副本，可共享） |
| 改动落点 | 直接改你的工作目录 | 默认隔离 checkout，改动要带回来 |
| 历史 | git commit + 会话记录分离 | DeltaDB 连续 delta，对话与改动同轨 |
| 回退粒度 | commit / stash | 任意点回退，对话与文件一起 |
| 协作 | 靠 PR 与外部工具 | 原生实时共享、行级评论、review thread |
| 运行位置 | 你的机器 | 发送者所在环境；浏览器 turn 无 shell |
| 数据边界 | 只经模型供应商 | 模型供应商 + Cloudflare 全量存储 |

**5. 生态选择是“沿用约定、闭源本体”。** 技能目录、`AGENTS.md` 这些约定与 Zed 生态其它工具一致，接入成本低；但 Delta 本体在 `zed-industries` 的 131 个公开仓库中找不到对应仓库，文档也没有开源声明，DeltaDB 更没有公开规范。路线图里还有一条有意思的自我定位：**Claude Code plugin**——把别的 harness 的对话与改动也记进 DeltaDB，再回到 Delta 审阅。

## 证据矩阵

| 结论 | 证据来源 | 证据位置 | 置信度 / 限制 |
| --- | --- | --- | --- |
| thread 同时持有对话与工作副本，可整体回退 | 官方文档 | `/docs/concepts/core-concepts` | 高（原文明确） |
| DeltaDB 以连续 delta 取代 commit 快照 | 官方文档 + 首页 | `/docs/concepts/delta-and-git`、首页 | 高 |
| Delta worktree 不是 git worktree | 官方文档 | `/docs/concepts/core-concepts`、`/docs/concepts/worktrees` | 高（文档专门澄清） |
| 托管 checkout 有自己的 git 仓库，commit 不会自动出现在你的仓库 | 官方文档 | `/docs/troubleshooting`、`/docs/agents/review-and-sync` | 高 |
| turn 在发送者环境里跑，浏览器 turn 无 shell | 官方文档 | `/docs/collaboration/collaborate-thread`、`/docs/collaboration/delta-on-the-web` | 高 |
| 没有权限系统、没有沙箱、不询问就加载仓库配置 | 官方文档（自述缺口） | `/docs/privacy-and-security/agentic-safety` | 高（官方自陈） |
| 仓库、commit、deltas 存在 Cloudflare R2 / Durable Objects / KV / D1 | 官方文档 | `/docs/privacy-and-security/data-storage` | 高 |
| 密钥在离开设备前被识别并脱敏，但有明确限制 | 官方文档 | `/docs/privacy-and-security/security` | 高（限制也由官方列出） |
| 启动需登录、联网，且需有 beta 权限 | 官方文档 | `/docs/troubleshooting`、`/docs/installation` | 高 |
| 协作者的草稿会由发送者机器上的 agent 一并在同一个 turn 执行 | 由两条官方规则推导：草稿一起提交 + turn 在发送者环境运行 | `/docs/collaboration/collaborate-thread` | 中（**判断**，文档未直接这样表述） |
| MCP 与沙箱尚未落地 | 官方路线图 | `/roadmap` | 中（路线图自称可能变化） |
| Delta 本体闭源 | 本次 GitHub 核查：`zed-industries` 131 个公开仓库中无对应仓库，文档无开源声明 | `raw/sources/2026-09-17-delta-dev.md` | 中（观察，非官方声明） |
| 并发编辑的合并语义未知 | 文档中无 CRDT / 冲突解决表述，只有分叉后保留本地副本的恢复流程 | `/docs/troubleshooting` | 中（属“没有证据”，非“证据表明没有”） |

## 当前张力、风险与未决问题

1. **安全模型与协作能力不匹配。** 官方自述没有权限系统、没有沙箱，而产品核心是多人在场。把两条规则放在一起——协作者的草稿会在同一个 turn 里被一起提交、turn 又跑在发送者的机器上——意味着队友写下的内容会由你机器上的、无沙箱的 agent 执行。文档没有把这两件事联系起来讨论，这是我认为最需要在采用前确认的一点。
2. **仓库本身是可信输入。** `.agents/prepare` 会被执行、`.envrc` 会被代为授权、`AGENTS.md` 与技能会变成指令，而 Delta 不会先问你要不要加载它们。共享 thread 会把你带进别人的仓库配置里。官方把“worktree trust”列为 roadmap 项。
3. **云端强绑定。** 开工作区要在线且登录；归档三天后本地历史会被清掉，重开需要重新下载；文件内容与 commit 都在 R2。这既是协作能力的前提，也是最主要的锁定与可用性风险。
4. **心智模型摩擦已体现在官方 troubleshooting 里。** “我 commit 了但仓库里没有”“同名分支没有带过来改动”“worktree 历史不可用”都来自同一个根源：Delta worktree、checkout、git worktree 三者名字相近但语义不同。
5. **产品太新。** 三周多从 0.1.1 到 0.16.0，存在同日多版本；路线图里 MCP、沙箱、WSL、conversation branching 都还没到。把它当稳定基础设施还为时过早。
6. **未决问题。** DeltaDB 的并发合并语义未公开；是否支持自托管没有提及；浏览器 turn 与路线图 Remote runtime 的关系不明（首页展示的 Local/Cloud 切换在文档里找不到正式说明）；Jujutsu 支持官方自称不完整。

## 相关页面

- [[Coding Agent 编辑工具]]
- [[Coding Agent Shell 与 Git 权限边界]]
- [[Git 与 Agent 协作的摩擦点和演进方向]]
- [[Agent Harness]]
- [[Code Agent]]
- [[持久化 Agent Harness 的设计模式]]

## 来源指针

- `raw/sources/2026-09-17-delta-dev.md`（本次抓取的逐页事实，含原文引用）
- https://delta.dev/ ｜ https://delta.dev/docs/concepts/core-concepts ｜ https://delta.dev/docs/concepts/delta-and-git ｜ https://delta.dev/docs/concepts/worktrees
- https://delta.dev/docs/agents/subagents ｜ https://delta.dev/docs/agents/skills ｜ https://delta.dev/docs/agents/review-and-sync
- https://delta.dev/docs/collaboration/collaborate-thread ｜ https://delta.dev/docs/collaboration/delta-on-the-web
- https://delta.dev/docs/privacy-and-security/agentic-safety ｜ https://delta.dev/docs/privacy-and-security/data-storage ｜ https://delta.dev/docs/privacy-and-security/security
- https://delta.dev/docs/whats-in-the-latest ｜ https://delta.dev/roadmap ｜ https://delta.dev/pricing
