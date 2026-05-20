## 意图

增强 heartbeat 和 planner 的上下文加载，使其在每次运行时获得更完整的项目状态信息。

## 范围

- heartbeat prompt STEP 2 增加上下文加载项（goals、signals、logs、git fetch）
- planner prompt 已满足要求（已有 Context 段和历史日志读取）
- 同步更新到 .team/prompts/

## 可能涉及的文件

- `prompts/team-heartbeat.claude.md`（已修改）
- `prompts/team-planner.claude.md`（无需修改，已有 context）
- `.team/prompts/team-heartbeat.claude.md`（同步）
- `.team/prompts/team-planner.claude.md`（同步）

## 测试方法

- DoD exec 检查：grep -c context 两个 prompt 文件
- Markdown 格式验证：head -1 grep "#"

## 风险

- 低风险：仅修改 prompt 文本，不影响运行时代码
- 回滚：revert 单个 commit 即可恢复
