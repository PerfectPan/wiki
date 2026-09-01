---
title: AI Slop
description: 识别生成式默认选择在界面、文案与代码中留下的具体重复模式，并区分坏味道与有意设计。
type: topic
category: ai
created: 2026-07-11
updated: 2026-09-01
timestamp: 2026-09-01
tags:
  - design
  - frontend
  - code-quality
  - writing
source_refs:
  - https://github.com/yetone/kill-ai-slop/blob/6bfd693c075d405e2061620ce31b3d8c4eb4b920/skill/references/taxonomy.md
  - https://github.com/yetone/kill-ai-slop/blob/6bfd693c075d405e2061620ce31b3d8c4eb4b920/skill/references/detection.md
  - https://github.com/code-yeongyu/oh-my-openagent/blob/17104e1f6c86a47ab50ab2e1f5b5e0a6603443b8/packages/shared-skills/skills/remove-ai-slops/SKILL.md
resource:
  - https://github.com/yetone/kill-ai-slop/blob/6bfd693c075d405e2061620ce31b3d8c4eb4b920/skill/references/taxonomy.md
  - https://github.com/yetone/kill-ai-slop/blob/6bfd693c075d405e2061620ce31b3d8c4eb4b920/skill/references/detection.md
  - https://github.com/code-yeongyu/oh-my-openagent/blob/17104e1f6c86a47ab50ab2e1f5b5e0a6603443b8/packages/shared-skills/skills/remove-ai-slops/SKILL.md
---

# AI Slop

## 摘要

AI slop 不是“用了 AI 就一定很差”，而是生成式默认选择在缺少取舍时反复出现：界面把能加的效果全堆上去，文案只说空泛的好处，代码为了显得完整而增加并不承担责任的分支、抽象和注释。它们的共同问题不是某个 CSS 类、词语或函数本身，而是**没有服务具体产品、读者或边界的默认套路**。

以下模式来自两个公开规则集的归纳：一个聚焦 UI 和文案，另一个聚焦代码质量。它们是审阅清单，不是自动删除清单。

## 界面与视觉

### 配色

| 模式 | 常见形态 | 更好的判断 |
| --- | --- | --- |
| 蓝紫渐变 | `indigo → violet → pink` 被用于 hero、按钮、阴影和背景 | 颜色是否来自品牌或内容语义；若只是“看起来像 AI 产品”，删到一个有理由的强调色 |
| 渐变标题 | `background-clip: text` 的彩色大标题 | 标题层级应先靠字号、字重与留白；渐变必须有信息或品牌理由 |
| 棕黄“温暖”色盘 | stone / amber / orange 浅底铺满页面 | 食物、工艺、纸本等领域可成立；普通工具产品不应把“温暖”简化成焦糖色 |
| 默认语义彩虹 | 蓝提示、黄 warning、绿 success、红 error 各自套 `-50/-600` | 状态要先用文案和层级表达；语义色应来自自己的色板且只用于真正需区分的状态 |
| 同色三件套状态框 | 同一红/黄/绿同时做背景、边框和文字 | 中性底加一处克制提示通常更可读；不要让颜色承担全部信息 |
| 氛围渐变 | 深色页面后方一团 radial glow，卡片也从上亮到下暗 | 若不指向对象或层级，就是装饰噪音；用实色、细边和紧阴影建立层次 |

### 字体与层级

| 模式 | 常见形态 | 更好的判断 |
| --- | --- | --- |
| 单词衬线斜体 | 无衬线标题中突然插一个 Playfair / Lora 斜体词 | 这是廉价“编辑感”；优先用同家族字重、换行或位置强调 |
| UI 正文滥用展示衬线 | SaaS / 工具正文使用大幅 display serif | 出版和内容产品可以有意使用；信息密集 UI 默认应优先可读性 |
| 装饰性删除线、荧光笔和下划线 | 非编辑语义的 strike、mark、underline | 删除线用于删除，underline 用于链接；装饰需表达额外含义 |
| 句内高亮关键词 | 一段正文不断用彩色词或粗体词“抓重点” | 让标题、段落结构和留白承担重点；保留真正的术语或风险提示 |
| 终端风格泛化 | 非代码 UI 使用等宽字体、ASCII 边框、黑底暖色 | 只有当终端隐喻是产品的真实交互语言时才保留；代码区之外使用普通 UI 字体 |

### 组件与版式

| 模式 | 常见形态 | 更好的判断 |
| --- | --- | --- |
| 发光状态点 | 在线/ready 点带 ping、pulse 或绿色光晕 | 状态应有文字和稳定图形；动画只在真的传达变化时使用 |
| 彩色左边框 callout | 每段内容都包成 rounded card + `border-left: 4px` | callout 是例外语义，不是列表的皮肤 |
| 粉彩图标砖 | feature grid 中每个 icon 都在浅色圆角方块里 | 图标只在能快速区分内容时出现；优先明确的文本和信息结构 |
| 玻璃拟态和过大圆角 | backdrop blur、半透明卡、`rounded-full` 卡片、24px+ radius | 表面应有清楚层级；圆角要一致并满足内外嵌套关系 |
| 巨大模糊阴影 | 小卡片拖着几十像素范围的阴影 | 阴影应与元件尺度匹配；细边或紧接触阴影通常足够 |
| 不嵌套的圆角 | 外层和内层使用相同的大 radius | 内圆角应按 padding 收缩，或干脆不要多层容器 |
| 徽章和 pill 泛滥 | 每处都有 New、Beta、Popular、Pro 的圆角色块 | badge 只表示真实状态、版本或稀缺信息 |
| AI 感 SVG 吉祥物 | blob、圆眼、宇宙飞船等与产品无关的内联 SVG | logo/插画要服务识别或叙事，不应用来填空 |
| 图标套同色半透明底 | 蓝 icon 放蓝色透明圆角方格，重复出现在每个 feature | 图标可继承正文色；背景色应表达可交互或状态，而非纯装饰 |
| 全大写数据卡墙 | 大写 micro-label + 数字/图标的三列可互换卡片 | 展示一个真正重要的指标；其余信息按任务流组织 |

