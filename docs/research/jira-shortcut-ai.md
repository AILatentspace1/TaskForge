# Jira AI vs Shortcut: 智能任务拆分机制调研

## 概述

本文调研 Jira AI (Atlassian Intelligence/Rovo) 和 Shortcut (Korey.ai) 的智能任务管理能力，聚焦任务拆分（split）、依赖推断和 AI 辅助工作流，提炼可改进 TaskForge planner prompt 的策略。

---

## 1. Jira AI (Atlassian Intelligence / Rovo)

### 1.1 核心概览

Atlassian Intelligence 现已整合入 **Rovo** 品牌，是 Atlassian 的企业级 AI 平台。核心优势在于全平台上下文拉取能力 — Confluence 文档、Jira 需求、Slack/Loom 对话等。2026 年新增 **Jira Agents**（基于 MCP 协议的 Agent 架构）和 **Workflow Builder**（AI 自动创建工作流状态和规则）。

### 1.2 任务拆分 — AI Work Breakdown

特性名 **"AI work breakdown"**，将 Epic/Story 自动拆分为子任务：
- AI 分析父 issue 的描述、验收标准及关联的 Confluence 页面
- 生成建议的 child work items 列表，每项含 summary 和 description
- 用户可逐个编辑、删除或自定义，确认后批量创建并自动关联
- 2025 年扩展至 **Jira Plans**（跨团队计划场景），支持估算发布日期和资源规划

### 1.3 子任务生成 — Create Child Work Items

- 基于父 issue 详情生成建议子任务列表
- 接受后自动创建并建立 parent-child 链接
- **"Create work items inline in the backlog"**（Beta）可从 Confluence 链接或 Loom 视频直接在 Backlog 内联生成

### 1.4 依赖推断

**Jira AI 目前没有独立的 AI 依赖推断功能。** 依赖关系仍需手动设置。但通过以下方式间接辅助：
- **NL Search in JQL** — 自然语言查询依赖（如 "show me all blockers for this epic"）
- **"Link similar work items"** — 发现相似 issue 并建立链接，间接辅助依赖识别

### 1.5 智能分配

**Rovo AI 目前没有自动推荐 assignee 的能力。** 任务分配依赖 Jira Automation 规则引擎（基于组件、自定义字段、Round-robin 等传统策略）。JSM 场景下有 **AI Ticket Triage**（自动分类和路由），但非 Jira Software 的通用能力。

### 1.6 自然语言创建

最成熟的能力：
- **AI Work Creation**（GA）：从 Confluence 页面直接识别并创建 Jira issue
- **Slack/Teams 集成**：从聊天线程上下文自动生成 summary 和 description
- **NL JQL Search**：自然语言翻译为 JQL 查询
- **AI Automation**：自然语言描述自动化规则，AI 自动生成 Automation rule

---

## 2. Shortcut (Korey.ai)

### 2.1 AI 概览: Korey + Shortcut for Agents

Shortcut 的 AI 战略在 2025 年转向 **AI Agent 协作模式**：
- **Korey.ai** — "AI Orchestration Agent"，连接工具、对话和代码，跨 Slack/GitHub/Shortcut 联动
- **Shortcut for Agents** — 将 AI Agent 像人类工程师一样指派 Story，能 scope 工作、写代码、更新文档、推进任务

### 2.2 AI Write: 自然语言创建任务

Korey 的核心能力是**自然语言到 Story 的转换**：
- 输入 "Can you turn this into stories for the team?"
- 自动分析 Slack 对话/文档上下文
- 创建 3 个开发就绪的 Story，每个含验收标准 (Acceptance Criteria)
- 关联相关 Slack 消息作为上下文
- 还能**改进现有 Story**，将模糊描述转化为清晰的验收标准

### 2.3 AI Estimate / AI 分类

Shortcut **不提供独立的 AI Estimate 或自动 Label 分类功能**。工作量估算仍依赖传统的 Story Points 手动分配。Korey 在创建 Story 时根据上下文自动填充规格和细节，间接辅助估算。

### 2.4 工作流自动化

基于规则的声明式系统（非 AI 驱动）：
- **VCS Automations** — GitHub/GitLab/Bitbucket PR 状态自动同步 Story 状态
- **Epic Automations** — Epic 自动开始/完成
- **Iteration Automations** — 自动创建未来迭代、将未完成 Story 移入下个迭代
- **自定义工作流** — 状态变更时自动触发操作

