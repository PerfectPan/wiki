---
title: 聚合型 Agent CLI 的架构设计观察
description: 从 ketch 代码试读中提炼聚合型 agent CLI 的命令边界、后端抽象、抓取链路和可靠性设计启发。
type: synthesis
category: tooling
status: seed
created: 2026-06-30
updated: 2026-06-30
timestamp: 2026-06-30
tags:
  - cli
  - agent-tools
  - scraping
  - search
source_refs:
  - raw/sources/2026-06-30-ketch-cli-review.md
  - https://github.com/1broseidon/ketch
resource:
  - raw/sources/2026-06-30-ketch-cli-review.md
  - https://github.com/1broseidon/ketch
---
# 聚合型 Agent CLI 的架构设计观察

## 问题

面向 agent 的聚合型 CLI，如果只是把多个搜索、抓取、文档和代码查询后端包在一起，哪些设计仍然值得学习？哪些部分不应该被误判为稳定基础设施？

## 简答

聚合型 agent CLI 的核心价值不在“拥有独家能力”，而在把外部后端和脏的网页抽取流程包装成稳定、可组合、可解析的工具边界。命令面要窄，后端要 adapter 化，输出要机器可读，失败语义要清楚；真正的可靠性不能靠单个 backend，而要靠外层 fallback、重试和结果校验。

## 源码案例：ketch

`1broseidon/ketch` 是一个 Go 写的单体 CLI。它把 web search、code search、docs search、scrape 和 crawl 放到一个二进制里，面向 AI agent 和终端用户调用。

它不是搜索引擎，也不是完整 agent 框架。更准确的定位是：把多个不稳定但有用的外部能力封成一个统一命令面，让 agent 可以通过 shell 调用获得搜索结果、代码片段、文档片段或网页 Markdown。

## 命令边界

`ketch` 的命令划分比较克制：

- `search` 处理 web search，并可选择 `--scrape` 把结果页正文抓下来。
- `code` 处理开源代码搜索。
- `docs` 处理库文档搜索。
- `scrape` 处理 URL 到 Markdown / raw HTML / selector extraction。
- `crawl` 处理小规模站点抓取。
- `browser`、`config`、`cache`、`version` 是支撑命令。

这里的启发是：聚合工具可以宽，但单个命令的职责要窄。`search`、`code`、`docs` 都叫搜索，但它们的 backend universe 不同，所以 `-b/--backend` 被放在各自子命令下，而不是做成全局 flag。这避免了一个全局参数在不同命令里产生歧义。

## 后端抽象

聚合型 CLI 最容易犯的错，是把多个 provider 的差异泄漏到调用者。`ketch` 的基本做法是：

- CLI 层只解析命令参数和选择 backend。
- 每一类能力定义自己的接口，例如 web search 的 `Searcher`。
- Brave、DuckDuckGo、SearXNG、Exa、Sourcegraph、GitHub、Context7 等都作为 adapter。
- token 获取、rate limit、上游错误和 schema 解析留在 adapter 内部。

这个结构的好处是调用面统一，坏处是统一界面可能掩盖 backend 的稳定性差异。实际试用里，DDG 会 rate limit，grep.app 会 504，Context7 需要 API key，GitHub 需要 token，Exa 和 Sourcegraph 又有自己的上游依赖。外层自动化不能只看“命令成功存在”，还要知道每个 backend 的失败模式。

## 抓取链路

`scrape` 是这类工具里最值得学习的部分。成熟的网页抽取不是简单 `curl | readability`，而是一条带判断和降级的流水线：

1. HTTP fetch。
2. 限制 body 大小，避免异常页面拖垮进程。
3. 解析 HTML，判断是不是 JS shell。
4. 如果像 React / Next.js / Vue / SvelteKit / Qwik / Astro 这类客户端渲染页，尝试 browser render。
5. 用 readability 抽正文。
6. 转 Markdown。
7. 支持 selector extraction、raw HTML、trim、max chars 等 agent 友好的输出控制。

