# ADR 0001: Locking model, atomic writes, and event granularity

- Date: 2026-03-02
- Status: Accepted

## Context
The repo had drift between lock docs and lock schema, and lacked explicit decisions on write semantics and event detail.

## Decision
1. Locking model: lease lock with heartbeat + stale reclaim (`docs/schemas/lock.json` canonical).
2. Atomic writes: temp-file + `os.replace` for `task.json`, `state.json`, `.lock`.
3. Event granularity (minimum required):
   - TASK_CREATED
   - STAGE_TRANSITION
   - STAGE_COMPLETED / TASK_COMPLETED
   - LOCK_RECLAIMED (when applicable)

## Consequences
- Deterministic conflict handling in repo-native queue.
- Recoverability and auditability through explicit lock recovery events.
- Lower ambiguity for orchestrator implementation and tests.
