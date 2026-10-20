---
title: Algebraic Effects
description: 代数效应是"可以恢复的 throw"；它和效应系统、"副作用写成值"分别回答什么问题，各语言实现到什么程度，以及 Effect、React 借用了其中哪些部分
type: topic
category: languages
created: 2026-04-12
updated: 2026-10-20
timestamp: 2026-10-20
tags:
  - algebraic
  - effects
  - effect-system
source_refs:
  - raw/sources/algebraic-effects.md
  - raw/sources/javascript-generators.md
  - raw/sources/effect-ts.md
  - https://link.springer.com/chapter/10.1007/978-3-642-00590-9_7
  - https://en.wikipedia.org/wiki/Effect_system
  - https://ocaml.org/manual/5.5/effects.html
  - https://koka-lang.github.io/koka/doc/book.html
  - https://overreacted.io/algebraic-effects-for-the-rest-of-us/
resource:
  - raw/sources/algebraic-effects.md
  - raw/sources/javascript-generators.md
  - raw/sources/effect-ts.md
  - https://link.springer.com/chapter/10.1007/978-3-642-00590-9_7
  - https://en.wikipedia.org/wiki/Effect_system
  - https://ocaml.org/manual/5.5/effects.html
  - https://koka-lang.github.io/koka/doc/book.html
  - https://overreacted.io/algebraic-effects-for-the-rest-of-us/
---
# Algebraic Effects

## 摘要

代数效应是一种控制流机制，可以理解为"可以恢复的 throw"：函数执行到一半 `perform` 一个请求，离它最近的 handler 接住请求，决定怎么处理，然后可以 `resume` 把答案送回去，函数从 `perform` 那一行接着执行。handler 拿到的除了请求本身，还有"从 perform 处继续执行"这件事，即续体（continuation）。

handler 对 resume 的不同用法，分别对应常见的控制流：

| handler 怎么用 resume | 等价于 |
| --- | --- |
| 不调用 | 异常 |
| 立刻用一个值调用 | 依赖注入（React Context、Effect 的 Service） |
| Promise 完成后调用 | async/await |
| 调用方要下一个值时才调用 | 生成器 |
| 对同一个 resume 调用多次 | 回溯、枚举所有可能 |

Plotkin 与 Pretnar 在 2009 年把异常处理推广到所有能用"一组操作 + 等式"（代数理论）描述的计算效应，提出了 handler；论文摘要写明这类效应的计算 monad 是该理论的 free-model monad，也就是说，用了效应的程序可以看成一棵操作树，handler 负责解释树上的每种操作。"代数"二字来自这里，和群、环用运算与公理定义是同一种思路。

## 和效应系统、"副作用写成值"的关系

三个概念回答不同的问题，互相独立，可以单独出现，也可以叠加：

| 概念 | 回答的问题 | 例子 |
| --- | --- | --- |
| 副作用写成值（monad） | 副作用在代码里是什么形态：先构造一个不执行的值，再交给运行时执行 | Haskell 的 IO、Effect 的 `Effect<A, E, R>` 对象树 |
| 代数效应 | 运行时怎么处理：程序发出请求，由外层 handler 解释，可以 resume | OCaml 5、Koka、Eff |
| 效应系统 | 编译期怎么检查：在类型里记录函数会产生哪些效应，没处理完就报错 | Java 的受检异常（Wikipedia 称之为"a relatively limited example of an effect system"）、Koka 的效应类型、Effect 的 E 与 R |

效应系统和代数效应的关系，类似 TypeScript 和 JavaScript：一个只在编译期检查，不改变运行行为；另一个决定运行时怎么执行。只有代数效应、没有效应系统时（如 OCaml 5），漏写 handler 要到运行时才报错。

代数效应和函数式编程不是强耦合的：它本身是一种控制流机制，命令式语言也能用（OCaml 5 有可变状态和对象；在 JS 里用生成器就能模拟）。强耦合于函数式的是"副作用写成值"这条路线。

## 各语言的实现程度

| 能力 | JS（生成器模拟）/ Effect | Java | OCaml 5 | Koka |
| --- | --- | --- | --- | --- |
| 自定义效应和 handler | 生成器库可以；Effect 只有内置几种 | 不支持 | 支持 | 支持 |
| resume 一次 | 生成器可以，但每层都要写 `function*` | 不支持 | 支持 | 支持 |
| 对同一个 resume 调用多次 | 不支持（生成器只能往前走） | 不支持 | 不支持（手册：续体只能 resume 一次） | 支持（手册 3.4.10 "Resuming more than once"） |
| 调用链中间的函数不用改写 | 不支持 | — | 支持 | 支持 |
| 效应写进类型并检查 | Effect 记录 E 与 R | 只有受检异常 | 不支持 | 支持（手册 3.2 "Effect types"、3.2.3 "Polymorphic effects"） |

