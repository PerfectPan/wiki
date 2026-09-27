# 双 Token 流程图生成记录

- 日期：2026-09-27
- 工具：内置 imagegen
- 图片：`raw/assets/2026-09-27-dual-token-lifecycle.png`
- 用途：解释同源 Web 示例中的登录、业务访问、刷新与退出。
- 本文件是生成记录，不是协议事实来源；技术依据见 Wiki 页面的 RFC 与 OWASP 链接。
- 已检查中文文字、箭头方向、RT 轮换及退出后旧 AT 的有效期限制。

## 完整提示词

```text
Use case: infographic-diagram.
Create one polished, easily understood Chinese educational infographic for a developer wiki. Landscape approximately 2400x1600, white background, large legible Chinese sans-serif typography, restrained blue for AT and amber for RT, flat icons, clear arrows, generous whitespace. No decorative slogans, no watermark. Technical accuracy and Chinese text legibility are essential.

Title exactly: "双 Token：AT 访问，RT 续期"
Subtitle exactly: "同源 Web 应用示例 · AT 为 JWT · RT 为随机字符串"

At top show two simple labeled token cards:
Blue "AT / access token" with "短期有效 · 调业务接口"
Amber "RT / refresh token" with "较长期有效 · 只向认证服务换新"

Main layout is four large numbered panels, read left to right then next row, each shows browser on the left and server on the right, with straight directional arrows and no crossing lines:
1. "登录" — browser -> authentication server arrow "POST /auth/login". Server -> browser arrow "AT + RT". Caption "AT 存内存；RT 放 HttpOnly Cookie". A small server storage icon caption "服务端保存 RT 摘要与会话状态".
2. "访问业务" — browser -> business API arrow "Authorization: Bearer AT". API caption "校验签名、有效期与权限". Bottom caption "RT 不随业务请求发送".
3. "刷新" — browser -> authentication server arrow "POST /auth/refresh + RT". Server -> browser arrow "新 AT + 新 RT". Caption "原子轮换：旧 RT 作废，新 RT 生效". Small text "刷新需要查询服务端状态".
4. "退出" — browser -> authentication server arrow "POST /auth/logout". Server caption "撤销会话的刷新能力". Browser caption "清除 AT 与 RT Cookie". Bottom caption "仅本地验证时，旧 AT 可用至过期".

Bottom highlighted note exactly: "想让旧 AT 立即失效？业务请求还需检查撤销或会话状态。"
Small footer exactly: "接口路径为设计示例；双 Token 不等于完全无状态。"

Do not add lifetime numbers, do not depict RT going to business API, do not suggest JWT signatures encrypt contents, and do not depict logout as instantly invalidating offline-validated AT. Every label should be readable at ordinary screen width. Return a finished bitmap illustration.
```
