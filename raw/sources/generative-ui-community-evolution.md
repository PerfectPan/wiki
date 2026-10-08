<!-- accessed: 2026-10-08; scope: public documentation, releases, pinned source specifications -->

# 生成式 UI 社区进展核查

主题正文见 [[wiki/syntheses/ai/generative-ui-evolution]]。本记录区分三种证据：官方已发布能力、公开规范和源码定义、本文从机制做出的设计推断。

## 来源快照

| 对象 | 日期或固定版本 | 采用的资料 |
| --- | --- | --- |
| Claude 自生成视觉内容 | 发布公告 2026-03-12，Cowork 更新注明 2026-04-22；帮助页本次实时读取 | [官方公告](https://claude.com/resources/articles/claude-builds-visuals)、[Custom visuals](https://support.claude.com/en/articles/13979539-custom-visuals-in-chat-and-cowork) |
| MCP Apps | 规范版本 `2026-01-26`；仓库 HEAD `82221c0c8ce7661efa6771c9d461511b1650495f`，2026-09-25 | [规范](https://github.com/modelcontextprotocol/ext-apps/blob/82221c0c8ce7661efa6771c9d461511b1650495f/specification/2026-01-26/apps.mdx)、[SDK v2.0.3](https://github.com/modelcontextprotocol/ext-apps/releases/tag/v2.0.3) |
| A2UI | HEAD `db4306536438df46e4f0443b9c4ec0d5f1a42dc4`，2026-10-08 | [v0.9.1 协议](https://github.com/a2ui-project/a2ui/blob/db4306536438df46e4f0443b9c4ec0d5f1a42dc4/specification/v0_9_1/docs/a2ui_protocol.md)、[v1.0 候选说明](https://github.com/a2ui-project/a2ui/blob/db4306536438df46e4f0443b9c4ec0d5f1a42dc4/specification/v1_0/README.md) |
| json-render | 最新公开 release `v0.21.0`，2026-09-18；标签提交 `3ad381881194e7011ad3ccd6d668033495a06c29` | [release](https://github.com/vercel-labs/json-render/releases/tag/v0.21.0)、[catalog](https://github.com/vercel-labs/json-render/blob/3ad381881194e7011ad3ccd6d668033495a06c29/apps/web/app/%28main%29/docs/catalog/page.mdx)、[streaming](https://github.com/vercel-labs/json-render/blob/3ad381881194e7011ad3ccd6d668033495a06c29/apps/web/app/%28main%29/docs/streaming/page.mdx) |

MCP Apps 的规范版本号与 SDK npm/release 版本独立。A2UI 原 `google/A2UI` 仓库入口重定向至 `a2ui-project/a2ui`，源码指针采用当前仓库名。

## 证据对照表

| 结论 | 证据来源和位置 | 置信度与限制 |
| --- | --- | --- |
| Claude 的临时视觉内容与持久 artifact 有不同用途 | 官方公告正文；帮助页 “Keep a visual” | 高，产品文档说明；没有在实际账号中逐项操作 |
| 视觉内容可以复制、下载或保存为 artifact | 帮助页 “Keep a visual” | 高，文档可确认；不把早期文章的“临时”理解为永远不能保留 |
| MCP Apps 早于 Michael 的文章发布 | [2026-01-26 官方公告](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/)，原文日期 2026-03-13 | 高；因此不能写成原文带来的后续标准化 |
| iframe 隔离与部分参数流兼容 | 固定规范 [470–487](https://github.com/modelcontextprotocol/ext-apps/blob/82221c0c8ce7661efa6771c9d461511b1650495f/specification/2026-01-26/apps.mdx#L470-L487)、[1120–1142](https://github.com/modelcontextprotocol/ext-apps/blob/82221c0c8ce7661efa6771c9d461511b1650495f/specification/2026-01-26/apps.mdx#L1120-L1142) | 高，规范明确；只反驳“流式必然无 iframe”的推断，不据此识别 Claude 自生成视觉的私有实现 |
| MCP Apps 由宿主控制 View 与服务端的调用 | 固定规范 [388–401](https://github.com/modelcontextprotocol/ext-apps/blob/82221c0c8ce7661efa6771c9d461511b1650495f/specification/2026-01-26/apps.mdx#L388-L401)、[1680–1728](https://github.com/modelcontextprotocol/ext-apps/blob/82221c0c8ce7661efa6771c9d461511b1650495f/specification/2026-01-26/apps.mdx#L1680-L1728) | 高，工具可见性和隔离要求；没有验收每个宿主的实现 |
| 关键操作不能依赖部分工具参数 | 固定规范 [1120–1142](https://github.com/modelcontextprotocol/ext-apps/blob/82221c0c8ce7661efa6771c9d461511b1650495f/specification/2026-01-26/apps.mdx#L1120-L1142) | 高，规范明确 MUST NOT；部分通知是可选能力 |
| A2UI v0.9.1 是官网当前版本，v1.0 仍是候选 | [官网版本表](https://a2ui.org/)、固定源码 [v1.0 README](https://github.com/a2ui-project/a2ui/blob/db4306536438df46e4f0443b9c4ec0d5f1a42dc4/specification/v1_0/README.md#L1-L7) | 高，候选状态交叉核对；不以代码文件已存在推断稳定发布 |
| A2UI 把结构与数据分开，渲染端需要已知目录和校验 | 固定 v0.9.1 协议 “Protocol overview & data flow”“Component catalog”“prompt-generate-validate loop” | 高，规范定义；本次未运行各 renderer 的一致性测试 |
| A2UI v0.9.1 统一 MIME 类型并放宽 surface ID 生命周期唯一性 | [演进说明 5–28](https://github.com/a2ui-project/a2ui/blob/db4306536438df46e4f0443b9c4ec0d5f1a42dc4/specification/v0_9_1/docs/evolution_guide.md#L5-L28) | 高；活动 surface 之间仍要求唯一，不能重复创建未删除的 surface |
| json-render 用目录限定可描述的组件、动作和函数 | 固定 catalog 文档 8–18；生成提示词示例 90–108 | 高，文档与 schema 示例；不推断任意动作自动获得业务授权 |
| json-render 以 JSON Patch 流构建界面描述 | 固定 streaming 文档 8–105 | 高，格式与编译器调用；没有性能或不同 renderer 的运行验证 |
| 后端仍须独立处理身份、权限与持久化 | 基于上述规范分工的应用设计判断 | 推断；这是本文建议，不是三个项目共享的现成业务功能 |

## 容易混淆或已经落后的说明

- MCP Apps 和 Claude 自生成视觉内容不是同一个功能。Claude 的 [交互连接器说明](https://support.claude.com/en/articles/13454812-use-interactive-connectors-in-claude) 明确把连接器界面与临时生成的视觉内容分开。连接器的 iframe 文档不能直接证明后者的渲染方式。
- A2UI 官网介绍在本次读取时仍以 `actionResponse`、`surfaceProperties` 概括候选版；固定候选源码的演进说明已经描述 `callRendererFunction`、`callAgentFunction` 及相应响应，并移除 `theme`。正文只保留双向调用方向和候选状态；具体接口以 [候选演进说明](https://github.com/a2ui-project/a2ui/blob/db4306536438df46e4f0443b9c4ec0d5f1a42dc4/specification/v1_0/docs/evolution_guide.md#L5-L23) 为准。
- A2UI 的文档头存在早期创建日期；本次不拿该日期当作各版本正式发布时间。
- `pi-generative-ui` 的 README 消息示意仍出现 `user-message`，但当前 `PageToHost` 只有 `RpcCall`。当前行为采用类型定义、分派实现和 release 交叉核对，见 [[raw/sources/michael-liv-claude-generative-ui]]。
- “组件目录约束”不等于所有模型输出天然合法。A2UI 明确要求 prompt → generate → validate；json-render 也需要应用提供组件实现与动作处理。

## 核查方法与未覆盖范围

- 实时读取原文、官方公告、规范网站和 GitHub release；用 GitHub API 固定提交与标签，读取具体规范/文档文件。版本状态以 2026-10-08 的观测为界。
- Pi 深读范围含扩展入口、窗口状态、页面运行时、RPC、SVG 写入、构建和测试条件；其余社区对象主要核对公开规范、接口示例和发布变化，没有把文档检查写成实现端验收。
- 未安装 MCP App、A2UI renderer 或 json-render 示例，未访问个人 Claude 账号，未进行生成质量、性能、网络隔离或跨平台对比实验。
- 没有查到统一的可比成本或成功率证据，因此正文不按性能、价格、星数排序，也不声称覆盖全部社区项目。
- 图中“应用事件处理器 → 业务后端鉴权与持久化”是本文明确标出的设计建议，其余组件和消息可回查到所列源码或规范。
