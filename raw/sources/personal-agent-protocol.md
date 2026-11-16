<!--
source: https://personalagentprotocol.org
type: doc
published: 2026-11-10
fetched: 2026-11-16
note: Personal Agent Protocol (Poppy) v1.0 specification and extensions
-->

# Personal Agent Protocol（Poppy）v1.0 — 来源核查记录

## 访问元信息

- 站点首页：<https://personalagentprotocol.org>
- 官方文档索引：<https://personalagentprotocol.org/llms.txt>
- 已核查文档（版本 1.0，Apache License 2.0）：
  - 介绍：<https://personalagentprotocol.org/docs/introduction.md>
  - 1.0 规范全文：<https://personalagentprotocol.org/docs/1.0/spec.md>（由 2026-11-10 发布的 0.4 版冻结修订为 1.0）
  - 扩展总览：<https://personalagentprotocol.org/docs/1.0/extensions.md>
  - Operations 扩展（v3）：<https://personalagentprotocol.org/docs/1.0/extensions/operations.md>
- 访问日期：2026-11-16

## 核查位置与事实摘录

- **设计定位（`docs/introduction.md` & `spec.md` §1–§2）**：
  - 解决个人智能体（Personal Agent，代表单个自然人 User 行动的软件）与企业（Company）交互时的二选一困境（要么企业全面封禁 Agent，要么 Agent 用用户的账号密码登录并点击面向人类设计的网页，导致用户无法限制权限、企业也无法区分人机）。
  - 提供从“封禁 → 匿名查询 → 登录后查看 → 经用户批准执行写操作 → 完全访问”的细粒度控制。
  - 六个协议组件（`spec.md` §1.1）：Discovery（发现）、Operator recognition（运营商识别）、Sessions（会话）、Account access（账户授权）、Interaction channels（交互通道）、Task coverage and extensions（任务边界与扩展）。会话（Sessions）与账户访问（Account access）相互独立：未登录请求只带 `Poppy-Session` 头；已登录请求同时携带 `Poppy-Session` 头与 OAuth 访问令牌。
- **服务发现与双向校验（`spec.md` §3）**：
  - 企业必须在 `https://{domain}/.well-known/poppy.json` 发布发现文档，允许 HTTPS 重定向，但最终 URL 路径必须精确为 `/.well-known/poppy.json` 且无查询参数。
  - 双向防冒用检查：`organization.domain` 必须等于最终提供该文档的主机名；若有 OAuth issuer，则通过 `https://{organization.domain}/.well-known/oauth-protected-resource`（RFC 9728）发现授权服务器，且授权服务器元数据（RFC 8414）的 `protected_resources` 必须包含 `https://{organization.domain}`。
  - 除发现重定向与本地回环回调外，协议禁止在重定向中携带令牌、Session JWT、客户端断言或凭据，且禁止连接对方提供的回环、私网或链路本地地址（防 SSRF）。
- **OAuth 账户授权与 Agent 身份（`spec.md` §4）**：
  - **§4.1 Agent 身份**：Personal Agent 的 `client_id` 必须是返回其客户端元数据文档的 HTTPS URL（遵循 OAuth CIMD 草案），文档包含同域名的 `jwks_uri`、`redirect_uris` 且 `token_endpoint_auth_method` 为 `private_key_jwt`（RFC 7523）。客户端断言的 `aud` 必须精确等于企业 issuer 字符串（防恶意企业将断言重放到其他企业的 token 端点），有效期 `exp - iat <= 5` 分钟，企业必须支持 `ES256` 与 `PS384`。
  - **§4.2 Direct Sign-In（首选）**：OAuth 2.0 授权码 + PKCE（`S256`）。授权响应必须携带 RFC 9207 `iss` 参数供 Agent 核对；跨设备打开授权链接时必须带 `prompt=consent` 并遵守 RFC 10027（BCP 247）；支持企业要求 Pushed Authorization Requests（PAR，RFC 9126）。
  - **§4.3 Device Sign-In**：OAuth 2.0 设备授权流程（RFC 8628），Agent 必须校验 `verification_uri` 主机名属于企业 `issuer` 或 `organization.domain` 及其子域，并同时展示企业名称与域名。
  - **§4.4–§4.5 令牌与 DPoP / Resource**：支持刷新令牌轮换与 DPoP（RFC 9449）绑定（每个 DPoP 密钥仅限单个 `User ID` 使用，刷新时必须用同一 DPoP 密钥签名）；初始登录不带 `resource` 参数以覆盖企业向 Agent 开放的全部服务，后续调用若子服务（如独立 MCP 服务器）在 RFC 9728 元数据中声明了异于主域名的 `resource`，则用刷新令牌带 `resource`（RFC 8707）换取该服务专用令牌。
  - **§4.7 Scopes 与 `scope_hints`**：通过 `auth.scopes` 描述权限用途，通过 `auth.scope_hints` 标注 `changes`（`none` / `reversible` / `irreversible`）与 `personal_data`（`true` / `false`）；企业不得授予超出请求范围的 scope。
