## T-0017: 强化 heartbeat/planner 上下文加载逻辑

**Goal**: ai-framework
**Skill**: engineering

### Summary

增强 heartbeat prompt STEP 2 的上下文加载，新增以下数据源读取：
- `<runtime_dir>/goals/current.md` — 目标对齐验证
- `<runtime_dir>/policies/signals.md` — 信号感知
- `<runtime_dir>/log/*.jsonl` — 运行连续性
- `git fetch <remote> --quiet` — 远程分支状态刷新

同步 planner prompt 到 `.team/prompts/`。

### DoD Results

| Check | Result |
|-------|--------|
| heartbeat-has-context-section | pass |
| planner-has-context-section | pass |
| prompt-valid | pass |

### Review Report

`.team/scratch/T-0017/gstack-review.md` — APPROVED

### QA Report

`.team/scratch/T-0017/gstack-qa.md` — SMOKE_OK

### Known Limitations

- 仅修改 prompt 文本，运行时行为取决于 Claude Code 对新指令的执行

---
*This is a draft PR awaiting human review.*
