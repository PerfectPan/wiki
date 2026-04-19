---
title: SSO
type: topic
category: architecture
status: seed
created: 2026-04-12
updated: 2026-04-19
tags:
  - sso
  - auth
  - cas
source_refs:
  - raw/sources/SSO.md
---
# SSO

- 单点登录。SSO用于在一处系统中登录， 切换到其他系统时，不必再次输入用户名密码。
- 问题：多应用切换中，会面临 cookie 跨域和 session 共享的问题
- CAS
	- 名词：
		- ST：Service Ticket
	- 访问 APP1 系统
		- 用户访问 APP1 系统，APP1 系统是需要登录的，但用户现在没有登录
		- 跳转到 CAS server，即 SSO 登录系统。SSO 系统也没有登录，弹出用户登录页
		- 用户填写用户名、密码，SSO 系统进行认证后，将登录状态写入 SSO 的 Session，浏览器（Browser）中写入 SSO 域下的 Cookie。【此处的 Cookie 可以确保不用重复登录 SSO 系统】
		- SSO 系统登录完成后会生成一个 ST，然后跳转到 APP1 系统（302 重定向），同时将 ST 作为参数传递给 APP1 系统（挂在 url 的 query 上）
		- APP1 系统拿到 ST 后，从后台向 SSO 发送请求，验证 ST 是否有效
		- 验证通过后，APP1 系统将登录状态写入 Session 并设置 APP1 域下的 Cookie。【仅仅是在 APP1 域下的 Cookie】
	- 访问 APP2 系统
		- 用户访问 APP2 系统，没有登录，跳转到 SSO
		- 由于 SSO 已经登录了，不需要重新登录认证
		- SSO 生成 ST，浏览器跳转到 APP2 系统，并将 ST 作为参数传递给 APP2
		- APP2 拿到 ST，服务端访问 SSO，验证 ST 是否有效
		- 验证成功后，APP2 将登录状态写入 Session，并在 APP2 域下写入 Cookie
	- SSO，APP1 和 APP2 在不同的域下，它们之间的 Session 不应该是的共享的，这样可以更加保证用户信息安全

## Source Pointers

- `raw/sources/SSO.md`
