---
title: ES Module 加载与 Import Maps
type: synthesis
category: frontend
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - esm
  - import-maps
  - module-loading
  - browser
  - polyfill
source_refs:
  - /Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2023_08_08.md
  - /Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2025_01_31.md
---
# ES Module 加载与 Import Maps

## 问题

浏览器里的 ES Module 到底怎么加载？`Import Maps` 和 `es-module-shims` 这类方案分别在补哪一层能力？

## 简答

ES Module 至少可以拆成“解析 specifier / 建立模块图 / 初始化绑定 / 执行模块”几个阶段。`Import Maps` 解决的是 specifier 到资源地址的映射，而 `es-module-shims` 一类方案则是在原生能力不够时，用 polyfill 把这套加载机制补出来。

## 综合结论

- 2023-08 的 journal 已经给出一个很稳定的模块加载心智：
  - 先解析模块说明符；
  - 再构建模块图；
  - 初始化模块绑定；
  - 最后执行模块。
- 这份材料还补了一个很关键的差异：ESM 使用的是值引用，因此循环依赖时的表现和 CommonJS 不一样。这个差异不是“语法糖”，而是模块系统语义不同。
- 2025-01 的 journal 则把 `Import Maps` 和 `es-module-shims` 放回浏览器实现层来看：
  - `Import Maps` 负责告诉浏览器“这个 specifier 应该映射到哪里”；
  - `es-module-shims` 这种 polyfill 方案，本质上是在浏览器缺乏完整支持时，自己接管部分解析和加载逻辑。
- journal 里对 `es-module-shims` 的观察也很有价值：它不是简单字符串替换，而是在用更底层的方式介入模块解析与执行时机。
- `modulepreload` 则补的是性能层：它不是重新定义模块图，而是让模块更早被下载、解析和编译。
- 这些材料合起来，比较稳的理解是：
  - 模块系统语义：由 ESM 规范决定；
  - specifier 映射：由 Import Maps 一类机制决定；
  - 浏览器兼容与补丁：由 `es-module-shims` 一类 polyfill 接管；
  - 性能优化：由 `modulepreload` 等资源提示负责。

## 未决问题

- 现在仓库里还没有把 ESM / Import Maps / bundler rewrites / integrity 校验放在一起画成一张完整链路图。
- `es-module-shims` 的内部实现仍可以继续拆成更具体的 topic，例如“浏览器侧模块 polyfill 的改写策略”。

## 来源指针

- `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2023_08_08.md`
- `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2025_01_31.md`
