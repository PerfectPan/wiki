---
title: Suspense
type: topic
category: frontend
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - suspense
source_refs:
  - raw/sources/Suspense.md
---
# Suspense

- 实现 Suspense Children
	- 这部分就是 `use` hook 的工作，也是 react-router 中 `Await` 组件的工作
		- promise pending 时，Suspense Children 应该 throw promise，使其被 react 捕捉，终止这一部分组件树的渲染流程，并挂载 handler
		- promise resolve 时，handler 触发，使这一部分组件树重新渲染；
		- promise resolve 后再渲染的流程中，Suspense Children 应该渲染出预期内容；
		- promise reject 时，Suspense Children 应该 throw error 使其被最近 ErrorBoundary 捕捉；
- 在前后端传递 promise 状态
	- 在上述流程中，还有隐藏问题没有解决：如何 promise 对象的信息在整个流程中由 Server 传递给 Browser，使得 Suspense 组件在首屏渲染和追加渲染的 Hydrate 流程中不会出错。
	- Remix (react-router) 的思路是：
		- 首屏渲染时，在 Browser 为 Suspense 组件创建一个 pending promise 对象，react hydrate 时发现 Suspense 组件依赖 pending promise，自然渲染为 fallback 内容；
		- 追加渲染时，在 Server 返回的 HTML 中额外添加一部分内容，包括 promise resolve 的值和将 Browser 上 pending promise resolve 的脚本

		  ```html
		  <div hidden id="S:1">
		  <script async="">
		    // 挂在 window 上的一个可以 resolve 对应 promise 的函数
		    __remixContext.r("routes/_index", "promiseArr", ["reviews1", "reviews2"]);
		  </script>
		  </div>
		  <script>
		  $RC("B:1", "S:1");
		  </script>
		  ```
- 可以辅助阅读：[https://juejin.cn/post/7248606482014896185](https://juejin.cn/post/7248606482014896185)
-

## Source Pointers

- `raw/sources/Suspense.md`

