# Rush vs pnpm workspace 调研素材（官方文档、release notes、issue 与本地实测）

- 访问日期：2026-10-19。
- 版本快照（`npm view <pkg> time --json --registry https://registry.npmjs.org/`）：`@microsoft/rush` 最新 5.181.0（2026-10-06）；`pnpm` 最新 12.14.0（2026-10-15），另有 11.28.6、10.34.7 两条维护线；`@changesets/cli` 最新 3.0.3（2026-09-14）；`turbo` 2.11.9（2026-10-16）。
- 源码快照：changesets 仓库 main `e2ee472`（2026-10-16）；changesets/action main（读 `src/readChangesetState.ts`、`src/run.ts`）。
- 范围：rushjs.io 与 pnpm.io 文档、pnpm GitHub release notes、pnpm/rfcs 仓库、rushstack 与 dependabot-core 的 issue、npm 下载量接口、State of JS 页面；公开仓库 `PerfectPan/agent-kit` 的配置与 Dependabot PR 记录；两次本地实测（见「验证记录」）。没有在真实仓库里试迁，没有在 GitHub Actions 上跑 changesets/action 配 pnpm 原生发版的组合。

本文件记录能直接引到的事实，判断写在 [[wiki/comparisons/tooling/rush-vs-pnpm-workspace]] 和 [[wiki/topics/tooling/pnpm-versioning]]。

## Rush 的发布节奏与活跃度

