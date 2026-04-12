---
title: Front End
type: topic
category: tooling
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - front
  - end
source_refs:
  - raw/sources/Front End.md
---
# Front End

- [[Front End Framework]]
- [[CSS]]
- [[JavaScript]]
- [[EcmaScript]]
- [[TypeScript]]
- [[Component Library]]
- [[SVG]]
- [[State Management]]
- [[Font]]
- [[Bundle]]
- [[JavaScript Runtime]]
- [[富文本编辑器]]
- [[Cross Platform]]
- 打包工具：
	- [[Webpack]]
	- [ncc](https://www.npmjs.com/package/@vercel/ncc)：专门用来打包 node.js 文件
- 截图库：
	- https://zumerlab.github.io/snapdom/
- 目录最佳实践？
	- types 存放前端定义的实体类型，看起来这个分离会比较好
	- features 业务组件
	- components 纯 UI 组件
	- hooks
	- service 逻辑层
- Performance Optimization：
	- https://marvinh.dev/blog/speeding-up-javascript-ecosystem/
- https://modern-web.dev/guides/
- Node Server Framework：
	- https://www.farrowjs.com/
- Package Manager：
	- https://medium.com/@sdboyer/so-you-want-to-write-a-package-manager-4ae9c17d9527
	- https://docs.vlt.sh/cli/configuring
- Formatter：
	- https://biomejs.dev/
- [[Linter]]：
	- https://biomejs.dev/
- Editor：
	- https://novel.sh/docs/introduction
	- https://www.blocknotejs.org/ - prosemirror based
- 响应式：
	- https://github.com/nx-js/observer-util
- Plugin System：
	- https://www.framer.com/developers/plugins/introduction
		- iframe 隔离
		- react 方式开发
		- 本地 localhost 连接线上，跟 aily GUI 开发类似
		- 调用 API 应该就是封装一个 bridge 可以 invoke 宿主环境的 API
		- 使用了这个 [[Vite]] 插件，有点看不懂 https://github.com/liuweiGL/vite-plugin-mkcert/tree/main
- Schema Validation
	- https://valibot.dev/
	- https://zod.dev/
	- https://github.com/jquense/yup
	- 统一的标准： https://standardschema.dev/
		- 一些库框架可以使用 standard schema 作为输入，这样 schema lib 无关了，比如 trpc
			- https://github.com/trpc/trpc/pull/6079
		- ```ts
		  // copy & paste
		  import type {StandardSchemaV1} from '@standard-schema/spec';

		  export async function standardValidate<T extends StandardSchemaV1>(
		    schema: T,
		    input: StandardSchemaV1.InferInput<T>
		  ): Promise<StandardSchemaV1.InferOutput<T>> {
		    let result = schema['~standard'].validate(input);
		    if (result instanceof Promise) result = await result;

		    // if the `issues` field exists, the validation failed
		    if (result.issues) {
		      throw new Error(JSON.stringify(result.issues, null, 2));
		    }

		    return result.value;
		  }

		  // 引入
		  import * as z from 'zod';
		  import * as v from 'valibot';
		  import {type} from 'arktype';

		  // 统一的方式消费，一些库框架可以使用 standard schema 作为输入，这样 lib 无关了
		  const zodResult = await standardValidate(z.string(), 'hello');
		  const valibotResult = await standardValidate(v.string(), 'hello');
		  const arktypeResult = await standardValidate(type('string'), 'hello');
		  ```
	- https://arktype.io/
- 自建 DSL：
	- https://discord.com/developers/docs/interactions/message-components#responding-to-a-component-interaction
	- https://learn.microsoft.com/en-us/adaptive-cards/authoring-cards/universal-action-model
- 动画库：
	- https://www.framer.com/motion/
	- https://gsap.com/
	- https://www.easing.dev/
- Syntax：
	- https://shiki.style/
	- https://react-syntax-highlighter.github.io/react-syntax-highlighter/demo/
		- https://github.com/react-syntax-highlighter
	- https://github.com/rexxars/react-lowlight/tree/main
- 在线编码：
	- https://livecodes.io/docs/overview/
		- SDK 封装的代码可以看一下，目前感觉跟 CUI SDK 是差不多的，不过他是只有 iframe 模式看起来
			- 配置的编码化可以看看，还有对各个语言框架的简单封装，会使用的更简单一些
- Benchmark:
	- https://github.com/google/tachometer
- Network：
	- https://swr.vercel.app/zh-CN
	- https://tanstack.com/query/latest/docs/framework/react/overview
	- https://blog.skk.moe/post/why-you-should-not-fetch-data-directly-in-use-effect/#Chu-Li-Race-Condition #[[Design Pattern]]
		- 为什么你不应该在 React 中直接使用 useEffect 从 API 获取数据
		- race condition
		- 缓存请求
		- 缓存刷新
		- 请求合并去重
		- error retry
		- preload
		- 分页
		- middleware
- 协同编辑
	- https://liveblocks.io/
		- 一套完善的基建，还有基于基建做的解决方案（评论 / 反馈 / 白板）
		- 不过感觉这类还是会很难开发，本身背后依靠的服务还是 live blocks 提供的，没有提供 self host 的解决方案
		- API 的设计是可以参考一下的，感觉下了不少功夫
- LowCode / NoCode
	- https://www.framer.com/
- WebAuth
	- https://webauthn.io/
- [[Secure ECMAScript]] 相关：
	- https://guybedford.com/secure-modular-runtimes
- 社区生态相关：
	- https://e18e.dev/
		- https://github.com/fuzzyma/e18e-tools
- JavaScript Engine:
	- https://github.com/boa-dev/boa
	- https://github.com/servo/servo
-

## Source Pointers

- `raw/sources/Front End.md`

