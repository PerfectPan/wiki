---
title: Raycast
type: topic
category: tooling
created: 2026-04-12
updated: 2026-05-16
tags:
  - raycast
  - desktop-app
  - webview
  - productivity
source_refs:
  - raw/sources/Raycast.md
  - raw/sources/2026-05-16-raycast-2-technical-deep-dive.md
  - https://www.raycast.com/blog/a-technical-deep-dive-into-the-new-raycast
---
# Raycast

## 摘要

Raycast 是一个以键盘优先为核心的桌面生产力工具。它从 macOS launcher 演进为包含 AI Chat、Notes、扩展、同步、文件搜索、窗口管理等能力的平台。Raycast 2.0 为支持 macOS 和 Windows，改成了自建 hybrid desktop 架构：平台原生宿主负责 OS 集成，WebView 承载共享 UI，Node 负责共享业务逻辑，Rust 负责性能敏感模块。

## 常用能力

- 窗口管理：把程序移动到另一个显示器、快速左半屏/右半屏等。
- 常用工具：查看 IP、测速、颜色提取、翻译、时区转换、货币转换。
- Quicklink：快速打开指定网站或带关键词搜索，例如从 Raycast 直接发起 bilibili 搜索。
- Snippet：可用于常用文本或代码模板。
- Favorite / 快捷键：高频命令可以添加快捷键或收藏。
- Raycast AI：深度集成自然语言操作和应用上下文，但需要注意授权边界和文件访问范围。

## Raycast 2.0 技术架构

Raycast 2.0 的重点不是简单从 native 改成 web，而是把不同职责拆到合适的层：

- **Host app**：macOS 用 Swift/AppKit，Windows 用 C#/.NET 8/WPF。负责窗口、全局快捷键、菜单栏或 tray、平台 API、加载 WebView、监管 Node 后端。
- **Web frontend**：一个 React + TypeScript 工程，按 Launcher、AI Chat、Notes、Settings 等窗口构建 entry points，两端共享 UI 代码。
- **Node backend**：一个长驻 Node 进程，负责数据库访问、扩展运行时、长期服务和业务逻辑。多数产品功能在这一层和 web frontend 中开发。
- **Rust core**：负责性能和可移植性更敏感的模块，包括数据层、同步 schema 和文件索引器。

这些 runtime 通过平台 message handlers 和 stdio transport 通信，并通过集中声明接口、生成 typed clients 来降低跨 Swift/C#/Node/WebView/Rust 的边界错误。

## 为什么不用 Electron 或 Tauri

Raycast 认为 Electron 对多数桌面产品仍然是合理选择：成熟、生态强、能显著降低基础设施成本。但 Raycast 自身高度依赖 OS 深度集成，例如全局快捷键、剪贴板、accessibility API、窗口管理、浮层、不抢焦点的 panel、透明效果等。

它最后选择自建 native shell + system WebView，是为了获得：

- macOS 上使用系统 WKWebView，而不是额外打包 Chromium。
- 对窗口、浮层、透明、焦点和平台 API 的细粒度控制。
- 一套共享 React/TypeScript UI 与 Node 业务逻辑，降低跨平台功能重复开发。
- 必要时随时退回 native 实现关键交互。

代价也明确：需要自己维护 Electron 已经提供的大量基础设施，包括 IPC、WebView、native shell、Node backend 之间的调试、性能和跨平台差异。

## Native feel 的关键

Raycast 的判断标准不是“看起来像 native”，而是用户不知道技术栈时会不会以为它就是普通 Mac app。文章里一个关键表述是：Raycast 不是“web app 加一点 native hook”，而是“native app 用 web 做 UI”。

关键细节包括：

- 不在桌面控件上使用 web 式 `cursor: pointer`。
- macOS 上多数控件不做 web 式 hover highlight。
- Settings 打开为独立 native window，而不是 web modal 或 side panel。
- Popover 和 tooltip 用 native window 渲染，可以越过 WebView/window 边界。
- 处理 WebKit/WebView2 在隐藏窗口、resize、展开、首次显示时的 throttling、空白帧和闪烁。
- IME、accessibility、drag and drop 等原生框架免费提供的行为，在 WebView 架构下需要显式补齐。

## 文件索引器

Raycast v1 文件搜索依赖 Spotlight metadata，能力受限且不适合 Windows。v2 用 Rust 重写文件索引器，直接扫描文件系统并用文件系统事件保持索引更新。

Windows 上常规遍历 NTFS 太慢，因此 Raycast 做了专门的 NTFS scanner，直接读取 Master File Table，把全盘扫描压到秒级。

## 内存与性能取舍

Raycast 2.0 承认内存高于 v1：

- v1：典型使用后约 200–300 MB。
- v2：类似场景约 350–450 MB。
- v2 hidden main window 的主要成本来自 WebView WebContent 和 Node backend。

这说明 hybrid desktop 架构确实带来更高 baseline，但 Raycast 的处理方式是把它变成可测量、可解释、可优化的问题：跟踪 `phys_footprint`，优化 lazy loading、icon/image、V8 heap，并用 Memory Pressure 而不是简单进程数字判断真实系统压力。

v2 同时在部分场景更快：文件搜索由 Rust indexer 直接支持；AI Chat、Markdown、code block 和长文本渲染则受益于 WebKit 的文本布局能力。


## 对话补充：Electron 与自建 WebView 的边界

这次讨论里进一步澄清了一点：Raycast 不用 Electron，并不是因为 Electron 完全做不了全局快捷键、剪贴板、窗口置顶、透明窗口或 native menu。Electron 可以覆盖很多系统能力，复杂场景也可以通过 native addon、多 BrowserWindow、frameless window、透明窗口等方式绕出来。

真正差别在控制边界：

- Electron 给的是一套通用桌面 runtime：Chromium renderer + Electron native binding + Node 集成。
- Raycast 2.0 要的是自己掌握平台原生壳：macOS 用 Swift/AppKit + WKWebView，Windows 用 C#/WPF + WebView2。
- 对 Raycast 这种系统入口级工具，窗口、焦点、浮层、快捷键、透明、accessibility、IME、拖拽等细节越靠近系统边界，越适合直接放在原生壳里掌控。

所以更准确的判断不是“Electron 给不了”，而是：Electron 给的是通用抽象；Raycast 要的是特例控制权。逃逸到 native 的地方越多，自建 native shell 的收益越明显。

## 可复用教训

- 桌面 hybrid 架构的核心不是 native vs web，而是控制边界：哪些必须 native，哪些可以 web，哪些适合 shared backend/core。
- “像 native”主要不是视觉，而是行为：焦点、hover、popover、resize、IME、accessibility、渲染时机这些小边界决定质感。
- WebView 不是免费抽象；高品质桌面体验需要理解并绕开 WebKit/WebView2 的浏览器默认假设。
- 内存增长可以接受，但必须可测量、可解释、可持续优化，不能用“现代机器内存大”糊弄过去。
- 技术栈选择也是组织选择：招聘、迭代速度、跨平台覆盖和维护成本都在里面。

## 风险提醒

- Raycast AI 和扩展生态可能接触本地文件、剪贴板、应用上下文等敏感信息，应注意权限范围和 key 泄露风险。
- 自建 hybrid stack 只有在产品确实需要深 OS 集成、强 native feel 和跨平台共享时才值得；普通桌面应用直接用 Electron 往往更稳。

## 来源指针

- `raw/sources/Raycast.md`
- `raw/sources/2026-05-16-raycast-2-technical-deep-dive.md`
- <https://www.raycast.com/blog/a-technical-deep-dive-into-the-new-raycast>
