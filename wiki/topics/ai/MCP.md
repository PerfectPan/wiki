---
title: MCP
description: Model Context Protocol 从本地上下文连接协议演进为远程 Agent 基础设施的完整脉络、核心模型与选型边界
type: topic
category: ai
status: active
created: 2026-04-12
updated: 2026-07-30
timestamp: 2026-07-30
tags:
  - mcp
  - agent
  - oauth
  - protocol
  - security
source_refs:
  - raw/sources/MCP.md
  - https://www.anthropic.com/news/model-context-protocol
  - https://modelcontextprotocol.io/specification/2025-03-26/basic/transports
  - https://blog.modelcontextprotocol.io/posts/2025-09-26-mcp-next-version-update/
  - https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/
  - https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/
  - https://blog.modelcontextprotocol.io/posts/2025-12-19-mcp-transport-future/
  - https://modelcontextprotocol.io/specification/2026-07-28
  - https://blog.modelcontextprotocol.io/posts/2026-07-28/
resource:
  - raw/sources/MCP.md
  - https://www.anthropic.com/news/model-context-protocol
  - https://modelcontextprotocol.io/specification/2026-07-28
  - https://blog.modelcontextprotocol.io/posts/2026-07-28/
---
# MCP

## 摘要

Model Context Protocol（MCP）是 AI 应用连接外部数据、工具和工作流的开放协议。它不替代模型、Agent 框架或 function calling，而是标准化 Host、Client 与 Server 之间如何发现能力、发起调用、返回结果、处理授权并协商扩展。

MCP 的演进可以分成四个阶段：

1. 2024 年以本地 `stdio` 和上下文连接为起点；
2. 2025 年进入远程化，补齐 Streamable HTTP、OAuth、用户交互、结构化输出和 Registry；
3. 2025 年末开始承载长任务、扩展和企业治理；
4. 2026-07-28 将核心协议重构为无状态、可路由、可缓存的请求/响应模型。

它的核心价值一直是“统一协议”，但协议承担的范围已经从工具接入扩展到数据、交互、异步任务、UI 和授权边界。

## MCP 不是什么

- **不是 Agent 框架**：它不负责规划、记忆、反思、上下文压缩或多 Agent 编排。
- **不是 function calling 的替代品**：function calling 描述模型如何表达一次工具调用；MCP 描述应用如何发现并连接外部能力。MCP Client 可以使用模型原生 function calling，也可以解析模型生成的其他结构化输出。
- **不是工具市场本身**：Registry 和各产品的 Connector 目录负责分发与发现；MCP 负责连接时的协议。
- **不自动保证安全**：协议提供身份、授权和能力边界，但 Server 是否可信、工具权限是否过大、调用是否需要确认，仍由部署方和 Client 治理。

## 基本架构

```text
用户
  ↓
Host（Claude、IDE、Agent 应用）
  ├─ MCP Client A ── MCP Server A ── 文件、数据库或 API
  └─ MCP Client B ── MCP Server B ── SaaS 或内部系统
```

- **Host** 管理用户体验、模型上下文、权限与多个 Client。
- **Client** 与一个 Server 建立协议关系，把模型或 Host 的意图翻译成 MCP 请求，再把结果送回 Host。
- **Server** 暴露标准化能力，并负责实际访问本地资源或远程系统。

早期 MCP 的三类核心 primitive 是：

- **Resources**：由应用读取的上下文和数据；
- **Prompts**：Server 提供的可复用提示模板；
- **Tools**：模型或应用可以调用的动作。

后续版本加入或扩展了 elicitation、Tasks、Apps 和其他扩展能力，但“Host 掌握用户边界，Server 提供外部能力”仍是稳定心智模型。

## 演进时间线

### 2024-11：从本地上下文连接开始

Anthropic 在 2024-11-25 开源 MCP，希望用一套协议替代每个 AI 应用与每个数据源之间的定制集成。首批能力包括规范、SDK、Claude Desktop 的本地 Server 支持，以及 Google Drive、Slack、GitHub、Git、Postgres、Puppeteer 等示例 Server。

