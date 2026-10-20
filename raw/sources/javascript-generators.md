# JavaScript 生成器与 yield 的类型：来源与验证记录

## 访问元信息

- 访问日期：2026-10-19 至 2026-10-20
- MDN 页面（en-US）：
  - [Iterators and generators](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Iterators_and_generators)
  - [Iteration protocols](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols)
  - [yield*](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/yield*)
  - [Symbol.iterator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol/iterator)
  - [Method definitions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Method_definitions)
- 运行环境：Node.js v24.18.0，TypeScript 5.9.3（`strict`），effect 4.0.5

## 核查证据

### MDN 原文

- Iterators and generators，"Generator functions" 一节：先手写迭代器，再用生成器重写。
  > "Generator functions provide a powerful alternative: they allow you to define an iterative algorithm by writing a single function whose execution is not continuous."
  > "The behavior of this code is identical, but the implementation is much easier to write and read."
- Iterators and generators，"Iterables" 一节：
  > "Iterables which can iterate only once (such as Generators) customarily return `this` from their `[Symbol.iterator]()` method, whereas iterables which can be iterated many times must return a new iterator on each invocation of `[Symbol.iterator]()`."
- Iteration protocols，"The iterator protocol" 中 `done` 字段：
  > "Has the value `true` if the iterator has completed its sequence. In this case, `value` optionally specifies the return value of the iterator."
- Iteration protocols，"Interactions between the language and iteration protocols"：生成器函数返回 generator objects，"which are iterable iterators"。"Error handling" 一节："Most iterators are implemented with generator functions"。
- yield*，"Description"：
  > "`yield*` first gets the iterator from the operand by calling the latter's `[Symbol.iterator]()` method. Then, each time the `next()` method of the generator is called, `yield*` calls the iterator's `next()` method, passing the argument received by the generator's `next()` method (always `undefined` for the first call) … If the iterator result has `done: true`, then the `yield*` expression stops executing and returns the `value` of that result."
- Symbol.iterator，"User-defined iterables"：示例 `class Foo { *[Symbol.iterator]() { yield 1; … } }` 与 `myIterable[Symbol.iterator] = function* () { … }`。
- Method definitions，"Syntax"：语法块列出 `*generator(parameters) {}` 与 `*[expression](parameters) {}`（生成器方法 + 计算属性名）。该页没有直接使用 `*[Symbol.iterator]` 的示例。

## 验证记录

以下类型均用 TypeScript 编译器 API（`checker.typeToString`）打印，运行结果均用 Node.js 实际执行。

### 生成器的推导类型

| 代码 | 推导结果 |
| --- | --- |
| `function* count() { yield 1; yield 2; return "完" }` | `() => Generator<1 \| 2, string, unknown>` |
| 不写注解且使用 `const name = yield "你叫什么？"` | 报错 TS7057：`'yield' expression implicitly results in an 'any' type because its containing generator lacks a return-type annotation.` |
| 注解 `Generator<string, string, string \| number>` | `name: string \| number`，`age: string \| number` |
| 传给参数类型为 `() => Generator<string, string, number>` 的函数 | `age: number`（N 来自上下文） |
| `askName: () => Generator<string, string, string>`，`const name = yield* askName()` | `name: string` |
| `askAge: () => Generator<string, number, string>`，`const age = yield* askAge()` | `age: number` |
| `class Ask<A> { *[Symbol.iterator](): Generator<Ask<A>, A, any> { return yield this } }`，`yield* new Ask<string>(…)` | `string`；外层生成器为 `Generator<Ask<string> \| Ask<number>, string, any>` |
| 同上，但删掉注解 | 结果为 `any`，并报 TS7057 |
| 同上，但第三个参数写成 `unknown` | 报错 `Type 'unknown' is not assignable to type 'A'` |
| 手写 `next(answer?: any): IteratorResult<Ask<A>, A>` 的迭代器 | `yield*` 结果同样是 `string` / `number` |
| 手动驱动：`g.next(); g.next(123)`，而 `name` 的类型是 `string` | 编译 0 个错误；运行时 `TypeError: name.toUpperCase is not a function` |

### 运行顺序

- `count()` 调用后函数体不执行；4 次 `next()` 依次得到 `{value:1,done:false}`、`{value:2,done:false}`、`{value:"完",done:true}`、`{value:undefined,done:true}`。
- `chat()` 第一次 `next("被忽略")` 的参数被丢弃；`next("董事长")` 让 `name = "董事长"`；`next(18)` 得到 `{value:"董事长 18 岁",done:true}`。
- 用一个会打印每次调用的可迭代对象验证 `yield*`：外层每调用一次 `next(v)`，内层迭代器的 `next(v)` 才被调用一次；内层返回 `{done:true,value:"结束值"}` 时，`yield*` 表达式的值为 `"结束值"`。外层中途调用 `return("不要了")` 时，内层迭代器的 `return("不要了")` 被调用。
- `yield* [1, 2]` 依次交出 1、2，表达式的值为 `undefined`。`yield* 42` 抛出 `TypeError: number 42 is not iterable`。
- `return yield this` 的执行顺序：第 1 次 `next()` 停在 `yield this`，`return` 尚未执行；第 2 次 `next("董事长")` 恢复后执行 `return`，得到 `{done:true,value:"董事长"}`。
- 生成器对象同时有 `next`、`return`、`throw`，且 `g[Symbol.iterator]() === g`；数组没有 `next`，每次 `[Symbol.iterator]()` 返回新的迭代器。
- 类本身可以作为可迭代对象：`class Foo { static *[Symbol.iterator]() { … } }` 不实例化也能 `[...Foo]`；把函数对象的原型改成带 `[Symbol.iterator]` 的对象，再用 `class Users extends KeyClass {}` 继承，`[...Users]` 同样可用。

### async/await 编译到 ES2015

`tsc --target ES2015` 编译：

```ts
export async function load(get: () => Promise<string>) {
  const text = await get();
  return text.length;
}
```

输出把函数体改写成 `__awaiter(this, void 0, void 0, function* () { const text = yield get(); return text.length; })`。`__awaiter` 中的 `step` 在 `result.done` 时 resolve，否则对 `result.value` 调用 `.then(fulfilled, rejected)`，`fulfilled` 调用 `generator.next(value)`，`rejected` 调用 `generator["throw"](value)`。

## 未覆盖

- 未测试浏览器引擎，只在 Node.js 24 上运行。
- 未测试异步生成器（`async function*`）和 `for await`。
