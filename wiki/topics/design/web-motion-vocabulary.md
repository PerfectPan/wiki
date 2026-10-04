---
title: 网页动效词汇与描述方法
description: 持续整理网页动效的触发方式、效果名称、常见变化与操作要求，附悬停详解、描述示例和需求模板
type: topic
category: design
created: 2026-10-02
updated: 2026-10-04
timestamp: 2026-10-04
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
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:hover
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:focus-visible
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:focus-within
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll_snap
  - https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/
  - https://www.w3.org/WAI/ARIA/apg/patterns/carousel/
resource:
  - raw/sources/2026-10-02-adrianpunk-web-motion-dictionary.md
  - https://x.com/AdrianPunk115/status/2099485951701721585
  - https://x.com/AdrianPunk115/status/2099772129478869309
  - https://x.com/AdrianPunk115/status/2100209733567430964
  - https://motion.dev/docs/react-scroll-animations
  - https://motion.dev/docs/react-layout-animations
  - https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:hover
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:focus-visible
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:focus-within
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll_snap
  - https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/
  - https://www.w3.org/WAI/ARIA/apg/patterns/carousel/
---

# 网页动效词汇与描述方法

这里按触发方式、画面变化、时序和操作要求整理网页动效词汇，供查找名称、区分相近效果和编写需求时使用。词条可以随新案例和来源继续补充，同一种效果的别名与变体放在一起。

各节的描述示例由词汇和操作要求组合编写，方便根据自己的页面调整。

