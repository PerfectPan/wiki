---
title: TypeScript
description: TypeScript 类型集合观、声明与模块边界，以及 7.1 Content Mapper 如何把非 .ts 文件接入类型检查
type: topic
category: languages
created: 2026-04-12
updated: 2026-10-25
timestamp: 2026-10-25
tags:
  - typescript
  - content-mapper
source_refs:
  - raw/sources/typescript.md
  - raw/sources/reylo-typescript-content-mapper.md
  - https://devblogs.microsoft.com/typescript/announcing-typescript-7-1-beta/
  - https://github.com/microsoft/typescript-go/pull/4712
resource:
  - raw/sources/typescript.md
  - raw/sources/reylo-typescript-content-mapper.md
  - https://devblogs.microsoft.com/typescript/announcing-typescript-7-1-beta/
  - https://github.com/microsoft/typescript-go/pull/4712
---
# TypeScript

- 可以把类型先理解成“值的集合”
	- 子类型就是更小的值集合，父类型就是更大的值集合
	- `never` 可以理解为空集，`unknown` 可以理解为全集
- `{}` 在 TypeScript 4.8 之后更接近“任何非 null / undefined 的值”，不是“任意对象”
	- 如果想表达“普通对象”，`Record<string, unknown>` 往往比 `{}` 更贴切
- 宝藏材料：https://github.com/microsoft/TypeScript/wiki
- 声明全局或局部变量（有 export / import 的话就说明文件是模块，定义变量是局部变量了，需要 declare global 如果要指定全局变量）：
	- `declare var/let/const` 声明变量/常量
	- `declare function` 声明函数
	- `declare class` 声明 class
	- `declare enum` 声明枚举变量
	- `declare namespace` 声明命名空间(空间下必须有属性才生效)
	- `.d.ts` 文件一旦有 `import` 或 `export`，就会被当成模块文件，顶层声明默认不再进入全局作用域
	- 如果顶层声明既不是 `declare` 也不是 `export`，TypeScript 会直接报错
- 声明全局或局部类型：
	- `interface` 声明接口
	- `type` 声明类型别名
- 变量或类型的导入导出：
	- `export` 导出变量
	- `export namespace` 导出（含有子属性的）对象
	- `export default` ES6 默认导出
	- `export =` commonjs 导出模块
	- `export as namespace` UMD 库声明全局变量
- 扩展变量或模块：
	- `declare global` 在模块中声明全局变量或全局类型
	- `declare module` 声明模块或扩展模块
	- `/// <reference />` 三斜线指令引用声明文件（在全局声明文件里引入其他声明文件）
- `satisfies` 适合做“满足约束但不丢失当前推导结果”的校验
	- 它会验证表达式是否满足目标类型，但不会像直接写类型注解那样把表达式整体拓宽
	- 当对象既要校验 key / value 约束，又想保留字面量级别的推导时，比 `as` 或显式标注更稳妥
- `filter` 默认不会自动把 `Boolean` 之类的运行时判断当成类型收窄
	- 如果希望 `filter` 后得到更窄的数组类型，通常要写显式的 type predicate
	- 只想排除 `null | undefined` 时，可以写成 `item is NonNullable<typeof item>`
- monorepo 里使用 project references 时，如果子包路径都先被当成 `node_modules` 依赖，`paths` 可以把它们重新映射回仓库内源码路径，帮助 TypeScript 建立正确的项目引用关系
- 继承 `Error`、`Array` 这类内置类型时，如果产物需要降到 ES5，要额外留意原型链修复
	- ES5 没有 `new.target`，编译结果无法完整模拟 ES6 对内置类型子类化的语义
	- 常见补救方式是在构造函数里手动 `Object.setPrototypeOf(this, FooError.prototype)`
	- 这类问题不只影响 `Error`，凡是依赖内置类型子类化语义的场景，在老目标环境里都要优先怀疑原型链是否断了
- 工具库：
	- pattern-match：https://github.com/gvergnaud/ts-pattern
	- https://github.com/sindresorhus/type-fest

## Content Mapper（7.1）

### 本质

TypeScript 原来只认识自己能解析的文件。7.1 加了 Content Mapper（内容映射器）：遇到已登记扩展名时，不直接解析原文，而是启动外部进程，把文件内容交出去，再拿回一段可被 TypeScript 解析的虚拟文本，用来做类型检查。

外部进程还可以返回 span mapping（原文和虚拟文本的位置对照）。报错、hover、跳转就能落回 `.vue`、`.svelte`、`.sql` 等原文件里的正确位置。

