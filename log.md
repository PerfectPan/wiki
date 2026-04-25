# 变更记录

这个文件是追加式记录，用来登记有意义的知识库变更。

## 记录模板

```md
## 2026-04-12

- 摘要：
- 页面：
  - [[页面名]]
- 来源：
  - raw/sources/example.md
- 备注：
```

## 2026-04-19

- 摘要：精修 `product` 簇，移除一批过薄或草稿态 topic，新增 `Obsidian vs Logseq` 对比页，并将 `Color and Perception` 调整到 `frontend`。
- 页面：
  - [[wiki/comparisons/product/Obsidian vs Logseq|Obsidian vs Logseq]]
  - [[wiki/topics/product/Logseq|Logseq]]
  - [[wiki/topics/frontend/Color and Perception|Color and Perception]]
  - [[index]]
- 来源：
  - [[deep-research-report]]
  - `raw/sources/Logseq.md`
  - `raw/sources/Color and Perception.md`
  - `raw/sources/BlockSuite.md`
  - `raw/sources/Cross Platform.md`
  - `raw/sources/Design.md`
  - `raw/sources/GreatMinds.md`
  - `raw/sources/Prototype.md`
  - `raw/sources/RSS.md`
  - `raw/sources/UX.md`
  - `raw/sources/未来工作方向.md`
- 备注：本轮遵循轻改原则，保留 raw 原件不动；`journals/` 仍未在当前仓库中整体迁入。

## 2026-04-19

- 摘要：并行精修其余分类，删除一批空壳、链接堆和明显时效性 topic，并将 `富文本编辑器` 从 `systems` 调整到 `tooling`。
- 页面：
  - [[index]]
  - [[log]]
  - `wiki/topics/frontend/*`
  - `wiki/topics/tooling/*`
  - `wiki/topics/systems/*`
  - `wiki/topics/architecture/*`
  - `wiki/topics/ai/*`
  - `wiki/topics/languages/*`
  - `wiki/topics/algorithms/*`
  - `wiki/topics/career/*`
  - `wiki/topics/life/*`
- 来源：
  - `wiki/topics/*`
  - `raw/sources/*`
- 备注：本轮以轻改和高置信度降级为主；`raw/` 保持 append-only，不清理其中对已降级 topic 的历史链接。

## 2026-04-19

- 摘要：补充第一批真正的 synthesis / comparison 页面，把 agent 工作流、RSC 心智模型、状态管理选型维度与渲染策略对比沉淀进 `wiki/`。
- 页面：
  - [[wiki/syntheses/ai/Agent 驱动 Wiki 的维护流程|Agent 驱动 Wiki 的维护流程]]
  - [[wiki/syntheses/frontend/RSC 的协议与渲染心智模型|RSC 的协议与渲染心智模型]]
  - [[wiki/syntheses/frontend/状态管理的技术选型维度|状态管理的技术选型维度]]
  - [[wiki/comparisons/frontend/SSR vs SSG vs RSC|SSR vs SSG vs RSC]]
  - [[index]]
- 来源：
  - `AGENTS.md`
  - `SCHEMA.md`
  - `deep-research-report.md`
  - `wiki/topics/ai/*`
  - `wiki/topics/frontend/*`
  - `raw/sources/2023.04.24-2023.05.07.md`
  - `raw/sources/RSC.md`
  - `raw/sources/SSR.md`
  - `raw/sources/SSG.md`
  - `raw/sources/State Management.md`
  - `raw/sources/React.md`
  - `raw/sources/Waku.md`
- 备注：这批页面以现有仓库材料为主，没有回写 `raw/`；dated raw 残留只在确有长期价值时作为来源指针被抽取。

## 2026-04-20

- 摘要：补做一条 `journals` 抽取，把 dated raw 残留里关于 FLIP 布局动画的长期结论沉淀为 frontend synthesis。
- 页面：
  - [[wiki/syntheses/frontend/FLIP 布局动画的心智模型|FLIP 布局动画的心智模型]]
  - [[index]]
