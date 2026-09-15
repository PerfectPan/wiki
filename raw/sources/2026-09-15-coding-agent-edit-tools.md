# Coding Agent 编辑工具实现调研摘录

来源时间：2026-09-15

## 调研范围与方法

目标是回答一个问题：主流 coding agent 让模型改文件时，到底在模型和文件系统之间放了哪一层协议。

做法是从各家的**一手材料**取证，优先顺序为：仓库源码 > 官方工具文档 > 官方博客。第三方博客、二手总结只用来找线索，不作为引用依据。所有引用都在 2026-09-15 实际抓取并核对过内容。

下文的「关键事实」都可以在对应来源里直接验证。

## 一、OpenAI Codex：apply_patch

- 工具定义：`create_apply_patch_freeform_tool` 把 `apply_patch` 注册为 **Freeform tool**，格式 `grammar` + `lark`，函数注释写着 “Well-suited for GPT-5 models”，描述里明确 “This is a FREEFORM tool, so do not wrap the patch in JSON.”
  - https://github.com/openai/codex/blob/70eb36203dbb8c75d006b39cdfae74bd04e18a65/codex-rs/core/src/tools/handlers/apply_patch_spec.rs
- 语法（Lark）只有十几行：`*** Begin Patch` / `*** Add File:` / `*** Delete File:` / `*** Update File:` / `*** Move to:` / `*** End of File` / `*** End Patch`，`@@` 后面可以不带行号、只带一行上下文。
  - https://github.com/openai/codex/blob/70eb36203dbb8c75d006b39cdfae74bd04e18a65/codex-rs/core/assets/tools/apply_patch.lark
- 解析器注释明确说 parser 比 spec **宽松**，允许 marker 周围有多余空白；它不检查 patch 能否应用到文件系统。
  - https://github.com/openai/codex/blob/70eb36203dbb8c75d006b39cdfae74bd04e18a65/codex-rs/apply-patch/src/parser.rs
- 匹配函数 `seek_sequence` 单独成文件，是“多轮容错、命中即停”的实现。
  - https://github.com/openai/codex/blob/70eb36203dbb8c75d006b39cdfae74bd04e18a65/codex-rs/apply-patch/src/seek_sequence.rs
- 公开实现里存在 `streaming_parser.rs`、`text_file.rs`（换行处理）、`invocation.rs`（验证）、`lib.rs`（逐项执行 + delta）。
- 文章侧的技术描述（六阶段链路、非事务、delta）见 `raw/sources/2026-09-13-codex-apply-patch.md`。

## 二、Anthropic：API 层 text editor tool 与 Claude Code 的 Edit

API 层（Messages API 的 client tool）：

- 工具名 `str_replace_based_edit_tool`，命令集为 `view` / `str_replace` / `create` / `insert`。
- `str_replace` 要求 `old_str` “must match exactly, including whitespace and indentation”。
- `insert` 是**行号式**插入：`insert_line` 表示“插入到第几行之后”。
- 版本：`text_editor_20250728`（Claude 4 及以后）与 `text_editor_20250124`；`max_characters` 只在新版可用。
- 来源：https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool （抓取时曾用 https://docs.claude.com/en/docs/agents-and-tools/tool-use/text-editor-tool 同一页面）

Claude Code 自己的 `Edit` 工具（与 API 层工具不是同一个东西）：

- “performs exact string replacement. It takes an `old_string` and a `new_string`… It doesn't use regex or fuzzy matching.”
- 三个必须同时满足的检查：read-before-edit（本次会话里读过该文件，被截断的 `PARTIAL view` 不算）、Match（差一个空白字符就失配）、Uniqueness（必须唯一，否则要补上下文或 `replace_all: true`）。
- 对“读完之后文件被改过”的情况有明确规则：只要 `old_string` 仍能在当前内容里唯一精确匹配，就允许编辑，并在结果里提示文件还有其它改动；否则要求重新读。
- 用 Bash 的 `cat` / `nl` / `bat` / `head` / `tail` / `sed -n` / `grep` / `rg`（单文件、无管道重定向）查看文件，也算满足 read-before-edit。
- `Write` 是整文件覆盖，不追加、不合并，且对已存在文件有同样的 read-before-edit 约束（Jupyter notebook 和部分读取过的文件在所有模型上都强制重读）。
- 来源：https://code.claude.com/docs/en/tools-reference （同页的 Edit tool behavior / Write tool behavior / Read tool behavior 小节）

## 三、Gemini CLI：replace

- `replace` 参数：`file_path`、`instruction`（语义描述）、`old_string`、`new_string`、`allow_multiple`。
- 默认要求**恰好一次**匹配，`allow_multiple: true` 才全部替换。
- 文档原话：“requires significant context around the `old_string` to ensure it modifies the correct location.”
- 同文件里 `write_file` 是整文件覆盖，且“Requires manual user approval”。
- 来源：https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/file-system.md

