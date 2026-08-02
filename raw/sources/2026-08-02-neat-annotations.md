# neat-annotations 调研快照（2026-08-02）

## 来源与快照

- 官网：<https://neat-annotations.syabro.com/>
- 仓库：<https://github.com/syabro/neat-annotations>
- 源码快照：`83199c8c`（2026-07-22，调研时 main HEAD）
- 对照：<https://roughnotation.com/>
- CSS `light-dark()`：<https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/light-dark>

## 仓库事实

- 创建于 2026-07-16；调研时 422 stars、11 forks、0 open issues。
- 主要贡献者 `syabro` 35 commits，另一贡献者 1 commit。
- MIT；没有 tag、release、package.json、npm package、CI 或自动化测试。
- 核心 `neat-annotations.css` 为 152 行、8537 bytes，gzip 约 1790 bytes。
- 官网推荐未固定 tag/commit 的 jsDelivr GitHub URL。

## 实现事实

- `.ann` 使用 `position: relative; display: inline-block; overflow: visible`。
- `::before` 用 data URI SVG mask 绘制 46×38 箭头。
- `::after` 用 `content: attr(data-note)` 绘制绝对定位标签。
- 八个方向 class 通过 physical top/right/bottom/left 定位。
- 颜色、mark、字体、间距、偏移、旋转、label 宽度通过 CSS variables 暴露。
- 支持无标签 highlight、`ann-no-mark`、嵌套标注和 rainbow animation。
- rainbow 遵守 `prefers-reduced-motion`；箭头对 forced-colors 有处理。
- 默认 mark 使用 `light-dark()`；宿主需要设置合适的 `color-scheme` 才能切换 dark 分支。

## 浏览器实测

- 在当前 Chromium 中，OKLCH、relative OKLCH、`light-dark()`、mask 和 `@property` 均被支持。
- 官网八方向、预设色、自定义色、嵌套标注、长标签与暗色主题工作正常。
- 标注为绝对定位，不进入文档流；官网通过大块留白和移动端横向滚动避免碰撞，这不是库自动提供的能力。

## 风险与限制

- 可能被祖先 `overflow: hidden/clip` 裁切，或覆盖相邻内容并越出 viewport。
- `inline-block` 改变文本断行和 line-height，不适合跨行长文本。
- generated content 不能承载唯一可访问语义；重要内容需真实 DOM / `aria-describedby`。
- physical direction 不自动适配 RTL 和 vertical writing mode。
- print 背景、分页和截图裁切需要单独验证。
- CDN 跟随默认分支且无 SRI，生产环境应 vendoring 或固定内容 hash。
- 现代颜色语法对旧 Safari、旧 WebView 和旧 Electron 需要兼容测试。
