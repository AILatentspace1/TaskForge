# TaskForge Lifecycle

TaskForge moves work through one small task at a time.

```text
goal -> planner -> board inbox -> triage -> plan -> build -> review -> qa -> draft PR -> human review -> merge/close -> retro
```

## Roles

- Planner: turns the current human goal into small PR-sized tasks.
- Heartbeat: advances one selected task per run.
- Reviewer: checks scope drift, plan completion, structural bugs, and test gaps.
- QA: verifies objective DoD and captures evidence.
- Retro: archives completed work, reports progress, and recommends cleanup.

## Task States

- `inbox`: candidate task accepted onto the board.
- `triaged`: task has been checked against the current goal and DoD quality.
- `planned`: implementation plan exists.
- `in-progress`: implementation has started.
- `review-ready`: ready for gstack-style review gate.
- `qa-ready`: ready for QA/eval gate.
- `pr-ready`: all gates passed and draft PR can be created or updated.
- `pr-open`: draft PR exists.
- `awaiting-review`: CI is green and human review is needed.
- `merged`: PR was merged.
- `closed`: PR was closed without merge.
- `blocked`: automation cannot proceed without human input.
- `parked`: stale or low-confidence work removed from the active lane.

## Branch Metadata

Branch ownership lives under `task.branch_metadata`, not as a top-level task
field. The current shape is:

```json
{
  "base_remote": "origin",
  "base_branch": "main",
  "branch": null,
  "merge_base": null,
  "base_sha": null,
  "head_sha": null,
  "last_commit_sha": null,
  "last_pushed_sha": null,
  "pr_head_sha": null,
  "updated_at": null
}
```

The board stores facts. The automation decides how to use the configured git
remote in the target repository.

## Platform Support

TaskForge supports two automation platforms:

- **Codex** (Windows): uses PowerShell, scheduled via Codex cron.
- **Claude Code** (macOS/Linux): uses bash/zsh, scheduled via `CronCreate`.

Both platforms operate on the same runtime state (`board.json`, logs, scratch)
and can run concurrently on the same project.

### Platform Fields

Each task carries platform fields at the root level:

- `created_by_platform`: which platform created the task (`"codex"` or `"claude"`).
- `last_platform`: which platform last modified the task.

These fields are separate from `branch_metadata` which tracks git branch state.

### Concurrent Operation

Lock files include a `platform` field and `hostname`:

```json
{
  "pid": 12345,
  "started_at": "2026-05-17T12:00:00Z",
  "automation": "team-heartbeat",
  "platform": "claude",
  "hostname": "my-machine"
}
```

When an automation finds a lock from a different platform that is less than 60
minutes old, it exits silently to avoid conflicts. Stale locks (older than 60
minutes) are overwritten regardless of platform.

Log entries in `log/*.jsonl` also include a `platform` field for audit tracing.
