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

views_json="$($GH_BIN api graphql -f query='query($owner:String!,$number:Int!){ user(login:$owner){ projectV2(number:$number){ views(first:30){ nodes{ name layout filter verticalGroupByFields(first:10){nodes{... on ProjectV2FieldCommon{name}}} sortByFields(first:10){nodes{direction field{... on ProjectV2FieldCommon{name}}}} } } } } }' -F owner="$OWNER" -F number="$PROJECT_NUMBER" 2>/dev/null || true)"

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

# Ask for follow-up until the 6 views have distinct configuration signatures.
# Signature = name-independent tuple of filter + vertical group + sort rules.
view_rows="$($GH_BIN api graphql -f query='query($owner:String!,$number:Int!){ user(login:$owner){ projectV2(number:$number){ views(first:30){ nodes{ name filter verticalGroupByFields(first:10){nodes{... on ProjectV2FieldCommon{name}}} sortByFields(first:10){nodes{direction field{... on ProjectV2FieldCommon{name}}}} } } } } }' -F owner="$OWNER" -F number="$PROJECT_NUMBER" --jq '.data.user.projectV2.views.nodes[] | [.name, (.filter // ""), ((.verticalGroupByFields.nodes // []) | map(.name) | join("+")), ((.sortByFields.nodes // []) | map(((.field.name // "") + ":" + (.direction // ""))) | join("+"))] | @tsv' 2>/dev/null || true)"

# Keep only required views
required_rows=""
while IFS=$'\t' read -r name filter vgroup sort; do
  [[ -z "${name:-}" ]] && continue
  for need in "${required_views[@]}"; do
    if [[ "$name" == "$need" ]]; then
      required_rows+="$name\t$filter\t$vgroup\t$sort\n"
      break
    fi
  done
done <<< "$view_rows"

required_count=$(printf '%b' "$required_rows" | sed '/^$/d' | wc -l | tr -d ' ')
sig_unique_count=$(printf '%b' "$required_rows" | sed '/^$/d' | awk -F'\t' '{print $2"|"$3"|"$4}' | sort -u | wc -l | tr -d ' ')

if [[ "$missing" -gt 0 ]]; then
  echo "[$(date '+%F %T')] REMINDER: project views incomplete; missing_count=$missing" >> "$LOG_FILE"
elif [[ "$required_count" -lt 6 ]]; then
  echo "[$(date '+%F %T')] REMINDER: unable to evaluate all required views; found=$required_count" >> "$LOG_FILE"
elif [[ "$sig_unique_count" -lt 6 ]]; then
  echo "[$(date '+%F %T')] REMINDER: view config not yet distinct; unique_signatures=$sig_unique_count/6" >> "$LOG_FILE"
fi

exit 0
