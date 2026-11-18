---
title: 模型使用与常见问题
description: 记录模型使用中的具体问题、处理技巧和适用范围，区分外部经验与自行验证的结果。
type: topic
category: ai
created: 2026-09-15
updated: 2026-11-18
timestamp: 2026-11-18
tags:
  - llm
  - agent
  - gemini
  - claude-code
  - cache
  - performance
source_refs:
  - https://github.com/promptfoo/promptfoo
  - https://www.promptfoo.dev/docs/providers/custom-script/
  - raw/sources/2026-09-15-googlecloudtech-gemini-flash.md
  - https://x.com/GoogleCloudTech/article/2099507349828350285
  - https://code.claude.com/docs/en/hooks
  - raw/sources/claude-code-multi-agent-token-audit.md
  - https://code.claude.com/docs/en/prompt-caching
  - https://developers.openai.com/api/docs/guides/latest-model
---

# 模型使用与常见问题

按模型或工具记录实际使用中的问题、可尝试的处理办法和适用范围。外部经验注明来源，亲自验证后再补充结果。

## Gemini

### 用 Read Hook 减少零碎读取和越界重试

**适用范围：这项技巧默认只对 Gemini 启用，其他模型直接跳过。状态：外部经验整理，来源信息已省略，尚未自行复现。**

当 Gemini 连续读取很短的代码片段，或请求超过文件末尾的行号时，可以通过 Read Hook 调整读取行为。先按模型名称判断是否启用，再介入文件读取工具；其他模型是否需要这项调整，应单独验证。

处理分为两步：

- **读取后给提示**：单次读取过短、需要更多上下文时，提示模型扩大范围，或读取较短文件的全文；已经明确目标行时，仍按需读取。提示不强制修改读取范围。
- **读取前处理越界**：起始行超出文件总行数时，把请求调整为文件尾部的一段。这个处理改变了请求位置；采用时应同时告知模型原请求越界、实际返回的行范围，避免误认内容。

扩大读取范围可能减少工具调用，也可能引入无关内容，不宜给所有模型统一套用。具体读取长度按文件和任务选择；尝试时固定其他配置，用相同任务比较耗时和完成质量。

#### 最小实现（Claude Code command hook）

下面是独立整理的 Python 3 示例，不是原始脚本。保存为项目内的 `.claude/hooks/gemini_read.py`。示例只处理 `Read`，仅检查不超过 1 MiB 的普通文本文件；未知模型、异常输入、空文件和读取失败均保持工具原有行为。

`READ_HOOK_MODEL` 是这个示例自定义的环境变量，由启动方填入实际模型名。未设置或不是 Gemini 时不生效；只用于固定 Gemini 的会话，切换模型要同步更新并重启。混合模型子任务需要由宿主逐次传入真实模型，不能共享一个固定值。

```python
import json
import os
import sys
from pathlib import Path


def positive_int(value):
    return type(value) is int and value > 0


def handle(event):
    model = os.environ.get("READ_HOOK_MODEL", "").lower()
    if "gemini" not in model or event.get("tool_name") != "Read":
        return
    args = event.get("tool_input")
    if not isinstance(args, dict):
        return
    phase = event.get("hook_event_name")
    limit = args.get("limit")
    output = {"hookEventName": phase}
    if phase == "PostToolUse" and positive_int(limit) and limit < 200:
        output["additionalContext"] = (
            "需要整体上下文时，建议一次读取 300～500 行或短文件全文；"
            "已明确目标行时继续局部读取。"
        )
    elif phase == "PreToolUse":
        offset = args.get("offset")
        name = args.get("file_path")
        if not positive_int(offset) or not isinstance(name, str) or not name:
            return
        path = Path(name)
        if not path.is_absolute():
            path = Path(event.get("cwd") or os.getcwd()) / path
        if not path.is_file() or path.stat().st_size > 1024 * 1024:
            return
        with path.open("rb") as file:
            content = file.read(1024 * 1024 + 1)
        if len(content) > 1024 * 1024 or b"\x00" in content:
            return
        content.decode("utf-8")
        lines = content.count(b"\n") + int(bool(content) and not content.endswith(b"\n"))
        if lines == 0 or offset <= lines:
            return
        size = limit if positive_int(limit) else 100
        start = max(1, lines - size + 1)
        output["updatedInput"] = {**args, "offset": start, "limit": lines - start + 1}
        output["additionalContext"] = (
            f"原请求起始行 {offset} 超过文件末尾；已调整为第 {start}～{lines} 行。"
            "这是尾部切片，不代表已找到原目标。"
        )
    else:
        return
    return {"hookSpecificOutput": output}


try:
    event = json.load(sys.stdin)
    result = handle(event) if isinstance(event, dict) else None
    if result:
        print(json.dumps(result, ensure_ascii=False))
except (OSError, ValueError, TypeError):
    pass
```