## 文案

| 模式 | 典型信号 | 替代方式 |
| --- | --- | --- |
| 空泛的 AI 营销语 | “not just X, it’s Y”、“unlock the power”、“game-changer”、“blazing fast” | 说清对象、数字、限制和后果，例如“索引时间从 10 分钟降到 4 分钟” |
| 三段式口号 | “Fast. Beautiful. Yours.”、每段都是短促形容词 | 用一个可验证的主张和解释它的证据 |
| emoji 当 UI 结构 | 每个标题、按钮和 bullet 都有 ✨🚀🔥 | emoji 只在内容语义或人际语气确实需要时使用；不要替代信息层级 |
| 宽泛承诺 | seamless、effortless、next-level、revolutionary | 描述具体动作、输入、输出与失败边界 |

## 代码

| 模式 | 具体症状 | 默认处理 |
| --- | --- | --- |
| 明显注释 | 重述代码、章节分隔线、被注释掉的旧代码、没有行动项的 TODO | 删除；但保留业务原因、边缘条件、工单链接、算法/正则解释和 BDD 标记 |
| 过度防御 | 对静态保证的值重复 null/type check、每层重复校验、无理由 catch-all | 保留系统边界、I/O、外部 API 和可空 DB 字段的防御；要删边界校验必须先证明内部已有等价保护 |
| 伪完整的异常处理 | `except Exception`、空 `catch {}`、只 `console.error(e)` 的 catch | 捕获已知错误并收窄类型，未知错误向上抛；顶层 CLI/HTTP 边界的记录加重抛可合理 |
| 不必要复杂度 | 超过三层嵌套、复杂三元、四个以上谓词混在一处、超过五个散参数、巨大函数 | 用 guard clause、命名中间值或结构化参数；性能热点和仓库既有惯例不应机械改写 |
| 变体分支链 | 按 enum/type/literal 做长 `if/else if` 链 | 在语言和项目惯例支持时改为穷尽匹配；布尔和范围判断本身不是坏味道 |
| 为未来而抽象 | 单次使用的 wrapper、只有一个实现却无测试/替换价值的 interface、只调用构造器的 factory | 删除或内联；真正隔离框架、测试替身或多个实现的 seam 应保留 |
| 层次泄漏 | UI 直接 import DB driver、handler 内塞业务规则、所谓 pure 函数偷偷 I/O | 把职责放回所属层；已有的务实短路模式需结合仓库判断 |
| 死代码 | 未用 import/private function、不可达分支、遗留 feature flag、debug print | 删除前检查反射、动态分发、字符串查找和回滚开关 |
| 伪重复 | 两段代码表面相似但业务意图不同，被强行抽成 helper | 只抽取真正相同且预期共同演化的逻辑；偶然相似宁可留在原处 |
| 伪“性能优化” | 将算法或缓存策略改复杂，却无法证明语义等价 | 只做显然等价的改动，如 hoist 重复计算、避免一次性中间集合、批量独立调用；不确定就不动 |
| 测试缺口 | 变更引入的可观察行为没有窄回归测试 | 先补最小行为测试；测试不绿时不要用“清理”之名继续删除 |
| 过大模块 | 超过 250 行纯代码，混合模型、规则、适配器和 I/O | 依职责拆成命名明确的模块；不要用 `utils`、`helpers`、编号文件或注释/空行规避 |

## 判断边界

“像 AI”不是充分证据。以下情况通常应先保留，再查产品语境：

- 紫色就是品牌色，或渐变是 logo/插画的必要部分；
- 衬线是出版、文化或内容产品的系统性选择；
- emoji 来自用户内容、选择器或真实对话语气；
- status badge、异常捕获、校验、重复代码和大文件存在可验证的业务/运行时理由；
- 某个复杂路径是受过 benchmark 约束的热点，或是项目长期一致的实现方式。

判断顺序应是：它服务什么具体对象？有没有更简单、仍保留该对象的做法？若不能明确证明，就把它记录为待讨论项，而不是删除。

## 来源指针

- [视觉、文案与组件模式](https://github.com/yetone/kill-ai-slop/blob/6bfd693c075d405e2061620ce31b3d8c4eb4b920/skill/references/taxonomy.md)
- [检测信号与常见误报](https://github.com/yetone/kill-ai-slop/blob/6bfd693c075d405e2061620ce31b3d8c4eb4b920/skill/references/detection.md)
- [代码异味与保留条件](https://github.com/code-yeongyu/oh-my-openagent/blob/17104e1f6c86a47ab50ab2e1f5b5e0a6603443b8/packages/shared-skills/skills/remove-ai-slops/SKILL.md)
- [hallmark](https://github.com/nutlope/hallmark) — 把本页的识别思路升级到生成侧：宏结构优先 + 58 道交付门禁；评审见 `raw/sources/2026-09-01-hallmark-skill-review.md`，收录见 [[Awesome Agent Skills]]
