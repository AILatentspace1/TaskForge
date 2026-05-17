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

## Applying TaskForge To A Project

TaskForge is installed once as a reusable system repository, then each target
project gets its own runtime `.team/` directory and Codex automations.

Assume:

```text
TaskForge repo: E:\workspace\TaskForge
Target repo:    E:\workspace\my-project
```

### 1. Create The Runtime Directory

In the target repo:

```powershell
New-Item -ItemType Directory -Force -Path .team\goals,.team\log,.team\daily,.team\scratch,.team\archive,.team\planner,.team\policies
```

Keep runtime state out of the target repo's git history:

```gitignore
.team/
```

### 2. Add `taskforge.config.json`

Create:

```text
<target-repo>\.team\taskforge.config.json
```

Example:

```json
{
  "version": 1,
  "system_name": "TaskForge",
  "system_repo": "E:\\workspace\\TaskForge",
  "prompt_source": "E:\\workspace\\TaskForge\\prompts",
  "runtime_dir": "E:\\workspace\\my-project\\.team",
  "target_repo": "E:\\workspace\\my-project",
  "project_name": "my-project",
  "remote": "origin",
  "base_branch": "main",
  "github_repo": "owner/my-project",
  "north_star": "Improve the scoped project area with small, reviewable, locally verifiable changes.",
  "allowed_paths": [
    "src/**",
    "docs/**",
    "tests/**"
  ],
  "runtime_state_gitignored": true
}
```

Important fields:

- `prompt_source`: where Codex automations read TaskForge prompts from.
- `runtime_dir`: where board/log/scratch state lives in the target repo.
- `github_repo`: GitHub `owner/repo` used for PR commands.
- `remote`: git remote used for branches, usually `origin`.
- `base_branch`: PR base branch, usually `main`.
- `north_star`: durable mission the automation must stay inside.
- `allowed_paths`: implementation paths heartbeat is allowed to edit.

### 3. Add The Current Goal

Create:

```text
<target-repo>\.team\goals\current.md
```

Template:

```markdown
# Goal: <project-area> Continuous Improvement

## North Star

Improve <specific project area> using small, reviewable, locally verifiable
changes.

## Success Criteria

- New tasks stay inside the configured scope.
- Every task is a small PR-sized slice.
- Every task has objective DoD checks.
- Draft PRs include DoD, review, and QA/eval evidence.

## Scope

Allowed:
- `src/**`
- `docs/**`
- `tests/**`
- `.team/**`

Not allowed:
- Changes outside the configured project area.
- Repo-wide refactors unless explicitly part of the goal.
- Direct pushes to the base branch.
- Remote branch deletion.

## Task Generation Hints

- Prefer deterministic local verification.
- Prefer evals, docs, reliability, and workflow improvements.
- Avoid unknown credentials, paid services, and long-running external systems.
```

### 4. Register The Three Automations

Create three Codex cron automations with the target repo as `cwd`.

Recommended schedules:

| Automation | Schedule | Prompt |
|---|---:|---|
| `team-planner` | every 6 hours at minute 5 | `prompts/team-planner.codex.md` |
| `team-heartbeat` | every 2 hours at minute 15 | `prompts/team-heartbeat.codex.md` |
| `team-retro` | daily 22:00 | `prompts/team-retro.codex.md` |

Each automation prompt should be the full fenced text under `## Prompt` from
the matching TaskForge prompt file. Set the automation `cwd` to the target repo
root, for example:

```text
E:\workspace\my-project
```

### 5. First Run Expectations

Planner:

- Reads `.team/goals/current.md`.
- Creates or updates `.team/board.json`.
- Adds small task candidates only when they fit the goal.

Heartbeat:

- Selects one board task.
- Advances it through plan/build/review/QA/PR states.
- Only edits `allowed_paths` and runtime state under `.team/`.

Retro:

- Detects merged/closed PRs.
- Archives old completed tasks.
- Writes `.team/daily/<date>.md`.
- Recommends cleanup without deleting remote branches.

### 6. Pausing

Create:

```text
<target-repo>\.team\PAUSE
```

Delete it to resume.

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
