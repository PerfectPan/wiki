# Its Hover 收录核查

- 来源：https://www.itshover.com/icons；https://github.com/itshover/itshover
- 访问日期：2026-10-07
- 源码提交：`e5fc90512d9bcd8e6cba407ebf88cb9458989ca3`

## 核查事实

- [plug-connected-icon](https://github.com/itshover/itshover/blob/e5fc90512d9bcd8e6cba407ebf88cb9458989ca3/icons/plug-connected-icon.tsx#L1-L79) 与 [heart-icon](https://github.com/itshover/itshover/blob/e5fc90512d9bcd8e6cba407ebf88cb9458989ca3/icons/heart-icon.tsx#L1-L59) 使用 React 与 `motion/react`，通过 `onHoverStart` / `onHoverEnd` 控制动画，并暴露 `startAnimation` / `stopAnimation`。这两个文件未自行处理焦点触发或减少动态效果的偏好。
- [图标分发文件](https://github.com/itshover/itshover/blob/e5fc90512d9bcd8e6cba407ebf88cb9458989ca3/public/r/plug-connected-icon.json) 声明 `registry:ui`、`motion` 依赖，复制图标与类型文件；不能把演示站的完整 Next.js 依赖都当作使用图标的必要依赖。
- [LICENSE](https://github.com/itshover/itshover/blob/e5fc90512d9bcd8e6cba407ebf88cb9458989ca3/LICENSE#L1-L4) 是 Apache-2.0 文本，[package.json](https://github.com/itshover/itshover/blob/e5fc90512d9bcd8e6cba407ebf88cb9458989ca3/package.json#L1-L8) 却写 MIT；这里只记录声明差异，未向维护者核实具体授权。

## 收录判断与未测试项

按“可参考”收录：图标与动效源码有直接参考价值，实际接入时还需补齐外层按钮语义、键盘触发和减少动态效果，并核对许可。未安装组件、测试服务端渲染或测量包体与运行性能；两个图标的观察不推广成整个库的审计结论。
