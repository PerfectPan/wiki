---
type: topic
title: uber/dig
category: architecture
tags:
  - go
  - dependency-injection
  - architecture
created: 2026-10-06
updated: 2026-10-06
timestamp: 2026-10-06
description: 解析 uber/dig 基于反射的依赖注入原理，类型匹配与 dig.As 机制，以及 TypeScript 与 Effect 的等价实现对照。
source_refs:
  - https://pkg.go.dev/go.uber.org/dig
  - https://effect.website/docs/requirements-management/services/
  - https://effect.website/docs/requirements-management/layers/
resource:
  - https://pkg.go.dev/go.uber.org/dig
  - https://effect.website/docs/requirements-management/services/
  - https://effect.website/docs/requirements-management/layers/
---

# uber/dig

uber/dig 是 Go 语言生态中一个基于运行时反射（Reflection）的依赖注入库。它的核心工作机制是：开发者向容器注册一系列普通构造函数，dig 通过反射读取这些构造函数的入参类型与返回值类型，并在调用方请求目标对象时，自动按类型拓扑关系将依赖解析并组装完成。

在本质上，dig 的整个自动解析与实例化流程，完全等价于开发者在程序入口处手写的以下三行装配代码：

```go
gormDB := db.NewGormDB()
repo := infra.NewTaskRepo(gormDB)
app := application.NewTaskApp(repo)
```

## new(T)：把类型当作值传递

在 Go 语言中，`new(T)` 是一个内建函数：它在内存中分配一个类型 `T` 的零值，并返回指向该零值的指针 `*T`。

当开发者书写 `new(domain.TaskRepository)` 时，由于 `domain.TaskRepository` 本身是一个接口类型，该调用返回的是一个「指向空接口的指针」。这个返回指针所持有的实际值没有任何业务作用，其存在的唯一目的，是**将 Go 语言中的静态「类型」当作普通「值」传递给函数参数**（这在 Go 语言尚未引入泛型机制的早期尤为必要）。

dig 内部正是通过以下反射调用取出接口 `I` 对应的反射类型对象：

```go
reflect.TypeOf(new(I)).Elem()
```

这种机制在语义上等同于 Java 语言中的 `Foo.class` 类字面量，或者 TypeScript / Effect 体系中用于标识依赖的 `Context.Service` 标签值：它们本质上都是在运行时承载类型身份的**类型令牌（Type Token）**。

## Provide 怎么按类型匹配

dig 容器的 `Provide` 方法在注册构造函数时并不会立即执行该函数，而是利用运行时反射读取该函数的完整签名，并在内部字典中按照精确的「类型」进行登记：
- **函数的参数类型**：标示该构造函数执行时需要消费哪些依赖类型；
- **函数的返回值类型**：标示该构造函数能够向容器提供哪些依赖类型。

```go
// 领域层：仅声明仓储抽象接口
type TaskRepository interface {
    GetByID(ctx context.Context, id int64) (*Task, error)
}

// 基础设施层：具体技术实现，返回具体结构体指针
func NewTaskRepo(db *gorm.DB) *taskRepoImpl { ... }

// 应用层：仅依赖抽象接口
func NewTaskApp(repo domain.TaskRepository) *TaskApp { ... }

// 组装根：注册到 dig 容器
c := dig.New()
c.Provide(db.NewGormDB)                                         // 提供 *gorm.DB
c.Provide(infra.NewTaskRepo, dig.As(new(domain.TaskRepository))) // 按接口类型登记
c.Provide(application.NewTaskApp)                               // 需要 domain.TaskRepository
```

当外部通过 `Invoke` 请求获取 `*TaskApp` 实例时，dig 会沿着类型依赖链递归反向追溯：
1. `NewTaskApp` 需要 `domain.TaskRepository` 类型；
2. 容器检索发现 `domain.TaskRepository` 由 `NewTaskRepo` 构造函数提供；
3. `NewTaskRepo` 需要 `*gorm.DB` 类型；
4. 容器检索发现 `*gorm.DB` 由 `NewGormDB` 构造函数提供；
5. 最终容器按照拓扑逆序依次调用各构造函数完成实例化，并将结果缓存在内部（dig 容器默认以单例形式缓存对象）。

### 核心解析逻辑伪代码

用 TypeScript 伪代码可以清晰刻画 dig 内部的核心解析机制：

```ts
type Type = unknown
type Constructor = (...args: unknown[]) => unknown

const providers = new Map<Type, Constructor>()
const cache = new Map<Type, unknown>()

function provide(ctor: Constructor, as: Type[] = []) {
  // 若未指定 as，则按返回值类型登记；若指定 as，则改为只按接口类型登记
  const keys = as.length > 0 ? as : returnTypesOf(ctor)
  for (const t of keys) {
    providers.set(t, ctor)
  }
}

function resolve(t: Type): unknown {
  if (cache.has(t)) return cache.get(t)
  const ctor = providers.get(t)
  if (!ctor) {
    // 容器未登记该类型，直至启动或调用期才抛出异常
    throw new Error(`missing type: ${String(t)}`)
  }
  const dependencies = paramTypesOf(ctor).map(resolve)
  const value = ctor(...dependencies)
  cache.set(t, value)
  return value
}
```

在类型匹配过程中，需注意两类典型边界情况：
- **类型冲突（Collision）**：dig 的匹配严格基于类型本身。若两个不同的构造函数返回了完全相同的类型，容器在注册或解析时会报告冲突；针对这种情况，需要使用 `dig.Name`（具名注入）或 `dig.Group`（值组切片）进行显式区分；
- **类型缺失（Missing Type）**：若某个构造函数所需的入参类型没有任何提供者注册，由于 Go 反射在静态编译期无法检查容器字典，该错误必须等到**应用启动执行容器装配时才会暴露报错**。

