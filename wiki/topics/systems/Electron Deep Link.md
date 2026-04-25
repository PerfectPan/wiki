---
title: Electron Deep Link
type: topic
category: systems
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - electron
  - deep-link
  - custom-protocol
  - installer
source_refs:
  - legacy-logseq-journals/2023_01_31.md
---
# Electron Deep Link

## 摘要

Electron Deep Link 的核心不是“如何解析一个 URL”，而是如何让操作系统把自定义协议稳定地路由回你的应用，并在安装期和运行期都维持这层注册关系。

## 关键点

- journal 里记录的重点不是某个单独 API，而是一整条链路：
  - 自定义协议要先在 OS 层注册；
  - 安装时通常就应该把注册写进去；
  - 运行时还要能检查当前协议是否仍归本应用所有，并在必要时重新注册。
- 这说明 deep link 不是纯前端逻辑，而是“应用 + 安装器 + 操作系统协议表”协同的问题。
- journal 里给出的 `NSIS` 片段很实用：Windows 下的核心就是往注册表写协议头、shell 行为和启动命令。
- 这也解释了为什么跨平台 deep link 往往不能只靠 Electron 应用本身，还要分别处理 macOS 和 Windows 的安装与协议注册细节。

## 相关页面

- [[Electron]]

## 来源指针

- `legacy-logseq-journals/2023_01_31.md`
