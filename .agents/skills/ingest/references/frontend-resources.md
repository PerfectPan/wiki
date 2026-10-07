# 前端资源的收录与分级

向 `wiki/topics/frontend/awesome-component-libraries.md` 添加组件库、视觉效果库或 CSS 参考站，或调整其分级时，按本文件处理。索引页保留资源用途、分级和来源；筛选步骤在此维护。

## 收录前核对

- 用途：读者遇到什么具体问题时会用到它？
- 用法：提供可安装的包、可复制的代码，还是供阅读的示例？需要哪些框架或依赖？
- 限制：浏览器兼容性、布局、服务端渲染、交互有哪些注意事项？区分文档说明和实际验证。
- 许可：能否找到许可和署名要求？只作阅读参考的站点，也不能默认其代码可任意复用。
- 证据：读过具体示例或使用文档，把来源、分级理由和未验证项记入该对象的原始资料。

## 分级

| 档 | 判断依据 |
| --- | --- |
| 推荐 | 示例有明确复用价值，说明和许可清楚；影响主要用途的限制已核对，或有值得学习的典型做法。 |
| 可参考 | 有具体用途和示例，但接入表现、兼容性或许可等仍需核对。 |
| 偏薄 | 材料不足以指导使用；仅在能说明具体问题、有教学价值时作为反例收录，否则留在原始资料中。 |

分级反映当前证据，不代表适用于所有项目。未经运行验证的内容不能写成实测结果。

完成原始资料评审后，在对应分级下添加一行用途与来源，并在 PR 中说明分级理由。具体对象值得单独解释时，再另建 topic；不要为收录步骤新增 synthesis。

## 明确不收

- 无 raw 素材、只有 star 数或营销页的链接（先补素材再谈收录）
- 纯 npm 重型框架组件库（MUI / Chakra 一类）——只当依赖使用时不构成收录；出现选型需求时走 comparison
- `raw/sources/component-library.md`（旧 Logseq 遗留 4 行链接清单：ant-design/pro-editor、headlessui、fancycomponents）——未评审，停留在 raw

## 尚未评审的候选

shadcn 生态动效组件站：Skiper UI、Aceternity UI、Magic UI、ReactBits、Animata、Origin UI、motion-primitives；旧清单遗留：ant-design/pro-editor、Headless UI、Fancy Components。

候选仅表示待评审，不表示已经收录。
