---
title: TanStack Router Type Inference
description: 拆解 TanStack Router 如何通过模板字面量类型解析 + 代码生成 + 路由树类型游走三层机制，实现路径参数和搜索参数的全栈类型推导
type: topic
category: languages
status: seed
created: 2026-07-26
updated: 2026-07-26
tags:
  - typescript
  - type-inference
  - tanstack-router
  - template-literal-types
  - codegen
source_refs:
  - ~/Workspace/blog/apps/web/src/routeTree.gen.ts
  - ~/Workspace/blog/node_modules/.pnpm/@tanstack+router-core@1.171.14/node_modules/@tanstack/router-core/dist/esm/link.d.ts
  - ~/Workspace/blog/node_modules/.pnpm/@tanstack+router-core@1.171.14/node_modules/@tanstack/router-core/dist/esm/route.d.ts
  - ~/Workspace/blog/node_modules/.pnpm/@tanstack+router-core@1.171.14/node_modules/@tanstack/router-core/dist/esm/routeInfo.d.ts
resource:
  - ~/Workspace/blog/apps/web/src/routeTree.gen.ts
  - ~/Workspace/blog/node_modules/.pnpm/@tanstack+router-core@1.171.14/node_modules/@tanstack/router-core/dist/esm/link.d.ts
  - ~/Workspace/blog/node_modules/.pnpm/@tanstack+router-core@1.171.14/node_modules/@tanstack/router-core/dist/esm/route.d.ts
  - ~/Workspace/blog/node_modules/.pnpm/@tanstack+router-core@1.171.14/node_modules/@tanstack/router-core/dist/esm/routeInfo.d.ts
timestamp: 2026-07-26
---

# TanStack Router Type Inference

## 摘要

TanStack Router 的路由类型推导是三层机制的叠加：TypeScript 模板字面量类型在编译时解析文件路径（如 `/blog/$slug`），代码生成器在构建时将路由树固化为显式类型声明，`RouteById` 工具类型在路由树联合类型中按 id 查找并提取对应的 params 和 search 类型。最终用户写 `useParams({ from: '/blog/$slug' })` 就能获得精确的路径参数类型。

## 问题

一个基于文件系统的路由：

```
routes/
  blog/
    $slug.tsx       → 路径 /blog/:slug
  index.tsx          → 路径 /
```

在 `$slug.tsx` 里怎么知道 `slug` 是路径参数并获取它的类型？

```ts
// routes/blog/$slug.tsx
export const Route = createFileRoute('/blog/$slug')({
  component: PostPage,
});

function PostPage() {
  const { slug } = useParams({ from: '/blog/$slug' });
  // 为什么 slug 自动是 string 类型？怎么推导的？
}
```

更进一步，如果加了 search validator：

```ts
const searchSchema = z.object({ page: z.number().default(1) });

export const Route = createFileRoute('/blog/$slug')({
  validateSearch: searchSchema,
});

// 使用处
const { page } = useSearch({ from: '/blog/$slug' });
// page 怎么知道是 number 类型？
```

## 简答

路由类型推导分三层：

1. **模板字面量类型解析**（编译时）：`ParsePathParams<'/blog/$slug'>` 在 TypeScript 类型系统里做字符串解析，遇到 `$` 提取后面的标识符作为路径参数名，生成 `{ slug: string }`
2. **代码生成**（构建时）：TanStack Router 的 Vite 插件扫描 `routes/` 目录，解析文件名，生成 `routeTree.gen.ts`，将路由结构固化为显式的类型声明
3. **路由树类型游走**（调用时）：`RouteById` 类型工具从路由树联合类型中匹配路由 id，提取对应的 params/search/loader data 类型

## 第一层：模板字面量类型解析

TypeScript 4.1 引入了模板字面量类型（Template Literal Types），允许在类型层面操作字符串。TanStack Router 用这个特性实现了一个"类型级正则解析器"。

