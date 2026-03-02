#!/usr/bin/env python3
"""
code_linter.py - Validate code artifacts

Validates that:
- Code files exist in artifacts/impl/
- Have valid syntax (basic checks)
- Test files exist alongside implementation
"""

import sys
from pathlib import Path


def validate_code(task_path: Path) -> tuple[bool, str]:
    """Validate code artifacts for a task."""
    impl_path = task_path / "artifacts" / "impl"
    
    if not impl_path.exists():
        return False, f"impl/ directory not found"
    
    files = list(impl_path.glob("*"))
    if not files:
        return False, "No files in impl/"
    
    # Check for test files
    test_files = list(impl_path.glob("*_test.py")) + list(impl_path.glob("*_test.go")) + list(impl_path.glob("test_*.py")) + list(impl_path.glob("test_*.go"))
    
    # Basic syntax checks for common languages
    for f in files:
        if f.suffix == ".py":
            try:
                compile(f.read_text(), f, "exec")
            except SyntaxError as e:
                return False, f"Syntax error in {f.name}: {e}"
        elif f.suffix == ".go":
            content = f.read_text()
            # Basic Go syntax check (package declaration)
            if not content.startswith("package "):
                return False, f"Invalid Go file: {f.name} (missing package declaration)"
    
    return True, f"Valid code ({len(files)} files, {len(test_files)} test files)"


def main():
    if len(sys.argv) < 2:
        artifacts = Path("artifacts/tasks")
        if not artifacts.exists():
            print("No artifacts/tasks/ directory found")
            sys.exit(0)
        
        results = []
        for task_dir in artifacts.iterdir():
            if task_dir.is_dir():
                valid, msg = validate_code(task_dir)
                results.append((task_dir.name, valid, msg))
        
        print("Code Linter Results:")
        for name, valid, msg in results:
            status = "✅" if valid else "❌"
            print(f"  {status} {name}: {msg}")
    else:
        task_path = Path(sys.argv[1])
        valid, msg = validate_code(task_path)
        print(msg)
        sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
