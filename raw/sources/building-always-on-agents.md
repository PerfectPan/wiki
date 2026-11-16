<!--
source: https://claude.com/resources/articles/building-always-on-agents
type: blog
author: William Hu
published: 2026-11-13
fetched: 2026-11-16
note: body pre-fetched and verified against page HTML
-->

# Building always-on agents — 来源核查记录

## 访问元信息

- 来源：<https://claude.com/resources/articles/building-always-on-agents>
- 标题：Building always-on agents
- 作者：William Hu（致谢 Rodrigo Olivares、Michael Segner）
- 发布日期：2026-11-13
- 访问日期：2026-11-16
- 栏目：Claude Platform · Best practices

## 核查位置与事实摘录

- **引言与动机**：
  - 定义常驻型 Agent（always-on agents）为跨多个会话（sessions）保持状态、无需人类逐步监督即可主动行动的 Agent；底层仍运行与普通 Agent 相同的核心循环（core loop），差异在于外围控制何时唤醒、跨运行保留什么以及如何把结果送达用户的架构组件。
  - 给出两点近期可行性原因：模型对用户意图与何时汇报的判断更稳；长程任务推理成本下降（文中引述某长程编码基准测试中 Opus 5.5 每解决一个任务的成本比 Opus 5 低 78%，而常规负载低 40%）。
- **《The cycle behind the always-on agent》**：
  - 说明“always-on”是用户体验描述，实际上 Agent 大部分时间处于休眠（asleep）状态，周期性唤醒执行一段工作（称为一次 **run**）：接收事件、完成任务、保存发生的信息，随后再次休眠。
  - 一次 run 在一个 **session**（消息与工具调用的记录）内工作。
- **《The core primitives》——五个核心组件**：
  1. **Event inbox（事件收件箱）**：
     - 触发源包括用户消息、webhooks、计划任务（scheduled tasks）和后台作业。若各事件源直接调用 Agent，会出现两个同时到达的事件启动竞争运行、或崩溃导致事件彻底丢失的问题。
     - 最小组成为三部分：持久化事件表（通常为关系型数据库表，按行追加并记录状态，基于源端唯一 ID 去重，建议从每用户一个 inbox 起步）、HTTP 接收端点（handler，快速返回确认，仅做轻量检查，把防提示词注入等深度检查留到 run 内）、后台消费进程（worker）。
     - 延续此前工作的事件（如用户回复）恢复已有 session，其余事件启动新 session。
     - 四条实践要求：handler 快速 ack；inbox 作为真实底稿（worker 唤醒后先从 inbox 拉最新事件，崩溃后新 worker 可接手同一事件重试）；每个 inbox 同一时刻只允许一个活跃 worker（运行中途到达新事件时可推入下一轮 run、并入当前 run 或中断重启）；worker 将连续到达的多条待处理事件合并批处理（batch）。
  2. **Timers（定时器）**：
     - 分为两类：Agent 为自己设定的跟进截止时间（**follow-up**，如检查对方是否回复）与固定周期执行的例行任务（**schedule**，如每日简报）。
     - 存放在独立于 inbox 的持久存储表（inbox 只存放已就绪待处理的事件）。
     - 定时器本身不直接启动 run，而是由后台调度服务（scheduler）固定间隔轮询到期记录：将到期的 follow-up 标记完成，将到期的 schedule 更新为下次触发时间，并向 inbox 插入一条事件唤醒 worker。
  3. **Memory（记忆）**：
     - 存放在独立持久存储（数据库或对象存储）支持的文件目录中，生命周期独立于 worker，参考 Claude Code 的 auto memory 与 Messages API 的 memory tool。
     - 经验法则是只保存无法再次从外部系统（如 issue tracker）查到的内容，外部系统已有的内容只存指针。
     - 划分为四类：
       - **User instructions**：用户对 Agent 行为的要求，单列文件并在每次 run 启动时加载。
       - **User notes**：了解到的用户角色、偏好和历史纠正；随规模增长可拆为多个小文件，每次 run 启动只加载索引，按需读取明细文件。
       - **Past messages**：已告知过用户的内容，避免重复发送；可存成每次必载的文件，或由 worker 加载最近几条与用户的对话。
       - **Task progress**：每个进行中任务的已完成项与剩余项；每次 run 启动只加载索引，按需拉取具体任务进度文件。
     - 提及离线回顾整理（**dreaming**）：在运行之外审阅历史会话，替换过期条目并提炼跨多次 run 的规律。
     - **《Inside the context window》**：每次 run 启动先加载系统提示词、工具定义和记忆文件（固定上下文开销，建议保持精简并配合 prompt caching）；新 session 只带这部分开销和触发事件，已有 session 还会带回此前 run 的消息和工具调用；会话过长时可压缩旧消息（compaction）或开新 session，重要信息需在过程中写入 memory。
  4. **Permissions（权限）**：
     - 三项机制：
       - **Credential store（凭据存储与外部代理注入）**：Agent 发送不带凭据的请求，由 Agent 环境之外的代理（proxy）在转发前注入真实密码或访问令牌。
       - **Auto mode（自动模式）**：使用分类器（classifiers）审阅较高风险动作并拦截危险操作，让模型改用更安全的做法；关键决策仍需用户审阅。
       - **Deferred tool calls（延后工具调用）**：遇到需要用户澄清或批准的工具调用时，暂停该调用、保存调用中途的 session 并结束当前 run；通过界面（如基于 MCP Apps 构建的交互卡片）向用户展示请求；用户回复作为新事件进入 inbox，启动新 run 并携带用户输入恢复已保存的 session；等待期间 worker 可继续处理其他事件而不阻塞。
  5. **Outbox（发件箱）**：
     - 后台运行结束有三种出口：向 outbox 写入一条发给用户的消息、决定无需发送任何内容、或通过 deferred tool call 请求权限/补充输入。
     - 简单场景可直接用 `send` 工具发送；需要控制消息发送节奏或从发送错误中恢复时，使用独立的 outbox 表与后台派发服务（dispatcher）。
     - 强调通过评测（evals）调节发送频率：宁可初期偏安静，再随时间推移逐步获取更多用户注意力。
- **页面配图核查**（HTML 内共 7 张图）：
  - `5dc803bf...gif`：run 唤醒、在 session 内工作、再次休眠的循环动图。
  - `bb08543a...png`：Event inbox 结构图（handler 写入表，worker 读取并推进 run）。
  - `c16694e6...png`：Timers 结构图（run 写入 timer，scheduler 轮询并将到期项推入 inbox）。
  - `e5d209d7...png`：Memory 目录结构示例图（instructions、user notes 索引与分文件、past messages、task progress 索引与分文件）。
  - `48757f0a...gif`：随时间推移上下文占用与 compaction / 新开 session 的变化动图。
  - `700b5f3a...png`：Outbox 结构图（run 写入 outbox，dispatcher 投递给用户）。
  - `9f8df7b2...gif`：五个组件串联成完整闭环的动图。

## 验证记录

- 已通过脚本直接抓取页面 HTML 并提取正文与全部 `<img>` 标签核对章节结构与表述。
- 本文属于架构设计指南，不包含可运行的开源代码库；未在本地搭建或压测文中描述的五组件服务。
- 整理页：[[wiki/topics/ai/personal-agent|Personal Agent 与 Super-agent]]、[[wiki/syntheses/ai/always-on-and-super-agent-architecture|常驻型 Agent（Always-on / Super-agent）的系统架构]]。
