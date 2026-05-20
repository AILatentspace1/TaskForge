PLAN_READY

## 架构决策

T-0018 目标：基于 T-0014 调研改进 retro prompt 实现 audit/retro 自动化

### 变更范围

1. `prompts/team-retro.claude.md` — STEP 2 增加 audit 上下文加载（risk-scan.json、历史日志）
2. `prompts/team-retro.claude.md` — daily report 增加 "Audit trail" 和 "Recurring pattern detection" 段落

### 设计理由

- T-0014 调研发现所有主流工具都有操作审计日志和模式识别能力
- 当前 retro 仅生成状态报告，缺少审计追踪和模式分析
- 增加 audit trail 为未来自动化决策提供可追溯依据
- pattern detection 可识别反复出现的问题并自动生成改进信号
