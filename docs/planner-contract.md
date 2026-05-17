# Planner Contract

`team-planner` turns human goals into board tasks. It is deliberately separate from `team-heartbeat`.

## Responsibilities

- Read `<runtime_dir>/goals/current.md`.
- Read `<runtime_dir>/board.json`, creating it if missing.
- Read recent `<runtime_dir>/daily/*.md`, `<runtime_dir>/log/*.jsonl`, `<runtime_dir>/archive/*.jsonl`, and useful gstack artifacts under `~/.gstack/projects/<slug>/`.
- Generate small, objective, PR-sized tasks.
- Deduplicate against active tasks, archived tasks, and prior candidates.
- Append candidates to `<runtime_dir>/planner/candidates.jsonl`.
- Promote only high-confidence candidates into `board.tasks[]` as `state: "inbox"`.

## Non-Responsibilities

- Do not modify configured implementation paths.
- Do not create branches.
- Do not commit.
- Do not push.
- Do not open PRs.
- Do not delete branches.

## Task Quality Bar

Each promoted task must have:

- `id`
- `title`
- `goal_id`
- `skill`
- `state: "inbox"`
- `source: "goal:<goal-file>"`
- `fingerprint`
- `priority`
- `why`
- `dod` with at least 3 objective checks
- `quality_gates.review`
- `quality_gates.qa`
- `branch_metadata` initialized for heartbeat to fill in
- `next_action`

## Branch Metadata

Planner initializes branch metadata, but does not create or inspect branches.
Heartbeat owns keeping these fields current as work moves through Build,
Review, QA, and PR creation.

Default metadata for a new task:

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

## Fingerprint

Use a stable hash of:

```text
goal_id + skill + normalized_title + key_files + dod ids
```

Skip a candidate when its fingerprint appears in:

- active `board.tasks[]`
- `<runtime_dir>/archive/*.jsonl`
- `<runtime_dir>/planner/candidates.jsonl`

## Board Cap

If active non-terminal tasks are 10 or more, do not promote new tasks. Record candidates only.

Terminal states:

- `merged`
- `closed`
- `parked`
- `blocked`
