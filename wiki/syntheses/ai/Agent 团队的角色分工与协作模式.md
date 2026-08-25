---
title: Agent 团队的角色分工与协作模式
description: 从 mihomo-rust 移植和 Cursor agent swarm 实验中提炼多智能体协作模式：为什么需要角色分工、四角色（PM/Architect/Engineer/QA）的职责与模型匹配、通过文件系统同步状态的工程机制，以及规划者/执行者分离的模型经济学。
type: synthesis
category: ai
created: 2026-08-18
updated: 2026-08-20
timestamp: 2026-08-20
tags:
  - agent
  - multi-agent
  - collaboration
  - harness
  - spec-driven
  - model-economics
source_refs:
  - raw/sources/2026-08-18-mihomo-rust-agent-team.md
  - https://maxlv.net/blog/porting-mihomo-to-rust-with-claude/
  - https://cursor.com/zh-Hant/blog/agent-swarm-model-economics
resource:
  - raw/sources/2026-08-18-mihomo-rust-agent-team.md
  - https://maxlv.net/blog/porting-mihomo-to-rust-with-claude/
  - https://cursor.com/zh-Hant/blog/agent-swarm-model-economics
---

# Agent 团队的角色分工与协作模式

## 问题

当项目规模大到单个 agent 的上下文窗口装不下、且需要不同层次的决策（架构、排期、实现、验证）时，多智能体团队应该怎么分工？角色之间靠什么同步状态，才能避免决策循环和理解偏差？

## 简答

核心思路是**按决策层次拆分角色**，用**文件系统作为 agent 间的通信协议**而非对话。四角色（PM / Architect / Engineer / QA）各自拥有不同类型的文档：ADR 定架构（不可协商）、spec 填细节（可讨论）、测试计划验证 spec。这种分层让 agent 不需要互相说服，只需要读写约定好的文件。

## 来源事实

mihomo-rust 项目（3 万行 Go → Rust 移植，11 个 crate，40 份 spec，2 份 ADR）使用了 Claude Code 的 Agent Team 机制，四个角色分工如下：

| 角色 | 模型 | 职责 | 拥有的文档 |
| --- | --- | --- | --- |
| PM | Sonnet | 路线图、优先级、里程碑退出标准 | `vision.md`、`roadmap.md`、`specs/*.md`（格式） |
| Architect | Opus | 差距分析、ADR、架构决策、技术方案审查 | `gap-analysis.md`、`adr/*.md` |
| Engineer | Sonnet | 实现代码、写测试、修 CI | 代码、测试 |
| QA | Haiku | 测试计划、覆盖率审查、CI 状态 | `specs/*-test-plan.md`、`ci-status.md` |

模型选择逻辑：架构决策需要最强推理（Opus），结构化执行用 Sonnet，模板化测试用最便宜的 Haiku。

角色间通过文件系统共享状态，关键原则：**ADR 决定架构（不可协商），spec 填充细节（可讨论），测试计划验证 spec**。

## 综合结论

### 1. 为什么需要多智能体：单 agent 的三个瓶颈

单 agent 不是不能做大型项目，但会遇到三个结构性瓶颈：

- **上下文窗口瓶颈**：3 万行代码 + 40 份文档，单个 agent 无法同时 hold 住全局架构和局部实现细节。上下文被早期探索、失败尝试、中间状态填满后，后续决策质量下降。
- **决策层次瓶颈**：架构决策（用不用 tonic）、项目管理决策（M1 先做什么）、实现决策（struct 字段类型）需要不同的思维模式。同一个 agent 用同一套上下文处理所有层次，容易在该严谨时偷懒、该灵活时僵化。
- **验证瓶颈**：agent 自己写代码自己验收，容易把中间推理当成完成证据。需要独立的 QA 角色来写测试计划、审查覆盖率。

多智能体的价值不是"人多力量大"，而是**把不同层次的决策隔离到不同的上下文窗口里**，让每个 agent 专注于自己的抽象层。

