---
title: Bundle
type: topic
category: tooling
status: seed
created: 2026-04-12
updated: 2026-04-19
tags:
  - bundler
  - build
  - performance
source_refs:
  - raw/sources/Bundle.md
---
# Bundle

- HMR 怎么评估？
- 是否可以有像目录树一样和源码来进行 diff，看出来哪些文件没有被打包进来
- 分析不出来的时候先尝试注释一些 plugin、loader，看看对耗时会不会有帮助
- 对于构建工具的文档要研读、熟悉
- 多思考，多尝试
- [[Tailwind]] 可能是构建慢的原因，要多考虑
- 构建分为编译文件，形成 graph 图，然后 emit，tree shaking 看着是发生在 emit 阶段，所以并不会让 hmr 变快，因为 graph 图还是要分析依赖的

## Source Pointers

- `raw/sources/Bundle.md`
