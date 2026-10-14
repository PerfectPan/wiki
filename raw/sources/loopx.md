<!--
source: https://github.com/loopx-project/loopx/tree/4e994b11f83103b99342a3b0e589a93d6b526f5d
type: repo
fetched: 2026-10-13
note: body pre-fetched; direct fetch skipped
-->

# LoopX 双目标的公开来源核查

## 访问元信息

- 对象：`loopx-project/loopx` 的公开文章《从一次性 Agent 到长程控制面》。
- 首次访问日期：2026-10-13；复核日期：2026-10-14。
- 固定提交：`4e994b11f83103b99342a3b0e589a93d6b526f5d`。
- 范围：双重优化目标及子项的公开定义。

## 核查证据

- [L60–66][objective]：依次提出最大化 Agent 产出、最小化人的注意力投入；产出因素依次为模型能力、有效并行度、时间利用率、目标对齐程度。具体工作由底层 Harness 和模型执行。
- [L65][objective]：技术目标为“无干预跑稳，有干预跑好”，包括持续推进、等待、重新规划、自我修复、验收后停止，以及反馈进入后续状态。
- [L210–219][attention]：交互面应呈现产物、证据和待决定的选择，围绕关键进展汇报，合并重复事件，减少无变化时的打扰；人的判断聚焦方向与质量标准。
- [L216–234][parallel]：有效并行需要控制评审和协调负担，优先选择验收边界可分离的工作。

## 验证记录

- 使用 GitHub CLI `gh api` 读取文章的固定 `ref`，按上述行号复核保留内容。
- 整理页按双目标和子项排列为无序列表；没有增加工程检查表或成本模型。
- 这里只核查文档表述，未运行 LoopX 或复现效果测试。

整理页：[[wiki/syntheses/ai/agent-loop-control-boundaries|Agent 循环工作流的控制边界]]。

[objective]: https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/apps/presentation/site/public/blog/zh/from-one-shot-agents-to-long-horizon-control/index.html#L60-L66
[attention]: https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/apps/presentation/site/public/blog/zh/from-one-shot-agents-to-long-horizon-control/index.html#L210-L219
[parallel]: https://github.com/loopx-project/loopx/blob/4e994b11f83103b99342a3b0e589a93d6b526f5d/apps/presentation/site/public/blog/zh/from-one-shot-agents-to-long-horizon-control/index.html#L216-L234
