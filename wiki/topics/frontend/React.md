---
title: React
type: topic
category: frontend
status: seed
created: 2026-04-12
updated: 2026-04-25
tags:
  - react
  - hooks
  - rsc
  - ssr
  - suspense
source_refs:
  - raw/sources/React.md
---
# React

- Hooks Library
	- https://react-hookz.github.io/web/?path=/docs/home--page
- 状态更新：
	- 引用变了才会重新渲染
	- [[zustand]] useShallow 内部会浅比较，不比较引用，优化 re render（为什么之前都不知道... 得用 react-scan 看看了..）
- 状态设定原则：状态尽量是正交的，其他状态都可以由这些原子状态计算得来，如果要避免状态计算的高复杂度，可以用 [[useMemo]] 来缓存状态
- 不要在组件函数内部再定义另一个组件。React 会按函数 identity 识别组件类型；如果每次 render 都重新创建子组件函数，React 会把它当成一个全新的组件，导致原子树被卸载再挂载，状态和副作用也会随之重置。
- 使用 [[useEffect]] 的时机只有在 component was displayed to the user，要想清楚这个逻辑是否有必要在这个时机执行。如果是通过用户交互触发的，就请放在 Event Handler 里面执行
- 如果要在子组件里去触发父组件的事件，最好直接放在 Event Handler 里就做掉了，如果放在 [[useEffect]] 里去做会触发两次 render，得不偿失
- 如果要到了同步父子组件状态的地步，那么最好可以把状态提一级，直接由父组件去控制子组件的状态，子组件就是一个纯渲染的组件
- 服务端请求按常理来说都会放在 [[useEffect]] 里，但可能会存在数据竞争的问题，这时候要用 cleanup 函数去清理状态，同时可能还有数据缓存的问题，不是一个很好解决的问题，不过社区应该已经有很好的 hooks / 框架去解决这些问题，如果是自己简单的写一下可以封装一个 hooks:
	- ```js
	  function useData(url) {
	    const [data, setData] = useState(null);
	    useEffect(() => {
	      let ignore = false;
	      fetch(url)
	        .then(response => response.json())
	        .then(json => {
	          if (!ignore) {
	            setData(json);
	          }
	        });
	      return () => {
	        ignore = true;
	      };
	    }, [url]);
	    return data;
	  }
	  ```
- 组件关注 mount / update / unmount 三个阶段，而 Effect 需要关注的是每一个分开的同步的过程（包含开始和结束）就够了，从组件的角度考虑会显得很复杂，React 会将 [[useEffect]] 里包裹的函数在「正确」的时机去进行同步，你要做的就是把这个开始和结束(cleanup function)的过程写好写对，标记好正确的 dependency array 即可
- React 借助 [[ESLint]] 能够静态分析出你的 [[useEffect]] 的 dependency array 是否缺少响应的响应式变量
- [[Ref]]
- [[useState]] 每次调用返回的都是上一次 snapshot 的值，初始化的时候会返回 initialValue 或者如果是个函数会将其在初始化阶段调用一次
- 自定义 Hooks 里的 useState 是独立的，可以理解为把函数展开
- https://github.com/bramblex/react-hooks React Hooks 在低版本上的 polyfill
	- 需要一个函数包裹 function component，里面实际上是一个 class component
	- class component 的 render function 是用 function component 创造的
	- 全局维护一个 context 栈，每次渲染的时候就把这个组件和 计数器 counter 推进去，counter 代表一个 function component 里 hooks 的顺序
	- 在组件渲染的时候里面用的 useState 就会用这个计数器和 class component 的 state 绑定在一起，然后用 setState 去封装更新函数
		- ```js
		  export function useState<T>(defaultState: State<T>): [T, SetState<T>] {
		      const { component, counter } = useCounter()
		      const componentState: { [counter: number]: T } = component.state
		      const componentSetters = component.__hooks__.setters
		  
		      if (!componentState.hasOwnProperty(counter)) {
		          if (typeof defaultState === 'function') {
		              componentState[counter] = (defaultState as () => T)()
		          } else {
		              componentState[counter] = defaultState
		          }
		  
		          componentSetters[counter] = (state, callback?) => {
		              const componentState: { [counter: number]: T } = component.state
		              if (typeof state === 'function') {
		                  const oldState = componentState[counter] as T
		                  component.setState({ [counter]: (state as (oldState: T) => T)(oldState) }, callback)
		              } else {
		                  component.setState({ [counter]: state }, callback)
		              }
		          }
		      }
		  
		      return [componentState[counter], componentSetters[counter]]
		  }
		  ```
- [[SSR]]：首屏页面直出，整个 JS 大小还是没变，JS 加载完以后 hydration，后续页面切换还是走客户端渲染，所以支持优化了首屏的 FCP，TTI 其实没有变
- [[RSC]]
	- 可以流式渲染，然后 JS 体积会小很多，如果 client component 尽可能少的话
	- 不用等请求的数据返回，可以直接返回一些有意义的 DOM 元素，后来返回以后再 streaming 把相关元素返回，在客户端打 patch 渲染，不仅优化 FCP，也优化了 TTI
- [[React Render Optimization]]
- React 18 的并发渲染会带来 Tearing 问题：
	- https://github.com/reactwg/react-18/discussions/69
	- https://github.com/reactwg/react-18/discussions/70
	- 并发渲染渲染到一半被更高优先级的渲染任务打断，组件 A 和 组件 B 共同依赖的状态被修改，就有可能出现渲染结束以后组件 A 用的是老的值，组件 B 用的是新的值（打断后被更新了状态）
		- 这里组件 A 最终没有用新的值跟状态管理库实现有关，React 感知不到外部的数据源改变的时机，如果你使用 React 内置的 hooks 来管理，比如 useState，那么最终组件 A 的值会被正确更新成新的值，也不会有 tearing 的问题
	- React 提供了 useSyncExternalStore 这个 API 来解决这个问题，当有出现状态更新的时候强制将本次渲染变为同步的，这其实就是失去了并发渲染带来的优势
		- 使用了这个 API 以后也不再能用 startTransition 的 API
	- daishi 的一些实践思考：https://blog.axlight.com/posts/why-use-sync-external-store-is-not-used-in-jotai/
	- jotai 会短暂 tearing 问题讨论的帖子：https://github.com/pmndrs/jotai/discussions/2137
	- jotai 内部实现采用的是 useReducer，那为什么也导致了 Tearing 呢
		- 因为单独使用 useState 或 useReducer 是没问题的，但 Jotai 采用了 useReducer + useEffect 进行同步更新这可能会导致 Tearing
		- 这样就是能享受 cocurrent 但是可能会存在偶发的 tearing 问题，daishi 认为这个问题还好
- 状态管理库的技术选型方向：
	- 原子化 vs 非原子化
	- mutable vs immutable
	- 手动(zustand) vs 半自动(jotai) vs 自动优化(mobx)
	- SSR / RSC 支持（zustand 无法支持，jotai 可以）
	- 解决 tearing 问题 vs 支持并发渲染
- [[Suspense]]

## Source Pointers

- `raw/sources/React.md`
