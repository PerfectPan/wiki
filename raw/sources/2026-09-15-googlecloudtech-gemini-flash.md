# Google Cloud Tech：Gemini Flash 与 Claude 协作

- 原文：Put Claude Fable 5.1 and Gemini 3.8 Flash on the same team
- 发布账号：Google Cloud Tech；署名：Alan Blount
- 来源：https://x.com/GoogleCloudTech/article/2099507349828350285
- 阅读日期：2026-09-15
- 本文件为正文阅读摘要，不是全文副本。通过 browser-harness 读取；未执行文中的配置或评测命令。

## 文章建议

文章以 Gemini Flash 负责快速执行、Claude 负责复杂规划为例，介绍统一接入、实际任务对照评测、模型分工和任务价值判断。

第三节建议为 Gemini 提供少量聚焦工具及严格的参数定义，并提供 `ask_for_help(reason, failed_attempts, context)` 入口，在歧义、不可逆操作或连续失败时升级。复杂任务可以先由 Claude 规划，再交给 Gemini 执行，由 Claude 检查结果。

第二节用检查 Git 分支和设计数据库迁移两个任务说明不同任务需要分别比较；作者也明确指出，这只是示例，需要使用自己的任务验证。第三节提醒，自动路由可能缺少判断信号，选错后重新执行会增加成本和延迟，因而建议按明确的任务边界组织协作。

## 收录判断

收录 Gemini 的任务范围、工具配置、求助入口和规划执行协作方式。工具数量、升级次数、性能倍数及请求处理比例只视为例子；模型价格、接入命令和平台设置未独立核验，不纳入操作指南。

## 评测工具补充

文章第二节使用 Promptfoo，通过 `exec:` 分别调用 OpenCode 的 Gemini 与 Claude 配置，运行同样的两个任务，再用 `promptfoo eval -c promptfooconfig.yaml --no-cache` 执行对照。展示的配置包含任务、命令及超时时间，没有质量断言。

因此收录时需要区分“组织运行”和“验证质量”：文章演示了前者，后者仍需明确完成标准。同时，外部命令的指标回传也需要接入方确认，不能把模型用量和成本视为自动可得。

- [Promptfoo 仓库](https://github.com/promptfoo/promptfoo)
- [Custom Scripts 文档](https://www.promptfoo.dev/docs/providers/custom-script/)

## ROI 粗略估算

文章第四节讨论任务收益与投入，没有给出完整的 ROI 统计。按它的思路，可以粗略写成下面的公式；这是阅读整理，不是原文公式或实测结果：

```text
ROI ≈（总收益 − 总投入）÷ 总投入 × 100%

总收益 ≈ 节省工时 × 单位工时价值
       ＋ 更快交付带来的额外价值
       ＋ 减少错误和故障所避免的预期损失

总投入 ≈ 模型调用费用（含重试和多模型交接）
       ＋ 团队学习、开发接入及运行维护成本
       ＋ 人工复核和返工成本
```

说白了，就是“用了 Agent 以后，多得到的价值减去多花的钱，再除以多花的钱”。与不用 Agent 的同一任务基线比较，收益和投入要按同一周期、同一货币口径估算，总投入要大于零。节省工时、交付提速和减少返工可能重叠，不要重复计算；复核和返工若已从节省工时中扣除，就不要再计入投入。难以折算的收益单独说明，不硬凑金额。
