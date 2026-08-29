---
title: Sandbox
description: 沙箱的基本概念、隔离机制和常见实现方式。
type: topic
category: systems
created: 2026-04-12
updated: 2026-08-29
timestamp: 2026-08-29
tags:
  - sandbox
  - isolation
  - container
  - security
source_refs:
  - raw/sources/Sandbox.md
  - wiki/syntheses/systems/容器资源隔离与超卖机制.md
resource:
  - raw/sources/Sandbox.md
  - wiki/syntheses/systems/容器资源隔离与超卖机制.md
---

# Sandbox

沙箱（Sandbox）是一种隔离执行环境，用于在受限的权限和资源下运行不可信或高风险的代码，防止其影响宿主系统或其他进程。

## 关键点

- **隔离边界**：沙箱通过操作系统的隔离机制（namespace、cgroups、seccomp 等）限制进程能看到什么、能用多少资源、能调用哪些系统调用。
- **资源限额**：CPU、内存、磁盘、网络等资源可以被限制，防止单个沙箱耗尽宿主资源。
- **生命周期**：沙箱通常是临时的，创建后执行任务，完成后销毁。持久化数据需要放在外部存储。
- **不可迁移**：容器级沙箱创建后绑定在宿主节点上，不支持热迁移，消失方式是销毁而非迁移。

## 常见实现层级

| 层级 | 隔离强度 | 代表技术 | 特点 |
| --- | --- | --- | --- |
| 线程级 | 弱 | 同进程内多线程 | 最轻量，但共享进程地址空间，一个线程崩溃可能影响全局 |
| 进程级 | 中 | fork + namespace | 独立进程地址空间，崩溃半径小，适合承载可崩溃任务 |
| 容器级 | 较强 | Docker、containerd、cgroups + namespace | 共享内核，资源隔离好，启动快 |
| 虚拟机级 | 强 | KVM、QEMU | 独立内核，隔离最彻底，但启动慢、开销大 |

## 相关页面

- [[wiki/syntheses/systems/容器资源隔离与超卖机制|容器资源隔离与超卖机制]]
- [[wiki/comparisons/systems/线程级隔离 vs 进程级隔离|线程级隔离 vs 进程级隔离]]
- [[wiki/syntheses/systems/Serverless 应用分层与隔离|Serverless 应用分层与隔离]]

## 来源指针

- MicroSandbox 文档：https://docs.microsandbox.dev/
