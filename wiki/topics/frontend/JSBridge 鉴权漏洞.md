---
title: JSBridge 鉴权漏洞
type: topic
category: frontend
status: seed
created: 2026-04-25
updated: 2026-04-25
tags:
  - jsbridge
  - security
  - auth
  - payment
source_refs:
  - http://myjsapi.alipay.com/jsapi/native/trade-pay.html
---
# JSBridge 鉴权漏洞

## 摘要

一类典型 JSBridge 安全问题：三方页面如果能直接调用高权限 JSAPI，而调用来源又缺少严格校验，就可能越过原本的业务流程边界，触发支付、确认收货等敏感行为。

## 关键点

- 这类问题的核心不在“有没有 JSBridge”，而在“谁可以调用哪些 JSAPI”。
- 如果桥接层只暴露了能力，却没有把调用来源、安全域名和业务上下文校验收紧，跳转到三方页面后仍可能触发原本只应在受信任场景里调用的 API。
- 这类问题在支付场景下尤其危险，因为桥接接口一旦直接影响订单状态、收货状态或支付确认，就不只是普通前端漏洞，而是业务安全漏洞。
- 这条记录给出的最实用结论是：高权限 JSAPI 不该只靠前端流程“默认可信”，而应该有明确的调用边界，例如白名单域名、上下文校验和更细的权限隔离。

## 相关页面

- [[OAuth]]
- [[应用层通信的可靠性边界]]

## 来源指针

- [tradePay JSAPI](http://myjsapi.alipay.com/jsapi/native/trade-pay.html)
