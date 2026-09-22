---
title: Coding Agent 编辑工具
description: 主流 coding agent 在“模型输出”和“文件系统写入”之间那一层编辑协议：四类实现、模糊匹配的容错阶梯，以及验证、审批与原子性的边界。
type: topic
category: ai
created: 2026-09-15
updated: 2026-09-15
timestamp: 2026-09-15
tags:
  - code-agent
  - tool-calling
  - apply-patch
  - agent-harness
source_refs:
  - raw/sources/2026-09-13-codex-apply-patch.md
  - raw/sources/2026-09-15-coding-agent-edit-tools.md
resource:
  - raw/sources/2026-09-13-codex-apply-patch.md
  - raw/sources/2026-09-15-coding-agent-edit-tools.md
---

# Coding Agent 编辑工具

## 摘要

coding agent 的编辑工具不是“写文件”这层薄封装。模型只会输出文本，文件系统只接受确定的读、写、删，两者之间必须有一层中间表示。这一层要同时回答三个问题：用**什么语言**描述修改，匹配失败时**退让到什么程度**，以及在真正落盘之前**验证到什么程度**。

主流实现可以归成四类：整文件重写、精确字符串替换、patch 语言、省略片段加专用 apply 模型。同一个 harness 往往同时提供两类以上——比如 Claude Code 用 `Write` 兜底、`Edit` 做日常修改，Cline 现在是 `editor` 加 `apply_patch`。

本页的取证来自各家源码与官方文档，逐条指针见 `raw/sources/2026-09-15-coding-agent-edit-tools.md`。

## 为什么这层协议值得单独看

模型写文件时的错误有很稳定的几类：

- **上下文漂移**。模型按“第 27 行”描述修改，但文件已经变了。只说行号是脆弱的，因为前面加一行，后面全部位移。
- **字面不精确**。差一个行尾空格、缩进少一层、复制到了弯引号，精确匹配就失配。
- **懒惰**。用 `// ... rest of code ...` 或 `...` 把没想清楚的部分糊过去。Aider 最初做 `udiff` 格式的动机就是 GPT-4 Turbo 的这个问题；Cursor 的实测也记录了 GPT-4 会省掉代码并用注释占位，还会顺手“清理”无关代码。

Aider 的官方文档把模型产出坏 diff 的具体方式列得很细：漏掉注释和空行、忘记给新增行加 `+`、把整块代码统一 outdent、不写新的 `@@` 直接跳到文件另一处。他们在基准里验证了容错的收益——**关掉 flexible patching，编辑错误增加 9 倍**。

所以这层设计的真正难点不在字符串处理，而在于：既要容忍模型的常见偏差，又不能容忍到改错地方。

## 四类实现

### 一、整文件重写

最朴素的一类。Aider 的 `whole` 格式要求模型返回完整文件内容，提示词里明确禁止用 “...” 或 “... rest of code ...” 省略。Claude Code 的 `Write`、Gemini CLI 的 `write_file` 都是这个思路，其中 Gemini 的写入还要求人工审批。

Cursor 的默认行为也落在这里，但走得更远：他们把全文件重写做成一个专门训练的 apply 模型（见第四类），因为“重写”这种输出形式对模型来说比 diff 更 in-distribution。

代价很直接：慢、贵、输出 token 量随文件长度线性增长，而且模型容易顺手改动无关部分。

### 二、精确字符串替换

社区事实上的默认解。核心三件套是 `old_string` / `new_string`、**精确匹配**、**唯一性要求**。

- **Claude Code 的 `Edit`** 明确“不做正则、不做模糊匹配”，并且要求三个检查同时通过：read-before-edit（本次会话读过该文件，被截断的 `PARTIAL view` 不算）、精确匹配、唯一命中。对“读完之后文件被改过”的情况，它给了一条很实际的规则——只要 `old_string` 仍能在当前内容里唯一精确匹配就允许编辑，同时在结果里提示文件还有其它改动。
- **Gemini CLI 的 `replace`** 在同样参数之外加了 `instruction`（这次改动的语义说明）和 `allow_multiple`；默认要求恰好一次匹配。
- **Cline 的 `editor`** 是严格匹配派，0 次或多次命中都直接报错，并且把错误信息写成模型能执行的下一步。
- **Zed 的 `edit_file`** 接受一组 `edits[]` 顺序应用，还专门在工具描述里警告：不要把 `read_file` 输出的行号前缀带进 `old_text`。
- **opencode 的 `edit`** 把 read-before-edit 做成硬约束：“没读过文件就调用会直接报错”。

Roo Code 一家就把这层的参数空间铺开了：`edit`（默认只替换第一处，`replace_all` 可全替换）、`edit_file`（默认要求唯一匹配）、`search_replace`（同样要求唯一匹配）三个重叠工具同时存在。

### 三、patch 语言

把修改写成一份可解析的变更描述，一次调用覆盖多个文件、多个修改点。

