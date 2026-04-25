---
title: npm Trusted Publishers
type: topic
category: tooling
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - npm
  - oidc
  - supply-chain
  - publishing
source_refs:
  - /Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2025_09_07.md
  - https://docs.npmjs.com/trusted-publishers
---
# npm Trusted Publishers

## 摘要

`npm Trusted Publishers` 是 npm 提供的一种基于 OIDC 的发布机制：CI 平台不再长期持有 npm token，而是在受信任平台上用短期凭证向 npm 换取发布权限。

## 关键点

- journal 里的总结指出，它的核心不是“又一个 token”，而是把发布权限和 CI 平台身份绑定起来。
- 这意味着 token 不再需要长期存放在本地或 CI secrets 中，而是临时换取、短期使用、用完即过期。
- 这种方案的价值主要在供应链安全与可审计性：
  - 减少长期 token 泄漏风险；
  - 让发布动作更容易追溯到具体平台和流程。
- 限制也很明显：它需要 npm 和对应平台都支持这套受信任关系，因此不是任何环境都能直接启用。

## 相关页面

- [[npm 包发布与发布链路实践]]
- [[前端依赖管理策略]]

## 来源指针

- `/Users/perfectpan/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/journals/2025_09_07.md`
- [npm Trusted Publishers](https://docs.npmjs.com/trusted-publishers)
