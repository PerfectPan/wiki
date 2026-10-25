# Reylo / TypeScript Content Mapper 核查记录

- 访问日期：2026-10-24（Asia/Shanghai）
- 主要来源：
  - https://devblogs.microsoft.com/typescript/announcing-typescript-7-1-beta/（2026-10-20）
  - https://github.com/microsoft/typescript-go/pull/4712
  - https://github.com/microsoft/TypeScript/blob/main/tsc/internal/tsoptions/contentmappers.go
  - https://github.com/microsoft/TypeScript/issues/63703
  - https://reylo.dev/ 、https://reylo.dev/llms.txt
  - https://github.com/colinhacks/reylo （本地克隆 `/workspace/reylo-src`，提交 `1eecb3e107af66d2565896869da1bd581b9ccd27`）
- 调研全文底稿：`/workspace/typescript-content-mapper-reylo-report.md`（同日整理）

## 核查过的关键路径（Reylo）

- `package.json`（`typescript.contentMapper`：`exec`、`dynamicConfig: true`）
- `src/mapper.ts`、`src/mapper-server.ts`、`src/rpc.ts`
- `src/analyze.ts`、`src/module-types.ts`、`src/loader.ts`
- `src/register.ts`、`src/bridge.ts`、`src/vite.ts`、`src/index.ts`、`src/project.ts`
- `packages/postgres/describe.ts`、`packages/*/tooling.ts`

## 关键观察（只读事实）

| 结论 | 来源 / 位置 | 观察 |
| --- | --- | --- |
| Content mapper 把外来扩展变成虚拟 TS 文本并带 span map | TS 7.1 Beta 博文；typescript-go#4712 | 注册扩展后 `transform` 产出可检查文本 |
| CLI 必须 `--runExternalCode` | #4712；`contentmappers.go` | mapper 是可执行进程；编辑器需 workspace trust |
| TS 本身不做 SQL 类型推断 | 博文 / PR 能力边界 | SQL→类型由 Reylo 在 `transform` 内完成 |
| Reylo 用开发库 PREPARE/Describe，不真正跑查询 | reylo.dev FAQ；`packages/postgres/describe.ts` | Postgres：`sql.unsafe(text).describe()` |
| 类型路径与运行时路径共用 `Session.analyze` / `.reylo/` 缓存 | `src/analyze.ts` 文件头与实现 | mapper 出 `declare Query`；register/Vite 出 `defineQuery` |
| Content-mapped 文件不 emit JS | #4712 Emit 节 | 故运行时需独立 loader |

## 验证记录

- 已读：官方 7.1 Beta 博文、PR #4712 描述、TypeScript `contentmappers.go`、Reylo 站点与上述源码路径。
- 未安装、未运行 Reylo；未对真实数据库做 PREPARE；未跑 `tsc --runExternalCode`。
- 未能打开：`https://x.com/colinhacks/status/2113480503026454950`（WebFetch 403；正文此前经 X API 已读，本记录不以该帖为独立证据）。

## 未在公开资料中找到 / 未完整展开

- 官方 Handbook 独立 Content Mapper 章节的稳定 URL。
- 官方通用 content mapper JS SDK 包名（PR 写 Later follow-up）。
- WASM 引擎内 nullability 等逐条算法（需再读 Rust）。
