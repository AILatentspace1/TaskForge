# AI PM 工具的 Review/Audit/Retro 自动化模式调研

> 调研来源：Linear、Jira、Asana、Monday、ClickUp、Agent 编排框架（CrewAI/AutoGen/LangGraph）
> 调研日期：2026-05-19

## 1. Review 自动化模式

### 1.1 Human-in-the-loop 确认流

所有主流 AI PM 工具采用 **Suggestion → Review → Confirm** 三步模式：

- **Monday AI**: AI 生成任务建议后，用户通过 Board Suggestions 界面逐一确认或修改
- **Jira AI**: AI Work Breakdown 生成 Epic/Story 后，需人工确认才创建子任务
- **Asana Intelligence**: Smart Rule 建议需人工审核后激活
- **ClickUp Brain**: AI 生成内容标注"AI-generated"，需人工确认

**TaskForge 借鉴**：当前 heartbeat 的 review-ready 状态已实现类似机制。改进点：
- 在 gstack-review 报告中增加 **diff-aware 变更摘要**，减少审查者的认知负荷
- 支持 **部分通过**（部分 APPROVED + 部分 NEEDS_CHANGES）

### 1.2 质量门禁（Quality Gates）

- **CrewAI Guardrail**: 运行时验证输出格式 + 自动重试（max 3 次）+ 失败反馈
- **LangGraph Checkpoint**: 状态快照支持 rollback/replay，review 不通过可回退到上一个 checkpoint
- **Linear Workflow**: 状态变更自动触发 review 要求（如 PR 需要至少 1 个 approve）

**TaskForge 借鉴**：
- 引入 **Guardrail 验证重试**：verify_dod 失败时反馈具体错误并自动重试（T-0011 已规划）
- 增加 **Checkpoint 快照**：每次状态变更前保存 board 快照，支持回退

### 1.3 Triage 快速操作

- **Linear**: Accept/Decline/Duplicate/Snooze 四键操作，秒级完成 inbox 清理
- **Jira AI**: AI Ticket Triage 自动分类和路由，减少人工判断
- **Shortcut**: 自定义自动化规则触发状态变更

**TaskForge 借鉴**：
- Planner prompt 增加 **triage 快速操作**（duplicate/decline/reclassify）
- Heartbeat PM triage 增加 **自动 decline** 规则（如 fingerprint 重复、超出 goal scope）

## 2. Audit 自动化模式

### 2.1 AI 操作审计日志

- **Asana AI Action Logs**: 完整记录每次 AI 操作的输入、输出、时间和触发条件
- **Monday Operation Tracking**: 每个 AI Block 执行都有可追溯的日志
- **Jira Audit Log**: 系统级操作审计，包含 AI 自动化的所有变更

**TaskForge 借鉴**：
- 在 `.team/log/` 中增加 **结构化 audit 事件**：
  ```json
  {"ts": "...", "action": "ai_operation", "block_id": "auto-categorize", "input": {...}, "output": {...}, "duration_ms": 1200}
  ```
- 为 heartbeat/planner 的每次 AI 决策记录 **决策依据**（如为什么选了 T-0014 而不是 T-0012）

### 2.2 依赖链追踪

- **Linear Blocking/Blocked**: 显式的依赖关系图，自动检测循环依赖
- **Jira Issue Links**: 多类型关联（blocks/is blocked by/relates to），支持可视化
- **LangGraph State Graph**: 有向图状态机，天然支持依赖追踪

**TaskForge 借鉴**：
- board.json 已支持 `blocked_by` 字段（T-0004 schema 扩展）
- 增加 **依赖链可视化** 输出：在 retro 中生成 markdown 依赖图
- Heartbeat 风险扫描（T-0010）已检测 blocked chain

### 2.3 变更溯源

- **Git-native Audit**: GitHub Projects 利用 git blame/commit 天然溯源
- **ClickUp Activity**: 每个任务的时间线视图，展示所有变更历史
- **Notion Page History**: 版本控制 + 差异对比

