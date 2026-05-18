# Open Source AI Project And Task Management Framework Research

Date: 2026-05-17

Goal: identify open source or open-core frameworks close to TaskForge's intended space: AI-readable project management, task boards, workflow state, delegation, audit trails, and research-to-task loops.

## Shortlist

| Framework | Fit for TaskForge | Useful patterns |
|---|---|---|
| [Taskosaur](https://github.com/Taskosaur/Taskosaur) | High. Open source project management with conversational AI task execution. | Traditional PM surface plus AI task execution, modular self-hosted architecture, conversational task operations. |
| [TaskML](https://taskml.dev/) | High. Task markup language for AI workflows and handoffs. | Human-readable task format, portable task plans, AI-friendly handoff records. |
| [TaskView](https://taskview.tech/) | High. Self-hosted PM with Kanban, dependencies, Git sync, MCP, and RBAC. | AI-accessible project data, scoped API tokens, dependency graphs, permissions. |
| [Delega](https://delega.dev/) | High. Open task API for AI agents. | Agent-created tasks, delegation chains, API/MCP/CLI access, task infrastructure. |
| [Muneral](https://muneral.com/) | Medium-high. Task tracker for AI agent swarms. | Workspace -> project -> milestone -> sprint -> task -> subtask hierarchy. |
| [Agiflow](https://agiflow.io/) | Medium-high. Project management for AI-assisted work. | One board across agents, task-level sessions, decisions, file references. |
| [AlloraOS](https://alloraos.com/) | Medium. Open-source project management with AI action logs. | Board/list/timeline views, step-by-step AI action audit trail. |
| [Iqonga](https://iqonga.org/) | Medium. Multi-agent workflow framework with human approval and schedules. | Step routing, human approval, scheduled/webhook workflow runs. |

## Findings

TaskForge is closest to an AI-native project management control plane, not a coding-agent runtime. Its core value should be:

- turning goals and research into small tasks
- maintaining a board that humans and AI systems can both read
- preserving decisions, evidence, status, and audit logs
- keeping project state portable as files
- making workflows resumable and reviewable

The strongest neighboring systems suggest that TaskForge should focus on project/task primitives before runner execution details.

## Patterns To Apply

1. Project hierarchy

TaskForge should explicitly model or document:

- workspace
- project
- goal
- milestone
- sprint or cycle
- task
- subtask
- dependency
- evidence

2. AI-readable task packets

TaskML and Delega point toward a portable task packet that can be passed to any AI assistant or automation. TaskForge tasks should be serializable into a compact handoff format with context, constraints, DoD, dependencies, and expected evidence.

3. One board for humans and AI

Agiflow, TaskView, and Taskosaur all point to the same product need: the board is the source of truth, not chat history. TaskForge should keep `.team/board.json` as the primary state and make every automation write back status, decisions, and evidence.

4. Scoped access and auditability

TaskView and AlloraOS highlight permission boundaries and action logs. TaskForge should document scoped access rules for AI automations: allowed paths, allowed task states, protected fields, and append-only logs.

5. Research-to-task loop

TaskForge's automatic research should not merely summarize sources. It should convert framework lessons into backlog items with clear DoD and evidence.

## Recommended TaskForge Direction

Keep TaskForge file-first and framework-agnostic, but reposition the research goal around AI project management:

- Add a project/task management model document.
- Add a task packet or handoff format.
- Add dependency and milestone guidance to schemas.
- Add policies for AI-readable audit logs and scoped task access.
- Keep coding execution as one possible downstream workflow, not the defining purpose.

## Sources

- Taskosaur: https://github.com/Taskosaur/Taskosaur
- TaskML: https://taskml.dev/
- TaskView: https://taskview.tech/
- Delega: https://delega.dev/
- Muneral: https://muneral.com/
- Agiflow: https://agiflow.io/
- AlloraOS: https://alloraos.com/
- Iqonga: https://iqonga.org/
