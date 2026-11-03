# Kitty OSC 5522 剪贴板协议 — 来源笔记

- 主题：Kitty 定义的 OSC 5522 剪贴板协议（按 MIME 读写系统剪贴板，含权限与状态应答）
- 访问日期：2026-11-03（Asia/Shanghai）
- 规范所有者：Kitty 项目文档（Kovid Goyal），不是 Ghostty

## 一手来源

| 来源 | URL | 读取内容 |
| --- | --- | --- |
| Kitty 官方文档 *Copying all data types to the clipboard* | https://sw.kovidgoyal.net/kitty/clipboard/ | 帧格式、编码、读/写流程、状态码、密码、paste mode 5522、DECRQM、多工器 `id` |
| Ghostty 1.4.0 发布说明 | https://ghostty.org/docs/install/release-notes/1-4-0 | 「Kitty Clipboard Protocol」一节：实现 OSC 5522（含 paste events），默认读提示、写允许，`clipboard-write-limit-bytes` 默认 64 MiB |
| TDN Clipboard（OSC 52 背景与 OSC 5522 索引） | https://toppk.github.io/revenant/tdn/osc/clipboard/ | OSC 52 语法与风险；Feature ID `osc-5522-clipboard` 指向 Kitty 扩展 |
| control-codes.page Kitty Clipboard | https://control-codes.page/osc/kitty-clipboard/ | 对官方文档的摘要与若干终端实现表；作交叉核对，以 Kitty 文档为准 |

## 核查摘要（相对官方文档）

- 帧：`OSC 5522;metadata;payload ST`，`OSC` 为 `]`，`ST` 为 `\`（文档写作 `\e\\` / BEL 族同类串终结）。
- payload 与若干 metadata 值（`mime` / `name` / `pw`）使用 RFC 4648 §4 标准 Base64，需 padding；非法 Base64 不得静默丢弃字符。
- 读：`type=read` + Base64(MIME 列表或 `.`)；应答 `OK` → 若干 `DATA` → `DONE`，或 `ENOSYS` / `EPERM` / `EBUSY`。
- 写：`type=write` → 若干 `wdata`（每 MIME 分块 ≤4096 字节未编码）→ 空 `wdata` 结束；成功 `DONE`；错误含 `EINVAL` / `EFBIG`（至少接受 64MB）等。
- 能力探测：`CSI ? 5522 $ p`；`Ps` 为 0 或 4 表示不支持。
- paste：`CSI ? 5522 h/l`；用户粘贴时终端可发 MIME 列表与一次性 `pw`。

## 验证记录

- 已阅读上述网页正文（非 Kitty / Ghostty 源码逐行审计）。
- 未在本机运行 Kitty 或 Ghostty 做 OSC 往返抓包；未测 tmux 透传与 `id` 回传。
- control-codes 实现表中 xterm「不支持」、Kitty「支持」与官方叙述一致；Ghostty 1.4 发布说明声明已实现，优先采信发布说明而非未更新的第三方矩阵行。
- Ghostty 作为采用方示例，不作为规范定义来源。

## 未覆盖

- Kitty 源码中的权限 UI 与密码持久化细节
- 各多工器（tmux/zellij）对 OSC 5522 的实际转发行为
- Windows ConPTY 路径
