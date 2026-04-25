---
title: 模板克隆与 DOM 渲染路径
type: synthesis
category: frontend
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - template
  - dom
  - rendering
  - lit
  - web-components
source_refs:
  - wiki/topics/frontend/Lit.md
---
# 模板克隆与 DOM 渲染路径

## 问题

现代前端框架为什么经常会把“模板解析”和“动态更新”拆开？`template cloning` 这条路径的核心价值是什么？

## 简答

因为大多数 UI 模板里，真正变化的部分只占很小一块。先把大部分静态 DOM 结构预解析成模板，再通过克隆和局部填洞的方式更新，比每次都从头重建整棵结构更划算。

## 综合结论

- 模板型渲染路线的关键在于：模板可以只创建一次，后续通过 `cloneNode` 反复复用。
- 这意味着渲染系统实际上做了两层工作：
  - 静态部分：预先固化成模板；
  - 动态部分：在克隆后的结果里填充“洞”。
- 这条路线最重要的收益不是“代码看起来更优雅”，而是它减少了重复解析和重复创建静态 DOM 的成本。
- 这里还有几个真实边界：
  - 如果占位符本身是 DOM 树，而不是简单文本，更新路径会更复杂；
  - 长列表和大规模重排仍然需要额外策略；
  - Lit 一类实现并不是简单复制模板，而是在“模板 + 动态洞”之间做了更细的运行时组织。
- 因此，模板克隆并不是所有框架都会采用的唯一答案，但它很好地解释了为什么很多现代 UI 系统会把“模板定义”与“局部更新”当作两回事来设计。

## 未决问题

- 当前仓库还没有把这条路径和 signal / fine-grained reactivity / virtual DOM 放在一页里比较。
- 后续如果继续积累渲染模型材料，可以补一页 comparison，专门比较 template cloning、virtual DOM 和 fine-grained DOM updates。

## 来源指针

- `wiki/topics/frontend/Lit.md`
