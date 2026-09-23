---
title: handdraw-style-prompter Skill 评审记录
date: 2026-09-22
topic: Awesome Agent Skills
sources:
  - https://github.com/yang0/handraw-style
  - https://github.com/yang0/handraw-style/tree/master/skills/handdraw-style-prompter
  - https://raw.githubusercontent.com/yang0/handraw-style/master/skills/handdraw-style-prompter/SKILL.md
  - https://raw.githubusercontent.com/yang0/handraw-style/master/skills/handdraw-style-prompter/references/model_capabilities.json
  - https://raw.githubusercontent.com/yang0/handraw-style/master/styles_200_reorganized.md
---

# handdraw-style-prompter Skill 评审记录

## 术语速查（wiki 注，非评审原文）

- **风格编号 / 参考名 / 生图名**：每条画风一个三位编号（001–274）；「参考名」是原作者起的风格名，「生图名」是实际写进提示词给图片模型看的名字。
- **垫图 / 兜底**：模型能力不确定时，把一张风格参考图随提示词一起传给图片模型；「兜底」指能力未知时一律传图，不靠猜。
- **激活（activation）**：模型只凭风格名字或文字特征就能稳定画出该风格，叫「名字激活 / 特征激活」；做不到就得垫图。
- **`traits`（特征）**：一句话描述该风格长什么样的文字（如「极简圆头人物、面无表情」），写进提示词；只保留正向描述，「避免 / 不要」这类负向句要过滤掉。
- **单图 / 四宫格 / 拼图**：参考图资产的三种形态——单张风格图、2×2 四格参考图、把多个小图拼成的大图。
- **纯图模式（pure-image）/ 图文模式（graphic-text）**：前者只让模型画主题画面、不在图里排文字；后者要把文字也排进画面。
- **布局图型（SC / IG / SB）**：另一类提示词，管画面怎么构图、文字怎么排（社媒卡 / 信息图 / 分镜三种）；与「风格」（只管画法）是两条线。
- **隔离说明 / 隔离块**：提示词里一段固定声明，规定参考图只许借鉴画风、不许照搬它的内容；图文模式下这段声明和本地路径不能出现在可复制给别人的提示词里。
- **风格锚点**：提示词末尾固定附加的风格标记短语（如「俏皮的手绘线条」），校验脚本禁止模型自行增减。
- **hub**：技能入口文件（SKILL.md），只做引导，细节放在 references / scripts。
- **gallery**：仓库自带的离线网页图册，用来在浏览器里浏览风格图；要求用浏览器标签页打开，不能直接开本地文件。
- **JSON 目录**：`styles.json`、`model_capabilities.json` 这类机器可读的取值清单，是编号、能力判定的权威来源。

## 基本信息

| 项 | 值 |
| --- | --- |
| Skill | `handdraw-style-prompter` v1.0.4（`references/version.json`） |
| 仓库 | https://github.com/yang0/handraw-style |
| 路径 | `skills/handdraw-style-prompter/`（仓库里另有一个 `skills/article-illustration-planner/`） |
| 许可 | MIT（© 2026 yang0），覆盖范围写在 LICENSE 里，只提到软件 |
| 最后提交 | 2026-09-21 `f65db5e` "fix: resolve community review issues, sanitize paths, and bump version to 1.0.4" |
| 访问日 | 2026-09-22 |
| 形态 | SKILL.md（14.7KB）+ `references/`（styles.json 1920 行、layouts.json、model_capabilities.json、attribution.json、118 个 layout prompt md）+ `scripts/`（11 个 python）+ `gallery/`（两个离线 HTML，各 12 万字符）+ 图片资产 |
| 数据规模 | 274 种风格（001–274）、118 条排版图型、274 张编号单图 + 41 张四宫格垫图 + 19 张拼图 + 118 张版式预览 |
| 定位 | 「选编号 → 出中英双语生图提示词」：把画风选择从形容词变成编号，默认不出图 |

## 它交付什么

默认只产出提示词，四部分：

