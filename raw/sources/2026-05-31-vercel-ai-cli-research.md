# Vercel Labs ai-cli 调研摘录

来源时间：2026-05-31

## 来源

- GitHub: https://github.com/vercel-labs/ai-cli
- npm: https://www.npmjs.com/package/ai-cli
- 官方站点: https://ai-cli.dev
- 本地浅克隆：`/tmp/ai-cli-research`

## 仓库事实

- 仓库：`vercel-labs/ai-cli`
- 描述：Generate anything from your terminal
- 默认分支：`main`
- 创建时间：2025-07-28
- 最新推送：2026-05-31
- 最新 GitHub release：`v0.3.0`，发布时间 2026-05-31 00:27:25 UTC
- npm latest：`0.3.0`
- GitHub 数据：511 stars、46 forks、3 watchers、公开 issue 0
- 语言构成：TypeScript 为主，另有 MDX、JavaScript、CSS、Shell
- License：npm 包声明 Apache-2.0；GitHub API 未返回仓库 licenseInfo
- 包名：`ai-cli`
- CLI 命令名：`ai`
- Node 要求：`>=20`
- 包管理器：Bun `1.3.9`

## 功能事实

`ai-cli` 是一个面向终端和 agent 的生成型 CLI，基于 Vercel AI SDK 和 Vercel AI Gateway。核心命令：

- `ai text`：生成文本，支持 prompt、stdin、`--image` 视觉输入、system prompt、temperature、max tokens。
- `ai image`：生成或编辑图片，支持 prompt、stdin 图片、多个 `--image` reference、size、aspect ratio、quality、style。
- `ai video`：生成视频，支持 prompt 或 stdin 图片，默认更长超时。
- `ai models`：从 AI Gateway 拉取模型目录，支持按 type 和 creator 过滤，支持 JSON 输出。

通用能力：

- `-m, --model` 支持逗号分隔多模型。
- `-n, --count` 支持每个模型生成多份。
- `-p, --concurrency` 控制并发。
- `-o, --output` 指定文件或目录。
- `--json` 输出结构化 metadata。
- TTY 下图片/视频支持 Kitty graphics protocol 预览。
- 非 TTY 下 image/video 默认把原始二进制写到 stdout，agent 使用时应显式传 `-o`。

## v0.3.0 变化

- 新增 repeatable `--image` reference，支持本地路径、`file://`、`http(s)://` 和 data URL。
- `ai text` 可区分 stdin 是图片字节还是文本，避免把图片二进制当成 prompt。
- 之前 `v0.2.1` 修复了 npm 全局安装时 CLI binary 指向 TypeScript 源码导致不可执行的问题。
- `v0.2.0` 引入动态模型发现、模型能力/价格 metadata、language-image 模型路由、`--provider` 改名为 `--creator`，并移除 `ai completions`。

## 本地验证

- `npx -y ai-cli@0.3.0 --version` 返回 `0.3.0`。
- `npx -y ai-cli@0.3.0 models --json` 可无 API key 拉取公开模型目录。
- 2026-05-31 本地拉取模型目录结果：总计 248 个模型；capability 计数为 text 192、image 38、video 26。部分模型可能同时具备多个 capability。
- `npx -y ai-cli@0.3.0 text "hello" --max-tokens 5 --json` 在未配置 `AI_GATEWAY_API_KEY` 时失败，错误为 unauthenticated request to AI Gateway。

## 源码观察

- CLI 使用 `commander` 注册 `text`、`image`、`video`、`models` 四个命令。
- `fetchGatewayModels()` 直接请求 `https://ai-gateway.vercel.sh/v1/models`，5 秒超时。请求失败时返回空模型集合并输出 warning；失败不会永久缓存。
- 默认模型：
  - text：`openai/gpt-5.5`
  - image：`openai/gpt-image-2`
  - video：`bytedance/seedance-2.0`
- text/image 默认超时 120 秒，video 默认超时 300 秒。
- 多任务通过自实现 `pMap` 并发执行；全部失败 exit 1，部分失败 exit 2。
- 输出逻辑在 `outputPath` 存在时写文件；没有 `outputPath` 且 stdout 非 TTY 时写 stdout；stdout 是 TTY 时写默认 `output.<ext>`。
- reference image 读取会直接读取本地文件、接受 URL 或 data URL；没有看到明显的大小限制。
- `image` 命令会识别 AI Gateway 中带 `image-generation` tag 的 language model，并通过 `generateText` + messages API 路由。
- GitHub Actions CI 包含 typecheck、format、lint、build、test。
- 测试文件覆盖 CLI、parse、models、image references、p-map、png、mp4、h264、shimmer 等模块。由于本地环境没有 `bun`，本轮未运行仓库测试。

## 开放 PR 信号

截至 2026-05-31，开放 PR 包括：

- #54：拒绝部分数字 flag 值。
- #51：智能文件命名和默认输出目录。
- #50：多 provider 支持，包括 OpenRouter、fal.ai、OpenAI direct。
- #45：给 image/text/video 增加 `--timeout`。
- #44：image 增加 `--seed`。
- #43：流式输出 `ai text`。

这些 PR 说明当前 CLI 仍在快速补齐“自动化可靠性”相关能力，尤其是 provider 解耦、可复现生成、超时可配置、流式文本和输出命名。

## 初步判断

`ai-cli` 不应被理解为完整 agent 框架。它更像一个窄而实用的生成型工具层：把文本、图片、视频生成统一成稳定 CLI 入口，让脚本和 agent 可以通过 stdin/stdout、`--json` 和文件路径组合工作流。

当前适合用在低风险、可重试、人工可验收的素材生成链路，例如：

- 多模型文案比稿。
- 小红书封面/插图/短视频草稿生成。
- 截图视觉理解和 UI 问题解释。
- agent workflow 中的“生成一个文件产物”节点。

暂不适合作为高可靠生产链路唯一依赖：

- 强依赖 Vercel AI Gateway 可用性和模型目录稳定性。
- 生成调用成本需要外部记录，CLI 本身没有完整成本账本。
- 文件命名、超时自定义、多 provider、seed、streaming 等能力仍在开放 PR 中。
- 对 reference image / stdin 二进制缺少明显大小限制，自动化接入时需要外层约束。

