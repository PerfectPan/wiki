- [[RSC]] 框架
- Build 概览：
	- analyzeEntries: 分析客户端组件 / 服务端组件 / server action
		- 打包的时候会自动 inline client.js 文件，相当于是运行时的一段代码
		- [vite-plugin-rsc-managed]: vite 打包的时候入口加一个 entries.js，如果实际 resolve 没有，说明走了 file router，直接返回一段加载 pages 下的文件路由代码，这样就支持了两套代码，优先级是 entries.js > file router，main.js 同理
			- file router 就是针对 createPages 的语法糖
		- [vite-plugin-rsc-analyze]: 分析 'use client' 和 'user server' 指令，好像还做了些别的事情
			- 遇到客户端组件还会做一个转换
		- [vite-plugin-rsc-transform]:
			- 加载的时候调换 import 和 use 指令的顺序（为什么？）
			- `react-server-dom-webpack/node-loader` 就是对代码转了一层，类似 webpack loader 的作用，转换代码
				- client component：替换成一个引用 `registerClientReference`，里面会指明客户端组件代码的位置
			- build 的时候修改 ref 里文件的名字: `/Users/perfectpan/Workspace/waku/packages/waku/dist/client.js` -> `@id/assets/rsc2-d3563c2.js`，这个是最终输出的文件名字，哈希过（感觉客户端组件叫 rsc-xxx 有点怪..）
	- buildServerBundle： 写着为 RSC，感觉是不走 SSG，需要服务器的时候需要这个 build output
	- buildSsrBundle：渲染出 SSR
	- buildClientBundle：构建出 CSR 的包，如果页面是 static 的会构建出静态的 RSC 字符串（这样就是 SSG）
		- 对每个静态页面构建出一个 HTML，也放到 public 下
	- 根据不同的托管宿主组装代码结构
		- https://vercel.com/docs/build-output-api/v3
		- 如果需要一个服务器（SSR 也好，RSC 也好）会放到一个简单的 worker 下去跑
- [vite-plugin-rsc-entries]: 给 entries.js 末尾加一段代码，能够根据路由 import 代码，还给 `react-server-dom-webpack-server.edge.production.min.js` 加了个前缀 code（不知道为什么）
- [vite-plugin-rsc-serve]: 如果是 serverless 的话就需要额外打包一份 server 的代码来处理 ssr，用这个 plugin 解决
- [vite-plugin-rsc-index]: 处理 html 相关的逻辑
- 如果有 dynamic 的时候必须是要有 server 的（但是目前感觉没有解耦开来，就是打包目前是无脑都打了，但是如果最后是 SSG 的场景，SSR 那些文件都没用了），然后如果目标是 SSG，但是有 dynamic 页面我理解也是有问题的
- 没有单纯的 CSR 场景（都是 SSG 过了）
- 因为可能会直接访问某个路由，因此需要针对这些路由都 gen 出对应的 html 文件（SSG 场景），如果是 SSR 的话就不用了
- TODO 如果是 SSG 的话 ...catchAll 还会有用么？是不是要针对部署平台的路由设置什么的来兜底？
- 开发者可以通过 `createPage`，`createLayout` 来指定页面的位置，waku 会根据位置组合 layout 和 page，还有根据 path 去分析是不是动态的插槽，还是静态的页面，对内是暴露三个方法（其实这三个方法是最 low level 的，开发者也可以调用）：
	- renderEntries：给定一个入口，找到关联的组件
	- getBuildConfig：应该是 SSG 相关的逻辑
	- getSsrConfig：应该是 SSR 相关的逻辑
- 路由怎么做？
	- SSR 的时候 server 端会根据不同的路由，直接在 context 上注入路由信息，然后 client 端还是走 window.location 那一套，这样就能防止 server 端访问 window.location 失败的问题，同时只给用户暴露一个 useRouter，屏蔽两端的差异
	- TODO 有一些 skip 的逻辑还没看懂
- 然后生成 HTML 文件的时候都会直接把生成好的 RSC payload 放到文件中，这样就不用在客户端加载的时候重复去请求服务器获取服务器组件的 RSC payload（其实就是 RSC 场景 SSG 怎么做的问题）
- [[SSR]] 降级 CSR
	- ```js
	  if (document.body.dataset.hydrate) {
	    hydrateRoot(document.body, rootElement);
	  } else {
	    createRoot(document.body).render(rootElement);
	  }
	  
	  ```
- 文件系统下，动态生成的代码是动态 import 组件代码的，这样可以让动态生成的 entries.js  的体积减少
	- ```js
	  const entries = fsRouter(
	    import.meta.url,
	    (file) => /* @__PURE__ */ Object.assign({ "./pages/_layout.tsx": () => import("./pages/_layout.js"), "./pages/about.tsx": () => import("./pages/about.js"), "./pages/index.tsx": () => import("./pages/index.js") })[`./pages/${file}`]?.()
	  );
	  ```
- 现在的打包模式决定了部分 css 需要单独分析出来然后手动加到 html 中（Vite 是以 html 文件为入口的，这里其实是用了虚拟文件的做法）
- Bug：
	- reoptimize 的时候刷新似乎就会报 useContext not defined
	- 修改 css 偶现 报错，json 解析失败什么的
	- 中文路由没有兼容似乎
	- server component 套 client component 似乎会报错
	- layout 偶现丢失