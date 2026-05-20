# 跨框架调研综合总结与 TaskForge 行动计划

> 调研时间：2026-05-19，更新：2026-05-20 | 任务：T-0008 → T-0026 | 目标：ai-framework

## 1. 调研概览

对 5 大类 AI 项目管理/Agent 编排框架进行了系统调研，覆盖传统 PM 工具的 AI 增强和原生 Agent 编排两个维度。

| # | 框架 | 类型 | 文档 | 核心发现 |
|---|------|------|------|----------|
| 1 | Linear / GitHub Projects | 传统 PM + AI 增强 | linear-github-projects.md | 四层目标结构、Blocking/Blocked 依赖 |
| 2 | Jira AI / Shortcut | 传统 PM + AI 增强 | jira-shortcut-ai.md | AI 任务拆分、Korey 主动编排 |
| 3 | Notion AI / Asana Intelligence | AI-native PM | notion-asana-ai.md | 数据库驱动、4 步 Prompt 框架、风险扫描 |
| 4 | Monday AI / ClickUp Brain | AI-native PM | monday-clickup-ai.md | 原子化 AI Block、全工作区知识索引、Agent 分层 |
| 5 | CrewAI / AutoGen / LangGraph | Agent 编排 | agent-orchestration-patterns.md | Guardrail、Handoff、图状态机 |

## 2. 跨框架共性模式

### 2.1 Goal-to-Task 分解

所有框架都支持从高层目标到可执行任务的分解，但方式不同：

| 框架 | 分解方式 | 特点 |
|------|----------|------|
| Linear | Goals → Initiatives → Projects → Issues | 四层结构，可追溯 |
| Asana | AI Project Manager | 自然语言描述 → 完整项目计划 |
| ClickUp | AI Subtask Generator | 任务名/描述/评论 → 子任务建议 |
| CrewAI | Hierarchical Process | Manager Agent 动态分配 |
| AutoGen | Orchestrator 双账本 | Task Ledger + Information Ledger |
| LangGraph | 图状态机 | 条件边 + Send API 并行 |

**TaskForge 对应**: Planner 的 goal → task 分解。已借鉴 Asana 4 步框架（T-0009）和 Linear 四层结构（T-0016 增加 initiatives 层），实现 goal → initiative → task 三层链路。

### 2.2 依赖管理

| 框架 | 机制 | 自动推断 |
|------|------|----------|
| Linear | Blocking/Blocked 显式关系 | 否 |
| Asana | AI 依赖推断 | 是 |
| ClickUp | AI Assign + dependency | 是 |
| CrewAI | `context=[task1, task2]` | 显式声明 |
| LangGraph | 边 + 条件路由 | 显式定义 |

**TaskForge 对应**: `blocked_by` 字段已定义（T-0004 schema）。Planner 已实现 STEP 3.5 依赖分析 + 拓扑排序（T-0012），Heartbeat 已实现 STEP 3 跳过 blocked_by 未满足任务（T-0015）。

### 2.3 AI 任务生成

| 框架 | 生成方式 | 人机协作 |
|------|----------|----------|
| Asana | AI 生成项目计划 | 人工审核 |
| ClickUp | Subtask Generator | 建议 → 审核 → 确认 |
| Monday | Sidekick 5-7 子任务/30s | 嵌入式交互 |
| CrewAI | Agent 自主生成 | human_input 可选 |

**共识**: AI 生成任务后保留人工确认环节，而非完全自动化。

### 2.4 自动化工作流

| 框架 | 自动化模式 |
|------|-----------|
| Linear | 声明式自动化规则 |
| Monday | AI Blocks（原子化 AI 操作）+ Custom block（自然语言生成自动化） |
| ClickUp | Autopilot Agent（触发器驱动）+ Super Agent（多步骤） |
| CrewAI | Guardrail 验证 + retry 循环 |
| AutoGen | Handoff 按需委托 |
| LangGraph | 条件边 + 循环 + Send API |

**TaskForge 实现**:
- **Guardrail retry**（T-0011）: 借鉴 CrewAI，heartbeat verify_dod 失败后自动重试最多 2 次，记录 guardrail_feedback。
- **声明式自动化配置**（T-0022）: 借鉴 GitHub Actions/Linar，设计 automations.json 定义触发条件和超时。

### 2.5 状态管理

| 框架 | 状态模型 |
|------|----------|
| Linear | 固定状态机（Backlog → In Progress → Done） |
| Asana | Smart Projects 自动状态推断 |
| LangGraph | TypedDict + Reducer（增量合并） |
| AutoGen | 双账本（Task + Information） |
| CrewAI | 统一 Memory + scope 分层 |

**TaskForge 实现**:
- **state_history 审计**（T-0020）: 每个 task 增加 state_history 数组，记录每次状态变更的 from/to/at/by/run_id，为 retro 和 audit 提供数据基础。
- **风险扫描**（T-0010）: 借鉴 Notion AI，heartbeat STEP 3.5 扫描 stale_task（>48h）、blocked_chain、repeated_failure（≥3 attempts）三类风险。

### 2.6 人机协作

