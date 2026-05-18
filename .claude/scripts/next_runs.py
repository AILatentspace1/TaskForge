"""Compute TaskForge automations table for session-start display."""
import json
from datetime import datetime, timedelta
from pathlib import Path

TASKS_FILE = Path(__file__).resolve().parent.parent / "scheduled_tasks.json"
if not TASKS_FILE.exists():
    exit(0)

NAME_MAP = {
    "team-planner": ("Planner", "every 6h at :05"),
    "team-heartbeat": ("Heartbeat", "every 2h at :15"),
    "team-retro": ("Retro", "daily 22:00"),
}

CRON_HOURS = {
    "*/6": list(range(0, 24, 6)),
    "*/2": list(range(0, 24, 2)),
    "22": [22],
}


def next_run(minute: int, hours: list[int]) -> datetime:
    now = datetime.now().replace(second=0, microsecond=0)
    today = now.date()
    for h in sorted(hours):
        t = datetime(today.year, today.month, today.day, h, minute)
        if t > now:
            return t
    tomorrow = today + timedelta(days=1)
    return datetime(tomorrow.year, tomorrow.month, tomorrow.day, sorted(hours)[0], minute)


with open(TASKS_FILE) as f:
    data = json.load(f)

lines = [
    "IMPORTANT: Display the following TaskForge automations table to the user NOW. Do not skip this.",
    "",
    "## TaskForge Automations",
    "",
    "| Job | Schedule | Next Run |",
    "|-----|----------|----------|",
]

for task in data.get("tasks", []):
    prompt = task.get("prompt", "")
    cron = task.get("cron", "")
    for key, (name, schedule) in NAME_MAP.items():
        if key in prompt:
            parts = cron.split()
            minute = int(parts[0])
            hour_expr = parts[1]
            hours = CRON_HOURS[hour_expr] if hour_expr in CRON_HOURS else [int(hour_expr)]
            nr = next_run(minute, hours)
            lines.append(f"| {name} | {schedule} | {nr.strftime('%Y-%m-%d %H:%M')} |")
            break

print("\n".join(lines))
