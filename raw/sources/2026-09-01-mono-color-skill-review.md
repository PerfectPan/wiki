---
title: mono-color-skill 评审记录
date: 2026-09-01
topic: Awesome Agent Skills
sources:
  - https://github.com/yanliudesign/mono-color-skill
  - https://raw.githubusercontent.com/yanliudesign/mono-color-skill/main/SKILL.md
  - https://raw.githubusercontent.com/yanliudesign/mono-color-skill/main/design-system/colors.json
  - https://raw.githubusercontent.com/yanliudesign/mono-color-skill/main/evals/evals.json
  - https://raw.githubusercontent.com/yanliudesign/mono-color-skill/main/scripts/validate_design_system.py
  - https://raw.githubusercontent.com/yanliudesign/mono-color-skill/main/.github/workflows/validate.yml
---

# mono-color-skill 评审记录

## 对象

| 项 | 值 |
| --- | --- |
| Skill | `mono-color` |
| 仓库 | https://github.com/yanliudesign/mono-color-skill |
| 版本 | v1.2.0（CHANGELOG），MIT License |
| 形态 | 单 SKILL.md（34KB）+ `design-system/` 机器可读目录 + `evals/` + 校验脚本 + GitHub Actions |
| 热度 | ~2400 stars / 140 forks（发布约两周，2026-09-01 访问） |
| 定位 | 把主题、句子、实物或照片生成为「单墨/受控双色」编辑印刷风图像：孔版印刷质感、网点照片、25%-55% 留白、克制排版 |
| 访问日 | 2026-09-01 |

## 产物协议（事实）

