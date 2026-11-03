# DECRQPSR — 来源笔记

- 主题：Request Presentation State Report（CSI 查询呈现状态，DCS 应答 / DECRSPS 还原）
- 访问日期：2026-11-03（Asia/Shanghai）
- 页面：https://control-codes.page/csi/decrqpsr/

## 摘要

- 请求：`CSI Ps $ w`；`Ps=1` → DECCIR（`DCS 1 $ u … ST`），`Ps=2` → DECTABSR（`DCS 2 $ u … ST`）。
- 还原：DECRSPS `DCS Ps $ t … ST`。
- 依据 DEC STD 070 / VT510；xterm 实现；libghostty-vt 等多项现代实现在对照用例中无应答。
- 用途：对照 CSI/OSC/DCS 分层与 OSC 7501（程序业务状态）差异；折叠进 `wiki/topics/systems/terminal.md`，不单独开大页。

## 验证记录

已读 control-codes 页正文与 Support 表；未在本机对 xterm/Ghostty 复现用例 DECRQPSR-1…6。
