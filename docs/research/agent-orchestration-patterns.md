# 调研：Agent 编排系统的任务调度模式

> 调研时间：2026-05-18 | 任务：T-0007 | 目标：ai-framework

## 1. 概述

Agent 编排系统天然涉及 goal-to-task 分解、依赖管理和 handoff。本报告调研三大主流框架：CrewAI（角色驱动）、AutoGen（对话驱动）、LangGraph（图状态机），提炼 TaskForge 可借鉴的编排模式。

## 2. CrewAI

### 2.1 核心设计

CrewAI 以**角色驱动**为核心：Agent 通过 `role` + `goal` + `backstory` 三元组定义身份，Task 是最小执行单元。

### 2.2 执行模式

| 模式 | 特点 |
|------|------|
| **Sequential** | 任务按序执行，前一个输出作为下一个上下文 |
| **Hierarchical** | Manager Agent 动态规划、分配、审查任务 |
| **Consensual** | 多 Agent 民主决策（规划中） |

### 2.3 关键机制

**任务依赖与输出传递**：
- `context=[task1, task2]` 显式声明依赖，自动等待前置任务完成
- `async_execution=True` 支持并行执行，后续任务通过 context 声明同步点
- `output_pydantic` 约束结构化输出，`output_file` 自动落盘

**Guardrail 模式**：
```python
task = Task(
    description="Write a blog post",
    guardrails=[validate_word_count, "Content must be engaging"],
    guardrail_max_retries=3
)
```
验证失败时错误信息反馈给 Agent，Agent 修正后重试。

**统一 Memory 系统**：
- 复合评分：语义相似度 + 时效性 + 重要性
- 分层 scope：`/project/alpha/decisions`、`/agent/researcher`
- 自动整合：重复记忆合并（consolidation_threshold=0.85）

**错误处理**：
- Agent 级：`max_retry_limit`、`max_execution_time`、`max_iter`
- Task 级：`guardrail` + `guardrail_max_retries` 链式验证
- Memory 级：优雅降级，LLM 分析失败用默认值

## 3. Microsoft AutoGen

### 3.1 核心设计

AutoGen v0.4 基于**消息驱动**架构：Agent Runtime + Topic/Subscription pub/sub 通信。分为 Core API（底层消息传递）和 AgentChat API（高层团队编排）。

### 3.2 三种团队编排

| 模式 | 调度方式 | 适用场景 |
|------|----------|----------|
| **RoundRobinGroupChat** | 固定轮询 | 步骤固定、流程可预测 |
| **SelectorGroupChat** | LLM 动态选择下一个发言者 | 复杂场景、需要灵活调度 |
| **Swarm** | Agent 通过 Handoff 主动转移控制权 | 去中心化、按需委托 |

### 3.3 关键机制

**Orchestrator 双账本**：
- Task Ledger：高层计划，目标分解为子任务
- Information Ledger：收集到的信息和中间结果

**Handoff 模式**：
```python
agent = AssistantAgent("agent", handoffs=[
    Handoff(target="planner", message="Transfer to planner"),
    Handoff(target="heartbeat", message="Transfer to heartbeat")
])
```

**终止条件组合**：
```python
termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(20)
```

**Human-in-the-Loop**：
- `UserProxyAgent`：阻塞等待人类反馈
- `max_turns` + 循环：轮次间反馈，支持状态保存恢复
- Handoff to user：Agent 主动转交人类

**嵌套对话**：外层 Agent 触发内层 Group Chat 解决子任务，内部复杂性对外不可见。

## 4. LangGraph

### 4.1 核心设计

LangGraph 将工作流建模为**有向状态图**（Directed State Graph），核心三要素：节点（Nodes）、边（Edges）、状态（State）。

```python
graph = StateGraph(TaskForgeState)
graph.add_node("planner", planner_node)
graph.add_node("heartbeat", heartbeat_node)
graph.add_conditional_edges("heartbeat", router)
graph.compile()
```

### 4.2 状态管理

**Reducer 机制**：决定多节点更新同一字段时如何合并。

| Reducer | 行为 |
|---------|------|
| `operator.add` | 列表拼接 |
| `add_messages` | 消息去重追加 |
| 自定义函数 | 任意合并逻辑 |
| 无 Reducer | 直接覆盖 |

### 4.3 控制流

**条件边**：根据当前状态动态路由到下一个节点。
**循环**：原生支持有环图，节点可路由回自身。
**Send API（Map-Reduce）**：运行时动态并行，fan-out/fan-in 自动汇聚。

```python
def dispatch_tasks(state):
    return [Send("worker", {"task": t}) for t in state["pending_tasks"]]
```

### 4.4 持久化

- Checkpointer：每步自动保存状态快照
- 支持 MemorySaver（内存）、SqliteSaver（本地）、PostgresSaver（分布式）
- `thread_id` 隔离不同执行会话
- 状态历史与回放

### 4.5 子图与组合

每个角色封装为独立子图，有自己的内部状态 schema，通过映射与父图状态转换。支持模块化、复用、并行、隔离。

