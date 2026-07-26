---
title: TanStack Start Server Function Type Inference
description: 拆解 createServerFn 如何通过步骤构建器 + phantom '~types' 字段实现全栈类型推导——input validator 和 handler 的类型自动流向客户端调用处
type: topic
category: languages
status: seed
created: 2026-07-26
updated: 2026-07-26
tags:
  - typescript
  - type-inference
  - tanstack-start
  - phantom-type
  - server-functions
source_refs:
  - ~/Workspace/blog/apps/web/src/lib/admin-service.ts
  - ~/Workspace/blog/node_modules/.pnpm/@tanstack+start-client-core@1.170.13/node_modules/@tanstack/start-client-core/dist/esm/createServerFn.d.ts
  - ~/Workspace/blog/node_modules/.pnpm/@tanstack+start-client-core@1.170.13/node_modules/@tanstack/start-client-core/dist/esm/createMiddleware.d.ts
resource:
  - ~/Workspace/blog/apps/web/src/lib/admin-service.ts
  - ~/Workspace/blog/node_modules/.pnpm/@tanstack+start-client-core@1.170.13/node_modules/@tanstack/start-client-core/dist/esm/createServerFn.d.ts
  - ~/Workspace/blog/node_modules/.pnpm/@tanstack+start-client-core@1.170.13/node_modules/@tanstack/start-client-core/dist/esm/createMiddleware.d.ts
timestamp: 2026-07-26
---

# TanStack Start Server Function Type Inference

## 摘要

TanStack Start 的 `createServerFn` 是全栈类型推导的典型实现——服务端定义 input validator 和 handler，客户端调用时自动获得参数补全和返回值类型。核心机制是用 phantom `'~types'` 字段在步骤构建器（step builder）的链式调用中累积类型信息，最终通过 `TSS_SERVER_FUNCTION` 品牌符号注入到客户端调用的 Fetcher 中。

## 问题

一个 Server Function 长这样：

```ts
import { z } from 'zod';

const schema = z.object({
  slug: z.string().min(1),
  title: z.string().min(1),
});

export const upsertPost = createServerFn({ method: 'POST' })
  .inputValidator(schema)                 // 服务端校验
  .handler(async ({ data }) => {          // data 怎么知道是 schema 的类型？
    // ...
    return { ok: true, slug: data.slug };
  });

// 前端调用
const result = await upsertPost({ data: { slug: 'hello', title: 'Title' } });
//                                      ↑ 怎么自动补全 slug 和 title？
// result.ok       ↑ 怎么知道返回了 ok？
```

需要一种机制让 `createServerFn` 在每一步链式调用中累积类型信息，最终传递给客户端的调用入口。

## 简答

`createServerFn` 返回一个**步骤构建器**——一个联合类型，其中每个成员对应链式调用的一步。每一步返回新的构建器实例，其中泛型参数被更新。核心是通过 phantom `'~types'` 字段携带累积的类型信息。`.inputValidator()` 把 Zod schema 的输入/输出类型写入 phantom 字段；`.handler()` 把函数返回值类型写入；最终返回的 `Fetcher` 对象将所有累积的类型"固化为"客户端的调用签名。

## 完整链路拆解

### Step 1: `createServerFn` 返回步骤构建器

```ts
// 源码 createServerFn.d.ts（精简）
declare function createServerFn<TMethod extends 'GET' | 'POST'>(
  options: { method: TMethod }
): ServerFnBuilder<TRegister, TMethod, ...>;
```

`ServerFnBuilder` 是一个联合类型，包含四个接口：

```ts
type ServerFnBuilder<...> =
  | ServerFnWithTypes<...>     // 基础：携带类型镜像
  | ServerFnMiddleware<...>    // 支持 .middleware()
  | ServerFnValidator<...>     // 支持 .inputValidator()
  | ServerFnHandler<...>;      // 支持 .handler()
```

