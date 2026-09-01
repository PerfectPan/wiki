---
title: Skill 工程化的产物协议范式
description: 成熟 Agent Skill 的判据：产物协议、路由、gotcha、manifest、QA 与 repair；案例含 hatch-pet、ai-cli、bento-slides、mono-color
type: synthesis
category: ai
created: 2026-05-06
updated: 2026-09-01
timestamp: 2026-09-01
tags:
  - agent
  - skills
  - workflow
  - qa
  - provenance
  - evals
  - cli
source_refs:
  - raw/sources/2026-05-06-codex-pet-skill-article.md
  - https://mp.weixin.qq.com/s/uH71k1yAoF6xjsOYmVAJBg
  - raw/sources/2026-05-06-perplexity-agent-skills.md
  - https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity
  - raw/sources/2026-05-12-ai-cli-skill-review.md
  - https://github.com/vercel-labs/ai-cli/blob/main/skills/ai-cli/SKILL.md
  - raw/sources/2026-08-06-bento-slides-skill-review.md
  - https://github.com/nyblnet/bento/blob/main/plugins/bento-slides/skills/bento-slides/SKILL.md
  - raw/sources/2026-09-01-mono-color-skill-review.md
  - https://github.com/yanliudesign/mono-color-skill
resource:
  - raw/sources/2026-05-06-codex-pet-skill-article.md
  - https://mp.weixin.qq.com/s/uH71k1yAoF6xjsOYmVAJBg
  - raw/sources/2026-05-06-perplexity-agent-skills.md
  - https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity
  - raw/sources/2026-05-12-ai-cli-skill-review.md
  - https://github.com/vercel-labs/ai-cli/blob/main/skills/ai-cli/SKILL.md
  - raw/sources/2026-08-06-bento-slides-skill-review.md
  - https://github.com/nyblnet/bento/blob/main/plugins/bento-slides/skills/bento-slides/SKILL.md
  - raw/sources/2026-09-01-mono-color-skill-review.md
  - https://github.com/yanliudesign/mono-color-skill
---
# Skill 工程化的产物协议范式

## 问题

一个真正有工程价值的 Agent Skill，和普通 prompt wrapper 或轻量 workflow 的区别在哪里？

## 简答

成熟 Skill 的核心不是“让模型换一种说法”，而是在上下文预算内封装模型会稳定用错、漏用或不一致的领域 know-how。它既要先定义可消费的产物协议，也要用 description 做精确路由，用 evals 防止误加载，用 manifest 外部化任务状态，用脚本处理确定性编译，用 provenance 约束来源，用 QA 区分结构正确与语义正确，最后通过局部 repair 收敛失败。当约束本质上是审美或品味判断时，还要把它们翻译成机器可读的取值域目录、变量替换规则和逐项验收清单，主观质量才能被稳定执行。模型负责生成候选，不应直接拥有最终提交权。

## 综合结论

`hatch-pet` 的启发不在于 Codex 宠物本身，而在于它把一个看似主观的图像生成任务，改造成了可审计的资产流水线。用户输入只是 intent，最终交付却是 Codex app 能加载的 `pet.json` 与 `spritesheet.webp`。中间经过 request、job manifest、生成候选、来源记录、确定性编译、QA、局部修复和打包。

这说明 Skill 的价值边界应当从“提示模型怎么做”上移到“定义产物如何被验证和消费”。如果一个 Skill 只包含人格设定或几段 instructions，它最多是 prompt 模板；如果它定义了产物契约、状态机、工具边界、验收标准和失败修复路径，它才开始接近工程组件。

`hatch-pet` 展示了几条可迁移原则：

