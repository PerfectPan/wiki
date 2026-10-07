# Letta Context Repositories 文档核对

- 访问日期：2026-10-07。
- 输入：[Introducing Context Repositories](https://www.letta.com/blog/context-repositories/)，文章标注 2026 年 2 月。
- 补充：[MemFS](https://docs.letta.com/concepts/memfs)、[Memory & dreaming](https://docs.letta.com/configuration/memory)。
- 范围：官方文章与当前文档；未运行 Letta Code、同步或冲突合并测试。

## 文章的核心设计

Context Repository 是 agent 可直接读写的 Git 记忆仓库。文件名、目录和 frontmatter 描述帮助 agent 先定位再读取；记忆更新有版本；后台整理可在独立 worktree 中编辑后合并。

文章把 `system/` 定义为总是进入系统提示词的内容，并用初始化、反思和整理三个例子说明如何维护记忆。它提供了设计动机，但安装命令和目录规则不能直接当作当前规范。

## 与当前文档的差异

| 位置 | 当前说明 |
| --- | --- |
| MemFS / Memory structure | 根目录文件每回合进入系统提示词；旧 agent 使用 `system/`；子目录以 `MEMORY.md` 索引按需读取。 |
| MemFS / Semantic and vector search | 默认不附带语义或向量索引，使用普通文件搜索；可选 MemFS Search mod 扩展搜索。会话历史搜索是另一项能力。 |
| MemFS / Versioning and synchronization | 云端 agent 的仓库由 Letta 托管，本地 checkout 提交并推送后同步；local-only agent 在本机提交并自行备份。 |
| MemFS / Shared memory | 每个 agent 默认有自己的 MemFS；多 agent 共享是另一个配置场景，不能把单 agent 跨会话同步称为任意 agent 共享。 |
| Memory & dreaming / Dreaming | 后台子 agent 回顾会话并更新记忆；可按完成步骤数或压缩事件触发；“Agent reviews before applying”是 agent 复核，不是人工审批。 |

## 判断

Git 能追踪文本变更、恢复版本并处理合并，不能验证事实真假，也不能自动判定两条互相矛盾的记忆谁正确。删除当前文件也不等于抹除 Git 历史或远程备份。以上是对其存储方式的工程判断，未声称 Letta 已提供这些额外保证。
