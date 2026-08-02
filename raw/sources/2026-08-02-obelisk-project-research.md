# Obelisk 项目调研快照（2026-08-02）

## 调研对象

- 仓库：<https://github.com/tommy0103/obelisk>
- 源码快照：`71a80114`（2026-07-30，调研时 `main` HEAD）
- 最新 release：`v0.2.1`（2026-07-21）
- 调研日期：2026-08-02

## 仓库事实

- 创建于 2026-05-29；调研时 274 stars、16 forks、16 个 open issues。
- GitHub contributors API 只列出 `tommy0103`，104 次贡献。
- 主仓库许可证为 AGPL-3.0；单独发布的 docs-only skill artifact 使用 MIT。
- 支持索引 Claude Code、Codex 和 Kimi Code 的本地会话。
- CLI 和 Electron App 共用 `~/.obelisk/obelisk.sqlite`。
- 默认从 `~/.claude/projects`、`~/.codex/sessions`、`~/.kimi-code/sessions` 读取会话。

## 关键源码与文档位置

- `README.md`：产品入口、安装方式、数据来源、目录结构。
- `PRODUCT.md`：evidence before assertion、local trust、progressive density 等产品原则。
- `packages/core/src/providers/`：Claude、Codex、Kimi provider adapter。
- `packages/core/src/providers/types.ts`：统一 `TranscriptRecord` contract。
- `packages/core/src/schema.sql`：SQLite schema、FTS5 表和索引。
- `packages/core/src/query.ts`：query sandbox、FTS 查询和 memory API。
- `packages/core/src/persist.ts`：统一 record 持久化。
- `packages/core/src/writer-lease.ts`、`tx.ts`、`write-coordinator.ts`：单写者 lease、事务与重试。
- `docs/adr/0001-0007`：解析/持久化分层、运行时 contract、可审计构建、Electron 和并发决策。
- `skill-doc/SKILL.md`、`skill-doc/references/`：Agent 查询与显式记忆工作流。

## 本地验证

在干净 clone 中分别安装根工作区和 `app/` 依赖后执行：

```text
npm ci
cd app && npm ci
cd ..
npm test
npm run typecheck
npm run lint
```

结果：

- 295/295 tests passed。
- TypeScript typecheck passed。
- ESLint 0 errors、4 warnings。
- `npm audit` 在根工作区报告 1 个 high severity 的间接依赖问题：`brace-expansion` 的内存耗尽风险，有可用修复。

只在根目录执行 `npm ci && npm test` 会缺少 Electron、Vue、better-sqlite3、chokidar 等 App 依赖；当前仓库把 App 作为独立 package 管理，完整测试前还需在 `app/` 执行 `npm ci`。

## 已确认的公开限制

- Issue #9：默认 FTS5 `unicode61` tokenizer 使 CJK 内容难以检索。
- `query.ts` 还显式要求 memory query 和 summary 使用英文。
- Issue #16：首次检索存在无标题 session、自命中、已知空 memory recall 等预算浪费。
- Issue #5：provider package 插件化尚未完成。
- Issue #22：live patch 可能在滚动期间提交并导致时间线位移。

## 外部对照来源

- Claude Code sessions：<https://code.claude.com/docs/en/sessions>
- claude-history：<https://github.com/raine/claude-history>
- agent-sessions：<https://github.com/jazzyalex/agent-sessions>
- Letta Code：<https://github.com/letta-ai/letta-code>
- OpenMemory：<https://mem0.ai/openmemory>

## 调研判断

Obelisk 的长期价值不在桌面会话浏览，而在把不同 coding agent 的原始会话投影为统一、可查询、可回溯的本地证据层，并把人工批准的 Markdown memory 作为二级综合缓存。当前适合 Trial，不适合承担唯一长期记忆系统；主要限制是中文检索、单维护者、早期版本和敏感会话集中存储风险。