### 2. 角色分工的本质：按决策层次拆分，不按任务类型拆分

四角色不是"前端 agent / 后端 agent / 测试 agent"这种按任务类型的拆分，而是按**决策层次**拆分：

- **Architect** 决策"是什么"（架构、接口、分歧策略）
- **PM** 决策"先做什么"（优先级、依赖、里程碑）
- **Engineer** 决策"怎么做"（具体实现）
- **QA** 决策"做完了吗"（测试、覆盖率、CI 状态）

这种拆分的好处是每个角色的上下文窗口只需要装自己那一层的信息。Architect 不需要看每个函数的实现，Engineer 不需要操心排期。

模型匹配也遵循这个原则：推理强度按 Architect > PM ≈ Engineer > QA 递减，成本也递减。

### 3. 文件系统是 agent 间的通信协议，不是对话

多 agent 协作最容易踩的坑是让 agent 之间互相发消息讨论。讨论没有结构，容易产生决策循环（A 问 B，B 问 A，谁也说服不了谁）。

mihomo-rust 的做法是让 agent **通过读写约定好的文件来同步状态**：

- Architect 写 ADR，PM 和 Engineer 读 ADR 来了解架构决策
- PM 写 roadmap，Engineer 读 roadmap 来知道先做什么
- QA 写测试计划，Engineer 读测试计划来知道验收标准

关键是**每个文件有明确的 owner**，其他角色只能读不能改。这避免了多个 agent 同时改一个文件导致的冲突。

### 4. 三层文档分层：ADR → spec → 测试计划

文档不是越多越好，关键是分层清晰：

- **ADR（架构决策记录）**：不可协商的架构决策。比如"Transport 层用 `Box<dyn Stream>` 而非泛型"、"gRPC 手写 gun 帧不引入 tonic"。一旦写入，所有角色必须遵守。
- **spec（技术规格）**：可讨论的实现细节。包括 YAML schema、struct shapes、error types、与上游的分歧。Architect 审查技术内容，PM 控制格式。
- **测试计划**：验证 spec 的测试矩阵。QA 根据 spec 的 error types 生成测试用例。

这三层形成一个单向信息流：ADR 约束 spec，spec 约束测试计划。不需要 agent 之间互相讨论，只需要按层读写。

### 5. 上游分歧的分类决策法

移植项目最棘手的问题是"上游的 bug 要不要复制"。ADR-0002 定义了二分类法：

- **Class A（安全/隐私/路由意图）**：硬错误，拒绝加载。用户读配置时以为得到 X，实际得到 Y 更不安全。
- **Class B（性能/兼容性）**：警告一次，继续运行。流量到达正确目的地，只是走了更慢的路径。

这个分类法的价值在于给 Engineer 一个**默认规则**："不确定时选 Class A，在 PR 描述中标注"。不需要每次都暂停来请求 Architect 决策。

### 6. 模型分工的经济学：规划者用强模型，执行者用便宜模型

Cursor 的 agent swarm 实验（从零实现 SQLite）验证了一个关键结论：**不是所有角色都需要用最强模型**。

实验测试了四种模型组合（规划者 + 执行者）：

| 规划者 | 执行者 | 定位 |
| --- | --- | --- |
| GPT-5.5 | GPT-5.5 | 全高端模型 |
| Grok 4.5 | Grok 4.5 | 成本效益基准 |
| Opus 4.8 | Composer 2.5 | 高端判断 + 高效执行 |
| Fable 5 | Composer 2.5 | 较低端规划者 |

核心发现：

- **Opus 4.8（规划者）+ Composer 2.5（执行者）的组合，以远低于全 Opus 的成本达到了相近的质量**。规划者负责"想清楚做什么"，需要强推理；执行者负责"把事做完"，可以用更便宜更快的模型。
- **单 token 价格不等于总成本**。Fable 5 单 token 价格比 Opus 4.8 高约一倍，但因为用的 planning tokens 少得多，规划者账单反而更低；不过执行者消耗了好几倍 tokens，整体成本更高。
- **提交数不等于产出**。旧版 Grok 4.5 两小时产生 68,000 次提交（新版的 70 倍），但效果更差——大部分是无效忙碌（反复折腾、来回变动）。

