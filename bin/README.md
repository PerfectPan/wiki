# bin

这个目录存放给 agent 和终端使用的命令入口。

当前主要命令：

- `wiki`
- `wiki.ts`

提示词库的命令也是同一个入口：

```text
bin/wiki prompts list [--tag <tag>] [--level <档>] [--json]
bin/wiki prompts search <关键词>
bin/wiki prompts show <id>
bin/wiki prompts check
```

提示词文件格式见 `prompts/README.md`。

说明：

- 这两个文件不是知识内容，而是仓库的工作流工具。
- `wiki.ts` 是 ESM，仓库没有构建步骤，模块类型靠根目录 `package.json` 的 `"type": "module"` 声明。Node 判定 `.ts` 的模块类型时会向上找最近的 `package.json`，仓库没有的话会越出仓库边界（例如命中 `~/package.json` 的 `"type": "commonjs"`），`bin/wiki` 就会报 `Cannot use import statement outside a module`。请不要删掉那个 `type` 字段。
- `bin/wiki research <topic>` 用于生成深度调研提示词，要求包含架构图、数据流、扩展面、证据矩阵和 Wiki PR 验收。
- 如果 Obsidian 没有显示不支持的文件类型，这个目录在文件列表里可能会看起来像“空目录”。
- 日常使用这个知识库时，可以优先关注 `wiki/` 和 `raw/`。
