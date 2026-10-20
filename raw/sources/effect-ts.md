# Effect（Effect-TS）：来源与验证记录

## 访问元信息

- 访问日期：2026-10-16 至 2026-10-20
- 源码：npm 包 `effect@4.0.5` 的 `dist/`（下文行号均指这个版本）；部分阅读也对照了 `effect@4.0.3`（agent-kit 锁定的版本），结构相同。
- 版本日期来自 npm registry：`effect` 包创建于 2022-11-23，3.0.0 发布于 2024-04-16，4.0.0 发布于 2026-10-01。
- 类型参数顺序：`@effect/io@0.41.2` 的 `Effect.d.ts:83` 与 `effect@2.2.5` 的 `dist/dts/Effect.d.ts:80` 为 `Effect<R, E, A>`；`effect@2.3.0` 的 `dist/dts/Effect.d.ts:79` 为 `Effect<out A, out E = never, out R = never>`。
- React 绑定：`@effect/atom-react@4.0.5`，peerDependencies 为 `react >=19.0.0 <20.0.0`、`effect ^4.0.5`、`scheduler >=0.25.0 <0.29.0`。
- agent-kit 引用固定到提交 [`e7396c5`](https://github.com/PerfectPan/agent-kit/tree/e7396c50a7cb50cd8011651d8886b2fe440e8f1c)。
- 官网：[Why Effect?](https://effect.website/docs/v4/getting-started/why-effect)、[The Effect Type](https://effect.website/docs/v4/getting-started/the-effect-type)、[Managing Services（v3）](https://effect.website/docs/v3/requirements-management/services/)。访问时 v4 文档只覆盖入门（Effect 类型、生成器、两类错误、基础并发、运行），Service、Layer、Scope、TestClock 仍在 v3 文档中，v3 示例使用 `Context.Tag`。
- 来历：[mikearnaldi/effect-ts](https://github.com/mikearnaldi/effect-ts) 早期仓库称其为 "functional effect system for TypeScript"，以 ZIO 和 ZIO-Prelude 为主要灵感和移植参照；[Effect 官方推文](https://x.com/EffectTS_/status/1628377536328617984)宣布 fp-ts 并入 Effect（2023 年 2 月前后）。

## 核查证据

### 运行时

| 位置 | 观察到的内容 |
| --- | --- |
| `dist/internal/core.js:14` | `effectVariance = { _A: identity, _E: identity, _R: identity }`：A/E/R 在运行时只是恒等函数 |
| `dist/internal/core.js:71` | `EffectProto` 带 `[Symbol.iterator]() { return new SingleShotGen(this) }` |
| `dist/Utils.js:37` | `SingleShotGen.next(a)`：第一次返回 `{ value: this.value, done: false }`，之后返回 `{ value: a, done: true }` |
| `dist/internal/effect.js:321` | `FiberImpl`：字段包括 `_stack`、`context`、`interruptible`、`_interruptedCause` |
| `dist/internal/effect.js:430` | `runLoop`：`while (true)` 中执行 `current = current[evaluate](this)`；返回 `Yield` 时退出循环 |
| `dist/internal/effect.js:479` | `getCont(symbol)`：从 `_stack` 弹出帧，跳过不带 `contA` / `contE` 的帧 |
| `dist/internal/effect.js:367` | `interruptUnsafe`：可中断且正在运行时设 `_deferredInterrupt`，挂起时直接 `evaluate(failCause(...))` |
| `dist/internal/effect.js:797` | `callbackOptions`：注册回调后返回 `Yield`；`tryPromise` 只在 `try` 函数声明了参数时创建 `AbortController` |
| `dist/internal/effect.js:855`、`:973` | `gen` 调用 `fromIteratorUnsafe`；后者在 `contA` 中调用 `iter.next(value)`，未结束时把自己压回 `_stack` |
| `dist/internal/effect.js:1990` | `uninterruptible`：设 `fiber.interruptible = false` 并压入 `setInterruptibleTrue` 帧 |
| `dist/internal/effect.js:1815`、`:1833` | `scoped` 新建 Scope 放入 context，退出时 `scopeCloseUnsafe`；`acquireRelease` 在 `uninterruptibleMask` 中执行 acquire 并 `scopeAddFinalizerExit` |
| `dist/internal/effect.js:2452` | `forkIn` 把"中断子 fiber"登记为 Scope 的 finalizer |
| `dist/internal/effect.js:2535` | `runPromiseWith`：Exit 为 Failure 时 `throw causeSquash(exit.cause)` |
| `dist/Scheduler.js:219` | `MaxOpsBeforeYield` 默认值 2048 |
| `dist/Context.js:68`、`:89` | `Service` 创建 `function KeyClass() {}` 并 `Object.setPrototypeOf(KeyClass, ServiceProto)`；`ServiceProto.evaluate(fiber)` 返回 `exitSucceed(get(fiber.context, this))` |
| `dist/Layer.js:945` | `provideWith(self, that, f)`：先 build `that` 得到 context，再在其中 build `self`；`provide` 用 `identity`，`provideMerge` 用 `Context.merge(that, self)` |

### 类型定义

| 位置 | 内容 |
| --- | --- |
| `dist/Effect.d.ts:84` | `interface Effect<out A, out E = never, out R = never>`，带 `[Symbol.iterator](): EffectIterator<Effect<A, E, R>>` |
| `dist/Effect.d.ts:208` | `EffectIterator<T>.next(...args: ReadonlyArray<any>): IteratorResult<T, Success<T>>` |
| `dist/Effect.d.ts:1950` | `gen: <Eff extends Effect<any, any, any>, AEff>(f: () => Generator<Eff, AEff, never>) => Effect<AEff, [Eff] extends [Effect<infer _A, infer E, infer _R>] ? E : never, …R…>` |
| `dist/Context.d.ts:61` | `interface Key<out Identifier, out Shape> extends Effect<Shape, never, Identifier>` |

### agent-kit

- [`docs/architecture/authoring.md#L200`](https://github.com/PerfectPan/agent-kit/blob/e7396c50a7cb50cd8011651d8886b2fe440e8f1c/docs/architecture/authoring.md#L200)：普通 TS 模块只有在需要实时跟随、文件监听、后台刷新索引或带背压的并发扫描时才迁到 Effect。
- [`docs/architecture/authoring.md#L214`](https://github.com/PerfectPan/agent-kit/blob/e7396c50a7cb50cd8011651d8886b2fe440e8f1c/docs/architecture/authoring.md#L214)：端口一律写成类形式的 `Context.Service`。
- [`ledger-session.ts#L82`](https://github.com/PerfectPan/agent-kit/blob/e7396c50a7cb50cd8011651d8886b2fe440e8f1c/packages/harness/src/application/services/ledger-session.ts#L82)：`saveLedger` 用 `Effect.uninterruptible` 包住写入；[`#L128`](https://github.com/PerfectPan/agent-kit/blob/e7396c50a7cb50cd8011651d8886b2fe440e8f1c/packages/harness/src/application/services/ledger-session.ts#L128) `lockLedger` 的 R 含 `Scope.Scope`。
- [`apply-install.ts#L328`](https://github.com/PerfectPan/agent-kit/blob/e7396c50a7cb50cd8011651d8886b2fe440e8f1c/packages/harness/src/application/use-cases/apply-install.ts#L328)：`applyInstall` 用 `Effect.scoped` 包住整个安装过程。
- [`lease-manager.ts#L276`](https://github.com/PerfectPan/agent-kit/blob/e7396c50a7cb50cd8011651d8886b2fe440e8f1c/packages/agent-kit-collab/src/lease/application/use-cases/lease-manager.ts#L276)：租约心跳用 `Effect.forkScoped`。

## 验证记录

环境：Node.js v24.18.0，TypeScript 5.9.3（`strict`），effect 4.0.5，@effect/atom-react 4.0.5，React 19.3.1，@tanstack/react-query 5.104.4，esbuild 0.25。

### async/await 与 Effect 的六组对比（Node.js 实际运行）

| 场景 | async/await | Effect |
| --- | --- | --- |
| 创建即执行 | 创建 Promise 后请求次数 1 | 创建 `Effect.tryPromise` 后请求次数 0 |
| 重试 3 次 | `retryP(() => fetch(), 3)` 请求 4 次 | `Effect.retry({ times: 3 })` 请求 4 次 |
| 失败类型 | `catch (e)` 中 `e` 为 `unknown` | `Effect<User, NotFound \| NetworkError>` 经 `catchTag("NotFound")` 变为 `Effect<User \| null, NetworkError>` |
| 漏提供服务 | 无编译检查 | 只提供 Http、漏 Logger：编译报错 `Type 'Logger' is not assignable to type 'never'` |
| 取消（中间层漏传 signal） | 53ms 取消，请求仍在 202ms 完成 | 304ms 取消，305ms 底层请求被 abort，Exit 为 Interrupt |
| 锁 + 100ms 超时，写入需 300ms | 102ms 释放锁，303ms 写入落盘 | 303ms 写入落盘，306ms 释放锁，Exit 为 TimeoutError |
| 三个并发任务，A 在 50ms 失败 | B、C 在 202ms、302ms 仍然完成 | B、C 在 53ms 被取消 |

### 同一需求的两种写法

需求：2 秒超时；网络错误最多重试 3 次、间隔 100ms；404 不重试；可取消；测试时替换 HTTP。普通版 `loadUser` 本体 32 行，Effect 版 10 行。用同一个假 HTTP 跑五个场景（第 3 次才成功、一直网络错误、404、请求卡住、50ms 取消），两版的结果、请求次数和 abort 行为一致；普通版取消时抛出调用方的 `signal.reason`，Effect 版 Exit 为 Interrupt。

### 包体（esbuild `--bundle --minify --format=esm --platform=browser`，`gzip -9`）

| 入口 | 压缩后 | gzip |
| --- | --- | --- |
| 普通版 `loadUser` | 807 B | 472 B |
| 只调用 `Effect.runPromise(Effect.succeed(1))` | 25131 B | 8958 B |
| Effect 版 `loadUser` + `HttpLive` + `runPromiseExit` | 46516 B | 16383 B |

### 每步开销（20 万步，7 次取中位数）

| 写法 | 每步 |
| --- | --- |
| 普通函数调用 | 0.4 ns |
| async/await 每步 await 一次 | 27.5 ns |
| `yield* Effect.succeed` + `runSync` | 31.7 ns |
| `yield* Effect.sync` + `runSync` | 51.9 ns |
| `yield* Effect.sync` + `runPromise` | 61.4 ns |

### 类型与运行时细节

- `yield* Users`（`class Users extends Context.Service<Users, Shape>()("app/Users")`）推导为 Shape，交出的 Effect 为 `Effect<Shape, never, Users>`。运行时 `typeof Users === "function"`、`Users.key === "app/Users"`、`Effect.isEffect(Users) === true`；`Users[Symbol.iterator]()` 是 `SingleShotGen`，第一次 `next()` 交出 `Users` 本身，`next(impl)` 返回 `{ done: true, value: impl }`。未提供时运行结果为 `Die: Service not found: app/Users`。
- 函数写法 `Context.Service<Counter>("A")` 与 `Context.Service<Counter>("B")` 的 R 都是 `Counter`：给需要 A 的程序提供 B，类型变成 `Effect<number, never, never>`，编译通过，运行时 `Die: Service not found: A`。类写法 `C1`、`C2` 提供错时 R 仍为 `C1`。
- `Effect.gen` 中写 `yield Users`（少写 `*`）：tsc 0 个诊断，`users: never`，程序类型为 `Effect<never, never, Users>`；运行时仍拿到实现对象。effect-tsgo 0.50.0 二进制中包含规则名 `missingStarInYieldEffectGen`（未单独运行该规则）。
- `if (user === undefined) yield* Effect.fail(...)` 不写 `return` 时，后续 `user.name` 报 `'user' is possibly 'undefined'`。
- `runPromise` 失败时 reject 的就是 E 对象本身（实测 `{"_tag":"TodoNotFound","id":7}`）。
- `acquireRelease` + `scoped`：成功、中途失败、100ms 超时中断三种结束方式，都按"打开 a → 打开 b → 关闭 b → 关闭 a"执行；`openFile` 的类型为 `Effect<string, never, Scope>`，`Effect.scoped` 后 R 为 `never`。
- @effect/atom-react：`Atom.runtime(Layer)`、`appRuntime.atom(effect)`、`Atom.family`、`useAtomValue`、`AsyncResult.builder(...).onErrorTag(...)` 示例在 React 19.3 下 tsc 通过；用 `AtomRegistry.mount` 再 unmount，atom 通过 `acquireRelease` 获取的资源被释放。Atom 模块在 4.0 标为 `@stability unstable`。

## 未覆盖

- 未在浏览器中运行 React 示例，只做了类型检查和 Node.js 中的 AtomRegistry 验证。
- 每步开销是单机微基准，只用于量级比较。
- 未阅读 Effect 的 tracing、metrics、调度器分发的完整实现。