- **Sessions、伪匿名 User ID 与委托密钥（`spec.md` §5）**：
  - **§5.1 Pairwise User ID**：Personal Agent 为每个用户在每家企业分配稳定、不透明且互不相同的 `User ID`（`sub`），严禁包含或由邮箱、手机号、姓名等个人信息派生（即便加盐哈希也不允许），使企业能跨会话识别回访用户，但不同企业无法串通撞库。也支持每次匿名浏览生成一次性 `User ID`。
  - **§5.2–§5.3 `Poppy-Session` 头与委托密钥（Delegated keys）**：
    - 每个业务请求携带 `Poppy-Session`（`typ: poppy-session+jwt`，算法 `ES256`）与 `Poppy-Version: 1.0`。
    - Session JWT 不直接用 `jwks_uri` 中的主密钥签名，而是由有效期不超过 24 小时的委托密钥签名；主密钥签发不含任何用户或企业信息的委托凭证（`typ: poppy-delegation+jwt`，放在 Session JWT 头的 `poppy_dlg` 字段中）。每个委托密钥仅用于单一 `User ID`。
    - Session JWT 载荷包含 `iss`（`client_id`）、`aud`（企业标识符）、随机 `sid`（Session ID）、`sub`（User ID）、绑定当前请求的 `htm` 与 `htu`、`iat`、`jti`，以及存在访问令牌时的令牌哈希 `ath`。
    - 会话校验失败返回 HTTP 400 `{"error": "invalid_session"}`（不用 401，防止标准 OAuth 客户端库误删有效访问令牌）。
    - **Operator signatures**：建议同时使用 HTTP Message Signatures（RFC 9421）与 Web Bot Auth 对 `poppy-session` 和 `authorization` 头签名，供边缘 WAF/反爬网关识别运营商。
- **三类交互通道（`spec.md` §6–§8）**：
  - **§6 Web browsing（Browser Join）**：支持将受控浏览器加入当前 Session，三步流程：
    1. 浏览器访问 `GET {browser_session_endpoint}`，拿到含一次性隐藏 `code` 的表单与绑定该浏览器的短效 `__Host-` Cookie（`SameSite=Strict`、`HttpOnly`、`Cache-Control: no-store`、`frame-ancestors 'none'`）；
    2. Agent 在模型不可读的宿主代码中从自身浏览器页面读取 `code`，发送 `POST {browser_session_endpoint}/authorize`（携带 `Poppy-Session` 及含 `poppy:browser-sign-in` scope 的访问令牌）完成授权；
    3. 浏览器提交表单 `POST {browser_session_endpoint}`，企业核对步骤 1 的 Cookie 与步骤 2 的授权后种下会话 Cookie。访问令牌全程不经过浏览器，同时防范跨站请求伪造（CSRF / Session Fixation）与跨设备诱导授权。若网站无法按 scope 限制网页内操作，企业必须在 `poppy.json` 中设置 `web.unscoped: true` 并在授权页明确告知用户。
  - **§7 APIs**：支持 `openapi`（OpenAPI 3.0/3.1）与 `mcp`（Streamable HTTP，兼容 MCP 2025-06-18 及 2026-07-28）。
  - **§8 Conversations**：定义 `poppy` 对话协议（`POST {endpoint}` 创建、`POST {endpoint}/{id}/messages` 发消息、`GET {endpoint}/{id}/events` 轮询或 SSE 流式读取、`POST .../handoff` 请求企业真人介入、`POST .../close` 关闭）。每条请求带用户级唯一 `id` 保证重试幂等；每条消息必填 `author.type`（`agent` 或 `human`），可选携带结构化 `data`、因果游标 `as_of_request` / `as_of_cursor`、用户状态 `context`（`locale`、`time_zone`、`user_available`）及 `extensions`；支持创建关联父会话的 `Direct Conversation`（`parent_conversation_id`）让用户直接与企业对话。
