---
title: GitHub Home Feed 抓取实验
created: 2026-06-22
source: local gh api probe
---

# GitHub Home Feed 抓取实验

## 背景

目标是验证是否可以把 `https://github.com/` 首页 Feed 中的活动转成每日摘要，并进一步推送与沉淀到 `PerfectPan/wiki`。

## 本地账号与关注规模

本地 `gh` 登录账号为 `PerfectPan`。`gh api user` 显示：

```json
{
  "login": "PerfectPan",
  "followers": 59,
  "following": 165,
  "public_repos": 87
}
```

## 严格 followee 事件抓取

用 `/user/following` 获取 165 个 followee，然后逐个请求 `/users/{login}/events/public`，只保留最近 24 小时的 `WatchEvent`、`PullRequestEvent`、`ReleaseEvent`。

实验结果：

- 约 77 条有效事件。
- `PullRequestEvent` 约 71 条。
- `WatchEvent` 6 条。
- `ReleaseEvent` 0 条。

观察：

- 严格 followee 抓取可以表达“我关注的人做了什么”。
- 但逐个 followee 请求延迟较高，且 PR 噪音明显多于 star / release。
- 这种模式更适合作为补充信号，不适合作为主数据源。

本轮 star 信号包括：

- `fi3ework` starred `BuilderIO/skills`
- `Dup4` starred `obra/superpowers`
- `yisar` starred `suxin2017/lynx-proxy`
- `hyf0` starred `Boshen/rust-performance-improvement-plan`
- `fengmk2` starred `liangmiQwQ/vp-config`
- `losfair` starred `openbsd/src`

## GitHub Home Feed 对齐验证

截图中的第一张 GitHub Home Feed 卡片显示：

- `bartlomieju contributed to denoland/deno`
- PR `#35406`
- 标题：`fix(node/test): route nested top-level test() to a subtest`
- 状态：`Merged`
- `bartlomieju merged 3 commits`
- 正文摘要来自 PR body 开头

用 `/users/PerfectPan/received_events?per_page=20` 能找到同一事件：

```json
{
  "type": "PullRequestEvent",
  "actor": "bartlomieju",
  "repo": "denoland/deno",
  "action": "merged",
  "number": 35406,
  "created_at": "2026-06-22T09:48:29Z",
  "pr_api_url": "https://api.github.com/repos/denoland/deno/pulls/35406"
}
```

再用 `/repos/denoland/deno/pulls/35406` 补详情，可以得到：

```json
{
  "number": 35406,
  "title": "fix(node/test): route nested top-level test() to a subtest",
  "html_url": "https://github.com/denoland/deno/pull/35406",
  "merged": true,
  "merged_at": "2026-06-22T09:48:29Z",
  "commits": 3,
  "comments": 0,
  "review_comments": 2
}
```

GraphQL 补查：

```json
{
  "comments": { "totalCount": 0 },
  "reviewThreads": { "totalCount": 1 },
  "reviews": { "totalCount": 2 },
  "commits": { "totalCount": 3 }
}
```

这说明 GitHub 网页 Feed 的卡片可以由 `received_events` 加 PR / repo / release 详情基本复原。评论数这类 UI 字段可能是 GitHub 前端的聚合视图，不应强依赖单个 REST 字段。

## 结论

用于每日摘要的主数据源应为 `/users/PerfectPan/received_events`，因为它更接近 GitHub Home Feed 的语义：来自 watched repositories 和 followed users 的活动流。

`/users/{followee}/events/public` 只适合作为补充，用于发现 followee star 的项目、或给跟随对象行为加权。

直接抓 `github.com` 网页 DOM 不适合作为稳定实现：本轮 Chrome 读取 GitHub 首页 DOM 多次超时，且网页结构、排序和聚合规则没有稳定 API 契约。
