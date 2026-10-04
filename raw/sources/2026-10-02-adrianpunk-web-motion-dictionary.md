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

## 触发分类

[上篇](https://x.com/AdrianPunk115/status/2099485951701721585)在连续编号词条之外，另列了以下 10 类触发。它们说明动效在什么条件下发生；具体视觉变化由后面的动效词条描述。

| 类别 | 中文名称 | 常见子类或描述维度 |
| --- | --- | --- |
| Hover | 悬停 | enter / leave / state / intent / group or parent / proximity：进入、离开、持续悬停、悬停意图、父级或分组悬停、接近目标 |
| Focus | 焦点 | focus / focus-visible / focus-within：获得焦点、需要显示焦点提示、自身或后代获得焦点 |
| Click / Tap / Press | 点击、轻点与按压 | active / toggle / double click / long press：按下状态、切换、双击、长按 |
| Pointer | 指针 | move / position / proximity / direction / velocity：移动、位置、距离、方向、速度 |
| In view / Scroll-triggered | 进入视口或滚动触发 | enter / leave / once / replay / direction / trigger point：进入、离开、只播放一次、重复播放、滚动方向、触发位置 |
| Scroll-linked | 滚动进度关联 | scroll-driven / scrub / pin / progress：由滚动驱动、随滚动进度播放、固定元素、进度映射 |
| Gesture | 手势 | drag start / move / end / swipe / pinch / rotate：开始拖拽、拖拽中、结束拖拽、滑动、捏合、旋转 |
| Load / Route | 加载与路由 | page load / on mount / route enter / exit / transition complete / data ready：页面加载、挂载、路由进入与离开、过渡完成、数据就绪 |
| State change | 状态变化 | expand-collapse / select-deselect / loading-success-error / on-off / content update / value change：展开与收起、选中与取消、加载与结果、开关、内容更新、数值变化 |
| Timer / Idle | 定时与空闲 | delay / autoplay / interval / idle / loop：延迟、自动播放、定时重复、空闲、循环 |

Hover 可与 reveal、lift、swap、underline、tilt、magnetic 等视觉效果组合。只写 Hover 不能说明元素如何变化；只写效果名也不能说明何时触发。[上篇](https://x.com/AdrianPunk115/status/2099485951701721585)

## 连续编号词条目录

### 上篇：第 1–16 项

来源：[教你准确描述页面怎么动](https://x.com/AdrianPunk115/status/2099485951701721585)。

| 编号 | 英文词条 | 中文名称 |
| --- | --- | --- |
| 1 | Easing | 缓动 |
| 2 | Duration | 持续时间 |
| 3 | Delay | 延迟 |
| 4 | Stagger | 错峰播放 |
| 5 | Spring | 弹簧动画 |
| 6 | Fade in / out | 淡入与淡出 |
| 7 | Crossfade | 交叉淡化 |
| 8 | Slide in / out | 滑入与滑出 |
| 9 | Scale in / out | 缩放入场与退场 |
| 10 | Blur reveal | 模糊显现 |
| 11 | Clip-path reveal | 裁剪路径显现 |
| 12 | Mask reveal | 遮罩显现 |
| 13 | Wipe transition | 擦除式过渡 |
| 14 | Text reveal | 文字显现 |
| 15 | Line reveal | 逐行显现 |
| 16 | Word reveal | 逐词显现 |

### 中篇：第 17–36 项

来源：[视差滚动、磁吸按钮与鼠标跟随](https://x.com/AdrianPunk115/status/2099772129478869309)。

| 编号 | 英文词条 | 中文名称 |
| --- | --- | --- |
| 17 | Character reveal | 逐字显现 |
| 18 | Typewriter | 打字机效果 |
| 19 | Scramble text | 字符扰动 |
| 20 | Text morphing | 文字形变 |
| 21 | Parallax scrolling | 视差滚动 |
| 22 | Multi-layer parallax | 多层视差 |
| 23 | Horizontal scroll | 横向滚动 |
| 24 | Scroll zoom | 滚动缩放 |
| 25 | Sticky scrollytelling | 固定区域滚动叙事 |
| 26 | Image sequence | 图像序列 |
| 27 | Scroll snap | 滚动吸附 |
| 28 | Progress indicator | 阅读或滚动进度指示 |
| 29 | Magnetic button | 磁吸按钮 |
| 30 | Tilt card | 倾斜卡片 |
| 31 | Cursor follower | 光标跟随元素 |
| 32 | Cursor spotlight | 光标聚光效果 |
| 33 | Mouse-following eyes | 视线跟随鼠标 |
| 34 | Cursor trail | 光标轨迹 |
| 35 | Pointer-reactive background | 响应指针的背景 |
| 36 | 3D object follow | 三维物体跟随 |

### 下篇：第 37–56 项

来源：[组件反馈、布局过渡与页面转场](https://x.com/AdrianPunk115/status/2100209733567430964)。

| 编号 | 英文词条 | 中文名称 |
| --- | --- | --- |
| 37 | Accordion | 折叠面板 |
| 38 | Dropdown / Tooltip / Popover | 下拉菜单、提示与浮层，含 Mega menu |
| 39 | Modal / Dialog transition | 模态框与对话框过渡 |
| 40 | Drawer / Bottom sheet | 抽屉与底部面板 |
| 41 | Tab transition | 标签页切换 |
| 42 | Carousel / Slider transition | 轮播与幻灯片切换 |
| 43 | Toast / Snackbar | 短暂消息提示 |
| 44 | Animated counter / Odometer | 数字计数与里程表式滚动 |
| 45 | Skeleton loading | 骨架屏加载 |
| 46 | Loading indicator | 加载指示 |
| 47 | Success / Error feedback | 成功与错误反馈 |
| 48 | Icon morphing | 图标形变 |
| 49 | Layout animation | 布局动画 |
| 50 | Shared element transition | 共享元素过渡 |
| 51 | Page transition | 页面转场 |
| 52 | Feedback | 反馈 |
| 53 | Affordance | 操作暗示 |
| 54 | Focus | 焦点 |
| 55 | Reduced motion | 减少动态效果 |
| 56 | Input modality support | 输入方式支持 |

## 容易混淆的范围

- 四层分别回答使用什么工具、什么条件触发、发生什么视觉变化、怎样满足 UX 要求；10 类触发不计入 56 个连续编号词条。[上篇](https://x.com/AdrianPunk115/status/2099485951701721585)
- 第 28 项 Progress indicator 表达阅读位置或滚动进度；第 46 项 Loading indicator 表达操作或数据尚在加载。[中篇](https://x.com/AdrianPunk115/status/2099772129478869309)、[下篇](https://x.com/AdrianPunk115/status/2100209733567430964)
- Focus 在触发分类中指获得焦点等条件，第 54 项则把焦点作为 UX 要求；第 52–56 项不能当作单独的视觉效果清单。[上篇](https://x.com/AdrianPunk115/status/2099485951701721585)、[下篇](https://x.com/AdrianPunk115/status/2100209733567430964)
