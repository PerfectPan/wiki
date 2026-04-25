---
title: Monorepo
type: topic
category: tooling
status: seed
created: 2026-04-12
updated: 2026-04-25
tags:
  - monorepo
source_refs:
  - raw/sources/Monorepo.md
---
# Monorepo

- 使用 [[Yarn]] workspace 来管理依赖，使用 [[Lerna]] 来管理 [[npm]] 包的版本发布。
	- 推荐阅读：https://zhuanlan.zhihu.com/p/71385053
- 评价标准和框架对比：https://monorepo.tools/
- 感觉能够管理好依赖（增量下载），然后能解决包发布就能基本能解决 monorepo 的问题了？远程 cache 这些感觉还用不太到。构建并行化其实还不知道怎么检测的
- TypeScript `project references` 在 monorepo 里有一个常见坑：如果子包都按 npm 包的方式被装进 `node_modules`，TS 默认未必能把它们识别成工作区里的源码项目。这时往往要用 `paths` 显式把包名映射回仓库内路径，才能让 project references 正常串起来。
- 发包链路也要额外注意 workspace 边界。一个常见坑是：`npm pack` 不会因为声明了 `bundleDependencies`，就自动把 monorepo 里的本地包一起打进去，所以多包仓库的发布验证不能只按单包直觉来想。
-

## Source Pointers

- `raw/sources/Monorepo.md`