**Codex 的 `apply_patch`** 是这一类的代表。它被注册成 freeform tool，参数不是 JSON 而是一段必须匹配 Lark grammar 的文本——本质上是 constrained decoding 在工具层的用法，见 [[LLM 结构化输出的可靠性边界]]。语法核心只有十几行，支持四种文件级意图（Add / Delete / Update / Move），`@@` 可以只写一个、也可以在后面跟一行函数或类名当上下文线索，**不写行号**。

它的执行链路把职责切得很干净：解析只回答“文本是否合法”，验证回答“能否应用到当前文件”，执行才动文件系统。写入前会把整份 patch 在内存里试算一遍，拿到 `new_content` 和用于展示的 unified diff，之后才收集受影响路径（含 Move 的目标路径）交给 sandbox policy 与审批。执行阶段是逐项顺序提交，**不是跨文件事务**：第三个 hunk 失败，前两个不回滚，失败结果里会带上已经提交的 delta。细节见 `raw/sources/2026-09-13-codex-apply-patch.md`。

亲缘关系值得留意：

- Aider 的 `udiff` 同样要求**不写行号**，提示词原话是 “Don't include line numbers like `diff -U0` does. The user's patch tool doesn't need them.”
- Codex 这套格式已经被跨厂商移植：Cline 的 `apply_patch` 执行器自称实现的是 “the documented **GPT-5** apply_patch grammar”，并容忍老提示词留下的 `%%bash`、`apply_patch <<"EOF"` 包裹；Roo Code 仓库里有同名的 `parser.ts` 和 `seek-sequence.ts`；opencode 的 `apply_patch` 工具描述几乎是 Codex 原文。
- Roo 的 `apply_patch` 是个混合体：头部沿用 Codex 的 `*** Update File:`，块内却是带行号的标准 unified diff。

代价是系统要养一门语法、一个容错匹配器、换行处理、路径解析和部分失败报告。Codex 没有消除复杂度，只是把它集中到一层可测试、可审计的基础设施里。

### 四、省略片段 + 专用 apply 模型

最后这一类把“合并”这件事外包给一个专门训练的模型。

Continue 的 `edit_existing_file` 直接把省略写进工具定义：`changes` 参数允许用 `// ... existing code ...` 占位未变部分。这种片段人类读得懂，但对通用模型来说合并回去很难。

Cursor 的解法是两段式：planning 交前沿模型，applying 交一个在“整文件重写”任务上微调的模型，并用自定义的推测解码（speculative edits）加速——因为代码编辑时下一个 token 有很强先验，可以“用确定性算法而不是草稿模型来推测”，官方数字是等价于整文件重写但快最多 9x。他们也说明了为什么放弃 diff：diff 迫使模型用更少 token 思考，且在训练数据里 out of distribution。

Morph 和 Relace 把这条路线做成了独立服务，工具形态也很像：Morph 的 Fast Apply 吃 `<code>` + `<update>` 返回合并结果，官方数字 10,500 tok/s、98% 准确率，文档里直说这是 “the same concept Cursor uses for instant apply”；Relace 推荐的 `edit_file` 签名是 `path` + `instruction`（一句话说明，用来“guide the apply model”）+ `edit`（只写变化行）。两家的工具描述都在教模型怎么写占位注释，包括“删除一段时也必须给出上下文”。

这条路的取舍很清晰：直接绕开了空白、重排、多处命中的匹配问题，换来一个新依赖和一份新的失败模式（apply 模型合并错、或者干脆返回 no-op）。

## 真正拉开差距的是容错阶梯

四类实现都要面对“模型的 SEARCH 块和文件对不上”。各家的做法高度相似：**分级退让，命中即停**。

| 实现 | 退让阶梯 |
| --- | --- |
| Codex `seek_sequence` | 逐行完全相等 → 忽略行尾空白 → 忽略两端空白 → 去掉两端空白后再把 Unicode 破折号、弯引号、特殊空格归一成 ASCII |
| Aider `search_replace` | 策略：精确 SEARCH/REPLACE → 当作 patch 让 git cherry-pick → 用 diff-match-patch 模糊套用；每一档再叠加预处理：strip 首尾空行 → 相对缩进 → 反转行序 |
| Cline `apply-patch-parser` | 原文精确 → `trimEnd` → `trim` → 都不中才退到相似度打分（文本先做 NFC 归一化） |
| Roo `multi-search-replace` | 归一化字符串上算 Levenshtein 相似度，阈值 0.8–1.0，在 `:start_line:` 附近 40 行窗口内 middle-out 搜索，默认阈值其实是 1.0（即默认精确） |
| Zed `edit_file` | 按缩进差异做对齐（`old_text` 与匹配区间不要求行数一一对应） |