- 来源：
  - `raw/sources/2023.05.08-2023.05.21.md`
  - `raw/sources/Front End.md`
- 备注：没有迁入日记原文，只抽取 pages 未覆盖、且具有长期复用价值的技术结论。

## 2026-04-22

- 摘要：补做一条 `journals` 抽取，把旧 Logseq `journals/2024_05_29.md` 里关于依赖解析与 SAT 规约的长期结论沉淀为 tooling topic。
- 页面：
  - [[wiki/topics/tooling/Dependency Resolution|Dependency Resolution]]
  - [[wiki/topics/algorithms/Algorithm|Algorithm]]
  - [[index]]
- 来源：
  - `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2024_05_29.md`
  - `https://borretti.me/article/dependency-resolution-made-simple`
  - `https://github.com/dart-lang/pub/blob/master/doc/solver.md`
- 备注：这条内容不在旧 `pages/Algorithm.md` 里，而是在 `journals/` 中；因此属于后补的 journal 抽取，不是 `pages` 漏迁修复。

## 2026-04-25

- 摘要：继续从旧 Logseq `journals/` 抽取带总结的长期内容，补充依赖管理与 npm 包发布两篇 tooling synthesis。
- 页面：
  - [[wiki/syntheses/tooling/npm 包发布与发布链路实践|npm 包发布与发布链路实践]]
  - [[wiki/syntheses/tooling/前端依赖管理策略|前端依赖管理策略]]
  - [[index]]
- 来源：
  - `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2024_05_02.md`
  - `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2024_09_08.md`
  - `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2025_05_02.md`
  - [[wiki/topics/tooling/Dependency Resolution|Dependency Resolution]]
- 备注：这批不是把 journal 整页迁入，而是只抽“链接 + 已成形总结”的条目，继续遵守 `journals` 非整体迁移规则。

## 2026-04-25

- 摘要：继续从旧 Logseq `journals/` 抽取 frontend 与 ai 的高价值总结，补充 React 18 streaming / hydration、Next.js middleware 鉴权绕过与 MCP SSE 多实例路由策略。
- 页面：
  - [[wiki/syntheses/frontend/React 18 流式 SSR 与渐进式 hydration|React 18 流式 SSR 与渐进式 hydration]]
  - [[wiki/topics/frontend/Next.js Middleware Auth Bypass|Next.js Middleware Auth Bypass]]
  - [[wiki/syntheses/ai/MCP SSE 多实例路由策略|MCP SSE 多实例路由策略]]
  - [[index]]
- 来源：
  - `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2024_05_02.md`
  - `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2025_03_24.md`
  - `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2025_04_22.md`
  - `wiki/topics/frontend/SSR.md`
  - `wiki/topics/frontend/RSC.md`
  - `wiki/topics/ai/MCP.md`
- 备注：这批继续遵循“只抽有结论的 journal 条目，不迁整页日记”的规则。

## 2026-04-25

- 摘要：继续从旧 Logseq `journals/` 抽取剩余的高价值实现与工程策略，补充 `mcp-remote`、`npm Trusted Publishers` 与应用层通信可靠性边界。
- 页面：
  - [[wiki/topics/ai/mcp-remote|mcp-remote]]
  - [[wiki/topics/tooling/npm Trusted Publishers|npm Trusted Publishers]]
  - [[wiki/syntheses/frontend/应用层通信的可靠性边界|应用层通信的可靠性边界]]
  - [[index]]
- 来源：
  - `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2025_03_30.md`
  - `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2025_05_03.md`
  - `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2025_09_07.md`
- 备注：这批依旧遵循 “链接 + 已成形总结” 才抽取的原则；像只有单条链接、无明确结论的 journal 记录暂时保留在原处。

## 2026-04-25

