---
title: GitHub Home Feed 每日摘要方案
description: 设计一个每日抓取 GitHub Home Feed、筛选有意义项目、推送摘要并沉淀到 wiki 的自动化流程。
type: synthesis
category: tooling
status: seed
created: 2026-06-22
updated: 2026-06-22
timestamp: 2026-06-22
tags:
  - github
  - automation
  - feed
  - digest
  - wiki
source_refs:
  - raw/sources/github-feed/2026-06-22-github-feed-probe.md
  - https://docs.github.com/en/rest/activity/events
  - https://docs.github.com/en/rest/users/followers
resource:
  - raw/sources/github-feed/2026-06-22-github-feed-probe.md
  - https://docs.github.com/en/rest/activity/events
  - https://docs.github.com/en/rest/users/followers
---
# GitHub Home Feed 每日摘要方案

## 问题

每天手动刷 GitHub Home Feed 的成本越来越高。理想系统应该每天自动抓取关注对象和 watched repository 产生的活动，筛出真正值得关注的项目，推送一份短摘要，并把可复用的日报沉淀到 `PerfectPan/wiki`。

## 简答

第一版应以 `/users/PerfectPan/received_events` 作为主数据源，而不是直接抓 GitHub 网页或逐个抓 followee。它最接近 GitHub Home Feed 的底层事件语义；对入选事件再补 repo、PR、release 和 GraphQL 详情，最后生成推送消息，并在 wiki 仓库里以每日 PR 形式保存 raw digest。

## 领域边界

这个系统可以按四个边界拆开：

- **Feed 采集**：负责读取 GitHub 事件、处理分页、窗口和 API rate limit。
- **项目理解**：负责把原子事件聚合成候选项目，并补充仓库、PR、release 元数据。
- **摘要生成**：负责把候选项目排序、去噪、分组，输出稳定 Markdown。
- **分发与沉淀**：负责推送到通知渠道，并把 Markdown 与原始事件 JSON 写入 wiki PR。

关键领域对象：

- `FeedEvent`：GitHub Events API 的原子事件，包含 `id`、`type`、`actor`、`repo`、`created_at` 和 payload。
- `ActivityCard`：接近 GitHub Home Feed 卡片的归一化展示对象，例如 merged PR、starred repo、published release。
- `CandidateProject`：按 repository 聚合后的项目候选，带事件列表、来源人物、repo metadata 和分数。
- `DigestItem`：最终进入日报的一条摘要，包含标题、理由、链接和来源事件。
- `KnowledgeSink`：把每日摘要写入 wiki 的适配器。
- `Notifier`：把摘要推送到 Telegram、飞书、Slack、邮件或 GitHub Issue 的适配器。

## 数据源选择

主数据源：

```text
GET /users/PerfectPan/received_events
```

选择理由：

- 它比逐个 followee 事件更接近 `https://github.com/` 首页 Feed。
- 它天然包含 followed users 和 watched repositories 共同产生的活动。
- 本轮实验中，截图里的 `bartlomieju contributed to denoland/deno` PR 卡片可以由 `received_events` 加 PR 详情复原。

辅助数据源：

```text
GET /user/following
GET /repos/{owner}/{repo}
GET /repos/{owner}/{repo}/pulls/{number}
GET /repos/{owner}/{repo}/releases/{id}
GraphQL pullRequest comments / reviews / reviewThreads
```

使用方式：

- `following` 用来给 followee 触发的事件加权，而不是替代主 feed。
- `repo` metadata 用来补 description、language、topics、stars、pushed_at。
- `pulls` 用来补 PR title、body、merged、commits、html_url。
- GraphQL 只在入选 PR 上补网页卡片式的评论与 review 聚合信息，避免请求量过大。

不推荐直接抓网页 DOM。网页排序、聚合和结构没有稳定契约；本轮 Chrome 读取 GitHub 首页 DOM 也不稳定。网页可以用于人工验收，不应作为生产数据源。

## 每日抓取流程

推荐调度：

- 每天北京时间 09:00 和 18:00 各跑一次，第一版可以先只跑 09:00。
- 抓取窗口使用过去 36 小时，而不是严格 24 小时，避免 GitHub Events API 延迟导致漏数据。
- 输出日报时只展示目标自然日或最近一次未推送窗口内的新事件。

推荐流程：

1. 读取 `received_events` 前 3 页，每页 100 条。
2. 读取 following 集合，用于打分和标注。
3. 丢弃已在历史 raw event JSON 中出现过的 event id。
4. 保留高价值事件：`WatchEvent`、`ReleaseEvent`、`PullRequestEvent`、`ForkEvent`、高密度 `CreateEvent`。
5. 对入选 repo 补 repo metadata。
6. 对入选 PR / release 补详情。
7. 按 repo 聚合为 `CandidateProject`。
8. 用评分器排序并截断到 5 到 15 条。
9. 生成 Markdown 摘要。
10. 推送通知。
11. 写入 wiki 分支并开 PR。

