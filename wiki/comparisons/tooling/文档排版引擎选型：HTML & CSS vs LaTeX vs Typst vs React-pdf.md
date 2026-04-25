---
title: 文档排版引擎选型：HTML & CSS vs LaTeX vs Typst vs React-pdf
type: comparison
category: tooling
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - typesetting
  - pdf
  - latex
  - typst
  - react-pdf
source_refs: []
---
# 文档排版引擎选型：HTML & CSS vs LaTeX vs Typst vs React-pdf

## 当前结论

如果目标是高质量 PDF、强分页能力和更稳的 CJK 排版，LaTeX 仍然是更稳妥的默认选项；如果更看重实时预览、前端协作和交互式开发体验，HTML & CSS 或 React-pdf 往往更顺手，但要接受排版控制力较弱的现实。

## 备选项

- HTML & CSS：最通用，实时预览和响应式体验最好，但原生分页和高质量排版较弱。
- LaTeX：排版质量、分页与 CJK 能力更强，但开发体验最重。
- Typst：语法和编译体验更现代，介于 Web 与 LaTeX 之间，但生态和 CJK 稳定性还不够稳。
- React-pdf：适合 React 技术栈和实时预览，但排版能力有限。

## 取舍分析

| 方案 | 优势 | 风险 | 适用场景 |
| --- | --- | --- | --- |
| HTML & CSS | 通用性强、前端团队熟悉、实时预览好、响应式自然 | 无原生分页、浏览器兼容差异、精细排版与 CJK 需要补洞 | Web 优先、模板变化快、先要开发效率 |
| LaTeX | 排版质量高、Knuth Plass 换行、分页成熟、CJK 支持更稳 | 学习曲线陡、实时预览弱、工具链和调试体验偏陈旧 | 简历、论文、正式 PDF、重排版质量 |
| Typst | 语法更现代、编译快、可定制换行 | 生态较新、CJK 稳定性不足、实时预览能力不完全开放 | 想摆脱 LaTeX 复杂度、又仍然重视排版质量 |
| React-pdf | 适合 React 团队、可复用组件、实时预览与分页都可做 | 对复杂排版、CJK 和高级版式支持有限 | React 应用内生成 PDF、工程集成优先 |

## 推荐理由

- 这条记录 已经不是简单收藏，而是把几个候选排版引擎按统一标准做了取舍，标准包括：
  - 换行算法质量；
  - CJK 排版；
  - 分页能力；
  - 实时预览体验。
- 把这些标准放在一起看，LaTeX 的优势很集中，尤其适合“排版质量优先”的场景。
- 但如果团队本身就是前端团队，且文档需要频繁交互预览或和现有 React 代码复用，HTML & CSS 或 React-pdf 会更务实。
- Typst 更像一个值得持续观察的中间路线：它试图保留排版系统的能力，同时降低 LaTeX 的上手成本，但目前还不够稳到能在所有 CJK 场景里直接取代 LaTeX。
