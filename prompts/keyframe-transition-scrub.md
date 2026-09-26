---
id: keyframe-transition-scrub
title: 关键帧插值做滚动转场
scene: 想让页面转场跟着滚动或手势逐帧 scrub，而不是硬切或淡入淡出时
level: 可参考
tags:
  - design
  - video
  - interaction
source: https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world
source_note: 原文 Technique 5 的第二个用法
notes:
  - 用上一段的末帧当下一段的起始帧，接缝才连续
  - 需要物理和一致性强的视频模型（原文点名 Seedance 2.5）
added: 2026-09-22
---

````text
Build a demo page for a suitcase that uses a video model to create interactive transitions between a couple of screens. Each screen should show the suitcase in a different state, with vertical motion that feels appropriate for scrolling:
- Initially, have the suitcase floating high up in the air
- Then have it land on the floor and pop open
- Finally, have its contents neatly land into it from the top
Generate the initial frame using your image generation skill. Then, generate a video clip that starts from that frame and animates to the next state. Use the final frame of that video to seed the next transition so that it continues seamlessly. Scrub through the transitions one by one as the user scrolls.
Use this fal.ai API key: sk-a1b2c3d4…
Use a video model with strong physics and consistency, like Seedance 2.5.
````