- 摘要：继续从旧 Logseq `journals/` 抽取 frontend 的高价值结论，补充 ES Module / Import Maps、shadcn registry 分发模式与 JSBridge 鉴权漏洞。
- 页面：
  - [[wiki/syntheses/frontend/ES Module 加载与 Import Maps|ES Module 加载与 Import Maps]]
  - [[wiki/syntheses/frontend/shadcn Registry 组件分发模式|shadcn Registry 组件分发模式]]
  - [[wiki/topics/frontend/JSBridge 鉴权漏洞|JSBridge 鉴权漏洞]]
  - [[index]]
- 来源：
  - `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2023_05_06.md`
  - `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2023_08_08.md`
  - `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2025_01_31.md`
  - `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2025_04_20.md`
  - `http://myjsapi.alipay.com/jsapi/native/trade-pay.html`
- 备注：这批仍然属于 “有链接且已有明确总结” 的 journal 抽取；不会把只含单条收藏的日记记录硬迁进 wiki。

## 2026-04-25

- 摘要：继续补做剩余的高置信度通用结论，新增事件循环、Fetch streaming、GET body 语义与 Electron Deep Link，并把 `.d.ts` 规则补进 `TypeScript` 页面。
- 页面：
  - [[wiki/syntheses/frontend/事件循环与 Microtask 检查点|事件循环与 Microtask 检查点]]
  - [[wiki/syntheses/frontend/浏览器 Fetch Streaming 的读取边界|浏览器 Fetch Streaming 的读取边界]]
  - [[wiki/topics/systems/GET 请求的 body 语义|GET 请求的 body 语义]]
  - [[wiki/topics/systems/Electron Deep Link|Electron Deep Link]]
  - [[wiki/topics/languages/TypeScript|TypeScript]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2023_01_31.md`
  - `legacy-logseq-journals/2023_04_03.md`
  - `legacy-logseq-journals/2023_07_15.md`
  - `legacy-logseq-journals/2023_08_06.md`
  - `legacy-logseq-journals/2023_11_23.md`
- 备注：这批继续只抽“已经形成可复用结论”的通用技术条目，不把题解、单链收藏或 TODO 强行提升为 wiki 页面。

- 摘要：继续补做剩余的系统与前端通用结论，补充 SSL/TLS、Electron 更新排障、强制 reflow 与 React Context 颗粒度问题。
- 页面：
  - [[wiki/topics/systems/SSL 与 TLS 握手|SSL 与 TLS 握手]]
  - [[wiki/topics/systems/Electron Auto Update 排障|Electron Auto Update 排障]]
  - [[wiki/syntheses/frontend/强制 reflow 的工程边界|强制 reflow 的工程边界]]
  - [[wiki/syntheses/frontend/React Context 颗粒度与 Selector 路径|React Context 颗粒度与 Selector 路径]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2022_10_30.md`
  - `legacy-logseq-journals/2023_06_21.md`
  - `legacy-logseq-journals/2024_01_21.md`
  - `legacy-logseq-journals/2024_03_06.md`
- 备注：这批继续只提升已有明确判断的通用结论；剩余的大头仍是题解、单链收藏或产品观察，我会继续筛，但不会硬迁。 

- 摘要：继续补做前端渲染与校验相关条目，补充 React 重渲染优化、Zod vs Valibot 与模板克隆渲染路径。
- 页面：
  - [[wiki/topics/frontend/React Render Optimization|React Render Optimization]]
  - [[wiki/comparisons/frontend/Zod vs Valibot|Zod vs Valibot]]
  - [[wiki/syntheses/frontend/模板克隆与 DOM 渲染路径|模板克隆与 DOM 渲染路径]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2023_12_16.md`
  - `legacy-logseq-journals/2024_01_16.md`
  - `legacy-logseq-journals/2024_01_21.md`
  - `legacy-logseq-journals/2024_12_14.md`
  - `raw/sources/React.md`
- 备注：这批继续只抽可以独立复用的结论，不把零散链接和单篇题解强行提升到 wiki 层。

- 摘要：继续补做系统性更强的产品、AI 与协作基础设施内容，补充 Logseq 架构演进、RAG 问答管线与 CRDT 数据压缩策略。
- 页面：
  - [[wiki/syntheses/product/Logseq 架构演进脉络|Logseq 架构演进脉络]]
  - [[wiki/syntheses/ai/RAG 问答管线|RAG 问答管线]]
  - [[wiki/syntheses/systems/CRDT 数据压缩策略|CRDT 数据压缩策略]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2022_11_19.md`
  - `legacy-logseq-journals/2023_04_03.md`
  - `legacy-logseq-journals/2023_05_06.md`
  - `legacy-logseq-journals/2023_05_13.md`
  - `legacy-logseq-journals/2023_11_18.md`
  - `wiki/topics/product/Logseq.md`
- 备注：这批继续优先提升能独立成页的系统性结论，而不是把相关链接简单堆回 topic。

- 摘要：继续补做剩余的系统调试与前端长期心智条目，补充前端框架演化、Provisional headers 调试路径与 JavaScript 优化启发。
- 页面：
  - [[wiki/syntheses/frontend/前端框架的四个时代|前端框架的四个时代]]
  - [[wiki/topics/systems/Provisional headers 调试路径|Provisional headers 调试路径]]
  - [[wiki/syntheses/frontend/JavaScript 优化启发|JavaScript 优化启发]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2022_10_05.md`
  - `legacy-logseq-journals/2023_06_25.md`
  - `legacy-logseq-journals/2024_03_29.md`
- 备注：这批继续只补能够独立复用的长期结论；更偏具体题解、单产品观察或零散收藏的 journal 条目仍保留在 raw 层。

- 摘要：继续补做 TypeScript 和 SSR 相关长期条目，补充类型收窄 / IIMT、reflect-metadata 与服务端客户端视图一致性。
- 页面：
  - [[wiki/syntheses/languages/TypeScript 类型收窄与 IIMT|TypeScript 类型收窄与 IIMT]]
  - [[wiki/topics/languages/reflect-metadata|reflect-metadata]]
  - [[wiki/syntheses/frontend/服务端与客户端视图一致性|服务端与客户端视图一致性]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2023_07_15.md`
  - `legacy-logseq-journals/2023_07_29.md`
  - `legacy-logseq-journals/2024_01_01.md`
  - `wiki/topics/architecture/@opensumi%2Fdi.md`
  - `wiki/topics/frontend/SSR.md`
  - `wiki/topics/frontend/useEffect.md`
- 备注：这批继续优先提升能独立复用的概念与约束；不会把单篇收藏和细碎观察硬转成 wiki 页面。

- 摘要：继续补做系统与运行时实践条目，补充小程序运行时架构、Windows 文件锁重试、Node ESM 下的 `__dirname` 与 flex 自动最小尺寸陷阱。
- 页面：
  - [[wiki/syntheses/frontend/小程序运行时架构思路|小程序运行时架构思路]]
  - [[wiki/topics/systems/Windows 文件锁与 fs.rename 重试|Windows 文件锁与 fs.rename 重试]]
  - [[wiki/topics/systems/Node|Node]]
  - [[wiki/topics/frontend/CSS|CSS]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2022_08_05.md`
  - `legacy-logseq-journals/2022_10_31.md`
  - `legacy-logseq-journals/2022_11_25.md`
  - `legacy-logseq-journals/2024_08_26.md`
- 备注：这批仍然以“已有明确总结的工程经验”为准，不把零散收藏和未成形观察硬拉进 wiki。

- 摘要：继续从旧 Logseq `journals/` 并行抽取多簇高价值条目，补充 ai / frontend / career / systems / tooling 的第二批页面与对比页。
- 页面：
  - [[wiki/topics/ai/Agent Client Protocol|Agent Client Protocol]]
  - [[wiki/topics/ai/MCP Client|MCP Client]]
  - [[wiki/comparisons/ai/Workflow vs Agent|Workflow vs Agent]]
  - [[wiki/syntheses/career/招聘中的搜索问题与用人标准|招聘中的搜索问题与用人标准]]
  - [[wiki/syntheses/career/结构化面试与行为追问|结构化面试与行为追问]]
  - [[wiki/comparisons/career/简历排版引擎选择|简历排版引擎选择]]
  - [[wiki/syntheses/frontend/RSC 与 CSS-in-JS 的兼容性约束|RSC 与 CSS-in-JS 的兼容性约束]]
  - [[wiki/syntheses/frontend/Web Components 的服务端渲染路径|Web Components 的服务端渲染路径]]
  - [[wiki/syntheses/frontend/html2canvas 的渲染局限与打印替代方案|html2canvas 的渲染局限与打印替代方案]]
  - [[wiki/comparisons/systems/线程级隔离 vs 进程级隔离|线程级隔离 vs 进程级隔离]]
  - [[wiki/comparisons/tooling/文档排版引擎选型：HTML & CSS vs LaTeX vs Typst vs React-pdf|文档排版引擎选型：HTML & CSS vs LaTeX vs Typst vs React-pdf]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2023_01_31.md`
  - `legacy-logseq-journals/2023_03_15.md`
  - `legacy-logseq-journals/2024_03_06.md`
  - `legacy-logseq-journals/2024_10_25.md`
  - `legacy-logseq-journals/2024_12_14.md`
  - `legacy-logseq-journals/2024_12_24.md`
  - `legacy-logseq-journals/2025_01_23.md`
  - `legacy-logseq-journals/2025_03_01.md`
  - `legacy-logseq-journals/2025_03_29.md`
  - `legacy-logseq-journals/2025_03_31.md`
  - `legacy-logseq-journals/2025_04_01.md`
  - `legacy-logseq-journals/2025_04_18.md`
  - `legacy-logseq-journals/2025_09_14.md`
- 备注：这批是并行抽取后的主线程集成结果；只提升带明确总结的条目，其余 journal 原文保留在 `legacy-logseq-journals/` 里继续待筛。

- 摘要：为避免 `journals` 中仍有高价值内容遗漏，补充归档旧 Logseq `journals/` 的全部原始副本到 `legacy-logseq-journals/`，并与前面的高价值抽取并行保留。
- 页面：
  - `legacy-logseq-journals/*`
  - [[index]]
- 来源：
  - `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/*`
- 备注：这一步是原始资料归档，不等于把所有 journal 直接提升为 wiki 页面；后续仍按“有明确总结的条目优先抽取”为原则继续沉淀到 `wiki/`。

- 摘要：继续补做剩余的高置信度通用结论，新增事件循环、Fetch streaming、GET body 语义与 Electron Deep Link，并把 `.d.ts` 规则补进 `TypeScript` 页面。
- 页面：
  - [[wiki/syntheses/frontend/事件循环与 Microtask 检查点|事件循环与 Microtask 检查点]]
  - [[wiki/syntheses/frontend/浏览器 Fetch Streaming 的读取边界|浏览器 Fetch Streaming 的读取边界]]
  - [[wiki/topics/systems/GET 请求的 body 语义|GET 请求的 body 语义]]
  - [[wiki/topics/systems/Electron Deep Link|Electron Deep Link]]
  - [[wiki/topics/languages/TypeScript|TypeScript]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2023_01_31.md`
  - `legacy-logseq-journals/2023_04_03.md`
  - `legacy-logseq-journals/2023_07_15.md`
  - `legacy-logseq-journals/2023_08_06.md`
  - `legacy-logseq-journals/2023_11_23.md`
- 备注：这批继续只抽“已经形成可复用结论”的通用技术条目，不把题解、单链收藏或 TODO 强行提升为 wiki 页面。

- 摘要：为避免 `journals` 中仍有高价值内容遗漏，补充归档旧 Logseq `journals/` 的全部原始副本到 `legacy-logseq-journals/`，并与前面的高价值抽取并行保留。
- 页面：
  - `legacy-logseq-journals/*`
  - [[index]]
- 来源：
  - `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/*`
- 备注：这一步是原始资料归档，不等于把所有 journal 直接提升为 wiki 页面；后续仍按“有明确总结的条目优先抽取”为原则继续沉淀到 `wiki/`。

## 2026-04-12

- 摘要：初始化适用于 Obsidian + agent + PR 审阅工作流的治理与 schema 文件。
- 页面：
  - [[AGENTS]]
  - [[SCHEMA]]
  - [[index]]
- 来源：
  - [[deep-research-report]]
- 备注：从操作模型中移除了 `drafts/` 和 `inbox/`，后续统一通过 branch 和 PR 审阅。

## 2026-04-12

- 摘要：移除了项目内 skill，把工作流入口统一收敛到 `bin/wiki` 和 `AGENTS.md`。
- 页面：
  - [[AGENTS]]
  - [[log]]
- 来源：
  - [[AGENTS]]
- 备注：仓库不再依赖 `.codex/skills/`，后续 agent 统一通过 CLI 入口工作。

## 2026-04-12

- 摘要：为迁移流程补充英文分类规则，并明确迁移默认遵循轻改原则。
- 页面：
  - [[AGENTS]]
  - [[SCHEMA]]
  - [[log]]
- 来源：
  - [[deep-research-report]]
- 备注：后续页面将按分类子目录落到 `topics`、`syntheses`、`comparisons` 中，内容优先保持原样。

## 2026-04-12

- 摘要：冻结当前一级分类，并补充 `tags` 的使用规则。
- 页面：
  - [[AGENTS]]
  - [[SCHEMA]]
  - [[log]]
- 来源：
  - [[AGENTS]]
  - [[SCHEMA]]
- 备注：后续迁移优先用 `tags` 表达细粒度主题，避免 taxonomy 膨胀。

## 2026-04-12

- 摘要：完成第一批迁移，优先落地成熟 topic 页面，并为迁移页面保留 raw 来源副本。
- 页面：
  - [[wiki/topics/architecture/Software Design|Software Design]]
  - [[wiki/topics/architecture/技术方案|技术方案]]
  - [[wiki/topics/ai/MCP|MCP]]
  - [[wiki/topics/product/Logseq|Logseq]]
  - [[raw/sources/RAG|RAG]]
- 来源：
  - `raw/sources/Software Design.md`
  - `raw/sources/技术方案.md`
  - `raw/sources/MCP.md`
  - `raw/sources/Logseq.md`
  - `raw/sources/RAG.md`
- 备注：这一批遵循轻改原则，正文尽量保持原样；`RAG` 暂时仍保留在 raw 层，后续再决定是否提升为 wiki 页面。

## 2026-04-12

- 摘要：补充迁移 `frontend` 第一组成熟页面，并将 `Ref`、`RSC` 相关图片一并纳入仓库。
- 页面：
  - [[wiki/topics/frontend/React|React]]
  - [[wiki/topics/frontend/RSC|RSC]]
  - [[wiki/topics/frontend/Ref|Ref]]
  - [[wiki/topics/frontend/useRef|useRef]]
  - [[wiki/topics/frontend/State Management|State Management]]
  - [[wiki/topics/frontend/zustand|zustand]]
  - [[wiki/topics/frontend/CSS|CSS]]
  - [[wiki/topics/frontend/SVG|SVG]]
  - [[wiki/topics/frontend/Component Library|Component Library]]
  - [[wiki/topics/frontend/Web Component|Web Component]]
  - [[wiki/topics/frontend/React Devtools|React Devtools]]
- 来源：
  - `raw/sources/React.md`
  - `raw/sources/RSC.md`
  - `raw/sources/Ref.md`
  - `raw/sources/useRef.md`
  - `raw/sources/State Management.md`
  - `raw/sources/zustand.md`
  - `raw/sources/CSS.md`
  - `raw/sources/SVG.md`
  - `raw/sources/Component Library.md`
  - `raw/sources/Web Component.md`
  - `raw/sources/React Devtools.md`
  - `raw/sources/React Render Optimization.md`
- 备注：正文保持轻改；`React Render Optimization` 当前仍为空页，只保留 raw 副本，未提升到 `wiki/`。

## 2026-04-12

- 摘要：继续迁移 `architecture` 与 `ai/product` 的成熟页面，补充设计、依赖注入、DDD、Agent、GPT、Code Agent 等主题。
- 页面：
  - [[wiki/topics/architecture/DDD|DDD]]
  - [[wiki/topics/architecture/Dependency Injection|Dependency Injection]]
  - [[wiki/topics/product/Design|Design]]
  - [[wiki/topics/ai/Agent|Agent]]
  - [[wiki/topics/ai/Code Agent|Code Agent]]
  - [[wiki/topics/ai/GPT|GPT]]
- 来源：
  - `raw/sources/DDD.md`
  - `raw/sources/Dependency Injection.md`
  - `raw/sources/Design.md`
  - `raw/sources/Agent.md`
  - `raw/sources/Code Agent.md`
  - `raw/sources/GPT.md`
- 备注：这批仍然遵循轻改原则，正文尽量保持原样，只补目录、frontmatter 和来源指针。

## 2026-04-12

- 摘要：完成旧 Logseq `pages/` 的全量迁移，所有页面都已进入 `wiki/topics/`，并保留 raw 来源副本。
- 页面：
  - `wiki/topics/*`
  - `raw/sources/*`
  - `raw/assets/*`
  - [[index]]
  - [[log]]
- 来源：
  - `raw/sources/`
  - `raw/assets/`
- 备注：本次全量迁移覆盖 `192/192` 个旧 `pages`；`journals/` 仍按既定规则未整体迁入。

## 2026-04-12

- 摘要：完成一轮整体分类纠偏，修正明显错分类页面，并将模板/周计划/链接堆等非稳定主题页降回 raw。
- 页面：
  - [[index]]
  - `wiki/topics/*`
  - `raw/sources/*`
- 来源：
  - `wiki/topics/*`
  - `raw/sources/*`
- 备注：本轮优先纠正高置信度错误，例如将算法页从 `ai/frontend` 挪回 `algorithms`，将工具页从 `languages` 挪回 `tooling`，并移除明显不应进入 `wiki/topics` 的时间范围页与模板页。

## 2026-04-12

- 摘要：对 `tooling` 再做一轮精修，把明显属于系统、语言、算法、前端、认证的页面挪出，并将过薄的占位页降回 raw。
- 页面：
  - [[index]]
  - `wiki/topics/tooling/*`
  - `wiki/topics/systems/*`
  - `wiki/topics/languages/*`
  - `wiki/topics/algorithms/*`
  - `wiki/topics/frontend/*`
  - `wiki/topics/architecture/*`
- 来源：
  - `wiki/topics/tooling/*`
- 备注：这一轮重点修正 `tooling` 的边界，让它更接近“工程工具与基础设施”而不是杂项兜底分类。

## 2026-04-12

- 摘要：更新 `tooling` 的定义，并将 `@opensumi%2Fdi` 调整到 `architecture`。
- 页面：
  - [[AGENTS]]
  - [[wiki/topics/architecture/@opensumi%2Fdi|@opensumi%2Fdi]]
  - [[index]]
- 来源：
  - `raw/sources/@opensumi%2Fdi.md`
- 备注：`tooling` 采用更宽泛的工具定义，但依赖注入容器实现细节仍归为 `architecture`。

## 2026-04-25

- 摘要：继续补做语言层面的剩余通用概念，补充 `Pkl`、`UTF-8 Overlong Encoding`，并把内置类型继承坑补进 `TypeScript`。
- 页面：
  - [[wiki/topics/languages/Pkl|Pkl]]
  - [[wiki/topics/languages/UTF-8 Overlong Encoding|UTF-8 Overlong Encoding]]
  - [[wiki/topics/languages/TypeScript|TypeScript]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2024_03_12.md`
  - `legacy-logseq-journals/2024_04_02.md`
- 备注：这批继续优先提升可长期复用的语言概念，不把只面向单一场景的零散观察硬转成独立页面。

- 摘要：继续补做产品与基础设施层面的剩余结论，补充短链服务价值、状态页定位与 Serverless 分层隔离。
- 页面：
  - [[wiki/topics/product/Status Page|Status Page]]
  - [[wiki/syntheses/product/短链服务的产品价值|短链服务的产品价值]]
  - [[wiki/syntheses/systems/Serverless 应用分层与隔离|Serverless 应用分层与隔离]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2023_05_16.md`
  - `legacy-logseq-journals/2024_03_25.md`
  - `legacy-logseq-journals/2024_04_28.md`
- 备注：这批继续只提升已经形成明确产品/系统判断的条目，不把泛产品收藏和杂项观察一股脑迁入 wiki。

- 摘要：继续补做剩余的语言与 React 机制条目，补充 `Civet` 与 `React Hooks API` 的最小实现心智。
- 页面：
  - [[wiki/topics/languages/Civet|Civet]]
  - [[wiki/syntheses/frontend/React Hooks API 模拟实现|React Hooks API 模拟实现]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2025_03_16.md`
  - `legacy-logseq-journals/2025_03_21.md`
- 备注：这批继续只吸收已经能独立说明概念的条目；停留在“只是想再看看”的收藏仍保留在 journal 原文里。

- 摘要：继续补做剩余的前端实现经验，补充小程序架构演进与 Ant Design 异步默认值渲染。
- 页面：
  - [[wiki/topics/frontend/小程序架构演进|小程序架构演进]]
  - [[wiki/topics/frontend/Ant Design 异步默认值渲染|Ant Design 异步默认值渲染]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2022_10_31.md`
  - `legacy-logseq-journals/2022_11_01.md`
- 备注：这批仍然只提升已有明确工程结论的实现经验，不把细碎 UI 收藏或未成形观察继续硬迁。

- 摘要：继续补做交互规范层的高价值条目，补充交互式 UI 的可访问性基线。
- 页面：
  - [[wiki/syntheses/frontend/交互式 UI 的可访问性基线|交互式 UI 的可访问性基线]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2025_10_08.md`
- 备注：这页提炼的是一组长期适用的交互约束，不是某个单一组件或单篇文章的摘要。

- 摘要：继续补做剩余的前端工具与隔离实现条目，补充 `CVA` 与 `whyframe`。
- 页面：
  - [[wiki/topics/frontend/CVA|CVA]]
  - [[wiki/topics/frontend/whyframe|whyframe]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2025_03_23.md`
  - `legacy-logseq-journals/2025_04_20.md`
- 备注：这批继续只提升已经有明确实现心智的工具页，不把单纯组件库收藏扩展成空洞 topic。

- 摘要：继续补做剩余的产品观察与语言细节修正，补充 `AI Cover`、`Teable`，并把 TypeScript 内置类型继承的边界补强。
- 页面：
  - [[wiki/topics/product/AI Cover|AI Cover]]
  - [[wiki/topics/product/Teable|Teable]]
  - [[wiki/topics/languages/TypeScript|TypeScript]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2024_02_09.md`
  - `legacy-logseq-journals/2024_03_13.md`
  - `legacy-logseq-journals/2024_04_02.md`
- 备注：这批开始把剩余的单条但仍有长期价值的产品观察纳入 wiki，同时继续把 journal 里的重复结论并回已有主题页。

- 摘要：继续补做剩余的隔离与容器基础设施条目，补充同源 iframe 沙箱设计与 OCI 标准。
- 页面：
  - [[wiki/syntheses/frontend/同源 iframe 沙箱设计|同源 iframe 沙箱设计]]
  - [[wiki/topics/systems/Open Container Initiative|Open Container Initiative]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2023_05_16.md`
- 备注：这批继续优先提升系统性抽象，不把具体业务实现细节整页搬进 wiki。

- 摘要：继续补做前端基础概念，补充 `Polyfill` 与 `shim` 的关系。
- 页面：
  - [[wiki/topics/frontend/Polyfill|Polyfill]]
  - [[index]]
- 来源：
  - `legacy-logseq-journals/2022_10_31.md`
- 备注：这条属于通用概念补齐，用来承接 journal 中已经出现、但此前未单独落页的术语。
