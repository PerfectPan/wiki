<!-- source: https://michaellivs.com/blog/reverse-engineering-claude-generative-ui -->
<!-- author: Michael Liv; published: 2026-03-13; accessed: 2026-10-08 -->

# Michael Liv 的 Claude Generative UI 文章与 Pi 实现证据

本记录用于回查文章判断和后续实现。正文说明见 [[wiki/topics/ai/pi-generative-ui]]。原文、官方产品能力和开源复现是三个不同的证据范围。

## 来源与版本

- [原文](https://michaellivs.com/blog/reverse-engineering-claude-generative-ui)：页面标注 2026-03-13。
- [pi-generative-ui](https://github.com/Michaelliv/pi-generative-ui)：核查时默认分支 HEAD 为 `d1abf2cb38fbf54c4b91d06677c700193d495887`，提交时间 2026-06-03T21:47:29Z。
- [v0.3.0 release](https://github.com/Michaelliv/pi-generative-ui/releases/tag/v0.3.0)：发布于 2026-06-03T21:37:37Z，标签对应 `67e575add283ccb0ceb6d0b5affe5eb71ce9cd08`。核查时 GitHub releases 返回的最新公开版本为此版本。
- [v0.2.1 release](https://github.com/Michaelliv/pi-generative-ui/releases/tag/v0.2.1)：2026-03-15 发布，修复 SVG 样式缺失导致的颜色显示问题。
- `package.json` 为 0.3.0，但 `CHANGELOG.md` 的小节仍标为 unreleased。发布时间采用 GitHub release，不根据这行旧标题推断尚未发布。

## 文章证据分级

| 文章位置 | 作者记录的内容 | 证据限制 |
| --- | --- | --- |
| Part 1 / The Tool, Not the Markdown；The read_me Pattern | 工具参数承载 HTML，按模块读取设计说明 | 属于作者观察；Pi 公开源码能验证复现方式，不能据此证明 Claude 当前私有接口 |
| Part 1 / Not an Iframe | 通过流式显示、CSS 变量和模型自述推断直接注入父页面 | 推理不足；这些现象不能排除 iframe 与宿主消息桥接 |
| Part 3 / Attempts 1–4 | 比较整页替换、innerHTML、按节点数追加和 morphdom | 记录作者的实现过程，不是本次性能复现 |
| Part 4 / Extracting the Design Guidelines | 作者称从自己会话的工具响应中提取并去重说明 | 本次没有访问作者原始会话，不能独立验证其“逐字一致”的主张 |
| What's Next | sendPrompt、持久窗口等后续设想 | 不能按已实现能力收录；当前版本已主动取消业务事件返回 agent |

## 固定源码位置

以下链接均固定到 `d1abf2c`。

| 核查对象 | 位置 | 观察 |
| --- | --- | --- |
| 入口与参数流 | [index.ts:64–107](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.pi/extensions/generative-ui/index.ts#L64-L107) | 订阅 message_update，处理 start/delta/end，从部分 arguments 取 widget_code |
| 设计说明 | [guidelines.ts:775–801](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.pi/extensions/generative-ui/guidelines.ts#L775-L801) | 按五个模块组合公共与专用章节，用 Set 去重 |
| 布尔前置条件 | [index.ts:171–177](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.pi/extensions/generative-ui/index.ts#L171-L177) | 只判断传入布尔值，不读取 read_me 调用历史 |
| 窗口状态 | [session.ts:31–104](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.pi/extensions/generative-ui/session.ts#L31-L104) | 窗口、最新 HTML、定时器、finalized/closed 保存在内存；等 ready 后推送 |
| 页面数据流 | [runtime/index.ts:15–52](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.pi/extensions/generative-ui/runtime/index.ts#L15-L52) | 监听 content，更新 root；final 时异步运行脚本，只在控制台记录脚本错误 |
| 脚本顺序 | [runtime/morph.ts:14–71](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.pi/extensions/generative-ui/runtime/morph.ts#L14-L71) | DOM 差异更新；外部 script 逐个等待 load，再处理后续 script |
| 工具完成 | [index.ts:185–217](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.pi/extensions/generative-ui/index.ts#L185-L217) | 复用窗口，交付最终内容即返回；没有页面渲染成功回执 |
| 消息定义和分派 | [protocol.ts:16–65](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.pi/extensions/generative-ui/protocol.ts#L16-L65)、[rpc.ts:38–69](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.pi/extensions/generative-ui/rpc.ts#L38-L69) | PageToHost 只有 RpcCall；非协议用户数据被忽略。类型守卫主要检查 type，并非完整参数校验 |
| 写入边界 | [features/svg-saver.ts:26–43](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.pi/extensions/generative-ui/features/svg-saver.ts#L26-L43) | 已注册 svg.copy/svg.save；保存先开系统对话框，再 writeFile |
| 运行时打包 | [build.mjs:28–54](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.pi/extensions/generative-ui/build.mjs#L28-L54) | esbuild 打包页面代码，脚本内嵌到 HTML；此 shell 未声明 CSP |
| 清理 | [index.ts:239–245](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.pi/extensions/generative-ui/index.ts#L239-L245) | Pi session shutdown 时关闭仍管理的窗口 |

## 验证范围

- 已阅读 `tests/session.test.ts`、`tests/integration.test.ts` 及 CI 配置；未安装或运行 Pi/Glimpse，未执行上游测试，未复现窗口启动耗时或视觉效果。
- [CI 配置](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.github/workflows/test.yml#L9-L65) 覆盖三个系统与 Node 20/22，但 Linux/Windows 安装跳过 native build。不能写成所有原生窗口都已验收。
- [集成测试入口](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/tests/integration.test.ts#L7-L15) 在原生二进制缺失且没有强制开关时跳过。这里记录测试的覆盖条件，不报告测试通过。
- 未检查底层 Glimpse 的全部沙箱、网络或平台权限实现；“扩展 shell 未声明 CSP”的观察不延伸为“底层没有任何隔离”。

## RSS 来源核对

2026-10-08 检查原文 HTML：`rel="alternate"`、`type="application/rss+xml"` 的链接与导航 RSS 链接均指向 [https://michaellivs.com/rss.xml](https://michaellivs.com/rss.xml)。该 URL 返回 HTTP 200，Content-Type 为 `application/xml`，channel title 为 `/dev/michael`，包含 41 个 item。

目标文章的 item link/guid 为 `https://michaellivs.com/blog/reverse-engineering-claude-generative-ui/`，pubDate 为 `Fri, 13 Mar 2026 00:00:00 GMT`。rss-summary 的真实解析器通过 `feeds test --url ... --name '/dev/michael' --tags 'Articles,Blog'` 返回 41 items；此验证不发送摘要。

## 工具接口与设计说明

- [index.ts:14–36](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.pi/extensions/generative-ui/index.ts#L14-L36)：ReadMeParams 只有必填 modules 数组；ShowWidgetParams 的必填字段为 i_have_seen_read_me、title、widget_code，width/height/floating 可选。没有 loading_messages，没有 minItems、正数范围或 snake_case 正则。
- [index.ts:111–130](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.pi/extensions/generative-ui/index.ts#L111-L130)：读取说明的模型提示与执行返回；content.text 直接使用 getGuidelines 的结果，details 记录模块。
- [index.ts:146–217](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.pi/extensions/generative-ui/index.ts#L146-L217)：显示工具的适用场景、前置调用说明、代码片段要求和当前返回结构。
- [guidelines.ts:25–84](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.pi/extensions/generative-ui/guidelines.ts#L25-L84) 与 [775–801](https://github.com/Michaelliv/pi-generative-ui/blob/d1abf2cb38fbf54c4b91d06677c700193d495887/.pi/extensions/generative-ui/guidelines.ts#L775-L801)：公共设计规则、五类模块和共享章节去重。
- 原文 Part 1 报告 Claude show_widget 的四个字段，包含 1–4 条 loading_messages；Part 4 的记录使用 visualize:read_me。
