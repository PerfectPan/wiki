---
title: State Management
type: topic
category: frontend
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - state-management
  - zustand
  - optics
source_refs:
  - raw/sources/State Management.md
---
# State Management

- Optics: https://github.com/TSOptics/optics
	- 借鉴了 [[Functional Programming]]中的 optics 思想对嵌套对象进行状态管理，整个对象是 immutable 的，可以 ref 到对象的某个部分，订阅它的更新
	- 与 [[zustand]] 这种不同的是 optics 可以将具体的 optics 作为 props 传递给组件，让组件使用 useOptic 来订阅更新，整体不用感知大的 store，组件不用再区分纯渲染组件和订阅变化的组件以达到复用的效果。在 Root 层将更大的 optic 分解为若干小的 optic 传递给子组件
	- 不让子 state 变更引起父组件上的对象变更，从而触发父组件的 rerender，其实是靠 optics 来隔离，如果父组件的状态需要监听跨 optics 的变更，就要传入 denormalize 参数来深度递归监听。本质上一次变更就会创建一个新的 immutable 的对象，所以 Object.is 一定会不同，需要 optics 来做隔离
	- 不过 createState 返回的 optic，带 get/set/derive 等方法，但是 set 方法并不返回新的 optic 或 state，而是内部更新状态。这意味着 get/set 不是 pure function，而其实是基于 es6 proxy 实现的 store level 的 composition 和 decomposition，而非函数式里的 lens/optics
	- 本身 optics 可以分解，可以组合，非常灵活
	- 也提供了 vanilla 的方法
- [[zustand]]
- useSyncExternalStore 是在两个 snapshot 通过 Object.is 不同的时候才会触发 rerender，所以比如你 [[zustand]] 用 Object.assign 去更新对象，由于引用是同一个，不会触发订阅这个对象的更新
	- ```jsx
	  import { create } from 'zustand';
	  
	  export const useStore = create((set) => ({
	    name: 'John',
	    age: 42,
	    address: { city: 'New York', street: { name: '5th Avenue', number: 940 } },
	    setAddressNumber: (x: number) => {
	      console.log('x', x);
	      set((state) => {
	        console.log(state);
	        return {
	          address: {
	            ...state.address,
	            // const { name, number } = useStore((state) => state.address.street);
	            // 不会触发组件的更新
	            street: Object.assign(state.address.street, {
	              number: x + 1,
	            }),
	          },
	        };
	      });
	    },
	  }));
	  ```

## Source Pointers

- `raw/sources/State Management.md`
