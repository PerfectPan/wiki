# Name That Vibe

- 网站：https://namethatui.com/styles （NameThatUI 的姊妹站，同一作者 Jane Appleseed）
- 记录时间：2026-08-14

## 来源事实

- 定位是 UI 设计风格的图鉴（"Name that vibe"）：识别一个 look、学到它的正式名字和 defining signals、和相似风格区分开、复制一段 agent 可执行的 style brief。自称 "governed atlas, not a style dump" —— 每个风格必须有可信来源、可辩护的 signals、可识别的 specimen 才收录。
- 已收录 14 个风格：Skeuomorphism、Neumorphism、Glassmorphism、Liquid Glass、Web Brutalism、Neobrutalism、Y2K Digital Aesthetic、Frutiger Aero、Flat Design、Minimalism、Claymorphism、Vernacular Web、Aqua、Windows Aero。
- 每个风格带**术语状态标签**，区分四类：vendor design language（Aqua、Liquid Glass、Windows Aero）、industry-coined trend（Neumorphism、Glassmorphism、Neobrutalism、Claymorphism）、retrospective label（Y2K、Frutiger Aero、Vernacular Web）、contested label（Web Brutalism）。
- 词条 anatomy（以 /styles/glassmorphism 为例）：
  - 定义 + 范围说明（与 Liquid Glass、macOS vibrancy 划清界限）；"If you called it…" 口语映射。
  - "What makes it this — the defining signals"：3-5 条 signal，每条带分类标签（Surface & material / Color & contrast / Geometry & borders / Depth & light 等）。
  - "Style brief — paste into your agent"：现成 agent prompt，含具体 CSS 抓手（`backdrop-filter: blur(16px)` + `background: rgba(255,255,255,0.12)`）、警告不要漂向 Liquid Glass、要求 contrast scrim 和 reduced-motion / reduced-transparency fallback。
  - 易混风格并排 demo（Glassmorphism vs Liquid Glass：前者是任意表面的装饰皮肤，后者把玻璃留给浮动控制层）。
  - "Full style DNA"：属性表，每档标 defining / avoid / supporting / variable（如 typography 是 supporting："Light ink on glass"；背景类型是 variable）。
  - "In code"：核心 CSS 配方 + `@supports` 降级到近不透明 + SwiftUI `.ultraThinMaterial`。
  - "Accessibility & misuse"：玻璃上文字对比度不稳、遵守 `prefers-reduced-transparency`、`backdrop-filter` 性能成本。
  - "Origin"：历史锚点（Windows Vista Aero 2006、iOS 7 blur、macOS vibrancy）+ 外部参考（NN/g、Apple HIG）。
- In research（coming soon）：Swiss Style、Bauhaus、Art Deco、Art Nouveau、Memphis、Vaporwave、Internet Ugly。
- 站点共用 ⌘K 搜索、RSS、sponsor 位。

## 本库判断（2026-08-14）

- 与元素词典（NameThatUI 主站）是两个用途：主站解决"这个控件叫什么"，Vibe 解决"这个界面是什么风、怎么让 agent 做出这个风"。
- 价值在两点：一是术语状态标签（避免把营销词当规范术语）；二是 style brief 把抽象风格落成具体 CSS 抓手和 fallback 要求，可直接喂给 agent。
- 适合做 UI 方向选型时的"风格词典"，不适合当设计规范——风格是趋势描述，不是团队约定。
