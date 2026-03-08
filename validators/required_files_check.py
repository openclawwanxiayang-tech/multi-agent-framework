#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "artifacts" / "tasks"

REQUIRED = [
    "task.json",
    "state.json",
    "logs/events.ndjson",
    "artifacts/spec/spec.md",
    "artifacts/design/design.md",
    "artifacts/impl/main.go",
    "artifacts/qa/results.md",
]


def main() -> int:
    failures = 0
    for task_dir in TASKS.glob("*"):
        if not task_dir.is_dir():
            continue
        for rel in REQUIRED:
            p = task_dir / rel
            if not p.exists():
                print(f"❌ Missing: {task_dir.name}/{rel}")
                failures += 1
    if failures:
        return 1
    print("✅ Required files present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
