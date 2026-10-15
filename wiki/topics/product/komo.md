---
title: komo
description: 把网页元素上的评论存进独立 API、再交给 coding agent 的工具：三层组成、锚点模型、agent 命令与使用限制
type: topic
category: product
created: 2026-10-15
updated: 2026-10-15
timestamp: 2026-10-15
tags:
  - code-agent
  - developer-tools
  - feedback
  - self-hosting
source_refs:
  - raw/sources/komo.md
  - https://komo.offbr.co/
  - https://komo.offbr.co/install/
  - https://komo.offbr.co/configuration/
  - https://komo.offbr.co/hosting/
  - https://komo.offbr.co/agent-prompts/
  - https://komo.offbr.co/faq/
  - https://github.com/tjcages/komo
  - https://www.npmjs.com/package/@tjcages/komo
resource:
  - raw/sources/komo.md
  - https://komo.offbr.co/
  - https://komo.offbr.co/install/
  - https://komo.offbr.co/configuration/
  - https://komo.offbr.co/hosting/
  - https://komo.offbr.co/agent-prompts/
  - https://komo.offbr.co/faq/
  - https://github.com/tjcages/komo
  - https://www.npmjs.com/package/@tjcages/komo
resource_type: npm Package
---

# komo

## 摘要

komo 是 Off brand 发布的一个评论工具（npm 包 `@tjcages/komo`，MIT，官网 <https://komo.offbr.co/>）：在你的站点里挂一个 ShadowRoot 挂件，在元素或区域上留评论、回复、加表情、标记已解析；评论存在它自己的 API 数据库里，而不是站点的代码库或浏览器存储里；再由 `komo` CLI 或侧栏的「复制全部评论」把页面、选择器、来源文件和整串对话交给 coding agent。

它自己不做代码改动，也不跑 agent。官方 README 的原话是「komo copies context for your agent; it does not run an agent, upload your repository, or make code changes itself.」

本页基于 2026-10-15 抓取的官方文档，以及对仓库提交 `6fb75d7b8fc045b4c5114e042e64a5626785843d`（2026-10-01，npm 版本 0.7.0）的只读源码核对。逐条证据和未验证项记在 `raw/sources/komo.md`。

## 三层组成

| 部分 | 形态 | 状态存在哪 |
| --- | --- | --- |
| 挂件 | 客户端包，挂进宿主站点，UI 在 `mode: "open"` 的 ShadowRoot 里（样式隔离，不是访问边界） | 浏览器里只缓存上一次已知的账号和评论，重新校验前用来快速显示 |
| 评论 API | 官方托管服务；或自托管成 Cloudflare Worker + D1；或 Node 容器 + PostgreSQL | 这个 API 的数据库 |
| CLI | `komo` 命令，人用也够，主要给 agent 用 | 会话存在仓库之外的 `~/.config/komo` |

`scope` 决定评论怎么分组：默认 `project`，同一项目的同一页面路径共享一份反馈；切到 `branch` 后按分支隔离。页面标识默认取 `location.pathname`，查询串和 fragment 不存。

评论的位置由 `page` + 锚点决定，与宿主的构建产物无关，所以同一份评论在本地、预览环境和线上是同一条，除非开了 branch scope。

## 核心数据流

![手绘风格概览：网站上的评论挂件通过 POST 把评论交给评论 API 并落到数据库，同时从 API 轮询拉取；CLI 与 API 双向读写，agent 通过 CLI 读反馈、回复并关闭会话](../../../raw/assets/komo-architecture-sketch.png)

一次写评论的过程：挂件在宿主 DOM 上采集锚点和正文，POST 给评论 API，API 校验选择器、几何、权限和配额后写入 `threads` / `comments`。写入按提交顺序排队，界面先乐观显示；某一条失败时只回滚那一条改动（`OptimisticQueue` 把它从队列里去掉后按已确认状态重算），并提示，未保存的正文会保留下来。