前三项受运行时限制：要把"程序剩下的部分"保存下来以后再恢复，引擎需要支持保存和切换调用栈；多次恢复还要复制栈，并且很难和资源释放一起做对。后两项受类型系统限制：除了在类型里写效应，还需要效应多态，否则 `map` 这类高阶函数很难写（Java 中在 stream 的 lambda 里抛受检异常就是例子）。

## 和 Effect、React 的关系

- [[wiki/topics/languages/effect-ts|Effect]]：`yield* TodoApi` 相当于 perform，Layer 放进 `fiber.context` 的实现相当于立刻 resume 的 handler；R 列出尚未处理的服务，provide 一个就去掉一个。它用"副作用写成值"加生成器模拟出代数效应最常用的部分，不能自定义 handler，也不能多次 resume，调用链上到处要写 `Effect.gen`。
- React：Suspense 中组件 throw 一个 Promise，由最近的边界接管，形状上是"下层发起、上层处理"。Dan Abramov 在文中说明 Suspense 并不是真正的代数效应：Promise 完成后 React 重新渲染组件，而不是恢复调用栈。

## 笔记

- 副作用在顶层定义，结束后交还控制权
- 可以跨调用栈获取当前 Continuation
- 可以替换当前 Continuation 内 Effect 的实现
- 实验性质的库：
	- https://github.com/koka-ts/koka?tab=readme-ov-file
- 之所以说 [[react]] 也是一种 Algebraic Effects 是因为 React 内置 hook 是对 React 组件里副作用的抽象, 注册的 callback 则是该组件副作用的实现.
-
- https://overreacted.io/algebraic-effects-for-the-rest-of-us/
	- 当我们抛出一个异常的时候，执行引擎会摧毁所有上层调用栈以及其中的局部变量（「回卷（unwind）」）；但是当我们执行一个效应时，虚构的引擎会创建一个回调函数，这个回调函数的函数体是正在执行的函数体的剩余部分，并且在我们执行`resume with`时执行这个回调函数。
	- 可以把「做什么」和「怎么做」完全分离。
		- 它可以让你写代码的时候先把注意力都放在「做什么」上：
			- ```js
			  function enumerateFiles(dir) {
			    const contents = perform OpenDirectory(dir);
			    perform Log('Enumerating files in ', dir);
			    for (let file of contents.files) {
			      perform HandleFile(file);
			    }
			    perform Log('Enumerating subdirectories in ', dir);
			    for (let directory of contents.dir) {
			      // 我们可以递归或者调用别的有效应的函数
			      enumerateFiles(directory);
			    }
			    perform Log('Done');
			  }
			  ```
		- 然后再把上面的代码用「怎么做」包裹起来：
			- ```js
			  let files = [];
			  try {
			    enumerateFiles('C:\\');
			  } handle (effect) {
			    if (effect instanceof Log) {
			      myLoggingLibrary.log(effect.message);
			      resume;
			    } else if (effect instanceof OpenDirectory) {
			      myFileSystemImpl.openDir(effect.dirName, (contents) => {
			        resume with contents;
			      });
			    } else if (effect instanceof HandleFile) {
			      files.push(effect.fileName);
			      resume;
			    }
			  }
			  // `files`数组里现在有所有的文件了
			  ```
	- 代数效应同样允许我们不用写太多脚手架代码就能把业务逻辑和实现它的效应的具体代码分离开。比如说，我们可以在测试中用一个伪造的文件系统和日志系统来代替上面的生产环境

## Source Pointers

- `raw/sources/algebraic-effects.md`
- `raw/sources/javascript-generators.md`：用生成器模拟 perform / resume 的实验与限制
- `raw/sources/effect-ts.md`：Effect 的 Service、中断与 Scope 实现位置
- [Plotkin & Pretnar · Handlers of Algebraic Effects（ESOP 2009）](https://link.springer.com/chapter/10.1007/978-3-642-00590-9_7)
- [Wikipedia · Effect system](https://en.wikipedia.org/wiki/Effect_system)
- [OCaml 手册 · Effect handlers](https://ocaml.org/manual/5.5/effects.html)
- [Koka 手册](https://koka-lang.github.io/koka/doc/book.html)
- [Dan Abramov · Algebraic Effects for the Rest of Us](https://overreacted.io/algebraic-effects-for-the-rest-of-us/)