- **任务覆盖与技能索引（`spec.md` §9）**：
  - `GET {tasks.endpoint}` 返回 `excluded_tasks`（明确不通过协议提供的任务及替代方式 `alternative`）、`feedback.endpoint`（上报无法完成的任务，不含个人隐私数据）以及遵循 Agent Skills 发现提案（`0.2.0` schema，带 `sha256:` 摘要校验）的 `skill_index`。明确声明企业发布的 Skill 属于不可信企业内容，不授予任何权限，除非用户或配置显式允许否则禁止执行其中的脚本。
- **扩展机制与 `operations` 扩展（`docs/1.0/extensions.md` & `extensions/operations.md`）**：
  - 已定义 6 个官方扩展：`browser-control`（v1，网页步骤交还用户控制）、`disclosures`（v1，监管/过敏原等必读声明分离标注）、`links`（v1）、`mediated-sign-in`（v1，向尚未支持 OAuth 的企业代填用户凭据的过渡方案）、`operations`（v3）、`ucp`（v1，对接 Universal Commerce Protocol）。
  - **`operations`（v3）流程**：当操作具有业务副作用时，企业先拒绝执行并返回 `operation` 对象（含 `operation_id`、`revision`、禁渲染链接/图片的纯文本/基础 Markdown `summary`、JSON `terms`、`expires_at`）：API 返回 HTTP 403 `{"error": "approval_required", "operation": ...}`，MCP 返回 `isError: true` + `structuredContent.operation`，对话放入 `extensions.operations.operation`。个人 Agent 由用户确认（或按用户事先对明确条款的指令自动确认）后，携带绑定 `operation_id` 与 `revision` 的 `approval` 重发原请求；企业保证**仅按所批准的精确条款执行**，且**相同批准的重试至多执行一次（at most once）**。
- **安全与隐私考虑（`spec.md` §10）**：
  - §10.1 防跨企业提示词注入（企业返回内容一律视作数据而非指令，不得因企业 A 的内容去操作企业 B 或向企业 B 发送数据）；
  - §10.2 密钥隔离（遵循 `draft-ietf-wimse-aims` §8，访问令牌、刷新令牌、Session JWT、私钥、授权码、PKCE `code_verifier`、设备码及一次性验证码严禁进入模型上下文）；
  - §10.7 盲签名（Blind signing）：支持通过 RFC 9474 RSABSSA-SHA384-PSS-Deterministic（`PS384`）对客户端断言与委托凭证做盲签名，使 Personal Agent 服务端无法得知用户连接了哪些企业。

## 验证记录

- 已抓取并逐章核对 `personalagentprotocol.org` 的 `llms.txt`、`introduction.md`、`1.0/spec.md`、`1.0/extensions.md` 与 `1.0/extensions/operations.md`。
- 本次未运行站点提供的社区 Demo 或 Company Implementation Kit 校验器，协议请求与响应格式均直接依据 v1.0 规范正文核对。
- 手绘配图 `raw/assets/poppy-delegated-keys-architecture.png` 根据规范 §4.1、§5.1、§5.2 的 `client_id` 主密钥、短期委托密钥（`poppy_dlg`）与 `Poppy-Session` JWT 签名关系绘制，已逐项核对中英文标签与箭头方向。
- 整理页：[[wiki/topics/ai/personal-agent-protocol|Personal Agent Protocol（Poppy）]]、[[wiki/topics/ai/personal-agent|Personal Agent 与 Super-agent]]。
