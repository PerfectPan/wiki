# 来源处理规范

本文档定义外部来源进入本仓库的归一化处理流程。目标是让不同类型的来源（博客、文档、论文、推文等）以统一、可检索、可溯源的方式进入 `raw/sources/`，再按需提升到 `wiki/`。

## 1. 来源类型与处理策略

| 类型 | 存什么 | 存多少 | 格式 | 说明 |
| --- | --- | --- | --- | --- |
| **博客文章** | 正文 + 原始 HTML | 全文 | `.md` + `.html` | 单篇文章，完整抓取正文 |
| **技术文档** | 相关页面正文 | 按需 | `.md` | 只抓相关页面，不抓整个站点 |
| **论文** | PDF + 摘要 | 全文 PDF + 摘要 | `.pdf` + `.md` | PDF 存档，摘要方便检索 |
| **X / 推文线程** | 线程全文 | 全文 | `.md` | 保留作者、时间、链接 |
| **视频** | 字幕/转录文本 | 转录全文 | `.md` | 不存视频文件，只存文字 |
| **代码仓库** | README + 关键文件 | 按需 | `.md` | 不 clone 全量，只存 README 和关键文件 |
| **聊天记录** | 关键段落 | 摘录 | `.md` | 只存有价值的部分 |
| **书籍** | 笔记/摘录 | 摘录 | `.md` | 不存全书，存读书笔记 |
| **GitHub Issue / PR** | 正文 + 关键评论 | 全文 | `.md` | 保留链接和状态 |

## 2. 处理原则

### 2.1 分层存储

每个来源至少存一层，建议存两层：

```
raw/sources/YYYY-MM-DD-主题.html    # 原始格式（HTML/PDF 等），忠实存档
raw/sources/YYYY-MM-DD-主题.md      # 提取后的可读格式，方便引用
```

为什么存两层：
- 原始格式是最忠实的存档，未来可以重新提取
- Markdown 方便阅读、搜索和被 wiki 页面引用

### 2.2 不存的内容

- 网站导航、页脚、广告、评论区
- 视频/音频文件本身（只存转录文本）
- 代码仓库全量（只存 README 和关键文件）
- 随处可见、无价值的内容

### 2.3 存多少的判断

| 判断维度 | 全存 | 摘录 | 不存 |
| --- | --- | --- | --- |
| 长度 | < 5000 字 | > 5000 字 | 广告/导航 |
| 价值 | 核心论点 | 关键段落 | 无关内容 |
| 可替代性 | 难找/易变 | 好找/稳定 | 随处可见 |

## 3. 元数据规范

所有 `raw/sources/` 下的文件，开头加一个 HTML 注释作为来源头（不强制，旧素材可以没有）：

```markdown
<!--
source: https://maxlv.net/blog/porting-mihomo-to-rust-with-claude/
type: blog
author: Max Lv
published: 2026-04-12
fetched: 2026-08-18
-->

# 文章标题...
```

字段说明：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `source` | 是 | 原始 URL |
| `type` | 是 | 来源类型：blog / doc / paper / tweet / video / repo / chat / book |
| `author` | 否 | 作者 |
| `published` | 否 | 原始发布日期 |
| `fetched` | 否 | 抓取日期 |

来源头是 HTML 注释，不影响 Markdown 渲染。

## 4. 文件命名规范

```
YYYY-MM-DD-主题名.md
YYYY-MM-DD-主题名.html
```

- 日期：抓取日期或发布日期，优先用发布日期
- 主题名：英文或拼音，小写，连字符分隔
- 同一来源的不同格式用相同的文件名前缀，只改扩展名

示例：
- `2026-08-18-mihomo-rust-agent-team.md`
- `2026-08-18-mihomo-rust-agent-team.html`

## 5. 提取规范

从 HTML 提取 Markdown 时，必须保留：

- 标题层级（h1-h6 → #）
- 表格（`<table>` → Markdown 表格）
- 代码块（`<pre>` → ```）
- 行内代码（`<code>` → `` ` ``）
- 链接（`<a>` → `[text](url)`）
- 图片（`<img>` → `![alt](url)`，不下载图片，保留 URL）
- 列表（`<ul>`/`<ol>` → `-` / `1.`）
- 引用（`<blockquote>` → `>`）

必须去除：

- 网站导航、页脚
- 广告
- 评论区（除非有价值）
- 复制按钮等交互元素

## 6. 从 raw 提升到 wiki

`raw/sources/` 的素材提升到 `wiki/` 时：

1. 补充正式 frontmatter（title、type、category、created、tags、source_refs）
2. 整理内容结构（摘要、关键点、相关页面、来源指针）
3. `source_refs` 指向 `raw/sources/` 里的素材
4. 更新 `index.md` 导航

提升过程本身就是"整理 + 补 frontmatter"的过程，不需要修改 raw 里的原始素材。

## 7. 各类来源的具体处理

### 7.1 博客文章

- 抓取正文（标题、正文、代码、图片链接）
- 不抓导航、页脚、评论
- 存 HTML + Markdown 两份
- 保留作者和发布日期

### 7.2 技术文档

- 只抓相关页面，不抓整个站点
- 存 Markdown
- 记录文档版本或 commit

### 7.3 论文

- 下载 PDF 存档
- 生成摘要（标题、作者、摘要、关键结论）
- 存 PDF + 摘要 Markdown

### 7.4 X / 推文线程

- 抓取线程全文
- 保留作者、时间、每条推文的链接
- 存 Markdown

### 7.5 视频

- 获取字幕或转录文本
- 不存视频文件
- 存转录 Markdown，记录视频链接

### 7.6 代码仓库

- shallow clone 到临时目录
- 生成目录结构树（排除 .git、node_modules、dist 等）
- 提取关键文件内容（README、package.json、Cargo.toml、pyproject.toml、go.mod、Makefile、CLAUDE.md、AGENTS.md）
- 存为一份分析报告 Markdown
- 如 clone 失败，回退到只抓 README

### 7.7 聊天记录

- 只摘录有价值的段落
- 标注说话人
- 存 Markdown

### 7.8 书籍

- 不存全书
- 存读书笔记和关键摘录
- 记录书名、作者、章节
