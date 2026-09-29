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
-