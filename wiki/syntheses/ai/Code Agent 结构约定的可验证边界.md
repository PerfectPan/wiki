---
title: Code Agent 结构约定的可验证边界
description: 以 Vercel Labs konsistent 为例，说明项目结构约定如何从文档经验变成 agent 和 CI 可执行的契约。
type: synthesis
category: ai
created: 2026-07-02
updated: 2026-07-02
timestamp: 2026-07-02
tags:
  - code-agent
  - linter
  - typescript
  - ci
source_refs:
  - raw/sources/2026-07-02-vercel-konsistent-structural-conventions.md
  - https://github.com/vercel-labs/konsistent
  - https://vercel.com/changelog/enforce-consistent-code-for-agents-and-humans-with-konsistent
  - https://github.com/vercel/ai/issues/15868
resource:
  - raw/sources/2026-07-02-vercel-konsistent-structural-conventions.md
  - https://github.com/vercel-labs/konsistent
  - https://vercel.com/changelog/enforce-consistent-code-for-agents-and-humans-with-konsistent
  - https://github.com/vercel/ai/issues/15868
---

# Code Agent 结构约定的可验证边界

## 问题

大仓里的 code agent 怎样稳定遵守那些 TypeScript、ESLint 和测试都不直接表达的项目级结构约定？

## 简答

结构约定不能只写在 README 或靠 review 口口相传。对 code agent 来说，真正稳的方式是把“这类目录必须有哪些文件”“这个 barrel 必须导出哪些符号”“这个 adapter 必须继承什么基类”这类项目惯例变成可执行检查。`konsistent` 的价值就在这里：它把结构约定变成 `konsistent.json` 里的规则，再用 TypeScript AST 和文件系统检查在 CI 中验证。

## 来源事实

- Vercel Labs 在 2026-07-01 宣布 `konsistent` 开源；它是面向 TypeScript codebase 的结构约定 linter。
- `konsistent` 通过项目根目录的 `konsistent.json` 声明规则，检查路径模式、文件存在、导出、导入、声明、函数签名、class/interface 继承、barrel file 等结构。
- 它不是替代 ESLint、Biome 或 oxlint，而是覆盖这些工具不直接建模的项目级结构约束。
- Vercel 称它已用于 AI SDK 和 Chat SDK。
- npm 上 `konsistent` 当前版本为 `1.0.0-beta.1`，但历史文档关联过的 `konsistent-provider` 包存在明显 install script 风险，不应安装。

## 综合结论

### 1. Agent 需要的不只是上下文，还需要可验证约束

code agent 常见失败不是完全不知道该做什么，而是从几个样例里推断出一个“差不多”的结构：少导出一个类型、文件名跟目录名不一致、provider 没继承统一接口、barrel file 只 re-export 了一半。这些问题人类 reviewer 能看出来，但 reviewer 不应该长期承担这种低级结构差异的筛查。

`konsistent` 把这类隐性约定降成显性规则。它让 agent 面对的不是“请遵守项目风格”，而是“你提交的结构必须通过这些 predicate”。这比 prompt 约束稳定，也比事后人工 review 便宜。

### 2. 它适合并行结构，不适合任意架构洁癖

最适合 `konsistent` 的场景，是 monorepo 里已经形成重复模式的区域：

- `packages/{provider}/src/index.ts` 必须导出 provider factory 和 settings type；
- `plugins/{name}` 必须包含 `index.ts`、`manifest.json`、`README.md`；
- `adapters/{name}/factory.ts` 必须导出 `create{Name}Adapter`，并返回 `{Name}Adapter`；
- harness、bridge、protocol、demo package 这类多目录协作结构必须保持同形。

不适合的场景是把它当成架构发明器。没有 3 个以上重复样本时，规则往往只是个人偏好。更稳的流程是先观察项目里已经稳定出现的结构，再把强模式写成规则。

### 3. 这是 agent-native 工程的“结构层测试”

传统测试验证行为，TypeScript 验证类型，ESLint 验证文件内代码风格。`konsistent` 验证的是另一层：仓库结构与模块接口是否保持可预测。

这和 [[Agent-native 生成型 CLI 的产物协议]]、[[Agent Native 系统接口设计]] 是同一类思路：不要指望模型记住所有隐性规则，而是给它一个低熵、可检查、可修复的操作面。结构 linter 不是让 agent 更聪明，而是让 agent 犯错后能被确定性系统尽早拦住。

### 4. 供应链边界必须收紧

`konsistent` 本包的 npm metadata 显示由 Vercel/GitHub Actions 发布，并带 provenance；但 `konsistent-provider` 是另一个包，维护者不同，且 install script 包含外部 tarball 下载命令。历史 issue 已指出这个问题。

因此实际使用时应明确两条线：

- 可以评估和安装 `konsistent` 本包；
- 不安装 `konsistent-provider`，也不盲目信任任何未审计的 reusable convention package。

## 使用建议

1. 先选最强的 1 到 3 个重复结构，不要一开始覆盖全仓。
2. 第一版规则可以设为 warning，让团队先看漂移分布。
3. 对 code agent 高频修改的区域优先上规则，例如 provider、adapter、plugin、harness。
4. 规则描述应写清楚“为什么这条结构重要”，否则后续维护者只会把它当成麻烦。
5. reusable convention package 只从可信组织安装，并审计 package `exports["./konsistent"]` 指向的 JSON。

## 未决问题

- `konsistent` 目前仍是 beta，规则表达力和错误修复体验还需要观察。
- 它能发现结构偏差，但不负责自动设计更好的结构；规则质量仍取决于人类先识别出真实模式。
- 如果规则过多，可能把合理演进压成机械一致性，需要用 warning、例外和分层 rollout 控制成本。

## 相关页面

- [[Code Agent]]
- [[Agent Native 系统接口设计]]
- [[Agent-native 生成型 CLI 的产物协议]]
- [[Linter]]

## 来源指针

- `raw/sources/2026-07-02-vercel-konsistent-structural-conventions.md`
- `https://github.com/vercel-labs/konsistent`
- `https://vercel.com/changelog/enforce-consistent-code-for-agents-and-humans-with-konsistent`
- `https://github.com/vercel/ai/issues/15868`
