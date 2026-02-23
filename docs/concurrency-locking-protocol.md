# Concurrency & Locking Protocol (Pipeline MVP)

## Scope
Applies to Pipeline mode orchestration artifacts:
- `state.json`
- `events.ndjson`
- task folders under `artifacts/tasks/{task-id}`

## Lock File Format
Path: `.openclaw/locks/{resource}.lock`

```json
{
  "resource": "task:{task-id}:state",
  "trace_id": "<uuid>",
  "agent": "<agent-id>",
  "pid": 12345,
  "host": "<hostname>",
  "created_at": "2026-02-23T15:00:00Z",
  "expires_at": "2026-02-23T15:05:00Z",
  "version": 1
}
```

## Atomic Write Method
Default: temp-file + atomic rename.
1. Write full payload to `{target}.tmp.{trace_id}`
2. `fsync` temp file
3. `rename(temp, target)` (same filesystem)
4. `fsync` parent directory (when available)

Alternative when available: advisory `flock` around the critical section.

## Stale Lock Recovery
- TTL default: 5 minutes.
- A lock is stale if `now > expires_at`.
- Before force-release, verifier checks:
  1. process `pid` exists on `host` (if local), and
  2. last heartbeat/event for `trace_id` is older than TTL.
- If both checks indicate dead/inactive, lock may be force-released.
- Every force-release must append a structured event in `events.ndjson`.

## Concurrency Rules
| Operation | Safe Concurrent? | Rule |
|---|---|---|
| Read `state.json` | Yes | Multiple readers allowed |
| Append `events.ndjson` | Yes | Append-only, single-line JSON events |
| Update `state.json` | No | Must hold resource lock |
| Create new task | Yes | Use collision-free task ID |

## Must-Serialize Operations
- Stage transitions (`SPEC→DESIGN→...`)
- Artifact pointer/hash updates
- Any mutation of task state fields

## Lock Granularity
- Preferred: per-task lock (`task:{task-id}:state`)
- Optional global lock for repo-wide migrations (`repo:migration`)

## Failure Behavior
- On lock acquire timeout: backoff + retry (bounded)
- On repeated failure: escalate to human/manual review
- No partial writes: if atomic write fails, retain previous known-good file
