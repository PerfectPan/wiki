# Voila 扩展拆解实录（一手，全部由我在浏览器里直接读扩展源码得到）

来源：Chrome 扩展 ID `jpomhonnigcdannbfdjjnaaglldbdgjb`，
商店页 <https://chromewebstore.google.com/detail/voila/jpomhonnigcdannbfdjjnaaglldbdgjb>，
官网 <https://www.withvoila.app/>。
读取方式：在 `chrome-extension://<id>/` 下 fetch `manifest.json` / `freeze.js` / `content.js` 原文。

## 0. 商店页事实

- 版本 3.329.0，更新于 2026-07-16，体积 **428 KiB**
- **92 用户**，4 个评分，分类「开发者工具」
- 开发者：LA COMPAGNIE DES INTERNETS BORDELAISE（法国波尔多）
- 声明处理的数据：身份验证信息、网站内容
- 开发者原文（重要）：**"Your edits and settings are stored locally in your browser. The only network request is to the Claude API to generate responses. No tracking. No analytics."**
  → 推论：**没有自有后端**，全部逻辑在这 428KB 里；配合「身份验证信息」，基本可确定是 BYOK（用户自带 Claude API key），这也解释了它为什么按 credits 计费而非订阅。
- 商店描述提到能导出 **reusable skills**（官网首页未提）。
- 商店描述明确写有 GUI 面板：「Select any element on a page and open an **editable panel for its styles**, including color, spacing, typography, border radius, layout」
  → **修正**：此前文档里若写 Voila「只有自然语言输入」是错的，它是 GUI 面板 + 对话都有。

## 1. manifest（MV3）

```json
"content_scripts": [
  { "js": ["content.js"], "matches": ["<all_urls>"], "run_at": "document_idle" },
  { "js": ["freeze.js"],  "matches": ["<all_urls>"], "run_at": "document_start", "world": "MAIN" }
],
"host_permissions": ["<all_urls>"],
"permissions": ["storage", "activeTab", "declarativeNetRequest"],
"background": { "service_worker": "background.js" }
```

文件体积：`freeze.js` 889 B，`content.js` 879,910 B，`background.js` 697,496 B。

要点：
- **双层注入**：`content.js` 走隔离世界管 UI；`freeze.js` 走 **MAIN world + document_start**，是唯一能进入页面自身 JS 世界的通道。
- **权限极克制**：只有 `storage` / `activeTab` / `declarativeNetRequest`。**没有 `scripting`、没有 `tabs`、没有 `webRequest`**。`declarativeNetRequest` 是声明式改请求、不读请求内容，比 `webRequest` 隐私友好。权限声明与「无追踪无分析」的说法自洽。

## 2. freeze.js —— 时间冻结器（全文 889 字节，逻辑完整可读）

在 MAIN world、document_start 劫持 `requestAnimationFrame` / `setTimeout` / `setInterval`，维护速度因子 `e`（默认 1）：

- `e === 0` → **冻结**：rAF 回调压入队列 `u` 不执行；setTimeout 改为每 100ms 自旋重试；setInterval 跳过
- `0 < e < 1` → **慢放**：setTimeout 延时除以 e（拉长）；rAF 每 `max(1, round(1/e))` 帧才放行一次
- 解冻时把队列 `u` 里积压的回调一次性 flush
- 与隔离世界的通信：监听自定义事件 `cc-mf-sync`，读 `document.documentElement.dataset.ccMf`
- 幂等守卫：`window.__ccMF`

**用途判断**：解决「要改的东西在动」——下拉菜单一失焦就收、轮播在轮、hover 态一移开就没、动画中途的样式抓不住。
这也解释了为什么必须 document_start + MAIN：要赶在页面脚本拿到原始 rAF 引用之前替换，且必须在页面自己的 JS 世界里。

## 3. selector 生成（函数 `Ln`，反混淆）

```js
function Ln(e) {
  if (e.id) return `#${CSS.escape(e.id)}`;               // 自己有 id → 直接返回
  let t = [], n = e;
  for (; n && n.nodeType === 1 && t.length < 5; ) {       // 最多上溯 5 层
    let o = n;
    if (o.id) { t.unshift(`#${CSS.escape(o.id)}`); break; }  // 祖先有 id → 封顶
    let r = o.nodeName.toLowerCase();
    let i = Array.from(o.classList)
      .find(s => !s.startsWith("cc-") && /^[a-zA-Z_-]/.test(s));  // 第一个「干净」class
    i && (r += `.${CSS.escape(i)}`);
    let a = o.parentElement;
    if (a) {
      let s = Array.from(a.children).filter(l => l.nodeName === o.nodeName);
      s.length > 1 && (r += `:nth-of-type(${s.indexOf(o) + 1})`);  // 仅同名兄弟>1 才加
    }
    t.unshift(r), n = a;
  }
  return t.join(" > ");
}
```

配套 `jn(e)` 生成人读描述：标签名 + 第一个干净 class + 前 24 字符 textContent。

过滤 `cc-` 前缀 = 避免把自己注入的类名写进 selector；`/^[a-zA-Z_-]/` = 排掉哈希类名（CSS Modules / 原子类）。

**关键**：运行时它并不靠 selector 找元素——有元素对象缓存
```js
Xm = new Map();
function Qm(e){ let t = Xm.get(e); return t && t.isConnected ? t : null }
```
selector 只是**交接物**（写进导出 CSS、Linear 任务、喂给 Claude）。所以它可以拿「可能不唯一」换「短且可读」。

## 4. 样式怎么落地 —— 一个 `<style>` 全量重写

```js
function Z1(){ he.css = Ft.map(e => e.css).join("\n") }   // 编辑片段列表 Ft → 拼成整段 CSS

