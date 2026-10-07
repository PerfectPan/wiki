---
title: Agent 记忆方案对比：gbrain、memU、agentmemory 与 Letta
description: 按记忆写入责任、存储与召回方式、运行位置和治理成本比较四种 Agent memory 方案
type: comparison
category: ai
created: 2026-10-07
updated: 2026-10-07
timestamp: 2026-10-07
tags:
  - agent
  - memory
  - context-engineering
  - provenance
source_refs:
  - raw/sources/gbrain.md
  - raw/sources/memu.md
  - raw/sources/agentmemory.md
  - raw/sources/letta-context-repositories.md
  - https://github.com/garrytan/gbrain
  - https://memu.pro/
  - https://www.agent-memory.dev/
  - https://www.letta.com/blog/context-repositories/
  - https://docs.letta.com/concepts/memfs
  - https://docs.letta.com/configuration/memory
resource:
  - raw/sources/gbrain.md
  - raw/sources/memu.md
  - raw/sources/agentmemory.md
  - raw/sources/letta-context-repositories.md
  - https://github.com/garrytan/gbrain
  - https://memu.pro/
  - https://www.agent-memory.dev/
  - https://www.letta.com/blog/context-repositories/
  - https://docs.letta.com/concepts/memfs
  - https://docs.letta.com/configuration/memory
---

# Agent 记忆方案对比：gbrain、memU、agentmemory 与 Letta

## 当前结论

四者都保留跨会话信息，但主要分歧是**谁决定记什么、记录以什么为准、如何取回，以及谁负责纠错**。选择应从信息来源与维护方式出发，而不是只比较向量数据库或宣传的召回率。

以下是基于 2026-10-07 文档与源码的采用判断，未安装产品或进行同条件评测：

| 主要需求 | 优先评估 | 理由 |
| --- | --- | --- |
| 长期积累人物、组织、会议、事实及关系 | gbrain | 知识库、来源、图关系与后台整理覆盖面广，也承担更多状态维护工作 |
| 多个现有 agent 共享提炼后的记忆与技能 | memU | 宿主 agent 负责理解，统一 backend 负责保存和检索 |
| 自动记录开发会话，查回做过什么、接着完成任务 | agentmemory | hooks、session、observation 和本地检索直接围绕 coding 工作流 |
| 用文件和 Git 管理可编辑的长期上下文 | Letta Context Repositories / MemFS | 普通文件操作、按需读取、版本与 worktree 是主要组织方式 |

## 阅读范围与版本

| 对象 | 本次证据 |
| --- | --- |
| gbrain | `garrytan/gbrain` 提交 `5b5891069413b28b2fe3a50675116d67d5a1e145`；入口、engine、operation 注册、检索、撤回和存储说明 |
| memU | `NevaMind-AI/memU` 提交 `2c050bc9681a4c0aff1af211a000e73d14f33356`；service、领域模型、prepare/commit、检索与测试案例 |
| agentmemory | `rohitg00/agentmemory` 提交 `007a1a7fe8646a03d8652eb0712400cc6f0fcca3`；worker、采集、KV、检索、测试与评测定义 |
| Letta | 2026 年 2 月 Context Repositories 博客，加访问日的 MemFS、Memory & dreaming 文档；未读完整实现 |

前三项的链接与具体文件位置保存在页末的源码核对记录。文档声明与静态源码能确认设计和分支，不能证明真实宿主中的自动采集、恢复和召回已经生效。

## 架构差异：记忆从哪里来

```mermaid
flowchart TB
    subgraph G["gbrain：长期知识库"]
        G1["显式事实与来源页面"] --> G2["知识写入与后台整理"]
        G2 --> G3["Markdown + Postgres 或 PGLite"]
        G3 --> G4["关键词、关系、可选向量与综合回答"]
    end
    subgraph M["memU：宿主提炼，共享服务"]
        M1["adapter 读取会话"] --> M2["宿主 agent 编写 memory 或 skill"]
        M2 --> M3["commit_results：embedding 与存储"]
        M3 --> M4["progressive_retrieve 返回片段与文件"]
    end
    subgraph A["agentmemory：开发会话采集"]
        A1["hooks、MCP、REST"] --> A2["采集 inbox 与 observation"]
        A2 --> A3["本地状态与搜索索引"]
        A3 --> A4["会话注入或主动召回"]
    end
    subgraph L["Letta：Git 记忆文件"]
        L1["主 agent 或后台整理"] --> L2["checkout 或独立 worktree"]
        L2 --> L3["Git 提交；按部署方式同步"]
        L3 --> L4["常驻文件与按需读取"]
    end
```

