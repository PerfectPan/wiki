# prompts

这个目录保存提示词原文及使用说明。一条提示词一个 Markdown 文件，frontmatter 之后是来源中的正文；正文保留原语言，不额外包代码块。

原文存档不等于可直接执行的模板。有些条目是多轮对话示例，有些包含工具、模型或占位符要求；使用前先读 `notes`。原始转义错误也可能保留在正文中。

## frontmatter

标题、使用场景与说明默认跟随提示词语言。英文 prompt 使用英文 `title`、`scene`、`source_note` 和 `notes`，不要求另写中文译文。

```yaml
---
id: seed-string
title: Seed string
scene: When exploring visual directions for a page.
level: reference
tags:
  - design
  - exploration
source: https://example.com/original
source_note: Technique 1.
notes:
  - Requires a shell tool.
added: 2026-09-22
---
```

| 字段 | 必填 | 用途 |
| --- | --- | --- |
| `id` | 是 | 与文件名相同 |
| `title` | 是 | 短标题 |
| `scene` | 是 | 什么时候使用 |
| `level` | 是 | 现有分类值为 `recommended`、`reference`、`limited`；说明见 [[wiki/topics/ai/Prompt\|Prompt]] |
| `tags` | 是 | 用于筛选的英文短词列表 |
| `source` | 是 | 来源 URL 或素材路径 |
| `source_note` | 否 | 来源中的章节或位置 |
| `notes` | 否 | 使用条件、限制和已有观察；列表格式 |
| `added` | 是 | 加入日期，`YYYY-MM-DD` |

现有分级是整理者的判断，不表示已经测试过效果。是否继续保留分级，仍需结合提示词库的用途决定。

## 查找与读取

```text
bin/wiki prompts list [--tag <tag>] [--level <level>] [--json]
bin/wiki prompts search <keyword> [--json]
bin/wiki prompts show <id> [--meta]
bin/wiki prompts check
```

列表直接从文件读取，不维护另一份人工索引。`show` 输出存档正文；需要使用说明时直接打开文件，`--meta` 目前只输出部分元数据，不包含 `notes`。

## 新增提示词

将来源保存到 `raw/sources/`，再把提示词及元数据写进 `prompts/<id>.md`。说明正文是否为单次指令、多轮示例或反例，记录已知的格式问题与使用条件。运行 `bin/wiki prompts check` 后通过分支和 PR 审阅。

当前校验检查格式与必填字段，不证明提示词有效。可修改的模板是否需要与原文副本分开保存，尚待确定。
