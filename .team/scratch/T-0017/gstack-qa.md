SMOKE_OK

## QA Evidence

### DoD Verification

1. `heartbeat-has-context-section`: `grep -c context .team/prompts/team-heartbeat.claude.md` → 1 (pass)
2. `planner-has-context-section`: `grep -c context .team/prompts/team-planner.claude.md` → 2 (pass)
3. `prompt-valid`: `head -1 .team/prompts/team-heartbeat.claude.md | grep -c "#"` → 1 (pass)

### Diff Summary

```
prompts/team-heartbeat.claude.md  — STEP 2 增加上下文加载项（goals、signals、logs、git fetch）
.team/prompts/team-heartbeat.claude.md — 同步
.team/prompts/team-planner.claude.md — 新增同步文件
.team/scratch/T-0017/architect.md — 架构决策
.team/scratch/T-0017/plan.md — 计划
```

### Affected Surfaces

仅 prompt 文本变更，无 UI/运行时影响。
