---
title: 事件循环与 Microtask 检查点
type: synthesis
category: frontend
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - event-loop
  - microtask
  - promise
  - mutationobserver
  - browser
source_refs: []
---
# 事件循环与 Microtask 检查点

## 问题

浏览器里的 task 和 microtask 到底是什么关系？为什么 promise、`MutationObserver` 和事件处理的表现会让人误判执行顺序？

## 简答

task 是较粗粒度的事件循环工作单元，microtask 则是在 task 边界和回调完成后尽快清空的更高优先级队列。promise 回调之所以应被放进 microtask，而不是普通 task，是因为只有这样才能保持执行顺序稳定，并避免无意义地被渲染或其他 task 源打断。

## 综合结论

- 这条记录 的核心结论有两层：
  - 浏览器可能在 task 之间插入渲染；
  - microtask 会在当前 task 的回调阶段后被尽快清空，而不是像普通 task 那样等下一个循环片段。
- 这解释了为什么 promise 回调如果被当成普通 task，会出现两个问题：
  - 回调被渲染或其他任务额外延后；
  - 不同 task source 之间的相对顺序变得更不稳定。
- `MutationObserver` 会在 microtask 检查点附近批量触发，这也是它常被拿来和 promise 一起讨论的原因。
- 关于事件触发的观察也值得保留：
  - 代码里直接同步触发某个事件，往往仍处在同一段调用栈和冒泡链里；
  - 真正的用户交互则更接近一次独立 task 的进入点，因此 microtask 清空和后续冒泡/渲染的时机感受会不同。
- 对前端工程来说，最重要的不是死记“谁先谁后”，而是明确：
  - 哪些回调属于当前执行栈的一部分；
  - 哪些东西会被延后到 microtask 检查点；
  - 哪些东西可能在下一轮 task 或渲染之后才发生。

## 未决问题

- 当前仓库还没有单独记录 `requestAnimationFrame`、rendering opportunity 和 layout/paint 的关系。
- 如果后续积累更多浏览器调度案例，可以把 task / microtask / rendering 再整理成一页更完整的时间线图。
