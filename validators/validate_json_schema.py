#!/usr/bin/env python3
"""Validate core JSON files against docs/schemas/*.json using jsonschema if available."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "artifacts" / "tasks"
SCHEMAS = ROOT / "docs" / "schemas"


try:
    import jsonschema  # type: ignore
except Exception:  # pragma: no cover
    print("jsonschema not installed; skipping schema validation")
    sys.exit(0)


def load(name: str) -> dict:
    return json.loads((SCHEMAS / f"{name}.json").read_text(encoding="utf-8"))


def main() -> int:
    mapping = {
        "task.json": load("task"),
        "state.json": load("state"),
        ".lock": load("lock"),
    }
    event_schema = load("event")

    failed = 0
    for task_dir in TASKS.glob("*"):
        if not task_dir.is_dir():
            continue
        for file_name, schema in mapping.items():
            p = task_dir / file_name
            if not p.exists():
                continue
            try:
                obj = json.loads(p.read_text(encoding="utf-8"))
                jsonschema.validate(instance=obj, schema=schema)
            except Exception as e:
                failed += 1
                print(f"❌ {p}: {e}")

        events_path = task_dir / "logs" / "events.ndjson"
        if events_path.exists():
            for i, line in enumerate(events_path.read_text(encoding="utf-8").splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                    jsonschema.validate(instance=obj, schema=event_schema)
                except Exception as e:
                    failed += 1
                    print(f"❌ {events_path}:{i}: {e}")

    if failed:
        return 1
    print("✅ JSON schema validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
