---
title: Chrome DevTools
type: topic
category: tooling
status: seed
created: 2026-04-12
updated: 2026-04-19
tags:
  - chrome
  - devtools
source_refs:
  - raw/sources/Chrome DevTools.md
  - https://chromedevtools.github.io/devtools-protocol/
  - https://developer.chrome.com/docs/extensions/mv3/devtools/#overview
---
# Chrome DevTools

- http://127.0.0.1:${remote-debugging-port}/json 就能获得所有待调试页面的信息，但是至今不知道这个是哪里来的，找不到文档 UPDATE: https://chromedevtools.github.io/devtools-protocol/
	- 数据结构如下
	- ```json
	  {
	    "description": "",
	    "devtoolsFrontendUrl": "/devtools/inspector.html?ws=127.0.0.1:6729/devtools/page/06B2B44290775EB1F841F55CAAC11ED8",
	    "id": "06B2B44290775EB1F841F55CAAC11ED8",
	    "title": "飞书开发者工具",
	    "type": "page",
	    "url": "file:///Users/perfectpan/Documents/bytedance/op-fe-ide/packages/ide/libs/renders/gadget.html?uuid=2dc60810-02c1-11ed-b521-5f8733a922d9&slardarInitConfig=%7B%22bid%22%3A%22feishu_devtools_cli%22%2C%22isOpen%22%3Afalse%2C%22commonTags%22%3A%7B%22renderType%22%3A%22ide%22%2C%22cliVersion%22%3A%222.19.1%22%2C%22platform%22%3A%22Darwin%22%2C%22ideVersion%22%3A%222.19.1%22%2C%22commitHash%22%3A%22commitHash_placeholder%22%7D%7D&locale=zh-CN",
	    "webSocketDebuggerUrl": "ws://127.0.0.1:6729/devtools/page/06B2B44290775EB1F841F55CAAC11ED8"
	  },
	  ```
- https://chromium.googlesource.com/chromium/blink/+/refs/heads/main/Source/devtools/front_end/inspector.html
- https://zhaomenghuan.js.org/blog/chrome-devtools-frontend-analysis-of-principle.html
- https://juejin.cn/post/6844903565429833736
- inspector.html 比 devtools_app.html 就多了一个对页面的快照模块 「screencast」
- [Contributing to Chrome DevTools](https://docs.google.com/document/d/1WNF-KqRSzPLUUfZqQG5AFeU_Ll8TfWYcJasa_XGf7ro/edit#heading=h.xz439gqj1lwr)
- https://medium.com/@paul_irish/1e671bf659bb
- 扩展 Devtools：https://developer.chrome.com/docs/extensions/mv3/devtools/#overview
- 贡献指南：https://docs.google.com/document/d/1WNF-KqRSzPLUUfZqQG5AFeU_Ll8TfWYcJasa_XGf7ro/view
- Node SDK：https://github.com/cyrus-and/chrome-remote-interface，提供了一层抽象，方便发送 CDP 协议

## Source Pointers

- `raw/sources/Chrome DevTools.md`
- https://chromedevtools.github.io/devtools-protocol/
- https://developer.chrome.com/docs/extensions/mv3/devtools/#overview
