# near-membrane：源码阅读与归档调查记录

- 访问日期：2026-10-20 至 2026-10-21；社区和同类项目核查日期 2026-10-21。
- 仓库：<https://github.com/salesforce/near-membrane>（MIT，已归档，只读）。
- 固定提交：`19685c36d267071cc70c2876925f8a020361fe3d`（2026-09-18 17:59 北京时间，「This repo is ARCHIVED」），即仓库最后一个提交。
- 范围：读 `README.md`、`DESIGN_DOCUMENT.md`、`packages/near-membrane-base/src/membrane.ts`（4711 行）、`connector.ts`、`environment.ts`、`intrinsics.ts`、`packages/near-membrane-dom/src/browser-realm.ts`、`packages/near-membrane-node/src/node-realm.ts`，以及 2026 年 #481–#493 的 PR 和提交说明。没有运行测试，没有复现逃逸。

## 核查位置

- `membrane.ts`：`createMembraneMarshall`（同一份源码在 blue、red 两侧各求值一次，靠 `IS_IN_SHADOW_REALM` 分支）、指针协议、`BoundaryProxyHandler`、shadow target、`makeProxyStatic` / `makeProxyLive`、`Symbol.for('@@lockerNearMembraneUndefinedValue')`、`Symbol.for('@@lockerLiveValue')`。
- 约第 3738–3745 行：`callableConstruct` 接收侧 `args[i] = selectedTarget`。
- 约第 4197–4202 行：冻结对象返回 `IsFrozen & IsSealed & IsNotExtensible`。
- `test/cross-sandbox/`：34 个文件（#493 新增）。
- 上面两处只描述代码字面，没有写测试验证实际影响；topic 页已标为「没有验证影响」。

## 归档调查

- 归档提交 `19685c3` 只把 README 换成归档说明。3 秒前，同一账号用同样的标题和文件归档了 salesforce/LAVIS。
- 2026 年用同一模板归档的 salesforce 仓库有 30 多个，06-26 一次约 27 个由 OSPO 机器人账号完成（按 GitHub 上各仓库归档提交的作者和时间统计，可能有遗漏）。
- 仓库、issue、Salesforce 博客都没有写归档原因，也没有指向替代项目。npm 上 `@locker/near-membrane-*` 没有被标记为 deprecated，最后版本 0.19.1（npm 发布 2026-09-15 22:22 北京时间）。
- `@locker/sandbox` 0.29.3（npm 发布 2026-10-15）依赖 `@locker/near-membrane-dom` 0.19.1；解包看过，包含 #487、#489 的修复，不包含被回滚的 #488。
- Aikido 通告 <https://intel.aikido.dev/cve/AIKIDO-2026-167438>：`@locker/near-membrane-base` 0.7.0–0.18.0 高危沙箱逃逸，0.19.0 修复。
- 归档时仍开着的 #476 附一个内部工单链接，标题「Vulnerability in public near-membrane Salesforce github repo」；工单内容无法访问。
- 归档时有 7 个 issue 和 PR 未处理。
- PRB-0031933、W-23623814 等编号来自公开 PR 和提交说明，对应的内部工单无法访问。

## X 上的检索

- 维护者 @jimjag、@rwaldron、@caridy：没有找到与归档或这些修复相关的帖子。
- 找到的相关帖子：
  - @aikidointel 2026-09-01 05:09（北京时间）播报上述 Aikido 通告。
  - @DCF_io 2026-07-30 提到一个叫 SandDriller 的工具发现了沙箱逃逸，这个说法没有核实，topic 页没有采用。
  - @ivelivanov 2026-08-26、@handsontable 2026-09-22 的帖子和 @stomita 2024 年的帖子只是提到或讨论 near-membrane / Locker，与归档原因无关。

## 验证限制

- 「为什么归档」一节的推断（OSPO 例行清理、开发转到内部、不想公开披露逃逸细节）没有直接证据，topic 页已与事实分开写。
- 同类方案对比页里各项目的最新状态是 2026-10-21 按 GitHub 和 npm 查的；标了「待确认」和「常识背景」的项没有逐项核实。
- 没有使用任何幻灯片内容或渲染图。

## 2026 年的修复记录（从 wiki 页移出）

2026-10-22 起 `wiki/topics/frontend/near-membrane.md` 不再展开这些修复，原文保留在这里，供「为什么归档」一节引用。

时间均为北京时间。

| 时间 | 变更 | 内容 |
| --- | --- | --- |
| 02-25 | #481 | 加入 `DESIGN_DOCUMENT.md` |
| 04-09 | #483 | 不再 link `eval` |
| 04-27 | #485 | `protectDistortions` |
| 07-31 | #487（W-23623814） | live 目标的 setPrototypeOf 和 `__proto__` 只作用于 shadow target。攻击方式是把宿主的原型（例如宿主全局对象）拼到 live 目标上，再通过继承读到宿主全局；随后发布 v0.17.0 / v0.18.0 |
| 08-07 | #488（W-23552746） | live 目标上的 accessor defineProperty 只写到 shadow target |
| 08-14 23:00 | #489（W-23789302） | 修复变参 trap 的沙箱逃逸，23:09 发布 v0.19.0 |
| 09-09 | #491（W-24091454） | 回滚 #488 |
| 09-10 03:44 | #492 | v0.19.1（npm 发布 09-15 22:22） |
| 09-18 00:07 | #493（W-24137734） | 补上兄弟沙箱之间两次穿越的测试 |
| 09-18 17:59 | `19685c3` | 归档 |

