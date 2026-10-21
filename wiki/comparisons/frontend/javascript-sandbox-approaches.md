---
title: JavaScript 沙箱方案对比
description: 按隔离单位、跨界方式、身份保持、能力控制和安全定位对比 near-membrane、SES/Endo、ShadowRealm、qiankun / micro-app / wujie、LWS、vm2、isolated-vm、workerd、QuickJS-wasm、Caja、realms-shim 和 es-membrane，并按需求给出选择
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

## 当前结论

各方案最大的区别是**隔离单位**，也就是被隔离的代码关在哪一层里跑。层级越往下隔得越彻底，代价也越大：

1. **同一个 Realm，只换全局对象**：qiankun 的 `ProxySandbox`、micro-app 的 with 模式。内置对象共享，主要防全局变量和样式互相污染，不防恶意代码。
2. **同一个 Realm，冻结后共享**：SES / Endo 的 Compartment。不包装对象，靠 `lockdown()` 冻结所有内置对象，是 ocap（object capability，对象能力）意义上的安全边界。
3. **新 Realm 加同步、保持身份的对象 membrane**：[[wiki/topics/frontend/near-membrane|near-membrane]]、vm2。Realm 是一套独立的全局对象和内置对象（有自己的 `Object`、`Array`、`window`），但仍在同一个线程、同一块内存里，靠 Proxy 拦截。好处是能同步互相调用、兼容性最好、能直接操作宿主 DOM；坏处是一旦拦漏，沙箱就直接拿到宿主对象。
4. **新 Realm，只开 callable boundary**：ShadowRealm 提案。只有原始值和函数能跨界，普通对象过不去。
5. **独立的 V8 isolate**：isolated-vm、workerd。独立的堆，对象拿不到对面的引用，只能拷贝数据或传句柄。
6. **另一个 JS 引擎**：QuickJS 编译成 wasm，例如 Figma 插件和 quickjs-emscripten。对象表示完全不同，不存在「同一个对象」。

要跑不可信代码，近几年的趋势是独立 isolate 或 wasm，再加进程或虚拟机级别的隔离：同进程、同堆的 Proxy membrane 一直是逃逸漏洞的高发区，realms-shim 在 2019 年被攻破，vm2 至今在修 GHSA，near-membrane 最后几次提交也在补 trap 的边界情况。

## 备选项

资料核对日期 2026-10-21。状态里只写到日期的按 UTC 记。

| 方案 | 隔离单位 | 跨界方式 | 身份保持 | 安全定位 | 状态 |
| --- | --- | --- | --- | --- | --- |
| near-membrane | 新 Realm（浏览器同源 iframe，Node `vm`），同线程 | 双向 Proxy membrane，shadow target、懒投影、live / static；blue 侧首次跨界时做 distortion | 是，双向指针缓存，回程解包，不会 proxy 套 proxy | 只保证完整性，安全靠上层 distortion | 2026-09-18 归档，最终 0.19.1 |
| Miller / tvcutsem membrane | 同 Realm 的两张对象图 | Proxy 递归包装，可撤销 | 是，WeakMap 一一映射 | 语言模式和示例 | harmony-reflect 最后 push 2024-01-15 |
| es-membrane | 同 Realm 的多张对象图（wet / dry / damp） | Proxy + ProxyMapping，可配置 distortion | 是 | 构建工具，未声明是安全边界（归纳） | v2 重写中；npm 停在 0.9.0（2018） |
| SES / Endo | 同 Realm 的 Compartment，共享已冻结的内置对象 | 直接共享引用（先 `lockdown` / `harden`），能力靠 `globals` 交入 | 天然成立（不包装） | ocap 安全边界，不防 DoS 和内存耗尽 | 活跃；`ses` 2.3.0（2026-08-13）；Compartments 提案 Stage 1 |
| Agoric realms-shim | 新 Realm（同源 iframe）+ `with(scopeProxy)` | 直接引用 + 作用域 Proxy | 部分 | 想做安全边界，已被攻破 | README 标为 OBSOLETE / INSECURE |
| ShadowRealm | 引擎原生的新 Realm | callable boundary | 对象不跨界；函数每次跨界包一层新 wrapper（按规范语义推断，未逐行核对） | 隔离原语，不是现成沙箱 | Stage 2.7；Firefox 2026-02 移除实现，Chrome 原型阶段需开关，WebKit 需开关（待确认） |
| Figma 插件 | wasm 里的 QuickJS | 句柄 + 拷贝，宿主 API 显式注入 | 无跨堆身份 | 安全边界 | 2019-09-25 起采用；现状待确认 |
| quickjs-emscripten | wasm 里的 QuickJS VM | `QuickJSHandle`，手动 `dispose()` | 无跨堆身份 | README 称可安全执行不可信 JS | 活跃；0.32.0（2026-02-16） |
| qiankun | 同 Realm，假 window（Proxy 或快照） | 共享内置对象，只代理 window | 不涉及 | 应用共存隔离，不是安全边界（归纳） | npm 2.10.16（2023-11）；3.0 处于 rc |
| micro-app | 同 Realm（with + Proxy）或 iframe Realm | 代理 window；iframe 模式给 DOM 打补丁转发 | 不保证（待确认） | 应用共存隔离 | 1.0.0-rc.32（2026-06-25） |
| wujie | iframe Realm 跑 JS，shadow DOM 放 DOM | 框架代理或转发 DOM 访问（待确认） | 不保证（待确认） | 应用共存隔离 | 2.1.0（2026-06-15） |
| Google Caja | 改写和驯化后同页执行（ES5 SES + Domado） | taming membrane | 待确认 | ocap 安全边界 | 2021-01-31 归档，不再出安全补丁 |
| Lightning Locker | 同 Realm + secure wrapper | `SecureWindow` 等包装对象 | 否，拿到的是包装对象 | Salesforce 平台安全 | 被 LWS 取代（时间表待确认） |
| LWS | 每个 namespace 一个沙箱 | distortion（推断建立在 near-membrane 之上） | 是（官方文档：iframe 身份两侧一致） | Salesforce 平台安全 | 现行方案 |
| vm2 | Node `vm` context（新 Realm，同进程） | 双向 Proxy bridge（常识背景，未逐行核对） | 是（常识背景） | README 称不能作为唯一防线 | 2023 停更，2025-10 恢复维护；3.12.2（2026-09-08） |
| isolated-vm | 独立 V8 isolate | transferable：拷贝、`Reference`、`ExternalCopy` | 否，只有句柄 | 比同堆方案强，但 README 说不会自动安全 | 维护模式；7.0.1（2026-08-05） |
| Cloudflare workerd | 每个 Worker 一个 V8 isolate | capability binding / RPC（细节待确认） | 否 | README 称「not a hardened sandbox」，需外层 VM | 活跃 |

