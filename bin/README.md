# bin

这个目录存放给 agent 和终端使用的命令入口。

当前主要命令：

- `wiki`
- `wiki.ts`

提示词库的命令也是同一个入口：

```text
bin/wiki prompts list [--tag <tag>] [--level <档>] [--json]
bin/wiki prompts search <关键词>
bin/wiki prompts show <id>
bin/wiki prompts check
```

提示词文件格式见 `prompts/README.md`。

## Ingest 来源

```bash
bin/wiki ingest <url>                                        # 直抓并转 Markdown 存入 raw/sources/
bin/wiki ingest <url> --file <path>                          # 用预抓正文落盘，跳过直抓
bin/wiki ingest <url> --name <object-or-topic>               # 指定稳定名称，不含扩展名
bin/wiki ingest <url> --file <path> --author <name> --published <date>
```

`--file` 接受 Markdown 文件，或含 `content` / `markdown` / `body` 字段的 JSON（例如会话侧 web reader 工具的返回值）；JSON 里的 `title`、`author`、`publishedTime` 会自动提取写入头注释。此选项对所有来源类型都跳过直接抓取，手动保存的正文或源码调研记录也可使用。

文件保存为 `raw/sources/<name>.md`，发布日期与抓取日期只写入来源头。未指定 `--name` 时，从 URL 的末段推导名称；GitHub 使用仓库名，YouTube watch 链接使用视频 ID，站点首页使用域名。自动名称不够明确时使用 `--name`，命名规则见 `SCHEMA.md` 的「原始素材命名」。

若目标文件或对应的旧日期前缀文件已存在，CLI 报错且不覆盖；同一对象先阅读已有素材再合并，不同对象用不同名称。最终写入使用排他创建，避免并发抓取覆盖。CLI 的 GitHub 直抓结果只是仓库阅读入口；完整实现分析由 `.agents/skills/ingest/SKILL.md` 指导完成。

直抓拿到的正文少于 80 个字符时会直接报错退出。风控页和需要 JS 渲染的空壳都会被解成几乎空的 Markdown，这种情况不再写一个看起来成功的空文件。

### B 站视频

```bash
bin/wiki ingest <B站视频 URL> [--name <slug>] [--capture <json>] [--slides] [--language zh]
```

B 站的视频页、字幕接口和播放地址接口都有风控，直连通常返回 412。这条路径的流程是：先在浏览器会话里取一次元信息和播放地址，存成 JSON 用 `--capture` 传回来；工具负责下载音频、在本地转录（mlx-whisper）、修掉转录里的解码循环，结果写进 `raw/sources/`。加 `--slides` 会再把一份幻灯片缩略图总览写进 `raw/assets/`。

`--capture` 的 JSON 可以写成 `{ "meta": { bvid, cid, title, owner, duration }, "data": <playurl 接口返回体> }`，也可以直接就是 playurl 的返回体（含 `code` / `data` / `dash`）。没传 `--capture` 时会先试直连；被拦下时报错，并打印一段可以在浏览器会话里直接跑的取数脚本。

分步命令（下载、转录、抽帧可以分开跑，也可以只用其中一步）：

```bash
python3 tools/video.py streams <B站视频 URL> [--capture <json>] --out <目录>
python3 tools/video.py transcribe <音频或视频文件> --out-dir <目录> [--language zh]
python3 tools/video.py slides <视频文件> --out-dir <目录> [--interval 60] [--frames 330,570]
```

`slides` 默认每 60 秒抽一帧、拼成 5x5 的缩略图总览，用来先看清整场讲了哪些页；`--frames` 再对指定时间点取整帧，用来读表格和数字。抽出来的帧先落在临时目录，只把正文真正引用的复制进 `raw/assets/`。

## Wiki 用词检查

```bash
bin/wiki check-jargon                  # 全库扫描
bin/wiki check-jargon wiki/topics/ai   # 指定目录或文件
bin/wiki check-jargon --staged         # 暂存区新增或改写行
bin/wiki check-jargon --base origin/main # 从共同祖先到当前工作区，含未跟踪的新页面
```

