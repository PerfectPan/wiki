---
title: Mini Shai-Hulud npm supply-chain attack
source_type: article
created: 2026-05-12
source_refs:
  - https://www.stepsecurity.io/blog/mini-shai-hulud-is-back-a-self-spreading-supply-chain-attack-hits-the-npm-ecosystem
---

# Mini Shai-Hulud npm supply-chain attack

StepSecurity 披露 TeamPCP 的 Mini Shai-Hulud 蠕虫新一轮攻击。攻击影响 TanStack、UiPath、DraftLab、OpenSearch、Mistral 等 npm / PyPI 包。核心特征是：攻击者通过 CI/CD 链路盗取凭证，利用 GitHub Actions OIDC 与 npm trusted publishing 发布带有合法 SLSA provenance 的恶意包，再用偷到的 token 继续感染同一 maintainer 可发布的其他包。

关键事实：

- TanStack 事件中，攻击者通过 `pull_request_target` Pwn Request、GitHub Actions cache poisoning、Runner.Worker 内存中 OIDC token / secrets 提取，发布了 42 个 `@tanstack/*` 包的 84 个恶意版本。
- 恶意包带有合法 SLSA Build Level 3 provenance，但这是因为攻击运行在合法 CI/CD pipeline 内；provenance 证明“哪个 pipeline 产出”，不证明 pipeline 行为安全。
- 恶意 payload 通过 optionalDependencies 指向 `github:tanstack/router#79ac49e...`，该 commit 实际来自攻击者 fork，但 URL 看起来像合法 TanStack 仓库。
- payload 是约 2.3MB 单行混淆 JS，安装时会引入 Bun 并执行。
- 它会读取 GitHub Actions `Runner.Worker` 的 `/proc/{pid}/mem`，匹配 `{"value":"...","isSecret":true}` 结构，抓取 workflow 环境中所有 secrets，包括未显式引用、仅被 masking 的 secrets。
- 它还收集 AWS IMDSv2、ECS metadata、Vault、本地 cloud/dev/SSH/Git/npm/Docker/Kubernetes/AI 工具配置、shell history、钱包和聊天软件数据。
- 持久化方式包括 `.claude/settings.json` SessionStart hook、`.vscode/tasks.json` folderOpen task、macOS LaunchAgent、Linux systemd user service，以及注入 `.github/workflows/codeql_analysis.yml` 读取 `toJSON(secrets)`。
- C2 / IOC 包括 `git-tanstack.com`、`api.masscan.cloud`、`filev2.getsession.org`、`seed1.getsession.org`，以及 `router_init.js` hash `ab4fcadaec49c03278063dd269ea5eef82d24f2124a8e15d7b90f2fa8601266c`。

主要启发：

- SLSA / npm provenance 不是恶意代码检测机制。可信发布链路被攻陷后，会产出“合法签名的恶意包”。
- CI 中跑 `npm install` 不能被视为低风险行为；install script / optional dependency / git dependency 都可能变成凭证提取入口。
- GitHub Actions OIDC token 的权限边界和 workflow `id-token: write` 使用必须收紧。
- 供应链防御需要 package cooldown、网络 egress allowlist、可疑包尺寸/文件结构检测、CI secrets 最小化、依赖安装隔离和实时包情报。