## 四、Aider：可切换的 edit format

- 官方编辑格式清单：`whole`、`diff`（SEARCH/REPLACE 块）、`diff-fenced`（路径放在 fence 内，主要给 Gemini 系）、`udiff`（简化版 unified diff）、`editor-diff`、`editor-whole`（architect 模式下的 sub-agent 专用，提示词更聚焦于“执行编辑”而非“解决任务”）。
- 官方说明 “Different models work better or worse with different edit formats”，aider 会为常见模型选默认格式。
- `udiff` 的提示词明确要求：**不要写行号**（“Don't include line numbers like `diff -U0` does. The user's patch tool doesn't need them.”），并要求修改函数时用 hunk 整体替换整个代码块。
- `whole` 的提示词要求返回整个文件，并禁止用 “...” 或 “... rest of code ...” 省略。
- 来源：https://aider.chat/docs/more/edit-formats.html
- 容错实现：`aider/coders/search_replace.py` 里是「策略 × 预处理」的搜索阶梯：
  - 策略：`search_and_replace` → `git_cherry_pick_osr_onto_o`（把 SEARCH/REPLACE 当 patch，用 git 去套）→ `dmp_lines_apply`（用 Google diff-match-patch 做模糊套用）。
  - 预处理：strip 首尾空行、相对缩进（`RelativeIndenter`）、反转行序（默认关闭）。
  - 唯一性失配会抛 `SearchTextNotUnique`。
  - 来源：https://github.com/Aider-AI/aider/blob/main/aider/coders/search_replace.py
- 容错的代价与收益有官方量化：文档罗列了模型产生坏 diff 的典型方式（漏掉注释/docstring/空行、忘记给新行加 `+`、把整块代码统一 outdent、不写新的 `@@` 就直接跳到文件另一处），并给出结论 “Experiments where flexible patching is disabled show a 9X increase in editing errors on aider’s original Exercism benchmark.”
  - 来源：https://aider.chat/docs/unified-diffs.html
- Aider 的编辑基准榜（Exercism）除“正确完成率”外还单独统计 “Percent using correct edit format”，同一个模型换格式表现会变（例如 o1-mini、qwen2.5-coder、gemini-exp 走 whole）。
  - 来源：https://aider.chat/docs/leaderboards/edit.html

## 五、Cursor：fast apply + speculative edits

官方博客 “Editing Files at 1000 Tokens per Second”（2024-05-14，作者 Aman）：

- 把代码编辑拆成两段：planning 用前沿模型（chat），applying 用一个专门训练的模型。默认行为是**整文件重写**，条件是当前文件 + 对话历史 + 当前代码块。
- 为什么不用 diff（原文四点）：diff 迫使模型用更少的 token 思考；diff 在预训练/后训练数据里 out of distribution；行号会被 tokenizer 当成整体、模型也不擅长数行号；模型输出的 diff 普遍不精确（“Most models fail to output accurate diffs, with the exception of Claude Opus”）。
- 他们也观察到 GPT-4 的“懒惰”：省掉代码、用 “...” 或注释表示缺失区域，并顺手“清理”无关代码。
- 行号问题的解法写在明面上：“Motivated by the diff format from Aider, we eliminate the line number problem. Instead of a standard diff format, the model proposes diff hunks as search/replace blocks”——他们自己的格式是带 `@@ ... @@` 头、但**不含行号**的 search/replace 块。
- `speculative edits` 是自定义推测解码：因为代码编辑时下一个 token 有很强先验，可以“用确定性算法而不是草稿模型来推测”，等价于整文件重写但快最多 9x；实现上和 Fireworks 合作。评测集约 450 个 400 行以内的整文件编辑，用 Claude-3 Opus 当 grader。
- 来源（原 blog 已下线，Morph 文档直接链到 web.archive.org 的存档，本摘录即取自该存档）：https://web.archive.org/web/20240823050616/https://www.cursor.com/blog/instant-apply

## 六、fast apply 专用模型：Morph 与 Relace

Morph：

- 定位是“同一个模型，不同的推理引擎”，核心产品 Fast Apply：输入 `original code` + `edit snippet`，输出合并后的代码；官方数字 10,500 tok/s、98% 准确率（`morph-v3-fast` 96%、`morph-v3-large` 98%）。
- 文档原话把对照关系写清楚了：“It's the same concept Cursor uses for instant apply.”，并列举它相对 search-and-replace 与整文件重写的取舍：“search-and-replace… requires a separate tool call for each edit chunk and fails on whitespace, reordering, and ambiguous matches. Or full-file rewrites, which are slow and expensive.”
- 调用形态是 `<instruction>…</instruction><code>…</code><update>…</update>`，update 片段里用 `// ... existing code ...` 表示未变部分。
- 来源：https://docs.morphllm.com/models/apply 、https://docs.morphllm.com/guides/agent-tools

