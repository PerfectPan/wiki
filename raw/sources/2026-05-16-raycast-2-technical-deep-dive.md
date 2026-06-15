---
title: A Technical Deep Dive Into the New Raycast
source_url: https://www.raycast.com/blog/a-technical-deep-dive-into-the-new-raycast
ingested: 2026-05-16
type: article
---

# A Technical Deep Dive Into the New Raycast

## 来源事实摘录

Raycast 2.0 是 Raycast 自 2020 年发布以来最大的一次重写，也是首次同时运行在 macOS 和 Windows 上的版本。它从原先以 Swift/AppKit 为核心的 macOS 原生应用，转向一套自建 hybrid desktop 架构：平台原生宿主 + 系统 WebView + 共享 React/TypeScript 前端 + 长驻 Node 后端 + Rust 核心模块。

### 重写原因

- Raycast v1 起初是一个 macOS launcher，后来扩展成包含 AI Chat、Notes、extensions、sync、file search 等功能的生产力平台。
- 原架构开始限制后续功能：编译时间变长，AppKit 约束变多，深度 macOS 原生工程师也更难招聘。
- Windows 版本让团队必须重新思考跨平台架构；即使没有 Windows，Raycast 也认为原架构迟早要重构。

### 技术选型

Raycast 评估过 Electron、Tauri、自建 hybrid stack，以及 Flutter、Qt、React Native for Desktop、Swift 跨平台等路线。

- Electron：成熟、生态强，适合多数桌面应用；但 Raycast 对 OS 集成要求很深，包括全局快捷键、剪贴板、accessibility API、窗口管理、浮层、透明效果等。Electron 的 web/native 边界和 macOS 打包 Chromium 的成本不符合他们的控制需求。
- Tauri：同样在 native 控制力上不够，且当时成熟度不足，不适合押注公司级重写。
- 自建 hybrid stack：macOS 用 Swift/AppKit + WKWebView，Windows 用 C#/.NET 8/WPF + WebView2。这样保留平台 API 控制力，同时让 UI 和业务逻辑跨平台共享。

Raycast 明确说：这种方案不适合大多数桌面应用，因为要自己维护 Electron 已经提供的基础设施，包括 IPC、WebView、native shell、Node backend 之间的通信、调试和性能优化。

### 架构组成

- Host app：每个平台一个原生宿主。macOS 用 Swift/AppKit，Windows 用 C#/.NET 8/WPF。负责窗口、全局快捷键、菜单栏/tray、平台 API、加载 WebView、监管 Node 后端。
- Web frontend：一个 React + TypeScript 工程，按窗口构建 entry points，如 Launcher、AI Chat、Notes、Settings。
- Node backend：一个长驻 Node 进程，负责数据库访问、扩展运行时、长期服务和业务逻辑。产品功能大多在这一层和 web frontend 中开发。
- Rust core：用于性能和可移植性更敏感的部分，包括数据层、同步 schema、文件索引器。

多个 runtime 之间通过平台 message handlers 和 stdio transport 通信；接口集中声明，并为各端生成 typed clients，以获得跨 Swift/C#/Node/WebView/Rust 的编译期约束。

### 文件索引器

v1 文件搜索依赖 Spotlight metadata，覆盖和跨平台能力受限。v2 用 Rust 重写文件索引器，直接扫描文件系统并通过文件系统事件保持索引更新。

Windows 上常规遍历 NTFS 太慢，所以 Raycast 做了专门的 NTFS scanner，直接读取 Master File Table，把全盘索引从分钟级压到秒级。

### Native feel 的细节

Raycast 对 hybrid app 的判断标准不是“看起来像 native”，而是用户不知道技术栈时会不会认为它就是普通 Mac app。文章强调：他们不是“web app 加一点 native hook”，而是“native app 用 web 做 UI”。

具体做法包括：

- 不在交互控件上使用 `cursor: pointer`，因为桌面应用通常不这么做。
- macOS 上多数控件不做 web 式 hover highlight。
- Settings 打开为独立 native window，而不是 web modal/side panel。
- Popover 和 tooltip 用 native window 渲染，可以超出 WebView/window 边界。
- macOS Tahoe 采用 Apple 的 Liquid Glass material。
- 重点消除 WebView 视图切换、打开、窗口 resize 时的闪烁和空白帧。

### WebKit / WebView2 绕路

WebKit 为浏览器场景设计，对频繁显示/隐藏的 launcher 有不合适的默认假设。Raycast 做了不少 workaround：