## 评分规则

第一版可以用透明规则，不急着引入 LLM：

| 信号 | 加分 | 说明 |
| --- | --- | --- |
| followee starred repo | 高 | 最强项目发现信号 |
| release published | 高 | 明确可消费的新版本 |
| followed actor merged PR | 中 | 能反映项目活跃方向 |
| 多个 followee 触达同一 repo | 高 | 社交共识信号 |
| repo stars / recent pushed_at / topics 命中兴趣词 | 中 | 项目质量与相关性信号 |
| push / delete / label-only PR | 低 | 默认不进摘要，除非同 repo 聚合后有价值 |

兴趣词第一版可以配置为：

```yaml
interests:
  - agent
  - coding-agent
  - llm
  - mcp
  - ai
  - rust
  - typescript
  - javascript
  - toolchain
  - bundler
  - vite
  - deno
  - testing
  - performance
```

排序时应把“发现新项目”和“追踪活跃项目”分开：

- **发现新项目**：star、fork、新 release、多个 followee 同时触达。
- **活跃项目**：PR merged / opened、同一 repo 的高密度活动。

这样可以避免 PR 噪音淹没真正的新项目。

## 推送格式

每日通知应短，不要把 wiki 全量内容塞进消息：

```md
# GitHub Feed Digest - 2026-06-22

## 值得看

1. BuilderIO/skills - fi3ework starred
   Skills for coding agents. JavaScript, 2.3k stars.
   https://github.com/BuilderIO/skills

2. voidzero-dev/vite-plus - fengmk2 active PRs
   Unified web development toolchain. Recent merged PR: ...
   https://github.com/voidzero-dev/vite-plus

## 今天的 wiki 记录

PR: https://github.com/PerfectPan/wiki/pull/...
```

推送渠道先抽象为适配器：

- `webhook`：兼容飞书、Slack、Discord 的 generic webhook。
- `telegram`：适合个人即时推送。
- `email`：后置；配置和送达复杂度更高。
- `stdout`：本地调试和 CI 日志。

第一版建议先做 `stdout + webhook`。通知密钥只放 GitHub Actions secrets，不写入仓库。

## Wiki 沉淀方式

每日自动输出不应该直接写进 `wiki/syntheses/`，因为它更像原始事实和日报，不是长期综合结论。推荐写入：

```text
raw/sources/github-feed/YYYY/MM/YYYY-MM-DD.md
raw/sources/github-feed/YYYY/MM/YYYY-MM-DD.events.json
```

其中 Markdown 是人可读日报，JSON 是可复算事实层。

每次每日任务创建一个分支：

```text
automation/github-feed/YYYY-MM-DD
```

然后向 `PerfectPan/wiki` 开 PR。通知消息里带 PR 链接，由人决定是否合并。这样符合 wiki 仓库的 branch + PR 审阅规则，也避免自动任务直接污染 `main`。

后续如果连续多天出现同一项目，可以再由人或 agent 提升到：

```text
wiki/topics/tooling/<project>.md
wiki/syntheses/tooling/<topic>.md
wiki/comparisons/tooling/<decision>.md
```

## 状态与幂等

第一版不需要引入数据库。用 overlap window 加 raw JSON 去重即可：

- 抓过去 36 小时的 feed。
- 读取最近 7 天 `raw/sources/github-feed/**/*.events.json` 的 event id。
- 新事件才进入当日 digest。
- 如果同一天任务重跑，更新同一个分支和同一组文件。

ETag 可以作为第二阶段优化，用于减少 API 消耗；但不能把 ETag 当成唯一状态，因为 daily digest 更需要业务窗口去重。

## 错误处理

- GitHub API 失败：保留失败原因，推送一条降级通知，不写空日报。
- repo / PR detail 补全失败：保留事件基础信息，摘要中标记 metadata incomplete。
- wiki PR 创建失败：仍然推送 digest，并在通知中说明 wiki sink failed。
- notifier 失败：写 wiki PR 后让 GitHub Actions job fail，避免静默漏推。
- rate limit 低于阈值：停止补详情，只输出基础事件摘要。

## 未决问题

- 第一版推送渠道还需要确定，建议先选 generic webhook 或 Telegram。
- 是否每天自动 PR 可能会产生较多 PR；如果噪音过高，可以改成 weekly PR + daily notification。
- `received_events` 与网页 Home Feed 的排序不一定完全一致；系统目标应是复现有价值的活动，而不是逐像素复刻 GitHub 前端。

## 来源指针

- `raw/sources/github-feed/2026-06-22-github-feed-probe.md`
- GitHub REST Events API: <https://docs.github.com/en/rest/activity/events>
- GitHub REST Following API: <https://docs.github.com/en/rest/users/followers>
