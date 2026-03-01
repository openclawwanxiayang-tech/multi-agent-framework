#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/artifacts/status/project-progress.md"
REPO="openclawwanxiayang-tech/multi-agent-framework"

branch="$(git -C "$ROOT" branch --show-current)"
commit="$(git -C "$ROOT" rev-parse --short HEAD)"
remote="$(git -C "$ROOT" remote get-url origin)"
state="clean"
[[ -n "$(git -C "$ROOT" status --short)" ]] && state="dirty"

open_issues="$(gh issue list --repo "$REPO" --state open --limit 100 --json number --template '{{len .}}' 2>/dev/null || echo unknown)"
open_prs="$(gh pr list --repo "$REPO" --state open --limit 100 --json number --template '{{len .}}' 2>/dev/null || echo unknown)"

{
  echo "# Project Progress Status"
  echo
  echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo
  echo "## Repository"
  echo "- Remote: $remote"
  echo "- Branch: $branch"
  echo "- Commit: $commit"
  echo "- Working tree: $state"
  echo
  echo "## GitHub"
  echo "- Open issues: $open_issues"
  echo "- Open PRs: $open_prs"
  echo
  echo "## Key Docs"
  for f in docs/tasks.md docs/mvp-scope.md docs/architecture-v2.md docs/repo-scope.md; do
    if [[ -f "$ROOT/$f" ]]; then
      echo "- $f"
    fi
  done
} > "$OUT"

echo "wrote $OUT"
