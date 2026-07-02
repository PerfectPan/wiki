# 2026-07-02 Vercel Labs konsistent 结构约定调研

## 来源

- GitHub: https://github.com/vercel-labs/konsistent
- Vercel changelog: https://vercel.com/changelog/enforce-consistent-code-for-agents-and-humans-with-konsistent
- npm package: https://www.npmjs.com/package/konsistent
- 相关安全 issue: https://github.com/vercel/ai/issues/15868

## 来源事实

- Vercel 在 2026-07-01 的 changelog 中宣布 `konsistent` 开源。
- `konsistent` 是面向 TypeScript codebase 的 CLI linter，用 `konsistent.json` 声明项目结构约定。
- 它补的是 ESLint、Biome、oxlint 不覆盖的项目级结构约束，例如：
  - 匹配某个路径模式的文件必须导出某些函数或类型；
  - 某类目录必须包含固定文件；
  - 某类 class 必须继承或实现指定类型；
  - barrel file 必须从指定子模块 re-export。
- README 示例显示它可通过 `npm install konsistent --save-dev`、`pnpm add konsistent --save-dev` 或 `bun add konsistent --dev` 安装，并通过 `konsistent` / `konsistent check` 执行。
- npm 当前 `konsistent` 最新版本为 `1.0.0-beta.1`，发布时间为 2026-06-30，包声明 `publishConfig.provenance = true`，npm metadata 中也包含 provenance attestation。
- 核心实现使用 TypeScript compiler API 解析 AST，而不是正则扫文本；predicate 覆盖文件系统、声明、导出、导入、class/interface 继承、函数签名、barrel file、声明顺序等结构。
- 配置支持路径 placeholder、case transformation、静态 placeholder、条件规则、`must` / `mustNot`、warning/error severity、JSON/GitHub/Markdown 输出格式。
- `conventionSources` 支持复用约定：本地 JSON 或 npm 包。npm convention source 通过 package `exports["./konsistent"]` 且 `conditions: ["konsistent"]` 解析，并检查解析路径不能逃出 package 目录。
- Vercel changelog 称 `konsistent` 已用于 AI SDK 和 Chat SDK，以约束结构化代码约定。
- 相关安全 issue 显示，早期 Vercel AI SDK 文档曾提到安装 `konsistent-provider`；该 npm 包并非 Vercel 维护，`install` script 包含从外部 URL 安装 tarball 的命令，属于明显的供应链风险。这个包不应安装。

## 初步判断

- `konsistent` 的长期价值不是“多一个 linter”，而是把项目惯例变成 agent 和 CI 都能执行的结构契约。
- 对 coding agent 来说，它能降低“看了几个样例后凭感觉模仿”的不确定性，尤其适合 monorepo、provider/adapter/plugin/harness 这类并行结构。
- 它不替代 TypeScript、测试、ESLint 或架构设计；更像是把“每个 provider 都应该长成一样”这种 review 经验前移到机器检查。
- 最适合先用于已经有 3 个以上重复结构的地方，而不是拿它发明新架构。
- 使用时必须注意 npm source 边界：只安装 `konsistent` 本包和可信 convention package，不安装 `konsistent-provider`。
