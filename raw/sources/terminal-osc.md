# Terminal OSC（Operating System Command）核对记录

- 日期：2026-11-03（Asia/Shanghai）
- 对象：拟新增 `wiki/topics/systems/terminal-osc.md`
- 范围：OSC 帧格式、与 CSI/SGR 的职责分界、常见 Ps 选择器、解析生命周期、多工器与安全边界；不覆盖完整厂商私有目录，也不实现终端解析器

## 访问元信息

| 来源 | 地址 / 版本 | 访问日期 |
| --- | --- | --- |
| XTerm Control Sequences（PDF） | https://invisible-island.net/xterm/ctlseqs/ctlseqs.pdf ；文内标注 Patch #411、2026/08/23 | 2026-11-03 |
| ECMA-48 引用点 | 经 TDN / OSC 8 规范转述：§8.3.89 OSC、§8.3.143 ST | 2026-11-03 |
| Terminal Developers Network · OSC Overview | https://toppk.github.io/revenant/tdn/osc/ | 2026-11-03 |
| TDN · OSC Anatomy and parsing | https://toppk.github.io/revenant/tdn/osc/anatomy/ | 2026-11-03 |
| TDN · Clipboard（OSC 52） | https://toppk.github.io/revenant/tdn/osc/clipboard/ | 2026-11-03 |
| Hyperlinks in Terminal Emulators（OSC 8） | https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda | 2026-11-03 |
| iTerm2 Proprietary Escape Codes | https://iterm2.com/documentation-escape-codes.html | 2026-11-03 |
| 既有主题 | [[wiki/topics/systems/terminal]]、[[raw/sources/terminal-emulator-pty-guide]] | 2026-11-03 |

HTML 版 ctlseqs（`ctlseqs.html`）对本机返回 HTTP 403；正文以同日 PDF 文本抽取为准。

## 核查证据

| 观察 | 位置 |
| --- | --- |
| OSC 帧为 `OSC Ps ; Pt BEL` 或 `OSC Ps ; Pt ST`；xterm 接受 BEL 或 ST，查询回复使用与请求相同的终结符；ST 为 ECMA-48 文档终结符，BEL 为遗留兼容 | xterm ctlseqs「Operating System Commands」；TDN anatomy「Syntax」「Terminators」 |
| ECMA-48 只规定 OSC…ST 帧，不分配 Ps 语义；编号与语义主要来自 xterm 及后续模拟器；「支持 OSC」不等于支持每个选择器 | TDN OSC Overview「History and status」 |
| 未知 Ps 仍须消费到 ST/BEL 且不打印；payload 在分号前不得按 CSI 方式通用拆分，因标题/URI 可含 `;` | TDN anatomy「Terminators」「Syntax」；OSC 8 gist「Backward compatibility」 |
| xterm Patch #411 文档列出的常见 Ps 包括 0/1/2（标题）、4/5/10–19（颜色）、50（字体）、52（选区/剪贴板）等；同日 PDF 的 OSC 章节**未**将 Ps=7、Ps=8 列为 xterm OSC 选择器 | ctlseqs.pdf Operating System Commands 段（约文内 p.35–38） |
| OSC 8 超链接：`OSC 8 ; params ; URI ST` … 可见文本 … `OSC 8 ; ; ST`；鼓励 ST；`id=` 用于 hover 连结单元；错误实现才应把未知 OSC 打成乱码 | egmontkob gist；iTerm2「Anchor (OSC 8)」 |
| OSC 52：`OSC 52 ; Pc ; Pd`，`Pd` 为 base64 或 `?` 查询；xterm 可用 `allowWindowOps` 禁用；读取会把剪贴板经回复注入输入流 | ctlseqs OSC 52；TDN clipboard |
| OSC 7 / OSC 1337 CurrentDir：工作目录提示；iTerm2 将 `OSC 7` 记为 RemoteHost+CurrentDir 同义写法之一；OSC 133：FinalTerm 语义提示符 A/B/C/D | iTerm2 Shell Integration / FinalTerm；TDN Overview feature pages |
| 多工器：tmux 可拦截 OSC 52（`set-clipboard`）；DCS 透传内的 OSC 须用 ST，因 BEL 不能结束 DCS | TDN anatomy / clipboard；iTerm2 页首警示 |
| C1 单字节 `0x9c`/`0x9d` 在 UTF-8 下不可互操作；优先 7-bit `ESC ]` / `ESC \` | TDN anatomy；OSC 8 gist |

## 证据对照表（写入 topic 的同源表）

| 结论 | 证据来源 | 证据位置 | 置信度或限制 |
| --- | --- | --- | --- |
| OSC 是带字符串载荷的控制串，作用于网格外的「环境」能力 | TDN Overview；xterm ctlseqs | Overview；Operating System Commands | 高 |
| 帧格式：`ESC ]` + `Ps` + `;` + `Pt` + (`BEL`\|`ST`) | xterm；TDN anatomy；OSC 8 gist | 同上 | 高 |
| ECMA-48 不定义各 Ps 含义 | TDN Overview | History and status | 高（未直接打开 ECMA-48 PDF，依二手权威转述） |
| 「支持 OSC」须按选择器逐项谈兼容 | TDN Overview | History and status | 高 |
| 未知 OSC 应静默吞掉至终结符 | OSC 8 gist；TDN anatomy | Backward compatibility；Terminators | 高 |
| OSC 0/1/2、4、10–19、52 为 xterm 文档化选择器 | ctlseqs Patch #411 | Operating System Commands | 高（以该 PDF 版本为界） |
| OSC 8 超链接来自 VTE/iTerm2 社区规范，非同日 xterm OSC 表项 | egmontkob gist；ctlseqs 缺省 | gist 全文；PDF OSC 列表 | 高 |
| OSC 52 读写剪贴板/选区；读路径默认常被拒绝 | ctlseqs；TDN clipboard | OSC 52；Reads | 高；具体默认值因模拟器而异 |
| 多工器与 DCS 透传更宜用 `ST` | TDN anatomy | Terminators | 高 |
| 向 `Pt` 插值未过滤的 `BEL`/`ESC \` 可提前终结序列 | TDN anatomy | Security model | 高 |
| OSC 133 语义提示符便于模拟器跳转命令块 | iTerm2 FinalTerm 段 | FTCS_PROMPT 等 | 高；各壳集成脚本版本不一 |

## 验证记录

- 已读：上表来源；对照仓库既有 `terminal.md` 中 CSI/SGR 示例与备用屏幕说明，确认 OSC 应独立成页而非塞进入门页。
- 本机实验：在交互式 shell 中执行 `printf '\033]0;osc-wiki-probe\033\\'`（改标题）与 `printf '\033]8;;https://example.com\033\\link\033]8;;\033\\\n'`（超链接）。**未**将结果当作「所有模拟器均支持」的证明；标题变化依赖本会话所用模拟器，超链接依赖 OSC 8 支持与用户手势。
- 未测试：tmux/screen 透传矩阵、OSC 52 读写权限对话框、Kitty OSC 5522、各模拟器长度上限实测、Windows ConPTY。
- 未实现：完整状态机解析器或 fuzz。

## 未覆盖

Windows 控制台专有序列；完整 OSC 目录（TDN catalog）；图片协议细节（Sixel / Kitty graphics / iTerm2 File=）仅作边界提及。
