#!/usr/bin/env bash
set -euo pipefail

WORKDIR="/home/lenovo/.openclaw/workspace"
ENV_FILE="$WORKDIR/config/overnight-runner.env"
RUN_LOG="$WORKDIR/docs/plans/2026-02-23-overnight-autonomous-run-log.md"
TODO_FILE="$WORKDIR/docs/plans/2026-02-23-overnight-todo.md"
CHECK_LOG="$WORKDIR/.logs/overnight-checkpoint.log"
mkdir -p "$WORKDIR/.logs"

[[ -f "$ENV_FILE" ]] && source "$ENV_FILE"
: "${PUSH_POLICY:=checks_pass}"
: "${ON_CHECK_FAIL:=commit_wip_no_push}"
: "${BRANCH:=fix/mvp-surface-area}"
: "${REMOTE:=origin}"
: "${WORK_CYCLE_CMD:=}"

now() { TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M:%S GMT+8'; }
append_runlog() { echo "- $(now): PROGRESS | $1" >> "$RUN_LOG"; }

ensure_todo_update_log() {
  if ! grep -q '^## Update Log$' "$TODO_FILE" 2>/dev/null; then
    {
      echo
      echo "## Update Log"
      echo "- $(now): INIT | update log enabled for heartbeat freshness checks."
    } >> "$TODO_FILE"
  fi
}

append_todo_update() {
  ensure_todo_update_log
  echo "- $(now): CHECKPOINT | automated checkpoint executed." >> "$TODO_FILE"
}

run_checks() {
  local ok=0
  local ran=0

  if [[ -f "$WORKDIR/package.json" ]]; then
    ran=1
    if npm run -s lint >> "$CHECK_LOG" 2>&1 && npm test --silent >> "$CHECK_LOG" 2>&1; then
      ok=1
    else
      ok=2
    fi
  elif compgen -G "$WORKDIR/requirements*.txt" > /dev/null || compgen -G "$WORKDIR/pyproject.toml" > /dev/null; then
    ran=1
    if command -v pytest >/dev/null 2>&1 && pytest -q >> "$CHECK_LOG" 2>&1; then
      ok=1
    else
      ok=2
    fi
  else
    ok=1
  fi

  echo "$ok:$ran"
}

cd "$WORKDIR"
append_todo_update
append_runlog "task=checkpoint_start | branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"

if [[ -n "$WORK_CYCLE_CMD" ]]; then
  bash -lc "$WORK_CYCLE_CMD" >> "$CHECK_LOG" 2>&1 || true
  append_runlog "task=work_cycle | status=ran | cmd=$(printf '%q' "$WORK_CYCLE_CMD")"
fi

checks_result="$(run_checks)"
checks_code="${checks_result%%:*}"

if ! git diff --quiet || ! git diff --cached --quiet; then
  git add -A
  if [[ "$checks_code" == "1" ]]; then
    git commit -m "ops: overnight checkpoint $(TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M')" >> "$CHECK_LOG" 2>&1 || true
    append_runlog "task=checkpoint_commit | checks=pass"
    if [[ "$PUSH_POLICY" == "checks_pass" ]]; then
      git push "$REMOTE" "$BRANCH" >> "$CHECK_LOG" 2>&1 || append_runlog "task=checkpoint_push | checks=pass | status=failed"
      append_runlog "task=checkpoint_push | checks=pass | status=attempted"
    fi
  else
    if [[ "$ON_CHECK_FAIL" == "commit_wip_no_push" ]]; then
      git commit -m "wip: overnight checkpoint failed-checks $(TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M')" >> "$CHECK_LOG" 2>&1 || true
      append_runlog "task=checkpoint_commit | checks=fail | policy=commit_wip_no_push"
    else
      append_runlog "task=checkpoint_skip_commit | checks=fail"
    fi
  fi
else
  append_runlog "task=checkpoint_no_changes"
fi

append_runlog "task=checkpoint_end"
