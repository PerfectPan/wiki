---
title: hand-drawn-explainer-video-nikola Skill 评审记录
date: 2026-09-22
topic: Awesome Agent Skills
sources:
  - https://github.com/hi-nikola/hand-drawn-explainer-video-nikola
  - https://raw.githubusercontent.com/hi-nikola/hand-drawn-explainer-video-nikola/main/SKILL.md
  - https://raw.githubusercontent.com/hi-nikola/hand-drawn-explainer-video-nikola/main/references/stroke-story-workflow.md
  - https://raw.githubusercontent.com/hi-nikola/hand-drawn-explainer-video-nikola/main/evals/evals.json
  - https://github.com/geeklee/srt-whiteboard-animation
---

# hand-drawn-explainer-video-nikola Skill 评审记录

## 术语速查（wiki 注，非评审原文）

- **逐笔（故事）动画**：同一块画布上，画中笔迹跟着讲解声一笔笔实时落出来的动画，像真有人在白板上边讲边画。
- **程序动画**：另一条路线，用 SVG/HTML/GSAP 把预先画好的卡片、关系图做成动效；没有真实的「落笔画画」过程。
- **旁白 / SRT / ASS**：讲解词的配音音轨；SRT 是简单字幕文件；ASS 是带出现时间、位置、样式的高级字幕文件（关键词文字用它逐字显现）。
- **TTS**：文字转语音，这里指自动生成配音；「系统朗读」指操作系统自带的机械朗读声，「edge-tts」是微软 Edge 的在线 TTS。
- **多幕**：一段视频分成多个场景段落（scene），每幕是一张独立画面。
- **`timeline.json` / 时间窗**：时间轴文件；「时间窗」指一块画面被分配到的出场时间段（从第几毫秒到第几毫秒）。
- **annotation（标注）/ 区域**：人在源图上框出的一块块待绘制区域。`protectedRegions` 是受保护、不被后画内容覆盖的区域。raw 里另出现「左右双语义岛」一词，指一种左右分栏的画面结构，skill 文档未给更细定义。
- **扣空**：一块区域被后画上来的区域完全盖住，在它自己的时间段里实际看不见。
- **静止假手**：没有笔画动作时，一只画出来的手停在画面中央不动。
- **后续区域提前**：下一块区域没轮到自己的时间就先冒出来。
- **`skeleton` / `contour-wipe`**：渲染参数，`--ink-path skeleton` 指定线稿走 skeleton 路径；`--color-fill contour-wipe` 指定一种按轮廓走的上色方式（raw 仅强调它「只让轮廓感知上色」，未展开机制）。
- **`hand-follow` / `hand-height`**：前者控制画出来那只手移动到新位置时的跟手平滑程度（不影响画线快慢）；后者控制手的尺寸（手越大遮挡越多）。
- **finalize（统一收尾）/ `--source-overlay`**：最后一道工序，统一全片帧率、尺寸和时间基准再合成视频；source-overlay 控制最后要不要把原始源图淡入盖上去。
- **边界帧 / 峰值帧 / 转场帧 / 首帧 / 末帧**：人工验收时要逐帧看的关键画面：两块区域交接处的帧、动作最高潮的帧、场景切换的帧、每段的第一帧和最后一帧。
- **evals**：一组写死的「用户提问 + 期望回答」测试样例（含故意诱导犯错的反例），靠人或模型自查，不是自动测试。
- **dry run**：不真正调收费接口、先空跑一遍验证流程。

## 基本信息

