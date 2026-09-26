# prompts

这个目录存放**可直接复用的提示词**：一条提示词一个 Markdown 文件，正文是**原样复制的原文**，不改写、不翻译、不精简。

配套的工具是 `bin/wiki prompts`，配套的判据与索引是 wiki 页面（见文末）。

## 文件规则

- 文件名就是提示词的 `id`，例如 `seed-string.md` → `id: seed-string`。
- 正文**只能有一个 fenced code block**，用四个反引号包住，语言标 `text`：

````markdown
---
id: seed-string
title: Seed string（随机种子）
scene: 让模型做设计、命名、排版这类有「标准答案倾向」的创作，而它每次都交出同一套保守默认时
level: 推荐
tags:
  - design
  - exploration
source: https://example.com/the-original-post
source_note: 原文 Technique 1
notes:
  - 想补充的坑写在这里，不要写进正文
added: 2026-09-22
---

````text
这里是原样复制的提示词正文。
````
````

- 用四个反引号是硬要求：原文里带三反引号代码块（例如让 agent 输出代码的提示词）时，三反引号会截断解析。
- 正文之外不要再写别的段落；说明、坑、场景全部进 frontmatter，这样 `bin/wiki prompts show <id>` 打印出来的就是干净的原文。

## frontmatter 字段

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `id` | 是 | 与文件名一致，召回时用它 |
| `title` | 是 | 人读的短标题 |
| `scene` | 是 | **什么场景用**：一句触发条件，别写功能广告 |
| `level` | 是 | `推荐` / `可参考` / `偏薄`，标准见判据页 |
| `tags` | 是 | 英文小写短词，用于 `prompts list --tag` 过滤 |
| `source` | 是 | 原文出处：URL 或 `raw/sources/...` 路径 |
| `source_note` | 否 | 原文里的位置（章节、编号），方便回查 |
| `notes` | 否 | 自己补的坑、边界、注意事项（列表） |
| `added` | 是 | 加入日期，`YYYY-MM-DD` |

## 命令

```text
bin/wiki prompts list [--tag <tag>] [--level <档>]   列出提示词（--json 输出机器可读格式）
bin/wiki prompts search <关键词>                     在 id / title / scene / tags / 正文里搜
bin/wiki prompts show <id> [--meta]                  打印原文（--meta 连元数据一起打印）
bin/wiki prompts check                               校验所有提示词文件是否符合上面的规则
```

`bin/wiki check` 也认这个目录：`bin/wiki check prompts/seed-string.md` 会用提示词的规则校验，而不是 wiki 页面规则。

## 新增一条提示词

1. 把原文完整存进 `raw/sources/`（素材层，不改写）；
2. 在 `prompts/` 建 `<id>.md`，正文原样粘贴，元数据补齐；
3. 在 `wiki/topics/ai/Awesome Prompts.md` 的对应档加一行（一句话价值 + 指针）；
4. 跑 `bin/wiki prompts check`，然后走 branch + PR。

判据（什么值得收、三档怎么定）在 `wiki/topics/ai/Prompt.md`；可召回的人类版索引在 `wiki/topics/ai/Awesome Prompts.md`。
