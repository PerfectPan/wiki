---
title: GithubNext-Blocks
type: topic
category: frontend
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - githubnext
  - blocks
source_refs:
  - raw/sources/GithubNext-Blocks.md
---
# GithubNext-Blocks

- load 完以后给主页面发送已经加载好的消息，并带上 hash 值，去获取想要的 block 的代码来加载
- 本身有提供内置组件
- 可以用 BlockComponent 嵌套
- onUpdateContent 会直接渲染，然后向主页面发送内容改变的消息
- 官方支持 [[React]] DSL 可能是为了让包大小能够减少，容器准备好 React 环境即可
- dev 环境打包的路径是确定的，变相约束了代码的目录结构
- BlockComponent 只在 React 环境才会生成，但其实自己也可以直接用 iframe 来搞，是一样的
- setProps 的 bundle 为空，就走本地的加载
- 抽了一个通用的 runtime
- 每个文件通过一个 js script 标签加入 iframe 里，挂载成一个全局变量
- 然后加载，传入 props，进行渲染
- @loadable/component 能够 code split？
- blocks-dev 的方式是纯 React 环境，然后利用 Bundle 先组装代码包，再在 useEffect 的时机去设置渲染函数就结束了，以后 props 有变更就只更新全局的渲染函数，React 重新渲染
- blocks-runtime 的做法是加载完包以后立即执行（放在闭包里），如果下次有变化的话重新加载创建新的组件 - https://github.com/githubnext/blocks-runtime/blob/main/src/bundle.ts#L93
- ```
  // https://github.com/githubnext/blocks-runtime/blob/main/src/events.ts#L22
  // the `setProps` protocol is pretty ad-hoc (see `use-block-frame-messages.ts`):
      //   `{ bundle: null }` means the block was not found
      //   `{ bundle: [] }` means the block is from the dev server (load it locally)
      //   `{ bundle: [...] }` means the block is not from the dev server (load the bundle code)
      //   `{ props: ... }` means render the block with new props
      // `setProps` with `bundle` is called once, then `setProps` with `props` one or more times
  ```
-

## Source Pointers

- `raw/sources/GithubNext-Blocks.md`

