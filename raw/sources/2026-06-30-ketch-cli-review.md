# ketch CLI 代码试读摘要

来源：

- GitHub: https://github.com/1broseidon/ketch
- 试读 commit：`5e5a362` (`v0.9.5`, 2026-06-29)
- 试读时间：2026-06-30

## 原始事实

`ketch` 是一个 Go 写的单体 CLI，定位是面向 AI agent 和终端用户的 web search、code search、docs search、scrape、crawl 聚合工具。它不是独立搜索引擎，而是把多个外部后端封装在统一命令面后面。

命令面：

- `search`：Brave、DuckDuckGo、SearXNG、Exa
- `code`：grep.app MCP、Sourcegraph、GitHub Code Search
- `docs`：Context7
- `scrape`：网页抓取、Markdown 提取、raw HTML、CSS selector、JS browser fallback
- `crawl`：BFS / sitemap crawl、缓存、后台状态
- `browser`：安装或检查 headless browser
- `config`：输出有效配置和可用 backend
- `cache`、`version`：支持性命令

主要依赖：

- `spf13/cobra`：CLI 命令组织
- `go.etcd.io/bbolt`：本地缓存
- `PuerkitoBio/goquery`：HTML 查询
- `readeck/go-readability`：正文抽取
- `html-to-markdown`：HTML 到 Markdown
- `go-rod/rod`：浏览器渲染

核心实现观察：

- 顶层 command 只保留 `--json` 全局参数，`-b/--backend` 下沉到 `search`、`code`、`docs` 各自的 backend universe。
- 搜索后端通过 `Searcher` 接口隔离，CLI 层根据 backend 字符串选择具体 adapter。
- `scrape` 的主路径是 HTTP fetch -> JS shell 检测 -> 必要时 browser render -> readability 提取 -> Markdown 转换。
- JS shell 检测不仅看低可见文本，还看 Next.js App Router、React streaming、Vue、SvelteKit、Qwik、Astro 等 hydration / streaming marker。
- 抓取结果会记录来源类型：`http`、`http_shell`、`browser`。这样配置浏览器后，旧的 unrendered shell cache 可以被绕开。
- HTTP body 读取有 20 MiB 上限，避免异常页面撑爆进程。
- CLI 定义了面向 agent 的退出码：参数/校验 2，未找到 3，上游失败 4，前置条件缺失 5，取消 6。
- `search --scrape` 和多 URL `scrape --json` 对单个 URL 失败采用 warn-and-continue，适合批处理，但调用方需要检查 stderr 或结果数。

本地试用结果：

- `go test ./...` 通过。
- `go build` 通过。
- `search -b exa` 可用。
- `search -b ddg` 试用时出现 rate limited。
- `code -b sourcegraph` 可用。
- `code -b github` 可用，依赖本机 `gh` token。
- 默认 `code` 的 grep.app 后端试用时出现 504。
- `scrape` GitHub README、Go 文档页可用，输出较干净。
- Context7 docs 因未配置 API key 返回前置条件失败。
- macOS 上 `browser chrome` 不可用，因为 `chrome` 不在 PATH；配置完整路径 `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` 后，JS 渲染页抓取可用。
- 配置浏览器后，TokenReply pricing 这类 JS 渲染页面可以抓出内容；`--force-browser --select table` 可以直接抽出 Markdown 表格。

## 试读判断

`ketch` 的价值不在“搜索能力独家”，而在把 agent 常用的搜索、代码搜索、文档搜索、网页抽取、浏览器 fallback 等能力封成一个统一 CLI。它更像一个 agent 工具箱薄封装，而不是可直接替代现有 web search 的基础设施。

值得学习的是 CLI 架构和 agent-facing 设计：窄命令面、backend adapter、结构化输出、stderr/stdout 分离、退出码分类、抓取缓存来源标记、浏览器 fallback 的确定性语义。

不宜直接照搬的是对外部后端的稳定性假设。DDG、grep.app、Context7、Brave、Exa、GitHub、Sourcegraph 都有各自的 rate limit、token、API schema 和可用性边界。无人值守自动化如果使用类似聚合工具，必须在外层做 fallback、重试、结果数量校验和错误分类。
