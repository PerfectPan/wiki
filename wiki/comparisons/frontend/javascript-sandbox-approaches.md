---
title: JavaScript 沙箱方案对比
description: 把 JS 关起来跑的十几种方案怎么选：按隔离了什么分三档（同线程同堆只隔全局、独立的堆、独立线程或进程），再看能不能同步调用、是不是按防恶意代码设计；覆盖微前端框架、SES/Endo、同源和跨域 iframe、near-membrane、ShadowRealm、LWS、vm2、isolated-vm、workerd、QuickJS-wasm、Web Worker、Caja、realms-shim 和 es-membrane
type: comparison
category: frontend
created: 2026-10-22
updated: 2026-10-22
timestamp: 2026-10-22
tags:
  - sandbox
  - javascript
  - realm
  - micro-frontend
  - security
source_refs:
  - wiki/topics/frontend/near-membrane.md
  - raw/sources/near-membrane.md
  - https://github.com/endojs/endo/tree/master/packages/ses
  - https://github.com/tc39/proposal-shadowrealm
  - https://github.com/umijs/qiankun
  - https://github.com/jd-opensource/micro-app
  - https://github.com/Tencent/wujie
  - https://github.com/patriksimek/vm2
  - https://github.com/laverdet/isolated-vm
  - https://github.com/cloudflare/workerd
  - https://github.com/justjake/quickjs-emscripten
  - https://www.figma.com/blog/an-update-on-plugin-security/
  - https://github.com/googlearchive/caja
  - https://github.com/Agoric/realms-shim
  - https://github.com/ajvincent/es-membrane
resource:
  - wiki/topics/frontend/near-membrane.md
  - raw/sources/near-membrane.md
  - https://github.com/endojs/endo/tree/master/packages/ses
  - https://github.com/tc39/proposal-shadowrealm
  - https://github.com/umijs/qiankun
  - https://github.com/jd-opensource/micro-app
  - https://github.com/Tencent/wujie
  - https://github.com/patriksimek/vm2
  - https://github.com/laverdet/isolated-vm
  - https://github.com/cloudflare/workerd
  - https://github.com/justjake/quickjs-emscripten
  - https://www.figma.com/blog/an-update-on-plugin-security/
  - https://github.com/googlearchive/caja
  - https://github.com/Agoric/realms-shim
  - https://github.com/ajvincent/es-membrane
---
# JavaScript 沙箱方案对比

## 一段话结论

先想清楚防什么。只防前端应用互相踩全局，用 qiankun、micro-app、wujie；要第三方组件同步改宿主 DOM、平台管它能碰什么，走 [[wiki/topics/frontend/near-membrane|near-membrane]]（LWS）路线；要防恶意代码，A 档（同线程同堆）里只有 SES 按安全边界设计，而且 A 档都挡不住死循环和侧信道。更稳的是 B 档独立堆（QuickJS-wasm、单独进程里的 isolated-vm），或 C 档独立线程、进程（Worker、跨域 iframe、容器 / VM），代价是只能异步发消息。ShadowRealm 停在 Stage 2.7，别指望。

![米色底手绘风格示意图：JS 沙箱按隔离了什么分三档。A 同线程同堆只隔全局或内置对象：同 Realm 换全局、SES Compartment、同源 iframe、near-membrane、ShadowRealm；B 独立的堆：isolated-vm、workerd、QuickJS 编译成 wasm；C 独立线程或进程只能异步发消息：Web Worker、跨域 iframe、独立进程容器或 VM。每项标出能否同步调用、是否按防恶意代码设计，橙色标签表示按防恶意代码设计](../../../raw/assets/js-sandbox-isolation-layers.png)

三档是分组，不是强弱排名：SES 和 near-membrane 同在 A 档，前者按 ocap 安全边界设计，后者明说只保完整性。

## 对比表

资料核对于 2026-10-21。「—」表示资料里没法确认。

| 方案 | 档 | 怎么隔 | 同步调用 | 按防恶意代码设计 | 状态 |
| --- | --- | --- | --- | --- | --- |
| qiankun、micro-app | A | 同一个 Realm，只代理一个假 `window`；micro-app 也能借 iframe 跑 | 可以 | 否，只管应用共存 | qiankun npm 2.10.16，3.0 rc；micro-app 1.0.0-rc.32 |
| wujie | A | iframe 跑 JS，shadow DOM 放 DOM | 可以 | 否，只管应用共存 | 2.1.0 |
| SES / Endo | A | 同一个 Realm，`lockdown()` 冻结共享的内置对象，Compartment 各有全局，能力只经 `globals` 交进去 | 可以 | 是（ocap；不防 DoS、内存耗尽） | 活跃，`ses` 2.3.0 |
| 同源 iframe | A | 新 Realm，自带 DOM，父页面能直接摸到它的 `window` | 可以 | 否；单独用挡不住（realms-shim 的教训） | 浏览器原生 |
| near-membrane | A | iframe / Node `vm` 造新 Realm，加双向 Proxy membrane；DOM 共享，危险能力走 distortion | 可以 | 否，只保完整性 | 2026-09-18 归档，0.19.1 |
| LWS | A | 每个 namespace 一个沙箱，用 distortion 控制（推断底层是 near-membrane） | 可以 | 是，Salesforce 平台安全 | 现行；取代了用 secure wrapper 的 Lightning Locker |
| vm2 | A | Node `vm` 新 Realm，加双向 Proxy | 可以 | README：不能当唯一防线 | 2023 停更，2025-10 恢复；3.12.2 |
| ShadowRealm | A | 引擎原生的新 Realm，只过原始值和函数，没有 DOM | 可以 | 否，只保完整性 | Stage 2.7，没有浏览器默认开启 |
| Miller membrane、es-membrane | A | 同一个 Realm 里两张对象图之间的 Proxy membrane | 可以 | 否，是语言模式 / 构建工具 | harmony-reflect 最后 push 2024-01；es-membrane v2 重写中 |
| realms-shim、Caja | A | 同页执行加作用域 Proxy / 改写驯化 | 可以 | 是，但都已作废（realms-shim 2019 被攻破，Caja 2021 归档） | 不要用 |
| isolated-vm | B | Node 里的独立 V8 isolate，只能拷贝或传 `Reference` 句柄 | 可以（也有异步 API） | README：不会自动安全，建议放单独进程 | 维护模式，7.0.1 |
| workerd | B | 每个 Worker 一个 V8 isolate，靠 binding / RPC 通信 | — | 否，README 说要外层 VM | 活跃 |
| QuickJS → wasm | B | 另一个 JS 引擎，独立的 wasm 内存；不放进 Worker 就还在主线程 | 可以 | 是（Figma 插件；quickjs-emscripten 称可安全跑不可信 JS） | quickjs-emscripten 0.32.0 |
| Web Worker | C | 独立线程和事件循环，没有 DOM | 不行，只能 `postMessage` | — | 浏览器原生 |
| 跨域 iframe | C | 同源策略隔开；Site Isolation 下跨站 iframe 进单独进程（OOPIF） | 不行，只能 `postMessage` | 是 | 浏览器原生 |
| 独立进程 / 容器 / VM | C | 操作系统级隔离 | 不行 | 是 | — |

