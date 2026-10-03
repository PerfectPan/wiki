# D2：沿用已有规则的协作复跑

先读[新综合页：云端 Agent 运行时与系统边界](wiki/syntheses/ai/cloud-agent-runtime-and-system-boundaries.md)，再与[旧 D](../d/wiki/syntheses/ai/tetral-agent-runtime-architecture.md)比较。**这轮尚未收到人工 GSB 评分。**

## 本轮做了什么

仍由 GLM 5.3 分析与审阅、Gemini 3.8 Flash 写作和返修。输入仍是[文章链接与“整理到 wiki”](task.txt)。使用新的房间、会话和工作区，从同一 Wiki 基线 `e595104eaf5135287bf282553b87a14a71dd8c03` 开始，自行抓取原文；没有提供旧候选稿，也没有指定标题、章节、页面数量或表格。

角色模板沿用已有全局表达偏好和 Wiki 写作规则，要求 GLM 对照实际正文提出具体意见。本轮还明确了来源清理、交接结束回合及已有页面增量更新的工作方式；这些变化都在[GLM 提示词](prompts/glm.md)和[Gemini 提示词](prompts/gemini.md)中公开。因此这轮用于观察实际工作流的结果，不能单独把变化归因于某一句提示词。

## 自动加载与显式读取的区别

规则由客户端按自己的约定加载。[OpenCode 文档](https://opencode.ai/docs/rules/)说明了项目 `AGENTS.md` 和全局 `CLAUDE.md` 的回退机制；[Claude Code 文档](https://code.claude.com/docs/en/memory#agents-md)说明了用户级规则及按版本、配置选择项目说明文件的方式。启动时的自动加载不需要模型再发起一次 `Read`，没有对应工具记录也不能证明规则没有进入上下文。

本机的 Codex 与 Claude 全局文件中，“表达风格”小节一致。本次实际 Claude ACP 会话使用其自带的 **2.1.280**，旧 D 也是该版本；终端命令的 2.1.285 不能代替 ACP 的运行版本。两位成员均有成功读取仓库 `AGENTS.md` 和 `SCHEMA.md` 的记录。完整历史请求未被保留，本记录不声称从工具日志还原了所有自动注入内容。[运行信息与读取证据](runtime-evidence.json)不包含私有配置正文或会话密钥。

## 主持人的介入记录

1. 开始时错误地要求两位成员显式重读全局文件；[初始 GLM 提示词](prompts/initial-glm.md)、[初始 Gemini 提示词](prompts/initial-gemini.md)及[额外核验消息](reading-verification-message.txt)保留供核对。GLM 的工作区外读取被 Room 策略拒绝，交接暂时停下。
2. 董事长指出应区分自动加载与工具读取。主持人撤回重复读取门槛，[纠正消息](autoload-correction-message.txt)只恢复原有加载方式并继续任务；没有复制全局规则、修改权限或使用其他文件访问方式绕过拒绝。
3. 模型完成一轮返修后，房间达到默认连续唤醒深度，主持人[续接最终审阅](final-review-resume-message.txt)，没有加入内容意见。

此前采用重复“阅读偏好”副本的试跑已停止，不计入本次结果。

## 模型交付

- 更新 [Agent 输出检查：TTSR、权限规则与 PreToolUse hooks](wiki/comparisons/ai/agent-output-checks.md)
- 更新 [Agent Native 系统接口设计](wiki/syntheses/ai/agent-native-system-interface-design.md)
- 新增 [云端 Agent 运行时与系统边界](wiki/syntheses/ai/cloud-agent-runtime-and-system-boundaries.md)
- 更新 [OpenSeek 会话与运行时模型](wiki/syntheses/ai/openseek-session-runtime-model.md)
- 更新 [持久化 Agent Harness 的设计模式](wiki/syntheses/ai/persistent-agent-harness-design-patterns.md)
- 更新 [Agent Harness 的设计取舍](wiki/topics/ai/agent-harness-design-tradeoffs.md)
- 更新 [Agent Harness](wiki/topics/ai/agent-harness.md)

另有[原文正文](raw/sources/2026-10-03-the-next-scaling-problem.md)、[导航](index.md)、[已有文件差异](changes.diff)和[检查结果及文件校验值](validation.json)。归档与模型最终文件逐字节一致；主持人未润色或纠正候选正文。

## 审阅产生的实际修改

GLM 提出一轮返修，Gemini 将 WAL 的“调用约定”改为“排序规则”，将事件表的“严格时间序”改为“线程内顺序”，拆分简答长句，并把哈希公式改成代码块。GLM 最终宣告模型审阅通过。七份知识页的 frontmatter 与用词检查均通过；这些检查不证明事实准确或文字易读。

## 主持人的独立观察

这些是主持人的对照意见，未代替人工 GSB，也未回写候选：

- 新页正文约 5,848 字符，旧 D 约 9,761 字符；篇幅缩短，保留了 Bash 调用过程和系统局限，也把关联信息补回已有页面。
- 文风问题仍在：如“单一事实权威”“防裂脑与过期间隔防护”“制品中心协作”。本轮不能证明强调遵循已有规则后，可读性已经稳定改善。
- **运行时与 reducer 被混为一谈。** 新页把 Runtime 标为“纯 Reducer / 无 I/O”，并称它不发起外部网络 I/O。原文的 *The runtime boundary* 小节只把无 I/O 限制用于纯 reducer；*Calling the model* 明确描述运行时组装并发出请求。
- **副作用保证写得过满。** 新页用幂等回执推导出“杜绝同一副作用执行两次”。原文 *Write ahead of execution* 明确限定，该协议不能让任意外部系统都具备事务保证。

因此，“模型审阅通过”与“格式检查通过”没有消除这些问题。本轮保留原稿供比较，尚未采用到正式知识页，也没有改动原有 D/E/F 候选或其评分。