这一阶段的主场景是桌面端和开发工具：

- Client 通过 `stdio` 启动本地 Server；
- JSON-RPC 消息跟随进程生命周期；
- 双方通过初始化握手协商版本与能力；
- 重点是让模型读取本地上下文并调用工具，而不是大规模远程部署。

这解释了早期协议为何接近 LSP：它优先服务“一个 Host 与一个长期存活的本地进程双向通信”。

### 2025-03：远程 MCP 与 Streamable HTTP

随着 MCP 从本机走向远程服务，`2025-03-26` 规范用 **Streamable HTTP** 替代旧 HTTP + SSE transport：

- 一个 MCP endpoint 同时接受 HTTP `POST` 和 `GET`；
- Server 可选择用 SSE 返回流式消息；
- 初始化时可签发 `Mcp-Session-Id`；
- 仍保留双向请求、通知和 capability negotiation。

它让远程 MCP 可用，但把本地长连接模型也带进了 Web 基础设施：多实例服务往往需要 sticky session、共享 session store，网关还可能需要理解 JSON-RPC body。[[MCP SSE 多实例路由策略]] 记录的正是这一阶段的工程问题。

### 2025-06：交互、结构化结果与安全补强

`2025-06-18` 版本把 MCP 从“工具调用管道”推进为更完整的交互协议，重点包括：

- 工具结构化输出；
- Server 发起、Client 呈现的 elicitation；
- 更完整的 OAuth 授权模型；
- 针对 token passthrough、confused deputy、DNS rebinding 等问题的安全建议。

这时 MCP 已不只传递一次工具调用，还开始描述用户交互和授权流程。与此同时，Client 需要承担更明确的信任职责：展示调用内容、隔离令牌、执行最小权限，并防止 Server 借 Client 身份访问不该访问的资源。

### 2025-09 至 2025-11：生态分发、长任务与扩展

2025-09，官方 MCP Registry 进入预览，为公开 Server 提供统一发布与发现入口，也允许产品市场和企业私有 Registry 在其上建立子目录。

`2025-11-25` 一周年版本进一步加入：

- 实验性的 **Tasks**，支持 `working`、`input_required`、`completed`、`failed`、`cancelled` 等长任务状态；
- 可独立演进的 **Extensions**；
- URL mode elicitation，把凭据收集、第三方 OAuth 和支付等敏感交互移到浏览器；
- sampling with tools，让 Server 可请求 Client 侧模型与工具参与更复杂的循环；
- 本地 Server 安装安全要求、默认授权 scope 和企业身份策略。

这一阶段的变化说明 MCP 已从“上下文插头”变成 Agent 基础设施：除了工具和数据，还要处理长任务、用户交互、分发、身份和企业治理。

### 2025-12：有状态协议遇到规模化瓶颈

官方 Transport Working Group 总结了远程部署的共同问题：

- stateful connection 妨碍普通负载均衡和自动扩缩容；
- session 生命周期含义不清；
- 网关需要解析 JSON-RPC body 才能按工具路由；
- 简单工具也要承担会话存储和双向通信复杂度。

由此确定的方向是：**应用可以有状态，协议核心不必有状态**。这成为 2026 大版本的设计前提。

### 2026-07-28：无状态核心

第五版规范完成了 MCP 发布以来最大的结构变化：

- 移除 `initialize` / `initialized` 握手和 `Mcp-Session-Id`；
- 每次请求自行携带协议版本、客户端信息和能力；需要预发现时可调用 `server/discover`；
- `Mcp-Method` 和 `Mcp-Name` Header 让网关、WAF、限流与鉴权系统无需解析 body 即可路由；
- Multi Round-Trip Requests（MRTR）通过返回 `input_required`、补充输入后重试原调用，承载确认、补参数、elicitation、sampling 等中途交互；
- `tools/list`、`prompts/list`、`resources/list`、`resources/read` 支持缓存提示和确定性顺序；
- Tasks、MCP Apps、Skills over MCP 等进入显式协商、独立版本化的扩展框架；
- OAuth / OIDC 加强 issuer 校验和凭据签发方绑定，Dynamic Client Registration 转向 Client ID Metadata Documents；
- Roots、Sampling、Logging 和旧 HTTP + SSE transport 进入弃用期。

