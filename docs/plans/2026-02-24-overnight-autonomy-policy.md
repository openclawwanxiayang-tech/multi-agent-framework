# Overnight Autonomy Policy (2026-02-24)

## Selected operating mode
- Mode: **Full autonomous**
- Push policy: **Push only when checks pass**
- Checkpoint cadence: **Every 30 minutes**
- On check failure: **Continue working; commit WIP with failed-checks tag; no push**

## Why previous run failed
- Only heartbeat/logging automation existed.
- No autonomous execution loop or scheduled OpenClaw cron job.
- Logger created apparent activity without real delivery progress.

## New controls
1. `scripts/overnight_checkpoint.sh`
   - Appends timestamped TODO updates.
   - Runs optional work-cycle command.
   - Runs checks when available.
   - Commits checkpoint; pushes only when checks pass.
2. `scripts/overnight_watchdog.sh`
   - Alerts on stale run-log / stale commit / stale TODO board.
3. `config/overnight-runner.env`
   - Central policy config.

## Required scheduling (applied to system crontab)
- `*/15 * * * * scripts/push_progress_log.sh`
- `*/30 * * * * scripts/overnight_checkpoint.sh`
- `*/10 * * * * scripts/overnight_watchdog.sh`

## Notes
- Set `WORK_CYCLE_CMD` in `config/overnight-runner.env` to plug in the actual autonomous work executor.
- Current setup fixes the reliability/control gap and gives evidence trails for every checkpoint.

## Execution discipline (user directive)
- For every material change, update all three where applicable:
  1) **Docs** (design/policy/run-log artifacts)
  2) **Issues** (status, blockers, decisions)
  3) **PRs** (what changed, risk, review notes)
- No silent changes: each work step must leave a trace in at least one repo artifact and one GitHub thread.
