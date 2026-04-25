---
title: Redis
type: topic
category: systems
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - redis
source_refs:
  - raw/sources/Redis.md
---
# Redis

- Redis 往往在业务对数据读写性能要求高的场景下使用。通常用来作为缓存，即使缓存失效，也有正常的兜底逻辑。例如，业务将用户身份信息数据存储在 [[MySQL]]，由于数据量过大查询 MySQL 效率较低下，往往通过 session 将当前用户数据放在 Redis，并设置适当的过期时间，当 Redis 缓存失效时，用户重新登录，此时从 MySQL 读取用户信息并再次写入 Redis。
-

## Source Pointers

- `raw/sources/Redis.md`
