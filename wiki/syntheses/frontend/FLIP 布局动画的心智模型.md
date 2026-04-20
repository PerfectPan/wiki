---
title: FLIP 布局动画的心智模型
type: synthesis
category: frontend
status: seed
created: 2026-04-20
updated: 2026-04-20
tags:
  - animation
  - flip
  - motion
  - css
  - performance
source_refs:
  - raw/sources/2023.05.08-2023.05.21.md
  - raw/sources/Front End.md
---
# FLIP 布局动画的心智模型

## 问题

当布局从一种状态跳到另一种状态时，为什么直接给 CSS 布局属性加 transition 往往不理想？更稳的做法是什么？

## 简答

因为很多布局属性并不能平滑动画，而且直接推动布局变化会带来持续的 layout 开销。FLIP 的核心思路是：先让布局一步到位，再用 `transform` 把它“倒回去”，最后把这个偏移量动画到 0。也就是说，动画的是视觉补偿，不是布局过程本身。

## 综合结论

- dated raw 里的这段记录给出了一个很稳定的判断：布局动画的问题，往往不是“能不能变”，而是“应该让什么属性负责变”。
- 直接对 `justify-content`、位置、尺寸一类布局属性做动画，浏览器需要不断重新 layout；而 `transform` 这类属性通常只影响合成层，成本更低。
- FLIP 可以拆成四步：
  - First：记录变更前元素的位置与尺寸；
  - Last：让 DOM 直接切到目标布局；
  - Invert：计算新旧布局之间的位移和缩放差；
  - Play：给元素设置反向 `transform`，再把它动画回 `translate(0) scale(1)`。
- 这样做的关键不是“渐变布局”，而是“布局先完成，动画只负责把结果平滑展示出来”。
- 这份 journal 残留里还有两个很实用的细节：
  - 如果元素同时改变位置和尺寸，`transform-origin` 最好以中心为基准，否则偏移量会算歪；
  - 如果父节点在做 scale，子节点可能需要套一层反向 scale 来抵消视觉拉伸，否则文本和内容会被一起压缩。
- 因此，FLIP 更像一个布局动画的性能心智模型，而不是某个具体库的 API。`framer-motion` 只是把这套思路包装得更易用。

## 未决问题

- 当前仓库里还没有把 FLIP 与浏览器渲染流水线、合成层和布局抖动放在一起讲的页面，后续可以再补成一篇更底层的性能页。
- 这条笔记目前主要来自单次 journal 记录，缺少更多实际项目案例；如果后续在仓库里积累更多动画实践，这页可以再升级。

## 来源指针

- `raw/sources/2023.05.08-2023.05.21.md`
- `raw/sources/Front End.md`
