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
