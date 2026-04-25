---
title: useMemo
type: topic
category: frontend
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - usememo
source_refs:
  - raw/sources/useMemo.md
---
# useMemo

- 使用 useMemo 进行优化仅在少数情况下有价值：
	- 你明确知道这个计算非常的昂贵，而且它的依赖关系很少改变。
	- 如果当前的计算结果将作为 memo 包裹组件的 props 传递。计算结果没有改变，可以利用 useMemo 缓存结果，跳过重渲染。
	- 当前计算的结果作为某些 hook 的依赖项。比如其他的 useMemo / useEffect 依赖当前的计算结果。
- 不用 useMemo 的方法：
	- 把静态部分单独抽离出来
		- ```ts
		  export default function App() {
		    let [color, setColor] = useState('red');
		    return (
		      <div>
		        <input value={color} onChange={(e) => setColor(e.target.value)} />
		        <p style={{ color }}>Hello, world!</p>
		        <ExpensiveTree />
		      </div>
		    );
		  }

		  // 状态下移
		  export default function App() {
		    return (
		      <>
		        <Form />
		        <ExpensiveTree />
		      </>
		    );
		  }

		  function Form() {
		    let [color, setColor] = useState('red');
		    return (
		      <>
		        <input value={color} onChange={(e) => setColor(e.target.value)} />
		        <p style={{ color }}>Hello, world!</p>
		      </>
		    );
		  }
		  ```
	- 静态部分作为一个 props 传入
		- ```ts
		  // 当color改变，colorPicker重渲染，但是children的props并没有变化，
		  // 因此React会复用之前的children，ExpensiveTree没有重渲染，问题解决！
		  export default function App() {
		    return (
		      <ColorPicker>
		        <p>Hello, world!</p>
		        <ExpensiveTree />
		      </ColorPicker>
		    );
		  }

		  function ColorPicker({ children }) {
		    let [color, setColor] = useState("red");
		    return (
		      <div style={{ color }}>
		        <input value={color} onChange={(e) => setColor(e.target.value)} />
		        {children}
		      </div>
		    );
		  }
		  ```
	- React 虽说在会重渲染整颗子树（还没到 DOM 渲染那一步），但看起来如果一个对象没有变化（指向）的话是不会继续往下渲染的，相当于有这么一个基本的优化，之前都是因为每次都 create 新的 jsx 导致产生了新的对象，所以会有整棵子树都会重渲染的错觉

## Source Pointers

- `raw/sources/useMemo.md`
