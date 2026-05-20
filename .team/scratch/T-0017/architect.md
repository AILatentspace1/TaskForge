PLAN_READY

## 架构决策

T-0017 目标：强化 heartbeat/planner 上下文加载逻辑

### 变更范围

1. `prompts/team-heartbeat.claude.md` — STEP 2 增加上下文加载子步骤（goals、signals、logs、git fetch）
2. `prompts/team-planner.claude.md` — planner 已有 context 段和历史日志读取（STEP 1 item 8），无需额外修改
3. `.team/prompts/` — 同步更新

### 设计理由

- heartbeat 缺少 signals.md 读取，导致无法感知信号变更
- 缺少 goals/current.md 读取，无法验证任务与目标对齐
- 缺少历史日志读取，无法了解前次运行上下文
- 缺少 git fetch，远程分支状态可能过时
