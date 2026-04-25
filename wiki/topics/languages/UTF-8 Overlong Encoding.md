---
title: UTF-8 Overlong Encoding
type: topic
category: languages
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - utf8
  - encoding
  - security
  - unicode
source_refs: []
---
# UTF-8 Overlong Encoding

## 摘要

Overlong Encoding 指的是把本来可以用更短字节表示的字符，故意编码成更长的 UTF-8 序列。它本身不是合法的标准 UTF-8 用法，但历史上常被拿来做安全绕过。

## 关键点

- 核心在于：安全问题不在“编码长一点”，而在于不同系统对非法 UTF-8 的处理不一致。
- 如果过滤器按“正常 UTF-8”扫描，而后续某个解码阶段又把这种非法编码还原成真实字符，就可能出现绕过。
- 这类问题的本质是：
  - 校验与消费使用了不同的字符语义；
  - 同一串字节在不同阶段被解释成了不同结果。

## 相关页面

- [[Unicode]]
