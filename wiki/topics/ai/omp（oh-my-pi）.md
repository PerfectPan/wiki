---
title: omp（oh-my-pi）
description: 把 IDE 能力直接接进终端的 coding agent；其 TTSR（Time-Traveling Stream Rule）是「生成流中途拦截」型护栏的代表实现
type: topic
category: ai
created: 2026-09-25
updated: 2026-09-25
timestamp: 2026-09-25
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

omp（仓库 `can1357/oh-my-pi`，Stencil Labs 开发）是一个「把 IDE 接进来」的 coding agent：原生 Rust 核心的 agentic harness，把 LSP、调试器、浏览器、GitHub、持久记忆直接接入终端 agent，Windows 原生免 WSL，macOS / Linux 也可用。截至 2026-09 约 33k star，社区资料称其源自 Pi（mariozechner）的分叉延伸（GitHub 上并非 fork 关系）。它最值得关注的设计是 **TTSR（Time-Traveling Stream Rule）**：在模型生成流中途拦截可识别的错误、注入纠正、就地重试的护栏机制。

## 关键点

- **产品形态**：「IDE wired in」——LSP、调试器、浏览器、GitHub、持久记忆内置进终端 agent；对标 Claude Code / Cursor 一类工具，主打让 agent 看到你 IDE 看到的一切。
- **TTSR 解决的问题**：有些指导只在特定模式出现时才重要（禁用某个 API、某类危险 shell 片段、正文里反复出现的错误说法）。放进 AGENTS.md 这类常驻上下文是浪费——TTSR 是反应式的：**条件出现才注入，平时零成本**。
- **规则即 Markdown 文件**：放 `<项目>/.omp/rules/<名字>.md`（随仓库提交）或 `~/.omp/agent/rules/`（个人全局）。frontmatter 声明「何时何地反应」，正文 Markdown 是命中时注入给模型的纠正方案（「为什么错、该怎么做」）。
- **触发条件两种**：`condition` 是 JS 正则，对**流式累积内容**求值、可跨 chunk 命中；`astCondition` 是 ast-grep 结构模式（只对 edit/write 引入的源码生效），适合格式化或命名让正则脆弱的结构性规则。
- **监听面（scope）可精确收窄**：`text`（助手正文）/ `thinking` / `tool` / `tool:<name>` / `tool:<name>(<glob>)`（限定候选路径）；顶层 `globs` 是额外路径闸门。不写 scope 默认监听正文和所有工具参数，不含 thinking。
- **命中的语义是「打断 + 重试」，不是文本替换**：默认 `interruptMode: always`——响应立即停止、默认丢弃半成品（`contextMode: discard`）、带着规则正文重新生成；发生在工具调用执行**之前**（官方原话：TTSR 命中无法撤销已执行完的工具调用）。另有 `never` 档的软提醒（放行工具执行、把提醒附在结果旁），只在放行安全时用。
- **失控成本被结构封顶**：每条规则默认**一个 session 只触发一次**（`repeatMode: once`，fired 状态随 session 持久化，resume 不会重新武装）；`after-gap` 模式隔 N 个完整回合才可再触发。写得糟糕的规则最多浪费一次重试。
- **配套 CLI**：`omp ttsr test`（离线测规则，支持 `--verbose/--json`）、`omp ttsr list`（看生效规则）、`omp ttsr scan src/`（启用宽规则前先扫存量代码看误伤）。
- **性能特征**：匹配在本地 Rust 进程内、与生成**并行**进行，微秒到毫秒级，淹没在 LLM 生成延迟里；真正的成本在命中时（作废一次半成品生成），但比「完整生成 → 工具调用失败 → 修复回合」便宜。文档的告诫：正则保持线性、避免 `(.*)+` 类病态模式、危险规则收窄 scope、规则正文别放 secrets（命中时会发给模型）。
- **在护栏谱系中的位置**：omp 自己同时有 Hooks（工具执行周界的确定性拦截）和 TTSR（生成流中途拦截）两层——详见 [[Agent 护栏的拦截位置：生成流中途 vs 工具调用门禁]]。
- **生态信号**：HN（2026-08）已有用户把 OMP 当 harness 可用性的对比标杆；第三方有 Medium 综述与 composio 的 Pi vs OMP 对比。TTSR 概念为 omp 自有，暂无独立第三方讨论。

## 相关页面

- [[Agent 护栏的拦截位置：生成流中途 vs 工具调用门禁]]——TTSR 与 Claude Code deny/hooks 的取舍分析
- [[Agent Harness]]、[[Code Agent]]——harness 与 code agent 的整体图景
- [[Code Agent 结构约定的可验证边界]]——「用可执行检查替代祈使式嘱咐」的同族问题

## 来源指针

- raw/sources/2026-09-25-ttsr.md（TTSR 官方文档全文 + 项目背景附注）
- https://omp.sh/docs/ttsr 、https://omp.sh
- https://github.com/can1357/oh-my-pi
