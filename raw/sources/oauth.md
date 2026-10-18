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
