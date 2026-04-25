---
title: Computer Network
type: topic
category: systems
status: seed
created: 2026-04-12
updated: 2026-04-25
tags:
  - network
  - tls
  - certificate
  - proxy
source_refs:
  - raw/sources/Computer Network.md
---
# Computer Network

- **CA 只是拿自己的 private key 给原证书 append 了一个加密的 hash 值而已**
	- ![CleanShot 2023-11-09 at 00.19.10@2x.png](../../../raw/assets/CleanShot_2023-11-09_at_00.19.10@2x_1699460367883_0.png)
- 系统代理可以理解成操作系统层面预先配好的一组代理配置。支持该能力的应用会直接走这份系统级配置，而不是在应用里再次手动输入代理地址；浏览器这类应用往往默认接入，另一些应用则需要单独配置
- 正向代理更像 Charles 这类本地代理；反向代理更接近负载均衡，对客户端隐藏后端真实服务实例
- HTTPS 代理通常依赖隧道代理与本地受信任证书，本质上是在你的机器上建立一个“被系统承认的中间人”。因此它不仅能转发请求，也可能读取和改写流量
- TLS / HTTPS 的稳定心智是：
	- 证书负责证明“我连到的是不是目标服务器”
	- 对称密钥负责后续大部分数据通信
	- 如果需要服务端也验证客户端，则要再引入双向认证或其他身份方案

## Source Pointers

- `raw/sources/Computer Network.md`
