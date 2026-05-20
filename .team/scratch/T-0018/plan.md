## 意图

基于 T-0014 调研结果改进 retro prompt，增加 audit 追踪和 pattern 检测能力。

## 范围

- retro prompt STEP 2 增加上下文加载（risk-scan.json、历史日志）
- daily report 模板增加 "Audit trail" 段落
- daily report 模板增加 "Recurring pattern detection" 段落

## 可能涉及的文件

- `prompts/team-retro.claude.md`
- `.team/prompts/team-retro.claude.md`（同步）

## 测试方法

- DoD exec 检查：grep -c audit/pattern/head-1
- Markdown 格式验证

## 风险

- 低风险：仅修改 prompt 文本
- 回滚：revert 单个 commit