Relace：

- 推荐的 `edit_file` 工具签名是 `path` + `instruction`（一句话编辑说明，用来“guide the apply model”）+ `edit`（只写变化行，未变部分用 “// ... rest of code ...” 之类的注释占位）。
- 占位注释的写法在工具描述里被写得很细，包括“删除一段时也必须给出上下文”。
- 来源：https://docs.relace.ai/docs/instant-apply/agent

## 七、Cline：从 XML 式 replace_in_file 迁到 editor + apply_patch

- 当前 ClineCore 内置工具里，编辑相关的是 `editor`（“View and edit files”）和 `apply_patch`（“Apply unified diffs to files”）。
- 官方文档明确写了迁移关系：老文档里的 `read_file`、`replace_in_file`、`execute_command` 这类 XML 风格名字，在现在的 SDK/ClineCore runtime 里对应 `read_files`、`apply_patch`、`bash`。
- 来源：https://docs.cline.bot/tools-reference/all-cline-tools
- `editor` 执行器（`sdk/packages/core/src/extensions/tools/executors/editor.ts`）的关键行为：
  - 参数含 `insert_line`；给了它就是行号插入，否则是 `old_text` → `new_text` 替换；文件不存在则用 `new_text` 创建。
  - 严格匹配（无模糊），0 次或多次命中都报错：`No replacement performed: text not found` / `multiple occurrences of text found`。
  - 读写时按文件自身行尾风格归一化（注释里写明：读文件走 readline 会把 `\r` 吃掉，模型因此只会输出 LF，所以编辑必须换回文件自己的 EOL，否则会造成混合换行、破坏后续精确匹配）。
  - 替换用 `replace(..., () => newStr)`，避免 `$&`、`$1` 这类被 `String.replace` 展开。
  - 返回给模型的 diff 有行数预算（`maxDiffLines` 默认 200），超出会输出 “diff truncated (N more removed, M more added lines)”。
  - 错误信息是写给模型看的：`old_text` 为 null/缺失时会明确要求“不要原样重发这次调用”、并给出下一步怎么做。
  - 工具注册处标注 `retryable: false, maxRetries: 0`，注释是 “Editing operations are stateful and should not auto-retry”。
  - 来源：同上仓库路径 `sdk/packages/core/src/extensions/tools/executors/editor.ts`、`.../tools/definitions.ts`
- `apply_patch` 执行器的文件头写着 “Built-in implementation for the documented **GPT-5** apply_patch grammar. It accepts the freeform patch body directly and **tolerates the legacy shell wrapper form** used by older prompts.”；工具描述里重申 “Do not use line numbers; this format is context-based”，并把 `%%bash`、`apply_patch <<"EOF"` 这类包裹声明为“兼容但不推荐”。
  - 匹配阶梯（`apply-patch-parser.ts`）：先原始内容精确匹配 → `trimEnd` 匹配 → `trim` 匹配 → 都不中再退到相似度（相似度取最高分者），并对文本做 NFC 归一化。
  - 来源：`sdk/packages/core/src/extensions/tools/executors/apply-patch.ts`、`apply-patch-parser.ts`、`definitions.ts`

## 八、Roo Code（Cline 分支）：工具链最“动物园”的一家

官方文档同时列了四个重叠的搜索替换工具：

- `edit`：默认只替换**第一处**，`replace_all` 可全替换（文档注明 `SearchAndReplaceTool` 是它的废弃别名）。
- `edit_file`：默认要求**唯一匹配**（`expected_replacements` 可放宽），`old_string=""` 时创建/追加文件。
- `search_replace`：同样要求唯一匹配。
- `apply_diff`：带 `:start_line:` 提示 + 模糊匹配。
- `apply_patch`：工具名沿用 Codex 的 `*** Add File:` / `*** Update File:` / `*** Delete File:` 头，但块内是标准 unified diff（带 `@@ -10,7 +10,7 @@` 行号）。
- 来源：https://docs.roocode.com/advanced-usage/available-tools/edit 、 `/edit-file` 、 `/search-replace` 、 `/apply-diff` 、 `/apply-patch`
- `apply_diff` 文档里的实现细节：相似度用 Levenshtein distance + 归一化字符串，阈值通常取 0.8–1.0；在 `:start_line:` 附近、`BUFFER_LINES = 40` 的窗口内做 middle-out 搜索；每个文件有连续失败计数 `consecutiveMistakeCountForApplyDiff`。
- 源码 `src/core/diff/strategies/multi-search-replace.ts` 确认：`getSimilarity` 先 `normalizeString`（处理弯引号等）再算 Levenshtein；`fuzzySearch` 从窗口中点向两侧扩散取最高分；`fuzzyThreshold` 默认是 1.0（即默认精确匹配）；应用前会检测原文件是 `\r\n` 还是 `\n`。
- 仓库里同时存在 `src/core/tools/apply-patch/{parser,seek-sequence}.ts`，与 Codex 的实现同名同结构。
  - 来源：https://github.com/RooCodeInc/Roo-Code