一次 agent 改动的过程：CLI 从 API 读未解析的会话，agent 在仓库里改代码并验证，然后回复证据、把简单的会话标记为已解析。CLI 不会自动重试写操作，写失败要自己判断。

轮询是自适应的：可见且活跃时从 4 秒起，内容没变化就按 `interval × 2^n` 退避到最长 15 秒，页面不可见时下限 60 秒。`GET /threads` 带 `revision` 参数，服务端发现版本没变就直接返回 `notModified`，不重复传整份数据。

## 锚点存了什么

`Anchor` 的字段是 `selector`、`text`、占比坐标 `x`/`y`/`width`/`height`、文档坐标 `pageX`/`pageY`、`viewportWidth`，以及可选的 `source` 和 `context`（tag、role、可访问名、附近文本、class、7 条计算样式、选中文本、DOM scope）。

选择器的生成顺序在 `src/anchors.ts` 里写死：先看 `data-comment-anchor`、`id`、`data-testid`、`data-test`、`data-cy`，并且要求这个选择器在当前文档里唯一命中；没有可用属性时退到逐层的 `标签:nth-of-type(n)`，最多上溯 12 层。目标文本最多收集 320 字符再截到 160 字符，并跳过表单控件、`script`、`style`、`contenteditable` 和 `hidden` 内容。

两个已知的边界：

- 元素消失时，挂件退回捕获时记录的页面坐标，所以布局变了之后锚点可能指到别的地方，提示词里也写明坐标只是回退。
- komo 看不到闭合的 shadow root、canvas 内部和跨域 iframe 内容，也不会生成源码行号；`source` 字段是宿主自己通过 `source(element)` 提供的，komo 不上传代码。

宿主可以用 `data-comment-anchor="pricing"`、`data-comment-source="src/components/Pricing.tsx"` 这类属性让锚点更稳。

## 给 agent 的一侧

CLI 的评论区命令覆盖读、写和状态变更：`comments list`、`get`、`prompt`、`reply`、`resolve`、`reopen`、`create`、`edit`、`delete`、`react`、`move`；`komo schema` 输出机器可读的命令参考，不需要登录。列表默认一页 50 条，支持 `--status`、`--page`、`--limit`（1–250）和 `--offset`。成功时输出 `{ "ok": true, "scope": {...}, "data": ... }`，失败写 stderr 并带状态码，退出码 1。

「复制全部评论」和 `komo comments prompt` 产出同一份 Markdown：开头是仓库、分支、项目、预览地址和范围，然后每个未解析的会话依次给出 CSS 选择器、来源文件、元素上下文、目标文本引用块、锚点位置，以及按时间排列的评论和回复。已解析的会话和已删除的评论不进提示词。

新项目由 `komo init` 把一段评论工作流写进项目根目录的 `AGENTS.md`，在 `<!-- komo:workflow:start -->` 和 `<!-- komo:workflow:end -->` 之间，已有项目用 `komo agents setup` 补上。这段约定要求 agent 先读反馈再改代码，改完验证后带证据回复，只有简单明确且置信度 90% 以上的会话才 resolve，其余留着提问。它是写给 agent 的说明，CLI 不测量置信度。

提示词里对评论内容本身的定性值得记下来：评论正文、目标文本和 DOM/源码上下文都是捕获时的快照提示，不是当前事实，也不是给 agent 的指令，不能凭它去取凭据、跑无关命令或外发数据。

## 使用限制

