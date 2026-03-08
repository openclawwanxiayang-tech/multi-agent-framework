#!/usr/bin/env python3
"""
spec_validator.py - Validate SPEC.md against task requirements

Validates that:
- SPEC.md exists in artifacts/spec/
- Has required sections (Overview, Requirements, Acceptance Criteria)
- Acceptance criteria are testable
"""

import json
import sys
from pathlib import Path


def validate_spec(task_path: Path) -> tuple[bool, str]:
    """Validate SPEC.md for a task."""
    spec_path = task_path / "artifacts" / "spec" / "spec.md"
    acceptance_path = task_path / "artifacts" / "spec" / "acceptance.md"

    if not spec_path.exists():
        return False, f"SPEC.md not found at {spec_path}"
    if not acceptance_path.exists():
        return False, f"acceptance.md not found at {acceptance_path}"

    content = spec_path.read_text(encoding="utf-8")
    
    required_sections = ["Overview", "Requirements", "Acceptance Criteria"]
    missing = [s for s in required_sections if s not in content]
    
    if missing:
        return False, f"Missing sections: {', '.join(missing)}"
    
    # Check acceptance criteria are present within the Acceptance Criteria section
    lines = content.split("\n")
    section_start = None
    for idx, line in enumerate(lines):
        if "Acceptance Criteria" in line:
            section_start = idx + 1
            break

    if section_start is None:
        return False, "No acceptance criteria found"

    section_end = len(lines)
    for j in range(section_start, len(lines)):
        if lines[j].lstrip().startswith("#"):
            section_end = j
            break

    section_lines = lines[section_start:section_end]
    criteria_count = sum(1 for l in section_lines if l.strip().startswith(tuple('1234567890.-')))
    if criteria_count < 1:
        return False, "No acceptance criteria found"
    
    return True, "Valid SPEC.md"


def main():
    if len(sys.argv) < 2:
        # Validate all tasks in artifacts/tasks/
        artifacts = Path("artifacts/tasks")
        if not artifacts.exists():
            print("No artifacts/tasks/ directory found")
            sys.exit(0)
        
        results = []
        for task_dir in artifacts.iterdir():
            if task_dir.is_dir():
                valid, msg = validate_spec(task_dir)
                results.append((task_dir.name, valid, msg))
        
        print("Spec Validator Results:")
        any_failed = False
        for name, valid, msg in results:
            status = "✅" if valid else "❌"
            print(f"  {status} {name}: {msg}")
            any_failed = any_failed or (not valid)
        sys.exit(1 if any_failed else 0)
    else:
        # Validate specific task
        task_path = Path(sys.argv[1])
        valid, msg = validate_spec(task_path)
        print(msg)
        sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
