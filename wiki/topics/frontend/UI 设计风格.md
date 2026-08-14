---
title: UI 设计风格
description: 从第一性原理理解 UI 风格：界面必须回答的四个基本问题、驱动风格变迁的三种外力、区分风格的坐标系；Name That Vibe 等图鉴是模型的实例。
type: topic
category: frontend
created: 2026-08-14
updated: 2026-08-14
timestamp: 2026-08-14
tags:
  - ui
  - design-styles
  - design-systems
  - visual-language
  - glossary
source_refs:
  - raw/sources/2026-08-14-name-that-vibe.md
  - https://namethatui.com/styles
  - https://namethatui.com/styles/glassmorphism
resource:
  - raw/sources/2026-08-14-name-that-vibe.md
  - https://namethatui.com/styles
  - https://namethatui.com/styles/glassmorphism
---

# UI 设计风格

## 摘要

UI 设计风格不是审美偏好，而是界面在四个基本问题上的一揽子可识别答案：**怎么让人知道什么能点、什么在什么之上、这个表面是什么做的、这个产品是谁**。风格的变迁由三种外力驱动——渲染技术、用户素养、文化周期；所谓"风格"就是在这些约束下收敛出的一组连贯信号。Name That Vibe 这类图鉴是模型的实例化，不是模型本身。

## 第一性问题：任何界面都必须回答的四件事

1. **Affordance（可供性）**：用户怎么知道什么可交互？——拟物用物理隐喻（凸起的按钮看起来能按），扁平用习得惯例（色块 + 位置）。
2. **层次（Hierarchy）**：什么在什么之上、什么最重要？——靠深度、对比、留白回答。
3. **材质（Material）**：这个表面是什么做的？——材质暗示行为预期：玻璃可穿透、纸张可堆叠、金属可按压。
4. **身份（Identity）**：这个产品/平台是谁？——风格是差异化和平台识别的载体（Aqua 之于 Apple、Material 之于 Google）。

一个"风格"就是对这四个问题的成体系、可被文化识别的回答。说不出这四个答案的"风格"只是装饰。

## 风格为什么会变：三种外力

- **技术约束**决定什么可行。GPU 合成和 `backdrop-filter` 让玻璃拟态可行；高 DPI 让 1px 细线和大面积扁平可行；CSS 标准化让"裸 HTML"成为可复现的美学（Web Brutalism）。
- **用户素养**决定 affordance 能多抽象。触屏初期需要拟物教用户（iOS 6 的书架、木纹）；全民熟练后扁平才成立（iOS 7）。**用户越熟练，风格可以越抽象**。
- **文化周期**决定什么"过时"和什么"复兴"。风格被广泛采用后变得无聊 → 反动（Brutalism 是对模板化 SaaS 美学的反动）；老风格过了"丑"的阶段进入怀旧期 → 被追认（Y2K、Frutiger Aero 都是事后命名）。

## 区分风格的坐标系

- 材质隐喻：写实材质 ↔ 抽象数字表面
- 深度：平面 2D ↔ 模拟 3D
- 装饰：极简 ↔ 极繁
- 可供性策略：物理隐喻 ↔ 习得惯例
- 密度：留白 ↔ 塞满

两个风格"像"，本质是坐标系上的邻近点。例：Glassmorphism 与 Liquid Glass 都用玻璃材质，但前者把玻璃当**任意表面的装饰皮肤**，后者把玻璃保留给**浮动控制层**——材质的用法不同，不是材质本身不同。

## 风格谱系：14 种已命名风格

按坐标系上的位置归三簇（据 [Name That Vibe](https://namethatui.com/styles) 的收录，括号内为术语地位）：

**材质模拟系** —— 用渲染回答"这是什么做的"，占坐标系的高深度/高装饰端：

- Skeuomorphism —— 真实材质、物理光照、实物隐喻（基础词，拟物的源头）
- Aqua —— 糖果凝胶控件、细条纹、口香糖窗口按钮（vendor，Apple 2000s）
- Windows Aero —— 透明模糊窗框、镜面高光扫过、发光热区（vendor，Vista 起）
- Neumorphism —— 单一连续表面 + 双向软阴影 + 内凹按压态（industry-coined，2020）
- Glassmorphism —— 磨砂半透明面板、鲜艳背景透出、细亮边（industry-coined，2020）
- Liquid Glass —— 玻璃作为控制层、透镜折射、自适应自着色（vendor，Apple 2025）
- Claymorphism —— 内外阴影 + 超大圆角 + 漂浮膨松物体（industry-coined）
- Y2K Digital Aesthetic —— 液态金属、凝胶/塑料、虹彩蓝银（retrospective，千禧年前后）
- Frutiger Aero —— 自然与科技融合、水感光泽表面、天蓝草绿（retrospective，2004–2013）

**扁平与极简系** —— 放弃材质模拟，靠习得惯例回答 affordance，占低深度/低装饰端：

- Flat Design —— 纯色 2D 填充、无模拟深度、简单字形图标
- Minimalism —— 留白即材质、元素数受限、克制色板

**反体系与民间系** —— 对前两簇主导地位的反动或怀旧：

- Web Brutalism —— 浏览器默认材质、暴露文档结构、零装饰（contested label）
- Neobrutalism —— 粗黑描边、硬偏移阴影、高饱和平涂色块（industry-coined）
- Vernacular Web —— 平铺背景、GIF 动图装饰、徽章与计数器（retrospective，90s–00s 民间网页）

在研未收：Swiss Style、Bauhaus、Art Deco、Art Nouveau、Memphis、Vaporwave、Internet Ugly。

## 从模型推出的判断

- **没有最好的风格，只有对约束的适配**：B2B 工具重密度和惯例，消费品重身份和新奇；选错坐标系的位置比"做得不精致"更致命。
- **风格会回归，但回归的是信号不是复刻**：Y2K 复兴是用现代渲染做液态金属质感，不是真的做 Windows XP。
- **可访问性风险内生于信号**：半透明 ↔ 对比度不稳，拟物装饰 ↔ 认知负荷，动效 ↔ 前庭障碍。风格 brief 必须带 fallback（如玻璃拟态配 contrast scrim、`prefers-reduced-transparency` 降级），否则就是在拿风格换可访问性。
- **风格名的权威性分层**：vendor design language（Aqua、Liquid Glass）> 标准/框架术语 > 行业造词（Glassmorphism 这类 -morphism）> 事后追认（Y2K）> 争议标签（Web Brutalism）。写文档和 prompt 时越靠前越硬，营销词不当规范用。

## 实践含义

- 给 agent 下风格类指令时，写**信号**不写风格名："`backdrop-filter: blur(16px)` + 半透明白 12% + 1px 亮边"比"做成玻璃拟态"可执行、可验收。
- 评审时先定位坐标系（它在材质/深度/装饰轴上的哪里），再谈好不好看。
- 参考图鉴：[Name That Vibe](https://namethatui.com/styles)（14 种风格的 signals、style DNA、agent brief）是目前最系统的实例库；元素层面的命名见 [[UI 元素命名]]。

## 相关页面

- [[UI 元素命名]] —— 元素层面的"叫什么"，与本页的"是什么风"互为表里
- [[wiki/topics/frontend/Transitions.dev|Transitions.dev]] —— 动效参考，风格的时序维度

## 来源指针

- `raw/sources/2026-08-14-name-that-vibe.md`（Name That Vibe 站点事实与词条解剖）
- https://namethatui.com/styles
- https://namethatui.com/styles/glassmorphism
