---
title: near-membrane
description: Salesforce 给 Lightning Web Security 用的 JS 沙箱库：在同源 iframe 或 Node vm 里造一个新 Realm，用双向 Proxy membrane 把宿主对象懒投影进去；先从零讲它防什么、不防什么，再讲指针协议、写时复制、distortion，和 TC39 ShadowRealm 的关系，以及 2026-09-18 归档的事实和推断
type: topic
category: frontend
created: 2026-10-22
updated: 2026-10-22
timestamp: 2026-10-22
tags:
  - sandbox
  - javascript
  - proxy
  - realm
  - security
source_refs:
  - raw/sources/near-membrane.md
  - https://github.com/salesforce/near-membrane
  - https://github.com/salesforce/near-membrane/commit/19685c36d267071cc70c2876925f8a020361fe3d
  - https://intel.aikido.dev/cve/AIKIDO-2026-167438
  - https://developer.salesforce.com/docs/platform/lightning-components-security/guide/lws-architecture.html
  - https://github.com/tc39/proposal-shadowrealm/blob/main/explainer.md
  - https://github.com/nodejs/node/pull/65650
resource:
  - raw/sources/near-membrane.md
  - https://github.com/salesforce/near-membrane
  - https://github.com/salesforce/near-membrane/commit/19685c36d267071cc70c2876925f8a020361fe3d
  - https://intel.aikido.dev/cve/AIKIDO-2026-167438
  - https://developer.salesforce.com/docs/platform/lightning-components-security/guide/lws-architecture.html
  - https://github.com/tc39/proposal-shadowrealm/blob/main/explainer.md
  - https://github.com/nodejs/node/pull/65650
---
# near-membrane

## 摘要

