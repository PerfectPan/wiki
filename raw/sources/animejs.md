# Anime.js 源码核查记录

- 来源：https://animejs.com/；https://github.com/juliangarnier/anime
- 访问日期：2026-10-07
- clone 的源码提交：`01b81be1df6843ccfe0a71c0699a746bf740dd77`
- `package.json` 版本：`4.5.0`；记录的是该提交，不据此推断每个安装包版本。
- 范围：普通动画的 API、时间推进、Timeline、Scope、WAAPI 与属性适配器；布局模块只核对公开入口及调用顺序。

## 证据对照表

| 结论 | 固定版本位置 | 观察事实与限制 |
| --- | --- | --- |
| 统一播放控制 | [timer.js](https://github.com/juliangarnier/anime/blob/01b81be1df6843ccfe0a71c0699a746bf740dd77/src/timer/timer.js#L108-L198) | Timer extends Clock；JSAnimation 和 Timeline 继承 Timer |
| Engine 只推进运行中的根实例 | [engine.js](https://github.com/juliangarnier/anime/blob/01b81be1df6843ccfe0a71c0699a746bf740dd77/src/engine/engine.js#L60-L101) | 遍历活动链表并调用 tick，移除暂停实例；浏览器与 Node 使用不同调度入口 |
| 短参数归一化成 tween | [animation.js](https://github.com/juliangarnier/anime/blob/01b81be1df6843ccfe0a71c0699a746bf740dd77/src/animation/animation.js#L246-L369) | 目标注册、默认值、标量/数组/属性对象转关键帧片段 |
| 属性名与配置共用空间 | [helpers.js](https://github.com/juliangarnier/anime/blob/01b81be1df6843ccfe0a71c0699a746bf740dd77/src/core/helpers.js#L64-L66) | isKey 按 globals.defaults 排除保留参数名 |
| 插值和目标写入分工 | [render.js](https://github.com/juliangarnier/anime/blob/01b81be1df6843ccfe0a71c0699a746bf740dd77/src/core/render.js#L209-L284) | 缓动后插值，优先 setter，否则按对象/attribute/CSS/transform 写入 |
| 时间线位置语法 | [position.js](https://github.com/juliangarnier/anime/blob/01b81be1df6843ccfe0a71c0699a746bf740dd77/src/timeline/position.js#L35-L73) | 解析绝对时间、标签、相对偏移；< 为前一实例末尾，<< 为起点 |
| Scope 追踪实例 | [scope.js](https://github.com/juliangarnier/anime/blob/01b81be1df6843ccfe0a71c0699a746bf740dd77/src/scope/scope.js#L96-L143) | 在 execute 中临时设置 current/root/defaults，register 记录实例 |
| Scope 统一恢复 | [scope.js](https://github.com/juliangarnier/anime/blob/01b81be1df6843ccfe0a71c0699a746bf740dd77/src/scope/scope.js#L226-L249) | revert 实例、清理回调和 media query 监听 |
| WAAPI 为独立执行路径 | [composition.js](https://github.com/juliangarnier/anime/blob/01b81be1df6843ccfe0a71c0699a746bf740dd77/src/waapi/composition.js#L58-L84) | 调用元素原生 animate 方法；不由 JSAnimation 直接执行 |
| Timeline 可同步外部动画 | [timeline.js](https://github.com/juliangarnier/anime/blob/01b81be1df6843ccfe0a71c0699a746bf740dd77/src/timeline/timeline.js#L268-L285) | 暂停 synced 对象，把 currentTime 从 0 动画到 duration |
| 自定义属性读写 | [registry.js](https://github.com/juliangarnier/anime/blob/01b81be1df6843ccfe0a71c0699a746bf740dd77/src/adapters/registry.js#L1-L16) | registerAdapter 注册 getter / setter 并复用动画流程 |
| 已有布局动画 API | [layout.js](https://github.com/juliangarnier/anime/blob/01b81be1df6843ccfe0a71c0699a746bf740dd77/src/layout/layout.js#L1590-L1612) | update 顺序调用 record、用户回调、animate |
| 上游测试入口 | [parameters.test.js](https://github.com/juliangarnier/anime/blob/01b81be1df6843ccfe0a71c0699a746bf740dd77/tests/suites/parameters.test.js#L173-L220) | 包含单个属性参数测试，已读未运行 |
| 上游时间线测试 | [timelines.test.js](https://github.com/juliangarnier/anime/blob/01b81be1df6843ccfe0a71c0699a746bf740dd77/tests/suites/timelines.test.js#L231-L253) | 测试标签位置，已读未运行 |

## 已运行的接口验证

在 Node.js 中直接导入该快照的 `src/index.js` 与 `src/adapters/index.js`，使用内置 assert 核对六组行为。未安装依赖，验证脚本和 clone 均位于临时目录，不提交上游代码。

| 验证 | 实际结果 |
| --- | --- |
| 公共 duration 500、value 属性 duration 1000，linear 动画 seek 到 250 | value 为 25，opacity 为 0.5；业务对象的 duration 属性保持原值 7 |
| 对上述动画调用 cancel，再调用 revert | cancel 后 value 保持 25；revert 后 value 与 opacity 回到 0 |
| 两个对象分别到 10 和 20、第二个 delay 为 50、时长 100，在 100 时读取 | 第一个为 10，第二个为 10 |
| 两个 400 毫秒动画通过标签相隔 200 毫秒开始 | 总长 600；seek 到 400 得到 100/100，再退到 100 得到 25/0 |
| Scope 内创建动画，推进后调用 scope.revert | 属性回到初始值 |
| 自定义 Gauge 的 value 注册 getter / setter | 插值到 50% 时 setter 写入 50 |

六组全部通过。临时测试只覆盖普通对象和手动 seek 的语义，不能据此宣称 rAF、DOM、原生 WAAPI 或 React 集成已验证。

## 未测试项

未运行上游完整测试套件，未做包体、帧率或与 Motion 的性能对比。已读布局动画入口但未验证其浏览器行为；未验证所有参数组合、颜色/复杂字符串插值、动画冲突与第三方适配器。