| 项 | 值 |
| --- | --- |
| Skill | `hand-drawn-explainer-video-nikola` |
| 仓库 | https://github.com/hi-nikola/hand-drawn-explainer-video-nikola |
| 作者 | Nikola（X [@Nikola314159](https://x.com/Nikola314159)） |
| 最后提交 | 2026-09-02 `3ee5d1c` "feat: 完善手绘视频 Skill 双路线与公开案例" |
| 访问日 | 2026-09-22 |
| 许可 | 原创脚本与文档 Apache-2.0；`vendor/srt-whiteboard-animation/` 保留上游 MIT；示例媒体 CC BY 4.0（仅限作者有权许可的部分），第三方与商标见 THIRD_PARTY_NOTICES.md |
| 形态 | SKILL.md（74 行 hub）+ `references/`（12 篇）+ `scripts/`（9 个 py/mjs/ps1）+ `vendor/`（上游运行时快照）+ `evals/evals.json`（13 条）+ `preferences.json` + `docs/` + `examples/`（三个真实案例） |
| 定位 | 中文手绘知识讲解视频：交付配音、字幕、时间轴、可编辑工程和**真实 MP4**，默认拒绝「假装完成」 |

## 它交付什么

按交付范围分三档：

- **只要提示词**：读 `references/prompt-workflow.md`，输出自包含的 Flow / Nano Banana 提示词，不调收费接口、不需要本地依赖（这是交付范围，不是第三条制作路线）。
- **样片**：10–15 秒代表镜头，验证人物、笔迹、字幕和节奏。
- **完整视频**：真实 MP4 + SRT + 原稿 + 独立配音 + `timeline.json` + 可编辑工程 ZIP + 简短制作说明与验证报告。

并且明确：完整成片最少要交真实 MP4；无法完成的部分要标成缺口，不能用别的东西顶替。

## 两条路线不可混称

| 用户想要的效果 | 路线 | 必读 |
| --- | --- | --- |
| 画面被画出来、边讲边画、笔尖跟着线走 | 逐笔故事动画 | `references/stroke-story-workflow.md` |
| 流程卡片、关系图、独立元素、精确文字 | 程序动画（HyperFrames + SVG/HTML + GSAP） | `references/automation-workflow.md` |

画面结构（单场景 / 多幕故事 / 左右双语义岛）和视觉风格（自然肤色 Q 版人物 / 小黑风格 / 其他手绘风格）是逐笔路线内部的可组合选项，SKILL.md 专门说明「不是额外路线」。仓库里写死了几条反冒充纪律：不以 SVG 动画冒充真实逐笔绘制、不把「手绘风静图平移」当成逐笔、不用于写实数字人、不假装已经完成无法验证的成片。

## 核心做法

**1）逐笔流水线的顺序是硬的。**
声音先行（复用或合成完整旁白 → 真实音频 → SRT → `timeline.json`）→ 设计一张可绘制的完整画面（先写 `DESIGN.md` 和每幕配图策略）→ 按故事语义标注区域（`annotation.json`：`sequence` / `subtitle` / `startMs` / `durationMs` / `region` / `protectedRegions`）→ 渲染 → 统一收尾 → 分层验收。

**2）源图必须「可画」。**
`stroke-story-workflow.md` 第 2 节规定：按渠道和故事空间选 9:16 / 4:3 / 16:9；20 秒以上且多事件优先拆成多幅连续故事画面，每幅承载一个 4–8 秒事件；清晰深色轮廓、有限平涂、低纹理、充足留白；不生成长句、日期、法条、Logo；避开蜡笔噪点、半调网点、密集排线、摄影纹理和大面积深色填充——因为它们会被误识别成墨迹。还规定不能只凭文稿臆测坐标，必须实际看图后标注。

**3）源图可绘制性检查。**
`scripts/check_drawable_regions.py` 在标注后、打开预览台前跑，检查区域越界（`region_out_of_bounds`）、矩形重叠（`region_overlap`）、岛间留白不足（`gutter_too_small`，警告）、以及显著前景连通线同时进入多个区域（`foreground_bridges_regions`）。失败优先拆成多幅画面，其次才修源图。正式渲染前还要跑后端 `scripts/annotation_schema.py`：坐标越界、画布尺寸不符、缺时序字段是阻断错误；顺序不连续、时间窗重叠是提醒。

**4）渲染参数与「速度问题」的正确解法。**
默认 `--ink-path skeleton --color-fill contour-wipe --hand-follow 0.35`。文档反复强调：`hand-follow` 只平滑手部显示位置，**不会减慢笔迹**；实际观感由「区域可用时长 ÷ 线条与色块复杂度」决定。笔迹还是太快时，按顺序处理：延长或重分旁白时间 → 减少小零件、排线和纹理 → 缩小区域承载内容 → 拆成下一幕。手部尺寸与速度分开控制（`--hand-height`），16:9 复杂群像试 260–340。

**5）一个时间轴不变量。**
某个区域被后续区域或 `protectedRegions` 完全扣空时，渲染器要保持当前画布到该区域时间窗结束，不在画面中央放一只静止的假手，也不让后续区域提前。文档明确说这条不能靠删掉区域规避。

**6）统一收尾避开多幕时间戳问题。**
`scripts/finalize_stroke_video.py` 吃一份 manifest（`width/height/fps/narration/ass/scenes[{video,image,durationMs}]`），默认 `--source-overlay never`，只统一帧率、尺寸和时间基准再合入旁白与 ASS 字幕。只有逐幕末帧对照确认漏色时，才改成 `--source-overlay always`，在每幕最后约 0.9 秒开始淡入批准源图（淡入约 0.65 秒）。这样避开不同幕帧数取整导致的 concat / PyAV 时间戳错误。

**7）音画解耦。**
换画风不触发换声音或重做内容一致的旁白。默认配音是火山引擎 `seed-tts-2.0` 的刘飞音色 `zh_male_liufei_uranus_bigtts`；没有授权音轨时，继续做画面、字幕、时间轴，并把配音列为未完成项，而不是静默换成系统朗读或 edge-tts。

**8）文字不交给图片模型。**
日期、专名、法条、Logo、长中文、关键数字走字幕或确定性文字层；关键词一般 2–6 个汉字，用 ASS 逐字 `\kf` 或等价方式显现，并检查不压人物表情、不进字幕安全区、不与下一区域碰撞。

**9）上游快照的边界管理。**
`vendor/srt-whiteboard-animation/` 固定在上游 commit `325c5c71`（baseline parent `523ae939`），只带运行时脚本、素材、测试和 LICENSE，**故意不含上游 SKILL.md 和 agent 元数据**，这样包内只有一个可触发 Skill。`references/upstream-whiteboard-review.md` 把上游能力分成「已吸收 / 已用自己的方案覆盖 / 不设为默认」三类，并写明第 4 类要先做样片验证。

## 容易踩的坑（文档和 evals 里反复出现的）

1. 用 `hand-follow` 去「调慢画线」——它只改手部显示位置（eval #11 专门考这个）。
2. 把 SVG 卡片动画称作「逐笔绘制」，或把整图淡入、卡片飞入冒充落墨（eval #3、SKILL.md 明文禁止）。
3. 末帧没对照就叠加源图，或在逐幕已经完整上色时仍 `--source-overlay always` ——可能造成片尾裁切、缩放、闪变（eval #12）。
4. 空掩码区域没占满时间窗 → 中央出现静止假手、后续区域提前。
5. 图片模型写长中文、日期、Logo → 出错字和伪字；长文字必须交确定性文字层。
6. 并发批量生图换速度 → 长时间没有中间结果时既无法判断哪张成功，也容易整批重做。文档要求逐张生成、返回后立即保存和检查。
7. 为赶时长把配音硬塞进字幕窗口 → 应该延长画面或调整分镜，而不是牺牲已确认配音的故事感。
8. 降帧掩盖手速问题、用不完整 FFmpeg 反复重试（缺 `libx264`/`crf`、复制共享版 exe 缺 DLL 都写在文档里）。
9. UTF-8 中文文件被系统按 GBK 解码 → 显式指定 UTF-8，必要时给子进程 `PYTHONUTF8=1`，不改系统区域设置。
10. 把某个环境成功当成本机可运行 —— 预检只做本地检查，不读密钥、不装依赖、不调收费接口；失败只阻止依赖该能力的阶段。

## 怎么验收

**evals（13 条，含反例）。** `evals/evals.json` 每条是一句用户口吻的 prompt 加期望输出，其中反例占相当比例：`#3` 用户说「后端不可用就直接给我做成差不多的 SVG」，期望是必须说明效果变化、不能称逐笔；`#11` 用户问「把 hand-follow 调到 0.1 就能让画线变慢吧」，期望是纠正误解并给出正确调整路径；`#13` 用户说「TTS 没配好就用系统朗读代替」，期望是明确配音缺口、不静默替换。

**分层验收。** `references/quality-and-delivery.md` 分四层：文本（原稿 vs 字幕，限定词和数字不能少）、工程（按当前 HyperFrames 版本跑完整检查）、实际成片（完整解码音视频、每场景至少抽一帧、加看动作峰值 / 转场 / 末帧）、内容动作（手和物件分别移动、没有多手 / 缺肢 / 中文变形）。

**逐笔专属 10 条 + 边界帧。** 首帧无提前露线、新墨线贴近笔尖、`sequence`/`startMs` 与旁白一致、已完成区域持续保留、末帧还原批准源图并留至少 0.5 秒、手部缓动不抢画面、无纹理误判导致的乱画或漏色、多幕无重复帧 / 时间戳跳变、最终 MP4 音画字完整；两个以上语义区域时，必须加看「前区完成前约 0.2 秒 → 后区开始后约 0.2 秒」，再看每个切点前后 3 帧和最终 0.3–0.5 秒。

**自动检查工具，并明确声明能力边界。** `scripts/media_check.py` 检查真实文件、帧数、音频数值、音轨 / 时间轴覆盖，输出运动统计和联系表；文档写明它「不执行语音识别、不证明语义同步、不评判人物美感」，退出码 0 只代表本次自动检查无错误，报告里的警告和人工检查仍须处理；还点明自动检查无法判断语义岛提前泄漏、关键词压脸、片尾源图覆盖，必须看真实帧。`scripts/quick_validate.py` 是静态回归检查：frontmatter name、两条路线措辞、vendor 不含第二份 `SKILL.md`、默认音色与资源、凭据政策、后端运行时文件存在等。

**预检。** `scripts/preflight.py`（本地、不读密钥、不装依赖、不调配音）按机器发现文件填 `node` / `hyperframes_cli` / `chrome` / `ffmpeg` / `ffprobe` / `media_python` 等路径；`scripts/stroke_story_preflight.py` 额外检查内置后端、隔离 Python、渲染参数，并在临时目录完成一次无网络的小型 MP4 渲染与解码。`references/preflight-and-recovery.md` 按失败类型给恢复路径（DLL 初始化失败、模型权重缺失、缺开发依赖、浏览器超时、GBK 解码、布局冲突），并规定「无任何变化不再重跑同一命令」。

**没有 CI。** 仓库没有 `.github/workflows`；`evals.json` 是静态期望文本，不是可执行回归，`quick_validate.py` 也要人手动跑。

**本次评审的验证范围。** 只读代码与文档（2026-09-22）。本机没有跑渲染链路：逐笔路线需要 Python 3.10+ 隔离环境和 FFmpeg，预检与冒烟渲染都会装依赖 / 调本地编码器，超出这次只读评审的范围。所以「预检和冒烟渲染真的能跑通」这条是作者仓库的声明，wiki 未独立验证。

## 对照判据打分

| 维度 | 判定 | 说明 |
| --- | --- | --- |
| 产物协议 | 强 | 交付物清单写死（MP4 / SRT / 原稿 / 配音 / timeline / 工程 ZIP / 验证报告）+ 项目文件布局 + timeline 与 finalize manifest 两个 schema |
| description 路由 | 强 | 场景词明确（边讲边画 / 一笔一笔画出来 / 白板手绘 / 先画左边再画右边 / 知识讲解动画），并带负例（不用于写实数字人、不假装完成） |
| gotchas | 强 | hand-follow 不减速、contour-wipe 只叫轮廓感知上色、空掩码占满时间窗、source-overlay 默认 never、缺 TTS 不静默替换、图片模型不写长文字 |
| 确定性脚本 | 强 | 预检两个、区域检查、标注 schema、统一收尾、媒体验收、静态回归、配音 dry-run，各自边界清楚 |
| 外部化状态 | 中上 | 项目状态文件 + `timeline.json` + finalize manifest + 验证报告；但没有 hatch-pet 那种 job manifest / repair 状态机 |
| provenance | 强 | vendor 固定 commit + 保留 MIT + 明确排除上游 SKILL.md；上游借鉴记录分「已吸收 / 已覆盖 / 不设默认」；小黑风格标注来源并统一命名 |
| QA | 强 | 四层验收 + 逐笔 10 条 + 边界帧看片规定 + 明确声明自动检查的能力边界 |
| 负例 / evals | 强（文本层） | 13 条 evals 里有多条纠正误解和禁止冒充；但静态文本，无执行回归 |
| 相对判据页第六问（失败能否局部 repair） | 部分正例 | 强调「保留已通过阶段，只重做受影响阶段」，但靠规范约束而不是 manifest 驱动 |
| 相对判据页第七问（审美转检查项） | 正例 | Q 版蜡笔风格规范把配色 / 笔触 / 构图 / 运动写成可复制提示词块，并列出禁标签卡、禁字幕区文字等逐条约束 |

## 收录建议

- **Awesome 分级：推荐** — 现有案例里唯一覆盖「视频生产线」的样本，而且产物协议、provenance 和「自动检查不等于验收」的声明质量都在线。
- 不另开 topic 页：它是 skill 仓库，不是产品。
- 域内知识与同批入库的 [[handdraw-style-prompter]] 互补，合并写进 [[手绘风格与讲解视频的工程约束]]。

## 风险 / 限制

- **Windows 优先**：配音脚本 `volcengine_tts.ps1` 和 `install.ps1` 是 PowerShell，安装文档用 `$env:USERPROFILE`，本机验证组合（Python 3.12 + faster-whisper 1.2.1 / CTranslate2 4.8.1）也写在 Windows 语境里；macOS / Linux 的使用者要自己翻译。
- **依赖外部付费与授权**：云配音（火山引擎）、生图、图生视频都是可选能力，可能收费；文档反复要求先 dry run、复用缓存、避免盲目重试，但成本仍然由用户承担。
- **evals 不是回归测试**：13 条是期望文本，靠人或模型自查；没有 CI。
- **公开案例不完整**：README 提到的 7 分 29 秒完整成片没有公开，仓库只保留 36 秒精简工程；示例媒体只对作者有权许可的部分给 CC BY 4.0。
- **风格资产不成套**：`references/style-selection-and-updates.md` 自己列了「当前具备 / 当前不具备」，Q 版蜡笔风格只有文字规范和 Flow 提示词，没有示例图与已验证动画工程。
- 上游快照会随 geeklee/srt-whiteboard-animation 演进；文档要求「只吸收能用真实样片验证、且不改变已确认画风和配音的机制」，但这条靠维护者纪律，没有自动化检查。
