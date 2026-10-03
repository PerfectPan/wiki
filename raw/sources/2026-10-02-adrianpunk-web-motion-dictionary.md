<!-- source: https://x.com/AdrianPunk115/status/2099485951701721585 -->
<!-- type: x-series-summary -->

# Adrian Punk 网页动效词典：上、中、下篇来源摘要

## 来源

作者为 Adrian Punk（@AdrianPunk115）。以下为三篇文章的内容提要。

| 篇目 | 作者原始链接 | 发布日期（UTC+8） |
| --- | --- | --- |
| 上篇：教你准确描述页面怎么动 | [X](https://x.com/AdrianPunk115/status/2099485951701721585) | 2026-09-14 |
| 中篇：视差滚动、磁吸按钮与鼠标跟随 | [X](https://x.com/AdrianPunk115/status/2099772129478869309) | 2026-09-15 |
| 下篇：组件反馈、布局过渡与页面转场 | [X](https://x.com/AdrianPunk115/status/2100209733567430964) | 2026-09-16 |

## 系列内容提要

- **上篇**先区分实现工具、触发动作、视觉变化和 UX 约束，再解释第 1–16 个词条，涵盖时序参数、入退场和基础文字显现。值得保留的是先把行为说清，再复用项目已有工具。
- **中篇**的第 17–36 个词条涉及进阶文字、滚动空间和指针响应。重点区别是“到达某位置后播放”与“进度持续随滚动改变”；指针效果还要写清离开后的状态和触屏替代。
- **下篇**的第 37–51 个词条讨论组件状态、加载结果、布局和页面变化，第 52–56 个词条转向反馈、操作暗示、焦点、减少动态及输入方式。视觉过渡不能代替实际功能与反馈。

56 是系列连续编号的词条数，包含参数和 UX 规则，不等于 56 种独立动画。

下篇还提出案例积累方法：实际操作案例，记录来源、对象、触发、变化、结束状态、UX 处理和拟使用位置，再在自己的页面试一个局部，检查阅读、操作及手机表现后决定是否保留。

## 补充参考

以下官方文档补充实现与可访问性要求：

- [Motion 滚动文档](https://motion.dev/docs/react-scroll-animations)分别提供视口触发与滚动进度绑定；[GSAP ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)也区分触发播放、`scrub` 和 `pin`。
- [Motion 布局文档](https://motion.dev/docs/react-layout-animations)区分 `layout` 与 `layoutId`，可用来核对布局变化与共享元素过渡的实现。
- [WAI-ARIA 模态对话框模式](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)要求管理焦点和背景交互；初始焦点取决于内容及任务，不应机械地放在第一个按钮。
- [WCAG 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)讨论关闭非必要交互运动；[2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)另行约束自动播放；[2.5.7](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html)要求拖拽功能的非拖拽单指针替代，不能只补键盘操作。

这些词汇用于描述和查找动效。具体需求仍须写出对象、起止状态、重复策略及替代方式；实际观感、性能与输入操作需要在目标页面验证。

整理页：[[wiki/topics/design/web-motion-vocabulary|网页动画描述方法]]。
