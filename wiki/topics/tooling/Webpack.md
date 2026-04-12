---
title: Webpack
type: topic
category: tooling
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - sourcemap
source_refs:
  - raw/sources/Webpack.md
---
# Webpack

- devtool，其实就是 sourcemap 配置，有非常多的选项，分 dev 和 prod，然后还会分怎么反解，能不能解出第几行第几列，还是只能解出第几行，是 inline sourcemap 还是 data url 的形式 #Sourcemap
- 具体生成也有差异，我看 dev 模式的会有直接 eval 的方法来生成，需要有空具体研究一下
- 然后分包优化是需要你自己显示写出来的，不是内置的
- cacheGroups 就是让你自定义分包的规则
- ```js
  optimization: {
      splitChunks: {
        minSize: 30000,
        minChunks: 1,
        maxAsyncRequests: 5,
        maxInitialRequests: 4,
        automaticNameDelimiter: '_',
        chunks: 'all',
        cacheGroups: {
          reactBase: {
            name: 'reactBase',
            test: (module) => {
              return /^.*\/node_modules\/(?!@ant).*(react|redux).*$/.test(
                module.context
              );
            },
            chunks: 'initial',
            priority: 10,
          },
          editorCore: {
            name: 'editorCore',
            test: (module) => {
              return /^.*\/node_modules\/@opensumi\/(?!ide-utils).*$/.test(
                module.context
              );
            },
            chunks: 'initial',
            priority: 10,
          },
          vendor: {
            name: 'vendor',
            test: (module) => {
              return /node_modules/.test(module.context);
            },
            chunks: 'initial',
            priority: 5,
          },
        },
      },
      minimizer: [
        // For webpack@5 you can use the `...` syntax to extend existing minimizers (i.e. `terser-webpack-plugin`), uncomment the next line
        `...`,
        new CssMinimizerPlugin(),
      ],
    },
  ```

## Source Pointers

- `raw/sources/Webpack.md`

