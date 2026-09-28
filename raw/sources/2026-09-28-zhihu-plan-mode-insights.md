<!--
source: https://zhuanlan.zhihu.com/p/2087525914590573749
author: wangleineo
published: 2026-09-27 14:28 (page display)
fetched: 2026-09-28
method: browser-harness, existing Chrome tab, rendered article DOM
format: reading notes and paraphrase, not a verbatim copy
-->

# Plan Mode 已经死了吗？——阅读摘记

作者：wangleineo。浏览器中已读取正文；以下保留文章观点的摘要与来源关系，不收录导航、广告、账号信息或评论。

## 对原文的解读

作者将 Ayman Nadeem 的复盘理解为从预先固定计划的开发方式，转向观察结果后持续调整的迭代方式。减少独立的计划文档，不等于停止规划，也不等于文档失去解释系统的作用。

## 作者补充的信息分类

- **Spec**：用户和 agent 都知道的设计与技术决定，可以通过规格说明记录。
- **Defaults**：agent 知道、用户无需逐项关心的实现选择；用户不在意具体采用哪个可接受方案。
- **Gap**：agent 已经做出、用户尚不知道但应该知道的决定；用户若了解，可能会作出不同选择。

作者认为开发工具需要减少 Gap。模型产出更快、替人作出更多决定，并不意味着用户对系统的理解同步提升；作者判断，未经用户理解的决定可能随开发速度增加。文章未提供这一变化的量化测量。

## 文档与稳定行为

文章提到，关键变更可以用解释材料、图和交互演示帮助理解。重点是帮助人理解改变及备选方案，不是要求人在开始前批准一份穷尽所有细节的长计划。

作者还借《Regenerative Software》提出一个问题：如何描述软件，使 AI 多次生成实现时仍保持行为一致。这是文中的阅读启发，不能当作已经实现或验证的技术保证。

## 引用关系与核验范围

- 英文原文：[Plan mode is dead](https://www.aymannadeem.com/artificial/intelligence,/developer/tools/2026/09/24/plan-mode-is-dead.html)，仓库已有独立存档。
- 文中引用署名 bcherny 的讨论，涉及按需规划，以及用图和交互演示解释复杂变更。页面未给出对应讨论的直接链接，本次未独立核对原评论；不据此断言客户端当前实现或模型能力。
- 作者链接的另一篇文章：https://zhuanlan.zhihu.com/p/2035681706259247216 。本次未展开阅读。
- 文中书籍链接：https://learning.oreilly.com/library/view/regenerative-software 。本次未读取书籍内容。
- 已直接读取的来源：[Plan Mode 已经死了吗？](https://zhuanlan.zhihu.com/p/2087525914590573749)。
