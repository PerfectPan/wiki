# 终端模拟器 / PTY 入门讲解核对记录

- 日期：2026-11-03
- 对象：`wiki/topics/systems/terminal.md` 的入门重写
- 输入：既有主题页与 [[raw/sources/how-terminals-work|How Terminals Work 阅读记录]]；同日用户整理的终端 / 终端模拟器 / PTY 学习笔记（教学叙事，非官方文档）
- 配图：`raw/assets/terminal-emulator-pty-program.png`、`terminal-pty-vs-pipe.png`、`terminal-foreground-handoff.png`、`terminal-csi-osc-decrqpsr.png` 为手绘说明图，用于角色与数据流示意，不是标准文档附图

## 核对过的权威来源

| 主题 | 来源 | 采用点 |
| --- | --- | --- |
| 伪终端端点 | [pty(7)](https://man7.org/linux/man-pages/man7/pty.7.html) | master / slave；程序侧具有终端语义 |
| 终端接口与信号 | [POSIX General Terminal Interface](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap11.html) | 行规范、特殊字符、前台进程组；`Ctrl+C` 条件见 §11.1.9 |
| 终端属性 | [termios(3)](https://man7.org/linux/man-pages/man3/termios.3.html) | `ECHO`、`ICANON`、`ISIG` / `VINTR`；raw 通常关掉多项标志 |
| 控制序列与备用屏幕 | [xterm ctlseqs](https://invisible-island.net/xterm/ctlseqs/ctlseqs.html) | 颜色 / 光标序列；`ESC[?1049h` / `l` 与 Alternate Screen Buffer |
| CSI 呈现状态查询 | [DECRQPSR](https://control-codes.page/csi/decrqpsr/) | `CSI Ps $ w` → DCS DECCIR/DECTABSR；DECRSPS 还原；与 OSC 7501 对照 |
| Shell 与行编辑 | [Bash：What is a shell?](https://www.gnu.org/software/bash/manual/html_node/What-is-a-shell_003f.html)、[Readline Interaction](https://www.gnu.org/software/bash/manual/html_node/Readline-Interaction.html) | shell 不等于终端；交互式 Bash 常由 Readline 做行编辑 |
| 直观演示与既有修正 | [How Terminals Work](https://how-terminals-work.vercel.app/)、[[raw/sources/how-terminals-work]] | 网格、转义、信号、备用屏幕；纠正“cooked 模式等于 shell 行编辑”的过度简化 |

## 笔记里保留与改写的点

- 保留：三角色分工、PTY 相对普通管道的兼容性动机、前台进程组交接（继承 fd + `tcsetpgrp`）、程序发 ANSI / 模拟器画像素、备用屏幕解释退出全屏后滚动历史仍在。
- 改写：不把现代交互式 Bash 的退格、历史、补全说成“全靠内核秘书”；canonical 模式仍帮助简单 `read` / `scanf` 类程序，交互式 shell 通常会把终端调到适合 Readline 的模式。
- 改写：`0x03` 转 `SIGINT` 需 `ISIG` 且匹配 `VINTR`；收到 `SIGINT` 不保证进程退出。
- 旧图 `raw/assets/terminal-tty-shell.png` 不再由本主题页引用，文件按 append-only 保留。

## 未测试项

未实现完整终端模拟器；未逐项对比不同模拟器的控制序列与鼠标协议；未覆盖 Windows 控制台 / ConPTY；未把本机颜色输出当作所有终端都能正确渲染的证明。标准输入是否为 tty 的小实验沿用既有 `tty` / 管道对比结论，见 [[raw/sources/how-terminals-work]]。