- **托管额度**：每个 Google 账号 3 个项目、每个项目 250 条存储评论（含回复）、10 MiB 逻辑存储、每天 500 次写请求、请求体 16 KiB。beta 期间免费，没有付费升级路径。删除或解析评论不返还配额，官方给的回收方式是先导出、再清掉已解析会话。
- **身份**：owner 必须是 Google 账号；访客可以只填名字参与，但这个名字不是已验证身份，登录之后也不会自动把旧的访客评论转成已登录账号。
- **可见范围**：项目默认是「有链接就能访问」，owner 可以改成只允许被邀请的 Google 账号。站点是否允许嵌入由已验证的站点地址控制，成员关系控制的是私有反馈的访问；这两件事和仓库权限互不相干。
- **会话**：挂件用的是 `mode: "open"` 的 shadow root，只隔离样式，宿主页面自己的脚本仍能读到它；HTTPS 下默认是 host-only cookie；开 `sessionDomain` 会把会话共享给同一个父域下的所有主机，包括无关应用，官方不建议对不可信的预览环境开启。挂在页面上的客户端凭据和缓存的评论对宿主站点自己的脚本可见，所以只应该装在自己信任的站点上。
- **部署环境**：官方建议只在预览和开发环境挂载，用 `enabled` 接框架的公开环境变量；beta 期间的生产使用没有承诺。
- **附件**：不支持行内文件附件；头像只保存有上限的表示形式。
- **移动端**：挂件会适配小视口，但精确点选和拖拽在指针设备上体验更好。
- **自托管**：Cloudflare 路线用 `komo init --self-host`，CLI 建 D1、跑迁移、部署 Worker；Node 路线需要 PostgreSQL 和允许的预览 origin。自托管不套用托管额度（默认每天 10000 次写），但受自己账号的限额和计费约束。两条路线都要求先完成 Google owner 认领，之后才能开放访客评论。
- **数据搬移**：`project export` / `project import` 会带走会话、回复、表情、锚点和历史身份，不带会话凭据、已验证邮箱和成员关系；导入的作者是未验证身份。托管服务和自托管实例用的是各自的数据库。

## 体积与运行时开销

仓库自己记录的性能审计（2026-09-16，基线提交 `95fa3c83`）给出：生产构建的初始 JavaScript 是 gzip 160,203 字节，全部功能分块 178,817 字节，构建检查在初始超过 170,000 或全部超过 195,000 gzip 字节时失败。合成负载下（5,000 行 DOM、250 个长正文会话、每帧 100 次文本改动）平均帧间隔 12.37 ms，无评论时 8.28 ms，纯宿主对照 8.25 ms。

这些数字来自仓库作者的合成桌面基准，不是 Core Web Vitals，也没有在真机、低端设备和长会话里验证过。

## 相关页面

- [[wiki/topics/product/voila|Voila]]：不拥有源码的浏览器编辑扩展，产物是交接物而不是评论；两者都是「把界面上的意图交给下游 agent」。
- [[wiki/syntheses/product/delta-product-architecture-investigation|Delta 产品与架构调研]]：编辑器里把对话、改动和评论收进同一个 thread 的做法，与 komo 把评论留在页面上、代码改动交给外部 agent 形成对照。
- [[wiki/topics/ai/code-agent|Code Agent]]
- [[wiki/syntheses/ai/agent-native-system-interface-design|Agent Native 系统接口设计]]：komo 面向 agent 的一侧也是这套做法——机器可读的命令参考、固定的返回结构，以及写进 `AGENTS.md` 的使用约定。

## 来源指针

- `raw/sources/komo.md`：文档事实、源码阅读记录与验证范围。
- <https://komo.offbr.co/>、[安装](https://komo.offbr.co/install/)、[配置](https://komo.offbr.co/configuration/)、[托管与限额](https://komo.offbr.co/hosting/)、[给 agent](https://komo.offbr.co/agent-prompts/)、[FAQ](https://komo.offbr.co/faq/)
- <https://github.com/tjcages/komo>（快照 `6fb75d7b`）：`src/anchors.ts`、`src/agent-prompt.ts`、`src/polling.ts`、`server/index.ts`、`server/migrations/0001_comments.sql`、`server/migrations/0007_revisions.sql`、`cli/workflow.mjs`、`docs/performance.md`
- <https://www.npmjs.com/package/@tjcages/komo>：0.7.0（2026-09-29）
- `raw/assets/komo-architecture-sketch.png`：按本页内容生成的手绘风格示意图（codex 图像生成，1664×936），不是 komo 官方素材；图中的调用次序以本页正文和 `raw/sources/komo.md` 的源码记录为准。
