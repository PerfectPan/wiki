---
title: 网页动画描述方法
description: 用对象、触发、起止状态、时序、中断和替代操作描述网页动画，附动效词汇速查、改写示例与需求模板
type: topic
category: design
created: 2026-10-02
updated: 2026-10-03
timestamp: 2026-10-03
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

# 网页动画描述方法

网页动画需求要说明：**什么元素，在什么条件下，从什么状态变成什么状态，怎样结束，以及用户中途改变操作时怎么办。** “高级一点”“丝滑一点”可以表达偏好，还需要补上这些可观察的行为。

最小描述可以写成一句话：

> 当【触发条件】发生时，让【对象】从【起始状态】变到【结束状态】，采用【动效与节奏】；【离开、返回或中断】时这样处理，在【键盘、触屏、减少动态】下这样替代。

## 先写清六件事

先确定行为，再选动效名称和实现工具。技术工具、触发方式、视觉变化和 UX 要求分别回答不同问题；“使用 Motion”没有说明画面怎么动，“Hover”也没有说明悬停之后发生什么。[动效词典上篇][part1]、[下篇][part3]

| 要素 | 要回答的问题 | 描述示例 |
| --- | --- | --- |
| 对象 | 哪个元素动，哪些元素保持稳定？ | 作品卡片的封面和箭头响应，标题不位移 |
| 触发 | 点击、悬停、进入视口、滚动进度，还是状态更新？ | 卡片首次进入视口时播放；向上返回时不重播 |
| 起止状态 | 哪个属性从什么值变到什么值，沿什么方向？ | 从下方 12px、透明，变为原位、不透明 |
| 时序与手感 | 多久完成，谁先谁后，是否回弹？ | 标题先出现，卡片依次跟随；结束时减速，不回弹 |
| 结束与中断 | 移开后如何复位，重复操作取哪次结果？ | 指针离开后回正；连续筛选时跟随最后一次选择 |
| 替代操作 | 键盘、触屏和减少动态时怎么用？ | 键盘聚焦显示同样信息，触屏点击展开，减少动态时直接呈现结果 |

不必一开始就给出每个毫秒值。先写清动作、方向、先后和结束状态；需要统一节奏时，优先使用项目已有的时长与缓动规范。

## 按画面变化选择词汇

名称用于缩短描述，仍要补上对象、范围和结束状态。下面按想表达的效果查词，不要求把所有效果用在同一页。

### 出现、消失与文字

| 想表达的变化 | 常用词 | 还要说清什么 |
| --- | --- | --- |
| 从透明到可见，或逐渐消失 | Fade in / Fade out，淡入 / 淡出 | 哪个元素、是否配合位移、关闭是否更快 |
| 从某个方向进入或离开 | Slide，滑入 / 滑出 | 从哪一侧进入、移动多远、退出方向 |
| 从小到大或按下时收缩 | Scale，缩放 | 缩放中心、变化幅度、文字是否保持稳定 |
| 同一位置的新旧内容交替 | Crossfade，交叉淡化 | 两者是否重叠、容器尺寸如何变化 |
| 内容从边界内逐渐露出 | Clip-path reveal，裁剪揭示；Mask reveal，蒙版显现 | 几何边界还是柔边、从哪里开始、内容本身是否移动 |
| 从模糊到清晰 | Blur reveal，模糊显现 | 用在标题还是图片、正文何时能稳定阅读 |
| 文字分组依次出现 | Line / Word / Character reveal，按行 / 词 / 字符显现 | 如何分组、阅读顺序、整句何时显示完整 |
| 模拟输入或短暂解码 | Typewriter，打字机；Scramble text，乱码解码 | 是否只播一次、是否循环删除、最终文字保持多久 |

文字越长，越需要尽快保持可读；中文按词出现时要说明按语义短语分组。正文通常无需等待逐字播放。[上篇][part1]、[中篇][part2]

### 滚动、指针与空间

| 想表达的变化 | 常用词 | 还要说清什么 |
| --- | --- | --- |
| 滚到某处后播放一段动画 | Scroll-triggered / In view，进入视口触发 | 触发位置、播放一次还是重复、离开后是否复位 |
| 滚多少就播放多少 | Scroll-linked / Scrub，滚动进度绑定 | 哪段滚动对应哪段变化、反向滚动怎样返回 |
| 多层画面形成前后深度 | Parallax，视差 | 哪层快、哪层慢、最大位移、移动端如何减弱 |
| 一个区域固定，内容随章节变化 | Sticky scrollytelling，固定式滚动叙事 | 固定何时开始和释放、章节如何提示、窄屏如何排列 |
| 连续产品画面随滚动切换 | Image sequence，图片序列 | 帧序、反向播放、未加载时显示什么 |
| 按钮靠近光标、卡片随光标倾斜 | Magnetic button，磁吸按钮；Tilt card，倾斜卡片 | 感应范围、位移或角度上限、离开后的回位 |
| 圆环或亮区跟随光标 | Cursor follower，光标跟随；Cursor spotlight，光标聚光灯 | 跟随速度、作用区域、是否遮挡点击、触屏替代 |

