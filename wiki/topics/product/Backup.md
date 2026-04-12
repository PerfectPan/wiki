---
title: Backup
type: topic
category: product
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - backup
source_refs:
  - raw/sources/Backup.md
---
# Backup

- ```tex
  \ResumeItem{飞书开发者工具优化}
  \noindent{\textbf{项目简介}}\newline
  承载小程序/小组件/H5 应用的调试、预览和发布功能的飞书开发者工具，从武汉团队接手后发现整个项目很多功能不可用，用户负反馈高，需要整体围绕稳定性进行优化。
  \noindent{}\newline
  \noindent{\textbf{主要工作}}
  \begin{itemize}
  \item 解决了大量历史遗留问题，如小程序调试面板冗余信息过多、\ResumeUrl{https://open.feishu.cn/document/uYjL24iN/ukDOzYjL5gzM24SO4MjN}{体验评分面板}不可用、真机调试模块部分不可用等。
  \item 设计实现静态资源模块，内置应用模版和基础库代码，并支持远程热更新推送，解决网络资源拉取带来的问题。
  \item 项目埋点梳理，协助建设数据大盘，完成线上 JS Error 的监控，基于监控发现若干代码逻辑问题并完成修复。
  \end{itemize}
  \noindent{\textbf{项目结果}}\newline
  所有基础功能修复完成，2022 全年线上问题逃逸率从 60\% 降低至 30\%。后续为了解决当前项目架构混乱和开发者对于编辑器的优化诉求，还设计了基于 \ResumeUrl{https://github.com/opensumi/core}{OpenSumi} 的升级方案。
  ```

## Source Pointers

- `raw/sources/Backup.md`

