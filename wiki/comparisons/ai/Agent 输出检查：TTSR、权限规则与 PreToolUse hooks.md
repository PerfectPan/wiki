---
title: Agent 输出检查：TTSR、权限规则与 PreToolUse hooks
description: 比较生成过程中检查文本与工具执行前检查参数的差异，以及反馈方式、适用范围和失败处理
type: comparison
category: ai
created: 2026-09-25
updated: 2026-09-26
timestamp: 2026-09-26
tags:
  - agent
  - harness
  - guardrails
source_refs:
  - raw/sources/2026-09-25-ttsr.md
  - https://omp.sh/docs/ttsr
  - https://code.claude.com/docs/en/hooks
  - https://code.claude.com/docs/en/permissions
resource:
  - raw/sources/2026-09-25-ttsr.md
  - https://omp.sh/docs/ttsr
  - https://code.claude.com/docs/en/hooks
  - https://code.claude.com/docs/en/permissions
---

# Agent 输出检查：TTSR、权限规则与 PreToolUse hooks

## 当前结论

选择检查方式时，先看需要检查什么，以及检查必须在哪一步完成。TTSR 在模型生成过程中匹配内容；权限规则与 PreToolUse hooks 在工具执行前决定是否允许调用。hooks 也可以返回修改建议，因此不能按“只拒绝”和“会纠正”把它们分成两类。

## 备选项与差异

| 机制 | 检查什么 | 匹配后如何处理 |
| --- | --- | --- |
| omp TTSR | 生成中的文本、工具参数或 edit/write 引入的源码；scope 决定范围 | 默认停止当前生成，将规则正文提供给模型并重试；也可以配置成不中断，只补充提醒 |
| Claude Code permissions.deny | 权限系统支持的工具与参数模式 | 拒绝匹配的调用；具体匹配方式取决于工具 |
| Claude Code PreToolUse hooks | 工具名称与完整输入，也可由脚本补充检查 | 可拒绝调用并向模型返回原因，也可修改输入或补充上下文 |

TTSR 的 `thinking` scope 仅适用于供应商实际提供相应流的情况；这不表示它能检查模型未公开的内部推理。[TTSR 文档](https://omp.sh/docs/ttsr)说明了各类 scope 的范围。

PreToolUse 可以检查 edit/write 的输入内容，不一定需要解析 diff。其拒绝原因可以包含修改建议，详见 [PreToolUse 返回字段](https://code.claude.com/docs/en/hooks#pretooluse-decision-control)。

## 如何选择

如果要阻止某类工具操作，先检查[权限规则](https://code.claude.com/docs/en/permissions)能否准确表达限制；需要读取额外状态或进行自定义判断时，再考虑 PreToolUse hook。需要纠正助手正文、或希望在工具参数尚未生成完时就停止明显错误，可以考虑 TTSR。

例如，禁用某个 API 时，两种检查位置都可能适用：TTSR 可以在该名字出现时停止生成，hook 则可以检查完整的编辑输入。应通过实际样例比较漏检、误报和重试成本，不能仅凭拦截较早就认定更快或更可靠。

## 需要验证的限制

- TTSR 默认每条规则在一个 session 中触发一次；这能减少重复打断，却不保证同样的错误以后不会再发生。它也不能撤销此前已执行的工具调用。
- hook 的拒绝决定与 hook 自身执行失败是两回事。Claude Code 文档说明，普通错误及部分超时会让调用继续，因此不能把所有 hooks 都描述成“检查出错就拒绝”。见 [hook 退出码](https://code.claude.com/docs/en/hooks#exit-code-output)与[超时处理](https://code.claude.com/docs/en/hooks#timeouts)。
- 权限规则的匹配范围取决于工具；不能仅凭一个文件读取规则，就声称所有可能的读取途径都被禁止。
- 这些来源没有提供相同工作负载下的性能对比。本页不对 TTSR、权限匹配和 hooks 的成本排序。

## 来源指针

- [[raw/sources/2026-09-25-ttsr|TTSR 文档存档]]
- [omp TTSR](https://omp.sh/docs/ttsr)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
- [Claude Code permissions](https://code.claude.com/docs/en/permissions)
- [[omp（oh-my-pi）]]