| 框架 | 模式 |
|------|------|
| ClickUp | @Brain 随时调用、AI 建议后确认 |
| LangGraph | `interrupt()` 暂停 + `Command(resume)` 恢复 |
| AutoGen | UserProxyAgent、Handoff to user、max_turns 轮次间反馈 |
| Monday | Sidekick 嵌入式（在工作位置获得 AI 帮助） |

### 2.7 Agent 编排

| 框架 | 编排哲学 |
|------|----------|
| Monday | Digital Workforce（角色化数字员工） |
| ClickUp | Agent 分层（Super/Autopilot/Ambient） |
| CrewAI | 角色驱动（role + goal + backstory） |
| AutoGen | 消息驱动（Topic/Subscription） |
| LangGraph | 图论驱动（State + Node + Edge） |

### 2.8 Prompt Engineering

借鉴 Asana Intelligence 的 4 步 Prompt 框架，TaskForge 重构了 planner prompt 结构（T-0009）：

1. **Context** — 描述 agent 身份、职责和硬限制
2. **Task** — 定义 6 步执行流程
3. **Input** — 列出所有输入文件及其用途
4. **Output** — 定义结构化输出字段和 task schema

这种结构使 AI 输出一致性显著提升，也便于后续增量修改单个 section。

### 2.9 Review & Audit

| 框架 | Review 模式 | Audit 能力 |
|------|------------|-----------|
| Linear | 内置 review 状态 + comment thread | 完整操作审计日志 |
| Jira | AI 审查建议 + approval gate | Audit Log（可导出） |
| Asana | Status Update 驱动回顾 | 时间线视图 |

**TaskForge 实现**:
- **Retro audit 模式**（T-0018）: 基于 T-0014 调研，retro prompt 增加 audit trail（读取 state_history 分析瓶颈）和 recurring pattern detection（识别重复问题）。
- **效率指标量化**（T-0021）: retro 输出 4 个核心指标 — 任务完成率、平均 PR 合并时间、Heartbeat 空闲率、Planner 候选利用率。

### 2.10 Context Loading

借鉴 ClickUp Brain 的全工作区知识索引（T-0017），TaskForge 强化了 heartbeat/planner 的上下文加载：

- Planner STEP 1: 读取 goals、signals、daily reports、历史 log、candidates、archive
- Heartbeat STEP 2: 加载 board + git status + signals + dirty file 保护
- 两者均读取 `git fetch` 后的远程状态

核心原则：**在决策前加载尽可能多的持久化真相**，避免基于过时状态做错误决策。

### 2.11 Triage Operations

借鉴 Linear 的 triage 快速操作（T-0019），Planner STEP 3 增加候选分类：

| Disposition | 条件 | 行为 |
|-------------|------|------|
| duplicate | fingerprint/title 匹配已有任务/候选 | 不推广，记录 matches |
| decline | 超出范围/不可验证/需付费 | 不推广，记录 reason |
| snooze | 有效但 board cap 已满 | 追加候选，标记 board-cap |
| promote | 有效非重复 | 正常推广流程 |

Wrap-up 输出 triage 汇总：`triage: promoted=N duplicate=N declined=N snoozed=N`。

## 3. 差异化机会

### TaskForge 的独特定位

| 维度 | 传统 PM 工具 | Agent 编排框架 | **TaskForge** |
|------|-------------|---------------|---------------|
| 运行方式 | Web UI | Python SDK | **CLI + cron** |
| 目标用户 | 非技术用户 | 开发者 | **开发者/自动化工程师** |
| AI 依赖 | SaaS 内置 | 用户自备 LLM | **CLI Agent 驱动** |
| 状态存储 | 云端数据库 | 内存/数据库 | **Git + JSON 文件** |
| 审计能力 | 有限 | 无 | **Git 原生审计** |
| 门槛 | 低（但付费） | 高（需编码） | **中（prompt 驱动）** |

TaskForge 的差异化优势：
1. **Git-native 审计**：所有状态变更通过 Git 追踪，天然具备审计和回滚能力
2. **零基础设施**：无需数据库、服务器，JSON 文件 + cron 即可运行
3. **Prompt 驱动**：通过修改 prompt 文件即可定制行为，无需编程
4. **多平台 Agent**：支持 Claude Code 和 Codex CLI，可扩展到其他 Agent

## 4. TaskForge 行动计划

基于跨框架调研，按优先级排序的具体改进步骤：

### P0 — 质量保障

| # | 行动 | 来源 | 状态 |
|---|------|------|------|
| 1 | 为 `quality_gates`/`dod` 引入 Guardrail 验证 + 自动重试 | CrewAI | **已完成** (T-0011) |
| 2 | 修复 do_not_touch 冲突（T-0009/T-0010） | 内部发现 | **已完成** |

### P1 — 核心能力

| # | 行动 | 来源 | 状态 |
|---|------|------|------|
| 3 | Planner 消费 board schema 依赖字段 + 拓扑排序 | T-0004 遗留 | **已完成** (T-0012) |
| 4 | Heartbeat 消费依赖字段进行阻塞检查 | T-0004 遗留 | **已完成** (T-0015) |
| 5 | 基于 Asana 4 步框架改进 planner prompt | Notion/Asana | **已完成** (T-0009) |
| 6 | Heartbeat 增加风险检测（stale tasks、sliding deadlines） | Notion AI | **已完成** (T-0010) |