[salesforce/near-membrane](https://github.com/salesforce/near-membrane)（MIT，npm 作用域 `@locker/`）是一个同步的 JavaScript 沙箱库。它在同一个线程里再造一个 Realm（一套独立的全局对象和内置对象：浏览器里借同源 iframe，Node 里用 `vm`），宿主的东西都用 Proxy 懒投影进去。沙箱代码以为自己跑在顶层，改动却只落在沙箱里；宿主还能用 `distortionCallback` 把任何跨界的值换掉。

仓库描述是「JavaScript Near Membrane Library that powers Lightning Locker Service」，安全修复都带 `[LWS]` 标签，可以推断它是 Salesforce Lightning Web Security（LWS）的底层；LWS 官方文档没有点名它。库自己声明「提供完整性，不提供安全保证」。2026-09-18 17:59（北京时间）归档，最后的 npm 版本是 0.19.1。

本页依据 `main` 最后的提交 `19685c3`；源码和 README、`DESIGN_DOCUMENT.md` 不一致时以源码为准。

## 从零理解：它到底防什么

### blue 和 red

宿主一侧叫 **blue**，沙箱一侧叫 **red**。打个比方：blue 是你家，red 是给客人新装修的一间客房，里面的家具（`Object`、`Array`、`Array.prototype` 这些内置对象）全是新买的。客人怎么改客房的家具都改不到你家。客人要用你家的东西（`document`、`fetch`、你挂在 `window` 上的配置），你不把真东西搬过去，只隔着玻璃窗递一个「遥控器」（Proxy）。这道窗就是 membrane。递的时候你还能偷偷换掉（distortion），比如把 `alert` 换成只打日志的版本。

![米色底手绘风格示意图：左边 blue Realm 是宿主页面的 JS 世界，右边 red Realm 有自己的一套内置对象，中间的虚线是 membrane，上面有 distortion；下方示例展示沙箱改 Array.prototype.push 只影响 red](../../../raw/assets/near-membrane-blue-red-realms.png)

代码里 red 一侧也叫 shadow realm（变量 `IS_IN_SHADOW_REALM`），和下文 TC39 的 ShadowRealm 提案不是一回事。

### 「过膜」什么时候发生

不是启动时一次性把宿主全拷过去，而是 red 代码**碰到** blue 的东西时才过膜，一次一个值：

- 读全局：red 第一次读 `window.fetch`、`document`，才去 blue 取，取回来的是 Proxy。
- 顺着 Proxy 往下读：`document.body` 是在 `document` 的 Proxy 上读属性，结果 `body` 也过膜，变成另一个 Proxy。
- 调函数：red 调 blue 函数时，参数从 red 过膜到 blue，返回值再从 blue 过膜回来；抛出的错误也一样。

### 一个对象只对应一个 Proxy：身份映射

每一侧都有一张 WeakMap（`proxyPointerCache`），记着「我这边的原对象 ↔ 对面给它建的 Proxy」：

- 同一个 blue 对象，不管过膜多少次，red 拿到的都是同一个 Proxy，所以 `document.body === document.body` 在 red 里成立。
- 这个 Proxy 传回 blue 时，查表解包成原对象，不会出现「Proxy 套 Proxy」，blue 侧 `===` 也成立。

没有这张表，同一个对象过两次膜就是两个互不相等的 Proxy，靠 `===`、`Map`、`WeakMap` 认对象的代码全会乱。

### 为什么两个方向都要包

只包一个方向不够。假设 blue 直接拿到一个 red 的原始对象 `redObj`：

- `redObj instanceof Object` 是 `false`，因为它的原型是 red 那套 `Object.prototype`。
- `redObj.constructor.constructor('return this')()` 拿到的是 red 的 `Function`，执行后返回 red 的全局对象。

反过来更危险：red 直接拿到 blue 的原始对象，同一招就拿到 blue 的全局对象，沙箱等于没有。所以两个方向的值都要过膜包成 Proxy。near-membrane 还把两边的 `Object.prototype`、`Array.prototype` 等配成对（`link`），过膜时直接互换，`instanceof` 和原型链就能对上。

### 隔离了什么，没隔离什么

| 东西 | 怎么处理 |
| --- | --- |
| JS 内置对象（`Object`、`Array`、`JSON`、`Map`……） | red 用自己的一套，随便改不影响 blue |
| 宿主的全局变量（`window.config`、`fetch`……） | 懒投影成 Proxy；red 第一次写时复制到 red 本地，宿主不变 |
| DOM | **故意共享**：Lightning 组件要渲染到宿主页面上，所以 red 里的 `document` 就是宿主 `document` 的 Proxy，`appendChild` 会真的改宿主页面 |
| 危险能力（cookie、`alert`、某些 getter） | 宿主用 distortion 在过膜时换成受限版本 |

### 同一个线程、同一个事件循环、同一个堆

red 和 blue 跑在同一个线程、同一个事件循环里，用同一个堆。同源 iframe 本来就和父页面共用事件循环；跨域 iframe 在 Site Isolation 下可能进单独的进程（OOPIF），和父页面只能 `postMessage`。near-membrane 要同步互调，只能用同源 iframe。

后果：red 里一句 `while (true) {}` 就能卡死整个页面；red 疯狂分配内存，宿主一起受影响；计时类的侧信道也挡不住。这就是「完整性，不是安全」的意思：它保证 red 改不坏 blue 的对象，不保证 red 没法捣乱。

### 例子：一个爱打补丁的第三方脚本

```js
// 第三方组件，喜欢改全局
const thirdParty = `
  Array.prototype.includes = () => true;
  JSON.parse = () => ({});
  window.fetch = () => Promise.reject(new Error('vendor fetch'));
  console.log(document.cookie);

  const div = document.createElement('div');
  div.textContent = '第三方组件';
  document.body.appendChild(div);
`;
```

**不用沙箱**（直接 `(0, eval)(thirdParty)`）：宿主的 `[1].includes(2)` 变成 `true`，`JSON.parse` 坏了，`fetch` 全部失败，cookie 被读走。

**用沙箱**：

```js
import createVirtualEnvironment from '@locker/near-membrane-dom';

const { get: getCookie, set: setCookie } =
    Object.getOwnPropertyDescriptor(Document.prototype, 'cookie');
const distortions = new Map([
    [getCookie, () => ''],      // 沙箱读到空字符串
    [setCookie, () => {}],      // 沙箱写了也没用
]);

const env = createVirtualEnvironment(window, {
    distortionCallback(v) {
        return distortions.get(v) ?? v;
    },
});
env.evaluate(thirdParty);

// 回到宿主
[1].includes(2);                       // false：red 改的是自己那套 Array.prototype
JSON.parse('{"a":1}');                 // { a: 1 }：JSON 也是 red 自己的
window.fetch;                          // 还是原来的 fetch：red 写全局只写在 red 本地
document.body.lastChild.textContent;   // '第三方组件'：DOM 是共享的
```

- `createVirtualEnvironment(globalObject, options)` 和 `distortionCallback`、`env.evaluate` 都是真实 API；选项还有 `endowments`、`keepAlive`、`liveTargetCallback`、`maxPerfMode`、`protectDistortions`、`signSourceCallback` 等。
- 换 getter 的写法照仓库的 `examples/getter-distortion/`。这段代码是按源码行为写的示意，没有在浏览器里实际跑过。
- 简化了的地方：真实的 LWS 不是把 cookie 清空，而是按 namespace 隔开（键名加 `LSKey-{namespace}$` 前缀）。

### 能防什么，不能防什么

能防：

- 全局污染：改内置原型、改 `JSON`、覆盖全局函数，都只影响 red。
- 组件互相干扰：每个沙箱一套内置对象，A 改的东西 B 看不到。
- 直接拿敏感能力：宿主用 distortion 换掉的值，沙箱拿不到原版。

不能防：

- 死循环、长时间占用主线程。
- 吃内存。
- 侧信道（计时、Spectre 一类）。
- 滥用合法暴露的 DOM：DOM 是共享的，沙箱照样能在页面上画一个假登录框。

## 实现要点

### 同一份代码，在两个 Realm 各编译一次

核心是 `membrane.ts` 里的 `createMembraneMarshall`。blue 直接调用它；red 拿到的是它的**源码字符串**，用 red 自己的 `eval` 重新编译，所以 red 侧闭包里的 `Proxy`、`Reflect`、`WeakMap` 都是 red 自己的。两侧握手时互相交换 37 个函数（`callableApply`、`callableConstruct`、`callablePushTarget`……）。`distortionCallback`、`liveTargetCallback` 这些选项只交给 blue，red 侧代码里直接 `options = undefined`。

### 指针协议：对象从不直接跨界

`Pointer` 的类型是一个函数。调用它不返回对象，只把对象写进**创建方**闭包里的变量 `selectedTarget`，接收方立刻读出来再清空：

```ts
function createPointer(originalTarget) {
    return () => { selectedTarget = originalTarget; };
}
targetPointer();
const target = selectedTarget!;
selectedTarget = undefined;
```

blue 对象 `B` 第一次进 red：blue 先过 `distortionCallback` 得到 `B'`，建指针 `pB` 交给 red；red 新建 Proxy，回一个指针 `pR`；两边各自记进 `proxyPointerCache`。之后 `B` 再过膜直接发 `pR`，Proxy 回 blue 时调 `pB` 拿回 `B'`。

两侧之间只传函数和原始值，所以这套协议在 callable boundary（只能过原始值和函数）的约束下也成立，`DESIGN_DOCUMENT.md` §9.2.2 提到了这一点。代码里没有调用 `new ShadowRealm()` 的实现。

其他细节：属性描述符跨界时拍平成 7 个参数；`undefined` 和「没有这个字段」用 `Symbol.for('@@lockerNearMembraneUndefinedValue')` 区分；错误也走指针，沙箱 `catch` 到的是宿主错误对象的 Proxy。

### 哪些用自己的，哪些投影

`getESGlobalKeys` 和反射型内置对象（`Array`、`Object`、`Function`、`Error`、`Proxy` 等）两张表里的名字，red 用自己的，不从 blue 投影；反射型内置对象的 `prototype` 用 `link` 两边配对。其余全局（`Date`、`Promise`、`fetch`、`document`……）投影成 blue 的 Proxy。`Promise` 特意投影，是为了 `fetch` 返回的 promise 能正常用。

### shadow target 和写时复制

Proxy 的 target 是本地新建的占位对象（shadow target），类型要和真对象一致：函数用 `function () {}`，箭头函数用 `() => {}`，数组用 `[]`，否则 `typeof`、`Array.isArray`、`new` 和 Proxy 不变式会出错。

red 侧 Proxy 读操作直接问 blue；第一次写操作时决定走哪条路：

- **static**（默认）：把对方的自有属性和原型一次性复制到 shadow target，之后的读写都在副本上。这就是「改动只影响沙箱」：第一次写时复制。
- **live**：写操作透传到宿主真对象。数组、TypedArray 一开始就是 live；其他对象由 `liveTargetCallback` 决定（比如带 `Symbol.for('@@lockerLiveValue')` 标记的）。`div.style.color = 'red'` 能改到宿主 DOM 靠的就是它。live 对象的 `setPrototypeOf` 和 `__proto__` 赋值不透传。

`DESIGN_DOCUMENT.md` §5.3 说 static 发生在「对方对象完整性变化时」，和代码不一致：代码里任何第一次写都会触发。

### 全局对象懒投影

`lazyRemapProperties` 在 red 全局上给每个键装一个占位 accessor，第一次读或写才去 blue 取真描述符换上。为了不让 `Object.getOwnPropertyDescriptor(window, 'fetch')` 看出破绽，这几个反射方法都被包了一层：碰到没激活的属性先激活再调原函数。

### Distortion

`distortionCallback(target) => target'` 只在 blue 值**第一次**过膜时调用，结果按原值缓存。替换的粒度是值，换掉一个 getter 函数就改写了属性读取。`protectDistortions` 开启后，沙箱删除被换过的属性会抛错，防止删掉替换后从原型链上露出原版。局限：blue 函数内部调用的 `fetch`、`eval`、`setTimeout` 是 blue 自己的，不受 distortion 影响；把一个 blue 函数交给 red，等于把它能做的事都交了出去。

### 浏览器版怎么建

1. 建一个 `display: none`、`sandbox="allow-same-origin allow-scripts"` 的 iframe，拿到 red 的 `window` 和间接 `eval`。
2. `linkIntrinsics`，link `document` 和 `window` 原型链，再对 blue `window` 的键做懒投影。
3. `env.evaluate(sourceText)` 用 red 的间接 eval 执行。

README 大篇幅讲「detached iframe」，但代码里 `keepAlive` 默认是 `true`：iframe 隐藏但仍挂在 DOM 上。CSP 必须允许 `'unsafe-eval'`。多个沙箱各自连一次 blue，兄弟沙箱之间传值要穿两层膜（`redB(blue(redA_obj))`）。

性能上，README 说主要靠「laziness」：只激活代码实际碰到的那部分对象图。另外还有：把「查自有属性 + 取原型」合成一次跨界调用；0 到 5 个参数的调用专门生成 trap，不分配数组；`trackAsFastTarget` 让读属性直接在 blue 执行。

## ShadowRealm：标准化的「新 Realm」

[ShadowRealm](https://github.com/tc39/proposal-shadowrealm) 是 TC39 提案，想把「造一个干净的新 Realm」做成语言内置功能。

**API**：`new ShadowRealm()` 建一个新 Realm，`realm.evaluate(sourceText)` 在里面执行代码，`realm.importValue(specifier, bindingName)` 从里面加载模块并取出一个导出值。

**callable boundary**：只有原始值和函数能跨界。函数过去会被包成一个新的 wrapped function；普通对象过不去，直接抛 `TypeError`。所以不存在「同一个对象跨界后身份变了」的问题，但想传对象就得自己在上面搭一层 membrane。

**同线程、同堆、同步**：explainer 原话是和创建它的环境用同一个 JS 堆，代码在同一个线程同步执行。

**没有 DOM**：ShadowRealm 里只有 ECMAScript 内置对象，宿主可以再加。HTML 的集成方案（[whatwg/html#9893](https://github.com/whatwg/html/pull/9893)，未合并）只打算暴露标了 `[Exposed=*]` 的 Web API，不包括 DOM。

**动机**（[explainer](https://github.com/tc39/proposal-shadowrealm/blob/main/explainer.md)）：一个应用里有来自不同团队、供应商的程序，它们争抢同一个全局对象，互相踩。用 iframe 或 Worker 解决就得走异步消息、序列化数据，「often a deal-breaker」。主要目标原文是：

> provide a proper mechanism to control the execution of a program, providing a new global object, a new set of intrinsics, no access to objects cross-realms, a separate module graph and synchronous communication between both realms

explainer 还直接点名了 Salesforce：

> Sites like Salesforce.com make extensive use of same-origin iframes to create such global objects. Our experience with same-origin iframes motivated us to steer this proposal forward

**非目标**：不提供 IO 钩子，没法在里面控制或阻止 IO；不保证可用性（同一个线程，死循环照样卡住）；不提供完整的保密性（能计时、能做指纹）。explainer 的安全结论是「✅ integrity ⛔️ availability ⚠️ confidentiality」，和 near-membrane 的「完整性，不是安全」一致。

**用例**（explainer 列的）：第三方脚本、代码测试、代码库分段、模板库、DOM 虚拟化。

**和 near-membrane 的关系**：同一个想法的两种做法。near-membrane 借同源 iframe 拿新 Realm，再在两边之间搭一层完整的对象 membrane；ShadowRealm 由引擎原生建 Realm，边界只开给函数。near-membrane 的指针协议两侧只传函数和原始值，所以在 callable boundary 的约束下也成立；但仓库里没有基于 ShadowRealm 的实现。

**状态（2026-10）**：

- 2024-02 进入 Stage 2.7，至今还是 2.7。2024-12 再次申请 Stage 3，没有通过。
- 没有浏览器默认开启：Firefox 2026-02 移除了实现，Chrome 要开标志，WebKit 能查到的最后状态也是要开标志。WPT 已经删掉了 ShadowRealm 的测试（[wpt#59794](https://github.com/web-platform-tests/wpt/pull/59794)）。
- Node 的 [#65650](https://github.com/nodejs/node/pull/65650)（2026-08-30 北京时间开，仍未合并）提议删除 `--experimental-shadow-realm`，理由是浏览器都没实现、WPT 已删测试。
- 提案的 champions 里有 @caridy 和 @rwaldron，他们也是 near-membrane 的维护者。ShadowRealm 停滞和 near-membrane 归档时间上接近，但两者有没有关系纯属推测，没有任何证据。

## 为什么归档

**已确认的事实**（北京时间）：

- 2026-09-18 17:59:43，Salesforce 开源办公室（OSPO）负责人 Jim Jagielski 直接推送 `19685c3`「This repo is ARCHIVED」，只新增模板文件 `CONTRIBUTING-ARCHIVED.md`，不动代码，没有 PR。
- 3 秒前，同一个人用同样的标题和文件归档了毫不相关的 [salesforce/LAVIS](https://github.com/salesforce/LAVIS)。2026 年用这套模板归档的 salesforce 仓库有 30 多个。
- 没有任何官方说明：仓库、issue、博客都没写原因，没有指向替代项目；npm 包没有标 deprecated。
- Salesforce 仍在用这份代码：2026-10-15 发布的 `@locker/sandbox` 0.29.3 依赖 `@locker/near-membrane-dom` 0.19.1。
- Aikido 发布了 [AIKIDO-2026-167438](https://intel.aikido.dev/cve/AIKIDO-2026-167438)：`@locker/near-membrane-base` 0.7.0–0.18.0 有高危沙箱逃逸，0.19.0 修复。
- 归档时仍开着的 #476 附了一个内部工单，标题是「Vulnerability in public near-membrane Salesforce github repo」。
- 归档前几个月有几次逃逸修复，说明写得很细（#487、#489 等，逐条记录见 `raw/sources/near-membrane.md`）。

**推断**（没有直接证据）：更像 OSPO 对公开仓库的例行批量清理，开发可能转到内部。一个可能的动机是不想再公开披露逃逸修复的细节，但这只是时间上接近。

还不清楚：归档是 OSPO 定期清理还是 LWS 团队申请的，0.19.1 是不是最后一个公开版本。

## 使用限制

- **不是安全边界**：只保证完整性，安全靠上层 distortion；同堆同线程，挡不住死循环、吃内存和侧信道。
- **CSP 要允许 `'unsafe-eval'`**。
- **不可替换的属性**（`window`、`location`、`top`）只能保留身份；宿主里已经被改过的 DOM API 会原样投影进去。
- **live 对象上的 accessor defineProperty 仍会透传**到宿主对象（#488 想修，被 #491 回滚）。
- **已归档**：不会再有公开修复。直接依赖就钉在 0.19.1，不要用 0.19.0（内部有 P1 回归）。

## 相关页面

- [[wiki/comparisons/frontend/javascript-sandbox-approaches|JavaScript 沙箱方案对比]]
- [[wiki/syntheses/frontend/same-origin-iframe-sandbox-design|同源 iframe 沙箱设计]]
- [[wiki/topics/systems/sandbox|Sandbox]]
- [[wiki/syntheses/systems/electron-extension-isolation-boundaries|Electron 扩展隔离边界]]

## 来源指针

- `raw/assets/near-membrane-blue-red-realms.png`：脚本（matplotlib）画的米色底手绘风格示意，不是项目官方素材
- [salesforce/near-membrane](https://github.com/salesforce/near-membrane)：README、`DESIGN_DOCUMENT.md`；源码 `packages/near-membrane-base/src/membrane.ts`、`connector.ts`、`environment.ts`、`intrinsics.ts`、`types.ts`，`packages/near-membrane-dom/src/browser-realm.ts`、`types.ts`，`packages/near-membrane-node/src/node-realm.ts`，`examples/getter-distortion/`
- [归档提交 `19685c3`](https://github.com/salesforce/near-membrane/commit/19685c36d267071cc70c2876925f8a020361fe3d)、[salesforce/LAVIS](https://github.com/salesforce/LAVIS)（同批归档）
- [Aikido 通告 AIKIDO-2026-167438](https://intel.aikido.dev/cve/AIKIDO-2026-167438)
- [LWS 架构](https://developer.salesforce.com/docs/platform/lightning-components-security/guide/lws-architecture.html)
- [ShadowRealm 提案](https://github.com/tc39/proposal-shadowrealm)、[explainer](https://github.com/tc39/proposal-shadowrealm/blob/main/explainer.md)、[whatwg/html#9893](https://github.com/whatwg/html/pull/9893)、[nodejs/node#65650](https://github.com/nodejs/node/pull/65650)
- `raw/sources/near-membrane.md`：阅读范围、2026 年各次修复的逐条记录、归档调查记录
