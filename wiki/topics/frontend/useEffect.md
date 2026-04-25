---
title: useEffect
type: topic
category: frontend
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - useeffect
source_refs:
  - raw/sources/useEffect.md
---
# useEffect

- Unlike events, Effects are caused by rendering itself rather than a particular interaction.
- An Effect describes how to [synchronize an external system](https://beta.reactjs.org/learn/synchronizing-with-effects) to the current props and state.
- 编写 useEffect 的时候要尽可能的让每个副作用函数的功能是正交的，不要都一通写在一起，不然可能会造成部分逻辑不必要甚至错误的二次执行（比如上报日志）
- Global or mutable values can not be dependencies:
	- 脱离了 React 的 Data Flow，React 无法观测到，需要使用 [[useSyncExternalStore]] hooks 去读取订阅外部变量
	- [[useRef]] 的 current 属性是 mutable 的，但是它的改变不会触发 React 的 re-render，所以它也不属于[[响应式]]变量
- 换言之：Values declared inside the component body are “reactive”.
- Effect 里的逻辑是[[响应式]]的，Event Handler 里的逻辑是非响应式的
- useEffect 执行的时机是每次渲染结束
- 如果你想要读取最新的值且不想让他具备响应式的性质，使用 [[useEvent]] 去包裹它
- 如果在 useEffect 里使用了 setXXX 去更新变量，且这个值依赖前一个 state，可以用 updater function 去做以消除 dependency array 的依赖
	- ```js
	  // before
	  function ChatRoom({ roomId }) {
	    const [messages, setMessages] = useState([]);
	    useEffect(() => {
	      const connection = createConnection();
	      connection.connect();
	      connection.on('message', (receivedMessage) => {
	        setMessages([...messages, receivedMessage]);
	      });
	      return () => connection.disconnect();
	    }, [roomId, messages]); // ✅ All dependencies declared
	    // ...

	  // after
	  function ChatRoom({ roomId }) {
	    const [messages, setMessages] = useState([]);
	    useEffect(() => {
	      const connection = createConnection();
	      connection.connect();
	      connection.on('message', (receivedMessage) => {
	        setMessages(msgs => [...msgs, receivedMessage]);
	      });
	      return () => connection.disconnect();
	    }, [roomId]); // ✅ All dependencies declared
	    // ...
	  ```

## Source Pointers

- `raw/sources/useEffect.md`
