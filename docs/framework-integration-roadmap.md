# Framework Integration Roadmap

TaskForge should borrow architecture patterns from AI project and task
management frameworks without becoming only a coding-agent orchestrator.

## Phase 1: Clarify The Project Management Model

- Document workspace, project, goal, milestone, cycle, task, subtask, dependency, evidence, and audit-log concepts.
- Decide which concepts are schema fields now and which remain conventions.
- Add sample board fixtures for a research project and an implementation project.
- Define how planner, heartbeat, and retro use project-management fields.

## Phase 2: Define AI Task Packets

Create a portable task handoff format with these stable fields:

- Goal and project context.
- Task intent, constraints, dependencies, and blocked-by fields.
- DoD and expected evidence.
- Human approval requirements.
- Links to scratch files, decisions, and logs.

This keeps TaskForge useful with Codex, Claude, ChatGPT, local agents, MCP
tools, or humans without baking in one automation runtime.

## Phase 3: Add Board Governance

- Add scoped access rules for which actors can edit which task fields.
- Add dependency and stale-task policies.
- Add audit-log requirements for AI-made task changes.
- Add a daily retro format that reports project progress, not just PR status.

## Phase 4: Add Integration Surfaces

TaskForge should expose project state through file formats first:

- `.team/board.json`
- `.team/goals/current.md`
- `.team/planner/candidates.jsonl`
- `.team/log/*.jsonl`
- `.team/scratch/<task-id>/`

Later integration options can include MCP, CLI commands, GitHub issue sync, or
Kanban views. These should read and write the same board contract.

## Phase 5: Keep Execution Optional

TaskForge can coordinate coding agents, but that is a downstream use case.
The core framework should first be excellent at goal intake, task breakdown,
dependency tracking, evidence capture, review, QA, and retrospection.
