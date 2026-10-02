---
title: 网页动效词汇与描述方法
description: 区分动效的工具、触发、画面变化与 UX 要求，并把网页效果写成可实现、可验收的行为描述
type: topic
category: frontend
created: 2026-10-02
updated: 2026-10-02
timestamp: 2026-10-02
tags:
  - motion
  - animation
  - accessibility
  - ui
  - agent-prompts
source_refs:
  - raw/sources/2026-10-02-adrianpunk-web-motion-dictionary.md
  - https://x.com/AdrianPunk115/status/2099485951701721585
  - https://x.com/AdrianPunk115/status/2099772129478869309
  - https://x.com/AdrianPunk115/status/2100209733567430964
  - https://motion.dev/docs/react-scroll-animations
  - https://motion.dev/docs/react-layout-animations
  - https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
resource:
  - raw/sources/2026-10-02-adrianpunk-web-motion-dictionary.md
  - https://x.com/AdrianPunk115/status/2099485951701721585
  - https://x.com/AdrianPunk115/status/2099772129478869309
  - https://x.com/AdrianPunk115/status/2100209733567430964
  - https://motion.dev/docs/react-scroll-animations
  - https://motion.dev/docs/react-layout-animations
  - https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
---

# 网页动效词汇与描述方法

## 摘要

网页动效描述要回答：谁发生变化、由什么触发、从什么状态变到什么状态，以及用户如何继续操作。本页以 Adrian Punk 的动效词典为分类入口，补充官方实现资料与可访问性要求，供设计说明和 AI 编程任务引用。

**来源限制**：三篇 X 原文均无法直接读取，本次经转载阅读；未核对原始图片和视频。三篇出处、对应转载及阅读范围见[[raw/sources/2026-10-02-adrianpunk-web-motion-dictionary|合并阅读记录]]。下文明确标出的实现细节与范例由本库补充。

## 系列如何组织动效

