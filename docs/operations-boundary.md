# Operations Boundary

This repository contains product/framework artifacts.

Operational runtime automation for a specific OpenClaw host (long-running cron jobs, local watchdog scripts, host paths, and run logs) is intentionally maintained **outside** this repo.

## External location

- `/home/lenovo/.openclaw/ops/longrun/`
  - `scripts/`
  - `config/`
  - `docs/`

## Rationale

- Keeps framework repo focused on reusable product architecture/specs.
- Prevents host-specific automation from polluting product PRs.
- Reduces accidental coupling between runtime operations and framework design changes.

## Verification snapshot (2026-02-24)

- External longrun scripts smoke-tested successfully.
- Scheduled execution verified with accelerated cron drill, then restored to:
  - `*/15` progress log
  - `*/30` checkpoint
  - `*/10` watchdog
- Stale-condition simulation confirmed watchdog alert path.
- Session map auto-sync added externally (`sync_session_map.sh`, cron `*/2`) to keep channel/session mapping up to date.