每个接口只暴露自己的链式方法。TypeScript 的联合类型让你可以调用其**所有成员的共有方法**——但只有当前步骤对应成员的返回值会被正确类型化。

### Step 2: phantom `'~types'` 字段

所有类型信息存储在一个**刻意不被运行时读取的字段**上：

```ts
// 源码 createServerFn.d.ts 第 114-130 行
interface ServerFnWithTypes<
  TRegister, TMethod, TMiddlewares,
  TInputValidator, TResponse,
  TAllInput, TAllOutput
> {
  readonly '~types': ServerFnTypes<
    TRegister, TMethod, TMiddlewares,
    TInputValidator, TResponse,
    TAllInput, TAllOutput
  >;
}

interface ServerFnTypes<...> {
  method: TMethod;             // 'GET' | 'POST'
  strict: TStrict;             // strict mode
  middlewares: TMiddlewares;   // 中间件数组
  validator: TInputValidator;  // 来自 .inputValidator()
  response: TResponse;         // 来自 handler 返回值
  allInput: TAllInput;         // 合并所有中间件的 input
  allOutput: TAllOutput;       // 合并所有中间件的 output
  allServerContext: TAllServerContext;
}
```

`'~types'` 用的引号括起来的字符串作为字段名，这是一种约定——它不可能是用户定义的类型字段，也没有运行时访问的价值。它的唯一作用就是在 TypeScript 类型系统里作为一个信息载体。

### Step 3: `.inputValidator()` —— 把 Zod schema 类型编码进去

```ts
const step1 = createServerFn({ method: 'POST' });
// step1['~types'].validator = undefined
// step1['~types'].response  = undefined

const step2 = step1.inputValidator(schema);
// step2['~types'].validator = z.infer<typeof schema>
// 现在 TypeScript 知道 input 是 { slug: string, title: string }

const step3 = step2.handler(async ({ data }) => {
  // data: { slug: string, title: string } ← 自动推导
  return { ok: true, slug: data.slug };
});
// step3['~types'].response = { ok: boolean, slug: string }
```

每一步调用返回一个新的 `ServerFnWithTypes` 实例，其中 `'~types'` 对应的泛型参数被更新。

### Step 4: `.handler()` —— 最终固化类型

`.handler(fn)` 返回的不是构建器，而是一个 `Fetcher` 对象：

```ts
// 源码 createServerFn.d.ts（精简）
.handler<TNewResponse>(fn: (ctx) => TNewResponse):
  Fetcher<TMiddlewares, TInputValidator, TNewResponse>;

// Fetcher 的核心签名
type Fetcher<...> = {
  // 携带 TSS_SERVER_FUNCTION 品牌符号——告诉 RPC 层这是 Server Function
  [TSS_SERVER_FUNCTION]: true;
  
  // 调用签名：如果所有 input 都是 undefined，可以不传参
  // 否则必须传 { data: TAllInput }
  (...args: ...): Promise<TResponse>;
};
```

`TSS_SERVER_FUNCTION` 是一个 `unique symbol`（源码 `constants.d.ts`）：

```ts
declare const TSS_SERVER_FUNCTION: unique symbol;
```

这个品牌符号有两个作用：
1. **运行时**：RPC 序列化层识别这是 Server Function，将其序列化为服务端调用
2. **编译时**：TypeScript 通过 `unique symbol` 识别出这是 Fetcher 类型，确保类型安全

### Step 5: 中间件链的递归类型累积

中间件是 Server Function 最复杂的类型部分。每个中间件有自己的 input validator 和 server context。当链式调用多个中间件时，需要递归合并类型：

