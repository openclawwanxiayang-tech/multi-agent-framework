#!/usr/bin/env bash
set -euo pipefail

WORKDIR="/home/lenovo/.openclaw/workspace"
OUT_DIR="$WORKDIR/artifacts/overnight"
RUN_LOG="$WORKDIR/docs/plans/2026-02-23-overnight-autonomous-run-log.md"
TODO_FILE="$WORKDIR/docs/plans/2026-02-23-overnight-todo.md"
mkdir -p "$OUT_DIR"

ts_file=$(TZ=Asia/Shanghai date '+%Y%m%d-%H%M%S')
ts_human=$(TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M:%S GMT+8')
out="$OUT_DIR/${ts_file}-cycle.md"

issue_count="unknown"
issue_lines="gh unavailable or unauthenticated"
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  issue_count=$(gh issue list --repo openclawwanxiayang-tech/multi-agent-framework --state open --limit 200 --json number --jq 'length' 2>/dev/null || echo unknown)
  issue_lines=$(gh issue list --repo openclawwanxiayang-tech/multi-agent-framework --state open --limit 10 2>/dev/null || true)
  [[ -z "$issue_lines" ]] && issue_lines="(no open issues fetched)"
fi

todo_counts=$(grep -E '^\d+\. \[(todo|in_progress|done|blocked)\]' "$TODO_FILE" 2>/dev/null | sed -E 's/^.*\[(.*)\].*$/\1/' | sort | uniq -c | xargs || true)
[[ -z "$todo_counts" ]] && todo_counts="unavailable"

last_commit=$(git -C "$WORKDIR" rev-parse --short HEAD 2>/dev/null || echo none)
branch=$(git -C "$WORKDIR" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)

cat > "$out" <<EOF
# Overnight Work Cycle Snapshot

- Time: $ts_human
- Branch: $branch
- Last commit: $last_commit
- Open issues: $issue_count
- TODO status counts: $todo_counts

## Open issue sample

\`\`\`
$issue_lines
\`\`\`

## Notes
- Automated cycle snapshot generated.
- Use this artifact for morning handoff and progress audit.
EOF

echo "- $ts_human: PROGRESS | task=work_cycle_snapshot | artifact=${out#$WORKDIR/} | open_issues=$issue_count" >> "$RUN_LOG"
