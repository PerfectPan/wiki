---
title: CVA
type: topic
category: frontend
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - cva
  - css
  - typescript
  - api-design
source_refs:
  - legacy-logseq-journals/2025_04_20.md
---
# CVA

## 摘要

CVA（class-variance-authority）是一种把样式组合逻辑从大量条件分支里抽出来的 API 设计方式。它的价值不在“又一个 class 工具”，而在于把样式变体组织成更声明式、可类型约束的接口。

## 关键点

- journal 里的观察很清楚：
  - 它让你少写显式 `if / else` 或大量 `clsx` 条件拼接；
  - 底层仍然是在组合 class 名；
  - 但接口层更像“声明变体”，而不是“手写条件逻辑”。
- 另一条重要结论是：它并不强绑定 Tailwind，核心思路本质上与 class name 组合有关，所以 CSS Modules 等场景也能借鉴。
- 因此，CVA 更像一类“样式 API 设计方法”，而不是只属于某个 CSS 体系的专属工具。

## 来源指针

- `legacy-logseq-journals/2025_04_20.md`
