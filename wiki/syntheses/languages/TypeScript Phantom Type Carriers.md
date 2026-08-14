---
title: TypeScript Phantom Type Carriers
description: TypeScript 运行时和编译时之间的类型信息桥——通过 phantom type 字段在跨模块（服务端→客户端、配置→消费处）传递类型信息，零运行时开销
type: synthesis
category: languages
created: 2026-07-26
updated: 2026-07-26
tags:
  - typescript
  - phantom-type
  - type-inference
  - better-auth
  - tanstack
source_refs:
  - better-auth: plugins/additional-fields/client.d.mts, client/types.d.mts, types/helper.d.mts
  - "@tanstack/start-client-core: createServerFn.d.ts, createMiddleware.d.ts"
  - "@tanstack/router-core: link.d.ts, route.d.ts, routeInfo.d.ts"
resource:
  - better-auth: plugins/additional-fields/client.d.mts, client/types.d.mts, types/helper.d.mts
  - "@tanstack/start-client-core: createServerFn.d.ts, createMiddleware.d.ts"
  - "@tanstack/router-core: link.d.ts, route.d.ts, routeInfo.d.ts"
timestamp: 2026-07-26
---

# TypeScript Phantom Type Carriers

## 第一性原理

TypeScript 本质上是**两层计算**：

```
运行时层（JavaScript）              编译时层（TypeScript 类型系统）
──────────────────────              ──────────────────────────────
对象、函数、类的字面量值            类型、泛型、条件类型
在浏览器/server 里执行              在 tsc/vite 编译时被求值，然后擦除
两层之间的信息不能直接互通
```

**Phantom type carrier** 就是在这两层之间搭桥：在运行时对象上声明一个字段（比如 `$InferServerPlugin` 或 `'~types'`），运行时它永远是 `{}` 或 `undefined`，但在 `.d.ts` 类型声明里，编译器知道这个字段承载了丰富的类型信息。**运行时看不到、编译时打通。**

用伪代码表达：

```
对象 { $X: {} }           ← 运行时：空对象，0 开销
类型 { $X: { a: string } } ← 编译时：满载类型信息
```

这个思想本身不新——Haskell 的 phantom type parameter 早就用了——但在 TypeScript 里，它与泛型函数、条件类型、`infer` 组合后，变成了一种可工程化的全栈类型传递技术。

---

## 定义

一个 Phantom Type Carrier 满足三个条件：

1. **运行时值** 是一个无业务含义的占位符（`{}`、`undefined`、或 `unique symbol`）
2. **类型声明** 在该字段上附着结构化的类型信息（通过泛型参数投影到字段类型上）
3. **消费方** 通过 TypeScript 的 `infer` / 条件类型 / 索引类型从 phantom 字段中提取信息，合并到自己的类型系统中

三条流水线：**值 → key → type**。值永远是空壳，key 是钩子，type 是内容。

---

## 案例一：干净版本 — Better Auth 的 `$InferServerPlugin`

### 问题

服务端声明了 `role` 字段，客户端 `useSession()` 不知道有这个字段。

```ts
// 服务端
export const auth = betterAuth({
  user: { additionalFields: { role: { type: 'string', defaultValue: 'member' } } }
});

// 客户端
authClient.useSession().user.role; // 类型报错：User 上没有 role
```

### Phantom carrier 的实现

**运行时**（`.mjs`）—— 4 行：

```js
const inferAdditionalFields = (schema) => ({
  id: "additional-fields-client",
  version: "1.6.23",
  $InferServerPlugin: {}    // ← carrier 字段，值是空的
});
```

**类型声明**（`.d.mts`）—— 核心 5 行：

```ts
declare const inferAdditionalFields: <T>() => ({
  $InferServerPlugin: (
    T["options"]["user"] extends { additionalFields: infer U }
      ? { schema: { user: { fields: U } } }
      : { schema: { user: { fields: {} } } }
  )
});
```

三步：

1. `T` 是 `typeof auth`，泛型捕获了服务端完整配置类型
2. `infer U` 从 `additionalFields` 位置挖出字段元数据（`{ role: { type: 'string' } }`）
3. 计算结果投影到 `$InferServerPlugin` 的类型上

### 消费方如何读取

客户端 `createAuthClient` 的 `InferAdditionalFromClient` 类型：

```ts
type InferAdditionalFromClient<Options> =
  Options["plugins"][number] extends { $InferServerPlugin?: infer P }
    ? P extends { schema?: { user: { fields: infer Fields } } }
      ? InferDBFieldsOutput<Fields>   // { role: { type: 'string' } } → { role: string }
      : {}
    : {};

// 最终客户端类型
type User = BaseUser & InferAdditionalFromClient<...>;
// → { id, email, name, image, role: string }
```

**整个链路：服务端配置 → 泛型捕获 → infer 提取 → phantom field 承载 → 客户端 infer 反向读出 → 合并到消费方类型。**

