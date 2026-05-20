## T-0018: 基于 T-0014 调研改进 retro prompt 实现 audit/retro 自动化

**Goal**: ai-framework
**Skill**: planning

### Summary

基于 T-0014 调研（Linear/Jira/Asana review/audit/retro 模式），增强 retro prompt：

1. **Audit trail**: daily report 增加"审计追踪"段落，记录每次状态变更的结构化审计条目（任务 ID、状态变更、时间戳、触发源、AI 决策依据）
2. **Pattern detection**: daily report 增加"循环模式检测"段落，分析历史日志识别反复出现的问题（状态循环、CI 重复失败、依赖阻塞等），并自动生成改进信号
3. **上下文加载**: STEP 2 增加 risk-scan.json 和历史日志读取，为审计提供完整上下文

### DoD Results

| Check | Result |
|-------|--------|
| retro-has-audit-section | pass (grep -c audit = 4) |
| retro-has-pattern-section | pass (grep -c pattern = 4) |
| prompt-valid-markdown | pass |

### Review Report

`.team/scratch/T-0018/gstack-review.md` — APPROVED

### QA Report

`.team/scratch/T-0018/gstack-qa.md` — SMOKE_OK

### Known Limitations

- 仅修改 prompt 文本，运行时行为取决于 Claude Code 执行
- pattern detection 依赖历史日志积累，首次运行可能无足够数据

---
*This is a draft PR awaiting human review.*