## dig.As：改为按接口登记

在 Go 语言中，`dig.As` 并不是语言层面的内置语法，而是 dig 提供的一个标准辅助函数，其返回值是一个 `ProvideOption` 配置项。

这种 API 设计遵循了 Go 社区通用的 **functional options 模式**：构造函数的最后一个参数接收可变参数列表 `opts ...Option`，每个 Option 是一个闭包函数，按需修改内部配置。在 TypeScript 中大致相当于支持传入选项对象：`provide(newTaskRepo, { as: [TaskRepositoryToken] })`。

### dig.As 是「改为」按接口登记，而非「同时」登记

理解 `dig.As` 的最关键事实在于：**它是将构造函数的产出「改为」按接口类型登记，并非「同时」登记两者**。

dig 官方文档对此有明确的原话说明：
> "values produced by constructors will be then available in the container as implementations of all of those interfaces, but not as the value itself."

| 注册方式 | 容器内部登记的类型键 | 当后续依赖索要 `domain.TaskRepository` 接口时 |
|---|---|---|
| `Provide(NewTaskRepo)` | `*taskRepoImpl` | **无法找到匹配项，启动时报 missing type**。dig 只按类型键做精确字典匹配，Go 接口属于隐式实现，dig 不会在运行时遍历并猜测「哪个结构体恰好实现了该接口」 |
| `Provide(NewTaskRepo, dig.As(new(domain.TaskRepository)))` | `domain.TaskRepository`（具体结构体指针类型不再保留登记） | **成功匹配**：dig 识别到该接口有提供者，调用 `NewTaskRepo` 并将其返回值作为接口实例注入下游 |

### 等价的手写包装函数写法

dig 官方文档进一步指出，使用 `dig.As` 在效果上完全等同于由开发者自己手写一个显式返回接口类型的包装构造函数：

```go
c.Provide(func(db *gorm.DB) domain.TaskRepository {
    return NewTaskRepo(db)
})
```

手写包装函数通过函数签名直接声明返回值为 `domain.TaskRepository`，dig 便能自然按该接口类型登记，无需借助 `dig.As` 辅助配置。

## 为什么 TS 做不到，Effect 怎么做

Go 语言在编译为可执行文件后，其二进制运行时中依然完整保留了函数的参数类型与返回值类型元数据，因此 dig 能够通过反射读出函数签名。

而在 **TypeScript 中，所有类型系统信息在编译为 JavaScript 后会被擦除（Type Erasure）**。在运行时，Node.js 或浏览器环境面对 `constructor(repo: TaskRepository)` 时，完全无法得知 `TaskRepository` 到底是什么类型。因此，TypeScript 生态要实现依赖注入只有两条路径：

1. **装饰器机制 + `reflect-metadata`**：指示 TypeScript 编译器在编译期将有限的类型信息写入元数据（如 Inversify、tsyringe、NestJS 等框架所采用的方案）；但即使如此，面对复杂泛型或抽象接口时，依然必须由开发者手动附加 `@inject(TOKEN)` 字符串或显式令牌进行标识；
2. **显式运行时令牌（Type Token）**：即 Effect 体系所采纳的函数式路线。Effect 中的 `Context.Service` 标签在运行时是一个真实存在的常量值对象，扮演着与 Go 中 `new(domain.TaskRepository)` 完全一致的类型令牌角色。在 Effect 用例中，`yield* TaskRepository` 即明确表示「我要获取该令牌绑定的具体实例」。一个程序所需要的全部依赖被完整捕获在类型签名 `Effect<Success, Error, Requirements>` 的第三个参数 `Requirements` 中，如果上层组装时遗漏了任何一个依赖，**在静态编译阶段就会直接报错**。

### uber/dig 与 Effect 机制对比

| 架构特性 | uber/dig (Go) | Effect (TypeScript) |
|---|---|---|
| **模块依赖注册** | 模块内部通过 `Provide` 注册一组构造函数 | 模块导出强类型的 `Layer`（通过 `Layer.mergeAll(...)` 组合） |
| **实现与接口绑定** | 使用 `dig.As(new(I))` 将实现转换为接口类型登记 | 使用 `Layer.effect(Tag, make)` 将具体实现绑定至 `Context.Service` 标签 |
| **模块间可见性控制** | 通过 Scope 作用域与 `Export` 控制跨模块实例可见性 | 模块对外入口严格仅导出代表 facade 的 Service 标签 |
| **依赖缺失报错时机** | **运行时（应用启动装配时报 missing type）** | **静态编译期（TypeScript 编译器直接报错阻断）** |

## 相关页面

- [[wiki/topics/architecture/dependency-injection|Dependency Injection]]：依赖注入的核心概念、实现方式与在应用组装根中的核心落地准则。
- [[wiki/syntheses/architecture/ddd-bounded-context-and-aggregate|限界上下文、聚合与仓储]]：系统解析限界上下文语义边界、聚合一致性边界、facade 暴露机制以及仓储解耦。
- [[wiki/syntheses/architecture/ddd-implementation-approaches|DDD 的实现方式与取舍]]：全面梳理 DDD 在工程落地中的四种做法、仓储一致性约定、前后端模型共用与 Effect 定位。

## Source Pointers

- uber-go/dig 官方文档: https://pkg.go.dev/go.uber.org/dig （涵盖 `As`、`Name`、`Group`、`Scope`、`Export`）
- Effect 官方文档（Context / Layer / 依赖注入）: https://effect.website/docs/requirements-management/services/ 与 https://effect.website/docs/requirements-management/layers/
