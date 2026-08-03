# Electron 扩展系统调研快照（2026-08-02）

## 来源

- 主文：<https://cy4n.dev/post/designing-ext-system-in-electron>，发布于 2026-07-24。
- Electron `utilityProcess`：<https://www.electronjs.org/docs/latest/api/utility-process>
- Electron `MessagePortMain`：<https://www.electronjs.org/docs/latest/api/message-port-main>
- Electron Security：<https://www.electronjs.org/docs/latest/tutorial/security>
- Electron Process Sandboxing：<https://www.electronjs.org/docs/latest/tutorial/sandbox>
- Electron Web Embeds：<https://www.electronjs.org/docs/latest/tutorial/web-embeds>
- Electron Protocol：<https://www.electronjs.org/docs/latest/api/protocol>
- MDN `moveBefore()`：<https://developer.mozilla.org/en-US/docs/Web/API/Element/moveBefore>

## 原文事实

- 宿主是 Electron renderer + preload + thin main process，特权能力主要由 Rust core 提供。
- 每个扩展运行在独立 `utilityProcess`，拥有 Node 环境。
- main process 创建进程并转移 MessagePort，使 extension host 与 renderer 直接通信。
- IPC 抽象为 transport，再实现 `call-method` / `method-result` RPC。
- 扩展身份绑定到来源 port，不信任消息自报身份；service wrapper 负责权限检查。
- 扩展包使用 Node package，manifest 声明 contributions / permissions；第一版加载 CommonJS。
- 扩展 UI 使用 sandboxed iframe、自定义 scheme、宿主 shell iframe 和 CSS variables。
- iframe keep-alive 使用 `moveBefore()` 在 DOM 中原子移动节点。

## 官方文档核对

- `utilityProcess` 确实提供 Node.js 和 MessagePort，语义近似 `child_process.fork`，但由 Chromium Services API 启动。
- `MessagePortMain` 支持消息传输和 port ownership transfer。
- Electron 官方推荐 iframe 使用 `sandbox`，不推荐把 `<webview>` 作为默认方案。
- 官方安全清单要求：context isolation、process sandbox、CSP、权限处理、导航限制、IPC sender 校验、自定义协议、禁止向不可信内容暴露 Electron API。
- `moveBefore()` 保留 iframe loading state，但依赖较新的 Chromium。

## 综合风险

- 独立进程隔离内存和故障，不等于 OS sandbox；Node extension 仍可读环境、文件、网络并启动进程。
- TypeScript service shape 不能校验运行时不可信消息。
- 极简 RPC 仍缺 timeout、cancellation、backpressure、crash cleanup、versioning 和 subscription disposal。
- 同源 shell iframe 与 extension iframe 的 DOM 访问可能是双向的，必须用 sandbox、CSP、origin/source/schema 校验补边界。
- 自定义资源路由必须防 `..`、symlink 越界、错误 MIME 和跨扩展 origin 混用。
- 扩展供应链还需要签名、来源、版本、更新完整性、权限 diff 和撤权机制。