function jr(){                                             // 落地
  if (!V1) { SM().textContent = ""; let r = $M(); r && (r.textContent = ""); return }
  let e = Object.entries(he.tokens).map(([k,v]) => ` ${k}: ${v} !important;`).join("\n");
  let n = (e ? `:root { ${e} }\n` : "") + he.css;
  SM().textContent = n;                                    // 写主文档的 <style>
  let o = $M(); o && (o.textContent = n);                  // 同一份写进响应式预览 iframe
}
async function Yi(){ await tM(U1, { ...he, segs: Ft, undo: Object.fromEntries(xr) }) }  // 持久化
```

- **不碰元素本身**：不改 inline style、不改 class。所有修改汇总成一段 CSS 文本，写进自己的 `<style>` 的 textContent，每次**全量重写**而非增量 insertRule。
- **撤销免费**：`V1` 开关关掉 → textContent 置空 → 页面瞬间还原，**不需要记录任何原值**。
- **token 单独成层**：不混在规则里，统一输出 `:root { --accent: #xxx !important; ... }`。改一个 token 全站跟随。
- **双写**：主文档 + 响应式预览 iframe（390×844 那类画框）同步。
- `!important` 在 content.js 中出现 118 次。
- **文本修改走另一条路**：`IM()` 遍历 `he.texts` 的 `{selector, text}`，`querySelectorAll` 后直接改 `textContent`，不经过 CSS。

## 5. 支持的样式 —— 硬编码白名单，116 个属性

不是「任意 CSS」，是固定清单，按类：

- 布局定位：display, position, top/right/bottom/left, inset, float, clear, z-index, box-sizing, visibility, overflow(-x/-y)
- 尺寸：width, height, min/max-width, min/max-height, aspect-ratio, opacity
- 盒模型：margin(四向), padding(四向)
- Flex：flex, flex-direction/wrap/grow/shrink/basis, justify-content, align-items/content/self, justify-items/self, order, gap, row-gap, column-gap
- Grid：grid-template-columns/rows, grid-column/row/area, grid-auto-flow, place-items, place-content
- 边框描边：border(+width/style/color/radius/四向), outline(+color/width/style/offset)
- 背景：background(+color/image/size/position/repeat/clip)
- 文字：color, font-family/size/weight/style, line-height, letter-spacing, word-spacing, text-align/transform/decoration(+color)/indent/overflow, white-space, word-break, overflow-wrap, vertical-align
- 视觉效果：box-shadow, text-shadow, filter, backdrop-filter, mix-blend-mode, transform, transform-origin, clip-path
- 动效：transition(+property/duration/timing-function), animation
- 交互杂项：cursor, pointer-events, user-select, list-style(+type), object-fit/position, will-change

**比常见可视化编辑器 setter 宽的部分**：Grid 全家、clip-path、backdrop-filter、mix-blend-mode、aspect-ratio —— 一般 setter 里都没有。

## 6. 两个官网没写的能力

**（a）动效关键帧编辑**
```js
cg = ["translate","scale","rotate","opacity","width","height",
      "border-radius","background-color","color","border-color","filter"]
zL = { translate:"0px 0px", scale:"1", rotate:"0deg", filter:"blur(0px)" }   // 默认值
```
规则 key 形如 `motion-kf-${sel}`。→ 能给元素编排关键帧动画。
**这解释了 freeze.js 的存在**：能停住/慢放时间，才能逐帧调动画。两者是一套组合拳，不是两个独立功能。

**（b）低保真线框模式**（`voila-wap`）
向预览 iframe 注入：
```css
* { font-family: "Courier New", ui-monospace, monospace !important; text-shadow: none !important; }
html { background: #9aad86 !important; }
img, video, canvas, svg { image-rendering: pixelated !important; }
```
一键把真实页面降级成「纸原型」，用于讨论布局而不被视觉细节干扰。

## 7. UI 自身

- `attachShadow` × 1 → 面板 UI 装在 **Shadow DOM** 里，与宿主页面隔离
- 面板用 **React 18.3.1** 写（react-dom 完整打进 bundle）+ Tailwind 原子类
- 常量：`IN = "chrome-chat-host"`，主题色 `EN = "#0062ff"`

## 8. 一个必须写明的排查结论（避免误判）

content.js 中 `__reactFiber$` / `__reactInternalMemoized...` / `__REACT_DEVTOOLS_GLOBAL_HOOK__` 共 20+ 处命中，
**但这些全部出自打包进来的 react-dom 18.3.1 自身源码**（旁边就是 `reconcilerVersion: "18.3.1-next-..."`）。

反向验证：探测「读取宿主页面框架实例」的典型写法
`Object.keys(el).find(k => k.startsWith('__react'))` / `startsWith("__vue")` 等，命中数均为 **0**。

→ **Voila 不读宿主页面的框架内部，框架无关成立**。它进入 MAIN world 仅用于时间控制（freeze.js），不做框架内省。
（我第一次看 grep 计数时误判成「它读宿主 React」，看上下文后已推翻。文档里不要写错。）
