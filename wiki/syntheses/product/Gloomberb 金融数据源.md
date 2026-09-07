---
title: Gloomberb 金融数据源
description: Gloomberb（开源金融终端）的行情/财报/宏观/新闻数据分别来自哪里：Yahoo 非官方接口、SEC EDGAR、Treasury fiscaldata、Gloom Cloud，以及 broker 账号数据——免费源的可借鉴性与风险
type: synthesis
category: product
created: 2026-09-07
updated: 2026-09-07
timestamp: 2026-09-07
tags:
  - market-data
  - yahoo-finance
  - sec-edgar
  - data-providers
  - bloomberg
source_refs:
  - https://github.com/gloom-sh/gloomberb/tree/946ab2cdb4a02b9504de9ef8a596e75957167a09
  - https://github.com/gloom-sh/gloomberb/blob/946ab2cdb4a02b9504de9ef8a596e75957167a09/src/sources/yahoo-finance/http.ts
  - https://github.com/gloom-sh/gloomberb/blob/946ab2cdb4a02b9504de9ef8a596e75957167a09/src/sources/yahoo-finance/requests.ts
  - https://github.com/gloom-sh/gloomberb/blob/946ab2cdb4a02b9504de9ef8a596e75957167a09/src/sources/yahoo-finance.ts
  - https://github.com/gloom-sh/gloomberb/blob/946ab2cdb4a02b9504de9ef8a596e75957167a09/src/sources/sec-edgar.ts
  - https://github.com/gloom-sh/gloomberb/blob/946ab2cdb4a02b9504de9ef8a596e75957167a09/src/api-client/paths.ts
  - https://github.com/gloom-sh/gloomberb/blob/946ab2cdb4a02b9504de9ef8a596e75957167a09/src/plugins/builtin/treasury-auctions/client.ts
  - https://github.com/gloom-sh/gloomberb/blob/946ab2cdb4a02b9504de9ef8a596e75957167a09/src/data/fred-series.ts
resource:
  - https://github.com/gloom-sh/gloomberb/tree/946ab2cdb4a02b9504de9ef8a596e75957167a09
  - https://github.com/gloom-sh/gloomberb/blob/946ab2cdb4a02b9504de9ef8a596e75957167a09/src/sources/yahoo-finance/http.ts
  - https://github.com/gloom-sh/gloomberb/blob/946ab2cdb4a02b9504de9ef8a596e75957167a09/src/sources/yahoo-finance/requests.ts
  - https://github.com/gloom-sh/gloomberb/blob/946ab2cdb4a02b9504de9ef8a596e75957167a09/src/sources/yahoo-finance.ts
  - https://github.com/gloom-sh/gloomberb/blob/946ab2cdb4a02b9504de9ef8a596e75957167a09/src/sources/sec-edgar.ts
  - https://github.com/gloom-sh/gloomberb/blob/946ab2cdb4a02b9504de9ef8a596e75957167a09/src/api-client/paths.ts
  - https://github.com/gloom-sh/gloomberb/blob/946ab2cdb4a02b9504de9ef8a596e75957167a09/src/plugins/builtin/treasury-auctions/client.ts
  - https://github.com/gloom-sh/gloomberb/blob/946ab2cdb4a02b9504de9ef8a596e75957167a09/src/data/fred-series.ts
---

# Gloomberb 金融数据源

## 问题

Gloomberb 免费终端里的行情、财报、宏观、新闻数据到底从哪来？哪些是官方免费接口、哪些是灰色抓取、哪些要 API key、哪些实际走它自己的云？如果我们要自建同类数据层，哪些能直接借鉴、哪些要绕开？

## 简答

本地免费行情/财报主力是 **Yahoo Finance 的非官方 JSON 接口**（crumb+cookie 握手、UA 伪装，无 key、无官方承诺）；US 披露与部分财报走 **SEC EDGAR 官方 API**（合规免费）；美债拍卖直连 **Treasury fiscaldata**；FRED 等宏观系列因需要 key 而**藏在 Gloom Cloud 后面**由官方服务器代取；实时行情、新闻线、earnings 文稿、X 数据、全局搜索属于 Gloom Cloud 商业数据层（Free 延迟 15 分钟 / Pro 实时）。

一句话：**能合规免费直连的（EDGAR、Treasury）它直连；要 key 的（FRED）收进自己后端；Yahoo 免费量大但灰色，靠「provider 可替换 + 多源降级」来对冲风险。**

快照：`gloom-sh/gloomberb@946ab2c`（v0.13.2，2026-09-07 读取源码）。

## 数据源分层总览

