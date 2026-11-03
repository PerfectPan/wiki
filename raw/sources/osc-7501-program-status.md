# OSC 7501 Program Status Protocol — 来源笔记

- 主题：程序向终端报告运行状态（idle / working / blocked / done / error / clear）
- 访问日期：2026-11-03（Asia/Shanghai）
- 规范开创：Ghostty / Mitchell Hashimoto；修订 0.4（摘要页记为 2026-10-10）

## 一手与核对来源

| 来源 | URL | 读取内容 |
| --- | --- | --- |
| control-codes 提案摘要（rev 0.4） | https://control-codes.page/proposals/osc-7501/ | 帧格式、记录与 id、状态、键、探测、安全与上限、与 OSC 9;4 / 133 / 通知等关系 |
| Ghostty PR #14560 | https://github.com/ghostty-org/ghostty/pull/14560 | libghostty-vt 实现；“first net-new terminal specification pioneered by Ghostty”；宿主经 `GHOSTTY_TERMINAL_OPT_PROGRAM_STATUS` 持有记录；Ghostty GUI 暂忽略展示；合并于 2026-10-06 |
| phux 文档（实现方复述） | https://docs.phux.sh/program-protocol | 按 rev 0.4 应用；解析器称来自 libghostty；phux 展示与优先级细节属产品层 |
| Ghostty 1.4.0 发布说明 | https://ghostty.org/docs/install/release-notes/1-4-0 | Terminal Capabilities：解析 OSC 7501；libghostty 可解析，Ghostty GUI 暂忽略 |

规范正文曾以 gist 发布（PR 引用 https://gist.github.com/mitchellh/7acae3abd8355c1c00287d67e96c913a）；本次以 control-codes 对 0.4 的摘要与 PR 描述为准，未逐字核对 gist 全文。

## 核查摘要

- 报告：`OSC 7501 ; key=value : key=value … ST`；探测：`OSC 7501 ; ? ST`，应答以 `?` 开头并可带 `states=` / `kinds=`。
- 必填 `state`；未知/缺失 state 的报告整条忽略。
- 状态：`idle`、`working`、`blocked`、`done`、`error`；`clear` 删除记录（及子树）。
- `kind`（仅 blocked）：`permission` / `question` / `auth`；`progress` 0–100 或省略（不定进度）；`msg`/`title` 为 Base64 UTF-8，解码后不得含控制字符。
- 记录按 `id` 路径保存在终端（窗/标签/窗格）侧，非屏幕缓冲；RIS 清空，DECSTR 不动；切备用屏幕不动。
- libghostty-vt：校验后交给宿主；自身不长期存档；仅在宿主设置回调时回答 `?`。

## 验证记录

- 已读上述网页与 PR API 正文；未运行 Ghostty / phux，未对 PTY 做 OSC 往返抓包。
- 未审计 libghostty 源码行级实现；实现细节以 PR 与 control-codes / phux 文档交叉核对。
- 展示 UI（侧栏、通知、图标）留给终端产品，本笔记不把任何一家的 UI 写成规范要求。

## 未覆盖

- gist 原文与 0.1–0.3 全文 diff
- 多工器透传行为
- Windows ConPTY

## 配图

手绘：`raw/assets/osc-7501-report-path.png`、`osc-7501-states-lifecycle.png`、`osc-7501-report-sequence.png`（说明报告路径、状态生命周期、报告/探测时序；CSI/OSC/DCS 分层见 `terminal-csi-osc-decrqpsr.png`，本页不重复）。
