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

## 身份与鉴权

komo 只有三类身份，区别写在 `users.id` 的前缀上：

| 身份 | id 形式 | 怎么获得 | `verified` |
| --- | --- | --- | --- |
| Google 用户 | `google:<sub>` | 授权码 + PKCE | 1 |
| GitHub 用户 | `github:<id>` | 同上 | 1 |
| 访客 | `guest:<uuid>` | 只提交一个显示名（最多 60 字符） | 0 |

项目和 workspace 的 owner 必须是 Google 身份：`project_owners` 和 `workspaces` 两张表分别带 `CHECK(user_id LIKE 'google:%')` 和 `CHECK(owner_id LIKE 'google:%')`。自托管的 owner 用一次性 setup key 认领，服务端只存这个 key 的 SHA-256（`bootstrapHash`），认领成功后写入 `project_owners`，重复认领返回 409。

### 会话

服务端签发时生成一个双 UUID 的 token，数据库里只存它的 SHA-256（`sessions.token_hash`），并把会话绑定到具体项目（`sessions.project`）。有效期在代码里写成 100 年，注释给的理由是「Sessions should not force reviewers back through sign-in」，只有登出（`DELETE /me`）会删掉这一行。

每个请求显式带 `Authorization: Bearer <token>`，服务端按 token 哈希 + 项目 + 未过期查会话。浏览器侧同时存两处：HTTPS 下写 `__Host-bc-session-...` cookie，配置了 `sessionDomain` 时换成 `__Secure-` 加 `Domain`；另外写一份 localStorage。cookie 的 `Max-Age` 上限是 400 天，服务端会话比它长，所以续期实际上靠 localStorage，请求本身是 `credentials: "omit"`，不依赖浏览器自动带 cookie。

token 本身是两段随机 UUID，是不透明串，不含任何身份字段，也不是 JWT。解身份就是一次查表：按 `SHA-256(token)` 命中 `sessions.token_hash`，再 join `users`；会话作用域同时受请求里的 `project` 参数和 `sessions.project` 列约束，所以一个项目的 token 拿到另一个项目查不到行。没带 header、过期、项目不匹配这几种失败返回的 401 文案不区分彼此。命中之后，服务端只把 `id`、`name`、`verified`、`avatarUrl`、`accentColor` 五个字段当作调用方身份。

服务端只认 `Authorization` 头，没有基于 cookie 的会话校验路径：那个 cookie 是客户端自己读写的存储位置，不是凭据通道。好处是跨站请求不会被浏览器自动带上凭据，也就没有靠自动携带 cookie 冒充身份的请求面；代价是 token 必须能被页面脚本读到，所以宿主站点必须可信。

登录走标准授权码 + PKCE：服务端存 `state` 的哈希和 `code_verifier`，授权时用 S256 challenge；回调时除了查 `state`，还要比对 `__Host-comments-oauth` 这个 HttpOnly cookie（`timingSafeEqual` 比对、10 分钟过期、`DELETE ... RETURNING` 用完即删），用于确认完成流程的浏览器就是发起流程的那一个。

一轮登录里 token 的完整路径：

1. 站点页面（origin A）点击登录，挂件先开一个 `about:blank` 弹窗，再 `POST /auth/google/start`；服务端把 `state`、`verifier`、`exchange` 三个随机串存进 `oauth_states`（只存 state 和 exchange 的哈希），返回一个授权 URL。
2. 弹窗导航到评论 API（origin B）的 `/auth/google/authorize`；服务端 302 到 Google，`redirect_uri` 用的是 B 的 `/auth/google/callback`，同时在 B 上种下 `__Host-comments-oauth`。
3. Google 在弹窗里完成授权，把弹窗送回 B 的回调地址。
4. 服务端比对 state 与 cookie、用 `DELETE ... RETURNING` 消费掉那一行、拿 `code_verifier` 去换 access token、取 userinfo、写 `users` 和 `sessions`，得到原始 token。
5. 回调页在 origin B 上返回一段 HTML，内联脚本执行 `window.opener.postMessage({type, token, user}, <origin A>)` 然后关窗；页面 CSP 是 `default-src 'none'`，oauth cookie 同时清零。
6. 站点页面的监听器校验 `event.origin` 是 B、`event.source` 是它开的那个弹窗、`type` 正确、`user.verified === true`，通过后 `api.save({token, user})`，写进 cookie 和 localStorage，之后请求带 `Authorization`。

