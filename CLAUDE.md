# TaskForge Project

## TaskForge Scheduled Jobs

On session start, if `.claude/scheduled_tasks.json` exists, read it and display the automations table. Compute each job's next run time from its cron expression relative to the current time.

Use the mapping from prompt text to friendly name:
- `team-planner` → **Planner**
- `team-heartbeat` → **Heartbeat**
- `team-retro` → **Retro**

Display format:

```
## TaskForge Automations

| Job | Schedule | Next Run |
|-----|----------|----------|
| Planner | every 6h at :05 | 2026-05-18 18:05 |
| Heartbeat | every 2h at :15 | 2026-05-18 14:15 |
| Retro | daily 22:00 | 2026-05-18 22:00 |
```

Schedule column uses human-readable format:
- `5 */6 * * *` → `every 6h at :05`
- `15 */2 * * *` → `every 2h at :15`
- `0 22 * * *` → `daily 22:00`

Keep it minimal — table only, no extra explanation.