- **三件套交付**写死在 SKILL.md `Output Format` 节：生成栅格图 + 最终生成 prompt（```text 代码块）+ 本次配方说明（Mode / Ink / Layout / Type / Process / Originality 六字段）。prompt-only 仅在用户明确要求或无图像生成能力时允许。
- **Recipe Manifest**（Input Reading 之后的强制中间产物）：21 字段 YAML——subject、intent、exact_text、representation、ratio、carrier、substrate、mode、palette、inks、plate_roles、layout、empty_paper、visual_tension、focal_event、release_zone、unresolved_edge、image_treatment、type_hierarchy、disruption、imperfection_seed、imperfections。要求"do not skip fields"且默认不向用户暴露。
- **design-system/ 目录是 source of truth**：colors / compositions / typography / rhythm / carriers / imperfections 六个 JSON catalog，分别定义色板与底色、布局族几何、排版角色、视觉张力、载体信号（poster/zine/journal 等的 required/forbidden signals）、受控印刷瑕疵取值域。SKILL.md 明确："when an exact value differs, the catalog wins"——散文解释意图，目录约束取值。
- **确定性与默认值**：同输入必须解析出同一 manifest；通用色词有固定别名（blue→Cobalt、green→Botanical Green 等）；未指定主体默认 Cobalt + Terracotta；`imperfection_seed` 要求由 subject/text/palette/layout 推导稳定 hash 并跨重试保持。
- **失败降级路径**：精确文字渲染错误时，重试一次后改为生成 text-light 底图并声明排版应在布局工具中叠加，"Do not pretend distorted text is correct"。

## description / 路由

frontmatter description 是场景路由而非功能广告：列出中英双语触发场景（单色海报、双色印刷、单色调视觉、孔版印刷、risograph、网点照片、zine poster、duotone print、mono-color style 等）。SKILL.md 尾部另有 `Example Triggers` 节，8 条真实句式（中文 5 条、英文 3 条），覆盖海报、照片改风格、封面、沿用既有视觉等入口。

## 高价值 gotchas（摘自 SKILL.md）

- **墨数判定规则**：底色不算墨；两版叠印产生的深色不算第三种墨；墨量浓淡（近黑、浅网）只是 density 变化——模型极易把这三类误判为「三色」。
- **单色作业的套准漂移**：one-ink 中 registration drift 只能表现为同一墨的淡色二次印象，不引入第二色。
- **反自动做旧**：网点 + 限墨 ≠ 复古。未明确要求时禁止黄纸、褪色、sepia、旧化边框、怀旧道具（"automatic vintage styling" 列入 Hard Avoids）。
- **无参考图时反 stock-photo**：不默认完整人像/广告姿势，改用 2-4 个识别锚点（如"手扶车把、一段弯腿、轮弧、发丝方向"）做局部编辑裁切。
- **文字是素材不是装饰**：手写体只能做短插入语，永远不承载日期、地点、事实；微缩文字可作纹理但不得虚构机构、URL、赞助商。
- **浪漫主题反道具清单**：不用串灯、酒杯、星空、逆光剪影，改用一个可观察关系（共边、使用痕迹、暗示亲近的裁切）。

## 质量门与 evals

- **Final Quality Gate**：约 20 项语义 checklist——底色与墨数、焦点事件唯一、release zone 更安静、主体占画 45%-80%、标题与主体交叉/覆盖/紧锁、纸上曝光形成可见形状、字号 5x-12x 跳变、≤3 个 type voices、缩略图可识别、相对参考 ≥4 处结构差异等。
- **Generation and Inspection**：8+ 条重生成判据（出现第三墨、accent 超 30% 无理由、读作数字调色而非物理印刷、留白出界、主体不可识别、无 5x 字号跳变、文字乱码/虚构品牌、过贴参考等）。
- **evals/evals.json**：16 条 eval，每条含 prompt（多为中文真实句式）、expected_output、机器可查 assertions（`ratio`、`mode`、`ink_hexes`、`plate_roles`、`layout` 等），配 `evals/schema.json` 契约。
- **CI 强校验**（`.github/workflows/validate.yml`）：`validate_evals.py` 验 eval 契约、`validate_design_system.py` 验六目录一致性与参考板 PNG 尺寸、全量 JSON 语法检查。设计系统的取值域本身有回归保护。

## 原创性防火墙（独有设计）

Originality Firewall 把「不抄参考」变成可枚举规则：对任何给定参考，subject and crop / layout family / headline wording / headline location / image shape or count / grid structure / type pairing / metadata treatment / ratio / disruption device 十个结构变量至少改变四个；禁止复现参考的物件排布、断行、日期、logo、边框系统和签名。

## 对照判据打分（见 Skill 工程化 synthesis）

| 维度 | 判定 | 说明 |
| --- | --- | --- |
| 产物协议 | 强 | 三件套 + 21 字段 Recipe Manifest；交付物与配方均结构化 |
| description 路由 | 强 | 双语场景触发词 + Example Triggers |
| gotchas | 强 | Hard Avoids + Quality Gate + 失败判据；墨数判定类 gotcha 是模型稳定踩坑点 |
| 数据驱动目录 | 强 | design-system/*.json 为 source of truth，"catalog wins"；本仓库现有案例中独有 |
| 确定性脚本 | 中 | 校验脚本 + CI 在仓库侧完整；但运行时编译（seed hash、瑕疵选择）仍由模型执行，无脚本强制 |
| QA | 强（语义层） | 结构层在 CI，语义层为可枚举 checklist；retry-once + text-light 降级 |
| 负例 / evals | 中上 | 16 条 eval 带 assertions 且进 CI；但缺相邻 skill 混淆类 negative routing eval |
| repair / manifest | 弱-中 | 无 job manifest 与局部 repair；单次生成任务属性使然，降级路径存在 |
| 相对 bento-slides | evals/CI 更完整 | bento 强在单文件产物契约；mono-color 强在取值域目录化 + 评测回归 |
| 相对 hatch-pet | 无流水线 | 无 manifest 状态机、无确定性编译、无局部 repair |

## 收录建议

- **Awesome 分级：推荐（recommended）** — 作为「视觉系统约束型 Skill」正例。
- 判据页视角的价值：现有案例覆盖「资产流水线型」（hatch-pet）与「文档产物协议型」（bento-slides），mono-color 补上第三类——**把审美判断工程化**：取值域收进 catalog、验收写成可枚举 checklist、原创性写成变量替换规则。适用于输出质量依赖大量主观约束的生成任务。
- 本笔记只评 skill；作者的设计方法论本身不另开产品页。

## 风险 / 限制

- 效果强依赖底层图像生成模型的网点/限墨执行力；evals 的 assertions 是设计意图断言，未见公开的自动化跑分结果。
- SKILL.md 34KB 全量加载，上下文成本偏高；design-system 六目录按需读取的指引存在，但加载纪律靠模型自觉。
- 评审基于源码与文档阅读（2026-09-01），未实际安装跑图验证输出质量。
