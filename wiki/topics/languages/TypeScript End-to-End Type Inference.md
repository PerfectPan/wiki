---
title: TypeScript End-to-End Type Inference
description: 拆解全栈类型推导的核心技巧——通过 phantom type 字段和泛型链条，让服务端配置类型原封不动"流"到客户端，无需手动对齐前后端类型定义
type: topic
category: languages
status: seed
created: 2026-07-26
updated: 2026-07-26
tags:
  - typescript
  - type-inference
  - generic
  - better-auth
  - phantom-type
source_refs:
  - ~/Workspace/blog/node_modules/.pnpm/better-auth@1.6.23/node_modules/better-auth/dist/plugins/additional-fields/client.d.mts
  - ~/Workspace/blog/node_modules/.pnpm/better-auth@1.6.23/node_modules/better-auth/dist/plugins/additional-fields/client.mjs
  - ~/Workspace/blog/node_modules/.pnpm/better-auth@1.6.23/node_modules/better-auth/dist/client/types.d.mts
  - ~/Workspace/blog/node_modules/.pnpm/better-auth@1.6.23/node_modules/better-auth/dist/types/helper.d.mts
  - ~/Workspace/blog/apps/web/src/lib/auth.ts
  - ~/Workspace/blog/apps/web/src/lib/auth-client.ts
resource:
  - ~/Workspace/blog/node_modules/.pnpm/better-auth@1.6.23/node_modules/better-auth/dist/plugins/additional-fields/client.d.mts
  - ~/Workspace/blog/node_modules/.pnpm/better-auth@1.6.23/node_modules/better-auth/dist/plugins/additional-fields/client.mjs
  - ~/Workspace/blog/node_modules/.pnpm/better-auth@1.6.23/node_modules/better-auth/dist/client/types.d.mts
  - ~/Workspace/blog/node_modules/.pnpm/better-auth@1.6.23/node_modules/better-auth/dist/types/helper.d.mts
  - ~/Workspace/blog/apps/web/src/lib/auth.ts
  - ~/Workspace/blog/apps/web/src/lib/auth-client.ts
timestamp: 2026-07-26
---

# TypeScript End-to-End Type Inference

## 摘要

全栈 TypeScript 应用里一个经典痛点：服务端声明了某个字段（比如 `user.role`），客户端调 `useSession()` 时却不知道有这个字段，得手动声明类型对齐。Better Auth 的 `inferAdditionalFields` 插件用一套"phantom type + 泛型链条"的技巧解决了这个问题：服务端配置的类型信息通过编译时的类型计算，原封不动传递到客户端，整个过程不产生任何运行时代码。

## 问题

服务端 auth 配置里扩展了一个 `role` 字段：

```ts
// auth.ts (服务端)
export const auth = betterAuth({
  user: {
    additionalFields: {
      role: { type: 'string', defaultValue: 'member', input: false }
    }
  }
});
```

客户端怎么知道 `useSession()` 返回的 user 对象有 `role` 字段？如果不做任何处理：

```ts
// auth-client.ts (客户端)
const { data } = authClient.useSession();
data.user.role; // ❌ 类型报错：User 上不存在 role
```

需要一种机制让服务端声明的类型"流"到客户端。

## 简答

核心机制：**服务端用 `typeof` 捕获泛型函数的返回值类型，通过一个类型层面的"钩子字段"（`$InferServerPlugin`）将配置里的字段信息编码进插件对象中。客户端创建 `createAuthClient` 时读取这个钩子字段，用条件类型和 `infer` 把字段信息从服务端配置里提取出来，最终合并到客户端 User/Session 类型上。**

运行时代码只有 4 行，类型计算全部在编译阶段完成。

## 完整链路拆解

以 Better Auth 的 `inferAdditionalFields` 为具体案例，从服务端到客户端走完完整链条。

### Step 1: 服务端 `betterAuth` 是泛型函数

```ts
// 简化后的函数签名
declare const betterAuth: <Options extends BetterAuthOptions>(
  options: Options
) => Auth<Options>;
```

你传入的配置对象被 TypeScript 准确捕获为类型 `Options`。返回的 `Auth<Options>` **内部保留了这个 `Options`**，后续可以用 `typeof` 重新访问到它：

```ts
export const auth = betterAuth({ ... });
// typeof auth = Auth<具体的 Options>
// 其中 Options 包含:
//   user: { additionalFields: { role: { type: 'string', defaultValue: 'member' } } }
```