## 5. 对比分析

| 维度 | CrewAI | AutoGen | LangGraph |
|------|--------|---------|-----------|
| **核心范式** | 角色驱动 | 对话/消息驱动 | 图状态机 |
| **调度方式** | Sequential/Hierarchical | RoundRobin/Selector/Swarm | 条件边 + 循环 |
| **依赖管理** | context 列表 | Handoff 转移 | 边 + Send API |
| **状态管理** | Memory + scope | 双账本 | State + Reducer |
| **人机协作** | human_input | UserProxyAgent/Handoff | interrupt() |
| **错误处理** | Guardrail + retry | 终止条件组合 | Checkpoint 回滚 |
| **并行支持** | async_execution | Swarm | Send API |
| **持久化** | output_file | 无内置 | Checkpointer |
| **学习曲线** | 低 | 中 | 高 |
| **灵活性** | 中 | 高 | 最高 |

### 设计哲学差异

- **CrewAI**：**角色化思维** — 以 Agent 身份为中心，任务围绕角色分配。适合团队协作模拟。
- **AutoGen**：**消息思维** — 以通信协议为中心，Agent 完全解耦。适合分布式多 Agent 系统。
- **LangGraph**：**图论思维** — 以状态流转为中心，精确控制执行路径。适合复杂工作流编排。

## 6. TaskForge 可借鉴模式

### 模式 1：Guardrail + 自动重试（CrewAI）

TaskForge 的 `quality_gates` 和 `dod` 是静态定义，缺乏运行时验证和重试机制。可引入：
- 每个 dod 项定义验证函数
- Heartbeat 巡检时执行验证
- 验证失败自动反馈 + 重试（max_retries=3）

### 模式 2：Handoff 按需委托（AutoGen）

当前 Heartbeat/Planner/Retro 通过 cron 固定调度。可引入 Handoff 模式：
- Heartbeat 巡检后根据 board 状态动态 handoff 到 Planner 或 Retro
- 减少无效的定时运行

### 模式 3：图状态机 + Reducer（LangGraph）

board.json 可升级为图状态模型：
- 任务列表用 `operator.add` reducer 增量更新
- `blocked_by` 用条件边实现依赖检查
- Heartbeat 巡检循环建模为有环图

### 模式 4：双账本（AutoGen）

board.json 可拆分：
- Task Ledger：任务分解计划和 DoD
- State Ledger：当前状态、执行结果、历史

### 模式 5：分层 Memory（CrewAI）

`.team/scratch/` 目录天然对应 scope 分层：
- `/goals/ai-framework` — 目标级
- `/tasks/T-0001` — 任务级
- `/agents/planner` — 角色级

### 模式 6：Checkpoint 持久化（LangGraph）

每次 Heartbeat/Planner/Retro 执行后保存 board.json 快照：
- 支持状态回滚
- 历史演进追溯
- 中断后恢复

### 模式 7：子图组合（LangGraph）

Planner/Heartbeat/Retro 各自封装为独立子图：
- 独立开发、测试
- 灵活组合新角色（Reviewer、QA）
- 子图内部状态不污染全局

### 模式 8：嵌套编排（AutoGen）

Planner 分解的子任务触发独立嵌套循环：
- 任务内部的 Plan → Code → Review 循环
- 结果汇总回主 board
- 内部复杂性对外不可见

## 7. 跨框架对比（完整）

| 模式 | Linear/GitHub | Jira/Shortcut | Notion/Asana | Monday | ClickUp | CrewAI | AutoGen | LangGraph |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| AI 任务生成 | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 依赖推断 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 角色化 Agent | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 状态机 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| 人机协作 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 并行执行 | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| 持久化/回滚 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| 嵌套编排 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |

## 8. TaskForge 改进建议

1. **Guardrail 机制**：为 dod 增加 runtime 验证 + 自动重试 + 反馈循环（P0）
2. **Handoff 动态调度**：Heartbeat 根据 board 状态 handoff 到对应角色（P1）
3. **图状态模型**：将 board.json 升级为 Reducer 模式的增量状态（P1）
4. **双账本拆分**：board.json 拆为 Task Ledger + State Ledger（P2）
5. **Checkpoint 快照**：每次运行后保存 board.json 快照支持回滚（P2）
6. **子图组合**：各角色封装为独立子图，支持灵活扩展（P3）

## 9. 信息来源

- [CrewAI Documentation](https://docs.crewai.com/en/concepts/tasks)
- [CrewAI Memory](https://docs.crewai.com/en/concepts/memory)
- [CrewAI Hierarchical Process](https://docs.crewai.com/en/learn/hierarchical-process)
- [AutoGen v0.4 - Microsoft Research](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/)
- [AutoGen SelectorGroupChat](https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/selector-group-chat.html)
- [AutoGen Handoffs](https://microsoft.github.io/autogen/stable//user-guide/core-user-guide/design-patterns/handoffs.html)
- [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- [LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangGraph Subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs)
