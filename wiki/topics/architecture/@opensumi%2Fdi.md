---
title: @opensumi/di
type: topic
category: architecture
status: seed
created: 2026-04-12
updated: 2026-04-19
tags:
  - dependency-injection
  - ioc
  - typescript
source_refs:
  - raw/sources/@opensumi%2Fdi.md
---
# @opensumi/di

- 整个框架会严重依赖 reflect-metadata 这个基础库
- Injectable 只是一个调用 Reflect 注册类的 metadata 的元信息
- AutoWired 懒实例化，不用这个的话就是在构造器里用 @Inject() 去注册，这样在创建这个对象的时候会直接实例化
- 在你 import reflect-metadata 且使用 decorator 的时候 #TypeScript 会默认调用 Reflect.metadata 注册元信息，目的就是运行时注册类型信息：
	- ```ts
	  class Line {
	    private _start: Point;
	    private _end: Point;
	    @validate
	    @Reflect.metadata("design:type", Point)
	    set start(value: Point) {
	      this._start = value;
	    }
	    get start() {
	      return this._start;
	    }
	    @validate
	    @Reflect.metadata("design:type", Point)
	    set end(value: Point) {
	      this._end = value;
	    }
	    get end() {
	      return this._end;
	    }

	    @Reflect.metadata("design:paramtypes", [A, Number])
	    constructor(a: A, b: number) {

	    }
	  }
	  ```
	- ```js
	  import { Autowired, Injectable, Injector } from '@opensumi/di';
	  // import { C } from './C';

	  @Injectable()
	  class A {
	    // @Autowired()
	    // cInstance: C;
	    @Autowired('2')
	    c: number;

	    @Autowired('3')
	    d: number;

	    constructor() {
	      console.log('A create');
	    }
	  }

	  @Injectable()
	  class B {
	    aInstance: A

	    c = 1

	    constructor(aInstance: A, b: number) {
	      this.aInstance = aInstance;
	    }
	  }

	  const injector = new Injector([A, B, {
	    token: '2',
	    useValue: 1
	  }, {
	    token: '3',
	    useValue: 2
	  }]);
	  console.log('done');

	  console.log(injector.get(B));

	  export { B }

	  // tsc 后

	  "use strict";
	  var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
	      var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
	      if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
	      else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
	      return c > 3 && r && Object.defineProperty(target, key, r), r;
	  };
	  var __metadata = (this && this.__metadata) || function (k, v) {
	      if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
	  };
	  Object.defineProperty(exports, "__esModule", { value: true });
	  exports.B = void 0;
	  const di_1 = require("@opensumi/di");
	  // import { C } from './C';
	  let A = class A {
	      constructor() {
	          console.log('A create');
	      }
	  };
	  __decorate([
	      (0, di_1.Autowired)('2'),
	      __metadata("design:type", Number)
	  ], A.prototype, "c", void 0);
	  __decorate([
	      (0, di_1.Autowired)('3'),
	      __metadata("design:type", Number)
	  ], A.prototype, "d", void 0); // 是对原型链上的进行注入
	  A = __decorate([
	      (0, di_1.Injectable)(),
	      __metadata("design:paramtypes", [])
	  ], A);
	  let B = class B {
	      constructor(aInstance, b) {
	          this.c = 1;
	          this.aInstance = aInstance;
	      }
	  };
	  B = __decorate([
	      (0, di_1.Injectable)(),
	      __metadata("design:paramtypes", [A, Number])
	  ], B);
	  exports.B = B;
	  const injector = new di_1.Injector([A, B, {
	          token: '2',
	          useValue: 1
	      }, {
	          token: '3',
	          useValue: 2
	      }]);
	  console.log('done');
	  console.log(injector.get(B));

	  ```
- 然后我们需要初始化 Injector 这个容器类，后续也可以通过 addProvider 去动态注入要被容器管理的对象，可以直接是 value，也可以是 class，也可以是工厂函数，也可以是 alias 引用
- 然后也可以调用 overrideProviders 去覆盖已有的 provider
- 一开始 addProvider 加入 Provider 的时候并不会直接实例化，而是创建一个 creator 对象，这个对象会维护当前实例化的状态（用以检测循环依赖），如果对象是单例的话还会直接挂到 creator 对象上，最后会直接把 token 到 creator 的映射存到 creatorMap 上的，在后续真正实例化的时候会取出来
- 容器类支持嵌套子容器，支持按照 Domain 分组（Injectable 指明）
- 暴露了函数 `markInjectable`，包裹函数以注册 metadata，`setParameters` 注册这个函数的依赖，相当于不用装饰器这个语法糖了
- 然后还有维护一个 tag -> token -> token 的 map，通过 tag 去找到真正的 token，其实不是很懂这里的用处是什么
- 还支持面向切面编程（AOP）的装饰器，这个跟 DI 关系应该不是很大（？），就是类似函数的执行前，执行后，报错等时期的执行的函数，以后再研究
- TODO 输出 dependency graph
- TODO 为什么要再写一个 DI 框架？

## Source Pointers

- `raw/sources/@opensumi%2Fdi.md`
