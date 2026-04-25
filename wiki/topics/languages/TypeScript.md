---
title: TypeScript
type: topic
category: languages
status: seed
created: 2026-04-12
updated: 2026-04-25
tags:
  - typescript
source_refs:
  - raw/sources/TypeScript.md
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

## Source Pointers

- `raw/sources/TypeScript.md`