### Step 2: `typeof auth` 捕获具体类型

```ts
// auth-client.ts
import type { auth } from './auth.js';

// typeof auth 就是 Auth<Options>
// 这个类型提供了整个服务端 auth 配置的完整类型信息
```

`typeof` 在这里的关键作用是：**把运行时的 JavaScript 变量 `auth` 转换成编译时的 TypeScript 类型**。泛型函数返回的 `Auth<Options>` 不会丢失 `Options` 的信息。

### Step 3: `inferAdditionalFields` — 用 infer 挖出 additionalFields

这是整个技巧的核心。先看运行时代码：

```js
// client.mjs — 运行时代码（4 行）
const inferAdditionalFields = (schema) => {
    return {
        id: "additional-fields-client",
        version: "1.6.23",
        $InferServerPlugin: {}    // ← 空对象！
    };
};
```

运行时它就是返回一个带空对象标记的普通插件。所有类型计算都在类型声明文件里：

```ts
// client.d.mts — 类型声明（精简后）
declare const inferAdditionalFields: <T>(schema?) => ({
  $InferServerPlugin: (
    // 第一步：从 T 里拿到 BetterAuthOptions
    T extends { options: BetterAuthOptions }
      ? T["options"]      // ← Auth 对象取 .options
      : never
  )["user"] extends { additionalFields: infer U }
    ? {
        schema: {
          user: { fields: U }   // U = { role: { type: 'string', ... } }
        }
      }
    : { schema: { user: { fields: {} } } }
});
```

分步理解：

**第一步：拿到原始配置。**

你把 `typeof auth` 传给 `inferAdditionalFields`，它检查 `T extends { options: BetterAuthOptions }` — 是的，`Auth<Options>` 内部有 `options` 字段，取出 `T["options"]`，获得完整的 `BetterAuthOptions` 类型。

**第二步：用 `infer` 提取子结构。**

```ts
options["user"] extends { additionalFields: infer U } ? U : {}
```

TypeScript 的条件类型和 `infer` 关键字一起使用，可以从一个复杂类型中"挖出"某个位置的子类型。这里就是：如果 `user` 属性里存在 `additionalFields`，就把它的类型绑定到 `U`，然后用到 `schema.user.fields` 里。

**第三步：输出 schema 对象。**

最终的类型计算结果是：

```ts
$InferServerPlugin: {
  schema: {
    user: { fields: { role: { type: 'string', defaultValue: 'member', input: false } } }
  }
}
```

这个类型信息被"焊"在了插件对象的类型声明上。

### Step 4: 类型桥 — `$InferServerPlugin` 的作用

Better Auth 的插件系统约定了一条规则：**服务端插件可以在 `$InferServerPlugin` 字段上附着类型信息，客户端 `createAuthClient` 会通过 `InferAdditionalFromClient` 读取这些信息**。

这不是运行时行为（运行时 `$InferServerPlugin` 就是 `{}`），而是 TypeScript 类型系统层面的约定。就像 JSON 是前后端的数据交换格式，`$InferServerPlugin` 是服务端和客户端插件之间的类型交换格式。

### Step 5: 客户端如何读取并合并类型

`createAuthClient` 内部用一系列类型工具读取插件信息并构建最终客户端的 User 类型。关键代码：

```ts
// client/types.d.mts（精简）

// 从插件数组里提取服务端声明的额外字段
type InferAdditionalFromClient<Options, Key extends string> =
  Options["plugins"] extends Array<infer Plugin>
    ? Plugin extends { $InferServerPlugin?: infer SP }
      ? SP extends { schema?: { user: { fields: infer Fields } } }
        ? Fields extends Record<string, DBFieldAttribute>
          ? InferDBFieldsOutput<Fields>   // 把 DBFieldAttribute 转成 TS 类型
          : {}
        : {}
      : {}
    : {};

// 客户端 User 类型 = Better Auth 内置字段 + 服务端额外字段
type InferUserFromClient<Options> =
  User                                            // { id, email, name, image }
  & UnionToIntersection<InferAdditionalFromClient<Options, "user">>
  // { role: string }
```

一步步走：

```
插件数组:
  [inferAdditionalFields<typeof auth>()]
       ↓
找到有 $InferServerPlugin 的插件
       ↓
取出 schema.user.fields
       ↓
{ role: { type: 'string', defaultValue: 'member' } }
       ↓
InferDBFieldsOutput 转换
       ↓
{ role: string }
       ↓
& 合并到 base User 类型上
       ↓
最终 User = { id, email, name, image, role }
```

