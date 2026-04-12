---
title: SSH
type: topic
category: systems
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - ssh
source_refs:
  - raw/sources/SSH.md
---
# SSH

- SSH 没有类似 https 的证书认证方式，口令认证和基于密钥的安全认证（一个例子是 github 的认证方式，自己 gen ssh key 放到 github 服务器上）
- 连接 SSH：ssh -X([[X11]]) root@ip -p port
- [[WSL]] Ubuntu 设置开启 SSH 服务 https://www.jianshu.com/p/ad7761c3fa73
- 启动 SSH 服务：service ssh restart
- SSH 服务配置：（/etc/ssh）
	- ```yaml
	  Port 2222
	  ListenAddress 0.0.0.0
	  PermitRootLogin yes
	  PasswordAuthentication yes
	  ```
- TODO WSL 开机自动开启 SSH service
- TODO https://plantegg.github.io/2019/06/02/%E5%8F%B2%E4%B8%8A%E6%9C%80%E5%85%A8_SSH_%E6%9A%97%E9%BB%91%E6%8A%80%E5%B7%A7%E8%AF%A6%E8%A7%A3--%E6%94%B6%E8%97%8F%E4%BF%9D%E5%B9%B3%E5%AE%89/
- [[Windows]] 电脑配置：
	- ```
	  netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=2222 connectaddress=[[WSL address]] connectport=[[WSL SSH Service Port]]

	  netsh advfirewall firewall add rule name=WSL2 dir=in action=allow protocol=TCP localport=2222
	  ```
-

## Source Pointers

- `raw/sources/SSH.md`