**滚动触发与滚动绑定要分清。** 前者到达条件后自行播放；后者由滚动位置决定动画进度。固定区域（Pin）是另一项选择，不意味着一定要绑定动画进度。[上篇][part1]、[中篇][part2]、[Motion scroll](https://motion.dev/docs/react-scroll-animations)、[GSAP ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)

### 组件反馈、布局与页面

| 想表达的变化 | 常用词 | 还要说清什么 |
| --- | --- | --- |
| 内容展开、收起，周围元素让位 | Accordion，折叠展开 | 展开方向、可同时打开几项、再次点击如何收起 |
| 面板从边缘进入 | Drawer / Bottom sheet，抽屉 / 底部面板 | 从哪里进入、是否模态、怎样关闭、焦点如何返回 |
| 等待时保留内容结构 | Skeleton，骨架屏 | 占位尺寸、数据到达如何替换、失败时显示什么 |
| 操作得到处理中、成功或失败反馈 | Loading / Success / Error feedback | 即时响应、真实进度或不定进度、重试入口 |
| 列表筛选、增删后重新排列 | Layout animation，布局过渡 | 哪些对象保持身份、如何补位、中途再改状态怎么办 |
| 列表里的对象连续变成详情中的对象 | Shared element transition，共享元素转场 | 两端对应关系、进入与返回位置、目标已消失时怎么办 |
| 整页切入切出 | Page transition，页面转场 | 前进和返回方向、加载期间显示什么、能否打断 |

弹窗、提示、标签页是组件名称，它们可以使用不同动效。写“打开弹窗”以后，还要说明背景、焦点与出现方式；写“页面转场”以后，还要说明是否需要某张图片或标题保持连续。[下篇][part3]、[Motion layout](https://motion.dev/docs/react-layout-animations)

## 把“手感”变成可调整的要求

| 词汇 | 控制什么 | 更有用的描述 |
| --- | --- | --- |
| Duration，时长 | 单次变化持续多久 | 按钮及时响应，较大的面板移动稍慢；不要让关键操作等待动画 |
| Delay，延迟 | 触发后等待多久才开始 | 标题之后再出现说明；加载和错误反馈立即给出 |
| Stagger，交错 | 一组元素的开始时间依次错开 | 按阅读顺序出现，并限制整组完成时间 |
| Easing，缓动 | 动画的速度如何变化 | 开始响应快，接近终点时减速 |
| Spring，弹簧 | 惯性和回弹的表现 | 轻微越过终点后快速停稳，或明确要求不回弹 |

“柔和”“有重量感”可以和这些具体要求一起使用。描述 Spring 时先说明回弹与停稳的目标，无需为了使用专业词而随意填写 stiffness、damping 等参数。[上篇][part1]、[Motion transitions](https://motion.dev/docs/react-transitions)

## 从模糊要求改成具体描述

下面的数值是设计示例，实际项目优先沿用已有动效规范。

**首屏入场**

原要求：“卡片出来得高级一点。”

改写：六张案例卡片首次进入视口时，从下方 12px 淡入原位，按从左到右、从上到下的顺序开始，相邻间隔 50ms，单张持续 200ms，结束时减速。整组约 450ms 完成；返回该区域不重播，减少动态时直接显示卡片。

**指针反馈**

原要求：“按钮跟着鼠标动，要丝滑。”

改写：仅让首要按钮产生磁吸反馈。指针进入按钮区域后，按钮朝指针方向移动，位移最多 4px；点击范围保持稳定，移开后回到中心。键盘聚焦时显示清楚的焦点环，触屏使用普通按下反馈，减少动态时取消位移。

**布局更新**

原要求：“筛选时加个动画。”

改写：点击筛选项后立即显示选中状态；保留的卡片从旧位置移动到新位置，移除项淡出，新增项淡入。不要重新播放整组首屏入场。连续切换时跟随最后一次选择，不排队等待；减少动态时直接更新排列并保留结果信息。

## 可以直接填写的需求模板

```text
场景与目的：这段动画帮助用户理解什么变化？
对象：哪些元素变化，哪些保持稳定？
触发条件：何时开始，只播一次还是重复？
起止状态：位置、尺寸、透明度或内容怎样变化？
时序：谁先谁后，多久完成，采用什么缓动或回弹？
结束与中断：移开、返回、重复操作、加载失败时怎样处理？
操作适配：键盘、触屏和减少动态时保留哪些功能与反馈？
实现约束：复用哪些现有工具；需要哪些图片、模型或字体？
验收：列出用户操作顺序，以及每一步能看到和操作的结果。
```

例如，把筛选和详情弹窗写成一段完整要求：

```text
复用项目现有动画方案，实现案例列表的筛选与详情查看。

点击筛选项后立即更新选中状态；保留的卡片从旧位置移动到新位置，
在 220ms 内结束，使用 ease-out；移除项淡出，新增项淡入。
连续切换时以最后一次选择为准，不重新播放整组首屏入场。

点击卡片或用键盘激活后打开模态详情弹窗，180ms 内淡入。
弹窗内容较长，打开时先聚焦标题；Tab 留在弹窗内部，背景不可交互。
Escape 和关闭按钮均可关闭，焦点返回原卡片；若卡片已被筛掉，
返回筛选控件。快速关闭时打断入场，不等待长动画。

触屏保留同一个可点击入口。开启减少动态后取消卡片位移，
直接更新排列，保留选中与结果信息。
分别检查连续筛选、快速打开关闭、键盘、触屏和减少动态。
```

## 描述时不能漏掉的操作要求

- **焦点随任务安排。** 模态对话框打开后，背景不可交互，Tab 留在内部，关闭后通常回到触发者。初始焦点取决于内容：长内容可聚焦标题，破坏性确认可先聚焦取消操作，不能一律写“第一个按钮”。[WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)
- **减少动态要改变实际运动。** 简化视差、缩放和持续跟随，同时保留状态和必要反馈。Motion 的 `reducedMotion="user"` 可处理其位移、缩放和布局动画，自写指针循环仍需单独处理。[Motion accessibility](https://motion.dev/docs/react-accessibility)、[WCAG 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)
- **自动播放要允许用户控制。** 自动开始、超过五秒且与其他内容并列呈现的移动内容，除必要活动外应可暂停、停止或隐藏。把桌面端指针效果换成手机自动旋转，还需要检查这些条件。[WCAG 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)
- **替代操作不止键盘。** 拖拽排序也提供可点击的上移、下移按钮；滑动切换也提供上一项、下一项入口，方便无法拖拽的触屏用户操作。[WCAG 2.5.7](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html)

上述 WCAG 2.3.3 为 AAA，2.2.2 为 A，2.5.7 为 AA；使用这些要求时，应结合项目目标等级检查完整流程。

## 从参考页面积累自己的描述

遇到喜欢的动画，先实际操作，再记录**页面地址、对象、触发、画面变化、结束状态、替代操作和拟使用位置**。截图记录外观，录屏帮助观察时间顺序；没有检查过的输入方式，标为待验证。[下篇][part3]

先在自己的一个组件上试用，确认内容可读、操作可完成、手机端可用，再决定是否保留。CSS、Motion 或 GSAP 的选择放在行为明确之后；优先复用项目已有方案，简单效果无需额外引入大型动画库。[上篇][part1]

## 相关页面

- [[wiki/topics/frontend/ui-element-naming|UI 元素命名]]：先说明哪个组件和状态发生变化。
- [[wiki/topics/design/interface-polish-details|界面质感细节]]：进一步调整可中断动画、入场顺序与退场节奏。
- [[wiki/topics/frontend/transitions-dev|Transitions.dev]]：查阅微交互参考。
- [[wiki/syntheses/frontend/flip-layout-animation-mental-model|FLIP 布局动画的心智模型]]：理解布局变化的实现。
- [[wiki/syntheses/frontend/interactive-ui-accessibility-baseline|交互式 UI 的可访问性基线]]：检查完整操作流程。

## 来源

- Adrian Punk《Vibe Coding 网页动效词典》：[上篇][part1]、[中篇][part2]、[下篇][part3]。
- [[raw/sources/2026-10-02-adrianpunk-web-motion-dictionary|动效词典来源材料]]。
- 实现与可访问性依据见各节所附的官方文档。

[part1]: https://x.com/AdrianPunk115/status/2099485951701721585
[part2]: https://x.com/AdrianPunk115/status/2099772129478869309
[part3]: https://x.com/AdrianPunk115/status/2100209733567430964
