---
title: Morphicons 实现调研原始记录
created: 2026-08-05
source_type: website-and-source-code
source_refs:
  - https://www.morphicons.com/#how
  - https://github.com/guillermolg00/morphicons
  - https://github.com/guillermolg00/morphicons/releases/tag/v1.4.1
---
# Morphicons 实现调研原始记录

## 调研范围

- 官网 “How it works” 页面与交互演示。
- GitHub 仓库 README、`package.json`、核心源码与测试目录结构。
- 重点审阅的源码：
  - `src/core/parse.ts`
  - `src/core/normalize.ts`
  - `src/core/resample.ts`
  - `src/core/plan.ts`
  - `src/core/interpolate.ts`
  - `src/core/spring.ts`
  - `src/core/serialize.ts`
  - `src/dom/index.ts`

React、Vue、Svelte 和 React Native 适配层只核对架构和调用方式，没有逐行审阅。由于本地环境缺少 Bun，本次没有重新运行仓库测试。

## 直接观察到的实现事实

### 输入与归一化

- 接受 SVG `d` 字符串或结构上兼容 Lucide `IconNode` 的数据。
- 支持 `path`、`line`、`circle`、`ellipse`、`rect`、`polyline` 和 `polygon`。
- 将直线、quadratic curve、arc 和基础图形统一转换为 cubic Bézier。
- 不支持 `<g>` 和 `transform`；坐标需要是已展开的字面值。

### 重采样

- 每条子路径默认采成 64 个点。
- cubic Bézier 弧长使用 8 点 Gauss–Legendre quadrature 估计。
- 使用 safeguarded Newton 和二分 bracket 反求目标弧长对应的曲线参数。
- 默认拐角阈值为 `π/8`，即 22.5°。
- 拐角作为精确采样锚点，其余点按弧长分配。
- 闭合路径不把任意 `M` 起点当作固有锚点；其循环起点在规划阶段处理。

### 对应和路径匹配

- 同时尝试两种遍历方向。
- 闭合轮廓尝试全部循环偏移，以对齐后的评分选择起点。
- 子路径配对成本由质心距离与弧长差组成，长度差权重为 `0.35`。
- 子路径数量不同时使用满射分配；多出的路径由已有路径复制，而不是压缩到一个点。

### 对齐

- 使用闭式二维 Procrustes 求旋转、缩放和平移，不需要 SVD。
- 对遍历方向的评分为 `residual + 0.05 × |θ| / π`，用于在残差接近时选择较短旋转。
- 默认按子路径局部对齐。
- 拼接点云的全局 residual 小于 `5e-3` 时，共享整图旋转和缩放参数。

### 插值

- 相似变换在自然空间中插值：角度线性变化，缩放使用 `σ^t`，残余形变在已对齐坐标系中线性混合。
- 源码保留了 raw coordinate lerp 作为对照实现，但默认使用 polar interpolation。
- 每帧输出缓冲区预分配。

### 动画驱动

- 使用阻尼弹簧驱动进度。
- 弹簧通过半隐式 Euler 积分，内部目标步长为 `1/240s`，每帧最多拆 16 个子步。
- 所有实例共享一个 `requestAnimationFrame` scheduler。
- 动画中途切换目标时，从当前输出点集重新建立计划，并保留弹簧速度。
- 飞行过程中序列化采样后的 polyline；settle 后写回目标 canonical cubic path。
- DOM driver 会检查 `prefers-reduced-motion`。

## 项目状态快照

调研时间：2026-08-05。

- GitHub 仓库创建时间：2026-08-01。
- 本次调研时最新 Release：v1.4.1，发布时间为 2026-08-04。
- License：MIT。
- `package.json` 声明 ESM-only、zero runtime dependencies，并通过 subpath exports 提供 core、DOM、React、Vue、Svelte 和 React Native 入口。

项目状态会持续变化，以上数据只代表调研当日快照。

## 来源

- https://www.morphicons.com/#how
- https://github.com/guillermolg00/morphicons
- https://github.com/guillermolg00/morphicons/releases/tag/v1.4.1

