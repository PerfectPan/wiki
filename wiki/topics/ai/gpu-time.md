---
title: gpu-time
description: 浏览器本地运行的小型神经模型，把自然语言时间表达解析为日期、时间段与 RFC 5545 重复规则
type: topic
category: ai
created: 2026-09-28
updated: 2026-09-28
timestamp: 2026-09-28
tags:
  - nlp
  - neural-network
  - webgpu
  - browser
  - time-parsing
source_refs:
  - raw/sources/2026-09-28-gpu-time.md
  - https://gpu-time.arikko.dev/
  - https://github.com/arikchakma/gpu-time
resource:
  - raw/sources/2026-09-28-gpu-time.md
  - https://gpu-time.arikko.dev/
  - https://github.com/arikchakma/gpu-time
---

# gpu-time

## 摘要

gpu-time 是一个实验性的小型神经模型解析器，把英文（和西班牙文）的自然语言时间表达转成具体日期、时间段和 RFC 5545 重复规则。推理完全在浏览器本地完成（CPU 或 WebGPU），输入不发送到服务器。作者是 Arik Chakma，MIT 协议，npm 包名 `gpu-time`（v0.5.0）。适用场景是提醒输入框、日程表单和命令栏这类短文本；作者在 MODEL_CARD 里明确说不适合长文档抽取，也不适合日期错误有真实后果的场景（账单、合规、医疗）。

## 关键点

- **模型很小，任务很窄**：发布模型 38,745 参数（官网 "Inside the Model" 仍写 24,761，是早期 checkpoint 的旧文案，以 MODEL_CARD 为准）、两层双向 scan、hidden size 32。整个 npm 包 Brotli 压缩后 45,561 字节，作者给自己定的发布上限是 50,000 字节。
- **35 个语义角色 + CRF 解码**：模型给每个 token 预测一个角色（小时、星期、月份、数量、重复标记、filler 等，共 40 个 slot），一个 40×40 转移矩阵把它当 linear-chain CRF 训练，CPU 上对所有 backend 统一做 Viterbi 序列解码；另有独立的边界分数把一句话切成多个独立表达。
- **模型没有词表**：tokenizer 只给字符形状、长度、大小写、拼写 hash 这类特征，月份名单只存在于编译器里。模型靠拼写特征认识 "October"，上下文由 five-tap 卷积和双向 scan 提供。
- **caller context 不进模型**：时区、夏令时、参考日期、展开上限全部由推理之后的 TypeScript 处理；模型只输出 token 角色和边界，编译器把它们拼成 typed Schedule，日历解析器再算出具体时刻。
- **backend 按批大小分派**：`auto` 模式在批次达到 32 条输入或 512 tokens 时走 WebGPU，否则留在 CPU——小输入时设备 dispatch 和 readback 开销占主导。WebGPU 内核按块并行处理 scan 并携带精确块前缀，块边界不重置上下文；shader 在构建期把模型常量拼进去并直接内联进 JS bundle。
- **输出带解释性**：`occurrences`（ISO start/end）、`rrules`（RFC 5545）、`diagnostics`（拒绝原因）、`spans`（答案来自原文的字符偏移）。没有公开 AST 或 token 标签。未知时区直接拒绝调用，不静默回退。

## 训练与评测里值得借鉴的做法

来源仓库的训练管线（PyTorch）记录了几个小模型/窄任务工程的通用经验：

- **监督数据是生成的，不是爬的**。标签来自生成器自身的结构，从不在模型自己的输出上训练；真实语料靠 "harvest"——chrono-node 与自家 tagger 双教师一致才收，且每一行都要通过编译验证，错误标注进不了语料。
- **negative flip 的解法是 focal distillation**（Yan et al., CVPR 2021）。warm start 上微调新家族会破坏无关旧案例；`alpha=0` 只约束参考模型已答对的 token、其余放开，才能学到新家族，`alpha=1` 时模型完全学不动。checkpoint 平均作为替代方案被测量过，两个方向都更差。
- **token 训练与序列评测的差距用 sequence-level 损失弥补**（Edunov et al., NAACL 2018 的 k=2 情形）。只对解码错误的序列推高 gold path 分数；系数极其敏感，0.05 到 0.005 之间就是「多对 1 个 authored 案例、丢 5 个 chat 案例」和「少对 1 个、多赢 3 个」的取舍。
- **导出检查防家族回退**：导出时同轮构建候选与在产基线并逐个 gold 集合比较，池化提升不能掩盖单一家族回退。512 个 fixture 对 PyTorch logits、1,000 条序列对真实 WebGPU 验证量化推理 parity。
- **评测纪律**：结构 holdout 和未见句式家族分开（只 holdout 渲染字符串会泄漏短语家族）；评估 split 先于训练切出（修复过 13.9% 的验证/训练重叠）；种子波动约 1.85 个百分点，更小的单次差异当噪音。

## 已知边界

摘自 MODEL_CARD 的 Limitations（完整清单见来源）：

- "in N units" 表示经过时长时会被读成未来时间（"He ran a quarter mile in four minutes" 返回一个时间）。
- 1900–2059 的裸四位数字读作年份（`at 1930` 返回 1930 年），1900 以下的四位年份可能读成时钟。
- 以星期命名的人名会被读成星期；em dash 不支持；歧义数字日期跟随调用方 `dateOrder`（默认 MDY）。
- 模糊表达（ASAP、after work）按设计不给时钟值；只有英文和西班牙文，其他语言可能错得没有诊断。
- 真实用户措辞上的准确率未测量——评测集是生成的语料家族、公开语料 holdout 和作者手写/LLM 标注的金标准集，作者对此写得很坦白。

## 相关页面

- [[wiki/syntheses/ai/llm-101|大模型 101]]——对比参考：参数量光谱另一端（百亿级 LLM）的基本概念

## 来源指针

- [[raw/sources/2026-09-28-gpu-time|gpu-time 来源存档]]
- [gpu-time 官网](https://gpu-time.arikko.dev/)
- [arikchakma/gpu-time 仓库](https://github.com/arikchakma/gpu-time)
