#!/usr/bin/env bash
set -euo pipefail

# Watchdog for Project 3 view completeness/config follow-up.
# Silent on success unless still incomplete.

OWNER="WanxiaJaneYang"
PROJECT_NUMBER="3"
WORKDIR="/home/lenovo/.openclaw/workspace"
LOG_DIR="$WORKDIR/logs"
LOG_FILE="$LOG_DIR/project-board-watchdog.log"
mkdir -p "$LOG_DIR"

required_views=(
  "Localization Track"
  "Now"
  "Foundation Gate"
  "DataPack Pipeline"
  "Quality"
  "Backlog"
)

GH_BIN="${GH_BIN:-}"
if [[ -z "$GH_BIN" ]]; then
  GH_BIN="$(command -v gh 2>/dev/null || true)"
fi
if [[ -z "$GH_BIN" && -x "/home/linuxbrew/.linuxbrew/bin/gh" ]]; then
  GH_BIN="/home/linuxbrew/.linuxbrew/bin/gh"
fi
if [[ -z "$GH_BIN" ]]; then
  echo "[$(date '+%F %T')] ERROR: gh not found" >> "$LOG_FILE"
  exit 0
fi

views_json="$($GH_BIN api graphql -f query='query($owner:String!,$number:Int!){ user(login:$owner){ projectV2(number:$number){ views(first:30){ nodes{ name } } } } }' -F owner="$OWNER" -F number="$PROJECT_NUMBER" 2>/dev/null || true)"

if [[ -z "$views_json" ]]; then
  echo "[$(date '+%F %T')] WARN: unable to read project views" >> "$LOG_FILE"
  exit 0
fi

missing=0
for v in "${required_views[@]}"; do
  if ! printf '%s' "$views_json" | grep -Fq "\"name\":\"$v\""; then
    missing=$((missing+1))
  fi
done

if [[ "$missing" -gt 0 ]]; then
  echo "[$(date '+%F %T')] REMINDER: project views incomplete; missing_count=$missing" >> "$LOG_FILE"
fi

exit 0