| 数据类别 | 本地免费路径 | 云端路径 | 备注 |
| --- | --- | --- | --- |
| 价格/当前报价 | Yahoo chart 接口（meta.regularMarketPrice） | Gloom Cloud `/market/*` | 本地报价是轮询近似，实时订阅流在云端 |
| 财报/基本面 | Yahoo fundamentals-timeseries + SEC EDGAR supplement | Gloom Cloud `/cloud/financials` | 仅 US+USD ticker 走 SEC 补充 |
| SEC filings / XBRL | SEC EDGAR 官方 API | Gloom Cloud SEC 路径 | |
| 期权链 | Yahoo v7 options | Gloom Cloud options | |
| 宏观（FRED 系列） | 无 | Gloom Cloud `/cloud/fred`（官方后端代取） | FRED 免费但要 key，客户端不直连 |
| 美债拍卖 | Treasury fiscaldata 直连 | — | 官方无 key |
| 新闻 | Yahoo search news + RSS | Gloom Cloud news + X（Pro） | 多源聚合 |
| 组合/券商数据 | 本地 + broker 插件（账号授权） | 不同步云 | 独立插件仓库 |

## 各源拆解

### 1. Yahoo Finance —— 免费主力，但是非官方抓取

代码：`src/sources/yahoo-finance/{http,requests,snapshots,options,quote-summary}.ts`、`src/sources/yahoo-finance.ts`

用到的端点全部是无 key 的非官方 JSON 接口：

| 端点 | 数据 | 需要 crumb |
| --- | --- | --- |
| `query1.finance.yahoo.com/v8/finance/chart/{symbol}` | K线/价格历史 + `meta.regularMarketPrice`（当前价近似） | 否 |
| `query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{symbol}` | 财报/财务指标时间序列 | 否 |
| `query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?modules=...` | 公司资料、股东、分析师、盈利日历 | **是** |
| `query1.finance.yahoo.com/v7/finance/options/{symbol}` | 期权链 | **是** |
| `query1.finance.yahoo.com/v1/finance/search?q=` | ticker 搜索、相关新闻 | 否 |

反爬机制（`http.ts`）：请求 `fc.yahoo.com` 拿 cookie → 请求 `query2.finance.yahoo.com/v1/test/getcrumb` 拿 crumb → 后续请求带 crumb+cookie；UA 伪装成浏览器、带 Yahoo Referer。容错：3 次重试、1.5s 指数退避、20s 超时，401/403/429 时清 crumb 重握手。

**免费报价的真相**：桌面端「接近实时」报价是 chart 接口 `meta.regularMarketPrice` + 轮询近似，不是交易所订阅流；真正的实时流（WebSocket）在 Gloom Cloud（Pro）。

### 2. SEC EDGAR —— 官方 API，最稳的合规源

代码：`src/sources/sec-edgar.ts`

官方公开接口，带合规 UA：

- `www.sec.gov/files/company_tickers_exchange.json`（ticker→CIK 映射）
- `data.sec.gov/submissions`（提交记录）
- `data.sec.gov/api/xbrl/companyfacts`（XBRL 结构化财报）

用途：对 **US 交易所 + USD 计价** 的 ticker 用 SEC 官方数据**补充/校准 Yahoo 的 financial statements**（`shouldSupplementSecStatements` 限定在美交所与美元标的）。这是可以直接照抄的官方路径。

### 3. Treasury fiscaldata —— 官方无 key，直连

代码：`src/plugins/builtin/treasury-auctions/client.ts`

美债拍卖直连 `api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/.../auctions_query`，无 key、浏览器端 CSP 也放行（`connect-src` 白名单含此域）。

### 4. FRED / Shiller 等宏观 —— 藏在 Gloom Cloud 后面

代码：`src/data/fred-series.ts`（`CACHE_SOURCE = "gloomberb-cloud"`）、`src/plugins/builtin/econ-statistics/client.ts`、`src/plugins/builtin/market-valuation/sources.ts`

FRED 官方 API 免费但要 key。Gloomberb 客户端**不直连 stlouisfed**，而是调 `api.gloom.sh` 的 `/cloud/fred`（`getCloudFredSeries`、`getCloudShiller`），由官方后端持有 key 代取——FRED 因此也变成了它的账号/订阅杠杆。启发：**「官方要 key 的免费源」的正确姿势是自托管代理，key 不下发客户端。**

### 5. Gloom Cloud —— 商业数据层

代码：`src/api-client/{paths,data,request,socket}.ts`、`src/plugins/builtin/shared/plan-access.ts`

