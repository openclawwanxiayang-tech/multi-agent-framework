#!/usr/bin/env bash
set -u

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH"

WORKDIR="/home/lenovo/.openclaw/workspace"
LOG_FILE="$WORKDIR/docs/plans/2026-02-23-overnight-autonomous-run-log.md"
STATE_FILE="$WORKDIR/.overnight_status.txt"

mkdir -p "$(dirname "$LOG_FILE")"

now_cn() {
  TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M:%S GMT+8'
}

status="working"
if [[ -f "$STATE_FILE" ]]; then
  status="$(cat "$STATE_FILE" | tr -d '\n' || true)"
  [[ -z "$status" ]] && status="working"
fi

last_commit="none"
if git -C "$WORKDIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  last_commit="$(git -C "$WORKDIR" rev-parse --short HEAD 2>/dev/null || echo none)"
fi

open_issues="unknown"
if command -v gh >/dev/null 2>&1; then
  open_issues="$(gh issue list --repo openclawwanxiayang-tech/multi-agent-framework --state open --limit 100 2>/dev/null | wc -l | tr -d ' ')"
fi

{
  echo "- $(now_cn): AUTO_LOG | status=$status | last_commit=$last_commit | open_issues=$open_issues"
} >> "$LOG_FILE"
