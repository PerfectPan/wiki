---
title: TypeScript 类型收窄与 IIMT
type: synthesis
category: languages
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - typescript
  - narrowing
  - mapped-types
  - type-system
source_refs:
  - wiki/topics/languages/TypeScript.md
---
# TypeScript 类型收窄与 IIMT

## 问题

TypeScript 在控制流里的类型收窄和 IIMT 这类技巧，分别解决什么问题？为什么它们值得单独记住？

## 简答

类型收窄解决的是“运行时判断如何反馈到类型系统”，而 IIMT 解决的是“如何把联合类型映射成另一组更可消费的结果”。前者更像推理路径，后者更像类型层面的构造技巧。

## 综合结论

- `Type Narrowing` 说明了一个重要事实：TypeScript 并不是只看显式注解，还会利用控制流来缩小值集合。
- 这让 `discriminated union` 成为很稳定的建模方式，因为它把运行时分支和类型推理绑在了一起。
- 同一份记录里提到的 IIMT（Immediately Indexed Mapped Type）则属于另一类技巧：
  - 先对联合类型做映射；
  - 再立即索引回联合结果；
  - 用来把“联合里的每一个成员”映射成一套新结构。
- 这类技巧的价值，不在花哨，而在于它能把原本散落的联合成员，重新组织成更好消费的类型结果。
- 放在一起看，这两条材料其实补的是 TypeScript 的两种核心能力：
  - 收窄：让类型系统更贴近运行时条件；
  - 构造：让复杂类型结果可以被系统化生成。

## 未决问题

- 当前仓库还没有单独展开 `discriminated union`、IIMT、条件类型和分布式行为之间的关系。
- 后续如果继续沉淀 TypeScript 主题，可以把这页拆成更偏“技巧清单”的 comparison 或 patterns 页面。

## 来源指针

- `wiki/topics/languages/TypeScript.md`
