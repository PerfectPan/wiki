---
title: browser-use 本地 CDP 连接为什么会被系统代理劫持
type: synthesis
category: ai
status: active
created: 2026-04-23
updated: 2026-04-23
tags:
  - browser-use
  - cdp
  - proxy
  - playwright
  - debugging
source_refs:
  - memory/2026-04-23.md
  - https://github.com/PerfectPan/wiki/pull/3
---
# browser-use 本地 CDP 连接为什么会被系统代理劫持

## 问题

当 `browser-use` 在本机启动 Chrome 并通过 CDP 连接本地调试端口时，为什么会出现看起来像工具本身坏掉的错误，例如 `connecting through a SOCKS proxy requires python-socks` 或 `did not receive a valid HTTP response`？

## 简答

高概率不是 `browser-use` 本身坏了，而是系统代理把本应直连的 `127.0.0.1` / `localhost` WebSocket 连接也接管了。`browser-use` 底层依赖会读取系统代理设置，如果没有显式排除本地地址，连接 `ws://127.0.0.1:<cdp-port>` 时就可能错误走代理，导致 CDP 握手失败。

## 综合结论

- 这类问题的误导性很强，因为表面现象往往像是工具链缺依赖、版本不兼容，或者 Chrome 没正常启动。
- 这次排查里，确实先后出现了几个“假线索”：
  - `browser-use` 未安装；
  - Python 3.14 下有 event loop 兼容问题；
  - 安装后报出与 SOCKS 相关的错误；
  - 后续又报 `did not receive a valid HTTP response`。
- 但真正的根因并不在这些表层现象里，而在系统代理配置。排查中可以看到本机代理信息里存在：
  - `http -> http://127.0.0.1:7890`
  - `https -> http://127.0.0.1:7890`
  - `socks -> http://127.0.0.1:7890`
- `browser-use` 底层使用的 HTTP / WebSocket 组件会读取这些代理配置；如果本地地址没有被 `NO_PROXY` / `no_proxy` 排除，那么即使目标是 `ws://127.0.0.1:<cdp-port>`，连接也可能被错误转发给代理。
- 一旦发生这件事，现象就会非常混乱：
  - 某些组件会误以为自己正在走 SOCKS 代理，于是报缺 `python-socks`；
  - 某些组件会直接收到代理返回的非预期响应，于是报 WebSocket / HTTP 握手无效；
  - 排查者容易误判为 `browser-use`、Playwright、Chrome 或 Python 本身有问题。
- 这类问题最稳的处理顺序应该是：
  1. 先确认 Chrome 本地调试端口本身可用；
  2. 再检查系统代理是否污染了 localhost / 127.0.0.1；
  3. 只有在本地地址已明确绕过代理后，才继续排查工具和版本兼容性。
- 实际可用的修复方式是，在运行 `browser-use` 之前显式设置：
  - `NO_PROXY=127.0.0.1,localhost`
  - `no_proxy=127.0.0.1,localhost`
- 一旦绕过本地代理，这次的 `browser-use open` 与 `browser-use state` 就恢复正常，说明关键瓶颈不是工具能力，而是本机网络环境。

## 未决问题

- 这条经验目前还是通过会话排查沉淀出来的，还没有进一步抽象成统一的 shell 包装或启动脚本。
- 如果未来频繁使用 `browser-use`、Playwright、或其他依赖本地 CDP 的工具，可能需要一个默认带 `NO_PROXY` 的本地启动约定，避免重复踩坑。
- 还可以进一步总结成更广义的规则：凡是本地调试端口、回环地址、Unix socket 到 TCP 桥接这类链路，都应优先排查系统代理污染，而不是先怪应用层。

## 来源指针

- `memory/2026-04-23.md`
- `https://github.com/PerfectPan/wiki/pull/3`