- WebKit 会在认为 view 不可见时 throttle `requestAnimationFrame`、CSS animation 和 timer。Raycast 通过把窗口 order front 但设置 `alphaValue = 0`，并禁用 occlusion detection，避免显示前渲染被节流。
- compact 到 full-size 展开时，为避免先前不可见区域空白，WKWebView frame 始终保持 expanded size，让内容预先渲染在窗口可见范围之外。
- WebKit 在 animated window resize 时会暂停绘制，Raycast 覆盖 `NSWindow.setFrame`，改用 implicit Core Animation，让 WebView 在 resize 时继续绘制。
- 使用 `_doAfterNextPresentationUpdate` 确认 WebView 完成绘制后再显示窗口，避免 stale/empty content 闪一下。
- Emoji picker 曾因字体 fallback 很慢，最后通过启动时预热 emoji font 解决。
- 内部支持运行时切换 WebKit Feature Flags，用于解锁 60 FPS 上限和启用 `requestIdleCallback`。

Windows 侧 WebView2/Chromium 也需要处理 acrylic blur、custom title bar、多窗口环境、初始化参数、避免白矩形闪烁，以及未聚焦窗口的 throttling。

### 内存和性能

Raycast 承认 v2 比 v1 更吃内存：

- v1：典型使用后约 200–300 MB。
- v2：类似场景约 350–450 MB。
- v2 hidden main window 粗略拆分：
  - WebView WebContent：约 120–200 MB
  - Node.js backend：约 150–200 MB
  - Native Swift shell：约 40 MB
  - WebKit GPU process：约 18 MB
  - WebKit Networking：约 12 MB

文章强调 Activity Monitor 的进程数字不能简单相加，因为 macOS 有 compressed memory、clean/dirty pages、shared frameworks 等机制；真正该看的是 Memory Pressure。Raycast 同时跟踪 `phys_footprint`，并继续优化 lazy loading、icon/image、V8 heap 等。

性能上 v2 在文件搜索和 rich text rendering 上更强。文件搜索由 Rust indexer 直接支持；AI Chat、Markdown、code block 和长文本渲染则更适合 WebKit。

### 取舍

收益：

- 开发速度：hot reload 让 UI 改动低于 1 秒可见，不再频繁重新编译 Swift target。
- 一套团队，两端平台：多数产品功能在 shared web frontend 和 Node backend 中完成。
- 招聘：React/TypeScript/Node 工程师比深 AppKit 工程师更容易找。
- richer UI：富文本编辑、Markdown、复杂布局和动画更容易构建。
- extensions 简化：Node 随 app 打包，扩展不再需要用户首次安装时另下 Node；内部功能和扩展开发栈趋同。

成本：

- 内存 baseline 更高。
- 四套 runtime 带来调试和维护复杂度。
- Windows 环境碎片化，WebView2 版本、硬件、显示配置差异更大。
- 一些 AppKit 免费提供的 native 行为，如 accessibility、drag and drop、IME 边界，需要在 WebView 中显式补齐。
- 为控制内存，v2 更积极销毁 inactive windows，冷启动窗口可能有短延迟，需要在 warm grace period 和内存回收之间找平衡。

## 初步综合判断

这篇文章的核心价值不是“Raycast 选了 WebView”，而是展示了一个成熟桌面产品如何在 native feel、跨平台复用、招聘、开发速度和内存 baseline 之间做工程取舍。

对大多数桌面应用，Raycast 自己也承认 Electron 仍然更合适。Raycast 的特殊性在于它高度依赖 OS 集成和窗口行为细节，同时又有大量可共享的 UI/业务逻辑和扩展生态，因此才值得自建 hybrid stack。

可复用教训：

1. 桌面 hybrid 架构不是二选一问题，而是控制边界问题：哪些必须 native，哪些可以 web，哪些应该放 shared backend/core。
2. “像 native”主要不是视觉，而是行为：焦点、hover、popover、resize、IME、accessibility、渲染时机这些小边界决定质感。
3. WebView 不是免费抽象。要达到高品质，需要理解并绕开 WebKit/WebView2 的浏览器默认假设。
4. 内存增长可以接受，但必须可测量、可解释、可持续优化；不能用“现代机器内存大”糊弄过去。
5. 对组织来说，技术栈选择同时是招聘、迭代速度和产品覆盖面的选择，不只是运行时性能选择。

## 对话补充：Electron 与自建 WebView 的边界

这次讨论里进一步澄清了一点：Raycast 不用 Electron，并不是因为 Electron 完全做不了全局快捷键、剪贴板、窗口置顶、透明窗口或 native menu。Electron 可以覆盖很多系统能力，复杂场景也可以通过 native addon、多 BrowserWindow、frameless window、透明窗口等方式绕出来。

真正差别在控制边界：

- Electron 给的是一套通用桌面 runtime：Chromium renderer + Electron native binding + Node 集成。
- Raycast 2.0 要的是自己掌握平台原生壳：macOS 用 Swift/AppKit + WKWebView，Windows 用 C#/WPF + WebView2。
- 对 Raycast 这种系统入口级工具，窗口、焦点、浮层、快捷键、透明、accessibility、IME、拖拽等细节越靠近系统边界，越适合直接放在原生壳里掌控。

所以更准确的判断不是“Electron 给不了”，而是：Electron 给的是通用抽象；Raycast 要的是特例控制权。逃逸到 native 的地方越多，自建 native shell 的收益越明显。
