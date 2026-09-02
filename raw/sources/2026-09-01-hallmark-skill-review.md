---
title: hallmark Skill 评审记录
date: 2026-09-01
topic: Awesome Agent Skills
sources:
  - https://www.usehallmark.com/
  - https://github.com/nutlope/hallmark
  - https://raw.githubusercontent.com/nutlope/hallmark/main/skills/hallmark/SKILL.md
  - https://raw.githubusercontent.com/nutlope/hallmark/main/skills/hallmark/references/slop-test.md
  - https://raw.githubusercontent.com/nutlope/hallmark/main/skills/hallmark/references/structure.md
  - https://raw.githubusercontent.com/nutlope/hallmark/main/skills/hallmark/references/anti-patterns.md
---

# hallmark Skill 评审记录

## 基本信息

| 项 | 值 |
| --- | --- |
| Skill | `hallmark` v1.1.0 |
| 仓库 | https://github.com/nutlope/hallmark |
| 出品 | Together AI，MIT |
| 形态 | SKILL.md（67KB hub）+ `references/`（structure 15KB / study 43KB / anti-patterns 26KB / slop-test 31KB / verbs/*） |
| 规模 | 20 themes · 21 macrostructures · **58 道 slop-test 门禁** |
| 定位 | 「拒绝 AI 味」的设计 skill：greenfield 建页、审计、重设计、设计 DNA 提取 |
| 谱系 | 自述规则来自 Anthropic frontend-design skill、Claude cookbook frontend aesthetics、2026 "tactile rebellion" 共识 |
| 访问日 | 2026-09-01 |

## 四个动词，各有各的输出

一个默认行为 + 三个显式动词，每个有独立输出契约：

| 动词 | 输入 | 输出 |
| --- | --- | --- |
| *(default)* build | 简报/项目 tokens/框架 | 可工作页面 + stamp（印章式元数据），交付前过 58 门禁 |
| `audit` | 任意页面 | **只诊断不修改**：按反模式目录打分的排序 punch list |
| `redesign` | 现有页面 | 保留路由/组件归属/文案意图/品牌/IA，只换视觉-交互层；`--mood` 可选 |
| `study` | 截图或 URL | DNA 诊断报告 → 三选一后续：用 DNA 重建 / lock 成可移植 `design.md` / 停在诊断 |

### study 的防御性设计（最重的部分）

- URL/图片模式自动检测；URL 模式经 WebFetch 浅抓取，HTML/CSS 按不可信惰性数据处理，忽略页面内的一切远程指令
- 拒绝清单：themeforest / framer templates / webflow templates / gumroad UI kits / dribbble / behance；auth 墙、SPA 壳、<1KB body → 显式降级要截图，不许静默退化
- 「永不复制像素」；`design.md` 发射比诊断有更紧的拒绝层，需声明来源是自己的作品或自有品牌的公开参考
- 提取结构不提取像素：macrostructure、archetypes、type-pairing、colour anchor

## 核心机制

- **先选宏结构，再穿衣**：六轴结构指纹——标题位置 / 正文构图 / 分隔语言 / 按钮语气 / 图像处理 / 出场模式；每轴有命名模式与真实世界参照。
- **不重复最近 3 个宏结构**：读取项目记忆，拒绝重复；slop test 第 F 轴按「结构距离」而非视觉距离评分——换配色不算变化。
- **58 道门禁 + 交付前自评**：交付前逐项回答且必须全为 no；门禁分通用与 genre 域（atmospheric 放宽 radial-bloom 门、modern-minimal 放宽零彩中性门）；先跑自评六轴（Philosophy/Hierarchy/Execution/Specificity/Restraint/Variety）再写预览块的 slop test 行。
- **20 主题 × 结构指纹表**：每主题建议 heading/body/divider/button/image/reveal/nav/footer 组合；不知道选什么时按领域给三选一，**永不默认**。
- **8 条基础约束**：Type（双字体分工）/ Colour（OKLCH、单锚色、强调 <5%）/ Space（命名刻度、4 的倍数、禁止随手 17px）/ Motion（指数缓出、每动画配 reduced-motion 替代）/ Voice（每主题独立语域，禁 SaaS 中性腔）/ Layout（偏置不对称）/ Hierarchy（2 秒可读的 display/body/label 权重梯）/ Restraint（**better nothing than bad something**）。
- **按需加载 references**：slop-test.md 明确「此步才加载，更早不需要」；动词执行前必须先读对应 reference，不许凭直觉。

## 对照判据打分

| 维度 | 判定 | 说明 |
| --- | --- | --- |
| 产物协议 | 强 | 四动词各有输出契约；audit 的「只诊断不修改」是干净的职责切分 |
| description 路由 | 强 | 动词路由 + 歧义时一次澄清（study 还是当参考？） |
| gotchas | 强 | 反模式目录点名成册；模板市场 URL 拒绝；不可静默降级 |
| 渐进披露 | 强 | hub + 按步加载 references，且写明加载时机 |
| 确定性脚本 | 弱 | 未见 scripts/ 与 evals 目录；宏结构记忆靠上下文非外部 manifest |
| QA | **最强** | 58 门禁 + 六轴自评 + genre 作用域；audit 把 QA 本身做成了动词 |
| 负例 / evals | 强（负例侧） | anti-patterns.md 26KB 命名式负例目录；无路由 evals |
| 相对 mono-color | QA 更重、目录化稍轻 | mono-color 有 CI 校验的 evals 断言；hallmark 靠门禁清单与结构指纹 |
| 相对判据页第七问 | 直接正例 | 审美品味（AI slop）→ 命名目录 + 结构指纹 + 逐项门禁 |

## 收录建议

- **Awesome 分级：推荐（recommended）** — 作为「反默认失败型 Skill」与 QA 门禁化正例。
- 与 [[AI Slop]] 页的既有归纳（kill-ai-slop / remove-ai-slops）同域：hallmark 把 slop 识别升级为**产物侧的生成约束 + 交付侧门禁**，是「识别清单 → 生成时约束」的工程化路径。
- 纯 skill 形态，无独立产品面，不另开 topic 页。

## 风险 / 限制

- SKILL.md 67KB + references 全量 >150KB，上下文成本为已收录案例中最高；渐进披露是必要补偿而非可选优化。
- 「拒绝重复最近 3 个宏结构」依赖会话内项目记忆，跨会话需外部 memory 配合，skill 自身未提供 manifest。
- 58 门禁由模型逐项自评，无脚本强制；与 hatch-pet 的确定性编译思路相比仍是「自检」而非「验证」。
- 评审基于源码与文档（2026-09-01），未实测生成质量。
