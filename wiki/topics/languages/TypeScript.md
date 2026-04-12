---
title: TypeScript
type: topic
category: languages
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - typescript
source_refs:
  - raw/sources/TypeScript.md
---
# TypeScript

- 宝藏材料：https://github.com/microsoft/TypeScript/wiki
- 声明全局或局部变量（有 export / import 的话就说明文件是模块，定义变量是局部变量了，需要 declare global 如果要指定全局变量）：
	- `declare var/let/const` 声明变量/常量
	- `declare function` 声明函数
	- `declare class` 声明 class
	- `declare enum` 声明枚举变量
	- `declare namespace` 声明命名空间(空间下必须有属性才生效)
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
- 工具库：
	- pattern-match：https://github.com/gvergnaud/ts-pattern
	- https://github.com/sindresorhus/type-fest

## Source Pointers

- `raw/sources/TypeScript.md`