- **模型输出是生产材料，不是最终成果。** 图像模型可以生成 base pet 和 row strips，但只有经过记录、抽帧、拼 atlas、验证和打包后，才成为可加载资产。
- **关键状态必须外部化。** 长任务不能靠模型上下文记忆进度，`imagegen-jobs.json` 这类 manifest 才能承载依赖、输入、输出、来源、hash、派生规则和完成状态。
- **并行不等于共享提交权。** 子代理可以生成候选和写 QA note，但不能修改 manifest、record、finalize、repair 或 package；父代理作为 control plane 统一提交 truth。
- **确定性脚本应承担编译器角色。** 抽帧、透明背景检查、尺寸校验、hash 校验、spritesheet 组装和打包都不该让模型自由发挥。
- **QA 要分结构层和语义层。** schema、尺寸、alpha、帧数、空 cell 可以自动验证；身份一致性、状态语义和视觉质量仍需要视觉检查。
- **repair 优于 retry。** 失败时重开最小失败范围，保留已通过部分，比整套重跑更稳定、更便宜，也更符合生产系统的维护方式。

这套范式也能迁移到代码、UI、文档、知识库、数据处理和自动化运营任务。凡是输出物要长期复用，就应该问：

1. 最终产物的消费协议是什么？
2. 哪些步骤是模型生成，哪些步骤必须确定性执行？
3. 任务状态是否写在外部 manifest 中？
4. 来源、hash、依赖和完成状态是否可审计？
5. QA 是否同时覆盖结构正确和语义正确？
6. 失败后能否局部 repair，而不是只能整体 retry？
7. 主观或审美判断是否已被翻译成可枚举的取值域、防火墙规则与逐项验收清单？

## Perplexity 的 Skill 设计原则

Perplexity 这篇文章补上了另一层：不是只看一个高级 Skill 的内部流水线，而是从 Skill 库维护者角度说明什么值得成为 Skill、如何写、如何评审、如何维护。它的核心判断是：Skill 是模型与环境的上下文工程，不是传统软件，也不是人类 README。

几个原则很硬：

- **Skill 是目录，不是单文件。** `SKILL.md` 应该是 hub；确定性逻辑进 `scripts/`，重文档进 `references/`，模板和 schema 进 `assets/`，首次配置进 `config.json`。
- **description 是路由触发器，不是功能介绍。** 好 description 应描述“用户什么时候会需要它”，最好来自真实 query；坏 description 只解释这个 Skill 有什么用。
- **每个 Skill 都是税。** index 层的 `name: description` 每个 session 都付费；Skill body 加载后也会污染后续上下文。因此句子级检查是：没有这句话，agent 会不会做错？不会就删。
- **gotchas 是最高价值内容。** 模型已经知道的通用命令和常识不该写；真正值钱的是边界、反例、已知失败和容易误路由的相邻场景。
- **先 eval，后写 Skill。** 至少要覆盖真实用户 query、已知失败、相邻领域混淆；negative examples 往往比 positive examples 更能防止路由污染。
- **维护是 gotchas flywheel。** 失败就加 gotcha；误加载就收紧 description 并加 negative eval；该加载却没加载就补关键词和 positive eval。不要随手改 description，因为小词改动可能影响整个 Skill 库。

这让 Skill 工程从“写一个好提示词”变成“管理一个有路由成本、上下文成本和回归风险的能力索引”。新增一个 Skill 可能让其他 Skill 变差，这是典型的 action at a distance。


## ai-cli Skill 案例：合格但偏薄的 README 摘要型 Skill

`vercel-labs/ai-cli` 的 `skills/ai-cli/SKILL.md` 是一个有代表性的中间状态：它不是坏 Skill，因为它清楚说明了工具边界、核心命令和 piping 模式，也明确提醒 agent 生成图片或视频时应使用 `-o` 保存文件，避免在非 TTY 场景把原始二进制写进 stdout、污染上下文。这个提醒属于真正的 gotcha，比重复 README 命令更有价值。

但它还没有完全进入工程操作型 Skill。它缺少几类关键约束：