- 默认 API：`https://api.gloom.sh`；实时走 `/cloud/ws` WebSocket。
- 覆盖：quote、financials、history、options、holders、analyst research、short interest、corporate actions、statements、SEC filings/13F、earnings calls/transcripts、CDS、Congress、经济日历、FRED、Shiller、yield curve、FX、news、tweets、全局搜索（transcripts+news+filings）。
- Free vs Pro：客户端写死 `CLOUD_QUOTE_DELAY_MINUTES = 15`、`CLOUD_NEWS_DELAY_HOURS = 12`；`effectivePlan`（free/pro/trial）由服务端 `/account/profile` 下发，延迟由云端施加，客户端不自行判定。
- 本地 Yahoo 能覆盖的（报价、财报）用户可不登云；云的价值在**本地源给不了的**：实时、transcripts、X、全局搜索、以及需 key 的宏观。

### 6. 新闻 —— 多源聚合

代码：`src/sources/yahoo-finance.ts`（`getNews` 走 Yahoo search newsCount）、`src/news/aggregator.ts`、`src/plugins/builtin/news/wire/rss/source.ts`

- 免费本地：Yahoo search 接口带出的新闻条目 + 各 RSS feed（throttled fetch，30 req/min，自带 TTL 缓存）。
- 云：Gloom Cloud news（免费 12 小时延迟）、X feed（Pro）。
- aggregator 按 provider priority 合并去重。

### 7. Broker / 券商数据 —— 用户账号授权，不是公开数据

代码：org `gloom-sh` 下独立插件仓库 `gloomberb-ibkr`、`gloomberb-ibkr-gateway`、`gloomberb-public`、`gloomberb-robinhood`、`gloomberb-simplefin`

- IBKR：Flex Web Service 账号同步 / Gateway 实时行情与交易。
- Public：官方 API secret，只读账号+持仓。
- Robinhood：走 **Robinhood Trading MCP server** 的只读账号/equity 接口。
- SimpleFIN：一次性 token 换只读持仓。
- 连接数据只存本机，**不进 Gloom Cloud sync**。

## 结论：免费源能不能借鉴

| 源 | 性质 | 借鉴建议 |
| --- | --- | --- |
| SEC EDGAR | 官方、免费、无 key、稳定 | ✅ 直接照抄；注意合规 UA 与频率 |
| Treasury fiscaldata | 官方、免费、无 key | ✅ 直接接；宏观/美债好来源 |
| FRED | 官方、免费但要 key | ⚠️ 可接，但 key 要放自己后端代理，别下发客户端 |
| Yahoo 非官方接口 | 免费、无 key、灰色 | ⚠️ 个人工具可用；生产慎押注；必须配多源降级 + 缓存 + crumb 握手整套容错 |
| Gloom Cloud | 商业订阅 | ❌ 数据不开放；可以借鉴的是「需要 key 的免费源收进后端做产品杠杆」这一层设计 |

架构层最值得抄的其实是**「provider 可替换」**：同一 `DataProvider` 接口 + 优先级路由（命中即止）+ SQLite TTL 缓存（stale/expire 两段式）——这是它敢把身家押在灰色 Yahoo 上还不出事的前提。

## 证据矩阵

| 结论 | 证据来源 | 证据位置 | 置信度 / 限制 |
| --- | --- | --- | --- |
| 本地免费行情/财报走 Yahoo 非官方接口 | 源码端点与 crumb 握手 | `src/sources/yahoo-finance/http.ts`、`requests.ts` | 高；端点可能随 Yahoo 变动 |
| quoteSummary / options 需要 crumb，chart / timeseries / search 不需要 | `fetchJson` vs `fetchJsonWithCrumb` 调用点 | `requests.ts`、`options.ts`、`quote-summary.ts` | 高 |
| SEC 仅补充 US+USD ticker 的 statements | `shouldSupplementSecStatements` | `src/sources/yahoo-finance.ts` | 高 |
| FRED 客户端不直连，走 gloomberb-cloud | `CACHE_SOURCE = "gloomberb-cloud"` | `src/data/fred-series.ts` | 高 |
| Treasury 直连 fiscaldata | CSP 白名单 + client | `worker.ts`、`treasury-auctions/client.ts` | 高 |
| Cloud Free=15min 延迟、Pro=实时 | 客户端常量 + `effectivePlan` 服务端下发 | `plan-access.ts`、`api-client` | 中；延迟数值是 2026-09 时点，随计划变更 |
| broker 数据只存本机不进云 sync | README 声明 + sync sanitize | `README.md`、`src/sync/core-contributors.ts` | 高 |

## 相关页面

- [[wiki/syntheses/product/Gloomberb 调研|Gloomberb 调研]]

## 来源指针

- `gloom-sh/gloomberb@946ab2cdb4a02b9504de9ef8a596e75957167a09`（2026-09-07 读取）
- `src/sources/yahoo-finance/`、`src/sources/sec-edgar.ts`、`src/data/fred-series.ts`
- `src/api-client/paths.ts`、`src/api-client/data.ts`、`src/plugins/builtin/shared/plan-access.ts`
- `https://gloom.sh/docs/cloud-market-data`
