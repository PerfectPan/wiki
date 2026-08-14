---
title: Mini Shai-Hulud npm 供应链攻击
type: synthesis
category: tooling
created: 2026-05-12
updated: 2026-05-12
tags:
  - npm
  - supply-chain
  - github-actions
  - slsa
  - ci-cd
source_refs:
  - raw/sources/2026-05-12-mini-shai-hulud-npm-supply-chain.md
  - https://www.stepsecurity.io/blog/mini-shai-hulud-is-back-a-self-spreading-supply-chain-attack-hits-the-npm-ecosystem
---
# Mini Shai-Hulud npm 供应链攻击

## 问题

Mini Shai-Hulud 这类 npm 蠕虫为什么比普通恶意包更危险？它对 npm trusted publishing、SLSA provenance 和 GitHub Actions OIDC 的信任模型有什么启发？

## 简答

它不是简单的 typosquatting 或一次性投毒，而是利用 CI/CD 凭证和 OIDC 发布能力自传播：先让恶意代码在合法 pipeline 内运行，偷取 GitHub / npm / cloud secrets，再用这些权限发布更多恶意版本。最关键的教训是：SLSA provenance 只能证明包由某个 pipeline 产出，不能证明 pipeline 在产出时没有被恶意步骤控制。

## 攻击链

1. **payload staging。** 攻击者在 TanStack/router 的 fork 中提交伪装为 `@tanstack/setup` 的包，通过 `prepare` hook 执行混淆 JS。commit 可通过 `github:tanstack/router#<hash>` 访问，看起来像合法仓库引用。
2. **包内容注入。** compromised package 中新增 `optionalDependencies` 指向攻击者 fork commit，并在包根目录加入约 2.3MB 的 `router_init.js`。文件数量和 tarball 体积显著异常。
3. **合法 CI/CD 发布。** 恶意代码利用 GitHub Actions 中可用的 OIDC token / npm trusted publishing 能力，绕过正常 publish step，发布带合法 provenance 的恶意 npm 版本。
4. **凭证窃取。** payload 读取 GitHub Actions `Runner.Worker` 进程内存，提取所有 secrets；同时收集 AWS/ECS/Vault、SSH、npm、Docker、Kubernetes、AI 工具配置、shell history 等本地凭证。
5. **自传播。** 蠕虫寻找 npm publish token 或通过 GitHub OIDC 换取 per-package publish token，枚举 maintainer 可发布的包并继续投毒。
6. **持久化与外泄。** payload 写入 Claude Code hook、VS Code folderOpen task、LaunchAgent/systemd user service，并通过 GitHub dead-drop commits 或 C2 域名外泄数据。

## 关键判断

- **provenance 是出处证明，不是行为证明。** 如果 build pipeline 被恶意代码控制，最终产物依然可以拥有合法 SLSA attestation。
- **install phase 是高危执行点。** `prepare`、`postinstall`、`optionalDependencies`、`github:` dependency 都能在依赖安装阶段执行代码。
- **CI secrets 的暴露面比 YAML 看起来更大。** Runner.Worker 内存抓取意味着未在当前 step 显式引用的 secrets 也可能被读出。
- **OIDC 让 token 更短命，但不自动安全。** 一旦恶意代码在 runner 内执行，短命 token 仍可被即时换成发布权限。
- **AI 工具配置已进入攻击面。** payload 明确读取 Claude、Kiro 等 AI 工具配置，说明 agent/AI devtool 已经被纳入供应链攻击目标。

## 防御要点

- 对 CI runner 做网络 egress allowlist，至少限制安装阶段访问未知域名。
- 对新发布 npm 版本设置 cooldown，不要在发布后几分钟内自动进入生产 CI。
- 检测包体积、根目录异常文件、`optionalDependencies` 中的 `github:` URL、install scripts 和短时间连续发布。
- 最小化 GitHub Actions `permissions`，谨慎授予 `id-token: write`，把 release/publish workflow 与测试 workflow 分离。
- 避免在安装依赖的 job 中暴露高价值 secrets；发布 token、cloud token、npm token 应只在最小 job/step 可见。
- 发现命中版本后，不只升级依赖，还要检查持久化文件、注入 workflow、npm token、GitHub tokens、cloud credentials、SSH key 和开发机本地配置。
- 不要把 `npm audit signatures` 或 SLSA provenance 当成恶意包检测的充分条件。

## 未决问题

- 生态层面如何在不破坏 maintainer 体验的情况下限制 OIDC publishing 被滥用？
- npm registry 是否应对 tarball size anomaly、根目录额外可执行文件、异常 `github:` dependency 做更强策略拦截？
- CI runner 是否应默认阻止普通 dependency install 读取 `/proc/*/mem` 或访问 cloud metadata endpoint？

## 来源指针

- `raw/sources/2026-05-12-mini-shai-hulud-npm-supply-chain.md`
- https://www.stepsecurity.io/blog/mini-shai-hulud-is-back-a-self-spreading-supply-chain-attack-hits-the-npm-ecosystem