token 不进 URL、不 redirect 回站点、也不靠跨站 cookie：回调页在 B 上，与站点跨源，只能通过 `postMessage` 交给开启它的那个窗口，目标 origin 是发起登录时记下的那个（CLI 登录时换成 `http://127.0.0.1:<高位端口>`）。

回调地址永远在 API 域上，与站点无关：托管版固定是 `https://komo.offbr.co/auth/google/callback`；自托管要用自己 Worker 或 Node 服务的地址，并加进 Google OAuth 客户端的授权回调地址；client id 和 secret 存在 API 的环境变量里（没配时 `/auth/*/start` 返回 503 `Sign-in is not configured.`），所以站点方不需要自己的 Google Cloud 项目。你的站点域在这个流程里只出现两次：写进 `oauth_states.origin` 当作 `postMessage` 的目标，以及要过站点白名单。

CLI 用的是同一套凭据，区别只在怎么拿到：`komo login` 在本机起一个临时 HTTP 服务，浏览器登录后用 `postMessage` 把 token 交给它，它再写到仓库之外的 `~/.config/komo`（目录 0700、文件 0600）。取 token 的顺序是环境变量 `KOMO_TOKEN` 优先，其次是这个文件，两者都没有就报 `No saved session. Run komo login, or set KOMO_TOKEN.`。CLI 的每个请求除了 `Authorization`，还带一个 `Origin` 头，因为站点审批检查对它同样生效。

### 登录入口由服务端下发

挂件要先问服务端给哪些登录方式：`GET /config` 返回 `google`、`github`、`guests`、`guestResolve`、`private` 五个开关（`github` 只有配了 GitHub 的 client id 和 secret 才为真，`guests` 在项目是 private、`allowGuests` 为 false 或 owner 还没认领时为假）。

访客这条路完全不跳转：填一个名字，`POST /auth/guest {name}` 直接返回会话，挂件存下来就用。Google 和 GitHub 那条是弹窗，不是把你的页面导航走：挂件先 `window.open("about:blank", "branch-comments-signin", "popup,width=600,height=720")` 占一个空白窗，拿到 `start.url` 之后再把弹窗指过去，站点本身不动。先开空窗是因为 `window.open` 必须落在用户点击的同步调用栈里，放到等待 `auth/*/start` 返回之后再开就会被浏览器当成弹窗拦掉；`start` 请求失败时这个空窗会被关掉并把错误抛回界面。空白窗在导航前继承的是站点自己的源，所以监听器除了比对 `event.source`，还要比对 `event.origin` 是 API 的源，否则同一个空窗就能伪造消息。只有需要已验证身份的动作才会要求登录，比如关闭会话（`guestResolve` 打开时访客也可以关）。

### 谁能看到评论

- **站点层**：请求的 `Origin` 要落在项目已批准的站点列表里（支持 `https://*-preview.example.com` 这类最左标签单层通配，通配不跨点），localhost 直接放行。不在列表里返回 403 `site_not_approved`，同时不下发 CORS 头。
- **项目层**：项目默认公开，能打开该站点的人都能读写。切成 `private` 后每次读写都要过 `requireMember`，它查两件事：`verified` 为真且 id 以 `google:` 开头，然后再看 `project_owners` 和 `project_access` 里有没有这个用户。所以访客身份进不了私有项目，GitHub 身份也进不了——后一条是从代码读出来的，没有实际跑过。
- **邀请**：`project_invites` 存邮箱、token 哈希和 7 天过期时间，接受邀请时用登录账号的邮箱匹配，每个项目最多 50 条待接受邀请。

### 限流和配额