---

## 案例二：增加链条 — TanStack Start 的 `'~types'`

### 差异

Better Auth 的 phantom carrier 承载的是"配置时的静态字段"。TanStack Start 需要承载"链式调用中动态累积的状态"——每加一个 `.inputValidator()` 或 `.handler()`，类型信息就要更新一次。

### 解决：步骤构建器

`createServerFn` 的返回类型是一个**联合类型**，每个成员对应链式调用的一个阶段：

```ts
type ServerFnBuilder =
  | ServerFnWithTypes<...>   // 基础形态
  | ServerFnValidator<...>   // .inputValidator() 可用
  | ServerFnHandler<...>;    // .handler() 可用
```

每个成员内部都有同一个 phantom carrier 字段：

```ts
interface ServerFnWithTypes<TMethod, TInput, TOutput> {
  readonly '~types': {
    method: TMethod;
    validator: TInput;   // 被 .inputValidator() 更新
    response: TOutput;   // 被 .handler() 更新
  };
}
```

切换阶段时，泛型参数被更新，返回新的 `ServerFnWithTypes` 实例：

```ts
const step1 = createServerFn({ method: 'POST' });
// step1['~types'].validator = undefined

const step2 = step1.inputValidator(z.object({ slug: z.string() }));
// step2['~types'].validator = { slug: string }   ← phantom 字段更新

const step3 = step2.handler(async ({ data }) => {
  return { ok: true };
});
// step3['~types'].response = { ok: boolean }     ← phantom 字段更新
```

### 额外技巧：品牌符号

最终 `.handler()` 返回的 `Fetcher` 对象上还有一个 `TSS_SERVER_FUNCTION` brand（`unique symbol`），用于运行时 RPC 序列化层识别它：

```ts
type Fetcher = {
  [TSS_SERVER_FUNCTION]: true; // brand: 告诉 RPC 层这是 server function
  (payload: TInput): Promise<TOutput>;
};
```

品牌符号是 phantom carrier 在"运行时值"维度的延伸——不只是空值，还承载了一个运行时角色（被 RPC 层识别）。但核心的输入/输出类型推导仍然走 `'~types'` phantom 字段。

---

## 案例三：增加代码生成 — TanStack Router

### 为什么两个技巧不够

路由的类型信息来源是**文件系统**（`routes/blog/$slug.tsx`）。TypeScript 的类型系统读不到文件系统，所以"纯类型技巧"走不通。TanStack Router 用代码生成弥补：

1. **构建时**：Vite 插件扫描 `routes/` 目录 → 生成 `routeTree.gen.ts`
2. **编译时**：模板字面量类型解析 `$slug` 语法
3. **消费时**：路由树联合类型 + `RouteById` 筛选

### 第一层：模板字面量做字符串解析

```ts
// link.d.ts — 纯类型层面的字符串解析
type ParsePathParams<TPath extends string> =
  TPath extends `${infer Before}$${infer After}`
    ? ... // 遇到 $ → 提取后面的标识符作为 param 名
    : ...;

// ParsePathParams<'/blog/$slug/{category}'> → { slug: string; category?: string }
```

`infer` 用在字符串模式匹配上：`${infer Before}$${infer After}` 找到第一个 `$` 并切割字符串。

### 第二层：代码生成固化路由树

```ts
// routeTree.gen.ts（构建时自动生成）
export interface FileRoutesByFullPath {
  '/blog/$slug': typeof RouteImport_3;  // 指向 routes/blog/$slug.tsx 的模块类型
}
```

`typeof RouteImport_3` 拿到了该路由的 `validateSearch`、`loader` 结果等全部类型信息。这一步**不可被类型推导替代**，因为文件系统的信息不在 TypeScript 的认知范围内。

### 第三层：联合类型筛选

```ts
// routeInfo.d.ts
type RouteById<TRouteTree, TId> =
  TRouteTree extends { id: TId; types: any } ? TRouteTree : never;
```

利用分布式条件类型从路由树联合（所有路由类型的 `union`）里筛出匹配的那一个：

```ts
// useParams 内部做的事
RouteById<TRouteTree, '/blog/$slug'>['types']['allParams']
// → { slug: string }
```

### 这个案例的 phantom carrier 在哪

不在单个字段上，而在**代码生成架构**里——`routeTree.gen.ts` 就是编译时的类型信息载体，运行时根本不存在这个文件里的类型声明。载体从"字段"升级成了"文件"。

---

## 三种模式的本质