### Step 6: `DBFieldAttribute` → 实际 TypeScript 类型

最后一步是把数据库字段的元描述转成 TypeScript 类型：

```ts
// DBFieldAttribute 的结构（概念上）
type DBFieldAttribute = {
  type: 'string' | 'number' | 'boolean' | ['admin', 'user']
  defaultValue?: unknown
  required?: boolean
  input?: boolean
  returned?: boolean
};

// InferDBFieldsOutput 的转换逻辑（概念上）
// { role: { type: 'string' } }         → { role: string }
// { age:  { type: 'number' } }         → { age: number }
// { role: { type: ['admin', 'user'] }} → { role: 'admin' | 'user' }
```

## 运行时 vs 编译时：双管线架构

这是这个技巧最精妙的部分——类型计算和代码执行完全分离：

```
                    编译时                                    运行时
              ┌──────────────────┐                     ┌──────────────────┐
              │ 100+ 行 .d.mts   │                     │ 4 行 .mjs         │
              │                  │       ts compile    │                  │
              │ 条件类型         │  ───────────────→   │ {                │
              │ infer 提取       │      类型擦除       │   id: "...",     │
              │ UnionToIntersect │                     │   version: "...",│
              │ 泛型推导         │                     │   $InferServer    │
              │                  │                     │     Plugin: {}   │
              │                  │                     │ }                │
              └──────────────────┘                     └──────────────────┘
              
              让 TypeScript 做：                         让 JavaScript 做：
              "推导出 user.role 是 string"               "把插件对象传给 createAuthClient"
```

TypeScript 编译器做完了所有类型计算，输出到 `editor.getTypeOf(user.role)` → `string`。JavaScript 打包器只打包那 4 行 `.mjs` 代码，类型声明文件不产生任何运行时代码。

## 用到的 TypeScript 高级特性

| 特性 | 作用 | 出现位置 |
|---|---|---|
| **泛型函数** `<Options>` | 捕获传入的完整配置类型 | `betterAuth()` 签名 |
| **`typeof`** | 将运行时变量转为编译时类型 | `typeof auth` |
| **条件类型** `T extends A ? X : Y` | 根据类型结构做分支 | 判断是否包含 `additionalFields` |
| **`infer`** | 从复杂结构中提取子类型 | `additionalFields: infer U` |
| **`UnionToIntersection`** | `A \| B` → `A & B` | 合并多个插件产生的字段 |
| **Mapped Types** | `{ [K in keyof T]: ... }` | `InferDBFieldsOutput` |
| **Tuple 递归** | `[infer Head, ...infer Tail]` | 遍历插件数组 |
| **`satisfies`** | 运行时不做类型转换，仅校验 | `authOptions satisfies BetterAuthOptions` |

## 为什么这个技巧重要

1. **告别手动类型对齐。** 不用在客户端写 `interface ExtendedUser extends User { role: string }`。服务端是唯一的类型来源，加一个字段两边自动同步。

2. **零运行时成本。** 所有计算都在 TypeScript 编译阶段完成，打包进浏览器的代码没有类型体操的痕迹。

3. **可复用模式。** 任何需要在"配置端"声明、在"消费端"享受类型安全的场景都适用——不只是 auth，RPC 框架（tRPC）、ORM、表单库（TanStack Form）都在用同样的思路。

4. **类型流和运行时流解耦。** `$InferServerPlugin` 在运行时是 `{}`，但在类型系统里是一个丰富的信息载体。这种"类型层面编程"是现代 TypeScript 库的主流范式。

## 相关页面

- [[TanStack Start Server Function Type Inference]]
- [[TanStack Router Type Inference]]
- [[TypeScript]]
- [[reflect-metadata]]

## 来源指针

- Better Auth 源码: `node_modules/better-auth/dist/plugins/additional-fields/client.mjs` — 运行时只有 4 行
- Better Auth 源码: `node_modules/better-auth/dist/plugins/additional-fields/client.d.mts` — 类型声明 100 行
- Better Auth 源码: `node_modules/better-auth/dist/client/types.d.mts` — 客户端 `InferUserFromClient` 定义
- Better Auth 源码: `node_modules/better-auth/dist/types/helper.d.mts` — `UnionToIntersection`、`ExtractPluginField` 等辅助类型
