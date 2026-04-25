---
title: reflect-metadata
type: topic
category: languages
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - typescript
  - decorators
  - metadata
  - reflection
source_refs:
  - legacy-logseq-journals/2023_07_15.md
  - wiki/topics/architecture/@opensumi%2Fdi.md
---
# reflect-metadata

## 摘要

`reflect-metadata` 是 TypeScript 生态里一套历史悠久的 metadata 方案。它的重要性不在于“现在是不是官方未来”，而在于大量依赖注入与装饰器生态都曾建立在这套运行时类型信息之上。

## 关键点

- journal 里的核心判断是：
  - 这套方案最早和旧装饰器提案绑定；
  - 后续提案方向变化后，它并没有成为语言标准本身；
  - 但 TypeScript 生态里很多库仍沿用它来读取运行时 metadata。
- 对使用者来说，最关键的工程事实是：TypeScript 只会帮你把设计时类型信息按约定写进 metadata；真正的读取、注册和消费逻辑仍靠库本身完成。
- 所以它更像一个历史上非常关键的桥梁层，而不是“现代装饰器的终局答案”。

## 相关页面

- [[TypeScript]]
- [[@opensumi/di]]

## 来源指针

- `legacy-logseq-journals/2023_07_15.md`
- `wiki/topics/architecture/@opensumi%2Fdi.md`
