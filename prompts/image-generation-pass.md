---
id: image-generation-pass
title: 用图像生成补质感（而不是渐变和形状）
scene: 界面一眼看出是 AI 生成时——只有渐变、色块和基础形状，缺材质与光影
level: 可参考
tags:
  - design
  - image-generation
  - agent
source: https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world
source_note: 原文 Technique 4
notes:
  - 正文里的 sk- 开头字符串是原文的占位符，不要把真实 key 写进仓库
  - 原文给了三条接入路径：用 agent 自带图像工具、让 Codex CLI 走 ChatGPT 订阅、或给一个带消费上限的 API key
  - key 建议放 gitignored 文件并在 AGENTS.md / CLAUDE.md 里写明「仅供开发、不得随产品发布」
added: 2026-09-22
---

The design is pretty plain. Add more personality using image generation. Consider shaders or 3D effects in combination with images to create more interesting visuals.
For image generation, use this OpenAI API key (only use it locally, do not store it in the code or product): sk-a1b2c3d4…
Verify that your work looks right frame-by-frame in the browser.
