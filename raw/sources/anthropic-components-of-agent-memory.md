---
title: Components of agent memory 阅读证据
description: Anthropic 关于记忆笔记、离线整理和 wiki 的实验记录与证据边界
created: 2026-11-08
updated: 2026-11-08
source_refs:
  - https://www.anthropic.com/research/components-of-agent-memory
---

# Components of agent memory 阅读证据

## 来源与范围

- 来源：[Anthropic · Components of agent memory](https://www.anthropic.com/research/components-of-agent-memory)
- 阅读日期：2026-11-08
- 资料版本：所提供的文章正文，包含图示文字与图注。未独立核查网页版本或发布日期。
- 本记录摘记实验设置与观察，不是全文翻译，也没有复现实验。

## 章节与证据

### Memory can be a prediction about what the future will need

CL-Bench 1.0 数据库任务中，每道题开启新会话，只有记忆目录跨会话保留。模型答题后得到正确答案，可以记录经验。文中 Opus 5 将假设检验成规则，较早模型可能只留下未经检验的猜测。图 3 报告 Opus 5 无状态平均奖励为 0.564，使用记忆为 0.828。这是该任务的平均奖励，不是通用准确率。

### Claude has learned to judge salience

图 4 比较 Sonnet 3.7 与 Fable 5 各一次游戏运行，观察点约为 10,000 步。前者保存 413 个文件、获得一枚徽章；后者保存 10 个文件、获得四枚徽章。后者更偏向保存策略、计划与规则，而不是每轮屏幕可见的状态。模型不同且各只有一次运行，不能据此认定减少文件数导致更好的成绩。

### Dreaming can correct memory

图 6 至图 8：Claude 将 Pokémon 中 PokéCenter 的方位记错，误以为已经穿过 Mt. Moon。离线整理对照会话记录发现错误并改写笔记，随后该运行抵达 Cerulean City；未修正笔记的运行反复返回旧路线。这是具体案例，不是所有记忆错误都能被自动修正的证明。

### Dreaming can build new memory representations

图 10 使用 Stainless 内部资料，约 350,000 个文件、420M token，评估集为 25 道问题。Opus 5 智能体经过 2 至 128 次会话构建和维护 wiki。仅 wiki 满足的评分标准比例从 13% 增至 48%，wiki 加搜索从 54% 增至 61%，仅搜索为 53%。wiki 加搜索每题节省约 20,000 token，但构建和维护 wiki 本身消耗计算资源。

图 11 的合并资料任务中，跨文档且需要判断或计算的项目，查阅 wiki 得分 87%，仅搜索为 73%。另一个 LAB 任务的大部分标准可从单份文档检索，wiki 没有明显增益。图 12 还展示 wiki 达到原始文档大小的 1.77 倍。

### Dreaming can promote notes up the memory hierarchy

图 13：每次会话预先加载的记忆必须精简。文章指出，注入会占用 token，错误可能进入每次会话，加载内容也不保证模型遵循。文中描述 Claude Code 自动记忆只加载 MEMORY.md 开头的 200 行或 25 KB，其余内容按需读取。

### Dreaming can focus memory on a specific goal

图 14 的合同任务中，多个智能体同时编辑共享条款表，概括遗漏与互相覆盖导致 57 条评分事实只保留 41 条，约 72%。改进指令后，每份合同由单个智能体负责独立页面并逐字引用条款，满足标准的比例达到 100%。任务指令、并发写入方式和摘录方式同时改变，无法单独归因于其中一个因素。

### Thinking backward, looking forward

结尾明确保留了维护时机、信息过时与计算成本等开放问题。对日志做搜索可以作为记忆基础，wiki 等表征需要持续维护以避免错误积累。

### Steering Claude to write memory

图 5 与相邻正文：要求“只记录失败”削弱了 Opus 5 和 Opus 4.7 从记忆获得的增益。文章认为，对这些模型不宜预先固定过于严格的记忆选择规则。该观察不表示所有模型、所有提示规则都会如此。