## 九、Zed：edit_file 的批量编辑与流式应用

- `edit_file` 的输入是 `path` + `edits[]`，每次 edit 给出 `old_text` / `new_text`，**按顺序**应用到当前 buffer（测试里明确写了「后面的编辑在前面的编辑结果上重新找唯一匹配」）。
- 工具描述里专门警告：`read_file` 的行号前缀（6 字符右对齐 + 一个 tab）不要带进 `old_text` / `new_text`。
- 代码里存在按缩进差异做模糊对齐的处理，测试注释引用 zed issue #60302（`old_text` 第一行缺缩进、且与匹配区间行数不对齐的场景），说明 `old_text` 与 buffer 区间是按模糊匹配对齐而不是按行数一一对应。
- 另有独立的 `crates/edit_prediction/src/udiff.rs`，复用 `zeta_prompt::udiff` 的 `DiffParser` / `find_context_candidates` / `disambiguate_by_line_number` 来解析和应用模型输出的 udiff（这属于编辑器内联预测，不算 agent 工具，但同一套 apply 逻辑）。
- 来源：https://github.com/zed-industries/zed/blob/main/crates/agent/src/tools/edit_file_tool.rs

## 十、SWE-agent：ACI 视角，编辑要过 linter

- SWE-agent 的出发点是把工具本身当设计对象（Agent-Computer Interface），论文 arXiv:2405.15793。
- 官方列出的四条 ACI 经验，其中第一条直接约束编辑：**编辑命令会先跑 linter，语法不通过就不让改进去**。
- 另外三条：自建文件查看器（每轮只显示 100 行，带滚动）而不是 `cat`；自建目录搜索命令，只列有匹配的文件（给出更多上下文反而让模型更困惑）；空输出回一句 “Your command ran successfully and did not produce any output.”。
- 来源：https://github.com/SWE-agent/SWE-agent/blob/main/docs/background/aci.md

## 十一、Continue：把“省略”写进工具定义

- `edit_existing_file` 的参数是 `filepath` + `changes`，`changes` 的描述要求“只写需要的改动”，并且**允许**在大文件里用 “// ... existing code ...” 之类的占位省略未变部分。
- 同时约束 “This tool CANNOT be called in parallel with any other tools, including itself”。
- 来源：https://github.com/continuedev/continue/blob/main/core/tools/definitions/editFile.ts
- 这种“省略式片段”正是 Aider udiff 与 Cursor fast-apply 想解决的问题的两端：前者要模型别省略，后者用专用模型把省略的片段合并回去。

## 十二、opencode：同时提供 edit 与 apply_patch

- `edit` 工具描述：精确字符串替换；**必须先读过文件**才能编辑（“This tool will error if you attempt an edit without reading the file”）；`oldString` 找不到或多处命中都报明确错误；多处命中时要么补上下文要么用 `replaceAll`；同样警告不要把 Read 输出的行号前缀带进字符串。
- `apply_patch` 工具描述直接沿用 Codex 的语言（`*** Begin Patch` / `*** Add File` / `*** Delete File` / `*** Update File` / `*** Move to` / `@@ def greet():`），并在描述里说明“必须给每个新行加 `+`”。
- 来源：https://github.com/sst/opencode （`packages/opencode/src/tool/edit.txt`、`apply_patch.txt`、`edit.ts`、`apply_patch.ts`）

## 横向观察（本次调研的判断，非引用）

1. 社区在“用什么语言描述修改”上分成四类：整文件、精确替换、patch 语言、省略片段 + apply 模型。绝大多数 harness 至少同时提供两类（整文件 + 替换，或替换 + patch）。
2. “行号”几乎被淘汰：Aider 从 udiff 提示词里删掉行号，Cursor 明确说行号难用并要求去掉，Codex/Cline/opencode 的 patch 语言里 `@@` 只带上下文不带行号。行号只作为**定位提示**存在于 Roo 的 `:start_line:` 和 `insert_line` 这类参数里。
3. 迁移方向是“模糊匹配 → 预验证 + 更好的错误信息”。Codex 选择在写之前验证整份 patch，Cline 的 editor 走严格匹配但把错误信息写成模型可执行的下一步，Roo 保留了可调阈值的模糊匹配。
4. 编辑工具的失败模式和上下文管理成本（工具输出预算、CRLF、行号前缀污染）比模型能力更容易被忽略，但都在实现里留下了明确痕迹。
