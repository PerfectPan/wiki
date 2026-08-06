---
title: bento-slides Skill 评审记录
date: 2026-08-06
topic: Awesome Agent Skills
sources:
  - https://github.com/nyblnet/bento
  - https://raw.githubusercontent.com/nyblnet/bento/main/plugins/bento-slides/skills/bento-slides/SKILL.md
  - https://raw.githubusercontent.com/nyblnet/bento/main/plugins/bento-slides/.claude-plugin/plugin.json
  - https://raw.githubusercontent.com/nyblnet/bento/main/docs/agents.md
  - https://bento.page/agents.md
  - https://github.com/nyblnet/bento/blob/main/README.md
---

# bento-slides Skill 评审记录

## 对象

| 项 | 值 |
| --- | --- |
| Skill | `bento-slides` |
| 仓库 | https://github.com/nyblnet/bento |
| 路径 | `plugins/bento-slides/skills/bento-slides/SKILL.md` |
| 插件版本（plugin.json） | 1.0.6 |
| 许可证 | MIT（仓库） |
| 产品 | Bento — 单文件 `.bento.html` office suite；slides 为第一款 app |
| 访问日 | 2026-08-06 |

安装入口（官方 docs）：

- Claude plugin marketplace：`/plugin marketplace add nyblnet/bento` 后装 `bento-slides@bento`
- 个人 skill：curl `https://bento.page/skills/bento-slides/SKILL.md`
- 重 schema：`https://bento.page/agents.md`（与 skill 配套，非 skill 内嵌全文）

## 产物协议（事实）

- 一副 deck = 一个自包含 `.bento.html`。
- 文档在 `#bento-doc` 的 `application/bento+json` 脚本块；`format: "bento/slides"`。
- Agent **只改该 JSON 块**；runtime HTML 压缩壳不动。
- JSON 内每个 `<` 必须写成 `\u003c`，避免 `</script>` 截断。
- 从零：curl 下载 `Bento_Slides.bento.html`；下载文件的 `#bento-doc` **为空**（浏览器首次打开才 mint showcase）。
- 新文档必须有 `size` 与 `theme`（含 `fontFamily`）；应省略 `docId` / `collab`（app 首次打开 mint）。
- 编辑已有 deck **不得** 重生成 `docId`。

## description / 路由

Skill frontmatter description 要点：

- 创建与编辑 Bento presentation
- 从无到有（自动下最新 app）、从素材、或改进已有 `.bento.html`
- 把内容映射到 chart / morph / state / ken-burns / motion path，而非静态 bullet
- 全文 schema 指向 `agents.md`

路由信号清晰：用户要 slide deck / presentation 时加载。

## 高价值 gotchas（摘自 SKILL.md / agents.md）

- Chart：bar/line `data` 必须是 **plain numbers**；`{value,...}` 对象会 coerce 成 0；仅 pie 用 `{name,value}`；`option` 纯 JSON，formatter 只能模板串，不能函数。
- Morph：跨 slide **稳定共享 id** + 后页 `transition:"morph"`；不同 id = 无 morph。
- 图/字体：data URI 进 `doc.assets`，引用 `asset:<key>`。
- Media：大视频勿 embed；autoplay 仅 present 且 video 需 `muted`。
- 勿整文件重生成 HTML；只写回 `#bento-doc`。
- 完成前 **必须打开看每一页**（溢出、拥挤、chart 静默丢 key 在 JSON 里看不见）。
- Runtime 另有 `window.bento.measure()` / `validate()`（在 agents.md；skill 提到要看片，未强制跑 validate）。

## 内容 → 能力映射（反默认失败）

Skill 明确禁止默认「段落 slideshow」，要求按素材类型选 feature（chart / table / morph / state slide / ken-burns / dash-march / countUp / media 等），并带 self-audit checklist。

## 对照判据打分（见 Skill 工程化 synthesis）

| 维度 | 判定 | 说明 |
| --- | --- | --- |
| 产物协议 | 强 | 单文件 JSON 契约 + 编辑边界 |
| description 路由 | 强 | 场景触发清晰 |
| gotchas | 强 | 多为模型会稳定踩的坑 |
| 渐进披露 | 中上 | SKILL hub + 外链 agents.md（非仓库内 references/） |
| 确定性脚本 / manifest | 弱 | 仅 curl 拉 shell；无 job manifest、无本地 schema 编译 |
| QA | 中上 | checklist + 要求目视；validate API 在 runtime，skill 未强制 |
| 负例 / evals | 弱 | 几乎无「何时不要用」与路由 eval |
| 相对 ai-cli | 更厚 | 领域协议 + 反 bullet 墙，不只是 README 命令表 |
| 相对 hatch-pet | 更薄 | 无 provenance / 子代理提交权 / repair 流水线 |

## 收录建议

- **Awesome 分级：推荐（recommended）** — 作为「文档/产物协议型 Skill」正例。
- 可进判据页案例节，论证：强产物契约 + 内容到能力映射 + gotcha，即使没有完整 manifest 流水线也值得学。
- **产品**（单文件 office、CRDT collab、E2EE relay）与 **Skill** 解耦；本笔记只评 skill。产品 topic 可另开，非必须与本条绑定。

## 风险 / 限制

- schema 与 shell 版本绑定；agents.md 写 guide version 与 app 对齐，未知 key 忽略。
- 目视验收依赖浏览器环境；纯 headless agent 难完成 skill 要求的「看每一页」。
- 未在本机实际跑通生成 deck（评审基于源码与文档，2026-08-06）。