这和 mihomo-rust 的模型匹配原则一致：推理强度按 Architect > PM ≈ Engineer > QA 递减。区别在于 Cursor 实验把"规划者/执行者"分得更彻底，证明了**强模型做决策、便宜模型做执行**的经济性。

### 7. 规格是新的工作单位

AI 能力每跃升一次，工程师的工作抽象层级就提高一层：

| 阶段 | 工作单位 | AI 做什么 |
| --- | --- | --- |
| 自动补全 | 一行代码 | 补全字符 |
| 早期模型 | 一个函数 | 实现函数体 |
| 单 Agent | 一个功能 | 写多个函数 |
| **Agent Swarm** | **规格（spec）** | **拆任务、写代码、测试、修复** |

Cursor 实验中，agent swarm 的输入是 835 页 SQLite 手册（即规格），输出是一个能通过 sqllogictest 的数据库实现。**真正稀缺的不是模型能力，而是对意图恰如其分的描述**。

这意味着：把时间花在写清楚规格上，比盯着 agent 写代码更高效。规格越精确，模型可以越便宜，产出越稳定。

## 适用场景与边界

值得用多智能体团队的场景：

- 项目规模大到一个上下文窗口装不下（>1 万行代码或多模块）
- 需要不同层次的决策（架构、排期、实现、验证）
- 有明确的文档驱动流程（愿意写 ADR 和 spec）
- 需要在里程碑之间保持一致性

不值得用的场景：

- 小型项目（< 5K 行），单个 agent 足够
- 探索性原型开发，结构化流程是负担
- 没有测试基础设施，无法验证 agent 产出质量

## 对个人 agent 系统的启发

- 即使不用多 agent，也可以借鉴**按决策层次拆分上下文**的思路：把架构决策写进 ADR，把实现细节写进 spec，让 agent 读文件而不是靠对话记忆。
- **CLAUDE.md / AGENTS.md 是单 agent 场景下的 ADR**：只写不能从代码推断的信息（构建命令、架构骨架、扩展点），不写过时信息。
- **Memory 要精简且可操作**：只存"不要做 X"或"做 Y 时注意 Z"的 feedback 规则，不存代码模式、Git 历史、调试方案。
- **测试是验证 agent 产出的唯一可靠手段**："看起来正确"不等于"运行正确"。
- **规划者用强模型，执行者用便宜模型**：架构决策、需求分析用强模型；按 spec 实现、格式调整用便宜快的模型；校验用脚本。不是所有任务都要上最强模型。
- **写好规格比写好代码更重要**：把需求说清楚（输入是什么、输出是什么、约束是什么），agent 产出质量更高。规格模糊时，agent 会反复试错，产生大量无效改动。
- **警惕无效忙碌**：看 agent 的产出要看最终结果（测试通过、规范校验），不看中间改了多少次。如果 agent 在反复修改同一个文件，说明规格不清楚，应该回去补规格。

## 相关页面

- [[wiki/topics/ai/Agent|Agent]]
- [[wiki/topics/ai/Code Agent|Code Agent]]
- [[wiki/syntheses/ai/Agent Harness 演进范式|Agent Harness 演进范式]]
- [[wiki/syntheses/ai/Agent 循环工作流的控制边界|Agent 循环工作流的控制边界]]
- [[wiki/syntheses/ai/Agent 驱动 Wiki 的维护流程|Agent 驱动 Wiki 的维护流程]]

## 来源指针

- `raw/sources/2026-08-18-mihomo-rust-agent-team.md`
- https://maxlv.net/blog/porting-mihomo-to-rust-with-claude/
- https://cursor.com/zh-Hant/blog/agent-swarm-model-economics