```ts
// 源码 createMiddleware.d.ts（精简）

// 向中间件数组追加新中间件
type AppendMiddlewares<TExisting, TNew> =
  TExisting extends ReadonlyArray<any>
    ? ReadonlyArray<TNew, ...TExisting>   // 展开合并
    : TExisting;

// 递归遍历中间件数组，合并所有 input
type IntersectAllValidatorInputs<TMiddlewares extends ReadonlyArray<any>> =
  TMiddlewares extends readonly [infer T, ...infer Rest]
    ? IntersectAssign<
        T['~types']['allInput'],
        IntersectAllValidatorInputs<Rest>
      >
    : {};

// 递归遍历中间件数组，合并所有 output
type IntersectAllValidatorOutputs<TMiddlewares> =
  // 同样的递归模式，但取 allOutput
```

注意这里的递归模式：`[infer Head, ...infer Tail]` 取出数组头尾，对 Head 读取 phantom 字段，对 Tail 递归调用自身。这是 TypeScript 类型层面上的"fold left"。

## 运行时 vs 编译时

跟 Better Auth 的 `$InferServerPlugin` 一样，这些 phantom 类型在运行时完全不存在：

```
                                 编译时                        运行时
                          ┌────────────────────┐       ┌──────────────┐
                          │ '~types' 字段       │       │ 无 phantom   │
                          │ 包含 validator、    │ ts →  │ 字段         │
                          │ response、          │ erase │              │
                          │ middlewares 类型    │       │ 只是一个     │
                          │                    │       │ Fetcher 对象 │
                          └────────────────────┘       └──────────────┘
```

运行时 `Fetcher` 就是一个带有品牌符号的普通函数对象。当客户端调用它时，TanStack Start 的 RPC 序列化层识别出 `TSS_SERVER_FUNCTION` 符号，把调用序列化成一个 HTTP POST 请求发给服务端，反序列化后执行 handler，再把结果返回来。类型信息只在编译阶段发挥作用（编辑器补全、错误检查）。

## 与你项目中 Server Function 的对应关系

你的 `admin-service.ts` 就是一个标准使用：

```ts
// apps/web/src/lib/admin-service.ts

// Step 1: 声明 Fn
createServerFn({ method: 'POST' })
  // Step 2: 加 validator
  .inputValidator(upsertSchema)
  // → 编译器知道 input 是 { slug, title, description, ... }
  // Step 3: 加 handler
  .handler(async ({ data }) => {
    // data 全部自动补全 ✅
    await requireAdmin();  // 权限校验在 handler 内部
    await getD1().prepare(...).bind(...).run();
    return { ok: true, slug: data.slug };
  });

// 前端组件里
await upsertPostServerFn({
  data: { slug: 'hello', title: 'Title', ... }
  //      ↑ 自动补全，拼错就报错
});
```

## 总结

TanStack Start 的 `createServerFn` 和 Better Auth 的 `inferAdditionalFields` 使用同一个核心技巧：

1. **Phantom type 字段**（`'~types'` / `$InferServerPlugin`）作为类型信息的容器
2. **泛型参数链式传递**——每一步调用更新泛型参数，返回新的类型对象
3. **运行时原型无关**——phantom 字段不包含业务逻辑，只做类型层面的信息传递
4. **TypeScript 编译后全部擦除**——运行时无开销

区别在于 TanStack Start 增加了**步骤构建器模式**（`.inputValidator().handler()` 链式调用）和**中间件递归合并**，使类型推导能力更强大。

## 相关页面

- [[TypeScript End-to-End Type Inference]]
- [[TanStack Router Type Inference]]

## 来源指针

- 项目代码: `apps/web/src/lib/admin-service.ts` — 实际使用案例
- TanStack Start 源码: `@tanstack/start-client-core/dist/esm/createServerFn.d.ts` — `ServerFnBuilder`、`ServerFnWithTypes`、`Fetcher` 定义
- TanStack Start 源码: `@tanstack/start-client-core/dist/esm/createMiddleware.d.ts` — `IntersectAllValidatorInputs`、`AppendMiddlewares` 定义
- TanStack Start 源码: `@tanstack/start-client-core/dist/esm/constants.d.ts` — `TSS_SERVER_FUNCTION` brand symbol