将以下配置合并到 `.claude/settings.local.json` 的现有 `hooks` 中，保留已有条目。启动这个固定 Gemini 会话前，在同一终端设置 `READ_HOOK_MODEL` 为实际模型名；这只控制 Hook 的启用，不会替你配置模型路由。

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "^Read$",
      "hooks": [{
        "type": "command",
        "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/gemini_read.py\"",
        "timeout": 5
      }]
    }],
    "PostToolUse": [{
      "matcher": "^Read$",
      "hooks": [{
        "type": "command",
        "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/gemini_read.py\"",
        "timeout": 5
      }]
    }]
  }
}
```

输入输出字段依据 [Claude Code Hooks 文档](https://code.claude.com/docs/en/hooks)：修改参数时保留完整输入，额外说明通过 `additionalContext` 交给模型。示例不自动批准工具调用。已用模拟事件验证脚本分支，尚未在真实模型会话中验证效果。

### Flash 负责日常执行，复杂问题及时求助

**适用范围：Google Cloud Tech 以 Gemini Flash 与 Claude 配合为例的使用建议，尚未自行复现。**

让 Gemini Flash 承担查询、检查、按既定方案执行等明确任务；需要复杂规划或风险分析时，再交给擅长深度推理的模型。重点是把 Gemini 的任务、工具和求助方式配清楚。

- **工具保持聚焦**：只提供任务需要的工具，例如读文件、写文件、运行测试，并用明确的 JSON Schema 定义参数。原文举了 3～5 个工具的例子，应理解为减少无关工具，不是固定数量限制。
- **明确怎么求助**：提供类似 `ask_for_help(reason, failed_attempts, context)` 的入口。遇到歧义、不可逆操作或连续失败时，带上原因、已做的尝试和必要上下文交给深度推理模型。涉及不可逆操作时，应在执行前判断是否升级。
- **复杂任务先规划再执行**：让 Claude 分析问题并制定方案，Gemini 按任务执行、汇报结果，再由 Claude 检查是否完成。规划角色按职责提供文档和约束，不必同时授予直接写文件的权限。
- **用实际任务决定分工**：比较完整任务的正确率、耗时和总成本，把重试与模型交接算进去。优先按清楚的任务边界分工，避免只凭第一次输入就自动猜测该用哪个模型。

原文的成本倍数、请求处理比例和“失败两次就升级”都是案例或示例配置，不作为通用保证；实际模型组合和升级条件要用自己的任务验证。

#### 用 Promptfoo 对比 Gemini 与 Claude 的完整任务表现

谷歌文章使用 [Promptfoo](https://github.com/promptfoo/promptfoo) 组织测试，通过 `exec:` 调用 OpenCode，让 Gemini 和 Claude 分别执行相同任务。评测链路是：

```text
Promptfoo（组织用例、收集结果）
  → OpenCode（运行 Agent、调用工具）
    → Gemini / Claude（完成任务）
