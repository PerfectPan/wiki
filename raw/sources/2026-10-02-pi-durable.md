<!-- source: https://github.com/earendil-works/pi -->
<!-- type: repository-review -->
<!-- fetched: 2026-10-02 -->
<!-- commit: 9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16 -->

# Pi Durable 1.0.0 源码阅读记录

## 范围

- 对象：`@earendil-works/pi-durable`，仓库 `earendil-works/pi` 的 `packages/durable`。
- 固定快照：`9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16`，查阅日期 2026-10-02。
- 包版本与发布说明：1.0.0，CHANGELOG 标记 2026-10-01；README 明确标为 Experimental。
- 方法：阅读 README、包定义、设计说明、核心实现和恢复测试；未安装依赖、运行上游测试或调用真实模型。
- 与本库旧资料的关系：2026-08-20 的 harness-v2 是历史设计，本记录不将它当作当前实现。

## 已核对的代码路径

下列路径均相对于固定快照的 `packages/durable/`；页末给出不可漂移的链接。

| 入口或模块 | 已读内容与结论 |
| --- | --- |
| `src/harness/harness.ts` | Harness 继承 Session；Conversation 提交输入、配置 agent、fork、abort；关闭时等待调度器中的调用结束 |
| `src/types.ts` | Conversation、Entry、Task、Submission、Document；Task checkpoint 为完整状态；Storage 接受原子写入批次 |
| `src/session/session.ts` | Promise 队列串行提交，依次执行回调、准备写入、存储、采纳内存状态和发布；未知存储错误令 Session 不再接受工作 |
| `src/session/transaction.ts` | 多种记录、文档变更和子任务组成同一批次；检查任务 owner 和文档生命周期 |
| `src/harness/submissions.ts` | `requestId` 在 conversation 范围去重；忙碌时进入 inbox 或拒绝；空闲输入原子创建消息、submission 与 generation |
| `src/harness/generation.ts` | `prepare/request/retry/poll/tools` 各阶段；请求参数、cutoff 与 deferred handle 持久化；流式 partial 先提交再观察 |
| `src/harness/tool.ts` | 参数校验、beforeTool、intent checkpoint、execute、afterTool、结果提交；默认 unsafe，恢复时保存策略和当前策略都 safe 才重跑 |
| `src/harness/scheduler.ts` | open 时把 running 恢复为 pending；阶段调度、任务迁移、abort 标记、owner 传播、旧调用写入检查 |
| `src/harness/agent.ts`、`live.ts` | `pi.agent` 可按历史 fork；`pi.live` 只留当前状态，fork 时重新初始化 |
| `src/storage/sqlite/storage.ts`、`node.ts` | 整批写入数据库事务；Node facade 使用队列与 BEGIN IMMEDIATE，默认 WAL / NORMAL |
| `src/storage/jsonl/storage.ts` | sidecar 先写、主文件 marker 后写；恢复按已提交 marker 重建；默认 fsync 关闭 |
| `src/harness/types.ts`、`src/env/index.ts` | extension/registry、task、hook、tool、prompt section、环境和存储扩展；环境接口不是安全沙箱 |

## 恢复测试提供了什么证据

| 测试文件与测试位置 | 观察到的断言 |
| --- | --- |
| `test/harness-tasks-recovery.test.ts`，`resumes an intent/effect/outcome task…` | 转账服务在恢复后被调用两次，但按 key 去重后只生效一次；幂等性来自模拟服务 |
| `test/harness-generation-recovery.test.ts`，`resends a request…` / `converts a committed partial…` | 中断请求重新发送；已提交 partial 转成 aborted assistant entry；使用已保存的请求选项 |
| `test/harness-tools-recovery.test.ts`，`answers an unsafe tool…` / `reruns a tool only…` | unsafe 工具不自动重跑并返回部分输出；safe/safe 才重跑 |
| 同上，`reruns a safe tool with the environment…` | 恢复后的 cwd 可以不同；工具被取消选择时不再执行 |
| `test/harness-ownership.test.ts` | 前台取消传播、后台边界、等待取消、子 agent 在重启后复用同一 child 和 submission |
| `test/harness-lifecycle.test.ts`，`joins a task handler that ignores its signal…` | close 等待忽略取消信号的代码退出；不是强制终止 JavaScript |
| `test/session-documents.test.ts`，`poisons the Session…` | 存储结果未知时不发布候选状态，并阻止后续提交 |
| `test/sqlite-storage.test.ts`，`rolls SQL rows and sequence allocation back…` | SQL 行与序列号在一个事务内回滚 |
| `test/storage-runtime-boundary.test.ts` | 检查包入口及 portable storage 的源码依赖图不引入 Node 内建模块；不是 Cloudflare 部署测试 |

以上为阅读测试源码得到的覆盖说明，不是本次执行通过记录。

## 需要保留的限制

- 一个 storage 由一个进程独占；不提供分布式租约或跨进程 owner 锁。SQLite 自身的事务锁不等于 Harness 的多实例所有权协调。
- 提交原子性覆盖库内记录，不覆盖外部模型、文件、进程和网络副作用。副作用完成而结果未存储时仍有不确定窗口。
- `requestId` 只去重输入接收；同一 key 被复用时返回既有 submission，不能当作新内容的新请求。
- 模型请求可能重发；beforeRequest 会重新执行。保存了请求基础状态，不等于冻结任意 hook 的计算结果。
- registry、settings 与执行代码不持久化，重启要重新提供；安全重放也需检查代码和运行环境变化。
- JSONL 的 `fsync: true` 在写 marker 前刷新 sidecar；主文件刷新出现在回收路径。不能仅据这个选项宣称每次已返回提交都耐断电。
- SQLite 默认 WAL / NORMAL 的说明承诺进程崩溃恢复，允许主机故障或掉电丢失最新提交；持久性需要按部署环境验收。

## 来源指针

- [durable README](https://github.com/earendil-works/pi/blob/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/durable/README.md)
- [durable CHANGELOG](https://github.com/earendil-works/pi/blob/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/durable/CHANGELOG.md)
- [agent-core CHANGELOG](https://github.com/earendil-works/pi/blob/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/agent/CHANGELOG.md)
- [核心数据模型](https://github.com/earendil-works/pi/blob/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/durable/src/types.ts)
- [Harness 源码](https://github.com/earendil-works/pi/tree/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/durable/src/harness)
- [Session 源码](https://github.com/earendil-works/pi/tree/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/durable/src/session)
- [Storage 源码](https://github.com/earendil-works/pi/tree/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/durable/src/storage)
- [测试源码](https://github.com/earendil-works/pi/tree/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/durable/test)
- [设计说明](https://github.com/earendil-works/pi/blob/9b3c19da5cffc4c5e8b6bd74c45abc1ab6bfcd16/packages/durable/docs/spec.md)

整理页：[[wiki/topics/ai/pi-durable|Pi Durable：可恢复的 Agent 执行库]]。