它解决的是接入问题：非 TS 文件也能进入和 `tsc` 同一套编译流程，而不是只在编辑器里做一层嵌入。Content Mapper 本身不理解 SQL、Vue 或数据库；具体语义由各 mapper 实现方在 `transform` 里完成。

### 数据流

配置边界：

- `tsconfig.json` 的 `contentMappers` 登记：用哪个 `package`、处理哪些 `extensions`，可选 `options`。
- CLI 必须显式加 `--runExternalCode`，否则不会执行外部 mapper。编辑器要有 workspace trust 和 content mapper 权限；不可信工作区一般不会把这个开关传给 LSP。
- mapper 包在 `package.json` 的 `typescript.contentMapper` 里声明 `exec`（启动命令）；`compilerOptions` 和 `dynamicConfig` 是可选项。

一次 `transform` 大致这样走：

1. 模块解析或 `include` 遇到已注册扩展名。
2. TypeScript 按 `exec` 启动进程，通过 STDIO 跑 JSON-RPC：`initialize` → `openProject` → 对每个文件 `transform` → `closeProject`。
3. `transform` 返回虚拟文本 `text`、扩展名 `extension`，可选 `mappings` 和诊断。checker 与语言服务在虚拟文本上工作，诊断再映射回原文。
4. 被 mapper 接管的文件不会输出成 JavaScript。增量构建时，mapper 配置身份可写进 `.tsbuildinfo`；若用了 `dynamicConfig`，靠 `openProject` 返回的 `configIdentity` 与 `watchedFiles` 判断缓存是否仍可用。

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontFamily':'ui-sans-serif,system-ui,sans-serif','primaryColor':'#c9d9e8','primaryTextColor':'#1f2933','primaryBorderColor':'#6a8aaa','lineColor':'#6b7280','secondaryColor':'#e6d0c0','tertiaryColor':'#cfe0c8','mainBkg':'#c9d9e8','nodeBorder':'#6a8aaa','clusterBkg':'#eef3f7','clusterBorder':'#6a8aaa'}}}%%
flowchart LR
  A["非 .ts 文件<br/>.sql / .vue / .svelte"] --> B["tsc / tsserver<br/>识别已注册扩展名"]
  B --> C["content mapper 进程<br/>JSON-RPC transform"]
  C --> D["虚拟 .ts 模块"]
  D --> E["类型检查 / hover / 跳转<br/>诊断映射回原文件"]

  classDef src fill:#f0ebe3,stroke:#9a9080,color:#1f2933
  classDef host fill:#c9d9e8,stroke:#6a8aaa,color:#1f2933
  classDef mapper fill:#d8cce8,stroke:#7a6a9a,color:#1f2933
  classDef virt fill:#cfe0c8,stroke:#6f9468,color:#1f2933
  classDef check fill:#e6d0c0,stroke:#a67c5d,color:#1f2933
  class A src
  class B host
  class C mapper
  class D virt
  class E check
  linkStyle 0,1,2,3 stroke:#6a8aaa,stroke-width:2px
```

### 限制

- 没有 `--runExternalCode`（或编辑器未授信）时，mapper 不会跑。
- mapper 是可执行外部代码，只适合受信任工作区。
- 被映射的文件不 emit JS；若还要在运行时加载同扩展名文件，需要 bundler / loader 另开一条路。
- TypeScript 不替你推断领域类型（例如 SQL 的 Params / Row）；那是 mapper 实现的责任。

### 来源

- [Announcing TypeScript 7.1 Beta](https://devblogs.microsoft.com/typescript/announcing-typescript-7-1-beta/)
- [microsoft/typescript-go#4712](https://github.com/microsoft/typescript-go/pull/4712)
- [[raw/sources/reylo-typescript-content-mapper|核查记录]]（含 Content Mapper 与 Reylo 对照）

落地示例见 [[wiki/syntheses/languages/reylo-sql-import-typescript|Reylo：SQL import 进 TypeScript 的实现原理]]（开发库 PREPARE 推类型 + 运行时 loader）。

## 相关页面

- [[wiki/syntheses/languages/reylo-sql-import-typescript|Reylo：SQL import 进 TypeScript 的实现原理]]
- [[wiki/syntheses/languages/typescript-phantom-type-carriers|TypeScript Phantom Type Carriers]]

## Source Pointers

- `raw/sources/typescript.md`
- `raw/sources/reylo-typescript-content-mapper.md`
