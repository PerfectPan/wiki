---
title: Ant Design 异步默认值渲染
type: topic
category: frontend
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - antd
  - react
  - async-data
  - form
source_refs: []
---
# Ant Design 异步默认值渲染

## 摘要

当 `Select` 这类组件的默认值依赖异步数据时，问题的关键通常不是组件“坏了”，而是默认值生效的时机早于选项数据就绪。

## 关键点

- 有两个非常实用的处理方式：
  - 等数据加载完，再渲染真实组件；
  - 或者通过改变组件 `key`，强制让 React 把它当成新组件重新初始化。
- 这说明默认值问题的本质是组件初始化时机，而不是单纯的受控 / 非受控 API 选择。

## 相关页面

- [[React]]