图概括的是主要路径，各自也有可选功能。依据见下文对应源码与文档；不能从某个产品有“图”或“向量”就推断默认路径已经启用它。

### gbrain：知识管理覆盖面广，备份不止文件

`createEngine` 支持 Postgres 与 PGLite；`BrainEngine` 包含页面、分块、来源、关系和时间线。`hybridSearch` 先取得词法与关系结果，再根据配置加入向量、融合与重排。模型生成的综合回答属于另一个可选能力。[engine-factory.ts][g-engine]、[hybrid.ts][g-search]

关键取舍是**文件可读与数据库必要性同时存在**：一部分知识可由 Markdown 重建，但数据库也保存未在文件中表达的事实、历史、授权、撤回与任务状态。只导出 Markdown 会丢失这部分恢复能力。[存储说明][g-record]

它适合把显式事实、资料和关系长期积累起来；自动采集与后台增强需要单独配置。关键词查询可以不配置模型 API，embedding、提取与综合则可能增加调用成本。`forget` 表示退出活动召回，不代表所有原始资料和备份已擦除。[记忆边界][g-boundary]

### memU：提炼在宿主，服务不生成总结

当前 `MemoryService` 只组合存储和 embedding。adapter 将新会话准备成任务，由现有 agent 决定忽略、修订或新增 Markdown；`commit_results` 接收结果；下次任务通过 adapter 召回。生成式模型成本发生在宿主，不能把“服务不调用 chat”理解为整个流程不用模型。[service.py][m-service]、[README][m-readme]

`progressive_retrieve` 这个名字容易误导：本次源码对 query 做一次 embedding，搜索片段，汇总命中的文件，并检索资源；没有多轮 LLM 判断“信息够不够”。模型对象是 `RecallFile`、`RecallFileSegment` 与 `Resource`，所以“Wiki / Markdown”描述的是可读内容形式，不代表底层只有文件。[agentic.py][m-agentic]、[models.py][m-models]

提交前先完成 embedding，可避免 provider 失败后留下部分写入；但后续多条存储操作没有统一事务回滚。评估批量更新时要区分这两个保证。[commit_results][m-agentic]

### agentmemory：先捕获过程，再组织召回

hooks 产生的事件进入 capture inbox，再调用 observe 保存会话 observation；重复事件与重试有单独状态。长期 `Memory` 还记录来源 observation、版本和替代关系。运行时通过 iii 的 `StateKV` 管理状态，不是直接维护一套 Git Markdown。[capture.ts][a-capture]、[types.ts][a-types]、[kv.ts][a-kv]

默认逐条 observation 处理使用不调用生成式模型的表示；生成式压缩需要启用。keyless 配置以关键词召回为起点，本地 embedding 需另行启用并首次下载模型；配置和数据具备后可以使用向量、图等检索方式。[observe.ts][a-observe]、[README][a-readme]、[search.ts][a-search]

**95.2% 不是回答准确率。** 项目报告测量 `recall_any@5`，只要求前五个结果出现任一正确来源会话；使用 BM25 加本地向量，没有生成答案或评判答案。它既不能证明多来源推理正确，也不能代表默认 keyless 配置。[评测定义][a-eval]

### Letta：普通文件操作与 Git 版本管理