报告包含文件、行列位置和修改建议；发现问题或执行失败返回非零状态，不修改文件。pre-commit 检查实际暂存内容，PR CI 检查相对目标分支的新增或改写行。需要本地自动检查时，按 `AGENTS.md` 安装 hook。完整扫描用于逐步整理已有页面，不要求在无关 PR 中一并修复旧内容。

检查 `wiki/` 下 Markdown 的标题、正文及 frontmatter 的 `title`、`description`。`raw/`、prompt 原文、代码块、行内代码、逐行以 `>` 标记的引用、HTML 注释和链接地址不检查。Wiki 链接只检查显式显示文本，保留原有页面名作为链接目标。表格与普通列表中的文字仍检查。

少数正式名称需要保留时，在同一行列出词项与理由；例外只作用于指定词项，不免除整页检查：

```markdown
《社会契约论》 <!-- jargon-allow: 契约; 原始书名 -->
```

机器检查覆盖明确词项，不判断论据是否充分、是否过度翻译或文风是否自然。Markdown 处理按上述常用写法识别；引用请每行使用 `>`，代码请使用代码块。

词表位于 `bin/jargon-rules.json`，参考 `technical-design-docs` skill 的 `references/jargon-dictionary.yaml` 中明确禁用词、替换建议与例外，并补充本仓库的用词要求。这里只维护适合确定性检查的词项，不依赖本机 skill 路径，也不复制整套 skill。“走、跑、整”等需按语境判断的单字不进入自动检查。“透传”允许使用，不在禁用词表中。新增词项时补充误报例外，并运行 `node --test tests/check-jargon.test.ts`。

## Agent 修改后检查

Claude Code 使用 `.claude/settings.json`，Codex 使用 `.codex/hooks.json`；两者的 `PostToolUse` 都调用 `bin/jargon-hook.ts`，复用同一词表与检查程序。文件编辑、Codex patch 和 shell 命令结束后，检查当前相对 `HEAD` 的未提交改动及新页面。shell 命令可能间接写文件，因此也会触发检查；同一份未修正的改动可能在后续调用后再次报告。

检查通过时不输出消息；发现问题时以 `additionalContext` 返回位置与修改建议，让 agent 在后续步骤修正，保留原工具结果。这不是生成过程中的 TTSR，也不会撤销已经写入的内容。检查无法完成时会说明失败，不能视为通过。检查范围可能包含会话开始前的未提交改动，agent 只应修改自己任务涉及的内容。

运行环境需要 PATH 中有 Node.js 24，与仓库 CLI 要求相同。配置从子目录启动时也能定位仓库脚本，不包含机器专属路径。

启用前，在对应客户端的 `/hooks` 中检查配置。Codex 要求项目可信，并由用户审阅、信任当前 hook 定义；定义变化后需要重新审阅，提交配置文件不等于已启用。Claude Code 也受项目信任及上级设置影响。这里不修改个人设置或自动写入信任记录。

来源：[Claude Code hooks](https://code.claude.com/docs/en/hooks)、[Codex hooks](https://learn.chatgpt.com/docs/hooks)。

说明：

- 这两个文件不是知识内容，而是仓库的工作流工具。
- `wiki.ts` 是 ESM，仓库没有构建步骤，模块类型靠根目录 `package.json` 的 `"type": "module"` 声明。Node 判定 `.ts` 的模块类型时会向上找最近的 `package.json`，仓库没有的话会越出仓库边界（例如命中 `~/package.json` 的 `"type": "commonjs"`），`bin/wiki` 就会报 `Cannot use import statement outside a module`。请不要删掉那个 `type` 字段。
- `bin/wiki research <topic>` 用于生成深度调研提示词，要求包含架构图、数据流、扩展面、证据矩阵和 Wiki PR 验收。
- 如果 Obsidian 没有显示不支持的文件类型，这个目录在文件列表里可能会看起来像“空目录”。
- 日常使用这个知识库时，可以优先关注 `wiki/` 和 `raw/`。
