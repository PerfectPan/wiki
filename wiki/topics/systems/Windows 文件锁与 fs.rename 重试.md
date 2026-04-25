---
title: Windows 文件锁与 fs.rename 重试
type: topic
category: systems
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - windows
  - filesystem
  - node
  - retry
source_refs:
  - legacy-logseq-journals/2022_08_05.md
---
# Windows 文件锁与 fs.rename 重试

## 摘要

Windows 上的杀毒软件或其他进程可能会短时间锁住新创建文件，导致 `fs.rename` 随机报 `EACCES` / `EPERM`。更稳的处理方式不是立刻失败，而是在一段时间窗口内做带退避的重试。

## 关键点

- journal 里的代码片段说明，这类失败常常不是永久错误，而是竞争性锁文件造成的暂时失败。
- 更稳的重试策略通常包含：
  - 仅对特定错误码重试；
  - 限定最大重试时间；
  - 使用逐步退避，而不是忙等；
  - 在重试前确认目标是否已经存在，避免重复覆盖。

## 相关页面

- [[Node]]
- [[文件系统 API]]

## 来源指针

- `legacy-logseq-journals/2022_08_05.md`
