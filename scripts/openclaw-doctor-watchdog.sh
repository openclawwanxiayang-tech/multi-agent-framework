#!/usr/bin/env bash
set -u
LOG_DIR="/home/lenovo/.openclaw/workspace/artifacts/doctor"
LOG_FILE="$LOG_DIR/openclaw-doctor.log"
mkdir -p "$LOG_DIR"

log(){ printf '%s %s\n' "$(date '+%F %T')" "$*" >> "$LOG_FILE"; }

last_restart_epoch=0
cooldown_sec=90

while true; do
  now=$(date +%s)

  if ! openclaw gateway status >/dev/null 2>&1; then
    log "gateway down -> start"
    openclaw gateway start >/dev/null 2>&1 || log "gateway start failed"
    sleep 5
  fi

  deep="$(openclaw status --deep 2>/dev/null || true)"

  # Doctor heuristic: if Discord enabled but not OK, restart gateway (cooldown protected)
  if echo "$deep" | grep -q "Discord"; then
    if ! echo "$deep" | grep -qE "Discord\s+│\s+ON\s+│\s+OK"; then
      if (( now - last_restart_epoch >= cooldown_sec )); then
        log "discord not OK -> gateway restart"
        openclaw gateway restart >/dev/null 2>&1 || log "gateway restart failed"
        last_restart_epoch=$now
      else
        log "discord not OK but in cooldown"
      fi
    fi
  fi

  sleep 45
done
