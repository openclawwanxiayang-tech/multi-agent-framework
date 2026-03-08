#!/usr/bin/env python3
"""
design_validator.py - Validate DESIGN.md against SPEC.md

Validates that:
- DESIGN.md exists in artifacts/design/
- Has required sections (Architecture, Implementation)
- Covers requirements from SPEC.md
"""

import sys
from pathlib import Path


def validate_design(task_path: Path) -> tuple[bool, str]:
    """Validate DESIGN.md for a task."""
    design_path = task_path / "artifacts" / "design" / "design.md"
    
    if not design_path.exists():
        return False, f"design.md not found at {design_path}"
    
    content = design_path.read_text()
    
    required_sections = ["Architecture", "Implementation", "Error", "Test"]
    missing = [s for s in required_sections if s not in content]
    
    if missing:
        return False, f"Missing sections: {', '.join(missing)}"
    
    return True, "Valid design.md"


def main():
    if len(sys.argv) < 2:
        artifacts = Path("artifacts/tasks")
        if not artifacts.exists():
            print("No artifacts/tasks/ directory found")
            sys.exit(0)
        
        results = []
        for task_dir in artifacts.iterdir():
            if task_dir.is_dir():
                valid, msg = validate_design(task_dir)
                results.append((task_dir.name, valid, msg))
        
        print("Design Validator Results:")
        any_failed = False
        for name, valid, msg in results:
            status = "✅" if valid else "❌"
            print(f"  {status} {name}: {msg}")
            any_failed = any_failed or (not valid)
        sys.exit(1 if any_failed else 0)
    else:
        task_path = Path(sys.argv[1])
        valid, msg = validate_design(task_path)
        print(msg)
        sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
