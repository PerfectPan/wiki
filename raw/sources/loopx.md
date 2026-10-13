<!--
source: https://github.com/loopx-project/loopx/tree/4e994b11f83103b99342a3b0e589a93d6b526f5d
type: repo
fetched: 2026-10-13
note: body pre-fetched; direct fetch skipped
-->

# LoopX 双目标的公开来源核查

## 访问元信息

- 对象：`loopx-project/loopx` 的长程 Agent 产品目标与评价文档。
- 访问日期：2026-10-13。
- 固定提交：`4e994b11f83103b99342a3b0e589a93d6b526f5d`。
- 范围：以下三个公开文件的文档主张，不据此判断产品采用价值或实现效果。

## 核查证据

| 观察到的事实 | 证据位置 | 限制 |
| --- | --- | --- |
| 同时优化有效产出与获得产出所需的人类注意力；四因素为模型能力、有效并行度、时间利用率、目标对齐程度 | [公开博客 L60–66][objective] | 定性目标，未给出四因素乘积、权重或测量单位 |
| 无新事实时等待，路线失效时重新规划，验收满足后停止；人的反馈应成为后续可继承状态 | [公开博客 L65–66][objective]、[概念导读 L34–45][primer] | 设计目标，不是无人干预必然成功的保证 |
| 重要交付、路线决策和主要阻塞值得汇报；普通刷新与无变化巡检不应重复打断人 | [公开博客 L210–219][attention] | 减少打扰仍需保留产物、证据和必要选择 |
| 并行收益需考虑 review 与协调负担；工作应有共同目标和独立边界，优先在验收边界可分离的地方并行 | [公开博客 L216–234][parallel] | Agent 数量本身不能代表有效并行度；紧密耦合的修改可能由一位 Worker 完成更省 |
| 显式表示为 `project_reward = f(quantity, quality, token_cost, user_attention_cost)` | [Reward Model L11–21][reward] | 产品评价框架；未定义具体函数或权重，不是模型训练奖励函数或 benchmark 替代 |
| Quantity 统计有界交付物；Quality 看有用性、证据与返工，数据不足时使用粗标签 | [Reward Model L25–57][quality] | 聊天量不能替代交付；不据此制造精确评分 |
| Token Cost 观察模型或执行预算，token 不可得时可使用配额槽位、运行分钟数等替代记录 | [Reward Model L59–70][budget] | 应注明单位，先在同一项目或宿主集成内保证可比 |
| User Attention Cost 观察人的指导投入；需要判断时应询问，避免让用户充当调度器 | [Reward Model L72–85][human] | 与 token 是不同维度；没有给出两者固定换算率 |
| 模型负责推理与执行，长期状态还需保留目标、权限、证据与恢复信息；人工反馈须保留权限和证据边界 | [概念导读 L3–45][primer] | 博客四因素的首项原文是“模型能力”；同时检查 Agent-loop 的执行与验证支持，是整理页的工程化解释 |

## 验证记录

- 在本机使用 GitHub CLI `gh api` 读取三个文件的固定 `ref`，按行核对正文。
- 仅核查文档表述，未安装或运行 LoopX，未复现 benchmark，也未测量吞吐、token 节省或人的注意力节省。
- 整理页中的修复 PR 场景和检查问题属于基于这些公开材料的综合建议，不是上游实测案例。
- 这里不将产出四因素、产品评价四维或 token 预算合成为新的成本公式。

整理页：[[wiki/syntheses/ai/agent-loop-control-boundaries|Agent 循环工作流的控制边界]]。

[objective]: https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/apps/presentation/site/public/blog/zh/from-one-shot-agents-to-long-horizon-control/index.html#L60-L66
[attention]: https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/apps/presentation/site/public/blog/zh/from-one-shot-agents-to-long-horizon-control/index.html#L210-L219
[parallel]: https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/apps/presentation/site/public/blog/zh/from-one-shot-agents-to-long-horizon-control/index.html#L216-L234
[reward]: https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/docs/product/foundations/project-level-reward-model.md#L11-L21
[quality]: https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/docs/product/foundations/project-level-reward-model.md#L25-L57
[budget]: https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/docs/product/foundations/project-level-reward-model.md#L59-L70
[human]: https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/docs/product/foundations/project-level-reward-model.md#L72-L85
[primer]: https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/docs/development/control-plane-course/00-concept-primer.md#L3-L45