- **默认操作协议不足。** 对 agent 来说，图片和视频生成的默认模式应该是 `-o <path-or-dir> --json`，然后从 JSON 的 `file` 字段读取产物路径，而不是让 agent 自己猜输出位置。
- **成本和速率边界不足。** `-m` 多模型、`-n` 多结果和 video 生成都会快速放大成本与失败率，Skill 应提醒 agent 只有在用户明确要求比较或批量生成时才扩大 fan-out。
- **失败处理不足。** 一个工程化 Skill 应写明超时、exit code、部分成功、降并发、换模型、保留成功产物和局部重试策略。
- **结果选择不足。** 多模型比较不只是“能同时生成”，还要告诉 agent 如何组织输出目录、如何记录模型来源、如何让用户或视觉检查参与最终选择。
- **负例不足。** Skill 应说明何时不要用这个工具，例如需要交互式长任务、需要严格可复现、没有 API key、或用户没有授权产生高成本 video。

这个案例说明：一个 Skill 可以“可用”但还不“老练”。README 摘要型 Skill 让 agent 知道工具存在；工程操作型 Skill 则把工具调用变成低噪声、低成本、可恢复、可审计的执行协议。

## bento-slides 案例：强产物契约、无完整流水线仍值得学

`nyblnet/bento` 的 `bento-slides` 落在 hatch-pet 与 ai-cli 之间，偏 **文档/产物协议型 Skill**：

- **产物协议硬。** 只编辑 `.bento.html` 里 `#bento-doc` 的 JSON；runtime 壳不动；`<` 必须 `\u003c`；从零 curl 拉最新 shell，且下载块为空——这些都是模型不读 skill 就会搞砸的边界。
- **description 是场景路由。** 用户要 slide / presentation / 从无做 deck 时加载，而不是介绍 Bento 有多酷。
- **默认失败模式被显式否定。** 禁止默认 bullet 墙，要求把素材映射到 chart、table、morph、state slide、ken-burns 等；self-audit 清单逼 agent 自检。
- **gotcha 密度高。** bar/line 必须 plain numbers、morph 靠稳定 id、大视频勿 embed、勿改 `docId` 等，属于领域 know-how 而非 README 复述。
- **未到 hatch-pet 流水线。** 无 job manifest、无确定性编译脚本、无 provenance/repair；验收依赖「打开看每一页」和 runtime `validate()`，skill 未强制脚本化。负例与 evals 仍弱。

它说明：即使没有完整 control plane，**先把可消费产物契约和反默认失败写死**，Skill 已经从 prompt 包装升到可收录的工程组件。收录索引见 [[Awesome Agent Skills]]；产品与 `window.bento` / 风格模型见 [[Bento]]；评审事实见 `raw/sources/2026-08-06-bento-slides-skill-review.md`。

## mono-color 案例：视觉系统约束型 Skill

`yanliudesign/mono-color-skill` 补上第三类：难点不是工具协议或产物格式，而是大量主观审美判断的生成型 Skill。它的工程化手法：

- **catalog wins**：`design-system/` 六个 JSON catalog（colors/compositions/typography/rhythm/carriers/imperfections）是取值域的 source of truth；散文只解释意图，"when an exact value differs, the catalog wins"——约束来源有了明确的优先级规则。
- **主观判据可枚举化**：原创性防火墙把「不抄参考」翻译成 10 个结构变量至少改 4 个的替换规则；Final Quality Gate 是约 20 项 yes/no 检查（焦点事件唯一、主体占画 45%-80%、字号 5x-12x 跳变等）；重生成判据同样可枚举（出现第三墨、留白出界、无 5x 跳变）。
- **反默认失败的负例清单**：Hard Avoids 列的不是常识性禁令，而是模型会稳定滑入的审美默认：自动做旧（网点 + 限墨 ≠ 复古）、stock-photo 姿势、浪漫道具堆（串灯/酒杯/星空）、安全的首左图右分割。
- **确定性默认**：同输入必须解析出同一 Recipe Manifest；通用色词有固定别名（blue→Cobalt）；瑕疵种子用稳定 hash 跨重试保持。
- **诚实降级**：精确文字渲染失败时，重试一次后改为 text-light 底图并声明排版应在布局工具叠加——"Do not pretend distorted text is correct"。
- **evals 带机器可查断言**：16 条 eval 的 assertions 含 `ratio`/`mode`/`ink_hexes`/`plate_roles`，与设计系统 catalog 一致性校验一起进 CI——取值域本身有回归保护，是现有案例中评测侧最完整的。
- **未到 hatch-pet 流水线**：无 job manifest、无运行时确定性编译、无局部 repair；单次生成任务属性使然，降级路径存在。

