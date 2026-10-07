# How Terminals Work 阅读记录

- 来源：https://how-terminals-work.vercel.app/
- 访问日期：2026-10-07
- 读取方式：网页需要 JavaScript 渲染，已在浏览器读取 01–14 节的正文与演示说明；未逐个测试所有交互。

## 采用的内容与补充核对

| 位置 | 采用的内容 | 补充或修正依据 |
| --- | --- | --- |
| 01 The Grid Model、02 What's in a Cell? | 字符网格、颜色和样式 | 不把“一字符一格”当成通则；[wcwidth(3)](https://man7.org/linux/man-pages/man3/wcwidth.3.html) 说明显示列宽 |
| 03 Escape Sequences、04 Input Goes Both Ways | 输出控制序列与输入按键编码 | [xterm](https://invisible-island.net/xterm/ctlseqs/ctlseqs.html) 核对 ESC、颜色、方向键及鼠标模式 |
| 05 Signals | Ctrl+C 字节经过终端处理后产生信号 | 需满足 ISIG / VINTR 条件，目标是前台进程组；[POSIX §11.1.9](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap11.html)、[termios(3)](https://man7.org/linux/man-pages/man3/termios.3.html) |
| 06 Raw vs Cooked Mode | canonical 与 non-canonical 输入处理 | 教程把 shell 和 cooked mode 对应得过于绝对；现代交互式 shell 的行编辑由 Readline / 自身编辑器处理，[Readline 文档](https://www.gnu.org/software/bash/manual/html_node/Readline-Interaction.html) 与 termios 分别解释两层职责 |
| 07 The Round Trip、14 Terminal Vocabulary | 模拟器、PTY、shell 与程序的双向输入输出 | [pty(7)](https://man7.org/linux/man-pages/man7/pty.7.html) 核对端点；PTY 带有终端语义，不能等同于普通 pipe |
| 09 The Alternate Screen Buffer、11 State Management | 备用屏幕与应用自己的状态 | xterm 核对 1049 模式；“应用状态归应用”不表示终端没有光标、样式和屏幕状态 |

## 未测试项

已在本地 macOS 用 `pty.openpty()` 创建伪终端，把 slave 作为 `tty` 的标准输入：返回 0 并报告终端设备；以管道传入 `hello` 时返回 1，输出 `not a tty`。这只验证标准输入的区别。

未实现终端模拟器，未逐项验证不同模拟器、输入协议、Unicode 或 Windows 行为，也未把颜色序列的字节输出当作所有终端都正确渲染的证明。