```ts
// 源码 link.d.ts（精简）

// 入口：解析路径字符串里的参数
type ParsePathParams<TPath extends string> =
  ParsePathParamsImpl<TPath, {}, {}, {}>;

// 具体解析逻辑：根据遇到的第一个特殊字符分发
type ParsePathParamsImpl<
  TPath extends string,
  TResult extends ParsePathParamsResult<...>,
> = TPath extends `${infer Before}$${infer After}`
  // 遇到 $ → 提取后面的参数名
  ? ParsePathParamsDollar<Before, After, TResult>
  : TPath extends `${infer Before}{${infer After}`
  // 遇到 { → 可选参数的开始
  ? ParsePathParamsOpenBrace<Before, After, TResult>
  : TPath extends `${infer Before}}${infer After}`
  // 遇到 } → 可选参数的结束
  ? ParsePathParamsCloseBrace<Before, After, TResult>
  : ... ;

// 结果类型
type ParsePathParamsResult<
  TRequired, TOptional, TRest
> = {
  required: TRequired;   // 必选参数名联合，如 'slug'
  optional: TOptional;   // 可选参数名联合
  rest: TRest;           // splat 参数
};
```

走一遍 `/blog/$slug` 的解析过程：

```
ParsePathParamsImpl<'/blog/$slug', {}, {}, {}>

→ 匹配 `${infer Before}$${infer After}`
    Before = '/blog/'
    After  = 'slug'

→ ParsePathParamsDollar<'/blog/', 'slug', {}>
    → 提取 'slug' 作为 required 参数
    → 返回 { required: 'slug', optional: never, rest: never }
```

模板字面量里的 `infer` 是在**字符串**上做模式匹配：`${infer X}$${infer Y}` 表示"在字符串里找到第一个 `$`，取出 `$` 前面的内容作为 X，后面的内容作为 Y"。

再走一遍更复杂的路径：