```

文章选择了“用一句话总结 Git 分支状态”和“设计数据库零停机迁移方案”两个任务。比较的是模型在 OpenCode 中完成任务的表现，结果也受工具、提示和运行环境影响，不是脱离 Agent 的模型能力排名。

Promptfoo 的 [自定义脚本接口](https://www.promptfoo.dev/docs/providers/custom-script/) 可以接入外部命令。文章给出的配置没有质量断言，因此只是建立了对照运行的入口，不能据此认为完成质量已自动验证。复用这个方法时，还要补上：

- **一致的任务环境**：使用相同代码版本、输入与权限；会写文件的任务使用独立工作副本，避免前一次运行影响后一次。
- **任务完成标准**：分支检查应与实际 Git 状态一致；迁移方案应检查兼容、回滚等必要条件，不能只判断是否生成了回答。
- **完整的计量**：确认外部命令如何回传耗时、用量与成本，不假定 `exec:` 会自动获得底层模型的全部指标。

先用少量真实任务找出 Gemini 适合承担的工作，再扩大用例集。文中的两个示例不足以证明所有任务都适合相同分工。

## Claude Code

### 叫回闲置的 subagent 会整段重写缓存

**适用范围：Claude Code 用 subagent 分多轮完成任务（实现、复审、修改、rebase）。状态：自行统计一次约一天的多 agent 开发任务的 transcript 验证。**

协调者让写代码的 subagent 交付后等 review，再用 SendMessage 叫回它修问题或 rebase。subagent 的缓存只保留 5 分钟（主会话在订阅额度内是 1 小时），等 review 往往超过 5 分钟，被叫回后的第一次请求要按写入价把整个上下文重写一遍，之后每次请求还要重读这份已经很大的上下文。1M 上下文的模型接近 1M 才自动压缩，subagent 的上下文常涨到 700k～900k，这个问题更明显。

这次任务里，被叫回的后续轮次输入侧花费 $298，比各自第一轮的 $203 还多；缓存过期后的整段重写约占总额 20%。计价方式和统计方法见 [[token-usage-and-billing]]。

处理办法：

- **叫回前先看成本**：从 transcript 取它最后一次请求的上下文大小和时间，判断缓存是否已过期，再比较两种做法。续用约等于剩余请求数 × 当前上下文，缓存已过期时再加一次整段重写；新开约等于剩余请求数 × 新上下文（简报、交接说明、要重读的文件），再加重新熟悉代码的请求。上下文大、缓存已过期、下一步又是一整轮工作时，新开通常便宜几倍；缓存还热的几次请求以内的追问，续用更划算。
- **派发时要交接说明**：预计有后续轮次的任务，要求交付里附上改动、决定和遗留问题，新开的 agent 从这份说明和 diff 接手。
- **控制复审轮次**：只在阻止合入的问题修复后复审，复审只核对这些修复，每轮新开 reviewer。这次任务里有个 reviewer 被同一会话叫回 7 轮，写缓存占它输入花费的一半以上。
- **不急着把 TTL 改成 1 小时**：社区实测把所有 subagent 改成 1 小时后总花费上升 8.6%。按这次的数据估算，全部改成 1 小时净省约 7%，只改 reviewer 约 2%，都不如改用法；确实需要隔一段时间再叫回的 agent，可在它的定义里单独设置 `experimental.cacheTtl`。

## GPT‑6.2 与 Codex

### 提示词写清交付范围

OpenAI 将 Astra 用于要求最高的任务，将 Sol 用于对成本更敏感的复杂任务。指南记录了 Astra 默认写作较简洁、意图不清时可能给出计划后停下来等确认的行为。长任务要写清可验证的交付物、哪些可逆决定允许模型自行处理，以及何时需要用户确认。写作时给出受众和必要背景，让最终回复可独立阅读。编码时说明要保留的调用行为与仓库约定。前端有视觉要求时提供字体、图片风格或设计参考，再核对渲染结果。[GPT‑6.2 提示词指南](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices)

### 采样温度按模型和接口判断

`temperature` 改变下一个 token 的采样概率。较低的值能降低输出波动，较高的值可用于发散候选。全局采样设置也可能改变中间推理路径。Google 明确指出 Gemini 3 将温度调低于默认值可能引发重复或推理质量下降。OpenAI 的 GPT‑6.2 指南要求省略温度字段，但未说明具体移除原因。调整推理投入时使用 `reasoning.effort`，需要多种候选时在提示中说明所需差异。[Gemini 3 默认温度](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/start/get-started-with-gemini-3?hl=en) · [GPT‑6.2 迁移清单](https://developers.openai.com/api/docs/guides/latest-model#migration-quickstart)

跨厂商的调用方要区分三种情况。GPT‑6.2 要求省略。Anthropic 的 `2026-10-21` API 版本对携带此字段的请求返回 400。Gemini 4 / 3.6+ 忽略自定义值并返回弃用提示。DeepSeek 在思考模式下忽略它，关闭思考时仍可调。自托管推理框架 vLLM 仍提供温度控制。不能仅凭 SDK 类型判断某个模型是否支持该字段。[Claude API 迁移](https://platform.claude.com/docs/en/api/migration-2026-10-21) · [Gemini API](https://ai.google.dev/gemini-api/docs/troubleshooting) · [DeepSeek 思考模式](https://api-docs.deepseek.com/guides/thinking_mode/) · [vLLM 采样参数](https://docs.vllm.ai/en/latest/api/vllm/sampling_params/)

迁移到 Astra 或 Sol 时，需要工具调用的应用使用 [[responses-api]]。新接入的推理强度可从 `medium` 起步，旧请求用 `none` 或 `minimal` 时迁到 `low`。按迁移清单移除所用端点不支持的其它采样和概率参数。缓存配置、命中与推理记录的排查见 [[kv-cache-vs-request-cache#GPT‑6.2：指令位置、缓存断点与推理记录]]。[GPT‑6.2 迁移清单](https://developers.openai.com/api/docs/guides/latest-model#migration-quickstart)

### Codex 生图入口与 API 模型选择

OpenAI 的 Images 2.6 公告将 Codex 列为可用入口。同一时期的 Codex 生图使用指南仍标注 `gpt-image-2`，所以产品上线公告与具体会话里工具实际调用的型号需要分别核对。要指定高细节、精细编辑的 Sunburst，可以通过 Image API 显式选择 `gpt-image-2.6-sunburst`，按 API 用量计费。[Images 2.6 发布公告](https://openai.com/index/introducing-images-2-6/) · [Codex 生图指南](https://learn.chatgpt.com/docs/image-generation) · [Sunburst 模型文档](https://developers.openai.com/api/docs/models/gpt-image-2.6-sunburst)

## 相关页面

- [[agent-harness]]
- [[code-agent]]
- [[token-usage-and-billing]]
- [[responses-api]]

## 来源指针

- [Google Cloud Tech：Gemini Flash 与 Claude 协作](https://x.com/GoogleCloudTech/article/2099507349828350285)；[阅读摘要](../../../raw/sources/2026-09-15-googlecloudtech-gemini-flash.md)
- `raw/sources/claude-code-multi-agent-token-audit.md`（多 agent 任务的账单拆分）；[How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching)
