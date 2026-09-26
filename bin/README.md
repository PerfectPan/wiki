# bin

这个目录存放给 agent 和终端使用的命令入口。

当前主要命令：

- `wiki`
- `wiki.ts`

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

词表位于 `bin/jargon-rules.json`，参考 `technical-design-docs` skill 的 `references/jargon-dictionary.yaml` 中明确禁用词、替换建议与例外，并补充本仓库的用词要求。这里只维护适合确定性检查的词项，不依赖本机 skill 路径，也不复制整套 skill。“走、跑、整”等需按语境判断的单字不进入自动检查。新增词项时补充误报例外，并运行 `node --test tests/check-jargon.test.ts`。

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
