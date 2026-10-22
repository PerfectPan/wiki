- https://www.ruanyifeng.com/blog/2019/04/oauth_design.html
- OAuth 就是一种授权机制。数据的所有者告诉系统，同意授权第三方应用进入系统，获取这些数据。系统从而产生一个短期的进入令牌（token），用来代替密码，供第三方应用使用
- 一般第三方应用要先去系统注册获取 client id 和 secret
- 第三方应用会向系统携带 client id，告诉系统是谁在请求，用户授权以后会 redirect 到第三方应用的网址，携带授权码，然后请求业务后端，业务后端用 client id 和 secret 加授权码去请求系统的令牌，再跳回到前端（可以是裸的令牌，可以是和业务绑定后的 token），然后前端就可以用这个令牌（以用户的身份）去请求用户在系统的信息了
- 看着向 Github 注册的 **Homepage URL** 和 **Authorization callback URL** 不会校验端口，只会校验域名和 callback 的 path
- TODO 如何结合这个进一步设计登录态？
-
## 回调地址登记模型的核查记录（2026-10-16）

- 来源：[Google OAuth 2.0 for Web Server Applications](https://developers.google.com/identity/protocols/oauth2/web-server)、[Auth0 Application Settings](https://auth0.com/docs/get-started/applications/application-settings)、[Auth0 Subdomain URL placeholders](https://auth0.com/docs/get-started/applications/wildcards-for-subdomains)、[Auth0 Confidential and Public Applications](https://auth0.com/docs/get-started/applications/confidential-and-public-applications)、[Auth0 OAuth 2.0 协议页](https://auth0.com/docs/authenticate/protocols/oauth)、[Auth0 Cross-Origin Authentication](https://auth0.com/docs/authenticate/login/cross-origin-authentication)、[auth0-spa-js `189007f1`](https://github.com/auth0/auth0-spa-js/tree/189007f161ebc10369a4e986fe2d7f133ea00766)、[Supabase Login with Google](https://supabase.com/docs/guides/auth/social-login/auth-google)。
- 抓取方式：Auth0 文档站是 Mintlify 渲染的前端页面，直接抓 HTML 只能拿到脚本；在文档路径后加 `.md` 才能拿到正文，例如 `https://auth0.com/docs/get-started/applications/application-settings.md`。
- 核查证据：
  - Google 页面原文：`Redirect URIs cannot contain certain characters including: Wildcard characters ('*') ...`，并写明不匹配时报 `redirect_uri_mismatch`。
  - Auth0 **Allowed Callback URLs** 用逗号分隔可以列多条。子域通配 `https://*.example.com` 不跨两层子域，且「不应在生产使用」；官方推荐 `{organization_name}` 占位符。**Allowed Web Origins** 说明它管的是 Cross-Origin Authentication、Device Flow 和 `web_message` 响应模式的来源，字段最多 100 条。
  - Auth0 把 single-page apps 和 native apps 归为 public 客户端，public 客户端不能持有 secret。
  - `auth0-spa-js@189007f1` 的 `src/Auth0Client.ts`：`loginWithPopup` 传 `{ response_mode: 'web_message' }`，`redirect_uri` 取 `window.location.origin`，先 `openPopup('')` 再设 `config.popup.location.href`，换 token 用 `code_verifier` 加 `grant_type: authorization_code`；`getTokenSilently` 用 `runIframe` 请求 `/authorize`，同样 `response_mode=web_message` 加 `prompt: 'none'`；默认 `cacheLocation` 是 memory。`src/utils.ts` 的 `runPopup` 先判断 `e.origin !== eventOrigin`，再看 `e.data.type === 'authorization_response'`。
  - Supabase 的 Google 登录文档要求客户自己建 Google OAuth 客户端，把 Google 侧的 Authorized redirect URIs 填成 Supabase 项目的回调地址，再把 client id 和 secret 交给 Supabase。
- 验证记录：只读文档和 SDK 源码，没有登录任何 Auth0 租户或 Supabase 项目，没有实际跑过这三种流程，没有复现 `web_message` 交互。第三方 cookie 与 SPA 静默续期的关系只核对了 Auth0 跨源登录那一处表述，没有找到 SPA 静默续期的对应说明。
- 配图：`raw/assets/oauth-callback-registration.png`（1659×948，codex 内置 image_gen）按页面「回调地址登记在谁那里，决定谁去换 token」一节生成。按 PR #114 的审阅意见改用手绘白板风格，与同次提交的 `raw/assets/komo-architecture-sketch.png` 保持一致：白底、黑色手绘线、手写标签、无标题条、无彩色块。生成两轮，第二轮只去掉左上角一个没有含义的紫色对话气泡。核对项：两栏标题、8 处方框文字、7 条箭头方向（两栏各一条授权请求向下、一条 code 向下；`带 code_verifier 换 token` 和 `带 secret 换 token` 两条回指授权服务器；`postMessage 会话 token` 从服务方 API 回到站点页面）、底部结论条文字。它不是 Auth0、Google 或 Supabase 的官方素材，也不能当作证据，只能配着正文看。

## 发现、注册与 mix-up 相关 RFC 的核查记录（2026-10-22）

- 来源：RFC 7591、RFC 7636、RFC 8252、RFC 8414、RFC 8707、RFC 9126、RFC 9207、RFC 9449、RFC 9700、RFC 9728 的 rfc-editor.org 纯文本；`draft-ietf-oauth-client-id-metadata-document-02`；datatracker 上 `draft-ietf-oauth-v2-1` 的最新版本号（-16）；OpenID Connect Dynamic Client Registration 1.0 的 `application_type` 定义。
- 核查证据：
  - RFC 9728 §3.3：返回的 `resource` 必须与拼 well-known 地址用的资源标识相同；地址来自 `WWW-Authenticate` 的 `resource_metadata` 时，必须与客户端请求资源服务器所用的 URL 相同，否则不得使用。
  - RFC 8414 §3.3：元数据中的 `issuer` 必须与拼地址用的 issuer 相同。
  - RFC 8252 §7.3：回环 IP 回调「The authorization server MUST allow any port to be specified at the time of the request」；§8.3 写明用 `localhost` 是 NOT RECOMMENDED。
  - RFC 7636：verifier 为 43 至 128 个 unreserved 字符；`plain` 仅在无法支持 `S256` 时允许；附录 B 示例 `dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk` → `E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM`，本地用 Python 重算一致。
  - RFC 9700 §2.1：确认 AS 支持 PKCE 的客户端「MAY rely on the CSRF protection provided by PKCE」；OIDC 中 `nonce` 提供 CSRF 防护；否则必须用一次性 `state`。§4.4.1 的 mix-up 第 6 步：攻击者拿到 code 后，公开客户端可直接兑换，否则做 code 注入。§4.5.3.1：PKCE 能挡 code 注入。§4.5.4：攻击者能改受害者请求里的 `code_challenge` 时，PKCE 挡不住注入。页面中「mix-up 时攻击者可以替换 `code_challenge`」是把 §4.4.1 和 §4.5.4 放在一起推出来的，已在页面里注明。
  - CIMD -02：§3 Client Identifier URL 的格式与简单字符串比较；§4.1 禁止共享 secret 类认证和私钥；§4.2 回调精确匹配；§5.2 缓存规则；§8.1 冒充、§8.5 钓鱼与显示 hostname、§8.6 SSRF（禁止抓取 RFC 6890 特殊用途地址，开发测试环境的回环例外不得用于生产）、§8.9 域名信任策略。
  - OIDC Registration `application_type`：默认 `web`；使用隐式模式的 web 客户端只能登记 https 回调、不能用 localhost；native 客户端只能用自定义 scheme 或 http 回环地址。
  - RFC 9126 示例响应：`{"request_uri": "urn:example:bwc4JK-ESC0w8acc191e-Y1LTC2", "expires_in": 90}`。
- 写入位置：`wiki/topics/architecture/oauth.md` 从「对接陌生服务时，RFC 6749 缺的几块」到「进一步加固：PAR、DPoP 与 OAuth 2.1」各节。`wiki/topics/ai/mcp-authorization.md` 改为只写和普通 OAuth 的差异，原理部分链接到这里。
- 验证范围：只读规范文本，没有在任何 AS 上实际跑 DCR、CIMD、RFC 9207 或 PAR，各家 AS 的支持情况没有逐个核对。DCR 示例响应里的 `client_id_issued_at` 是示例值。
- 配图：`raw/assets/oauth-mcp-discovery-sequence.png` 由 matplotlib 脚本生成（白底黑线，Noto Sans CJK SC），按 PR #114 审阅意见用白板风格。核对项：四条泳道、① 到 ⑧ 的箭头方向、三个虚线框（MCP 新增发现、MCP 新增自动注册、2026-07-28 强制核对 iss）的范围、`resource` 标注为 MCP 强制。

## 配图重绘记录（2026-10-22）

- 按用户反馈，`raw/assets/oauth-mcp-discovery-sequence.png` 以及同批的 `near-membrane-blue-red-realms.png`、`agent-workspace-layers.png`、`js-sandbox-isolation-layers.png` 改用与 `raw/assets/cloudflare-computer-architecture.png` 等配图相同的脚本风格重绘：米色底、浅色填充的圆角框、xkcd 手绘线条、Noto Sans CJK SC。内容、文件名和路径不变。时序图里 MCP 新增或强制的步骤改用橙色虚线框加橙色标签，请求箭头为红色实线，响应箭头为蓝色虚线；blue / red 示意图里 blue Realm 用蓝色、red Realm 用红色、membrane 和 distortion 用紫色。上一条记录里的「白底黑线」说明以本条为准。重绘后逐张打开核对了标签文字、箭头方向，确认中文没有显示成方框。
