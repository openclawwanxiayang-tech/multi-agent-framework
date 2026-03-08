# Concurrency & Locking Protocol

> Version: 1.1.0  
> Last Updated: 2026-03-02

---

## Overview

This protocol defines safe concurrent access for the repo-native queue under `artifacts/tasks/{task_id}`.

Canonical contract for lock files is `docs/schemas/lock.json`.

Lock model: **lease with heartbeat + stale reclaim**.

---

## Lock File Contract (Canonical)

### Location

`artifacts/tasks/{task-id}/.lock`

### Content

```json
{
  "$version": "1.0.0",
  "owner_id": "agent-pm-1",
  "host_id": "laptop-e1q327nm",
  "pid": 4242,
  "acquired_at": "2026-03-02T12:00:00Z",
  "heartbeat_ts": "2026-03-02T12:00:15Z",
  "ttl_seconds": 300
}
```

### Semantics

- `owner_id`: logical lock owner (agent/orchestrator)
- `host_id` + `pid`: process identity for diagnostics
- `acquired_at`: first lock acquisition timestamp
- `heartbeat_ts`: refreshed periodically while lock holder is active
- `ttl_seconds`: lease duration; stale if `now - heartbeat_ts > ttl_seconds`

---

## Acquisition & Release Rules

1. If `.lock` does not exist, create it with atomic write.
2. If `.lock` exists and lease is fresh, acquisition fails.
3. If `.lock` exists and lease is stale, reclaim is allowed after emitting a lock-recovery event.
4. Lock holder updates `heartbeat_ts` every `ttl_seconds / 3` (or faster).
5. On normal completion, holder removes `.lock`.

---

## Atomic Write Rule

All writes to `state.json` and `.lock` must use temp-file + rename in same directory.

```python
import json, os, tempfile

def atomic_write_json(path, data):
    directory = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)  # atomic replace on POSIX + modern Windows
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
```

---

## Stale Lock Recovery

A lock is stale when:

```text
(now_utc - heartbeat_ts) > ttl_seconds
```

On stale reclaim:
- remove stale `.lock`
- append event `{event: "LOCK_RECLAIMED", details: {previous_owner, previous_pid}}`
- continue acquisition with new owner

---

## Concurrency Guarantees

Safe concurrently:
- read `task.json`
- read `state.json`
- append `events.ndjson` (single line append per event)

Must be serialized by lock:
- stage transitions
- `state.json` updates
- lock replacement/recovery

---

## Source of Truth

When docs conflict:
1. `docs/schemas/lock.json`
2. runtime validator behavior
3. this document