1. 选中的风格：编号 + 生成名（如 `#018 · Minimal Deadpan Dialogue Cartoon`）；
2. 中文提示词，正文以 `风格名称：#018 · {generation_name}。` 开头，必须带 `参考作者/风格名称：{indexed name}` 标签；
3. 英文提示词，同样结构（`Style name: #018 · ...` / `Reference author/style name`）；
4. 一句说明：提示词可粘贴到任意生图 AI，出图由那个 AI 决定。

两种模式，同一编号可切换：

- `pure-image`（默认）：只写主题直接隐含的可见内容，末尾附一行小字 `当前处于纯图模式，可切换为图文模式。`；需要垫图时，把本地资源路径和参考图隔离说明写进两个提示词里，让用户自己上传。
- `graphic-text`：主题原文照抄（`主题：` / `Theme:` 后面不许扩写、改写、补场景），两个提示词末尾原样追加一段固定中文后缀（`【如果主题直白包含画面元素那就按主题出图……文字参与构图，图文一体】`，一个字都不能改），并且**不**把路径、上传说明、隔离说明放进可复制提示词，改成在提示词外向用户展示那张参考图。

另外支持「布局图型」路线（`SC-xxx` / `IG-xxx` / `SB-xxx`）：布局决定构图和文字结构，风格只影响画法；选布局时自动进 `graphic-text`，布局提示词与固定后缀叠加，输出一条完整提示词（不是双语两条）。

## 核心做法

**1）风格编号化，取值写进 JSON 目录。**
权威内容在 `styles_200_reorganized.md`（274 行 Markdown 表：编号 · 原参考名称 / 生图名称 / 核心视觉特征），`references/styles.json` 是脚本生成的索引（`scripts/build_library.py`），SKILL.md 明确「Markdown 改了要重跑脚本刷新索引」。274 条分 A–H 八组（国际社论漫画 35、国际绘本 19、现代平面 28、日本作者 41、中国作者 31、通用网感 46、附件新增 16、其他 58）。

**2）模型能力分层，决定要不要垫图。**
`references/model_capabilities.json`：`default` 是 `name_activation: unknown` + `use_reference_image: true`；只有 `gpt-image-2` 有 style 级标定（137 条 `name_activation`，模型级 `traits_activation: strong`）。`scripts/resolve_reference.py` 把「模型 + 风格编号」解析成四种来源之一：

- `name+style`：只用编号作者名 + 生成名 + 主题，不传图；
- `name+style+traits`：名字不够时补正向核心特征，不传图；
- `name+style+traits+reference-image` / `name+style+reference-image`：能力未知或特征为空时要求垫图，并给出 `images/individual/{bucket}/{number}.webp`（同编号有 `{number}_grid.webp` 时优先用四宫格）。

脚本对未知模型不猜能力，`unknown` 一律走兜底。

**3）正向特征过滤器。**
`positive_traits()` 按 `；;。` 和换行切分 `traits`，丢掉含「避免 / 不要 / 不准 / 禁止」的子句，以及「无写实纹理」这类否定式，只保留正向子句拼回去。

**4）参考图与主题的硬隔离。**
需要垫图时，SKILL.md 指定一段中英文隔离说明（`所附图片仅用于参考画风……最终画面内容完全以用户提供的主题为准。`），只抽线条、笔触、媒介、材质、色彩倾向、整体视觉语言；不得沿用参考图的主体、人物、动物、服装、道具、动作、姿态、场景、背景、构图、布局、文字或故事。声明「用户的主题是画面内容的唯一来源」。

**5）会话初始化契约。**
首次在本任务/线程调用时，必须用 `mcp__codex_app__open_in_codex` 以 browser tab 打开 `gallery/index.html`（明确禁止 `target.type="file"`、编辑器或文件预览），并在同一条回复里输出固定状态行 `当前处于纯图模式，可切换为图文模式。`；同一会话后续轮次不得重复打开或重复状态行，判定依据是对话上下文而不是状态文件。打开失败时给出动态解析出的本地 `file://` 兜底链接。

