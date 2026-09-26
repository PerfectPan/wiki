---
title: JWT
description: JWT 的结构、签名与加密的区别、常见算法、标准字段，以及实现时要防的攻击
type: topic
category: architecture
created: 2026-09-23
updated: 2026-09-26
timestamp: 2026-09-26
tags:
  - jwt
  - auth
  - security
source_refs:
  - https://www.rfc-editor.org/rfc/rfc7519
  - https://www.rfc-editor.org/rfc/rfc7515
  - https://www.rfc-editor.org/rfc/rfc7516
  - https://www.rfc-editor.org/rfc/rfc7518
  - https://www.rfc-editor.org/rfc/rfc8725
resource:
  - https://www.rfc-editor.org/rfc/rfc7519
  - https://www.rfc-editor.org/rfc/rfc7515
  - https://www.rfc-editor.org/rfc/rfc7516
  - https://www.rfc-editor.org/rfc/rfc7518
  - https://www.rfc-editor.org/rfc/rfc8725
---
# JWT

## 摘要

JWT（JSON Web Token，RFC 7519）是一种表示 JSON claims 的 token 格式，可使用 JWS 保护完整性，或使用 JWE 加密。服务端必须验证密码学保护与所需 claims；是否查询会话、权限或撤销状态，由应用设计决定。JWT 不规定获取流程，可以用于 [[OAuth]] 等协议。

本页主要讨论 JWS 形式的 JWT（RFC 7515）：**签名或 MAC 不会加密内容**。需要内容保密时可使用 JWE（RFC 7516）；签名与加密也可以嵌套。

## 结构

JWS 的紧凑格式是三段 Base64URL 字符串，用 `.` 连接：

```text
base64url(header).base64url(payload).base64url(signature)
# 结构示意，不是可验证的完整 token
```

| 段 | 内容 | 说明 |
| --- | --- | --- |
| header | `{"alg":"HS256","typ":"JWT","kid":"v1"}` | 签名算法、类型、密钥编号 |
| payload | `{"sub":"123","exp":1757703600}` | 业务字段。只是 Base64URL 编码，任何拿到 token 的人都能解开 |
| signature | `HMAC-SHA256(base64url(header) + "." + base64url(payload), key)` | 覆盖前两段，改任意一个字节都验不过 |

```mermaid
flowchart LR
  H[header] --> J["base64url(header) . base64url(payload)"]
  P[payload] --> J
  J --> S[签名算法 + 密钥]
  K[密钥 / 私钥] --> S
  S --> SIG[signature]
  J --> T["token = 前两段 . signature"]
  SIG --> T
```

## 标准字段（Registered Claims）

RFC 7519 §4.1 定义了这些字段。基础格式不强制全部存在，具体协议与应用应规定必填字段及验证要求：

| 字段 | 含义 |
| --- | --- |
| `iss` | 签发者 |
| `sub` | 主体，一般是用户 ID |
| `aud` | 接收方，校验方应确认自己在其中 |
| `exp` | 过期时间（Unix 秒）。用于有期限的访问凭证时应要求提供 |
| `nbf` | 在此时间之前无效 |
| `iat` | 签发时间 |
| `jti` | token 唯一编号，用于黑名单或"只能用一次" |

自定义字段放同一层即可。payload 不要放密码、手机号这类数据，也不要放太大的内容（每个请求都要带）。

## 签名算法

| 算法 | 类型 | 签发 | 校验 | 适合 |
| --- | --- | --- | --- | --- |
| HS256 | 对称（HMAC） | 共享密钥 | 同一个共享密钥 | 只有签发方自己验签 |
| RS256 | 非对称（RSA） | 私钥 | 公钥 | 多个服务各自验签、SSO |
| ES256 | 非对称（ECDSA） | 私钥 | 公钥 | 同上，密钥和签名更短 |
| EdDSA | 非对称（Ed25519） | 私钥 | 公钥 | 同上 |

HMAC 的签发方与验证方共享密钥，因此每个持有密钥的验证方也具备签发能力。共享范围必须受信任；需要把签发权限与验证权限分离时，可使用非对称算法，通过 JWKS 等方式发布公钥。

## 签名 ≠ 加密

- 签名（JWS）保证内容没被改过，不保证内容保密。
- 传输保密靠 HTTPS。
- 内容本身需要对持有者保密时，才用 JWE。JWE 的紧凑格式是五段：header、加密后的内容密钥、IV、密文、认证标签。

## 仅本地验证时的限制

以下讨论假设资源服务器只验证签名与 claims，不查询撤销或会话状态：

1. **无法仅凭 token 判断提前撤销**：要按用户或 token 撤销，可增加撤销列表、会话版本检查或内省接口。停用签名密钥也可使一批 token 失效，但影响范围更大。
2. **不能原地续期**：`exp` 在签名覆盖范围内，改了就验不过。续期只能签一个新 token。
3. **Bearer token 泄露后存在可用时间窗口**：短有效期可以限制窗口，但应结合撤销需求、凭证存储与实际风险确定期限。JWT 格式本身不提供防重放能力。

这几条如何在工程上取舍，见 [[Session vs JWT vs 双 Token]]。

## 常见攻击与防御

RFC 8725（JWT Best Current Practices）列出了主要问题：

| 攻击 | 做法 | 防御 |
| --- | --- | --- |
| `alg: none` | 把 header 里的算法改成 none，让服务端跳过验签 | 服务端写死允许的算法列表，不信 token 头里声明的算法 |
| 算法混淆 | 把 RS256 改成 HS256，拿公开的公钥当 HMAC 密钥签名 | 同上；每把密钥只绑定一种算法 |
| `kid` 注入 | 在 `kid` 里放路径或 SQL，诱导服务端加载攻击者控制的密钥 | `kid` 只能命中服务端已知的有限集合 |
| 弱密钥 | HS256 用短字符串做密钥，被离线暴力破解 | 用足够长的随机密钥（至少与哈希输出等长） |
| 跨服务复用 | 给 A 服务的 token 拿去调 B 服务 | 校验 `iss`、`aud`；不同用途的 token 用不同密钥或 `typ` 区分 |
| 重放 | 截获合法 token 重复使用 | 短 `exp`；一次性 token 用 `jti` 记录已用 |
| 窃取 | XSS 读取可访问的存储、传输泄露 | HTTPS；按客户端设计保护凭证存储；Cookie 方案还需考虑 CSRF；限制有效期 |

## 校验清单

1. 按服务端配置的算法验签，拒绝 `none` 和不在白名单里的算法。
2. 按 `kid` 选密钥，未知 `kid` 直接拒绝。
3. 校验 `exp`、`nbf`（允许少量时钟偏差）。
4. 校验 `iss`、`aud` 是否符合预期。
5. 有撤销需求时，查 `jti` 黑名单或会话记录。
6. 校验通过后再读取业务字段。

## 相关页面

- [[OAuth]]
- [[Session vs JWT vs 双 Token]]
- [[SSO]]

## 来源指针

- RFC 7519 JSON Web Token：https://www.rfc-editor.org/rfc/rfc7519
- RFC 7515 JSON Web Signature：https://www.rfc-editor.org/rfc/rfc7515
- RFC 7516 JSON Web Encryption：https://www.rfc-editor.org/rfc/rfc7516
- RFC 7518 JSON Web Algorithms：https://www.rfc-editor.org/rfc/rfc7518
- RFC 8725 JWT Best Current Practices：https://www.rfc-editor.org/rfc/rfc8725
