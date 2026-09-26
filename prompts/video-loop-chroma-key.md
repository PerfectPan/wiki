---
id: video-loop-chroma-key
title: 视频循环片 + 抠背景做动效
scene: 代码做不出的效果（玻璃折射、焦散、流体运动），需要一段能叠在 UI 上又不像视频的动效时
level: 可参考
tags:
  - design
  - video
  - image-generation
source: https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world
source_note: 原文 Technique 5 的第一个用法
notes:
  - 折射类效果要先把页面背景色渲进视频再抠背景，否则抠完就没有折射
  - 依赖外部视频模型与额度（原文用 fal.ai 一个 key 切模型）
added: 2026-09-22
---

````text
Can you replace the image on this page with a looping video clip that does something more interesting? Have the crystal splinter apart and slowly spin around. It should have awesome glassy effects that refract the page background and cast shadows and light around it.
To get convincing glass refraction effects, render the video of the glass over the page background colors first (so it bakes in the refraction effects), then remove the background with a video matting model.
Use this fal.ai API key: sk-a1b2c3d4…
Find appropriate recent models for video generation and background removal.
````