快速查阅：[[#触发方式：什么时候开始]]、[[#鼠标悬停（Hover）]]、[[#按画面变化选择词汇]]、[[#把“手感”变成可调整的要求]]、[[#可以直接填写的需求模板]]。

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

### 工具名称与效果名称

原文列举的工具分工是：CSS 用于常见样式过渡，Motion 用于 React 组件动画，GSAP 用于时间线和滚动编排，Three.js 用于网页 3D，Lottie 用于播放预制动画，Rive 用于有交互状态的动画。这些是实现方向，选好工具以后仍需说明触发和画面变化；已有项目优先复用现有方案。[上篇][part1]

## 触发方式：什么时候开始

触发条件与画面变化分开写。例如 Hover 可以触发抬升、变色或内容显现；Scroll-linked 可以控制缩放，也可以控制图片序列。这组分类来自[上篇][part1]，独立于原文后续连续编号的动效和 UX 词条。

| 触发方式 | 含义与常见细分 | 描述时补充 |
| --- | --- | --- |
| Hover，鼠标悬停 | 指针进入、停留在或离开元素；还可按停留意图、父级区域或距离触发 | 哪块区域感应、何时开始、移开怎样恢复；详见下节 |
| Focus，焦点 | 元素获得操作焦点；Focus-visible 表示需要显示焦点提示，Focus-within 表示自身或后代持有焦点 | 当前聚焦对象、提示样式、离开后是否关闭关联内容 |
| Click / Tap / Press，点击、轻触与按下 | Click / Tap 激活操作；Press / Active 是正在按下；Toggle 在开关状态间切换；另有 Double click 双击与 Long press 长按 | 按下与激活的反馈分别是什么，长按多久成立，取消后怎样恢复 |
| Pointer，指针 | Pointer move 持续移动；Position 映射坐标；Proximity 依据距离；Direction 依据方向；Velocity 依据速度 | 坐标作用范围、最大变化、离开后的状态；位置映射不等于只在进入时播放 |
| In view / Scroll-triggered，进入视口触发 | Enter / Leave viewport 对应进入与离开；Once 只播一次，Replay 再次进入时重播 | Trigger point 触发位置、Scroll direction 滚动方向、离开后保持还是复位 |
| Scroll-linked，跟随滚动进度 | Scroll-driven 用滚动位置控制进度；Scrub 表示进度同步，可约定少量跟随延迟 | 起止区间、倒滚行为；Pin 固定区块是另一项选择 |
| Gesture，手势 | Drag start / move / end 分别为拖拽开始、移动、松开；Swipe 快速滑动，Pinch 双指缩放，Rotate 旋转 | 边界、吸附或回弹目标、松开后的惯性、与页面滚动如何共存 |
| Load / Route，加载与页面切换 | Page load 首次加载、On mount 组件挂载、Route enter / exit 进入与离开页面、Transition complete 转场完成、Data ready 数据就绪 | 哪个阶段开始下一段动画，快速导航和加载失败时怎么办 |
| State change，状态变化 | Expand / Collapse 展开收起、Select / Deselect 选中取消、On / Off 开关，以及加载结果、内容更新和数值变化 | 从哪个状态到哪个状态，连续更新时保留哪次结果 |
| Timer / Idle，时间与空闲 | Delay 等待后开始、Autoplay 自动播放、Interval 定时切换、Idle 空闲触发、Loop 循环 | 等待和循环间隔、暂停入口、用户操作或页面不可见时怎样停止 |

Focus 不限于 Tab 操作，鼠标点击和程序安排也可能让元素获得焦点。`:focus-visible` 由浏览器结合输入方式等条件判断，并非“只匹配键盘”；`:focus-within` 则适合让含输入框的整块容器一起高亮。[MDN focus-visible][focus-visible]、[MDN focus-within][focus-within]

**描述示例：** 拖拽照片时让照片跟随指针，松开后对齐最近的插槽；超出容器边缘时限制位移。保留上移、下移按钮，并在手机上允许未开始拖拽的区域正常纵向滚动。[上篇][part1]、[下篇][part3]

### 鼠标悬停（Hover）

Hover 说明指针与元素的关系，悬停后的效果要另选。下面这些词分别描述触发时机、感应范围和视觉变化，并不都是 CSS 伪类名称。[上篇][part1]

| 悬停触发写法 | 含义 | 需要说明的条件 |
| --- | --- | --- |
| Hover enter，进入悬停 | 指针刚进入感应区时开始 | 感应区是按钮、图片还是整张卡片 |
| Hover leave，离开悬停 | 指针移出后撤销或复位 | 从当前状态返回，还是播放独立退场；快速进出能否中断 |
| Hover state，持续悬停 | 指针留在区域中时保持另一状态 | 保持静止状态还是持续运动 |
| Hover intent，悬停意图 | 停留一段时间后才触发，减少经过时误开 | 等待时长；到时前离开应取消，不能稍后再弹出 |
| Group hover / Parent hover，父级悬停 | 一个容器感应，多个内部元素一起响应 | 哪些子元素变化、谁先谁后；子元素之间移动时是否保持 |
| Proximity hover，临近触发 | 尚未进入元素，靠近一定距离就开始响应 | 感应半径、距离与效果强弱的关系；不等同于 CSS `:hover` |

| 悬停后的效果 | 画面变化 | 常用位置与约束 |
| --- | --- | --- |
| Hover reveal，悬停显现 | 露出说明、遮罩或附加操作 | 卡片与预览；必要信息还要能通过键盘、触屏访问 |
| Hover lift，悬停抬升 | 元素略微上移，阴影随之调整 | 作品或商品卡片；不要因位移让感应区反复进出 |
| Hover swap，悬停替换 | 主图换成另一视角，文字或图标换成另一内容 | 保持容器尺寸，写清移开是否恢复 |
| Hover underline，悬停下划线 | 线条从一端或中央展开 | 链接与导航；补上展开起点和收回方向 |
| Hover tilt，悬停倾斜 | 卡片按指针位置改变角度 | 对应 Tilt card；限制角度并保持文字可读 |
| Magnetic hover，磁吸悬停 | 元素或内部内容向指针轻微偏移 | 对应 Magnetic button；限制位移，移开后回位 |

**描述示例：** 作品卡片以整个卡片为感应区。指针进入后只抬升封面，并展开标题下划线；在卡片内部移动时保持，离开后从当前状态恢复。键盘聚焦卡片链接时显示同样的内容提示和清楚的焦点环；触屏直接显示标题与入口，减少动态时取消抬升。这是 Group hover 与 Lift、Underline 的组合示例。

触屏的 `:hover` 可能不出现、短暂出现或在点击后保持，不能把它当成可靠的功能入口。显示附加信息时，应保证键盘和触屏也能取得这些信息。[MDN hover][hover]

## 按画面变化选择词汇

名称用于缩短描述，仍要补上对象、范围和结束状态。下面按想表达的效果查词，不要求把所有效果用在同一页。

### 出现、消失与遮罩

| 想表达的变化 | 常用词 | 还要说清什么 |
| --- | --- | --- |
| 从透明到可见，或逐渐消失 | Fade in / Fade out，淡入 / 淡出 | 哪个元素、是否配合位移、关闭是否更快 |
| 从某个方向进入或离开 | Slide in / Slide out，滑入 / 滑出 | 从哪一侧进入、移动多远、退出方向 |
| 从小到大或缩小离开 | Scale in / Scale out，缩放进入 / 离开 | 缩放中心、变化幅度、文字是否保持稳定 |
| 同一位置的新旧内容交替 | Crossfade，交叉淡化 | 两者是否重叠、容器尺寸如何变化 |
| 改变几何边界，让内容逐步露出 | Clip-path reveal，裁剪揭示 | 矩形、圆形还是多边形，从哪里打开，内容本身是否移动 |
| 通过透明度图案逐步露出内容 | Mask reveal，蒙版显现 | 渐变柔边还是纹理、显现方向；与清楚几何边界的裁剪区分 |
| 从模糊到清晰 | Blur reveal，模糊显现 | 用在标题还是图片、正文何时能稳定阅读 |
| 遮挡层扫过，遮住旧内容后带出新内容 | Wipe transition，擦除转场 | 扫过方向、何时替换内容、能否跳过；区别于单个元素显现 |

这些是入退场的基本变化；同一元素可以组合淡入与位移，但应写清主动作。[上篇][part1]

### 文字显现与替换

| 想表达的变化 | 常用词 | 还要说清什么 |
| --- | --- | --- |
| 文字进入的统称 | Text reveal，文字显现 | 继续指定按行、词或字符处理，以及淡入、裁剪或位移 |
| 以完整的一行为单位出现 | Line reveal，按行显现 | 是否从行内裁剪窗口升起、多行顺序；适合较长标题 |
| 把句子分成词或短语后出现 | Word reveal，按词显现 | 如何分组、关键词是否先出现、整句何时显示完整 |
| 每个字符分别变化 | Character reveal，按字符显现 | 顺序、旋转或位移幅度；适合短词、数字等少量内容 |
| 模拟文字逐个被输入 | Typewriter，打字机 | 是否带输入光标、完成后是否保留、是否循环删除 |
| 随机字符逐渐替换为目标文字 | Scramble text，乱码解码 | 变化字符范围、何时停在正确文字、是否只播一次 |
| 一个短词连续变成另一个词 | Text morphing，文字变形 | 字符、字形或模糊交叉方式，宽度调整，循环何时暂停 |

文字越长，越需要尽快保持可读；中文按词出现时要说明按语义短语分组。正文通常无需等待逐字播放。[上篇][part1]、[中篇][part2]

**描述示例：** 状态栏从“正在同步”切到“同步完成”时，旧文字淡出、新文字在原位显现，宽度随内容平滑调整；结果保持可见，后续操作无需等待文字动画。这是文字替换的设计示例，和逐字符输入、随机解码是不同变化。

### 滚动与空间

| 想表达的变化 | 常用词 | 还要说清什么 |
| --- | --- | --- |
| 前景与背景以不同速度移动 | Parallax scrolling，视差滚动 | 哪层快、哪层慢、最大位移、移动端如何减弱 |
| 三层或更多画面各自移动，形成空间深度 | Multi-layer parallax，多层视差 | 每层方向与速度、边缘如何衔接、怎样保持画面组合完整 |
| 一排内容沿左右方向经过视口 | Horizontal scroll，横向滚动 | 原生横向滚动还是纵向滚动映射、区域如何退出、窄屏如何排列 |
| 图片或物体大小随滚动进度连续改变 | Scroll zoom，滚动缩放 | 缩放起止范围、中心与倒滚行为；区别于触发后自行播放的 Scale |
| 一个区域固定，内容随章节变化 | Sticky scrollytelling，固定式滚动叙事 | 固定何时开始和释放、章节如何提示、窄屏如何排列 |
| 连续产品画面随滚动切换 | Image sequence，图片序列 | 帧序、反向播放、未加载时显示什么 |
| 滚动落在指定卡片或章节的对齐位置 | Scroll snap，滚动吸附 | 对齐起点还是中心、强制还是临近吸附、长内容能否自由阅读 |
| 阅读位置反映在进度条或章节标记上 | Progress indicator，滚动进度提示 | 计算整页还是某个区域、内容高度变化时怎样更新；不是任务加载进度 |

**滚动触发与滚动绑定要分清。** 前者到达条件后自行播放；后者由滚动位置决定动画进度。固定区域（Pin）是另一项选择，不意味着一定要绑定动画进度。[上篇][part1]、[中篇][part2]、[Motion scroll](https://motion.dev/docs/react-scroll-animations)、[GSAP ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)

Scroll snap 描述滚动容器的对齐行为，可以直接使用 CSS 的吸附位置与对齐设置，不必默认实现成一段额外的播放动画。[MDN scroll snap][scroll-snap]

**描述示例：** 桌面端案例区把一段纵向滚动映射为横向浏览，卡片依次经过视口，进度标记显示当前位置；滚过最后一张后恢复正常纵向滚动。手机端使用纵向列表。这一例组合了横向滚动与进度提示，是否吸附需要另行决定。

### 鼠标与指针效果

以下效果都需要说明感应区域、幅度上限、离开状态和无指针设备的表现。[中篇][part2]

| 想表达的变化 | 常用词 | 还要说清什么 |
| --- | --- | --- |
| 按钮或内部文字向光标方向靠近 | Magnetic button，磁吸按钮 | 距离范围、位移上限、离开后的回位；点击范围保持稳定 |
| 卡片根据指针位置小幅旋转 | Tilt card，立体倾斜卡片 | 角度上限、高光或分层是否联动、文字可读性、离开后回正 |
| 圆点、圆环或操作标签跟随指针 | Cursor follower，光标跟随 | 跟随延迟、进入图片后的标签变化、系统指针能否定位、输入框如何处理 |
| 局部亮区随指针移动 | Cursor spotlight，光标聚光灯 | 光区大小、照亮背景还是边框、是否影响正文亮度 |
| 角色瞳孔朝指针方向移动 | Mouse-following eyes，鼠标跟随眼睛 | 瞳孔限于眼白内、离开后看向哪里、触屏保持静态或回应轻触 |
| 指针经过的位置留下逐渐消失的痕迹 | Cursor trail，光标拖尾 | 点、线或图片的密度和寿命；不同于仅有一个跟随圆环 |
| 背景图形按指针位置或距离变化 | Pointer-reactive background，指针响应背景 | 网格弯曲、粒子避让或渐变移动的范围，何时恢复；正文和控件保持稳定 |
| 立体模型、相机或光照响应指针 | 3D object follow，3D 物体跟随 | 改变哪个对象、旋转限制、离开回正、模型未就绪时的静态替代 |

聚光灯是局部照明变化，背景响应还可改变图形位置或形状；倾斜卡片也不等于完整的 3D 模型互动。触屏可以使用静态构图，不必自动改成持续旋转；持续运动的暂停要求见后文。

**描述示例：** 吉祥物只移动瞳孔，眼白与整张卡片保持不动；指针离开后瞳孔回到中间。光标拖尾仅用于旁边的展示空白区，经过按钮或正文时停止生成，并让已有痕迹淡出；触屏和减少动态模式关闭这两项装饰。

### 组件打开、关闭与切换

| 想表达的变化 | 常用词 | 还要说清什么 |
| --- | --- | --- |
| 内容展开、收起，周围元素让位 | Accordion，折叠展开 | 展开方向、可同时打开几项、再次点击如何收起 |
| 依附某个触发点出现选项、短提示或操作内容 | Dropdown / Tooltip / Popover，下拉菜单 / 提示气泡 / 弹出浮层 | 哪个触发点、空间不足时朝哪边展开、内容是否可操作；大型多列导航常称 Mega menu |
| 对话框与背景遮罩先后出现或消失 | Modal / Dialog transition，弹窗过渡 | 是否模态、缩放或位移起点、遮罩时序、焦点与关闭行为；不能仅凭 Dialog 名称推断一定模态 |
| 面板从边缘进入 | Drawer / Bottom sheet，抽屉 / 底部面板 | 从哪里进入、是否模态、怎样关闭、焦点如何返回 |
| 标签的选中指示器移动，关联面板随之切换 | Tab transition，标签页切换 | 指示器和内容的先后、交叉淡化还是滑动、容器高度和连续切换 |
| 固定区域切换图片或卡片 | Carousel / Slider transition，轮播切换 | 方向、循环边界、拖动后吸附、当前位置、上一项和下一项入口 |
| 出现短暂操作消息，停留后离开 | Toast / Snackbar，轻提示消息 | 出现位置、持续时间、是否带撤销、多次触发时替换还是堆叠；关键错误不能一闪而过 |

这些名称首先标识组件或反馈形式，仍需为它们选择淡入、缩放等具体变化。[下篇][part3]

Tooltip 提供短说明，不接收焦点；若浮层含按钮等可聚焦内容，就需要按可交互浮层处理。悬停提示在指针移到提示本身时也应保持，Escape 可关闭。APG 的 Tooltip 模式仍标注为讨论中的设计模式，此处用它说明组件区别。[APG Tooltip][tooltip]

轮播若自动播放，需要停止和重新开始的控制；鼠标悬停或键盘焦点进入时停止。因焦点进入而停止后，不应在焦点离开时自行恢复。[APG Carousel][carousel]

**描述示例：** 价格标签切换时，先将选中底色移动到目标标签，再替换关联内容；新旧面板高度平滑调整，连续选择只保留最后一次结果。复制价格链接成功后在角落显示轻提示，重复复制更新同一条消息，不叠成多层。

### 数字、加载与结果反馈

| 想表达的变化 | 常用词 | 还要说清什么 |
| --- | --- | --- |
| 数字从旧值过渡到新值，或像里程表一样逐位滚动 | Animated counter / Odometer，数字计数 / 滚动数字 | 起止真实数值、是否首次进入才播放、分隔符和单位稳定、减少动态时直接显示结果 |
| 等待时保留内容结构 | Skeleton loading，骨架屏加载 | 占位尺寸、明暗呼吸或扫光、数据到达如何替换、失败时显示什么 |
| 表示任务正在进行或已完成多少 | Loading indicator，加载指示 | 未知进度用不定指示，已知进度显示真实值；等待变长时提供状态说明和取消入口 |
| 结果通过图标、文字或局部变化呈现 | Success / Error feedback，成功 / 错误反馈 | 对勾绘制、完成高亮或错误抖动；同时说明结果、错误原因和修正入口 |
| 同一个控件的图标在两种状态间变化 | Icon morphing，图标形变 | 菜单变关闭、加号变减号或播放变暂停；按钮位置、点击范围和状态名称保持对应 |

数字动画不能代替准确数值，颜色变化不能独自解释成功或失败。加载动画与真实任务进度也要区分。[下篇][part3]

**描述示例：** 统计值更新时从当前显示值过渡到新结果，单位不动；期间又收到数据就改用最新目标值。展开详情时，加号变为减号，按钮仍在原位；减少动态时直接更新数字和图标。

### 布局变化与页面转场

| 想表达的变化 | 常用词 | 还要说清什么 |
| --- | --- | --- |
| 列表筛选、增删后重新排列 | Layout animation，布局过渡 | 哪些对象保持身份、如何补位、中途再改状态怎么办 |
| 列表里的对象连续变成详情中的对象 | Shared element transition，共享元素转场 | 两端对应关系、进入与返回位置、目标已消失时怎么办 |
| 整页切入切出 | Page transition，页面转场 | 前进和返回方向、加载期间显示什么、能否打断 |

写“页面转场”以后，还要说明是否需要某张图片或标题保持连续。Layout animation 处理位置与尺寸的变化，Shared element transition 还需要两端能识别为同一对象。[下篇][part3]、[Motion layout](https://motion.dev/docs/react-layout-animations)

## 把“手感”变成可调整的要求

| 词汇 | 控制什么 | 更有用的描述 |
| --- | --- | --- |
| Duration，时长 | 单次变化持续多久 | 按钮及时响应，较大的面板移动稍慢；不要让关键操作等待动画 |
| Delay，延迟 | 触发后等待多久才开始 | 标题之后再出现说明；加载和错误反馈立即给出 |
| Stagger，交错 | 一组元素的开始时间依次错开 | 按阅读顺序出现，并限制整组完成时间 |
| Easing，缓动 | 动画的速度如何变化 | 开始响应快，接近终点时减速 |
| Spring，弹簧 | 惯性和回弹的表现 | 轻微越过终点后快速停稳，或明确要求不回弹 |

“柔和”“有重量感”可以和这些具体要求一起使用。描述 Spring 时先说明回弹与停稳的目标，无需为了使用专业词而随意填写 stiffness、damping 等参数。[上篇][part1]、[Motion transitions](https://motion.dev/docs/react-transitions)

常见缓动还可细分为 Linear（匀速）、Ease-in（逐渐加速）、Ease-out（逐渐减速）、Ease-in-out（两端慢、中间快）和 Cubic-bezier（自定义曲线）。按运动目的选择：持续转动常用匀速，控件进入可使用及时启动、逐渐停稳的曲线；Stagger 控制一组元素的开始间隔，不是让每个元素依次播完再开始下一个。[上篇][part1]

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

- **Feedback，反馈。** 接受操作后立即表明响应，异步过程说明正在处理，结束后给出结果；失败时保留修正或重试入口。不要只做入场动画，却漏掉按下和加载状态。[下篇][part3]
- **Affordance，操作暗示。** 本页沿用来源的设计用语，指通过按钮边界、链接样式、展开箭头或拖拽把手提示可用操作。动效确认这些信号，关键入口在未悬停时也应可识别。[下篇][part3]
- **Focus，焦点与注意力。** 模态对话框打开后，背景不可交互，Tab 留在内部，关闭后通常回到触发者。初始焦点取决于内容：长内容可聚焦标题，破坏性确认可先聚焦取消操作，不能一律写“第一个按钮”。视觉上的突出也不能代替实际焦点安排。[WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)
- **Reduced motion，减少动态。** 简化视差、缩放和持续跟随，同时保留状态和必要反馈。Motion 的 `reducedMotion="user"` 可处理其位移、缩放和布局动画，自写指针循环仍需单独处理。[Motion accessibility](https://motion.dev/docs/react-accessibility)、[WCAG 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)
- **自动播放要允许用户控制。** 自动开始、超过五秒且与其他内容并列呈现的移动内容，除必要活动外应可暂停、停止或隐藏。把桌面端指针效果换成手机自动旋转，还需要检查这些条件。[WCAG 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)
- **Input modality support，输入方式适配。** 替代操作不止键盘。拖拽排序也提供可点击的上移、下移按钮；滑动切换也提供上一项、下一项入口，方便无法拖拽的触屏用户操作。[WCAG 2.5.7](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html)

上述 WCAG 2.3.3 为 AAA，2.2.2 为 A，2.5.7 为 AA；使用这些要求时，应结合项目目标等级检查完整流程。

## 从参考页面积累自己的描述

遇到喜欢的动画，先实际操作，再记录**页面地址、对象、触发、画面变化、结束状态、替代操作和拟使用位置**。截图记录外观，录屏帮助观察时间顺序；没有检查过的输入方式，标为待验证。[下篇][part3]

先在自己的一个组件上试用，确认内容可读、操作可完成、手机端可用，再决定是否保留。CSS、Motion 或 GSAP 的选择放在行为明确之后；优先复用项目已有方案，简单效果无需额外引入大型动画库。[上篇][part1]

## 继续补充词汇

新词放进对应的触发、效果、时序或操作要求小节，写出**中英文名称、可观察的变化、常见变体或适用位置、结束与替代条件、来源**。相同机制的别名并入已有条目；有新的行为区别时再单列。代表性示例补在所属小节，不需要每个词另开页面。

这页按概念维护，不沿用某篇文章的固定编号。来源的原始编号和范围保留在 [[raw/sources/2026-10-02-adrianpunk-web-motion-dictionary|来源材料]]，实现细节可链接到对应技术页面。后续增加来源时，同时补充来源指针。

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
[hover]: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:hover
[focus-visible]: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:focus-visible
[focus-within]: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:focus-within
[scroll-snap]: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll_snap
[tooltip]: https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/
[carousel]: https://www.w3.org/WAI/ARIA/apg/patterns/carousel/
