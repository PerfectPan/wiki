---
title: 用 AI 做设计的几个技巧
description: 从方向探索、独立截图评审到图像视频素材与删减，整理六个可复用做法及使用限制
type: synthesis
category: design
created: 2026-09-28
updated: 2026-09-28
timestamp: 2026-09-28
tags:
  - design
  - prompt
  - image-generation
  - video
  - agent
source_refs:
  - raw/sources/2026-09-22-lenny-world-class-designer.md
  - https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world
resource:
  - raw/sources/2026-09-22-lenny-world-class-designer.md
  - https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world
---
# 用 AI 做设计的几个技巧

## 这页整理什么

根据《How to turn your AI into a world-class designer》已保存的公开部分，整理 Technique 1–6。核心流程是：先探索方向，由人筛选并表达偏好，再通过截图评审和有目的的修改逐步完善。

下面的做法来自作者示例，标为“整理建议”的部分是本页的使用判断。模型名称、演示题材和评分阈值不作为通用前提；文中的案例也不能证明这些方法对所有任务都有效。

## 1. 用额外输入探索不同方向

原文 Technique 1 让工具先生成随机字符串，再让模型从中寻找配色、字体和布局的灵感，最后不把字符串显示在页面上。可复用的点是：给方向探索增加一个不同的输入，而不只是重复要求“独特一点”。[提示词原文](../../../prompts/seed-string.md)

**整理建议：**把它用在早期探索，比较多个结果后再选方向。随机输入不保证审美质量，也不能据此断言模型无法随机采样。

## 2. 先选方向，再把偏好写成可执行要求

原文 Technique 2 分成三个步骤：先要一批简短方向；自己选几条，说清喜欢和不喜欢的具体部分；等方向明确后，再让模型整理成实现提示词。[多轮对话示例](../../../prompts/design-direction-hunt.md)

其中最值得保留的是人的选择过程。例如“喜欢控制面板的触感，但不要卡通化；用材质而不是灰色渐变”比只给一个风格名字更具体。像素风、城市模型等题材只是文章里的例子，不必各自保存为通用 prompt。

## 3. 让独立上下文看截图，并限制迭代次数

原文 Technique 3 把当前截图交给另一个评审上下文，不带实现代码、历史讨论和上一轮解释；要求它给出具体视觉问题。作者也建议提供参考图，并先运行一两轮，观察是否有改进。[提示词原文](../../../prompts/design-critic-subagent.md)

**整理建议：**使用当前可用且能评审图片的模型，先约定最多两轮，每轮优先处理最重要的问题，由人决定是否继续。原文 prompt 中固定的模型名和“达到 9/10 才结束”是案例设置；复用时应替换，不能把自评分数当作客观验收。参考图用于说明目标，不要求照抄。

## 4. 需要图像时，明确素材要解决什么问题

原文 Technique 4 尝试用生成图像改善只依赖色块、渐变和基础形状的页面，并在浏览器中检查实际效果。

**整理建议：**先说清需要的是产品场景、材质、插画还是其他视觉内容，再生成素材并放回页面检查。不要只要求“增加个性”，也不要为了使用图像而增加无用装饰。API 接入方式与具体提示词分开管理，不需要保存带 key 占位符的泛化指令。

## 5. 视频素材可以用于循环动效和状态衔接

原文 Technique 5 提供了两个不同的方法：

- **循环动效：**先生成带纯色背景的循环视频，再做 chroma key 或 video matting。玻璃折射示例先把页面背景色渲进画面，再移除背景，使合成时保留与背景有关的视觉效果。[提示词原文](../../../prompts/video-loop-chroma-key.md)
- **状态衔接：**生成首帧与下一状态之间的片段，再把上一段末帧作为下一段起点；滚动或手势控制播放进度。[提示词原文](../../../prompts/keyframe-transition-scrub.md)

**整理建议：**先验证短片段的首尾衔接、背景合成和滚动控制，再投入更多生成成本。这些素材表达预先生成的视觉变化，不会自动变成可交互的物理模拟；具体模型名称只是来源中的示例。

## 6. 最后明确删掉什么

原文 Technique 6 的改进包括移除无意义的发光和渐变、减少重复标签、删除多余容器，并在其 iOS 示例中采用更合适的原生控件。

可复用的做法是指出具体冗余，并说明删除后页面应该更清楚地传达什么；不必把“图片网格”或“Apple 风格”固定为所有设计的目标。

## 使用范围

这些方法解决的是方向探索与视觉修改，不能代替功能、可访问性、响应式和性能检查。先明确用户任务和设计约束，再选择适用的技巧。

素材在 Technique 7 标题处截断，本页不补写未取得的内容。保留的 prompt 是原文副本，实际使用时仍需调整任务条件；本页不宣称做过跨模型效果评测。

## 相关页面与来源

- [[Prompt]]
- [[wiki/syntheses/product/AI 辅助设计的质量边界|AI 辅助设计的质量边界]]
- [[wiki/topics/design/界面质感细节|界面质感细节]]
- [文章存档：Technique 1–6](../../../raw/sources/2026-09-22-lenny-world-class-designer.md)
- [How to turn your AI into a world-class designer](https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world)
