# TaskForge

TaskForge is a versioned automation system for turning a human goal into
small, reviewable engineering tasks and moving them through a guarded
Plan -> Build -> Review -> QA -> PR workflow.

It is intentionally separate from project runtime state. A target repository
keeps live data such as `board.json`, logs, scratch reports, locks, and daily
reports in its own gitignored `.team/` directory. TaskForge keeps the reusable
system definitions: prompts, schemas, policies, and docs.

## Layout

```text
prompts/
  team-planner.codex.md
  team-heartbeat.codex.md
  team-retro.codex.md
schemas/
  board.schema.json
  task.schema.json
docs/
  lifecycle.md
  planner-contract.md
examples/
  taskforge.config.json
```

## Runtime Boundary

Versioned in TaskForge:

- automation prompts
- board and task schemas
- lifecycle and branch metadata docs
- validation and migration scripts
- reusable examples

Runtime in the target repo:

- `.team/board.json`
- `.team/log/*.jsonl`
- `.team/daily/*.md`
- `.team/scratch/**`
- `.team/archive/*.jsonl`
- `.team/LOCK`
- `.team/PAUSE`
- project-specific goals and signals

## Target Repositories

Each target repository provides its own runtime config at:

```text
<target-repo>\.team\taskforge.config.json
```

TaskForge prompts read that config to resolve project-specific values such as
the project name, runtime directory, GitHub repository, base branch, allowed
implementation paths, and north star. The prompts in this repository should
not hardcode a target project.
