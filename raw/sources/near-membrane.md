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
