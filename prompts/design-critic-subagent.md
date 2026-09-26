---
id: design-critic-subagent
title: 设计批评者子代理（critic loop）
scene: 模型自己评审自己的产出、越改越平庸时；需要外部审美判决和一个能收敛的停止条件
level: 推荐
tags:
  - design
  - agent
  - qa
source: https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world
source_note: 原文 Technique 3；作者用强模型当 critic，critic 只占不到 10% 输出 token
notes:
  - critic 的判据要客观：「5 张图排序」比「判断好不好看」稳定得多
  - 先只跑 1–2 轮看是否收敛，再加轮次，否则 critic 会让 agent 空烧 token
  - 9/10 的完成阈值留在实现者侧，不要写进 critic 的 prompt，否则打分不再独立
  - 参考图只当 baseline / moodboard，不要让它照抄
added: 2026-09-22
---

````text
I want you to improve this design. To figure out what to focus on, use a Fable 5 subagent as a design critic.
Follow this procedure at each iteration:
- Capture a screenshot of the current design
- Invoke the critic in a fresh context, with just the screenshot, not the code, implementation details, or earlier iterations/critiques
- Ask it to evaluate the aesthetic that the design is going for, imagine how a top design studio would execute this aesthetic, then outline the biggest gaps
- Lastly, it should provide a score out of 10 indicating how close the current design is to that studio-level quality bar
Provide this guidance to the critic in its prompt:
- It should think high-level about the overall structure and composition as well as look at the fine details
- It should watch out for patterns that feel overdone, excessive, or otherwise obviously AI-generated, and penalize them
- It should provide tight, specific feedback, not vague prose
- It should be bold and opinionated, not rely on what’s safe or easy
Your work is only complete when the critic independently deems it 9/10 or higher. Do not put that criterion in the critic prompt; keep it objective in its scoring. Use the same critic prompt each time.
````