- **#489 的逃逸**：6 个及以上参数的跨界调用，用 `arr[i] = x`（`[[Set]]`）把「对方目标指针 + 参数」填进一个继承 `Array.prototype` 的普通数组。沙箱先在 `Array.prototype` 上装一个数字下标的 setter，填参数时就会触发，借机改掉下标 0 的目标指针，把这次调用重定向到另一个宿主函数。commit 原文称之为「a confirmed sandbox escape」。修复是发送端和接收端都改用 `ReflectDefineProperty`，它不查原型链。
- **#488 → #491**：#488 想阻止沙箱把自己写的 getter 种到宿主共享的 live 对象上（宿主之后以原对象为 receiver 读这个属性时会执行沙箱代码）。#491 回滚的理由有两条：它没修到原工单（那是经 `ImageData.data` 的 setPrototypeOf 逃逸，已由 #487 修好）；live 读取解析的是原对象，accessor 只写在 shadow 上会读回 `undefined`，弄坏了 ISV 组件和客户组件之间合法的 getter 共享。回滚后，#488 描述的那种形态在最终版本里仍然存在。
- **#493 与 P1 事故**：PRB-0031933（P1）记录 0.19.0 打进 Locker 0.29.9 后弄坏了 Omniscripts 和 FlexCards，CRST、自动化和手工测试都没发现。原因是整个 karma 测试只覆盖一次 blue↔red 穿越，而 #488 弄坏的是兄弟沙箱之间的第二跳。#493 新增 `test/cross-sandbox/`，34 个 spec。npm 上公开的 `@locker/sandbox` 最高只到 0.29.3，所以 0.29.9 应是内部版本。

最终代码 = v0.19.1 + #493 的测试：包含 #487、#489 的修复，不包含 #488。不要使用 0.19.0。

**读代码时注意到、没有验证影响的两处**（只描述代码字面）：

1. `callableConstruct` 的接收侧仍用 `args[i] = selectedTarget`（`[[Set]]`）回填参数（`membrane.ts` 约第 3742 行），而 `callableApply` 的接收侧已在 #489 改成 `ReflectDefineProperty`。#489 的说明只提到 apply 的接收侧。construct 是否有同类风险，需要实际测试。
2. `callableGetTargetIntegrityTraits` 对冻结对象返回 `IsFrozen & IsSealed & IsNotExtensible`（约第 4199–4201 行），三个不同的位做按位与，字面结果是 0；`makeProxyStatic` 靠这个值决定是否冻结 shadow target。有没有别的路径兜底，没有跑测试确认。

## 2026-10-22 改写记录

- wiki 页新增「从零理解：它到底防什么」：过膜时机、身份映射、双向包装、隔离范围、同线程同堆的后果、有无沙箱的对比例子、能防和不能防。例子里的 `createVirtualEnvironment`、`distortionCallback`、`env.evaluate` 和其他选项名对照 `packages/near-membrane-dom/src/types.ts`、`browser-realm.ts`；改 `Array.prototype`、`JSON` 留在 red 依据 `intrinsics.ts` 的 `getESGlobalKeys` 和反射型内置对象表；`window.fetch = …` 只写 red 全局依据 `membrane.ts` 懒投影 accessor 的 setter（先激活，再对 red 全局 `ReflectSet`）；cookie 的 distortion 照 `examples/getter-distortion/` 的写法换 `Document.prototype.cookie` 的 getter / setter。例子没有在浏览器里实际运行。
- 新增 ShadowRealm 小节，依据提案 README（Stage 2.7、champions 含 @caridy、@rwaldron、2024-12 Stage 3 请求）、[explainer](https://github.com/tc39/proposal-shadowrealm/blob/main/explainer.md)（Motivations、Non-goals、How does a ShadowRealm operate、Security、Use Cases 各节）、[whatwg/html#9893](https://github.com/whatwg/html/pull/9893)（`[Exposed=*]`，未合并）、[nodejs/node#65650](https://github.com/nodejs/node/pull/65650)（创建于 2026-08-29T20:57Z，即北京时间 2026-08-30 04:57；核对时仍 open；正文引用 WPT 删除测试的 [wpt#59794](https://github.com/web-platform-tests/wpt/pull/59794)）。ShadowRealm 停滞与 near-membrane 归档的关联只是推测。
- 删去「2026 年的修复与事故」一节（内容移到上面），压缩实现细节、去掉重复句子。原页「读代码时注意到、没有验证影响的两处」见本文件「核查位置」。
- `javascript-sandbox-approaches.md` 的配图和表格按「隔离了什么」改为三档：A 同线程同堆、B 独立的堆、C 独立线程或进程。原图「越往下隔得越彻底」的单一排序和「兼容性最好」的说法没有依据，已删。各项「同步调用 / 按防恶意代码设计」标签依据本次核对的 README 和文档；workerd 能否同步调用、Web Worker 是否算防恶意设计没法确认，留空。