`limit()` 按时间桶写 `rate_limits` 表：每个项目每天 10 万次请求、非 GET 请求每 IP 每分钟 90 次、项目每天写入数（托管 500，自托管默认 10000）、托管服务全局每天 10 万次；开了 `KOMO_HOSTED` 时前面还有一层 Cloudflare 的 `EDGE_LIMIT` 按 IP 限流。评论数、字节数、成员数和表情数这些配额由数据库触发器兜底，超了抛 `komo_quota_exceeded`。

另外每个路由的请求体有字段白名单：`body()` 按路径规定允许出现的字段，多一个字段就返回 400。CLI 的 `KOMO_TOKEN` 就是同一个评审者的会话 token，README 写明它不绕过 owner 检查。

## 使用限制

- **托管额度**：每个 Google 账号 3 个项目、每个项目 250 条存储评论（含回复）、10 MiB 逻辑存储、每天 500 次写请求、请求体 16 KiB。beta 期间免费，没有付费升级路径。删除或解析评论不返还配额，官方给的回收方式是先导出、再清掉已解析会话。
- **身份**：访客只填名字就能评论，但这个名字不是已验证身份，之后用 Google 登录也不会把旧的访客评论转成已登录账号；私有项目的门槛和邀请机制见上一节。
- **可见范围**：项目默认是「有链接就能访问」，owner 可以改成只允许被邀请的 Google 账号。站点是否允许嵌入由已验证的站点地址控制，成员关系控制的是私有反馈的访问；这两件事和仓库权限互不相干。
- **会话**：挂件用的是 `mode: "open"` 的 shadow root，只隔离样式，宿主页面自己的脚本仍能读到它；会话长期有效（服务端 100 年、cookie 上限 400 天），所以凭据的暴露面跟着宿主站点走。开 `sessionDomain` 会把会话共享给同一个父域下的所有主机，包括无关应用，官方不建议对不可信的预览环境开启。挂在页面上的客户端凭据和缓存的评论对宿主站点自己的脚本可见，所以只应该装在自己信任的站点上。
- **部署环境**：官方建议只在预览和开发环境挂载，用 `enabled` 接框架的公开环境变量；beta 期间的生产使用没有承诺。
- **附件**：不支持行内文件附件；头像只保存有上限的表示形式。
- **移动端**：挂件会适配小视口，但精确点选和拖拽在指针设备上体验更好。
- **自托管**：Cloudflare 路线用 `komo init --self-host`，CLI 建 D1、跑迁移、部署 Worker；Node 路线需要 PostgreSQL 和允许的预览 origin。自托管不套用托管额度（默认每天 10000 次写），但受自己账号的限额和计费约束。两条路线都要求先完成 Google owner 认领，之后才能开放访客评论。
- **服务端源码**：MIT，服务端全部在公开仓库里（`server/` 下的 Worker 入口、校验、workspace 管理、项目成员管理、站点管理、导入导出、迁移和 `wrangler.jsonc`），npm 包里也带一部分服务端源码加打包好的 `dist/node.mjs`。托管服务就是这套代码加 `KOMO_HOSTED=true`。但线上**配置**不在仓库里（项目清单、Google client secret、D1 数据都看不到），也没有对「线上跑的是哪个提交」的可验证声明。
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
- <https://github.com/tjcages/komo>（快照 `6fb75d7b`）：`src/anchors.ts`、`src/agent-prompt.ts`、`src/polling.ts`、`src/api.ts`、`server/index.ts`、`server/validation.ts`、`server/project-management.ts`、`server/migrations/0001_comments.sql`、`server/migrations/0004_workspaces.sql`、`server/migrations/0007_revisions.sql`、`cli/agent.mjs`、`cli/workflow.mjs`、`docs/performance.md`
- <https://www.npmjs.com/package/@tjcages/komo>：0.7.0（2026-09-29）
- `raw/assets/komo-architecture-sketch.png`：按本页内容生成的手绘风格示意图（codex 图像生成，1664×936），不是 komo 官方素材；图中的调用次序以本页正文和 `raw/sources/komo.md` 的源码记录为准。
