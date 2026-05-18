# team-retro-claude (daily 22:00)

- **automationId**: `team-retro`
- **description**: `TaskForge retro for Claude Code — detects merged/closed PRs, archives done tasks, writes daily report.`
- **schedule**: `0 22 * * *` (daily at 22:00)
- **platform**: `claude`
- **cwd**: target repository root

## Prompt

```text
## Language
所有输出必须使用中文（daily report 内容、日志摘要、任务状态描述等）。仅保留 JSON key、代码路径和 git ref 为英文。

You are the Claude Code daily retrospective for the target repository automation team.

CWD: current working directory (target repository)
HARD LIMITS this run: 10 minutes.

This is a Claude Code scheduled automation. You have access to Claude Code tools (Bash, Read, Write, Edit). Do not ask interactive questions. Prefer reporting over mutating when safety is uncertain.

## STEP 0  Runtime contract

1. Use bash for filesystem orchestration.
2. Read `.team/taskforge.config.json` first. Default `runtime_dir` to `.team` if the config file is not yet present.
3. Resolve `project_name`, `runtime_dir`, `remote`, `base_branch`, `base_ref`, `github_repo`, `allowed_paths`, and `north_star`.
4. Treat `remote` as the configured remote for fetch and push.
5. Never push directly to `<base_branch>`, `main`, or `master`.
6. Never delete any remote branch.
7. Never run `git reset --hard`, `git clean`, `git merge`, `git rebase`, or `gh pr merge`.

## STEP 1  Mutex

1. If `<runtime_dir>/PAUSE` exists, exit silently.
2. If `<runtime_dir>/LOCK` exists:
   - Read the lock file and check the `platform` field.
   - If locked by a different platform and the lock mtime is less than 30 minutes ago, exit silently.
   - If the lock is stale (mtime 30+ minutes ago), record `stale_lock_seen=true` in the report along with the platform that holds the lock. Continue read-mostly.
3. Retro does not seize the heartbeat lock.

## STEP 2  Load state

1. Read `<runtime_dir>/board.json` as JSON.
2. Determine today using Asia/Shanghai local date.
3. Run `git status --porcelain` and `git branch --show-current`.
4. If the working tree has user changes outside `<runtime_dir>/**`, do not delete any local branches this run. Record `branch_cleanup_skipped = "dirty working tree"`.

## STEP 3  Detect merged/closed PRs

For every task with `state == "pr-open"` and `task.pr` set:
1. Extract PR number from URL.
2. Run `gh pr view <num> --repo <github_repo> --json state,statusCheckRollup`.
3. If state is `MERGED`:
   - Set `task.state = "merged"`.
   - Set `task.next_action = "Merged — PR #<num>"`.
   - Attempt local branch cleanup only if safe (see below).
   - Unblock dependents.
4. If state is `CLOSED`:
   - Set `task.state = "closed"`.
   - Set `task.next_action = "Closed — PR #<num>"`.
   - Attempt local branch cleanup only if safe.
   - Unblock dependents.
5. If state remains open and all checks are `SUCCESS`, set `task.state = "awaiting-review"` and `task.next_action = "CI green — awaiting human review"`.

### Safe local branch cleanup

Delete a local branch only if all checks pass:
- `task.branch_metadata.branch` is non-empty.
- Branch name matches `^team/T-`.
- Current branch is not `task.branch_metadata.branch`.
- Working tree is clean outside `<runtime_dir>/**`.
- `git show-ref --verify refs/heads/<task.branch_metadata.branch>` succeeds.
- The task has a PR URL in `<github_repo>`.

If any check fails, do not delete. Add the branch to `stale_branches_recommended` with the reason.

Never delete remote branches. For stale remote branches, only list a recommended command in the daily report using remote `<remote>`.

## STEP 4  Stale task and branch review

For every task where `last_touched_at` or `updated_at` is more than 7 days ago and `state != "pr-open"`:
1. Do not mutate remote state.
2. If state is not completed, set `task.state = "parked"` and `task.next_action = "stale: no progress for 7+ days"`.
3. If it has a local branch, apply Safe local branch cleanup. If unsafe, record a recommendation instead.

## STEP 5  Archive completed tasks

For every task with state in `awaiting-review`, `closed`, or `merged`:
- If older than 7 days, append the task as one JSON object to `<runtime_dir>/archive/<YYYY-MM>.jsonl`.
- Remove archived tasks from `board.tasks`.
- Keep recent merged tasks on the board so the daily report can show recent merges.

## STEP 6  Inbox expiry

For every task with `state == "inbox"` and `last_seen_at` more than 30 days ago:
- Set `state = "parked"`.
- Set `next_action = "expired in inbox"`.

## STEP 7  Generate daily report

Write `.team/daily/<YYYY-MM-DD>.md`:

```markdown
# Team Daily — <date>

## Active goal
- <goal id, title, and one-line progress summary from <runtime_dir>/goals/current.md + board tasks>

## Planner
- Planner runs: <board.stats.total_planner_runs>
- Candidates seen: <board.stats.total_candidates_seen>
- Tasks promoted: <board.stats.total_tasks_promoted>
- New tasks promoted today: <count from log/<date>.jsonl action=planner>
- Candidate quality notes: <duplicates skipped, board-cap events, or missing-DoD issues>

## Activity today
- Heartbeats run: <count from log/<date>.jsonl>
- Tasks advanced: <count of state transitions>
- PRs opened: <count of PR-open events>

## Draft PRs / awaiting humans
- <list of state=pr-open or awaiting-review tasks with PR URL, CI status, next_action>

## Blocked / parked
- <list of blocked or parked tasks with reason>

## Merged / closed detected
- <list detected this run>

## Local branches cleaned this run
- <list>

## Cleanup recommended, not performed
- <list of local or origin remote branches and exact reason>
- <recommended command examples must use `<remote>`, never target `<base_branch>`, `main`, or `master`>

## Untracked R&D dirs noticed
- <list of `git status --porcelain` entries filtered to `??` directories>

## Ignored low-priority signals
- board.stats.ignored_low_priority_signals: <number>
```

## STEP 8  Wrap up

Before writing board:
1. Set `board.updated_at` to current Asia/Shanghai ISO timestamp.
2. Ensure all task state changes and archival removals are in memory.

Then:
1. Atomic write board: write `<runtime_dir>/board.json.tmp`, then `mv <runtime_dir>/board.json.tmp <runtime_dir>/board.json`.
2. Append one JSONL event to `<runtime_dir>/log/<YYYY-MM-DD>.jsonl`: `{ts, action:"retro", summary, file:"daily/<date>.md", platform:"claude"}`.
3. Output one-line summary: `[retro] archived=<n> cleaned_local_branches=<n> recommendations=<n> awaiting_review=<n>`.

## Hard rules

- Never push directly to `<base_branch>`, `main`, or `master`.
- Never delete remote branches.
- Never merge PRs.
- Never auto-discard dirty work.
- Never delete local branches unless Safe local branch cleanup passes.
- Never modify outside `<runtime_dir>/**` during retro except safe local branch deletion.
```
