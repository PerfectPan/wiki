# Taste / TasteLab 收录核查

- 来源：https://www.tastelab.xyz/；https://github.com/senlindesign/taste-skill
- 访问日期：2026-10-07
- 源码提交：`6dce223f2f5665d3636ca9a44ec3a7aa1322a9b8`
- 对象：仓库中的 `taste` skill；不是调用托管设计服务。

## 核查事实

- [SKILL.md](https://github.com/senlindesign/taste-skill/blob/6dce223f2f5665d3636ca9a44ec3a7aa1322a9b8/SKILL.md) 定义从网页 URL 出发的流程：浏览器截图与 DOM 提取、测量、归纳规则、推断设计取舍、审阅后输出 `{domain}.md` 与 `{domain}.json`。要求 Playwright MCP；可选导出到编辑器或 agent 的规则文件。
- [extract.js](https://github.com/senlindesign/taste-skill/blob/6dce223f2f5665d3636ca9a44ec3a7aa1322a9b8/references/extract.js#L1-L100) 包含实际 DOM / computed style 提取逻辑，区分整页样式采样与视口内几何采样，并设元素数量上限；不是只有角色提示词。
- [step3-taste.md](https://github.com/senlindesign/taste-skill/blob/6dce223f2f5665d3636ca9a44ec3a7aa1322a9b8/references/step3-taste.md) 要求每条设计取舍附测量依据与可行的另一选择；[step4-observer.md](https://github.com/senlindesign/taste-skill/blob/6dce223f2f5665d3636ca9a44ec3a7aa1322a9b8/references/step4-observer.md) 再剔除通用、无证据或矛盾的描述。设计者当时的实际意图仍是推断，页面测量不能直接证明动机。
- SKILL 的 Self-audit 要求实际执行用词扫描、章节计数与 JSON 解析；[evals.json](https://github.com/senlindesign/taste-skill/blob/6dce223f2f5665d3636ca9a44ec3a7aa1322a9b8/evals/evals.json) 列出三个站点案例及检查断言，未见配套的自动运行脚本。Observer 允许只保留两条有依据的原则，而 eval 断言要求至少三条，两处标准尚不一致。
- [README](https://github.com/senlindesign/taste-skill/blob/6dce223f2f5665d3636ca9a44ec3a7aa1322a9b8/README.md#L1-L7) 有 MIT 标记并链接 `LICENSE`，但该提交的文件树中没有对应许可文件。

## 收录判断与未测试项

按“可参考”收录：有明确交付文件、数值依据、浏览器采样代码和检查步骤，适合学习“先测量，再解释取舍”的流程；需保留设计意图的推断性质，并核对检查标准和许可缺口。未安装 skill、修改任何 agent 配置、执行提取脚本或运行完整示例。