## 怎么选

- **几个前端应用同页共存，别互相污染**：qiankun、micro-app、wujie。接入便宜，但不防恶意代码。
- **第三方组件要同步操作宿主 DOM，平台控制它能碰什么**：near-membrane 路线（LWS）。安全全押在 Proxy 拦得对不对上；near-membrane 已归档，要自己维护。
- **互不信任的插件，接受先冻结整个运行环境**：SES / Endo。改内置原型的库可能跑不起来。
- **浏览器里跑不可信插件**：QuickJS-wasm（quickjs-emscripten）；怕卡主线程就放进 Worker。宿主 API 要一个个注册，句柄要手动释放。
- **Node 里跑不可信代码**：isolated-vm 放单独进程，或者直接容器 / VM。别把 `Reference` 交给不可信代码。
- **能接受全异步**：Worker 或跨域 iframe，浏览器原生的边界最省心。
- **想等标准**：ShadowRealm 停在 Stage 2.7，Firefox 已删实现，Node 也在提议删。

## 名词

- **Realm**：一套独立的全局对象和内置对象；两个 Realm 可以在同一个线程、同一个堆里。
- **intrinsics（内置对象）**：`Object`、`Array`、`JSON` 这些语言自带的对象，每个 Realm 一套。
- **membrane（膜）**：对象过边界时都包一层 Proxy，拿到的是代理不是原对象。
- **身份保持**：同一个对象来回穿过边界还是 `===`；做不到的话，靠 `===`、`WeakMap` 认对象的代码会乱。
- **distortion**：过边界时把值换成受限版本，比如把 `document.cookie` 的 getter 换掉。
- **lockdown / harden**：SES 冻结全部内置对象 / 冻结单个对象图。
- **ocap（对象能力）**：拿到对象引用就有权限，没有引用就没有；控制权限就是控制交出去哪些对象。
- **callable boundary**：只让原始值和函数过的边界，ShadowRealm 用的就是它。
- **V8 isolate**：V8 里独立的运行时实例，有自己的堆，彼此拿不到对象引用。
- **OOPIF**：out-of-process iframe，Site Isolation 下跨站 iframe 跑在单独的渲染进程里。
- **逃逸**：沙箱代码绕过边界拿到宿主对象，同堆的 Proxy 方案漏拦一个 trap 就可能发生。

## 来源指针

- [[wiki/topics/frontend/near-membrane|near-membrane]]：实现细节、ShadowRealm 和归档
- `raw/assets/js-sandbox-isolation-layers.png`：脚本（matplotlib）按本页三档画的米色底手绘风格示意，不是任何项目的官方素材
- `raw/sources/near-membrane.md`：各方案的核对记录、日期和待确认项
- [SES](https://github.com/endojs/endo/tree/master/packages/ses)、[Compartments 提案](https://github.com/tc39/proposal-compartments)
- [ShadowRealm 提案](https://github.com/tc39/proposal-shadowrealm)、[chromestatus](https://chromestatus.com/feature/5638053476433920)
- [qiankun](https://github.com/umijs/qiankun)、[micro-app](https://github.com/jd-opensource/micro-app)、[wujie](https://github.com/Tencent/wujie)
- [vm2](https://github.com/patriksimek/vm2)、[isolated-vm](https://github.com/laverdet/isolated-vm)、[workerd](https://github.com/cloudflare/workerd)
- [quickjs-emscripten](https://github.com/justjake/quickjs-emscripten)、Figma：[How we built the Figma plugin system](https://www.figma.com/blog/how-we-built-the-figma-plugin-system/)、[An update on plugin security](https://www.figma.com/blog/an-update-on-plugin-security/)
- [Caja](https://github.com/googlearchive/caja)、[realms-shim](https://github.com/Agoric/realms-shim)、[es-membrane](https://github.com/ajvincent/es-membrane)、[harmony-reflect membrane 示例](https://github.com/tvcutsem/harmony-reflect/blob/master/examples/membrane.js)
- LWS：[How LWS Compares to Lightning Locker](https://developer.salesforce.com/docs/platform/lightning-components-security/guide/get-started-compare-lws-locker.html)、[LWS 架构](https://developer.salesforce.com/docs/platform/lightning-components-security/guide/lws-architecture.html)