```
ParsePathParamsImpl<'/blog/$slug/{category}', {}, {}, {}>

→ 匹配 `$`：Before='/blog/', After='slug/{category}'
→ 提取 'slug'
→ 剩余 'slug/{category}'
→ 匹配 `{`：Before='slug/', After='category}'
→ 提取 'category' 作为 optional
→ 返回 { required: 'slug', optional: 'category', rest: never }
```

这样，最终 `useParams({ from: '/blog/$slug' })` 返回的 params 类型就是：

```ts
{ slug: string }
```

所有 params 值在 TypeScript 里都是 `string`（从 URL 解析出来的原始值）。

## 第二层：代码生成器固化为显式类型

模板字面量类型解析只能处理路径模式本身。但路由之间还有层级关系、加载器数据、搜索参数等——这些信息靠纯类型推导太复杂。所以 TanStack Router 在构建时生成 `routeTree.gen.ts`。

你的项目构建后会生成这个文件（`apps/web/src/routeTree.gen.ts`）：

```ts
// 自动生成的三个声明融合接口

export interface FileRoutesByFullPath {
  '/': typeof RouteImport_0;
  '/login': typeof RouteImport_1;
  '/blog': typeof RouteImport_2;
  '/blog/$slug': typeof RouteImport_3;
  '/projects': typeof RouteImport_4;
  // ...
}

export interface FileRoutesByTo {
  '/': typeof RouteImport_0;
  '/login': typeof RouteImport_1;
  '/blog': typeof RouteImport_2;
  '/blog/$slug': typeof RouteImport_3;
  // ...
}

export interface FileRoutesById {
  '__root__': typeof RouteImport_root;
  '/blog/$slug': typeof RouteImport_3;
  // ...
}
```

这三个接口使用 TypeScript 的**声明融合**（Declaration Merging）特性。`typeof RouteImport` 指向导入的路由模块，从而获得了每个路由文件导出的 `Route` 类型（包括它的 `validateSearch`、`loader` 等所有配置信息）。

代码生成器（Vite 插件的 `tsr:generate`）做了这些事：
1. 扫描 `routes/` 目录，找出所有 `.tsx` 文件
2. 根据文件路径推导路由 ID（如 `/blog/$slug`）
3. 生成带 `import()` 的 `typeof RouteImport_*` 声明
4. 输出到 `routeTree.gen.ts`

## 第三层：路由树类型游走

用户调用 `useParams({ from: '/blog/$slug' })` 时，`from` 参数被约束为 `FileRoutesByTo` 的 key：

```ts
// useParams 的类型签名（精简）
function useParams<
  TRouter, TFrom extends keyof FileRoutesByTo, TStrict = true
>(opts: { from: TFrom; strict?: TStrict }): RouteById<TFrom>['params'];
```

`RouteById` 是核心类型工具（源码 `routeInfo.d.ts`）：

```ts
// 从路由树联合类型中按 id 查找路由
type RouteById<TRouteTree, TId> =
  TRouteTree extends { id: TId; types: any }
    ? TRouteTree
    : never;
```

`TRouteTree` 是一个巨大的联合类型——所有路由类型的求和。`extends { id: TId }` 从里面筛选出 `id === TId` 的那一个子类型，然后读出它的 `types.allParams`：

```ts
// 最终推导
RouteById<TRouteTree, '/blog/$slug'>['types']['allParams']
// → { slug: string }
```

对于搜索参数，逻辑一样但走 `types.fullSearchSchema`：

```ts
// useSearch 的类型签名
function useSearch(opts: { from: '/' }):
  RouteById<TRouteTree, '/'>['types']['fullSearchSchema'];

// 如果路由有 validateSearch(searchSchema)，则
// fullSearchSchema = z.infer<typeof searchSchema>
// → { page: number }
```

## 完整示例走一遍

你的项目里有 `routes/blog/$slug.tsx`：

```ts
// routes/blog/$slug.tsx
import { z } from 'zod';

const searchSchema = z.object({
  page: z.number().optional().default(1),
});

export const Route = createFileRoute('/blog/$slug')({
  validateSearch: searchSchema,
  loader: async ({ params }) => {
    // params.slug → 类型安全 ✅
    const post = await getBlogPostServerFn({ data: { slug: params.slug } });
    return { post };
  },
  component: PostPage,
});

function PostPage() {
  const { slug } = useParams({ from: '/blog/$slug' });
  // slug: string ✅

  const { page } = useSearch({ from: '/blog/$slug' });
  // page: number ✅

  const { post } = useLoaderData({ from: '/blog/$slug' });
  // post: PostDetail | null ✅ — 来自 loader 返回值

  return <div>{post?.title}</div>;
}
```

每一个 router hook 都通过 `RouteById` 类型工具精确提取对应路由的类型信息，零运行时开销。

## 与其他模式的对比

| | Better Auth | TanStack Start Fn | TanStack Router |
|---|---|---|---|
| **类型来源** | 配置对象 | Zod schema | 文件名 + 代码生成 |
| **桥接机制** | `$InferServerPlugin` | `'~types'` phantom | 代码生成 + `RouteById` |
| **类型技巧** | `infer` + 条件类型 | 步骤构建器 + phantom | 模板字面量 infer + 联合类型筛选 |
| **构建时角色** | 无 | 无 | 代码生成是核心环节 |

## 为什么需要代码生成

TanStack Router 是三个模式里唯一**必须依赖构建时代码生成**的。原因：

1. **路由树可能很大**——完全靠 TypeScript 类型推导大型路由树的层级关系，编译时间不可接受
2. **文件系统信息**——TypeScript 无法在类型层面感知文件系统，必须由构建工具扫描并生成
3. **声明融合**——`FileRoutesByPath` 等接口需要在构建时显式声明，利用 TypeScript 的 declaration merging 特性

代码生成不是"偷懒"，是这个场景下唯一的可行方案。tRPC 里没有代码生成是因为它的路由定义是纯 JS/TS 代码（不需要文件系统扫描）。

## 相关页面

- [[TypeScript End-to-End Type Inference]]
- [[TanStack Start Server Function Type Inference]]

## 来源指针

- 项目代码: `apps/web/src/routeTree.gen.ts` — 自动生成的路由树类型
- TanStack Router 源码: `link.d.ts` — `ParsePathParams` 模板字面量解析
- TanStack Router 源码: `route.d.ts` — `RouteTypes`, `ResolveAllParamsFromParent` 定义
- TanStack Router 源码: `routeInfo.d.ts` — `RouteById` 类型工具
