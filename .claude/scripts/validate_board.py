"""Validate .team/board.json against TaskForge schemas after edits."""

import json
import sys
from pathlib import Path

BOARD = Path(".team/board.json")
BOARD_SCHEMA = Path(".team/schemas/board.schema.json")
TASK_SCHEMA = Path(".team/schemas/task.schema.json")


def main():
    if not BOARD.exists():
        sys.exit(0)

    try:
        import jsonschema
    except ImportError:
        # Fallback: just check valid JSON
        try:
            json.loads(BOARD.read_text(encoding="utf-8"))
            print("[OK] board.json: valid JSON (jsonschema not installed, skipping schema check)")
        except json.JSONDecodeError as e:
            print(f"[ERROR] board.json: invalid JSON — {e}")
            sys.exit(1)
        sys.exit(0)

    if not BOARD_SCHEMA.exists():
        sys.exit(0)

    try:
        board_data = json.loads(BOARD.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[ERROR] board.json: invalid JSON — {e}")
        sys.exit(1)

    schema_store = {}
    if TASK_SCHEMA.exists():
        schema_store[TASK_SCHEMA.resolve().as_uri()] = json.loads(
            TASK_SCHEMA.read_text(encoding="utf-8")
        )

    schema = json.loads(BOARD_SCHEMA.read_text(encoding="utf-8"))
    resolver = jsonschema.RefResolver(
        base_uri=BOARD_SCHEMA.resolve().as_uri(),
        referrer=schema,
        store=schema_store,
    )

    try:
        jsonschema.validate(board_data, schema, resolver=resolver)
        task_count = len(board_data.get("tasks", []))
        print(f"[OK] board.json: valid (v{board_data.get('version', '?')}, {task_count} tasks)")
    except jsonschema.ValidationError as e:
        path = ".".join(str(p) for p in e.absolute_path) or "(root)"
        print(f"[ERROR] board.json schema violation at {path}: {e.message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
