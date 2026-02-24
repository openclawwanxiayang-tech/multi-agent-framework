#!/usr/bin/env bash
set -euo pipefail

WORKDIR="/home/lenovo/.openclaw/workspace"
RUN_LOG="$WORKDIR/docs/plans/2026-02-23-overnight-autonomous-run-log.md"
TODO_FILE="$WORKDIR/docs/plans/2026-02-23-overnight-todo.md"
ALERT_LOG="$WORKDIR/.logs/overnight-watchdog.alert.log"
mkdir -p "$WORKDIR/.logs"

now_epoch=$(date +%s)
alert() {
  echo "[$(TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M:%S %z')] $1" >> "$ALERT_LOG"
}

# 1) Run log freshness
last_runlog_epoch=$(grep -E 'AUTO_LOG|PROGRESS' "$RUN_LOG" 2>/dev/null | tail -n 1 | sed -E 's/^- ([0-9-]+) ([0-9:]+).*/\1 \2/' | xargs -I{} date -d '{} +0800' +%s 2>/dev/null || echo 0)
if (( now_epoch - last_runlog_epoch > 20*60 )); then
  alert "ALERT run log stale >20m"
fi

# 2) Commit freshness
last_commit_epoch=$(git -C "$WORKDIR" log -1 --format=%ct 2>/dev/null || echo 0)
if (( now_epoch - last_commit_epoch > 90*60 )); then
  alert "ALERT no new commit >90m"
fi

# 3) TODO update freshness
last_todo_epoch=$(grep -E '^- [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} GMT\+8: .*' "$TODO_FILE" 2>/dev/null | tail -n 1 | sed -E 's/^- ([0-9-]+) ([0-9:]+).*/\1 \2/' | xargs -I{} date -d '{} +0800' +%s 2>/dev/null || echo 0)
if (( now_epoch - last_todo_epoch > 30*60 )); then
  alert "ALERT TODO board stale >30m"
fi