**6）溯源与版本。**
`attribution.json` 为每个参考作者记录在世 / 去世状态和维基来源；`contact_sheet_state.json` 记录当前拼图已填格数；`references/version.json` + gallery 内置的远程版本比对给出「发现风格库更新」提示和复制用的更新指令。

## 容易踩的坑（SKILL.md 与校验脚本共同钉死的部分）

1. 把垫图当内容源用 → 主体、构图、文字全被参考图带跑。隔离声明就是为了这个。
2. 机械照抄 `traits` 字段 → 把「避免……」这类负向句也写进提示词。必须先过滤。
3. 对未标定模型直接靠作者名激活 → 风格漂移。未知一律兜底垫图，且不许编造特征。
4. 图文模式下替用户「升华」主题 → 明文禁止扩写、改写、补场景元素和隐喻。
5. 自作主张加通用构图建议、质量声明、负面提示词，或那套固定风格锚点 → 明文禁止；校验脚本会断言默认输出里不得出现 `俏皮的手绘线条` / `playful hand-drawn linework`。
6. 图文模式的可复制提示词里露出本地路径、上传说明或隔离块 → 明文禁止（这是 Codex 专有的交互约束，换成别的宿主需要改）。
7. 编号或布局 ID 无效时臆造 → 要求用户从有效索引里选。
8. 布局和风格混为一谈 → 布局管构图与文字结构，风格管画法；风格垫图不得覆盖布局与主题。
9. 首次忘记开 gallery、用 file 型 tab 打开、或每轮重复初始化。
10. 在 `graphic-text` 模式里改动那串固定后缀的任何一个字（校验脚本逐字比对整段后缀）。

## 怎么验收

主要靠 `scripts/validate_library.py`（378 行）。它先跑 `build_library.py` 和 `build_layout_gallery.py`，然后断言：

- 风格编号 001–274 连续、`018` 必须映射到 `Minimal Deadpan Dialogue Cartoon`；
- `attribution.json` 里去世作者必须有验证来源；
- 能力清单的 `default` 必须是 `unknown` + 兜底为真，所有模型 / 风格的枚举值合法且引用的风格编号存在；
- 多组 `resolve()` 断言：未知模型必须用垫图、`gpt-image-2/001` 不许用垫图、纯名字型风格不得带 traits、有正向特征的风格走 name+traits、`217` 必须保住 traits 且用四宫格垫图、`262–268` 不许留多余的四宫格、`201` 这种空特征必须兜底；还构造了一个 `test-model` 假配置测「空特征 / 弱能力必须兜底」和「兜底时 traits 要保留」；
- 201–216 只能待在 G 组且只有 `205` 允许有 traits、217+ 必须在 H 组；
- 单图资产必须覆盖 001–274 且不能留在旧的扁平目录；拼图必须唯一覆盖 201–274、除最后一张外每张 16 格；拼图状态文件必须和当前拼图一致；
- gallery / README / STYLES.md 的交叉引用 token（拼图文件名、`#018`、版式预览图、布局锚点、提示词示例、版本检测、更新提示文案）；
- 直接跑 `prompt_style.py --style 18 --theme 秋天的第一杯奶茶`，断言输出包含风格名、双语标签和主题，且不含固定风格锚点；断言 `当前处于纯图模式，可切换为图文模式。` 出现在输出里；
- 同一条初始化契约必须同时存在于根 `SKILL.md` 和 `skills/handdraw-style-prompter/SKILL.md`。

本机实跑（2026-09-22，只读克隆到 /tmp）：

