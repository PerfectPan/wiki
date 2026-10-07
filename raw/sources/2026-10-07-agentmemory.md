# agentmemory 源码核对

- 访问日期：2026-10-07。
- 官网：<https://www.agent-memory.dev/>。
- 官网指向的仓库：<https://github.com/rohitg00/agentmemory>。
- 固定提交：`007a1a7fe8646a03d8652eb0712400cc6f0fcca3`。
- 范围：只读源码、README 与评测报告；未运行服务、采集会话或复现评测。

## 入口、模型与数据流

| 证据 | 核对结果 |
| --- | --- |
| [src/index.ts](https://github.com/rohitg00/agentmemory/blob/007a1a7fe8646a03d8652eb0712400cc6f0fcca3/src/index.ts) | 注册 iii worker、采集与检索函数、REST/MCP、viewer，组装 KV 与索引。 |
| [src/types.ts](https://github.com/rohitg00/agentmemory/blob/007a1a7fe8646a03d8652eb0712400cc6f0fcca3/src/types.ts) | `CompressedObservation` 关联 session、事实、文件和来源；长期 `Memory` 有版本、supersedes、sourceObservationIds 等字段。 |
| [capture.ts](https://github.com/rohitg00/agentmemory/blob/007a1a7fe8646a03d8652eb0712400cc6f0fcca3/src/functions/capture.ts) | capture inbox 保存待处理事件；调用 observe，按事件身份去重，失败可以进入 retrying/dead 状态。 |
| [observe.ts](https://github.com/rohitg00/agentmemory/blob/007a1a7fe8646a03d8652eb0712400cc6f0fcca3/src/functions/observe.ts) | 保存 observation；逐条生成式压缩需显式启用，默认生成不调用 LLM 的检索表示。 |
| [state/kv.ts](https://github.com/rohitg00/agentmemory/blob/007a1a7fe8646a03d8652eb0712400cc6f0fcca3/src/state/kv.ts) | `StateKV` 经 iii `state::get/set` 等调用管理状态，支持 file/redis 配置；不能把它概括成纯 Markdown 文件库。 |
| [search.ts](https://github.com/rohitg00/agentmemory/blob/007a1a7fe8646a03d8652eb0712400cc6f0fcca3/src/functions/search.ts) | 主召回存在关键词和可选向量路径；索引维护与记忆记录是不同职责。 |
| [hybrid-search.ts](https://github.com/rohitg00/agentmemory/blob/007a1a7fe8646a03d8652eb0712400cc6f0fcca3/src/state/hybrid-search.ts) | 混合检索可组合 BM25、向量与图；效果取决于 provider、向量和图数据是否存在。 |

## 默认与评测

[README](https://github.com/rohitg00/agentmemory/blob/007a1a7fe8646a03d8652eb0712400cc6f0fcca3/README.md) 区分 keyless 关键词召回与显式启用的本地 embedding；后者首次下载 `all-MiniLM-L6-v2`，之后在本机推理。MCP 接入、hook 自动采集和会话启动注入是不同能力，必须分别验证。

[LongMemEval 报告](https://github.com/rohitg00/agentmemory/blob/007a1a7fe8646a03d8652eb0712400cc6f0fcca3/benchmark/LONGMEMEVAL.md) 的 95.2% 是 500 道题上的 `recall_any@5`：前五个结果中是否出现任一 gold session。报告使用 BM25 与本地向量，没有答案生成或 judge，因此不能解读为端到端问答准确率，也不是默认 keyless 配置的成绩。

## 验证入口与限制

阅读 `test/capture-durable.test.ts` 的重复事件、并发和重启重放案例，测试用 mock KV；定位到 `test/hybrid-search.test.ts`、`test/agent-isolation-search.test.ts`。未运行这些测试，未验证实际崩溃后的磁盘恢复。

本地存储与不向外发送内容是不同问题：配置云 provider 后，相关调用可能出网；被召回到 coding agent 的内容还会进入该 agent 的模型请求。自动采集也需要另行确定项目范围、保留时间、脱敏和删除行为。
