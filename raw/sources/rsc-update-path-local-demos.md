# RSC 更新链路本地 demo 与源码核查记录

- 记录日期：2026-10-14
- 来源：本机与 agent 的对话中搭建并运行的两个 demo，以及 demo 依赖中的 TanStack 源码
- 位置：`~/rsc-demo/`（只记录形态，不复制 `node_modules`）

## 环境与版本

`~/rsc-demo/tss-rsc/node_modules` 中读到的版本：

| 包 | 版本 |
| --- | --- |
| `@tanstack/router-core` | 1.171.37 |
| `@tanstack/react-router` | 1.170.44 |
| `@tanstack/react-start` | 1.169.1 |
| `@tanstack/react-start-rsc` | 0.1.62 |
| `@tanstack/react-store` / `@tanstack/store` | 0.11.2 |
| `@vitejs/plugin-rsc` | 0.5.37 |
| `react` | 19.3.0 |

`next-demo/package.json` 中 `next` 写的是 `latest`，对话中运行时为 Next 16；当前 Mac 上该目录未安装依赖，版本没有在本机复核。

## demo 形态

- `next-demo`：Next App Router，`next dev -p 3101`。文件 `app/page.js`、`layout.js`、`actions.js`（Server Action）、`Button.js`（客户端组件）、`store.js`（内存计数），页面设置 `force-dynamic`。
- 纯 server function 版 TanStack Start demo：端口 3102，用于抓普通 server function 的请求和响应。
- `tss-rsc`：TanStack Start 开启实验性 RSC，端口 3103。`vite.config.ts` 插件为 `tanstackStart({ rsc: { enabled: true } })`、`rsc()`（`@vitejs/plugin-rsc`）、`viteReact()`。`src/routes/index.tsx`：
  - `getCard`（GET server function）调用 `createCompositeComponent` 渲染 `<section>`，里面有服务端 `Sidebar`、计数、渲染时间戳和 `props.children` 插槽。
  - `increment`（POST server function）把内存计数加上 `data.by`，返回 `{ count }`。
  - 路由 `loader` 返回 `{ Card: await getCard() }`；页面组件用 `<CompositeComponent src={Card.src}>` 渲染，插槽里放「服务端 +1」按钮（`await increment(...)` 后 `router.invalidate()`）和带 `useState` 的「本地 +1」按钮。
- 抓包脚本：`capture-next.mjs`、`capture-tss-rsc.mjs`。

## 观察到的请求与响应形态

### Next Server Action

- 请求是 POST，`next-action` header 携带 action id，参数在请求体。
- 响应 `Content-Type: text/x-component`，内容是整条路由的 RSC payload；服务端日志显示 RootLayout、Page、Sidebar 都重新渲染。
- 客户端导航请求带 `next-router-state-tree` header，服务端据此只返回变化的路由段。

### TanStack Start 普通 server function

- 请求地址形如 `/_serverFn/<base64>`，base64 解开是 `{"file": ..., "export": "increment_createServerFn_handler"}` 这样的 JSON。
- 参数和返回值用 seroval 序列化。payload 中 `t:10` 表示对象，`t:0` 表示数字，`i` 是引用 id，`o` 是标志位。
- 返回值外层包了一层，解开后是 `{ result: { count: 1 } }`。

### TanStack Start RSC

- RSC server function 的响应类型为 `application/x-tss-framed`：外层是 seroval，内部嵌入 Flight（RSC 协议）数据，客户端插槽位置是 `ClientSlot` 占位。
- 点一次「服务端 +1」发两个请求：先 POST `increment`，然后 `router.invalidate()` 让 loader 重跑，再 GET `getCard`。
- 点「本地 +1」后再点「服务端 +1」，本地计数保留，服务端计数和时间戳更新。

## 源码核查（tss-rsc 依赖内，行号对应上表版本）

`@tanstack/router-core/src`：

- `router.ts:2495` `invalidate` 定义；`:2524` 内部 `invalidate` 把 match 标记为失效；`:2570` `return this.load({ sync: opts?.sync })`。
- `router.ts:2421` `load: LoadFn`；`:2431` 客户端分支 `await loadClientRoute(this, opts)`。
- `router.ts:1367-1369` `this.getStoreConfig(this)` 后 `this.stores = createRouterStores(this.latestLocation, config)`。
- `load-client.ts:1941` `loadClientRoute`；`:1820` `runClientTransaction`，`:1828` 调 `executeClientLane`（定义在 `:1320`）。
- `load-client.ts:836` 取 `route.options.loader`；`:646` 附近调用 `loader(getLoaderContext(...))`。
- `load-client.ts:1882` `router.startViewTransition(...)`；`:1892` 定义 `commit`，内部调 `commitMatches`（`:1624`）；`:1903` `await router.startTransition(commit, matches)`。
- `load-client.ts:1621` `router.stores.setMatches(matches)`；`stores.ts:153` `setMatches` 定义。

`@tanstack/react-router/src`：

- `router.ts:117` `super(options, getStoreFactory)`。
- `routerStores.ts:1` 从 `@tanstack/react-store` 导入 `batch`、`createAtom`；`:13` `getStoreFactory`，服务端分支 `batch: (fn) => fn()`，客户端分支 `createMutableStore` / `createReadonlyStore` 为 `createAtom`。
- `Transitioner.tsx:31` 覆盖 `router.startTransition`，`:36` 调 `React.startTransition(fn)`。

`@tanstack/react-store/src/useSelector.ts:60` 返回 `useSyncExternalStoreWithSelector(...)`（来自 `use-sync-external-store/shim/with-selector`）。

## 验证范围

- 两个 demo 在对话中实际运行并抓包；本次写 wiki 时只重新读了 `tss-rsc` 源码和依赖源码，没有重新运行。
- TanStack 调用链来自读源码，没有打断点逐步验证。
- TanStack Start 的 RSC 支持标为 experimental，接口可能随版本变化。
