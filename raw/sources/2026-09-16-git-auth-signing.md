---
title: Git 认证与提交签名整理记录
type: source
created: 2026-09-16
source_refs:
  - https://git-scm.com/docs/gitcredentials
  - https://git-scm.com/docs/gitformat-signature
  - https://git-scm.com/docs/git-config
  - https://cli.github.com/manual/gh_auth_setup-git
  - https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification
  - https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
  - https://gnupg.org/documentation/manuals/gnupg/OpenPGP-Key-Management.html
---

# Git 认证与提交签名整理记录

素材来自 2026-09-16 关于 GitHub 认证和提交签名的讨论，以及同日核对的官方文档。这是按问题整理的记录，不是对话逐字稿或官方文档全文；不收录个人密钥、凭据、机器配置和账号历史。

## 讨论中的问题

- 使用 `gh` 登录后，拉取和推送是否仍由 Git 执行？
- SSH 认证密钥与 SSH 签名密钥分别解决什么问题？公钥应该登记在哪里？
- 本地私钥是给 commit 签名，还是加密 commit？Verified 说明了什么？
- GPG 与 SSH 签名有哪些取舍，管理能力更多是否意味着天然更安全？

## 核对的来源与章节

| 来源 | 对应章节与支持的事实 |
| --- | --- |
| [gitcredentials](https://git-scm.com/docs/gitcredentials) | AVOIDING REPETITION、CONFIGURATION OPTIONS：Git 通过外部 helper 获取凭据，helper 由配置选择 |
| [gh auth setup-git](https://cli.github.com/manual/gh_auth_setup-git) | 命令说明：将 GitHub CLI 配成 Git credential helper |
| [GitHub 认证](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github#authenticating-with-the-command-line) | 命令行认证：HTTPS 与 SSH 使用不同凭据 |
| [gitformat-signature](https://git-scm.com/docs/gitformat-signature#_commit_signatures) | Commit signatures：签名工具处理 commit payload，签名写入对象 |
| [GitHub 添加 SSH 密钥](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) | 密钥用途：认证与签名分别登记；同一公钥可登记两次 |
| [GitHub 签名验证](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification) | Default statuses、Persistent commit signature verification：状态含义及历史验证记录的保留范围 |
| [GitHub 签名配置](https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key) | Telling Git about your SSH key：Git 2.34 起支持 SSH 签名 |
| [GitHub 签名流程](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits) | 本地签名、推送与检查 Verified 是不同步骤 |
| [git-config](https://git-scm.com/docs/git-config) | gpg.format、gpg.ssh.allowedSignersFile、gpg.ssh.revocationFile：格式、信任与吊销配置 |
| [OpenSSH ssh-keygen](https://man.openbsd.org/ssh-keygen.1) | FIDO AUTHENTICATOR、ALLOWED SIGNERS：硬件密钥与验证有效期 |
| [GnuPG 密钥管理](https://gnupg.org/documentation/manuals/gnupg/OpenPGP-Key-Management.html) | quick-add-key、quick-set-expire、generate-revocation：子密钥、有效期与吊销证书 |
| [GnuPG 操作命令](https://www.gnupg.org/documentation/manuals/gnupg/Operational-GPG-Commands.html) | sign、encrypt：签名和加密是独立操作 |
| [git-pull](https://git-scm.com/docs/git-pull) | DESCRIPTION：fetch 后如何整合历史由选项和配置决定 |

## 收录判断

更新既有 `wiki/topics/tooling/Git.md`，保留数据模型和常用命令笔记，补入认证、签名及其取舍。SSH/GPG 的选择建议属于结合使用场景的判断，正文与官方机制说明分开表达。

两项讨论中的简化说法需要修正：把私钥签名称为加密会混淆用途；把有效期和吊销视为 GPG 独有能力，会遗漏 SSH 本地验证的允许列表、有效期和吊销配置。账号上今天显示哪些密钥，也不足以推断完整使用历史。
