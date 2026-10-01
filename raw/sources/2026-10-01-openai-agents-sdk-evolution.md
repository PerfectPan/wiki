<!--
source: https://openai.com/zh-Hans-CN/index/the-next-evolution-of-the-agents-sdk/
type: blog
author: OpenAI
fetched: 2026-10-01
note: direct HTTP fetch returned 403; body recovered via web reader
-->

# Agents SDK 的全新演进

Agents SDK 正在从开发者工具演进为平台。此次更新引入三大新原语（Harness、Sandbox、Sessions）、统一的 Agent Server 部署方式，以及全新的 Codex CLI。核心主题：安全地跨文件与工具运行长时 Agent。

## 从 SDK 到 Agent Server

开发者的反馈很明确：Agents SDK 作为编排框架很出色，但缺少在本地与生产环境都可靠运行的运行时基础。因此 Agents SDK 正在演进为 Agent Server。

新增 `singleDeploy: true` 配置后，同一份代码既能本地运行，也能部署到云端 Agent Server。配置示例如下：

```ts
// 之前：本地使用 SDK
const agentServer = new AgentServer({
  register: async (server: AgentServer) => {
    server.agent(mathTutorAgent);
  },
});

// 现在：本地与远程同一代码
const agentServer = new AgentServer({
  singleDeploy: true,
  register: async (server: AgentServer) => {
    server.agent(mathTutorAgent);
    server.agent(codeReviewerAgent);
  },
});
```

三种运行方式：

1. **本地运行**：`agentServer.startLocal()`，适用于开发和测试。
2. **本地与云端同一 server**：`singleDeploy: true`，一次构建、处处运行。
3. **云端 Agent Server**：`singleDeploy: true` 且 `export default`，由平台托管，支持远程触发（webhook、定时、队列）。

云端还提供 playground（在 trace 视图里逐步查看 agent 行为）、与 Chat 后端会话融合的会话管理，以及统一的 traces 面板（本地日志会自动同步到云端，方便排查只在生产环境出现的问题）。

## 三大新原语

### Sandbox：更接近生产级安全的执行环境

Agent 的瓶颈正在从模型能力转向安全地跨文件与工具执行任务。Sandbox 在 Agent Server 内置安全沙箱中运行 agent 的自定义工具与 MCP 工具，提供：

- 完全系统访问（安装依赖、运行测试、跨文件编辑），同时保护基础设施的其余部分；
- 逻辑隔离的网络、文件系统和进程，无需复杂的容器编排；
- 内置提示注入防护。

早期数据显示：appsec bug 减少 45%，漏洞修复速度提升 2.5 倍（与传统渗透测试相比）。示例：

```ts
const sandboxedAgent = new Agent({
  name: "Sandboxed Agent",
  instructions: "You are a helpful assistant.",
  tools: [webSearch, shell],
  sandbox: {
    enabled: true,
    filesystem: [{ hostPath: "./src", sandboxPath: "/workspace" }],
    network: { allowedDomains: ["api.example.com"] },
  },
});
```

### Sessions：跨执行的状态

生产级 agent 是长时任务：启动可能要几小时前，运行可能要几天，且可恢复。Sessions 提供跨 agent 调用的检查点与恢复：

```ts
const session = await agents.sessions.create({
  agent: documentAgent,
  input: "Analyze all documents in the repository",
  sandbox: { enabled: true },
});

// 几天后恢复并继续
await agents.sessions.resume(session.id, {
  input: "Now create a summary based on your findings",
});
```

Sessions 与 Chat 后端的会话正在融合为统一的会话管理 API。

### Harness：Agent 运行的容器

Harness 是 Agent 运行的容器（当前为 alpha 预览）：为每个会话提供隔离的沙箱化环境，内置工具和 MCP 服务器在会话内可用，为长时 agent 生命周期提供更强的隔离与资源控制。它把 agent 当作完整的应用对待，而不只是请求处理函数：

```ts
const agent = new Agent({
  name: "Research Assistant",
  instructions: "You are a research assistant.",
  tools: [webSearch, fileEditor, shell],
  harness: {
    timeout: 3600000, // 1 hour
    maxTurns: 50,
    sandbox: { enabled: true },
  },
});

const harness = agent.as_harness(); // 使用 harness 运行 agent
await harness.run("Research the latest developments in quantum computing");
```

## Codex CLI：与 Claude Code 同期发布

新的 Codex CLI 与 Claude Code 同期发布。Codex 完全基于 Agents SDK 构建，将 SDK 的编排与原语引入 CLI。对开发者意味着：

- 在终端中获得 SDK 的全部能力；
- 可从 CLI 无缝迁移到云端运行；
- 原生支持 MCP 服务器与中间件。

```bash
# 快速开始
codex "Fix the failing tests in auth module"

# 使用 MCP 服务器
codex --mcp-config ./mcp.json "Analyze the codebase"
```

## 对开发者的影响

- **中间件**：可组合的中间件栈（自定义日志、guardrail、缓存逻辑），本地与云端行为一致；
- **改进的本地工具**：功能齐全的本地 playground 与云端 traces；
- **统一 API**：Sandbox、Sessions、Harness、Chat 之前是不同 API，正在收敛为统一体验，未来几个月推出 beta。

相关资源：

- 文档：https://platform.openai.com/docs/guides/agents
- 快速上手：`npm install @openai/agents` / `pip install openai-agents`
- 本地 CLI Agent Server：`npx @openai/agent-server start`