系列按四层分类：工具决定如何实现，触发决定何时开始，类型决定画面变化，UX 规则约束操作。工具举例包括 CSS、Motion、GSAP、Three.js、Lottie、Rive；它们的名称不能代替行为说明。[上篇转载](https://www.jxxy.net/ai/articles/adrianpunk-web-motion-dictionary-part1/)

| 篇目 | 阅读重点 |
| --- | --- |
| 上篇，1–16 | 时序、显隐、位移与基础文字入场 |
| 中篇，17–36 | 文字变化、滚动空间、指针响应 |
| 下篇，37–56 | 组件和加载状态、布局与页面变化，以及 UX 要求 |

编号包含参数和使用规则，不能理解为 56 种独立动画。[中篇转载](https://www.jxxy.net/ai/articles/vibe-coding-web-motion-dictionary-2/)、[下篇转载](https://www.jxxy.net/ai/articles/adrianpunk115-vibe-coding-motion-dictionary-vol3/)

## 把触发、类型和参数分开

以下是结合官方资料整理的常用区别。

| 要描述的维度 | 词汇与含义 | 还需要写什么 |
| --- | --- | --- |
| 时间安排 | Duration 是播放时长；Delay 是开始前等待；Stagger 是一组元素依次错开开始 | 整组结束时间，关键操作是否需要等待 |
| 变化过程 | Easing 控制速度曲线；Spring 描述弹簧式响应 | 是否回弹，幅度及中途改变目标时的表现 |
| 属性变化 | Fade 改透明度，Slide 改位置，Scale 改大小 | 起点、终点和作用元素 |
| 滚动触发 | Scroll-triggered：到达位置后启动一段动画 | 触发区域，只播一次还是可重复 |
| 滚动绑定 | Scroll-linked：滚动进度决定动画进度 | 哪段滚动对应哪些值，反向滚动如何恢复 |
| 布局变化 | Layout animation：同一元素的位置或尺寸变化 | 哪些元素需要保留身份，增删项如何处理 |
| 共享元素 | Shared element transition：让不同状态中的对应对象连续变化 | 如何匹配对象，进入和返回各自的目标 |

参数可核对 [CSS transitions](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Transitions/Using) 与 [Motion transitions](https://motion.dev/docs/react-transitions)；滚动区别见 [Motion scroll](https://motion.dev/docs/react-scroll-animations)，布局与共享元素见 [Motion layout](https://motion.dev/docs/react-layout-animations)。

中篇的 Magnetic button、Tilt card、Cursor follower 分别指按钮趋近指针、卡片随指针倾斜、装饰物跟随光标；仅写 Hover 无法确定是哪一种。描述这类效果时应补上作用范围、最大位移、离开后的回位，以及无悬停输入时的版本。[中篇转载](https://www.jxxy.net/ai/articles/vibe-coding-web-motion-dictionary-2/)

## 工具落实到哪些能力

以下是本库根据官方文档整理的实现入口，不是必须安装的依赖清单。先检查项目现有方案，再判断是否缺少能力。

| 需求 | 可核对的实现入口 |
| --- | --- |
| 单个元素的样式过渡 | CSS `transition-property`、`duration`、`timing-function`、`delay`，明确要变化的属性。见 [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Transitions/Using) |
| React 元素进出视口、进度绑定 | Motion `whileInView` / `useInView` 与 `useScroll`；一次性播放需明确配置。见 [Motion scroll](https://motion.dev/docs/react-scroll-animations) |
| React 布局和对象对应关系 | Motion `layout` 与 `layoutId`；布局目标写在样式或类名中。见 [Motion layout](https://motion.dev/docs/react-layout-animations) |
| 滚动控制整段时间线 | GSAP ScrollTrigger 的 `start` / `end` 指定区间，`scrub` 绑定播放进度，`pin` 固定区域。三项各自独立。见 [ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/) |

## 动效必须保留的操作能力

下篇把反馈、焦点与输入方式纳入描述。本库进一步按标准细化以下边界，避免把视觉示例直接当作组件实现要求。

1. **模态与非模态要分清。** 模态对话框打开后，背景不可交互，焦点进入内部，Tab 在内部移动，Escape 可关闭；关闭后通常回到触发者。初始焦点随内容和任务决定，破坏性确认可以先放在取消操作，长内容可以先聚焦标题。不能统一写“聚焦第一个按钮”。[WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)
2. **减少动态要改变实际运动。** 对非必要交互运动提供关闭方式或响应系统偏好，保留结果信息。Motion 的 `reducedMotion="user"` 可关闭其位移、缩放和布局动画，但自写指针循环仍需单独处理。[WCAG 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)、[Motion accessibility](https://motion.dev/docs/react-accessibility)
3. **自动播放与交互触发分开检查。** 自动开始、超过五秒、与其他内容并列呈现的移动、闪烁或滚动内容，除必要活动外应可暂停、停止或隐藏。把鼠标跟随改成手机自动旋转不能直接视作合格替代。[WCAG 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)
4. **拖拽替代不止键盘。** 排序可以另提供可点击的上移、下移按钮。只增加方向键支持，仍可能让触屏用户无法在不拖拽时操作；标准分别检查键盘和非拖拽单指针操作。[WCAG 2.5.7](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html)

这里的 WCAG 2.3.3 为 AAA，2.2.2 为 A，2.5.7 为 AA；本文将其作为实现检查项，并不据此宣称某个页面已满足完整 WCAG 等级。

## 完整描述范例

以下是本库自写的需求示例，不是系列原文提示词；数值是此示例的设计选择，不是通用标准。

```text
检查项目现有动画方案，实现案例列表的筛选与详情弹窗。

用户点击筛选项后立即更新选中状态；保留卡片从旧位置移动到新位置，
在 220ms 内结束，使用 ease-out；移除项淡出，新增项淡入，
不要重新播放所有卡片的首屏入场。连续切换时以最后一次选择为准。

点击卡片或用键盘激活后打开模态详情弹窗，180ms 内淡入。
弹窗较长，打开时先聚焦标题；Tab 留在弹窗内部，背景不可交互。
Escape 和关闭按钮均可关闭，焦点返回原卡片；若卡片已被筛掉，
返回筛选控件。关闭动作不等待长动画。

触屏使用同一个可点击入口；不把必要操作藏在悬停状态。
用户开启减少动态后取消卡片位移，直接更新排列，保留选中与结果信息。
验收连续筛选、快速打开关闭、键盘操作、触屏和减少动态五种情况。
```

描述是否完整，可以按对象、触发、起止状态、时序、结束或中断、替代操作逐项检查。完成代码后仍须在实际页面操作，核对返回位置、焦点和最终状态，不能用静态截图证明全部交互正确。

## 相关页面

- [[wiki/topics/frontend/ui-element-naming|UI 元素命名]]：先确认组件和状态的名字。
- [[wiki/topics/frontend/transitions-dev|Transitions.dev]]：查看微交互实例。
- [[wiki/syntheses/frontend/flip-layout-animation-mental-model|FLIP 布局动画的心智模型]]：继续理解布局变化的实现。
- [[wiki/syntheses/frontend/interactive-ui-accessibility-baseline|交互式 UI 的可访问性基线]]：检查完整操作流程。

## 来源指针

- [[raw/sources/2026-10-02-adrianpunk-web-motion-dictionary|三篇出处与阅读记录]]。
- 作者 X：[上篇](https://x.com/AdrianPunk115/status/2099485951701721585)、[中篇](https://x.com/AdrianPunk115/status/2099772129478869309)、[下篇](https://x.com/AdrianPunk115/status/2100209733567430964)。
- 本次可读转载：[上篇](https://www.jxxy.net/ai/articles/adrianpunk-web-motion-dictionary-part1/)、[中篇](https://www.jxxy.net/ai/articles/vibe-coding-web-motion-dictionary-2/)、[下篇](https://www.jxxy.net/ai/articles/adrianpunk115-vibe-coding-motion-dictionary-vol3/)。
- 官方技术与可访问性依据已就近链接；查阅日期为 2026-10-02。
