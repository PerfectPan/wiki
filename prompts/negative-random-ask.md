---
id: negative-random-ask
title: 反例：要求「完全随机」
scene: 反例。以为让模型「完全随机」就能得到多样性时，先看这条实测结果
level: 偏薄
tags:
  - design
  - anti-pattern
source: https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world
source_note: 原文 Technique 1 的反例（同一条基线要求换着说法再来一次）
notes:
  - 结果和基线不同，但配色、结构、甚至同一个陶器隐喻都在重复
  - 模型没有真正随机的能力，随机性必须从模型外部带进来（见 seed-string）
added: 2026-09-22
---

Build me a landing page for my productivity app. Give me something totally unique. Make every design decision completely at random.