Context Repositories 的设计让 agent 用终端和文件工具维护记忆，通过目录与描述先定位、再读取。后台整理可在独立 worktree 中修改后合并。[原始博客](https://www.letta.com/blog/context-repositories/)

当前 MemFS 文档与博客有一处值得保留的区别：**新结构把根目录文件常驻到系统提示词，旧 agent 使用 `system/`**；子目录用 `MEMORY.md` 索引按需读取。默认没有语义或向量索引；可选搜索扩展与会话历史搜索是另外的能力。[MemFS](https://docs.letta.com/concepts/memfs)

云端 agent 的仓库由 Letta 托管，本地副本通过提交和推送同步；local-only agent 自行备份。每个 agent 默认有自己的 MemFS，跨会话保留不等于任意 agent 共享。后台 dreaming 的 agent 复核也不是人工审批。[MemFS](https://docs.letta.com/concepts/memfs)、[Memory & dreaming](https://docs.letta.com/configuration/memory)

## 生命周期：保存成功不等于下次用得对

下面以 memU 的已核对路径说明几个独立阶段；最后的纠错验证是本文建议，不是产品自动保证。

```mermaid
sequenceDiagram
    participant H as 宿主 adapter
    participant A as 宿主 agent
    participant M as MemoryService
    participant E as Embedding provider
    participant D as 数据库
    H->>A: prepare：新会话与已有记忆
    A->>A: 判断并编写 Markdown
    H->>M: commit_results
    M->>E: 对变更内容批量 embedding
    E-->>M: 向量
    M->>D: 写文件记录、片段和资源
    M-->>H: 提交结果
    Note over H: 成功后推进会话处理状态
    A->>M: 下次任务 progressive_retrieve
    M->>E: query embedding
    M->>D: 搜索片段并汇总文件
    M-->>A: 片段、文件与资源
    Note over A,D: 建议验证：纠正后旧结论是否仍被召回
```

依据：[bridging/pipeline.py][m-pipeline]、[agentic.py][m-agentic]。这里的 commit 是 memU 的写入操作，不应与 Letta 的 Git commit 混为一谈。

## 所有权、扩展和维护成本

| 维度 | gbrain | memU | agentmemory | Letta |
| --- | --- | --- | --- | --- |
| 运行位置与控制权 | 自管内容、数据库和 provider；远程 MCP 可共享 | 自托管 SQLite/Postgres，或 memU Cloud；宿主负责提炼 | 本地服务与状态；可配置外部 provider | 本地 checkout；云端仓库托管或 local-only |
| 核心维护循环 | 写入资料/事实 → 索引与整理 → 召回/综合 → 修正 | prepare → 宿主编辑 → commit → retrieve | 捕获 → 去重与组织 → 索引 → 注入/查询 | 编辑/反思 → 提交/合并 → 常驻或按需读取 |
| 扩展面 | CLI/MCP、engine、operation、模型 provider | TranscriptSource、host adapter、存储与 embedding provider | hooks、MCP/REST、provider、worker 函数 | 文件工具、记忆 skills、worktree、可选搜索 mod |
| 主要成本 | DB 与后台任务运维；可选模型调用 | 宿主提炼、embedding、backend；Cloud 条款另核对 | 采集与索引资源；可选压缩/模型；宿主集成维护 | 主 agent 与 dreaming token；同步与仓库维护 |
| 迁移与锁定风险 | 只迁 Markdown 会漏掉 DB 独有状态 | 可读正文仍需迁移记录、资源引用和配置 | observation、session、索引与集成需一起处理 | Git 内容易读；自动同步与上下文装载仍依赖运行时 |

运行与扩展信息来自上文源码和官方文档；成本、迁移风险是基于组件依赖的工程判断。本次没有核实套餐报价，也不比较账单金额。

## 数据边界：本地保存之后，内容还会去哪里

```mermaid
flowchart LR
    Logs["会话、工具输出、外部资料"] --> Capture["采集范围与写入规则"]
    Capture --> Store["文件或数据库"]
    Store --> Recall["按当前任务检索"]
    Recall --> Context["宿主 agent 的上下文"]
    Context --> Model["宿主模型：可能在云端"]
    Store -. 启用后 .-> Provider["embedding、提取、重排等 provider"]
    Store -. 配置后 .-> Remote["共享服务、Git remote 或备份"]
    User["用户控制范围、修正和删除"] --> Capture
    User --> Store
```

这是对四种方案共同数据路径的归纳，并非每种产品都启用所有箭头。gbrain 的[记忆边界][g-boundary]明确区分本地存储、云 provider 与宿主模型；memU 的 service 与 agentmemory 的 provider 配置也支持这个区分。

具体需要区分三件事：

1. **记录有来源，不等于事实正确。** 模型可能误读来源；召回时仍要核对时间、修订和适用项目。
2. **逻辑分类，不等于访问隔离。** gbrain 的 source 不能隔离共享本地文件或数据库凭据的调用者；memU 的 scope 过滤也不能替代服务认证。[gbrain 边界][g-boundary]、[memU service][m-service]
3. **撤回召回，不等于彻底删除。** 原始日志、Git 历史、远程副本和备份是独立对象；这是由各自存储方式推得的治理要求，不声称它们已经统一实现擦除。

## 如何实现 Agent Memory

下面是综合这些实现得到的设计建议，以“一个用户在多个 coding agent 中保留项目事实”为例。这里的字段与接口是建议方案，不是四个产品共有的 API。

### 1. 先确定保存的对象

将输入分成三类：会话事件记录“发生过什么”；长期事实记录“以后仍应遵守什么”；可复用步骤记录“遇到同类任务怎样做”。当前任务做到哪一步可以作为会话交接，但不要自动提升为永久规则。agentmemory 的 observation/Memory 分离、memU 的 memory/skill 分轨和 gbrain 的记忆边界分别提供了这些设计依据。[数据类型][a-types]、[memU 模型][m-models]、[记忆边界][g-boundary]

第一版可从明确的“记住这个”与用户纠正开始，等写入、纠错和召回可验证后再自动读取会话。自动提炼时先生成候选，附原始消息或工具结果位置，由宿主 agent 或后台任务决定是否写入；同一事件只处理一次。这样能复用 memU 的 prepare/commit 分离和 agentmemory 的事件去重方法。[prepare/commit][m-pipeline]、[事件采集][a-capture]

### 2. 选一份权威记录，索引从它派生

若重点是人工编辑与 Git 审阅，可以选 Markdown；若重点是多个 agent 并发写入、条件更新与过滤，可以选 SQLite 起步。无论选哪种，都要明确索引损坏后从哪里重建，以及哪些历史与撤回状态必须另外备份。文件与数据库同时参与时，不能只写“以文件为准”就省略恢复规则。[gbrain 存储说明][g-record]、[Letta MemFS](https://docs.letta.com/concepts/memfs)

```mermaid
flowchart TB
    Input["用户纠正、消息、工具结果"] --> Capture["采集：限制范围、事件去重、保存来源"]
    Capture --> Candidate["宿主 agent 或后台任务提炼候选"]
    Candidate --> Writer["写入：校验范围、版本与替代关系"]
    Writer --> Record["权威记录：Markdown 或数据库"]
    Record --> Index["派生索引：关键词；按需加入向量"]
    Query["当前任务、身份、项目、token 预算"] --> Retrieve["过滤后检索与排序"]
    Index --> Retrieve
    Retrieve --> Check["回查记录状态与版本"]
    Record --> Check
    Check --> Pack["带来源的少量上下文"]
    Pack --> Agent["宿主 agent 执行任务"]
    Agent -->|明确纠正或新事实| Writer
```

这个图增加了“返回前回查记录”一步：即使索引更新滞后，也不返回已经撤回或被替代的版本。它是针对异步索引的设计建议，依据是 gbrain 撤回时同时处理事实与派生内容的做法，见 [[raw/sources/gbrain#撤回为何需要修改多个对象|gbrain 撤回链路]]。

### 3. 让每条记忆可定位、可纠正

最小记录可以包含：

| 字段组 | 用途 |
| --- | --- |
| `id`、`revision` | 稳定身份与条件更新，防止旧会话覆盖新版本 |
| `scope` | 用户、项目以及可见范围；由调用方认证结果约束 |
| `kind`、`content` | 区分偏好、项目事实、操作步骤与正文 |
| `source_refs`、`observed_at` | 找到原始依据及记录时间 |
| `status`、`supersedes` | 标明生效、被替代或撤回，以及替代了哪条记录 |
| `valid_until` | 只有确有有效期的信息才填写，不能假设所有事实永久有效 |

例如“项目 A 改用 pnpm”应带项目范围与用户纠正来源，并替代 A 中旧的 npm 记录；不能把项目 B 的 npm 约定一起失效。不同项目适用不同规则不属于冲突。版本、来源和替代关系可参考 agentmemory 的 `Memory`，范围和撤回则参考 gbrain。[Memory 定义][a-types]、[记忆边界][g-boundary]

### 4. 把写入、修订和撤回做成明确操作

建议先提供 `remember`、`recall`、`revise`、`forget` 四个操作。写入返回记录 ID 和版本；修订带预期版本，过期时先重新读取；重试带事件 ID 或请求 ID；撤回返回活动记忆已失效的结果。SQLite 方案中把记录更新与待索引任务放进同一事务，再异步生成向量，失败可以重试而不会丢掉正文。

这是对 gbrain 的持久请求与修订检查、agentmemory 的 capture inbox 的简化应用。不要为了“用向量”让记住一句明确事实必须等待外部 embedding 成功；memU 当前先 embedding 再写入的做法则适合接受这种可用性取舍的系统。[gbrain 写入边界][g-record]、[capture inbox][a-capture]、[memU 提交][m-agentic]

“忘记”还要区分停止召回与物理清除。前者让记录失效并更新索引；后者需要说明原始日志、Git 历史、远端和备份的处理范围，不能用删掉一个索引条目代替。[gbrain 边界][g-boundary]

### 5. 检索先解决范围和预算

先按身份与项目限制候选，再做关键词检索；确有同义表达漏召回时加入向量检索。合并结果后去重，去掉失效或被替代的记录，优先保留与任务相关且来源明确的内容，按 token 预算截取。结果返回记录 ID、版本、时间、正文和来源，agent 可以继续读取完整证据。[gbrain 检索][g-search]、[agentmemory 检索][a-search]

会话启动只加载少量稳定规则和最近交接；具体问题再按需检索。Letta 的常驻文件与目录索引、agentmemory 的 `mem::context` 预算组装提供了两种可借鉴的实现。不要把 top-k 当作上下文预算：五篇长文也可能挤占当前任务。[MemFS](https://docs.letta.com/concepts/memfs)、[context.ts][a-context]

### 6. 后台维护与前台工作分开

前台记住用户明确纠正的事实；后台再整理重复内容、提炼技能、处理过期记录和更新索引。后台写入也要检查版本，不能覆盖前台刚接受的纠正。文件方案可以用 Letta 的独立 worktree；数据库方案可以用待处理任务和修订号。[Letta dreaming](https://docs.letta.com/configuration/memory)、[gbrain 写入边界][g-record]

外部网页或工具输出中的指令只作为待分析内容，不应因为被保存为“记忆”就获得改变权限或工具配置的能力；自动写入范围与业务操作权限分别控制。[gbrain 记忆边界][g-boundary]

### 7. 用完整闭环验收

| 场景 | 要观察的结果 |
| --- | --- |
| 保存后开启全新会话 | 目标宿主能主动取到记录，带正确来源 |
| 用户纠正 npm 为 pnpm | 后续回答采用新值；旧记录可追溯但不再作为有效约定 |
| 同一个事件重试两次 | 不产生两条重复记忆 |
| 查询另一个项目 | 不把原项目私有事实注入上下文 |
| 撤回后重建索引 | 已撤回内容不会因旧来源重导入而恢复生效 |
| provider 不可用或后台中断 | 能说明哪些写入已持久保存、哪些任务尚未完成 |
| 导出后在隔离目录恢复 | 恢复正文、来源、修订与撤回状态，而不只是搜索结果 |

把召回证据是否齐全与最终回答是否正确分开测量，另记录无关记忆比例、上下文 token、延迟与调用成本。先做几十条贴近实际工作的案例，再决定是否需要图关系、自动技能提炼或复杂重排；agentmemory 的检索评测也说明单个 recall 数字不能覆盖完整闭环。[评测方法][a-eval]

对当前文件优先 Wiki，可以先保留正文、frontmatter、来源指针和 PR，补按需检索与来源回查；已有结构已经覆盖内容维护，不必同时接入四套记忆系统。相关设计目标见 [[wiki/syntheses/ai/auditable-local-agent-memory-architecture|可审计的本地 Agent 记忆架构]]。

## 结论与证据对照、尚未验证的行为

| 结论 | 证据位置 | 置信度或限制 |
| --- | --- | --- |
| gbrain 有无 embedding 的不同召回分支 | `hybridSearch`；[源码][g-search] | 已读源码；未测实际 provider 降级 |
| Markdown 不是 gbrain 完整备份 | [system-of-record][g-record] 与 [memory-boundaries][g-boundary] | 官方明确；未恢复数据库 |
| memU 由宿主提炼，服务仅 embedding 与存储 | `MemoryService`、`commit_results`；[源码][m-service] | 已读实现；未验证宿主定时任务 |
| memU 当前检索不是多轮生成式判断 | `progressive_retrieve`；[源码][m-agentic] | 已读分支与结果结构 |
| agentmemory 的采集与召回是不同阶段 | capture/observe/search；[源码][a-capture] | 已读实现和 mock 测试案例；未测真实进程崩溃 |
| 95.2% 是来源会话召回，不是 QA | [LongMemEval 报告][a-eval] / Setup、Methodology | 指标定义明确；未独立复现 |
| Letta 常驻目录规则已区别新旧 agent | [MemFS](https://docs.letta.com/concepts/memfs) / Memory structure | 当前官方文档；未测迁移 |

没有统一数据集、相同模型、相同 token 预算和相同隐私约束下的四方结果，因此不作效果排名。真正试用时应检查：新会话自动召回、中文与混合语言查询、旧事实修正、跨项目误召回、撤回后的索引一致性，以及完整备份恢复。安装命令成功或某次 CLI 查询命中，都不能替代这些结果。

## 来源记录与相关页面

- [[raw/sources/gbrain]]
- [[raw/sources/memu]]
- [[raw/sources/agentmemory]]
- [[raw/sources/letta-context-repositories]]
- [[wiki/syntheses/ai/auditable-local-agent-memory-architecture|可审计的本地 Agent 记忆架构]]
- [[wiki/syntheses/ai/agent-proactive-context-management|Agent 主动上下文管理]]
- [[wiki/topics/ai/obelisk|Obelisk]]

[g-engine]: https://github.com/garrytan/gbrain/blob/5b5891069413b28b2fe3a50675116d67d5a1e145/src/core/engine-factory.ts
[g-search]: https://github.com/garrytan/gbrain/blob/5b5891069413b28b2fe3a50675116d67d5a1e145/src/core/search/hybrid.ts
[g-record]: https://github.com/garrytan/gbrain/blob/5b5891069413b28b2fe3a50675116d67d5a1e145/docs/architecture/system-of-record.md
[g-boundary]: https://github.com/garrytan/gbrain/blob/5b5891069413b28b2fe3a50675116d67d5a1e145/docs/guides/memory-boundaries.md
[m-readme]: https://github.com/NevaMind-AI/memU/blob/2c050bc9681a4c0aff1af211a000e73d14f33356/README.md
[m-service]: https://github.com/NevaMind-AI/memU/blob/2c050bc9681a4c0aff1af211a000e73d14f33356/src/memu/app/service.py
[m-agentic]: https://github.com/NevaMind-AI/memU/blob/2c050bc9681a4c0aff1af211a000e73d14f33356/src/memu/app/agentic.py
[m-models]: https://github.com/NevaMind-AI/memU/blob/2c050bc9681a4c0aff1af211a000e73d14f33356/src/memu/database/models.py
[m-pipeline]: https://github.com/NevaMind-AI/memU/blob/2c050bc9681a4c0aff1af211a000e73d14f33356/src/memu/hosts/bridging/pipeline.py
[a-readme]: https://github.com/rohitg00/agentmemory/blob/007a1a7fe8646a03d8652eb0712400cc6f0fcca3/README.md
[a-capture]: https://github.com/rohitg00/agentmemory/blob/007a1a7fe8646a03d8652eb0712400cc6f0fcca3/src/functions/capture.ts
[a-types]: https://github.com/rohitg00/agentmemory/blob/007a1a7fe8646a03d8652eb0712400cc6f0fcca3/src/types.ts
[a-kv]: https://github.com/rohitg00/agentmemory/blob/007a1a7fe8646a03d8652eb0712400cc6f0fcca3/src/state/kv.ts
[a-observe]: https://github.com/rohitg00/agentmemory/blob/007a1a7fe8646a03d8652eb0712400cc6f0fcca3/src/functions/observe.ts
[a-search]: https://github.com/rohitg00/agentmemory/blob/007a1a7fe8646a03d8652eb0712400cc6f0fcca3/src/functions/search.ts
[a-context]: https://github.com/rohitg00/agentmemory/blob/007a1a7fe8646a03d8652eb0712400cc6f0fcca3/src/functions/context.ts
[a-eval]: https://github.com/rohitg00/agentmemory/blob/007a1a7fe8646a03d8652eb0712400cc6f0fcca3/benchmark/LONGMEMEVAL.md
