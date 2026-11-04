<!-- source: https://mp.weixin.qq.com/s/z8JHkCyOVVKrXpKH-vy6tw -->
<!-- type: wechat-article -->
<!-- author: 刘军 -->
<!-- title: Durable Agent 详解：如何让 Agent 在云端长期稳定运行 -->
<!-- accessed: 2026-11-04 Asia/Shanghai -->

# AgentScope Durable Agent 来源笔记

## 访问元信息

- URL：https://mp.weixin.qq.com/s/z8JHkCyOVVKrXpKH-vy6tw
- 作者署名：刘军
- 访问日期：2026-11-04（Asia/Shanghai）
- 抓取方式：网页正文抓取（WeChat 文章页）；页面可能截断或改版，以下仅依据本次读到的正文。

## 文章主张（摘录级）

- 会话历史恢复对话连续性；Durable 进一步恢复任务执行连续性：进度、调用意图、执行结果落在进程外，并在模型调用 / 工具执行等环节设恢复边界。
- 五封通知邮件例子：前三封已确认；第四封服务已接受但本地未保存结果时崩溃；第五封未开始。恢复难点是判断第四封，不能靠“继续”或整任务重跑。
- Durable 要保证：输入有稳定身份；已确认工作可复用；未完成工作有去向；执行过程可重新观察。恢复位置是已提交逻辑边界，不是旧进程指令指针，也不保证外部动作恰好执行一次。
- 普通 Agent 循环把进度留在调用栈；会话 JSONL 可能只有 tool call、没有工具内部检查点。意图与结果之间的空隙需要内部提交 + 外部确认（幂等标识、原操作查询或补偿）。
- AgentScope HarnessAgent + Durable 执行内核：Session 统一提交范围；对象含 Conversation / Entry / Document / Task / Submission / Commit。
- Document：事务中可更新的结构化状态（收件人计划、回执、进度）；带类型与版本；基线 + 增量重建。
- Task：带阶段、checkpoint、终态的持久状态机；状态含 pending / running / waiting / sleeping / completing / terminal。
- Commit：同批可追加 Entry、改 Document、创建或推进 Task、更新 Submission；Session 内提交串行；模型与工具执行在事务外。
- 工具 Task：`call` 保存意图与重放策略后执行；`execute` 为意图已保存、结果未确认的恢复入口；策略双方均为 `safe` 才重跑，否则 `interrupted`。
- 自定义多阶段任务：父任务持久等待子任务（`allSettled` / `failFast`）；邮件例依赖外部幂等与查询。
- AgentCore：托管 Harness、中断续接、节点恢复；文中讨论共同 Session Store、Brain–Hands 分离、Environment、Agent as a Service 方向。Brain 管推理与上下文，Hands 管工具执行，通过已保存调用身份协作。

## 核查与验证限制

- 本次只读微信公众号正文，未审计 AgentScope / AgentCore 源码，未运行示例，未对照官方 API 文档逐字段核实。
- 未把本文与 `@earendil-works/pi-durable` 源码做同源证明；数据模型名词相近只作概念对照，不声称同一代码库。
- WeChat 页面可能截断、改版或图示缺失；若与线上原文冲突，以原文为准并回写本笔记。
