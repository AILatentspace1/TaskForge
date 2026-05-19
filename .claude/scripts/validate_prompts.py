"""Validate TaskForge prompt files (.team/prompts/*.md and prompts/*.md) after edits."""

import re
import sys
from pathlib import Path

PROMPT_DIRS = [Path(".team/prompts"), Path("prompts")]

CLAUDE_HEADERS = ["automationId", "description", "schedule", "platform"]
CODEX_HEADERS = ["automationId", "description", "rrule"]
REQUIRED_SECTIONS = ["Prompt"]
STEP_PATTERN = re.compile(r"^##\s+STEP\s+([\d.]+)", re.MULTILINE)
VALID_STATES = {
    "inbox", "triaged", "planned", "in-progress", "review-ready",
    "qa-ready", "pr-ready", "pr-open", "awaiting-review", "merged",
    "closed", "blocked", "parked",
}

errors = 0
checked = 0


def check_file(filepath: Path):
    global errors, checked
    checked += 1
    name = filepath.name
    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()
    is_codex = "codex" in name

    # Check required header fields (different for claude vs codex)
    required = CODEX_HEADERS if is_codex else CLAUDE_HEADERS
    for header in required:
        pattern = re.compile(rf"^- \*\*{header}\*\*:")
        if not any(pattern.match(line) for line in lines[:20]):
            print(f"[ERROR] {name}: missing header '{header}'")
            errors += 1

    # Check ## Prompt section exists
    if not any(line.strip().startswith("## Prompt") for line in lines):
        print(f"[ERROR] {name}: missing '## Prompt' section")
        errors += 1

    # Check STEP numbering — allow sub-steps like 3.5, 4.5
    steps = STEP_PATTERN.findall(text)
    if steps:
        # Extract major step numbers only (ignore sub-steps like 3.5)
        major = sorted(set(int(s.split(".")[0]) for s in steps))
        expected = list(range(major[0], major[-1] + 1))
        if major != expected:
            print(f"[ERROR] {name}: STEP numbering gap — major steps {major}")
            errors += 1

    # Check platform matches filename (claude files only)
    if not is_codex:
        for line in lines[:20]:
            m = re.match(r"^- \*\*platform\*\*:\s*`?(\w+)`?", line)
            if m:
                platform = m.group(1)
                if "claude" in name and platform != "claude":
                    print(f"[ERROR] {name}: platform='{platform}' but filename suggests 'claude'")
                    errors += 1

    # Check referenced schemas exist
    for ref in re.findall(r"`?\.team/schemas/(\S+?)`?", text):
        if not Path(f".team/schemas/{ref}").exists():
            print(f"[ERROR] {name}: references non-existent schema '.team/schemas/{ref}'")
            errors += 1


def main():
    for d in PROMPT_DIRS:
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md")):
            if "codex" in f.name:
                continue
            check_file(f)

    if errors:
        print(f"[FAIL] {errors} issue(s) across {checked} prompt files")
        sys.exit(1)
    elif checked:
        print(f"[OK] {checked} prompt files valid")
    else:
        pass  # No prompt files found, silent exit


if __name__ == "__main__":
    main()
