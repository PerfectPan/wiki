---
title: SVG
description: SVG 的基础图形、描边动画与相关实现资料入口
type: topic
category: frontend
status: seed
created: 2026-04-12
updated: 2026-08-05
timestamp: 2026-08-05
tags:
  - svg
  - graphics
source_refs:
  - raw/sources/SVG.md
resource:
  - raw/sources/SVG.md
---
# SVG

- https://svg.wtf/ 可视化搭建 SVG 的网站
- https://www.joshwcomeau.com/svg/friendly-introduction-to-svg/
	- SVG 教程
- 基础图形：Line，Rectangles，Circles，Ellipses，Polygons
- 对 stroke-dashoffset 做动画
	- ```html
	  <style>
	    polygon {
	      stroke-dasharray: 763, 10000;
	      stroke-dashoffset: 763;
	      transition:
	        stroke-dashoffset 3000ms;
	    }
	  </style>
	  
	  <svg viewBox="0 0 280 320">
	    <polygon points="..." />
	  </svg>
	  ```

## Source Pointers

- `raw/sources/SVG.md`

## 相关页面

- [[wiki/syntheses/frontend/SVG 图标自动 Morph 的实现路径|SVG 图标自动 Morph 的实现路径]]