更关键的是缓存要记录来源。`ketch` 把抓取结果标为 `http`、`http_shell` 或 `browser`。这样未配置浏览器时抓到的 JS 空壳不会长期污染缓存；后续配置浏览器后，可以绕开旧的 `http_shell` 缓存重新渲染。这是一个很小但很实际的可靠性设计。

## Agent-facing 输出协议

聚合型 CLI 要给 agent 用，不能只考虑人类终端体验。比较稳的输出协议至少包括：

- `--json` 输出结构化结果。
- `--minimal` 或类似模式用于管道。
- 机器结果走 stdout，warning 和进度走 stderr。
- 支持 `--max-chars`，避免一次抓取塞爆上下文。
- 支持 `--trim`，把 Markdown 装饰降到更适合模型读取的文本。
- 支持明确 exit code，而不是所有错误都 exit 1。

`ketch` 把参数错误、未找到、上游失败、前置条件缺失、取消分别映射成不同退出码。这个设计对脚本和 agent 很有价值，因为调用方可以把“缺 API key”和“网络后端失败”分开处理。

## 可靠性边界

`ketch` 也暴露了聚合工具的天然边界：聚合不是可靠性本身。

本地试用中：

- DDG 搜索出现 rate limit。
- grep.app code search 返回 504。
- Context7 docs 因没有 API key 不可用。
- macOS 上文档中的 `browser chrome` 不一定能工作，需要配置完整 Chrome binary path。
- 多 URL scrape 和 `search --scrape` 对单个 URL 失败会 warning 后继续，适合批处理，但调用方必须检查 stderr 或结果数量。

因此这类工具适合作为“可组合零件”，不适合作为无人值守自动化的唯一信息源。真正接入自动化时，外层应该负责：

- backend fallback；
- retry / backoff；
- token 和成本边界；
- 输出数量校验；
- stderr warning 收集；
- browser 路径和运行环境探测；
- 关键源的二次校验。

## 可复用设计原则

- 命令按能力分层，不按 provider 分层。用户应该调用 `search`、`code`、`scrape`，而不是直接面对一堆 provider 命令。
- backend 是 adapter，不是产品边界。provider 可以换，CLI 协议要稳定。
- 默认路径要快，复杂路径要显式。例如静态页走 HTTP，JS 页再上 browser；`--force-browser` 应该明确失败，而不是静默回落。
- 缓存要带 provenance。缓存命中不只取决于 URL，也取决于内容来源和抽取方式。
- partial failure 要可见。批处理可以继续，但不能让 agent 误以为全部成功。
- 面向 agent 的 CLI 要优先设计机器协议，而不是只优化漂亮的终端输出。

## 不应照搬的地方

- 不要把外部搜索后端的不稳定包装成“稳定搜索能力”。
- 不要默认把 provider token 明文写入宽权限配置文件。
- 不要用没有 fallback 的单 backend 承载定时任务。
- 不要把 browser 渲染当成默认路径；它慢、重、环境敏感，应该作为明确降级或 escape hatch。
- 不要因为一个工具同时支持 search、code、docs、scrape、crawl，就把它误认为完整 agent 平台。

## 与现有理解的关系

这页补充的是工具层设计观察，和 [[wiki/syntheses/ai/Agent-native 生成型 CLI 的产物协议|Agent-native 生成型 CLI 的产物协议]] 相邻但不相同。

前者关注生成型 CLI 如何交付文件产物；这里关注聚合型 CLI 如何封装外部查询、网页抽取和不稳定后端。两者共同点是：对 agent 来说，CLI 的价值不在“命令能跑”，而在稳定输入、稳定输出、清楚失败语义和可组合边界。

## 来源指针

- `raw/sources/2026-06-30-ketch-cli-review.md`
- https://github.com/1broseidon/ketch