### 2.5 关键设计理念: "Anti-Jiraturation"

- **"Let us do the work you hate"** — 自动化消灭繁杂操作，而非增加认知负担
- **AI 作为 Teammate 而非工具** — Korey 是主动的编排者，不是被动响应的按钮
- **Engineer-first** — 键盘快捷键优先、快速加载、避免过度配置
- **产品与工程统一** — Roadmaps + Objectives (OKR) + Iterations 在同一平台

---

## 3. 对比分析

| 维度 | Jira AI (Rovo) | Shortcut (Korey) |
|------|----------------|-------------------|
| AI 定位 | 嵌入式 AI 助手 | AI Agent 编排者 |
| 任务拆分 | AI Work Breakdown (成熟) | Korey NL→Story 转换 |
| 拆分策略 | 分析 issue 详情 + 关联文档 | 分析 Slack/文档上下文 |
| 子任务 | 自动生成 child work items | 自动创建开发就绪 Story |
| 依赖推断 | 无（靠 Link Similar 间接辅助） | 无 |
| 智能分配 | 无（靠 Automation 规则） | Korey 可指派 Agent |
| 自然语言 | NL→Issue, NL→JQL, NL→Automation | NL→Story + AC |
| 自动化 | Jira Automation (规则引擎) | Shortcut Automations (声明式) |
| AI Agent | Jira Agents (MCP 协议, 2026) | Korey + Shortcut for Agents |
| 成熟度 | 内容生成强，推理弱 | Agent 协作创新，功能有限 |

---

## 4. 关键发现

### 4.1 共同空白

1. **AI 依赖推断** — 两者均无真正的 AI 驱动的依赖关系自动推断。这是 TaskForge 可以形成差异化竞争力的方向。
2. **AI 工作量估算** — 两者都不提供可靠的 AI Estimate 功能。Jira 依赖手动 Story Points，Shortcut 同样。
3. **智能分配** — 都依赖传统规则引擎而非 AI 推理。

### 4.2 各自优势

- **Jira AI**: 任务拆分（AI Work Breakdown）最成熟，拆分后可直接批量创建子任务并关联。NL→JQL 是独特能力。
- **Shortcut**: AI Agent 编排理念领先，将 AI 作为"队友"而非工具。Korey 的跨工具上下文拉取能力强。

---

## 5. TaskForge 可借鉴的策略

### 策略 1: 上下文感知的任务拆分

Jira AI 的 AI Work Breakdown 成功在于它不仅分析 issue 本身，还拉取关联的 Confluence 文档。TaskForge 的 planner prompt 应该：

**建议**: 在 planner prompt 中增加上下文注入步骤 — 拆分任务前先读取 goal 文件、已有 research 文档、signals 策略，确保拆分结果与项目上下文对齐。当前 prompt 已部分实现（读取 goal 和 signals），但可以更明确地指导"分析关联文档后再拆分"。

### 策略 2: Agent 式任务推进而非纯自动化

Shortcut 的 Korey 模式展示了 AI Agent 主动编排的价值。TaskForge 的 heartbeat 可以借鉴：

**建议**: heartbeat 不仅是定时巡检，还可以支持"主动推进"模式 — 分析当前 board 状态，主动识别阻塞、推荐优先级调整、预判依赖冲突。当前 heartbeat 已有 PM triage 能力，但可以增加"proactive advisory"输出。

### 策略 3: AI 驱动的依赖推断

这是两者共同空白，也是 TaskForge 最大的差异化机会：

**建议**: 在 planner prompt 中增加依赖推断规则：
- 分析任务间的 key_files 重叠 → 推断隐式依赖
- 分析任务 dod 中的 exec cmd 是否依赖其他任务的产出文件 → 推断执行依赖
- 在 board.json 的 blocked_by 字段中自动填充推断结果

---

## 6. Action Items

1. [ ] 增强 planner prompt 的上下文注入逻辑，拆分前显式分析关联文档
2. [ ] 在 heartbeat 中增加 proactive advisory 输出（阻塞预判、优先级建议）
3. [ ] 设计依赖推断规则并集成到 planner prompt 中
4. [ ] 评估是否在 scratch 中增加 advisory.md 记录 heartbeat 的主动建议
