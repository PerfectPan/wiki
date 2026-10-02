<!-- source: https://x.com/AdrianPunk115/status/2099485951701721585 -->
<!-- type: x-series-review -->
<!-- fetched: 2026-10-02 -->

# Adrian Punk 网页动效词典：上、中、下篇阅读记录

## 来源与覆盖范围

作者为 Adrian Punk（@AdrianPunk115）。本记录合并同一系列的三篇来源，只保存出处、结构和阅读提要，不镜像原文。

| 篇目 | 作者原始链接 | 本次可读的转载 |
| --- | --- | --- |
| 上篇：教你准确描述页面怎么动 | [X](https://x.com/AdrianPunk115/status/2099485951701721585) | [觉醒 AI 知识库](https://www.jxxy.net/ai/articles/adrianpunk-web-motion-dictionary-part1/) |
| 中篇：视差滚动、磁吸按钮与鼠标跟随 | [X](https://x.com/AdrianPunk115/status/2099772129478869309) | [觉醒 AI 知识库](https://www.jxxy.net/ai/articles/vibe-coding-web-motion-dictionary-2/) |
| 下篇：组件反馈、布局过渡与页面转场 | [X](https://x.com/AdrianPunk115/status/2100209733567430964) | [觉醒 AI 知识库](https://www.jxxy.net/ai/articles/adrianpunk115-vibe-coding-motion-dictionary-vol3/) |

中、下篇原始链接来自转载页的原文信息。三个 X 页面均未能直接读取，访问返回 403；因此未完成与作者原文的逐段核对，也未验证图片、视频演示。以下“系列内容”均指转载所呈现的内容，不把转载更新日期当作原作发布日期。

## 系列内容提要

- **上篇**先区分实现工具、触发动作、视觉变化和 UX 约束，再解释第 1–16 个词条，涵盖时序参数、入退场和基础文字显现。值得保留的是先把行为说清，再复用项目已有工具。
- **中篇**的第 17–36 个词条涉及进阶文字、滚动空间和指针响应。重点区别是“到达某位置后播放”与“进度持续随滚动改变”；指针效果还要写清离开后的状态和触屏替代。
- **下篇**的第 37–51 个词条讨论组件状态、加载结果、布局和页面变化，第 52–56 个词条转向反馈、操作暗示、焦点、减少动态及输入方式。视觉过渡不能代替实际功能与反馈。

56 是系列连续编号的词条数，包含参数和 UX 规则，不等于 56 种独立动画。

## 官方资料核对与本库判断

以下内容是本次补充核对，不是作者原文：

- [Motion 滚动文档](https://motion.dev/docs/react-scroll-animations)分别提供视口触发与滚动进度绑定；[GSAP ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)也区分触发播放、`scrub` 和 `pin`。
- [Motion 布局文档](https://motion.dev/docs/react-layout-animations)区分 `layout` 与 `layoutId`，可用来核对布局变化与共享元素过渡的实现。
- [WAI-ARIA 模态对话框模式](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)要求管理焦点和背景交互；初始焦点取决于内容及任务，不应机械地放在第一个按钮。
- [WCAG 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)讨论关闭非必要交互运动；[2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)另行约束自动播放；[2.5.7](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html)要求拖拽功能的非拖拽单指针替代，不能只补键盘操作。

本库将它作为描述和查找动效的词汇入口。词条名称不是统一接口定义，具体行为仍须写出对象、起止状态、重复策略及替代方式；实际观感、性能与输入操作需要在目标页面验证。

整理页：[[wiki/topics/design/web-motion-vocabulary|网页动效词汇与描述方法]]。

## 2026-10-02 浏览器直接核对补记

初次阅读后，已通过 browser-harness 直接打开并读取三篇 X Article。上文的 403 和经转载阅读描述保留为首次取材记录；本次已补上原文正文与文字示例核对，当前覆盖范围以此补记为准。

| 原文 | 发布日期（UTC+8） | 主帖 `time[datetime]` |
| --- | --- | --- |
| [上篇](https://x.com/AdrianPunk115/status/2099485951701721585) | 2026-09-14 | `2026-09-14T13:10:32Z` |
| [中篇](https://x.com/AdrianPunk115/status/2099772129478869309) | 2026-09-15 | `2026-09-15T08:07:42Z` |
| [下篇](https://x.com/AdrianPunk115/status/2100209733567430964) | 2026-09-16 | `2026-09-16T13:06:35Z` |

时间取自各原帖对应的发布时间元素，未把文末推荐帖的时间或转载更新日期混入。核对包含三篇的四层分类、连续编号 1–56、正文解释、提示词文字示例，以及下篇最后的案例整理方法。中篇部分代码块延迟加载，已待加载后补读；提示词是页面文字，不是从插图推断出来的。

原文核对支持此前关于触发与类型、滚动触发与进度绑定、组件反馈和输入替代的提要。补充保留下篇第六节的方法：实际操作案例，记录来源、对象、触发、变化、结束状态、UX 处理和拟使用位置，再在自己的页面试一个局部，检查阅读、操作及手机表现后决定是否保留。主题页将其整理为可复用的观察步骤；“已观察与待验证分开记”是本库补充建议。

说明插图未逐张核验；本次没有在目标网页执行动效或可访问性测试，不能据文章描述断言示例已经实现全部行为。主题页中的官方实现边界和自写完整示例仍与作者原文分开标识。
