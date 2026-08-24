---
title: UI 元素命名
description: 为什么 UI 元素的名字重要：名字是设计-开发-agent 信道上的协议；好名字的三层权威来源与典型失败模式。
type: topic
category: frontend
created: 2026-08-13
updated: 2026-08-14
timestamp: 2026-08-14
tags:
  - ui
  - terminology
  - design-systems
  - naming
  - agent-prompts
source_refs:
  - raw/sources/2026-08-13-namethatui.md
  - https://namethatui.com/
  - https://namethatui.com/methodology
  - https://namethatui.com/vs
resource:
  - raw/sources/2026-08-13-namethatui.md
  - https://namethatui.com/
  - https://namethatui.com/methodology
  - https://namethatui.com/vs
---

# UI 元素命名

## 摘要

UI 元素命名不是文案问题，是通信问题：名字是设计师、开发者、agent 之间信道上的协议。名字含糊，实现就走样——"输入框里灰色的字"每个人理解不同，`placeholder` 只有一个意思。agent 时代这个问题更尖锐，因为 prompt 里的词就是 agent 的全部上下文。

## 为什么名字是第一性的

UI 实现的链路是：脑中的界面 → 语言描述 → 代码。名字是这条链路上压缩率最高的协议——一个词携带一整个概念（行为、结构、可访问性语义）。协议缺失或含糊，每个环节都在猜，猜的代价是返工和 bug。

agent 把代价放大了：人还能靠截图和上下文补全歧义，agent 只能靠词。"做个保存成功后弹一下的提示"会得到十种实现；"用 `role="status"` 的 toast，3 秒自动消失，hover 暂停"只有一种。

## 好名字的三层权威

一个名字硬不硬，看它在三层来源里是否一致：

1. **平台的用户可见名**——Apple HIG、Material Design 怎么叫（用户和平台文档的语言）
2. **框架的代码符号**——shadcn 的 `Toaster`、Sonner 的 `toast()`（实现的语言）
3. **可访问性标准的角色**——ARIA `role`、APG pattern（语义的语言）

三层一致时直接用；不一致时把限定词挂上——macOS 的 Sheet 和 web 的 Sheet 不是一个东西，要说"macOS Sheet"。

## 典型失败模式

- **用描述当名字**："那个灰色的、点了会消失的字"——它叫 placeholder
- **同义词混用**：toast / snackbar / notification 各有所指，混用导致实现与预期错位
- **自造黑话**：团队内部叫顺了的词，新人和 agent 都没有锚点
- **平台漂移**：把一个平台的概念名套到另一个平台

## 实践

- 写 issue / prompt 前先查正式名，用"符号 + 角色"描述，不用口语
- 易混淆词成对记：popover vs dropdown menu vs tooltip、switch vs checkbox vs radio
- 命名冲突时以平台官方名为锚，列别名而不是发明新名

## 参考

- [NameThatUI](https://namethatui.com/)：76 个词条的元素词典（Web 44 + macOS 32），每个词条带 anatomy（部件名 + 代码符号）、可直接粘贴的 agent prompt 和 debug prompt；其方法论即上面的三层权威
- 易混淆词表：https://namethatui.com/vs
- 事实层：`raw/sources/2026-08-13-namethatui.md`

## 相关页面

- [[UI 设计风格]] —— 本页是元素层面的"叫什么"，风格是界面层面的"是什么风"
- [[wiki/topics/frontend/Transitions.dev|Transitions.dev]] —— 动效参考

## 来源指针

- `raw/sources/2026-08-13-namethatui.md`
- https://namethatui.com/
- https://namethatui.com/methodology
- https://namethatui.com/vs