它说明：当 Skill 的难点是品味而非协议时，工程化抓手仍是同一套——把主观判断翻译成取值域、变量规则和逐项验收清单，审美领域同样适用「模型生成候选、判据拥有提交权」。视觉系统本体（色板 hex、布局族）是 skill 自己的 payload，不镜像进 wiki。收录索引见 [[Awesome Agent Skills]]；评审事实见 `raw/sources/2026-09-01-mono-color-skill-review.md`。

## 和 workflow 的关系

传统 workflow 擅长确定性链路，适合触发器、节点、固定分支和清晰输入输出。但当任务需要上下文理解、动态决策、候选筛选、多代理协作和局部修复时，画死节点图会越来越重。

Skill 更适合承载“半结构化生产流程”：协议和边界是硬的，执行路径可以由 Agent 根据状态选择。也就是说，成熟 Skill 不是 workflow 的反面，而是把 workflow 的确定性部分收进脚本和 manifest，把不确定的语义判断留给模型。

## 对 AgentOS / control plane 的启发

这篇文章最值得保留的判断是：Agent 系统的稳定性不靠更多 prompt，而靠协议、manifest、provenance、编译器、QA 和 repair。

可以把成熟 Skill 抽象成一条生产链：

```text
intent
-> request
-> job manifest
-> generated candidates
-> recorded provenance
-> compiled artifact
-> QA result
-> targeted repair
-> packaged asset
```

这条链路把模型关进工程边界里。创意层可以开放，协议层必须收紧；worker 可以并行，提交权必须集中；结构可以自动验，语义要单独看；失败可以重试，但更应该能定位和修复。

## 未决问题

- `hatch-pet` 依赖图像生成质量，Skill 只能降低漂移，不能彻底消除视觉不一致。
- 这种范式会增加脚本、manifest 和 QA 成本，不适合一次性小任务。
- 子代理并行会增加 token 和额度消耗，只有任务天然可并行且产物需要严格验收时才划算。
- `/goal` 这类目标驱动机制如果和 manifest / QA 结合，可能成为长任务持续推进的控制环，但仍需要明确完成证据和停止条件。
- Skill description 的路由质量需要持续 eval；一旦 Skill 库变大，新增或修改 description 可能通过隐式匹配影响其他 Skill。
- 自生成 Skill 不可靠。LLM 可以辅助整理材料，但真正的 Skill 需要人注入领域判断、gotchas、负例和维护经验。

## 相关页面

- [[Awesome Agent Skills]] — 过线条目的薄索引（Awesome）
- [[Bento]]
- [[ai-cli]]
- [[Code Agent]]

## 来源指针

- `raw/sources/2026-05-06-codex-pet-skill-article.md`
- https://mp.weixin.qq.com/s/uH71k1yAoF6xjsOYmVAJBg
- `raw/sources/2026-05-06-perplexity-agent-skills.md`
- https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity
- `raw/sources/2026-05-12-ai-cli-skill-review.md`
- https://github.com/vercel-labs/ai-cli/blob/main/skills/ai-cli/SKILL.md
- `raw/sources/2026-08-06-bento-slides-skill-review.md`
- https://github.com/nyblnet/bento/blob/main/plugins/bento-slides/skills/bento-slides/SKILL.md
- `raw/sources/2026-09-01-mono-color-skill-review.md`
- https://github.com/yanliudesign/mono-color-skill
- https://bento.page/agents.md
