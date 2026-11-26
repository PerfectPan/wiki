<!--
source: https://claude.com/resources/articles/skills-over-mcp-tasks-and-more
type: blog
published: 2026-11-24
fetched: 2026-11-26
-->

# MCP servers can now ship skills, run tasks, and more with Claude

- Category: Product updates
- Product: Claude apps, Claude Platform
- Date: November 24, 2026
- Reading time: 6 min

Skills over MCP is now in public beta in Claude, so MCP servers can ship skills alongside their tools. We're also giving servers ways to handle longer, more interactive work with Claude: Tasks and Elicitation are now generally available, and File Uploads is rolling out soon.

Two years ago, Anthropic [launched the Model Context Protocol (MCP)](https://www.anthropic.com/news/model-context-protocol) as a new standard for connecting AI agents to the systems where data lives. The spec has kept evolving to meet the connectivity needs of agents in production, and is becoming foundational for agentic messaging and orchestration.

With today’s updates, Claude can work with a server more like it works with another agent: learning from it, delegating to it, and exchanging input and files along the way.

## Ship expertise alongside tools with Skills over MCP

Tool names and descriptions tell Claude what a server can do, but don't cover how to handle specific use cases. With [Skills over MCP](https://modelcontextprotocol.io/extensions/skills/overview), servers can publish skills alongside their tools to help Claude take on longer, multi-step work. Claude loads a skill only when it's needed, keeping context use low. Skills update with the server, so developers can ship tools and guidance together and users have nothing separate to install.

Skills can cover best practices, step-by-step workflows, or even playbooks tailored to a user's account or organization. Using Skills over MCP:

- Shopify helps Claude design and update a merchant's online store end to end.
- HubSpot onboards customers and gets them set up in Claude.
- Atlassian helps Claude draw on deep organizational context for insights and work analysis.
- Carta will help Claude draft and issue equity from an uploaded document (coming soon).

Skills over MCP is in public beta in Claude and Claude Code, on by default for Pro, Max, and Ultra plans and available to Team plans once an admin enables it. Coming soon to Enterprise.

## MCP servers can now take on long-running, interactive work with Claude

Agents in production are taking on longer, more consequential jobs. Servers can now support that work by running it in the background, checking in with users, and receiving files from Claude.

**Hand off long-running work with [Tasks](https://modelcontextprotocol.io/extensions/tasks/overview).** Tool calls used to have to finish before Claude could move on. With Tasks, servers can run operations that take time, or even full agent loops, while Claude keeps working and picks up the result when it's ready. Using Tasks, [ZoomInfo](https://claude.com/marketplace/connectors/zoominfo) runs deeper accounts and contact research that previously took several prompts.

**Ask for input mid-call with [Elicitation](https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation).** Some actions need a user’s sign-off, like spending money or deleting data. With Elicitation, a server can pause to ask the user for input through a form or link, then continue where it left off. Using Elicitation:

- Supabase confirms costs before creating a paid project and before running destructive SQL.
- Railway asks before making potentially destructive changes, like removing a service.
- GitHub has users enter a repository's name before an agent deletes it.

Tasks and Elicitation are now generally available in Claude and Claude Code for Pro, Max, and Ultra plans, and rolling out to Team and Enterprise organizations.

**Send and receive files with [File Uploads](https://github.com/modelcontextprotocol/experimental-ext-file-uploads).** Claude will be able to pass files to MCP servers, not just text. The File Uploads extension sends PDFs, spreadsheets, and images to a server without passing them through the context window.

File Uploads is rolling out soon in Claude and Claude Code to Pro, Max, Ultra, and eligible Team and Enterprise plans.

## Add support to your plugins today

These features are part of the open MCP spec and its extensions, so a server that supports them works in any compatible client, not just Claude. To add support, see the docs for [Skills over MCP](https://code.claude.com/docs/en/mcp#use-skills-from-mcp-servers), [Tasks](https://code.claude.com/docs/en/mcp#mcp-tasks-for-server-authors), [Elicitation](https://code.claude.com/docs/en/mcp#respond-to-mcp-elicitation-requests), and [File Uploads](https://claude.com/docs/connectors/building/files?open_in_browser=1).

## Built on stronger foundations for connecting agents in production

Thanks to contributions from across the AI ecosystem, MCP now sees over 700 million monthly SDK downloads, and there are over 10,000 MCP connectors for Claude. We've worked with the MCP community to improve how MCP works in Claude. Over the past year, it has become:

- More token efficient: Tool search loads tool definitions only when needed, which can cut the context they use by over 85% in multi-server setups.
- Easier to scale: The latest MCP spec is stateless and supported across Claude products, making it easier to build servers and maintain their reliability as they grow.
- Simpler to authorize: The Enterprise Managed Auth extension lets admins authorize supported servers once, so users connect automatically.
- More interactive: The MCP Apps extension brings full interfaces into Claude, beside the conversation or full screen.

Together, these improvements make MCP easier to build on and adopt, and give the standard a strong base to continue evolving for the needs of agents in production.

## Thank you to the MCP community

MCP is an open standard, hosted by the [Agentic AI Foundation](https://aaif.io/) and shaped by the people who build on it. [Two years of progress](https://blog.modelcontextprotocol.io/posts/mcp-turns-two) came from the maintainers, contributors, and developers who wrote the spec, built the SDKs, shipped servers, and added client support. Thank you for making MCP what it is today.

---

## 扩展规范与文档核查记录（2026-11-26）

- **用途**：支撑 `wiki/topics/ai/skills-over-mcp.md`、`wiki/topics/ai/mcp-tasks.md`、`wiki/topics/ai/mcp-file-uploads.md`，以及 `wiki/topics/ai/mcp.md` 与 `wiki/topics/ai/mcp-2026-07-28.md` 的补充更新。
- **访问日期**：2026-11-26。
- **已读一手资料**：
  - Anthropic 产品更新公告：<https://claude.com/resources/articles/skills-over-mcp-tasks-and-more>（发布日期 2026-11-24；上面正文已剔除页尾“Related articles”导航链接和分隔噪音）。
  - MCP 两周年官方博客：<https://blog.modelcontextprotocol.io/posts/mcp-turns-two>（发布日期 2026-11-24；记录 Agentic AI Foundation 托管于 Linux Foundation、SDK 累计下载超 50 亿次且过去一年占超 45 亿次、Events 扩展进入 Beta、Skills over MCP 进入 Beta、File Uploads 处于草案原型、Enterprise-Managed Authorization 为 Stable）。
  - MCP 扩展总览与客户端支持表：<https://modelcontextprotocol.io/extensions/overview.md>、<https://modelcontextprotocol.io/extensions/client-matrix.md>（核对 SEP-3392 扩展生命周期 Experimental / Beta / Stable / Core 及各扩展当前阶段）。
  - Skills over MCP 概览与 Beta 规范：<https://modelcontextprotocol.io/extensions/skills/overview.md>、<https://raw.githubusercontent.com/modelcontextprotocol/ext-skills/main/specification/beta/skills.mdx>（核对 `io.modelcontextprotocol/skills`、SEP-2640 Final、`skills/list`、`skills/get`、`resources/directory/read`、manifest SHA-256 摘要校验、`"resources": "dynamic"`、512 文件 / 16 MiB 建议规模及 Security Considerations 全部条款）。
  - Tasks 扩展概览、SEP-2663 与稳定 Schema：<https://modelcontextprotocol.io/extensions/tasks/overview.md>、<https://modelcontextprotocol.io/seps/2663-tasks-extension.md>、<https://raw.githubusercontent.com/modelcontextprotocol/ext-tasks/main/schema/2026-07-28/schema.ts>（核对 `io.modelcontextprotocol/tasks` 处于 Beta, to Core 阶段、强一致创建、读写分离 `tasks/get` / `tasks/update`、协作式取消 `tasks/cancel`、终态与 `isError: true` / `failed` 边界、与 `2025-11-25` 不兼容对照、HTTP `Mcp-Name: taskId` 路由头及安全条款）。
  - File Uploads and Downloads 草案规范：<https://raw.githubusercontent.com/modelcontextprotocol/experimental-ext-file-uploads/main/README.md>、<https://raw.githubusercontent.com/modelcontextprotocol/experimental-ext-file-uploads/main/specification/draft/file-uploads.md>（核对 `io.modelcontextprotocol/files` 草案状态、`x-mcp-file`、`FileInput`、内联与 `upload_required` 两步带外上传、`requestState` 五步校验、`_meta["io.modelcontextprotocol/files"].downloads` 下载流程、目标安全校验、`omit`/`include` 凭据规则、网关中继规则、Security Implications 与 Open Questions）。
  - Claude Code MCP 官方文档：<https://code.claude.com/docs/en/mcp.md>（核对「MCP tasks that run on the server」「MCP tasks for server authors」「Respond to MCP elicitation requests」「Use skills from MCP servers」「Scale with MCP tool search」各章节的具体版本号、轮询区间、审批规则、扫描限制、不支持环境与组织策略）。
  - Claude 连接器文件传输文档：<https://claude.com/docs/connectors/building/files.md>（核对 Directory listing 要求、主机审批上限 50 个、`include` 限制、SDK 实测版本 `@modelcontextprotocol/server` 2.4.0 / `mcp` 2.3.0 / `fastmcp` 4.0.10 不兼容说明、文件数/响应时间/传输时长上限以及组织合规排除项）。
- **验证范围与未测试项**：
  - 本次仅阅读公告、公开规范与官方文档；未部署或运行任何 MCP Server / SDK，未在 Claude 或 Claude Code 账号中实测 Skills over MCP、Tasks、Elicitation 或 File Uploads 流程，也未抓包核对各客户端对扩展字段的实际兼容行为。
  - `modelcontextprotocol.io/extensions/client-matrix.md` 的 Markdown 导出表格中各客户端图标列未渲染勾选符号，因此正文中不据此汇总第三方客户端的逐项支持状态。
