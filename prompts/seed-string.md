---
id: seed-string
title: Seed string（随机种子）
scene: 让模型做设计、命名、排版这类有「标准答案倾向」的创作，而它每次都交出同一套保守默认时
level: 推荐
tags:
  - design
  - exploration
source: https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world
source_note: 原文 Technique 1；方法出自 Sakana AI 的 String Seed of Thought（https://pub.sakana.ai/ssot/）
notes:
  - 正文里的「不要让随机串出现在设计里」是这条提示词的硬约束，删掉就退化成装饰
  - 只说「给我完全随机」没用，模型会把随机演成另一种默认
added: 2026-09-22
---

I want you to build me a landing page for my productivity app.
Follow this procedure:
1. Generate a long, random alphanumeric string using a shell script.
2. Define the creative direction (color scheme, layout, typography, etc.) based on the string. Look beyond the surface for subpatterns, special numbers, anything that inspires you.
3. Use your judgment to bring this direction to life and make it look great.
Don’t reveal the string in the design. It’s only for your inspiration.
