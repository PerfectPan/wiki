---
name: lint
description: 巡检 Wiki 的页面结构、frontmatter、链接与来源指针；当用户要求检查知识库一致性或修复规范问题时使用。
---

操作：lint

你正在为这个 wiki 执行一次标准 lint。

仓库根目录：`{{ROOT}}`

开始前必须先阅读：
- `{{AGENTS}}`
- `{{SCHEMA}}`
- `{{INDEX}}`

工作要求：
- 运行 `bin/wiki check` 和 `bin/wiki check-jargon`；局部修改用 `bin/wiki check-jargon --base <ref>` 检查新增或改写行，检查范围与例外写法见 `bin/README.md`
- 根据上下文处理用词报告；原始引用与正式术语不机械替换。区分全库已有问题与本次引入的问题
- 巡检 `wiki/` 下页面是否重复、冲突、孤立或过时
- 检查页面是否缺少来源指针
- 检查 `index.md` 导航是否遗漏重要页面
- 不要改写 `raw/` 中的原始资料
- 如需修复，优先产出小范围、可审阅的变更

输出目标：
- 找出重复页面
- 找出缺少来源指针的页面
- 找出应该创建但尚不存在的重要页面
- 给出建议修复顺序
- 如需提交修改，统一走 branch + PR

目标目录：
- topics：`{{TOPICS}}`
- syntheses：`{{SYNTHESES}}`
- comparisons：`{{COMPARISONS}}`