### P2 — 能力增强

| # | 行动 | 来源 | 状态 |
|---|------|------|------|
| 7 | Heartbeat handoff 运行时交接 | AutoGen | T-0023 inbox |
| 8 | Heartbeat 每日进展报告生成 | 内部需求 | T-0024 inbox |
| 9 | ~~AI Block Schema~~ | Monday | **已 revert** (T-0013) |
| 10 | Context enrichment（强化上下文加载） | ClickUp | **已完成** (T-0017) |
| 11 | Initiatives 层（goal→initiative→task 三层结构） | Linear | **已完成** (T-0016) |
| 12 | state_history 审计追踪 | Jira/Linear | T-0020 awaiting-review |
| 13 | Retro 效率指标量化 | ClickUp/Monday | T-0021 awaiting-review |
| 14 | Retro audit/pattern 自动化 | T-0014 调研 | T-0018 awaiting-review |
| 15 | Planner triage 快速操作 | Linear | T-0019 awaiting-review |
| 16 | 声明式自动化配置 | GitHub Actions | T-0022 awaiting-review |
| 17 | Board velocity/cycle time 度量 | Linear | T-0025 inbox |

### P3 — 远期演进

| # | 行动 | 来源 | 状态 |
|---|------|------|------|
| 18 | 图状态模型（Reducer 增量更新 board.json） | LangGraph | 待评估 |
| 19 | Checkpoint 快照（状态回滚） | LangGraph | 待评估 |
| 20 | MCP 端点（外部 AI 访问 board 数据） | ClickUp | 待评估 |
| 21 | 子图组合（各角色独立封装） | LangGraph | 待评估 |

## 5. 目标达成度评估

| 目标 Success Criteria | 状态 | 证据 |
|----------------------|------|------|
| 完成至少 5 个框架调研 | **完成** | 6 个调研文档（Linear/GitHub、Jira/Shortcut、Notion/Asana、Monday/ClickUp、Agent 编排、Review/Audit/Retro） |
| 每个框架提炼可借鉴模式 | **完成** | 40+ 个模式，11 个已实现为 TaskForge 改进 |
| 将模式转化为改进建议 | **完成** | 21 条具体建议，15 个已形成任务（12 merged/closed） |
| 更新 schemas 支持新发现模式 | **完成** | T-0004 schema 扩展 + T-0016 initiatives + T-0020 state_history |
| 至少 3 个可执行改进任务 | **完成** | 15 个任务已执行，12 个已合并 |

**总计**: 19 个 PR opened，12 个 merged，6 个 awaiting-review，2 个 inbox 待推进。

## 6. 框架全景对比

| 模式 | Linear | Jira/Shortcut | Notion/Asana | Monday | ClickUp | CrewAI | AutoGen | LangGraph |
|------|:------:|:-------------:|:------------:|:------:|:-------:|:------:|:-------:|:---------:|
| Goal-to-Task | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| AI 任务生成 | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 依赖推断 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 自动化工作流 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 知识索引 | ✗ | ✗ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ |
| Agent 系统 | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 人机协作 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 并行执行 | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| 持久化/回滚 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| 嵌套编排 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| MCP 开放协议 | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |

## 7. 信息来源

### Phase 1 — 框架调研（T-0002~T-0008）
- docs/research/linear-github-projects.md（T-0002）
- docs/research/jira-shortcut-ai.md（T-0003）
- schemas/board.schema.json 依赖/handoff 扩展（T-0004）
- docs/research/notion-asana-ai.md（T-0005）
- docs/research/monday-clickup-ai.md（T-0006）
- docs/research/agent-orchestration-patterns.md（T-0007）
- docs/research/cross-framework-summary.md 本文档初版（T-0008）

### Phase 2 — 模式实现（T-0009~T-0022）
- .team/prompts/team-planner.claude.md 4 步框架重构（T-0009）
- .team/prompts/team-heartbeat.claude.md 风险扫描（T-0010）
- .team/prompts/team-heartbeat.claude.md guardrail retry（T-0011）
- .team/prompts/team-planner.claude.md 依赖分析 + 拓扑排序（T-0012）
- docs/research/ai-review-audit-retro.md review/audit/retro 调研（T-0014）
- .team/prompts/team-heartbeat.claude.md blocked_by 检查（T-0015）
- schemas/initiative.schema.json initiatives 层（T-0016）
- .team/prompts/team-heartbeat.claude.md + team-planner.claude.md 上下文加载（T-0017）
- .team/prompts/team-retro.claude.md audit/pattern 自动化（T-0018）
- .team/prompts/team-planner.claude.md triage 快速操作（T-0019）
- schemas/task.schema.json state_history 审计（T-0020）
- prompts/team-retro.claude.md 效率指标量化（T-0021）
- schemas/automations.schema.json 声明式自动化（T-0022）