这使远程 MCP 更接近标准 HTTP 工作负载：请求可落到任意实例，更容易部署到 serverless、edge 和普通负载均衡后，也更容易接入缓存、观测和企业身份系统。

协议无状态不等于业务不能保存状态。跨调用状态应由工具显式签发 handle，并由 Client 或模型在后续参数中带回。状态因此成为调用数据的一部分，而不是藏在 transport session 中。

## 为什么 MCP 能成立

MCP 并没有发明工具调用。它解决的是更上层的组合爆炸：

```text
没有标准协议：N 个 AI 应用 × M 个外部系统 = 大量定制集成
采用 MCP：N 个 Client 实现 + M 个 Server 实现
```

这个近似只有在协议、SDK 和生态实现足够兼容时才成立，但它说明了 MCP 的长期价值：

- Server 可以面向多个 Host 复用；
- Host 可以用同一套机制接入多个外部系统；
- 工具描述、调用结果、授权和交互边界更容易形成公共基础设施；
- 企业可以在网关、Registry、身份和审计层集中治理。

## 安全边界

MCP 扩大了 Agent 的行动面，也扩大了风险面。至少要区分四层：

1. **Server 信任**：安装本地 Server 等同于运行代码；连接远程 Server 等同于授权一个外部服务。
2. **工具信任**：工具描述可能被投毒，工具实现也可能在更新后改变行为。
3. **身份与令牌**：禁止 token passthrough；令牌必须绑定受众和签发方，Client 不应把一个系统的凭据转交另一个 Server。
4. **动作授权**：删除、付款、公开发布等高风险动作不能因为“走 MCP”就跳过用户确认和最小权限。

早期 OAuth 讨论暴露出的 confused deputy 问题并非 MCP 独有，但 MCP 允许用户自由接入第三方 Client 与 Server，使这类信任关系更常见。2026 版本通过 issuer 校验和凭据绑定缩小协议层风险，仍不能替代产品侧权限设计。

## 当前选型

### 本地工具

优先使用 `stdio`：

- 适合单机、单用户、IDE 和桌面 Agent；
- 生命周期简单，不需要开放端口；
- Server 仍是本地代码，安装来源和文件权限必须审查。

### 远程服务

新 Server 优先实现 `2026-07-28` 无状态模型：

- 不依赖隐式 session；
- 跨调用状态使用显式 handle；
- 接入标准 OAuth / OIDC、网关、限流和审计；
- 只有确实需要时才协商 Apps、Tasks 等扩展。

### 旧服务迁移

- 先定位 `Mcp-Session-Id`、进程内 session、server-to-client request 和旧 SSE 依赖；
- 把业务状态与 transport 状态拆开；
- 将中途确认或补参迁移到 MRTR；
- 按 SDK 支持矩阵逐步升级，不必为了版本号一次性重写仍在兼容期内的部署。

## 相关页面

- [[MCP Client]]
- [[MCP SSE 多实例路由策略]]
- [[mcp-remote]]

## 来源指针

- [Anthropic：Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
- [MCP 2025-03-26：Transports](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)
- [MCP：2025-06-18 版本重点回顾](https://blog.modelcontextprotocol.io/posts/2025-09-26-mcp-next-version-update/)
- [MCP Registry 预览](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/)
- [MCP 一周年与 2025-11-25 版本](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/)
- [MCP Transport 演进路线](https://blog.modelcontextprotocol.io/posts/2025-12-19-mcp-transport-future/)
- [MCP 2026-07-28 规范](https://modelcontextprotocol.io/specification/2026-07-28)
- [MCP 2026-07-28 发布说明](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- `raw/sources/MCP.md`