```text
$ python3 scripts/prompt_style.py --style 18 --theme "秋天的第一杯奶茶"
Selected style: #018 · Minimal Deadpan Dialogue Cartoon
风格名称：#018 · Minimal Deadpan Dialogue Cartoon。主题：秋天的第一杯奶茶。参考作者/风格名称：Poorly Drawn Lines / Reza Farazmand。
Style name: #018 · Minimal Deadpan Dialogue Cartoon. Theme: 秋天的第一杯奶茶. Reference author/style name: Poorly Drawn Lines / Reza Farazmand.
当前处于纯图模式，可切换为图文模式。

$ python3 scripts/resolve_reference.py --model midjourney --style 18
{"activation_source": "name+style+traits+reference-image", "use_reference_image": true, "prompt_traits": "极简圆头人物、面无表情、简单动物、灰蓝与米色小色块；……", "reference_path": ".../images/individual/001-200/018.webp"}

$ python3 scripts/resolve_reference.py --model gpt-image-2 --style 18
{"activation_source": "name+style", "use_reference_image": false, "prompt_traits": "", "reference_path": null}
```

没有 CI 接线：仓库里没有 `.github/workflows`，这套断言要靠人手动跑。

## 对照判据打分

| 维度 | 判定 | 说明 |
| --- | --- | --- |
| 产物协议 | 强 | 四段式输出 + 固定开头格式 + 模式化后缀 + 路径 / 隔离块的分模式处理；CLI 有确定性实现且被断言 |
| description 路由 | 中上 | description 写清了「编号 + 主题 → 双语提示词」和「用能力数据决定是否必须传参考图」，但没有负例（何时不要用） |
| gotchas | 强 | 隔离声明、特征过滤、未知模型兜底、图文模式禁扩写、禁自造建议，都是模型稳定会犯的错 |
| 确定性脚本 | 强 | build / gallery / split / validate / prompt / resolve，各管一段，且校验会先跑构建 |
| 外部化状态 | 中 | 有 attribution / contact sheet state / version，但没有 job manifest 那种任务状态机（单次生成本来也不需要） |
| QA | 强（结构层） | 378 行不变量断言，覆盖数据、资产、交叉引用和 CLI 输出；但只管结构，不管「风格是否真的被激活」 |
| 负例 / evals | 中 | 校验里含负向断言（不许出现锚点、空特征必须兜底），但没有路由层 eval，也没有 CI |
| 渐进披露 | 中 | SKILL.md 直接指向 JSON 目录和脚本，没有 Perplexity 式「按步加载 references」的显式约束 |
| 相对判据页第七问 | 正例 | 审美（画风）被翻成编号 + JSON 取值域 + 正向/负向特征过滤 + 垫图兜底 |

## 收录建议

- **Awesome 分级：推荐** — 作为「审美取值目录 + 模型能力分层」的第二个正例（第一个是 mono-color），也是「参考图隔离」的干净样本。
- 不另开 topic 页：它是素材库 + skill，没有独立产品面。
- 与同批入库的 `hand-drawn-explainer-video-nikola` 是同域互补：这个库负责「画成什么样」，那个 skill 负责「怎么把一幅画边讲边画出来」。两者在 wiki 里的关系写到 [[手绘风格与讲解视频的工程约束]]。

## 风险 / 限制

- 结构不变量不等于语义正确：`gpt-image-2` 那 137 条名字激活标定只有作者盲测背书，wiki 无法验证；274 条「参考作者 / 风格名」把真实在世作者名字写进提示词，署名与许可是这套库的长期争议点（MIT 只声明软件部分）。
- 图片资产（274 张单图 + 41 张四宫格 + 拼图 + 118 张版式预览）随仓库分发，LICENSE 未逐一说明图像版权。
- gallery 的版本检查会去读 GitHub raw 的 `version.json`，是网络依赖；SKILL.md 里的路径示例假定安装在 Codex 的包根目录下。
- 会话初始化依赖 Codex 专有工具 `mcp__codex_app__open_in_codex`，换宿主必须改。
- 文档数字与数据不一致：README / LAYOUTS.md 写「117 种排版图型」「信息图 30 种」，`layouts.json` 实际 118 条（信息图 31 条，含 `IG-031`），且 `SC-013` 编号空缺。不影响使用，但校验脚本没有覆盖这个不一致。