分歧点在于**边界画在哪里**。Codex 的容错只覆盖空白和引号，不覆盖变量名、关键字和结构；Aider 的模糊套用最激进，所以必须配合唯一性检查（失配会抛 `SearchTextNotUnique`）；Roo 保留可调阈值；Claude Code 和 Cline 的 `editor` 干脆完全不模糊，用精确匹配加清晰的错误信息换确定性。

一个容易被忽略的成本：模糊匹配可能改到语义相近但错误的位置，所以「预览 diff + 人工审批」几乎是这类实现的标配，而不是可选项。

## 写入之外的几层

编辑工具的质量差异，很大一部分不在匹配算法里。

**前置条件。** Claude Code 要求 read-before-edit（并且用 Bash 的 `cat`/`nl`/`sed -n`/`rg` 单文件查看也算数），opencode 把“没读过就报错”写进工具描述，Zed 直接警告行号前缀污染。这类约束把“模型凭记忆改文件”挡在门外。

**验证与回滚。** Codex 选择写前全量验证 + 失败时如实上报 delta；SWE-agent 的 ACI 经验里更极端——**编辑命令先过 linter，语法不通过就不让写进去**。三方都对跨文件事务保持沉默：普通文件系统很难给出跨目录、跨设备的原子语义，所以大家的共同选择是“尽量在动手前发现错误，动手后如实报告进度”。

**权限与审批。** Codex 在验证之后收集完整的受影响路径集合（包括 Move 的目标路径）再走 sandbox 和审批；Gemini 的 `write_file`、Cline 的编辑类工具都需要审批；Cline 还给了编辑工具 `retryable: false`，理由是“编辑操作有状态，不应该自动重试”。

**工程细节，但都很真实：**

- 换行符。Cline 的实现里写了原因：读文件走 readline 会把 `\r` 吃掉，模型因此只会输出 LF，编辑时必须换回文件自己的 EOL，否则会产生混合换行并破坏后续精确匹配。Codex 则可以选择统一成 LF 或保留原风格。
- 工具输出的预算。Cline 返回给模型的 diff 有 200 行上限，超出就截断并说明省略了多少行——否则一次大编辑会吃掉大量上下文。
- 转义。Cline 用 `replace(..., () => newStr)` 而不是 `replace(old, newStr)`，避免 `$&`、`$1` 这类序列被 `String.replace` 展开。
- 错误信息就是 prompt。Cline 在 `old_text` 缺失时的报错里明确写了“不要原样重发这次调用”，并给出下一步；opencode 在多处命中时报 “Provide more surrounding lines in oldString to identify the correct match”。这类文案是模型能否自己爬出来的关键。

## 当前格局

- **格式在收敛，但没有统一。** `apply_patch` 已经成了跨厂商的移植对象（Cline 称之为 GPT-5 的格式，Roo、opencode 都跟了），而 Anthropic 一侧坚持严格字符串替换、Aider 保持多格式可切换、Gemini 用替换加 `instruction`。
- **行号基本被淘汰。** Aider 从提示词里删掉行号，Cursor 明确说行号既难用又是 tokenizer 的坑，Codex 的 `@@` 只带上下文。行号只剩“定位提示”的角色，比如 Roo 的 `:start_line:`、Cline 的 `insert_line`。
- **格式和模型是共同演化的。** Aider 的文档说得直白：“Different models work better or worse with different edit formats.”，他们的榜单除了正确率还专门统计“使用正确编辑格式的比例”，同一个模型换格式表现会变（o1-mini、qwen2.5-coder、gemini-exp 走整文件反而更好）。
- 判断：这层设计更像协议设计而不是字符串处理。做得好不好，取决于容错边界画在哪、失败信息能不能让模型自己恢复，以及有没有在动手前把范围算清楚。

## 相关页面

- [[Code Agent]]
- [[Agent Harness]]
- [[Coding Agent Shell 与 Git 权限边界]]
- [[LLM 结构化输出的可靠性边界]]
- [[Agent-native 生成型 CLI 的产物协议]]
- [[OpenAI Programmatic Tool Calling]]

## 来源指针

- `raw/sources/2026-09-13-codex-apply-patch.md`（Codex apply_patch 全文拆解）
- `raw/sources/2026-09-15-coding-agent-edit-tools.md`（本次调研的逐条取证）
- https://github.com/openai/codex/blob/70eb36203dbb8c75d006b39cdfae74bd04e18a65/codex-rs/core/src/tools/handlers/apply_patch_spec.rs
- https://code.claude.com/docs/en/tools-reference
- https://aider.chat/docs/more/edit-formats.html
- https://aider.chat/docs/unified-diffs.html
- https://web.archive.org/web/20240823050616/https://www.cursor.com/blog/instant-apply
- https://docs.morphllm.com/models/apply
- https://docs.relace.ai/docs/instant-apply/agent
- https://docs.cline.bot/tools-reference/all-cline-tools
- https://docs.roocode.com/advanced-usage/available-tools/apply-diff
- https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/file-system.md
- https://github.com/SWE-agent/SWE-agent/blob/main/docs/background/aci.md
