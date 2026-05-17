# Linear vs GitHub Projects: 任务管理范式对比调研

## 概述

本文调研 Linear 和 GitHub Projects 的任务管理范式，提炼可借鉴的 goal-to-task 转化、board 设计、依赖管理和自动化 pattern。

---

## 1. Linear

### 工作流模型

Linear 采用极简、强观点的状态生命周期：`Backlog → Todo → In Progress → Done → Canceled`。

- **Triage**: 独立于正常工作流之外的收件箱，通过集成（Sentry/Slack/Intercom）创建的 Issue 默认进入 Triage，需人工审核后才进入正式流程。支持 Accept/Decline/Duplicate/Snooze 快速操作。
- **Cycles**: 类似 Sprint 的时间盒，默认两周，将 Issue 按迭代分组。

### 多维视图

- **List View** — 默认列表视图
- **Board View** — 按状态分列的看板
- **Timeline View** — 甘特图式时间线，展示项目进度和依赖

所有视图共享同一套 Filter 系统。

### 自动化

- **Triage Rules**: 基于可过滤属性的自动规则，支持跨团队路由
- **Workflow Automations**: 状态变更与 Release 里程碑联动
- **Webhook Triggers**: 12+ 种事件类型
- **Triage Intelligence**: LLM 驱动的智能分析，自动推荐 assignee、label 和关联 Issue

### Goal-to-Task 层次

```
Goals → Initiatives → Projects → Issues
```

- **Goals**: 最高层战略目标，跨团队、跨时间
- **Initiatives**: 将 Goal 拆分为重大主题
- **Projects**: 有明确起止日期的 Issue 集合
- **Issues**: 最小工作单元（Bug/Task/Feature/Epic）

### 依赖管理

通过 **Blocking Issues** 和 **Blocked Issues** 实现：
- Issue 可标记"被阻塞"或"阻塞其他"
- Timeline 视图以连线可视化依赖
- 完成前置任务后自动解锁后置任务

### 核心设计 Pattern

| Pattern | 说明 |
|---------|------|
| Opinionated Defaults | 提供合理默认配置，降低决策负担 |
| Triage as Inbox | 跨团队/集成请求隔离到 Triage，不污染正式工作流 |
| Cycles over Sprints | 更轻量的迭代概念，不强加 Scrum 仪式 |
| Speed as Feature | 以"速度"为核心卖点，从交互到架构都为此优化 |
| Keyboard-First | 全键盘导航，追求极快操作速度 |

---

## 2. GitHub Projects

### 工作流模型

GitHub Projects 不强制方法论，采用完全自定义的状态字段（Single Select）。默认 Todo / In Progress / Done，团队可自由定义。通过 **Built-in Workflows** 实现自动状态变更。

### 多维视图

- **Table View** — 高密度表格，支持筛选/排序/分组
- **Board View** — 经典 Kanban 看板
- **Roadmap View** — 基于自定义 Date/Iteration 字段的时间轴
- **Insights Charts** — 内置图表（burndown、饼图等）

每种 View 可独立配置筛选和分组方式，保存为命名视图。

### 自动化

- **When items are added** → 自动设置默认 Status
- **When items are closed/reopened** → 自动切换状态
- **When PRs are merged** → 自动关闭关联 Issue
- **Auto-archive**: 归档已完成 item
- **Auto-add**: 仓库中 Issue/PR 匹配条件时自动加入项目
- 可通过 **GraphQL API** 和 **GitHub Actions** 构建复杂自动化

### Issue 集成

核心 item 就是 Issue/PR，不是独立实体。项目和仓库数据实时双向同步。支持 **Draft Issues**（纯项目内草稿）和 **Sub-issues**（父子任务拆解）。

### Goal-to-Task 层次

```
Roadmap (里程碑/迭代规划) → Issue (具体任务) → Sub-issue (子任务拆解)
```

通过 Iteration 字段实现 Sprint 规划，Draft Issues 允许先规划后转换。

### 核心设计 Pattern

| Pattern | 说明 |
|---------|------|
| Item-centric | 一切都是 Issue/PR，项目只是视图层 |
| Bidirectional sync | 项目与仓库数据实时双向同步 |
| Custom fields as schema | 通过自定义字段定义团队元数据模型 |
| Methodology-agnostic | 不绑定 Scrum/Kanban，工具适配流程 |
| Template system | 项目模板包含视图、字段、工作流配置 |

---

## 3. 对比分析

| 维度 | Linear | GitHub Projects |
|------|--------|-----------------|
| 设计哲学 | 强观点、极简默认 | 灵活可定制、方法论无关 |
| Goal 层次 | Goals → Initiatives → Projects → Issues | Roadmap → Issue → Sub-issue |
| 默认工作流 | 固定 5 状态 | 完全自定义 |
| 自动化 | Triage Rules + Webhook | Built-in Workflows + Actions |
| 依赖管理 | 原生 Blocking/Blocked | 需通过自定义字段模拟 |
| 数据模型 | 独立实体 | Issue/PR 是一等公民 |
| AI 能力 | Triage Intelligence (LLM) | 无内置 AI |
| 迭代概念 | Cycles (轻量 Sprint) | Iterations |
| 适用场景 | 研发团队专用项目管理 | 开源/混合团队项目管理 |

---

## 4. TaskForge 可借鉴的 pattern

### Pattern 1: 分层 Goal-to-Task 链

Linear 的 `Goals → Initiatives → Projects → Issues` 四层结构提供了从战略到执行的可追溯链条。TaskForge 当前的 `goal → task` 两层模型可以借鉴中间层（类似 Initiative/Project），让 goal 可以拆分为更细粒度的主题，每个主题下再生成具体任务。

**建议**: 在 board.json 中增加 `initiatives` 字段，支持 goal → initiative → task 三层结构。

### Pattern 2: Triage as Inbox 隔离

Linear 的 Triage 机制将跨团队/集成的请求隔离到专门的收件箱，防止噪声污染正式工作流。TaskForge 的 `inbox` 状态有类似功能，但缺少快速分类操作（Accept/Decline/Duplicate）。

**建议**: 在 planner prompt 中增加 triage 快速操作指令，支持将 inbox 任务标记为 duplicate 或 decline。

### Pattern 3: 自动化规则引擎

两者都支持基于事件触发的自动化。Linear 的 Triage Rules 是声明式规则（条件 → 动作），GitHub Projects 的 Built-in Workflows 类似。TaskForge 的 heartbeat 已经实现了定时巡检，但缺少声明式事件规则。

**建议**: 未来可支持 `.team/policies/automations.json`，声明式定义事件触发规则（如 "当 task 状态变为 pr-open 时自动通知"）。

---

## 5. Action Items

1. [ ] 评估是否在 board.json 中增加 `initiatives` 层支持 goal → initiative → task 三层结构
2. [ ] 改进 planner prompt 增加 triage 快速操作（duplicate/decline）
3. [ ] 设计 `.team/policies/automations.json` 声明式自动化规则格式
4. [ ] 借鉴 Linear 的 Blocking/Blocked 机制增强 board schema 的依赖管理