**TaskForge 借鉴**：
- 利用 git commit 记录天然实现 **代码变更溯源**
- 在 board.json 中增加 `state_history` 数组记录每次状态变更：
  ```json
  [{"from": "inbox", "to": "triaged", "at": "...", "by": "heartbeat", "run_id": "..."}]
  ```

## 3. Retro 自动化模式

### 3.1 风险驱动的回顾

- **Notion AI**: 持续风险扫描（sliding deadlines、repeated blockers、team overload），在 retro 中优先展示高风险项
- **Asana Smart Status**: AI 自动分析项目健康状态，识别延期风险和资源瓶颈
- **Monday Predictive Analysis**: 基于历史数据预测任务完成时间，在 retro 中对比预期 vs 实际

**TaskForge 借鉴**：
- Retro prompt 增加 **风险摘要段落**：汇总 heartbeat 风险扫描（T-0010 STEP 3.5）的发现
- 增加 **预期 vs 实际对比**：planner 生成任务时的 `why` 字段 vs 实际执行结果

### 3.2 自动化效率指标

- **ClickUp AI StandUp**: 自动生成个人/团队状态报告，量化工作进展
- **Monday Board Suggestions**: 展示 AI 操作的预计节省时间
- **Linear Insights**: 团队速度（velocity）趋势图，周期对比

**TaskForge 借鉴**：
- Retro 增加 **效率指标**：
  - 任务完成率（merged / created）
  - 平均 PR 合并时间（从 pr-open 到 merged）
  - Heartbeat 空闲率（IDLE 次数 / 总心跳次数）
  - Planner 候选利用率（promoted / candidates_seen）
- 在 `board.stats` 中持久化指标数据

### 3.3 知识沉淀

- **Notion AI**: 自动从 retro 中提取 action items，转化为下一周期的任务
- **ClickUp Brain**: 从历史任务中学习团队工作模式，优化未来任务估计
- **CrewAI Memory**: 跨运行记忆积累，duplicate 去重

**TaskForge 借鉴**：
- Retro 输出自动写入 `.team/policies/signals.md`，供下个 planner 周期消费
- 增加 **模式识别**：识别反复出现的问题（如特定类型任务总是失败），写入 `learnings`

## 4. 跨工具共性模式总结

| 模式 | 代表工具 | TaskForge 适用性 |
|------|----------|------------------|
| Human-in-the-loop 确认 | 全部 | 已实现（review-ready 状态） |
| Guardrail 验证重试 | CrewAI | 已规划（T-0011） |
| AI 操作审计日志 | Asana/Monday | 建议实现 |
| 依赖链可视化 | Linear/LangGraph | 部分实现（blocked_by） |
| 风险驱动回顾 | Notion/Asana | 已规划（T-0010 + retro） |
| 效率指标量化 | ClickUp/Monday | 建议实现 |
| 知识自动沉淀 | Notion/CrewAI | 部分实现（signals.md） |

## 5. TaskForge 行动建议

1. **高优先级**：增加 state_history 数组记录任务状态变更历史（audit 基础设施）
2. **中优先级**：Retro prompt 增加效率指标输出（任务完成率、PR 合并时间、空闲率）
3. **中优先级**：Retro 自动将 follow-up actions 写入 signals.md 供 planner 消费
4. **低优先级**：Planner prompt 增加 triage 快速操作（decline/duplicate）
5. **低优先级**：依赖链 markdown 可视化输出（在 retro 中展示）

## 6. 与已有调研的关联

- T-0002（Linear/GitHub）：triage 操作、blocking 依赖
- T-0005（Notion/Asana）：风险检测、Smart Status、4-step prompt
- T-0006（Monday/ClickUp）：AI Block、guardrail 重试
- T-0007（Agent 编排）：CrewAI Guardrail、LangGraph Checkpoint
- T-0008（跨框架总结）：综合模式对比
- T-0009（planner 4-step）：Asana 结构化 prompt
- T-0010（风险扫描）：Notion 持续风险扫描
- T-0011（Guardrail 重试）：CrewAI 验证重试
