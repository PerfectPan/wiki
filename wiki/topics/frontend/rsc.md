---
title: RSC
type: topic
category: frontend
created: 2026-04-12
updated: 2026-10-14
tags:
  - react
  - rsc
  - ssr
source_refs:
  - raw/sources/rsc.md
  - raw/sources/rsc-update-path-local-demos.md
---
# RSC

- React 在服务端会把 Client Component 会被渲染成脚本的引用，Server Component 会被流式渲染成类JSON UI。引用和 JSON 再会传到浏览器中进行协调和视图更新。
- 虽然客户端组件不能直接 import 服务端组件，但是可以把服务端组件以 children 方式。比如可以写这样的代码`<ClientTabBar><ServerTabContent/></ClientTabBar>`。从客户端组件的角度来看，它的子组件将是一个已经渲染好的树，比如 `ServerTabContent`的输出。这意味着服务器和客户端组件可以在任何层级上嵌套和交错。
- ![CleanShot 2023-07-29 at 23.13.32@2x.png](raw/assets/cleanshot-2023-07-29-at-23-13-32-2x-1690643621625-0.png)
- 一些 Lib：
	- https://github.com/devongovett/rsc-html-stream
		- Inject an RSC payload into an HTML stream and read it back
- 实际尝试下来渲染还是一起上屏的，然后 RSC 字符串的顺序是没关系的，流式的部分应该在它处理 RSC 字符串的（不过含有客户端组件没有尝试，估计也还是要等客户端组件回传回来才会上屏，不然树是不完整的）： https://stackblitz.com/edit/vitejs-vite-11my8t?file=package.json,src%2Fmain.tsx,index.html&terminal=dev
- 1. 生成 RSC 协议字符串。
	- 比如我们有个组件树，App -> Foo。调 RSDWS（react-server-dom-webpack/server） 渲染 App 即可得到 RSC 协议的字符串。
		- ```js
		  import rsdws from "react-server-dom-webpack/server";
		  const { renderToPipeableStream } = rsdws;
		  import { App } from "./app/App.js";
		  renderToPipeableStream(<App />).pipe(process.stdout);
		  // 输出
		  // J0:["$","div",null,{"children":[["$","h1",null,{"children":"App"}],["$","p",null,{"children":"Foo"}]]}]
		  ```
	- 现在来加一个 Client 组件 Bar，注意 Client 组件在 RSC render 时不会引真实文件，而是被替换成 `{ $$typeof, filepath, name }` 的格式。这一步通常由框架或构建工具来做。然后 renderToPipeableStream 时加上 bundle 相关配置，webpack 的场景下需要 id、name 和 chunks 字段。
		- ```js
		  const Bar = {
		    $$typeof: Symbol.for("react.module.reference"),
		    filepath: "Bar.tsx",
		    name: "Bar",
		  };
		  renderToPipeableStream(<App />, { 'Bar.tsx': { Bar: { id: 'Bar.tsx', name: 'xxx', chunks: [] } } }).pipe(process.stdout);
		  
		  // 输出
		  // M1:{"id":"Bar.tsx","name":"xxx", "chunks":[]}
		  // J0:["$","div",null,{"children":[["$","h1",null,{"children":"App"}],["$","p",null,{"children":"Foo"}],["$","@1",null,{}]]}]
		  ```
	- 其中 `Mx` 表示模块，而 `["$","@1",null,{}]` 表示使用 M1 模块。
- 2. 消费 RSC 协议字符串
	- 消费是通过 RSDWC（react-server-dom-webpack/client）。RSDWC 有 browser、node、edge 等实现，提供 createFromFetch、createFromReadableStream 等不同的消费方法。createFromXXX 方法会产出一个处理 RSC 协议字符串的 Promise，最终通过 `use()` 使用，产生 JSX。
		- 比如 Browser 侧消费的例子：
			- ```js
			  import React, { use } from "react";
			  import { createFromFetch } from "react-server-dom-webpack/client";
			  import ReactDOM from "react-dom/client";
			  
			  const chunk = createFromFetch(fetch('/path/to/.'));
			  function Container() {
			    return use(chunk);
			  }
			  ReactDOM.createRoot(root).render(<Container />);
			  ```
		- 由于使用的是 react-server-dom-webpack，意味着加载方式遵循 webpack 的规范。如果你的实现不基于 webpack，需要对 `__webpack_require__` 和 `__webpack_chunk_load__` 打补丁。
			- ```js
			  globalThis.__webpack_chunk_load__ = async (chunkId: string) => {};
			  globalThis.__webpack_require__ = (moduleId: string) => {};
			  ```
- https://overreacted.io/how-imports-work-in-rsc/
	- 从模块划分的角度，为了让后端代码不引入前端代码，前端代码不引入后端代码，引入了 'use client' 和 'use server' 两个指令，同时为了让一份代码能够同时运行，服务端引入客户端组件的时候需要引入构建工具，让引入的客户端组件一个 ref，到客户端环境的时候才能真正的被消费，客户端组件引入服务端 action 同理
	- 这样就是一份代码，两个系统都能跑，跨越了系统的边界
- 一条很稳的理解是：RSC 的价值不只是“减少 bundle”，还在于它把服务器和客户端的优势拆开用了
	- 服务端组件可以直接访问服务端资源、减少客户端下载体积
	- 客户端组件则保留交互能力
	- 但 这里还需要补一个边界：RSC 仍然不能自动消灭 hydration 和客户端下载，很多场景只是把“所有组件都必须在客户端执行”的前提打破了

- `'use server'` 和 RSC 是两件事：
	- `'use server'` 标记的函数会被构建工具替换成一个 id，客户端调用时发 HTTP 请求到服务端执行，本质上是 RPC。Next 里请求通过 `next-action` header 带上 action id。
	- RSC 解决的是服务端组件渲染结果怎么传到客户端。两者常一起出现，是因为 Next 的 Server Action 响应会顺带返回新的 RSC payload；TanStack Start 的普通 server function 只返回 seroval 序列化的数据，不带 RSC。
- RSC 和打包器强耦合：服务端渲染时客户端组件要变成模块引用（见上面的 `M1`），客户端要能按引用加载对应 chunk。这需要构建时把 `'use client'` 模块拆出来并生成模块映射，所以 RSC 实现依赖具体的打包器集成，例如 `react-server-dom-webpack`、`@vitejs/plugin-rsc`。
- 和 Astro islands 对比：Astro 在服务端把页面渲染成 HTML，只有标记了 `client:*` 的组件作为 island 在浏览器 hydrate，其余部分不发 JS；它不传类似 RSC 的组件树协议，交互后的服务端更新也不在这套机制里。
- 交互后的更新：React 只做「解码 payload 成元素值 → `setState` 替换 → reconcile」，没有局部合并 payload 的 API。框架差别在替换粒度，见 [[wiki/syntheses/frontend/rsc-update-path-next-vs-tanstack|RSC 交互后的更新链路]]。

## Source Pointers

- `raw/sources/rsc.md`
- `raw/sources/rsc-update-path-local-demos.md`
