---
title: 可审计的本地 Agent 记忆架构
description: 如何用可编辑的事实层、带来源的画像层和混合检索，为长期 Agent 提供用户可控的本地记忆
type: synthesis
category: ai
status: seed
created: 2026-07-29
updated: 2026-08-02
timestamp: 2026-08-02
tags:
  - agent
  - memory
  - local-first
  - provenance
  - rag
source_refs:
  - https://x.com/asterove_ai/status/2082173389368909931
  - https://github.com/Asterove/AsterMem
  - https://github.com/tommy0103/obelisk
resource:
  - https://x.com/asterove_ai/status/2082173389368909931
  - https://github.com/Asterove/AsterMem
  - https://github.com/tommy0103/obelisk
---

# 可审计的本地 Agent 记忆架构

## 问题

长期 Agent 需要跨会话保留用户偏好、历史决策和项目事实，但常见记忆产品会把原始对话交给一个不可见的提炼与召回黑箱。用户难以知道系统记住了什么、依据是什么、何时会召回，也难以修正错误记忆。

## 简答

更可靠的个人 Agent 记忆应当把“可审计、可修改、可追溯”放在召回效果之前：原始事实保存在用户拥有的本地文件中；供会话启动使用的短画像由事实层派生；每条派生结论都保留来源；检索索引只是可重建的加速层，而不是唯一事实来源。

## 分层模型

### 1. 用户拥有的事实层

- 使用 Markdown 或其他可直接读取、diff、备份的格式保存长期事实。
- 删除、修改和归档必须可由用户直接完成，不应依赖模型或厂商后台。
- SQLite、向量索引、关键词索引可以提高查询效率，但都应能从事实层重建。
- 备份边界应明确，理想状态是复制一个目录即可恢复。

### 2. 带 provenance 的画像层

- 会话启动不应注入全部历史，而应注入短小、稳定的用户画像和当前项目摘要。
- 每条画像必须指向支持它的原始记忆；无法追溯的结论不应进入画像。
- 画像是派生视图，不是新的权威事实。用户修改事实后，系统应能重建画像并消除旧结论。
- 画像应支持逐条编辑、删除、关闭和过期处理，避免错误事实被长期固化。

### 3. 可重建的检索层

- 关键词搜索适合名称、命令、日期和精确措辞；向量搜索适合语义近似和表达变化。
- 混合检索通常比只依赖 embedding 稳定，中文场景还需要合适的分词策略。
- 检索结果应返回来源片段，而不只返回模型生成的总结。
- 更换 embedding provider 或模型时，索引应后台重建；事实层和关键词检索不应因此不可用。

### 4. 受约束的 Agent 接口

- Agent 应通过明确的 add、search、patch、archive 等工具操作记忆，避免直接获得不受限的目录写权限。
- read、write、config、admin、destructive 等能力应分 scope；破坏性动作需要额外确认。
- “写入一条记忆”和“把它提升为长期画像”应是两个不同动作，便于审计和纠错。

## AsterMem 案例

AsterMem 是这一架构的早期实现案例：

- 数据位于本机 `./data/`，使用 Markdown、SQLite、Chroma 和 Whoosh；
- 支持关键词与语义混合检索，中文关键词检索使用 jieba；
- 提供带来源的 profile layer，用短画像减少每次会话重复说明和上下文占用；
- 可连接 Ollama / LM Studio 离线运行，也支持多种云模型；
- 通过单用户 Web UI 和 Agent skill 管理记忆、模型配置与 API token。

它验证了“文件事实层 + 派生画像 + 可重建索引 + Agent 工具接口”可以包装成完整产品，但目前仍是早期项目：截至 2026-07-29，仓库历史和外部采用规模都很小，不能把产品声明等同于生产验证。

## Obelisk 案例：把会话历史作为证据层

[[Obelisk]] 展示的是相邻但不同的路线：它不先从对话自动提取用户画像，而是把 Claude Code、Codex 和 Kimi Code 已存在的本地会话统一索引为 SQLite 证据层，让 Agent 查询消息、工具调用、子 Agent、workflow 和文件历史；只有当检索得到的结论值得长期保存、且用户批准后，才把 Markdown memory 注册为二级综合缓存。

这补充了本页的一个重要边界：对于 coding agent，“事实层”不一定只有人工维护的 Markdown，也可以包含可重放的原始会话；但原始会话量大且含噪，仍需要一个可重建索引，不能直接作为每次会话的启动上下文。Obelisk 当前的默认 FTS 对中文不友好，也说明“本地可审计”并不会自动解决召回质量。

## 采用判断

对已有长期 Agent 系统，更稳妥的路线不是立即替换现有记忆，而是隔离试跑：

1. 使用脱敏测试数据运行 3–7 天。
2. 测量精确事实召回、语义召回、错误记忆修正、画像漂移和启动上下文节省。
3. 验证重建索引、导入导出、备份恢复和 provider 切换。
4. 检查默认凭据、监听地址、API token scope 和破坏性操作确认。
5. 只有在召回质量和治理能力都优于现有文件记忆后，再考虑迁移。

## 风险和边界

- 自动提炼会把模型误判变成长期偏见，provenance 只能帮助追责，不能保证结论正确。
- 本地运行不自动等于安全；默认密码、监听公网、弱 token scope 和第三方模型 provider 都可能让记忆外泄。
- 记忆越多，召回污染和过期事实越严重，需要过期、冲突和可信度策略。
- 项目采用 AGPL-3.0。本地个人使用通常边界清楚；若改造后作为闭源网络服务提供，需要单独评估许可证义务。

## 相关页面

- [[Agent 主动上下文管理]]
- [[Claude 5 时代的上下文工程]]
- [[RAG 问答管线]]
- [[Agent Harness 演进范式]]
- [[Obelisk]]

## 来源指针

- <https://x.com/asterove_ai/status/2082173389368909931>
- <https://github.com/Asterove/AsterMem>
- <https://github.com/tommy0103/obelisk>
