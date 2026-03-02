#!/usr/bin/env python3
"""qa_checker.py - Validate QA test results."""

import sys
from pathlib import Path


def validate_qa(task_path: Path) -> tuple[bool, str]:
    qa_path = task_path / "artifacts" / "qa" / "results.md"
    if not qa_path.exists():
        return False, f"results.md not found at {qa_path}"

    content = qa_path.read_text(encoding="utf-8").lower()
    required_checks = ["spec_validator", "design_validator", "code", "test", "pass", "fail", "evidence"]
    missing = [c for c in required_checks if c not in content]
    if missing:
        return False, f"Missing validation checks: {', '.join(missing)}"

    check_count = content.count("✅") + content.count("pass")
    return True, f"Valid QA results ({check_count} positive indicators)"


def main():
    if len(sys.argv) < 2:
        artifacts = Path("artifacts/tasks")
        if not artifacts.exists():
            print("No artifacts/tasks/ directory found")
            sys.exit(0)

        results = []
        for task_dir in artifacts.iterdir():
            if task_dir.is_dir():
                valid, msg = validate_qa(task_dir)
                results.append((task_dir.name, valid, msg))

        print("QA Checker Results:")
        any_failed = False
        for name, valid, msg in results:
            status = "✅" if valid else "❌"
            print(f"  {status} {name}: {msg}")
            any_failed = any_failed or (not valid)
        sys.exit(1 if any_failed else 0)
    else:
        task_path = Path(sys.argv[1])
        valid, msg = validate_qa(task_path)
        print(msg)
        sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
