# NameThatUI

- 网站：https://namethatui.com/
- 姊妹站：https://namethatui.com/styles （Name That Vibe，命名视觉风格）
- 作者：Jane Appleseed（@jane），Toronto 的 design systems engineer
- 记录时间：2026-08-13

## 来源事实

- 定位是 "visual dictionary of UI"：用大白话描述一个 UI 元素（如 "the gray text inside the box that disappears when you type"），返回正式名称、代码符号、以及可直接粘贴给 coding agent 的 prompt。口号："Shared names make design and implementation prompts precise."
- 词条规模 76 个：Web 44 个、macOS 32 个，可按平台过滤、按 Newest / Popular 排序。
- 词条页解剖（以 /web/toast 为例）：
  - 标题带别名（Toast (Snackbar)）与一行定义；"If you called it…" 列出口语说法到正式名的映射。
  - "Anatomy — every part, named"：把元素拆成几个部件，每个部件给正式名和代码符号（如 toast viewport = `Toaster`、status message = `role="status"`）。
  - "Prompt — paste into your agent"：现成的 agent 指令，描述行为约束（角落实位、自动消失、hover/键盘聚焦时暂停计时）。
  - "Debug prompt"：排障模板，列出经典失败模式（如没有 aria-live 区域导致屏幕阅读器不播报）。
  - "In code" 表：各框架/标准里的名字对照（ARIA `role="status"`、shadcn/ui `Toaster`、Sonner `toast()`）。
- "Commonly confused"（/vs）：18 组易混词对比，如 Popover vs Dropdown Menu vs Tooltip、Switch vs Checkbox vs Radio、Modal Dialog vs Drawer vs Sheet、Skeleton vs Empty State（"is COMING" vs "NOTHING here"）、Hamburger vs Kebab。
- Guides（"the decisions before the names"）：/appkit-vs-swiftui、/swift-vs-electron、/translate（60+ 元素的 plain name → AppKit → SwiftUI 翻译表）。
- 方法论（/methodology）：从可见的东西出发；对照三层权威来源（平台 HIG 的用户可见名、框架文档的代码符号、WAI-ARIA/APG/WCAG/WHATWG HTML/MDN 的可访问角色）；用 demo + anatomy 让区别显而易见。命名冲突时不假装存在通用名，而是把平台名挂在术语上、优先平台官方说法、列出可用别名。
- 交互细节：双击任意词显示大白话定义；⌘K 搜索；"Surprise me" 随机发现；有 RSS（"New terms ship often"）；三个 founding sponsor 名额。
- macOS 词条用 AppKit/SwiftUI 符号（`NSAlert`、`NSSplitView` 等），Web 词条用 HTML/ARIA/CSS 参照。

## 本库判断（2026-08-13）

- 按参考站使用：给 coding agent 下 UI 指令前，先查正式名和现成 prompt；做设计系统评审时对齐术语。挂在 frontend 参考清单里，与 Transitions.dev（动效菜谱）互补——一个管"叫什么"，一个管"怎么动"。
- 核心差异点不是词典本身，而是每个词条自带 agent prompt + debug prompt，直接服务于"用精确术语写实现 prompt"的工作流。
- 局限：76 词条覆盖仍少；macOS 部分对以 web 为主的项目用处小；词条是参考而非规范，团队内术语仍应以自己的设计系统为准。
