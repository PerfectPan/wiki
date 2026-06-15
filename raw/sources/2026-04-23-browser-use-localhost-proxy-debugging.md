# Browser-use / CDP localhost 代理排障记录

来源：`memory/2026-04-23.md`

## 原始事实

- 在一次 browser-use / Chrome remote debugging 排障中，页面正文最终可以通过 `browser-use state` 读取。
- 问题定位经验：涉及本地 CDP、Playwright、browser-use、Chrome remote debugging 的连接异常时，应先检查系统代理是否污染 `localhost` / `127.0.0.1`，再继续怀疑工具本身。
- 该经验来自一次真实排障后的复盘，不是官方文档结论。

## 可复用结论

当自动化工具需要连接本机调试端口，例如 Chrome DevTools Protocol 的 `http://127.0.0.1:<port>/json` 或 `ws://127.0.0.1:<port>/devtools/...` 时，系统代理、环境变量代理或客户端代理设置可能错误拦截本地环回流量。排障顺序应优先确认本地地址是否绕过代理。