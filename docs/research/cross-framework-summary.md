# 跨框架调研综合总结与 TaskForge 行动计划

> 调研时间：2026-05-19 | 任务：T-0008 | 目标：ai-framework

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

**TaskForge 对应**: Planner 的 goal → task 分解。可借鉴 Asana 的 4 步框架和 CrewAI 的 Hierarchical 模式。

### 2.2 依赖管理

| 框架 | 机制 | 自动推断 |
|------|------|----------|
| Linear | Blocking/Blocked 显式关系 | 否 |
| Asana | AI 依赖推断 | 是 |
| ClickUp | AI Assign + dependency | 是 |
| CrewAI | `context=[task1, task2]` | 显式声明 |
| LangGraph | 边 + 条件路由 | 显式定义 |

**TaskForge 对应**: `blocked_by` 字段已定义（T-0004 schema），但 planner 和 heartbeat 尚未消费。

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

### 2.5 状态管理

| 框架 | 状态模型 |
|------|----------|
| Linear | 固定状态机（Backlog → In Progress → Done） |
| Asana | Smart Projects 自动状态推断 |
| LangGraph | TypedDict + Reducer（增量合并） |
| AutoGen | 双账本（Task + Information） |
| CrewAI | 统一 Memory + scope 分层 |

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
| 1 | 为 `quality_gates`/`dod` 引入 Guardrail 验证 + 自动重试 | CrewAI | 候选已生成 |
| 2 | 修复 do_not_touch 冲突（T-0009/T-0010） | 内部发现 | **已完成** |

### P1 — 核心能力

| # | 行动 | 来源 | 状态 |
|---|------|------|------|
| 3 | Planner 消费 board schema 依赖字段 | T-0004 遗留 | 候选已生成 |
| 4 | Heartbeat 消费依赖字段进行阻塞检查 | T-0004 遗留 | 候选已生成 |
| 5 | 基于 Asana 4 步框架改进 planner prompt | Notion/Asana | T-0009 inbox |
| 6 | Heartbeat 增加风险检测（stale tasks、sliding deadlines） | Notion AI | T-0010 inbox |

### P2 — 能力增强

| # | 行动 | 来源 | 状态 |
|---|------|------|------|
| 7 | Heartbeat handoff 路由（根据 board 状态动态转移） | AutoGen | 候选已生成 |
| 8 | Heartbeat handoff 支持（跨平台交接） | T-0004 PR | 候选已生成 |
| 9 | AI Block Schema（标准化 AI 操作接口） | Monday | 待生成候选 |
| 10 | Context enrichment（强化上下文加载） | ClickUp | 待生成候选 |

### P3 — 远期演进

| # | 行动 | 来源 | 状态 |
|---|------|------|------|
| 11 | 图状态模型（Reducer 增量更新 board.json） | LangGraph | 待评估 |
| 12 | Checkpoint 快照（状态回滚） | LangGraph | 待评估 |
| 13 | MCP 端点（外部 AI 访问 board 数据） | ClickUp | 待评估 |
| 14 | 子图组合（各角色独立封装） | LangGraph | 待评估 |
| 15 | 效率量化指标 | Monday | 候选已生成 |

## 5. 目标达成度评估

| 目标 Success Criteria | 状态 | 证据 |
|----------------------|------|------|
| 完成至少 5 个框架调研 | **完成** | 5 个调研文档（Linear/GitHub、Jira/Shortcut、Notion/Asana、Monday/ClickUp、Agent 编排） |
| 每个框架提炼可借鉴模式 | **完成** | 每篇文档 3-8 个模式，总计 30+ 个模式 |
| 将模式转化为改进建议 | **完成** | 本文档 + 6 条具体建议已形成任务 |
| 更新 schemas 支持新发现模式 | **完成** | T-0004 schema 扩展已合并 |
| 至少 3 个可执行改进任务 | **进行中** | T-0009/T-0010 inbox + 3 个候选待 promote |

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

- docs/research/linear-github-projects.md（T-0002）
- docs/research/jira-shortcut-ai.md（T-0003）
- docs/research/notion-asana-ai.md（T-0005）
- docs/research/monday-clickup-ai.md（T-0006）
- docs/research/agent-orchestration-patterns.md（T-0007）
- schemas/board.schema.json（T-0004）