| | Better Auth | TanStack Start | TanStack Router |
|---|---|---|---|
| **Carrier 形态** | 单字段 `$InferServerPlugin` | 单字段 `'~types'` + 品牌符号 | 代码生成文件 `routeTree.gen.ts` |
| **静态 vs 动态** | 静态配置 | 链式调用的阶段状态 | 文件系统（不可被类型推导表达） |
| **运行时成本** | 空对象 `{}` | 品牌符号对象 | 0（生产代码不包含生成文件的内容） |
| **核心 TS 技巧** | `infer` + 条件类型 | 泛型步骤链 + phantom 字段 | 模板字面量 `infer` + 联合类型筛选 |
| **复杂度来源** | 多字段合并 | 链式累积 | 文件系统 → 类型系统的翻译层 |
| **适用场景** | 配置 → 消费端的静态字段传递 | 步骤构建器的链式类型累积 | 任何"外部信息 → 类型信息"的映射 |

三个案例都在回答同一个问题：**怎么让编译时的类型信息跨过模块边界、不丢失、零运行时成本地传递？** 答案都在 phantom carrier——无论叫 `$InferServerPlugin`、`'~types'`、还是整个代码生成文件。

---

## 为什么这个技巧重要

1. **零运行时成本。** phantom field 的值永远是 `{}`，打包后不产生额外代码。类型计算在空中完成。
2. **单一真相源。** 类型信息只在声明处定义一次，自动流向所有消费方。不需要手动写 `interface ExtendedFoo extends Foo { ... }`。
3. **可审计。** 类型流是可追踪的（`infer U` → `schema.user.fields` → `InferUserFromClient`），不像运行时反射一样不可预测。
4. **已成为生态共识。** 虽然 TypeScript 没有原生 phantom type 的语法糖，但 Better Auth、TanStack、tRPC、Zod 等库都在用同一种思想各自实现——说明这种模式是当前最有效的全栈类型传递方案。

## 信任契约：`.d.ts` 和 JS 可以不一致

这一整套技巧能成立，依赖 TypeScript 设计里的一个基本事实：**`.d.ts` 声明文件是宣言式的，编译器不验证实现文件（`.js`/`.mjs`）是否真的满足声明。**

编译管道：

```
源码 .ts
├── 编译 → .mjs（运行时执行）
└── 生成 → .d.mts（类型系统读取）

外部项目 import 时：
├── TypeScript 读 .d.mts → 类型检查
└── 打包工具读 .mjs → 运行时
```

两个文件完全独立，TypeScript 不做交叉验证。这导致了 phantom carrier 的核心矛盾：

```
.d.mts 声称:
  $InferServerPlugin: { schema: { user: { fields: U } } }

.mjs 实际:
  $InferServerPlugin: {}   // 没有 schema
```

这条链路能运行，需要两个条件同时成立：

1. **TypeScript 不验证声明文件和实现文件的一致性**——这是 TypeScript 的设计选择，不是为了 phantom type 开的特例，而是 `.d.ts` 为第三方 JS 库提供类型标注这个场景本身就要求声明和实现解耦
2. **消费方永远在类型层面读 phantom field，不在运行时触碰它**——`InferAdditionalFromClient` 是纯类型计算（type alias），编译后完全擦除。产生的 JS 里没有任何 `.schema.user.fields` 的运行时属性访问路径

换句话说，这个模式是**一个信任契约，不是编译器强制保证的安全**。如果一个粗心的开发者写了：

```ts
const fields = plugin.$InferServerPlugin.schema.user.fields; // ← 运行时访问
```

这行在编译时通过类型检查（`.d.ts` 说 `schema` 存在），但运行时 `schema` 是 `undefined`，直接炸。所以 phantom carrier 的使用方必须遵守约定：**只在 type alias / interface 里通过条件类型 `infer` 读取，不生成任何运行时代码去碰这个字段。**

实际上，Better Auth 的消费端 `InferAdditionalFromClient` 在读取时也加了防御：

```ts
// client/types.d.mts
Plugin extends { $InferServerPlugin?: infer SP }   // $InferServerPlugin 标了 optional
  ? SP extends { schema?: infer Schema }            // schema 也标了 optional
    ? ...
```

生产端的类型声明说 `schema` 必选，但消费端读的时候加了 `?`。这不是不一致——这是**知道 phantom carrier 在运行时是空对象，所以消费端类型读取全部走 optional，即使生产端说必选。** 两边的不对齐是故意的，是这条技术路线的隐含契约。

## 相关页面

- [[TypeScript]]

## 来源指针

- Better Auth v1.6.23: `plugins/additional-fields/client.mjs`（运行时代码 4 行）、`client.d.mts`（类型声明 100 行）、`client/types.d.mts`（`InferUserFromClient`）、`types/helper.d.mts`（`UnionToIntersection` 等）
- `@tanstack/start-client-core`: `createServerFn.d.ts`（`ServerFnBuilder`、`ServerFnWithTypes`）、`createMiddleware.d.ts`（`IntersectAllValidatorInputs`）
- `@tanstack/router-core`: `link.d.ts`（`ParsePathParams`）、`route.d.ts`（`RouteTypes`）、`routeInfo.d.ts`（`RouteById`）
