# Operations Boundary

This repository contains product/framework artifacts.

Operational runtime automation for a specific OpenClaw host (overnight cron jobs, local watchdog scripts, host paths, and run logs) is intentionally maintained **outside** this repo.

## External location

- `/home/lenovo/.openclaw/ops/overnight/`
  - `scripts/`
  - `config/`
  - `docs/`

## Rationale

- Keeps framework repo focused on reusable product architecture/specs.
- Prevents host-specific automation from polluting product PRs.
- Reduces accidental coupling between runtime operations and framework design changes.
