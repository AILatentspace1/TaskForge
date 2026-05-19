---
name: taskforge-status
description: Summarize current TaskForge board status — task counts by state, goal progress, blocked items, and active branches.
---

Read `.team/board.json` and output a concise status summary.

## Output Format

### Board Overview

| Metric | Value |
|--------|-------|
| Goals | {count} |
| Tasks | {count} total |
| Updated | {updated_at} |

### Tasks by State

| State | Count | Task IDs |
|-------|-------|----------|
| in-progress | N | T-XXXX, T-YYYY |
| blocked | N | T-XXXX |
| ... | ... | ... |

Only show states that have tasks.

### Blocked Tasks (if any)

For each blocked task, show: ID, title, blocked_by list, and next_action.

### Active Branches (if any)

Tasks with a non-null `branch_metadata.branch`:
- `T-XXXX` — title — branch name — PR status

### Stale Warnings

Flag tasks where `last_seen_at` is >7 days ago and state is not `closed` or `parked`.

## Rules

- Read only `.team/board.json`. No writes.
- Keep output under 40 lines.
- Skip empty sections entirely.
- Use Chinese for labels, English for IDs/paths.