- 每年发布的版本数（含少量预发布，排除 `created`/`modified` 键）：2023 年 68、2024 年 124、2025 年 29、2026 年截至 10-06 共 28。
- 2026-02 到 10 月从 5.167.0 发到 5.181.0；2026-07-01 以来 microsoft/rushstack 合并 154 个 PR，仓库共有 944 个 open issue（2026-10-19 查询）。
- Publishing 2.0 设计 [rushstack#3934](https://github.com/microsoft/rushstack/issues/3934)：创建于 2023-01-28，仍 open，最后一条评论 2023-08-10（有人问进展），2023-08-15 被加入 project 后无更新。
- Rush daemon：[RFC #5863](https://github.com/microsoft/rushstack/issues/5863)（2026-07-13，open）提出常驻进程 `rushd`，原文 "The default flip ships as Rush 6"。`apps/rush/CHANGELOG.md` 的 5.180.0、5.181.0 条目已在 rush-lib 里加入 daemon 支持和默认关闭的 `daemon.*` 实验配置。
- 跟进 pnpm 大版本：pnpm 10（2025-01-07 发布）在 Rush 侧 2025-06-02 合并支持；pnpm 11（2026-04-28）在 2026-06 至 07 合并支持，[#6103](https://github.com/microsoft/rushstack/issues/6103) "unblock pnpm 11 support" 仍 open；pnpm 12（2026-08-26）的 [#6131](https://github.com/microsoft/rushstack/pull/6131) "Close native pnpm compatibility gaps" 于 2026-10-14 合并，晚于 5.181.0，尚未进入正式版。`rush init` 模板默认的 `pnpmVersion` 仍是 9.15.9。

## Rush 官方定位

- 首页：<https://rushjs.io/>，"a scalable monorepo manager for the web"；卖点包括 "parallel builds, subset builds, incremental builds, and distributed builds"、"Repo policies allow new package dependencies to be reviewed"。
- Welcome 页：<https://rushjs.io/pages/intro/welcome/>，"We build hundreds of production NPM packages every day"。
- 维护者在 [rushstack#4011](https://github.com/microsoft/rushstack/issues/4011)（"What are the advantages of rushjs over pnpm workspace?"）的回复：
  - elliot-nelson，2023-04-02：「if you've got a small, single-focus repo, with a dozen or less packages, PNPM Workspaces is probably a better way」；「Rush's philosophy is very focused around large, corporate monorepos, where hundreds of developers are working on 200, 300, 400+ projects」；「for many, "pnpm workspaces + changesets" is a very reasonable alternative to Rush's publishing solution」。
  - octogonz，2023-04-06：「I think it's more about the number of people」；「Rush Stacks's main focus is multi-team monorepos」。
- `useWorkspaces` 的说明（<https://rushjs.io/pages/configs/pnpm-config_json/>）：开启后 Rush 使用 pnpm workspaces，在 `common/temp/` 生成 `pnpm-workspace.yaml` 和 `.pnpmfile.cjs`，用来实现 preferred versions 等功能。
- rushjs.io 的配置页落后于代码：pnpm-config 页缺 catalog、minimumReleaseAge、trustPolicy、allowBuilds 等字段，这些以 rush-lib 的 schema 和 CHANGELOG 为准。

## Rush 能力在 pnpm 侧的对应

| 能力 | Rush | pnpm 侧（版本取自 pnpm release notes） |
| --- | --- | --- |
| 固定工具版本 | `install-run-rush.js` + `rush.json` 的 `rushVersion`/`pnpmVersion` | `packageManager` 字段自动切换版本（9.7 引入），11 起可用 `devEngines.packageManager` + `pmOnFail` |
| 安装与 lockfile 校验 | `rush install` / `rush update` | `pnpm install --frozen-lockfile`（CI 默认）、`pnpm ci`（11.0） |
| 全局依赖设置 | `pnpm-config.json` 的 `globalOverrides` 等 | 直接写 `pnpm-workspace.yaml`：overrides、peerDependencyRules、allowBuilds（10.26）、minimumReleaseAge（10.16，11 起默认 1440 分钟） |
| 版本一致性 | `ensureConsistentVersions` + `rush check`（5.129 起移到 `common-versions.json`） | catalog（9.5）+ `catalogMode: strict`（10.12）只拦 `pnpm add`，全量检查要 syncpack `lint`（15.0 起支持 catalog） |
| 按依赖顺序跑脚本 | `command-line.json` bulk 命令 | `pnpm -r run` 拓扑顺序；11.25 / 12.1 起 `tasks.dependsOn` 按任务调度 |
| 增量构建与缓存 | `rush build`、`build-cache.json` + Azure/S3/HTTP 插件 | `pnpm pipeline`（12.4.0，2026-09-08，实验）本地缓存；`remoteCache`（12.12.0，2026-10-10）兼容 Turborepo Remote Cache API |
| cobuild | `cobuild.json` + Redis 锁，需云端构建缓存，仍为实验 | pnpm 和 Turborepo 都没有；Nx Agents（Nx Cloud）有分布式执行 |
| 项目选择 | `--to`、`--only`、`--impacted-by`、`--from`，`tag:`、`version-policy:` 选择器 | `--filter X...`、`X`、`...X`、`...[origin/main]`；`--from` 没有单一写法，`tag:`、`version-policy:` 没有对应 |
| subspaces | `subspaces.json`，一个仓库多份 lockfile（5.122 起） | 没有，一个 workspace 一份 lockfile |
| 依赖审批 | `browser-approved-packages.json`、`nonbrowser-approved-packages.json` + reviewCategory | 没有 |
| 发版 | change files、version policies（lockstep / individual）、`rush version`、`rush publish` | 11.13 起原生发版（见下节）；或 changesets |
| 版本 PR | 没有官方 Action，官方发布指南让 CI 直接推到目标分支 | changesets/action |
| deploy | `rush deploy`（`@rushstack/package-extractor`） | `pnpm deploy` |

## pnpm 原生发版

- [pnpm v11.13.0 release notes](https://github.com/pnpm/pnpm/releases/tag/v11.13.0)（2026-07-13）："Added native workspace release management"：`pnpm change` 把变更记录写成 changesets 兼容的 `.changeset/*.md`；`pnpm version -r` 消费记录、沿 `workspace:` 依赖传播升级、处理 fixed 分组和 `maxBump`、写 changelog，并把消费过的记录写进提交到仓库的 ledger；lanes 发布 `X.Y.Z-lane.N` 预发布版本。配置在 `pnpm-workspace.yaml` 的 `versioning` 下。
- 同一 release notes：changelog 默认 `registry` 存放，不提交 CHANGELOG.md，发布时把这次的条目拼在上一个已发布版本的 changelog 前面打进 tarball；消费过的记录要等 registry 确认已发布才被后续 `pnpm version -r` 清理。设 `versioning.changelog.storage: repository` 改为提交 CHANGELOG.md。
- 后续变化：11.16 起首发版本直接用 manifest 里的版本（文档 <https://pnpm.io/versioning>）；[v12.4.0](https://github.com/pnpm/pnpm/releases/tag/v12.4.0) 加 `pnpm change check`，只校验已提交的版本是否符合 `versioning.epics` 和 `versioning.fixed`；v12.6.0 起 `pnpm change check` 还校验未消费的记录文件；[v12.7.0](https://github.com/pnpm/pnpm/releases/tag/v12.7.0) 起 `pnpm version` 也给私有包升版本，私有包的 changelog 始终写进提交的 CHANGELOG.md。
- 文档 `docs/cli/change.md`（pnpm/pnpm.io 仓库）：`check` "reads no intents"，用于每个 PR 校验版本号，不检查 PR 是否漏写记录。
- `docs/settings/versioning.md`：`maxBump` 限制当前检出能发出的最大升级幅度，在依赖传播和 fixed 分组处理之后的最终发版计划上生效；`changelog.storage` 只有 `registry`、`repository` 两个值，没有可替换的 changelog 格式。
- 设计文档 [pnpm/rfcs `text/0006-monorepo-versioning.md`](https://github.com/pnpm/rfcs/blob/main/text/0006-monorepo-versioning.md)：
  - 「Enforcing coverage: `pnpm change check`」一节设计的是按分支 diff 找出改动的包、缺记录就失败（对应 `rush change --verify`），与 12.4 实际发布的功能不同。
  - 「Snapshot releases」一节设计了 `pnpm publish -r --snapshot [tag]`。
  - 「Unresolved Questions」列出：是否提供类似 changesets/action 的官方 Action、`pnpm version -r` 是否自己提交和打 tag、changelog 格式是否可插拔、是否从 conventional commits 生成记录。
- pnpm 文档 <https://pnpm.io/using-changesets> 的 GitHub Actions 示例仍使用 changesets/action。

## changesets 与 changesets/action 的相关实现

- `changeset publish` 发布前查询 registry，只发布还没发过的版本：`packages/cli/src/commands/publish-plan/getPublishPlan.ts:96-139`（changesets@`e2ee472`），过滤 `private` 包后对每个包调用 `publishTool.info`，按返回的 `versions` 判断是否已发布。发布后不回读确认。
- changesets/action 判断"开版本 PR 还是发布"的依据：`src/readChangesetState.ts` 用 `@changesets/read` 读取 `.changeset/*.md`；`src/index.ts:55-58` 以 `changesets.length !== 0` 作为 `hasChangesets`。版本 PR 描述从各包 `CHANGELOG.md` 中取出新版本对应的条目（`src/run.ts:40-48`）。

## 依赖升级机器人

- Dependabot 支持 Rush：[dependabot-core#2270](https://github.com/dependabot/dependabot-core/issues/2270) "Add support for Rush"，2020-07-01 创建，仍 open。
- Dependabot 对 pnpm 11/12：[dependabot-core#16397](https://github.com/dependabot/dependabot-core/issues/16397) 中维护者 2026-09-28 回复 "We don't officially support pnpm 11 or 12 at the moment. There's limited support for pnpm 11 today"；[#16513](https://github.com/dependabot/dependabot-core/pull/16513) "[Part 1 of 3] PNPM upgrade from 11.x.x to 12.x.x" 于 2026-10-09 合并。
- Renovate 支持 Rush：[renovatebot/renovate#3681](https://github.com/renovatebot/renovate/issues/3681)，2019 年起 open。

## 公开仓库观察：PerfectPan/agent-kit

- `rush.json` 有 15 个项目，其中 2 个挂在 lockstep 策略 `main` 上发 npm；没有 `build-cache.json`；根脚本 `build` 跑的是 `rush rebuild`（全量）。
- 为了开版本 PR 并在描述里附 changelog，仓库在 `scripts/` 下自写发版脚本，TypeScript 共 1082 行（含测试），版本 PR 用 `peter-evans/create-pull-request` 打开（#150 加入 `release-notes.ts`）。
- Dependabot：npm 升级 PR 共 35 个，0 个合入（34 个关闭、1 个打开，2026-10-19 查询）。#139 只修改 5 个 `package.json`，CI 在 `rush install` 失败，日志："The shrinkwrap file (pnpm-lock.yaml) is out of date. You need to run "rush update"."
- CI 成功运行的全程耗时 2–3 分钟（`gh run list --workflow ci.yml --status success` 最近 8 次）。

## 迁移案例

| 项目 | 方向 | 时间 | 原文 | 链接 |
| --- | --- | --- | --- | --- |
| microsoft/typespec | Rush → pnpm + changesets | 2024-01-24 合并 | "Remove the opinionated (wrongly so most of the time) middleman that brings more config pain than value" | <https://github.com/microsoft/typespec/pull/2775> |
| Azure/azure-sdk-for-js | Rush → pnpm workspace + Turborepo，迁移前 439 个项目 | 2025-08-07 合并 | 2024-08 首次尝试 #30835："take better advantage of pnpm features and workspaces" | <https://github.com/Azure/azure-sdk-for-js/pull/34941> |
| Azure/autorest | Rush → pnpm workspace + Chronus | 2026-06-10 合并 | PR 未写原因 | <https://github.com/Azure/autorest/pull/5190> |
| microsoft/power-platform-playwright-samples | Rush → npm workspaces | 2026-07-15 合并 | PR 未写原因 | <https://github.com/microsoft/power-platform-playwright-samples/pull/44> |
| wso2/agent-manager | Rush → pnpm | 2026-09-14 合并 | "Current console build takes 15-20 minutes cold"；"We're not working at the scale that Rush is beneficial"；迁移后冷构建约 1 分 20 秒 | <https://github.com/wso2/agent-manager/pull/1555> |
| hcengineering/platform | 尝试迁出，未合并 | 2024-12 | Devin 生成的 PR #7511、#7512、#7519 均关闭，仓库仍用 Rush | <https://github.com/hcengineering/platform/pull/7519> |
| microsoft/fluentui | Rush → Lerna + Yarn（现用 Nx） | 2019-07-20 合并 | "more popularity with our industry" | <https://github.com/microsoft/fluentui/pull/9827> |

2024-10 以后没找到大项目迁入 Rush 的公开 PR。新建即用 Rush 的有 bytedance/flowgram.ai（2025-02）、coze-dev/coze-studio（前端约 259 个项目）、coze-dev/coze-loop（2025-06）。仍在用 Rush 的还有 microsoft/rushstack、iTwin/itwinjs-core、microsoft/ApplicationInsights-JS、hcengineering/platform、VisActor/VChart、gooddata/gooddata-ui-sdk。

## 趋势数据

npm 周下载量（万次，`https://api.npmjs.org/downloads/range/`，各取完整 7 天）：

| 包 | 2024-09-29 周 | 2025-09-28 周 | 2026-09-27 周 |
| --- | --- | --- | --- |
| @microsoft/rush | 65.0 | 68.5 | 93.5 |
| pnpm | 1581 | 3221 | 24300 |
| turbo | 306 | 560 | 3382 |
| nx | 462 | 603 | 1228 |
| @changesets/cli | 95 | 148 | 673 |

接口返回的 2026-10-10 至 10-16 一周有三天为 0，属数据缺失，未采用。2026 年各包下载量都大涨，原因未核实。

State of JS：2024 年 monorepo 工具 "Used at Work" 人数 pnpm 3508、npm Workspaces 2438、Nx 1917、Turborepo 1412、Rush 147（<https://2024.stateofjs.com/en-US/libraries/monorepo_tools/>）；2025 年并入 Other Tools，pnpm 3940、Turborepo 1718、Nx 1682、Rush 74（<https://2025.stateofjs.com/en-US/other-tools/>，页面无日期）。两年口径不同。

## pnpm 的规划（pnpm/rfcs，2026-10-19）

- 2026-07 以来 pnpm/rfcs 共 29 个 PR，作者均为 zkochan；同期 pnpm/pnpm 主仓库提交中 zkochan 1515 次，第二名 127 次（commits API，2026-07-19 起）。
- 已合并、在 pnpm/pnpm `.changeset/` 未发布记录里没搜到对应实现：per-package permissions、agent skills in dependencies、config fragments。zstd registry tarballs 在未发布记录里有 6 处匹配，内容未读（GitHub code search 限流）。
- 已实现未发布：`lockfile.integrityTarget: tar`（`.changeset/lockfile-integrity-target.md`）；pnpr 存储 `pnpm pipeline --report` 的运行报告（`.changeset/pnpr-pipeline-runs.md`）。
- 已发布：`tool:` 协议（12.12.1）。
- 开放中：[rfcs#25](https://github.com/pnpm/rfcs/pull/25) pnpm 作为 CI 引擎与 pnpm CI 服务；[rfcs#34](https://github.com/pnpm/rfcs/pull/34) Cargo 生态与 pnpr 作为 crate registry；[rfcs#33](https://github.com/pnpm/rfcs/pull/33) 用 Bit 替代 Git（草案）。
- pnpr：pnpm/pnpm 仓库 `pnpr/` 目录，`pnpr/npm/pnpr/package.json` 版本 `0.1.0-alpha.15`，描述 "pnpm-compatible npm registry server, written in Rust"；文档 `pnpr-docs/introduction.md`（pnpm/pnpm.io 仓库）说明它同时支持 npm、Cargo、Python 和 OCI；许可证为 PolyForm Shield 1.0.0（`pnpm/rfcs` 的 `pnpr/README.md`）。
- 2025 年度总结 `blog/2025-12-29-pnpm-in-2025.md`：全局虚拟存储暂不默认开启，可能在以后的大版本默认开启。

## 验证记录

### changesets 3.0.3 + pnpm 10.34.5（2026-10-19，临时目录，已删除）

三包 workspace：`@t/a`、`@t/b`（0.19.0，b 依赖 `@t/a: workspace:^`）、`@t/c`（private，被 a 以 devDependency `workspace:*` 引用）。`.changeset/config.json` 设 `fixed: [["@t/a","@t/b"]]`、`privatePackages: { version: false, tag: false }`。

1. 只改 c 并提交：`changeset status --since=main` 退出码 0（不报缺记录）。
2. 再改 a、不写记录：退出码 1，"Some packages have been changed but no changesets were found"。
3. 给 a 写 patch 记录后 `changeset version`：a=0.19.1、b=0.19.1、c=0.0.0。

### pnpm 12.14.0 原生发版（2026-10-19，临时目录，已删除）

同样的三包结构，`pnpm-workspace.yaml` 设 `versioning.fixed: [["@t/a", "@t/b"]]`。

1. 改 a、不写记录：`pnpm change status` 输出 "No pending changes."，退出码 0；`pnpm change check` 输出 "No pending change intents to check." 和 "All package versions satisfy the configured versioning invariants."，退出码 0。
2. `pnpm --filter @t/a change --bump patch --summary "..." -y` 在非终端环境报错 "IO error: not a terminal"，没有写出文件；手写 `.changeset/fix-a.md` 后可用。
3. `storage: repository`：`pnpm change status` 显示 "@t/a: 0.19.0 → 0.19.1 (patch, via fixed+intent)"、"@t/b: 0.19.0 → 0.19.1 (patch, via fixed)"。`pnpm version -r` 后 a、b 为 0.19.1，c 不变；记录文件被删除；新增 `.changeset/ledger.yaml`（`"@t/a@0.19.1": dir: packages/a, intents: [fix-a]`）；`packages/a/CHANGELOG.md` 为 `## 0.19.1` / `### Patch Changes` / `- <summary>`，`packages/b/CHANGELOG.md` 只有 `## 0.19.1` 标题、没有条目；没有 git 提交和 tag。
4. 默认 `registry` 存放：写 minor 记录后 `pnpm version -r`，a、b 升到 0.20.0；记录文件 `.changeset/add-flag.md` 保留，新增 `.changeset/changelogs/` 目录和 `ledger.yaml`；之后 `pnpm change status` 输出 "No pending changes."。

### 未验证

- changesets/action 以 `pnpm version -r` 作为 version 脚本、在 GitHub Actions 上开版本 PR 的完整流程。
- Dependabot 和 Renovate 能否正确更新 pnpm 12 的根 lockfile。
- Rush lockstep 下没有改动的成员是否也会一起发布（按"同一策略共用一个版本"推断，未实测）。