## 取舍分析

| 如果需要 | 优先选 | 因为 | 需要承担的代价 |
| --- | --- | --- | --- |
| 多个前端应用在同一页面共存，互不污染全局变量和样式 | qiankun、micro-app、wujie | 只换全局对象或借 iframe 跑 JS，接入成本低 | 不防恶意代码；iframe 模式有跨 Realm 的 `instanceof` 问题 |
| 第三方组件要像原生一样直接操作宿主 DOM，同时由平台控制它能碰什么 | near-membrane 路线（LWS） | 同步、保持身份的 membrane 兼容性最好，distortion 可以按值替换 API | 安全全押在 Proxy 语义正确；near-membrane 已归档，需自行维护 |
| 跑互不信任的插件或第三方代码，接受冻结整个运行环境 | SES / Endo | 不包装对象就没有身份断裂，冻结后共享引用是安全的 | 要求整个应用先 `lockdown()`；依赖修改内置原型的库可能跑不起来（常识背景，本次没有逐个验证） |
| 在 Node 里跑不可信代码 | isolated-vm 放在单独进程里，或容器 / VM | 独立的堆，对象引用过不去 | 只能拷贝或传句柄，异步调用多；`Reference` 泄露给不可信代码仍可逃逸 |
| 浏览器里跑不可信插件，安全优先于性能 | QuickJS-wasm（quickjs-emscripten） | 对象表示完全不同，不可能发生对象混淆 | 解释执行比 V8 慢（常识背景，未测）；宿主 API 都要手动注册，句柄要手动释放 |
| 想要标准化、无需库的隔离原语 | 关注 ShadowRealm | callable boundary 从根上消除对象混淆 | 停在 Stage 2.7，Firefox 已移除实现，目前不能依赖 |

## 推荐理由

先按威胁模型选层：只防应用之间互相干扰，用微前端框架；要防恶意代码，优先独立 isolate、wasm 或进程 / 虚拟机隔离，不要只靠同堆的 Proxy membrane。near-membrane 的价值是让 LWS 这类平台以接近原生的兼容性，给每个 namespace 一个可以被 distortion 改写的虚拟 `window`；它和 SES 走相反的路：SES 共享但冻结，near-membrane 每个沙箱一套内置对象再用 membrane 连起来。

near-membrane 两侧只交换 37 个函数、对象用指针闭包表示，结构上已经接近「在 callable boundary 之上重建完整 membrane」，这是本页对它与 ShadowRealm 关系的解读，不是项目官方说法。

## 来源指针

- [[wiki/topics/frontend/near-membrane|near-membrane]]：near-membrane 的实现细节、修复历史和归档
- `raw/sources/near-membrane.md`：各方案的核对记录、日期和待确认项
- [SES](https://github.com/endojs/endo/tree/master/packages/ses)、[Compartments 提案](https://github.com/tc39/proposal-compartments)
- [ShadowRealm 提案](https://github.com/tc39/proposal-shadowrealm)、[chromestatus](https://chromestatus.com/feature/5638053476433920)
- [qiankun](https://github.com/umijs/qiankun)、[micro-app](https://github.com/jd-opensource/micro-app)、[wujie](https://github.com/Tencent/wujie)
- [vm2](https://github.com/patriksimek/vm2)、[isolated-vm](https://github.com/laverdet/isolated-vm)、[workerd](https://github.com/cloudflare/workerd)
- [quickjs-emscripten](https://github.com/justjake/quickjs-emscripten)、Figma：[How we built the Figma plugin system](https://www.figma.com/blog/how-we-built-the-figma-plugin-system/)、[An update on plugin security](https://www.figma.com/blog/an-update-on-plugin-security/)
- [Caja](https://github.com/googlearchive/caja)、[realms-shim](https://github.com/Agoric/realms-shim)、[es-membrane](https://github.com/ajvincent/es-membrane)、[harmony-reflect membrane 示例](https://github.com/tvcutsem/harmony-reflect/blob/master/examples/membrane.js)
- LWS：[How LWS Compares to Lightning Locker](https://developer.salesforce.com/docs/platform/lightning-components-security/guide/get-started-compare-lws-locker.html)、[LWS 架构](https://developer.salesforce.com/docs/platform/lightning-components-security/guide/lws-architecture.html)
