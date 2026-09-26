---
title: omp（oh-my-pi）
description: 终端 coding agent；TTSR 根据生成内容匹配规则，在需要时中断生成并提供修改建议
type: topic
category: ai
created: 2026-09-25
updated: 2026-09-26
timestamp: 2026-09-26
tags:
  - agent
  - harness
  - guardrails
source_refs:
  - raw/sources/2026-09-25-ttsr.md
  - https://omp.sh/docs/ttsr
  - https://github.com/can1357/oh-my-pi
resource:
  - raw/sources/2026-09-25-ttsr.md
  - https://omp.sh/docs/ttsr
  - https://github.com/can1357/oh-my-pi
---

# omp（oh-my-pi）

## 摘要

omp 是一个终端 coding agent。本页主要记录它的 TTSR（Time-Traveling Stream Rule）：生成内容匹配预设条件后，停止当前生成，将规则中的修改建议提供给模型，再重新生成。

## TTSR 如何工作

规则使用带 frontmatter 的 Markdown 文件。项目规则放在 `.omp/rules/`，个人规则放在 `~/.omp/agent/rules/`；frontmatter 定义匹配条件与范围，正文说明应该怎样修改。添加或修改规则后，需要启动新 session 才会重新发现规则。

`condition` 使用正则表达式，`astCondition` 使用 ast-grep 模式匹配 edit/write 引入的源码。`scope` 可以限定正文、工具及路径。默认不监听 thinking；显式开启也只适用于供应商提供的流。

默认模式会停止生成、丢弃当前未完成的响应，并带上规则正文重试。`interruptMode: never` 则允许响应或工具执行完成，再提供提醒。TTSR 无法撤销之前已经执行的操作。

## 使用时要注意什么

默认每条规则每个 session 只触发一次，状态随 session 保存。全局 `after-gap` 策略允许规则在间隔指定完整回合后再次触发。这个设置限制的是触发频率，不保证错误只发生一次。

窄而少见的条件适合按需提供指导；每个任务都需要遵守的约定，仍适合放在常驻上下文中。规则正文会发送给模型，因此不应包含 secrets。

使用 `omp ttsr test` 验证正反例，`omp ttsr list` 检查实际生效规则，`omp ttsr scan` 检查现有代码可能命中的位置。性能与误报需要按自己的规则测试。

## 相关页面

- [[Agent 输出检查：TTSR、权限规则与 PreToolUse hooks]]
- [[Agent Harness]]
- [[Code Agent]]

## 来源指针

- [[raw/sources/2026-09-25-ttsr|TTSR 文档存档]]
- [TTSR 官方文档](https://omp.sh/docs/ttsr)
- [oh-my-pi 仓库](https://github.com/can1357/oh-my-pi)
