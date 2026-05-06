# 深度解析：Codex Pet Skill

- 来源：微信公众号文章《深度解析：Codex Pet Skill》
- 作者：lencx / 浮之静
- 发布时间：2026-05-02 18:47 上海
- URL：https://mp.weixin.qq.com/s/uH71k1yAoF6xjsOYmVAJBg
- 读取时间：2026-05-06

## 来源事实摘录

文章围绕 OpenAI Codex 的 `hatch-pet` skill 展开，核心不是宠物功能本身，而是它展示了 Skill 工程化的一种成熟范式。

### 文章主张

- 真正有价值的 Skill 不是角色扮演 prompt，也不是把提示词保存成文件，而是把领域经验、边界、工具链、失败处理、验收标准和执行流程压缩成 Agent 可稳定调用的执行协议。
- `hatch-pet` 表面是生成 Codex 电子宠物，实质是一个面向 Codex app 的 animated pet asset pipeline。
- 该 Skill 将不可控的图像生成限制在可验证的工程边界中：图像由 `$imagegen` 生成，确定性脚本负责编排、记录、抽帧、验证、打包和修复。

### hatch-pet 的资产协议

- 最终产物位于 `${CODEX_HOME:-$HOME/.codex}/pets/<pet-name>/`，包含 `pet.json` 和 `spritesheet.webp`。
- spritesheet 是固定 8 列 9 行的 atlas，尺寸为 `1536x1872`，每格 `192x208`。
- 9 行分别表示：`idle`、`running-right`、`running-left`、`waving`、`jumping`、`failed`、`waiting`、`running`、`review`。
- 未使用 cell 必须完全透明；每行动画不仅要好看，还要能被 Codex app 的状态机消费。

### 编排与边界

- `SKILL.md` 规定正常视觉生成必须委托给 `$imagegen`，脚本只做确定性工作。
- 不能手改 `imagegen-jobs.json` 标记完成，不能复制本地文件冒充生成结果，必须通过 `record_imagegen_result.py` 记录真实生成结果。
- `prepare_pet_run.py` 负责创建 run 目录、prompt、layout guide、`pet_request.json` 和 `imagegen-jobs.json`。
- `imagegen-jobs.json` 是 job manifest，记录任务依赖、输入、输出、来源、hash、派生规则和完成状态。
- `running-left` 可以在满足条件时由 `running-right` 镜像派生，否则需要重新生成。

### 子代理与写权限

- base job 完成并记录后，row-strip visual generation 使用 subagents 并行生成。
- 子代理可以读 prompt、调用 `$imagegen`、检查候选图并返回 selected source 与 QA note。
- 子代理不能修改 manifest、不能执行 record、不能 finalize、不能 repair、不能 package。
- 父代理独占 manifest 与 package 写入，形成 control plane / worker plane 分离。

### QA 与 repair

- `finalize_pet_run.py` 要求所有 job 完成后，校验 provenance 和 hash，然后抽帧、检查、拼 atlas、验证、生成 contact sheet、渲染预览视频并打包。
- 自动 QA 能检查尺寸、alpha、空 cell、帧数、hash、透明背景等结构正确性。
- 视觉一致性仍需要人或模型检查，因为脚本不能证明“这还是同一只宠物”或某个状态语义是否正确。
- repair 采用最小失败范围修复：失败哪一行就重新打开哪一行 job，而不是整套重跑。

### 文章抽象出的 Agent 工程启发

- 不要把模型输出直接当成果，而要把它当生产材料。
- 关键状态不能藏在上下文里，必须外部化成 manifest。
- 多代理的关键不是并行，而是提交权隔离。
- QA 要区分结构正确和语义正确。
- repair 比 retry 更像工程。
- 更普适的构造方法是：模型生成候选，manifest 保存状态，脚本编译产物，QA 切分结构与语义，repair 局部收敛，control plane 统一提交。

### Codex /goal 命令

文章末尾还提到 Codex v0.128.0 引入 `/goal <objective>`，用于设置目标并让 agent 在一轮执行结束后围绕目标继续推进，直到目标完成或 token 预算耗尽。作者将其理解为更强的目标驱动执行循环。