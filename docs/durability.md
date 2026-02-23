# Durability & Recovery Protocol

> Version: 1.0.0  
> Last Updated: 2026-02-23

---

## Overview

This document defines the durability and recovery protocol for the v2.2 MVP. It ensures tasks can survive orchestrator crashes and resume safely.

---

## Status Values

| Status | Description | Recoverable? |
|--------|-------------|--------------|
| `PENDING` | Not yet started | Yes |
| `IN_PROGRESS` | Currently executing | Yes (if checkpoint exists) |
| `BLOCKED` | Waiting on dependency | Yes |
| `BLOCKED_APPROVAL` | Waiting on human approval | Yes (manual resolve) |
| `NEEDS_RECONCILE` | Checkpoint mismatch detected | Yes (manual review) |
| `WAITING_APPROVAL` | Pending approval | Yes |
| `COMPLETED` | Successfully finished | N/A |
| `FAILED` | Failed (no retries left) | No |

---

## Recoverable Tasks

On startup, identify tasks with status in:

```python
RECOVERABLE_STATUSES = {
    "IN_PROGRESS",
    "BLOCKED",
    "BLOCKED_APPROVAL", 
    "NEEDS_RECONCILE",
    "WAITING_APPROVAL",
    "FAILED"  # Only if retries remaining
}
```

---

## Lock Protocol

### Lock File Location

```
artifacts/tasks/{task-id}/.lock.json
```

### Lock File Format

```json
{
  "owner_id": "orchestrator-1",
  "host_id": "laptop-e1q327nm",
  "pid": 12345,
  "acquired_at": "2026-02-23T21:00:00Z",
  "heartbeat_ts": "2026-02-23T21:05:00Z",
  "ttl_seconds": 300
}
```

### Lock Acquisition

```python
def acquire_lock(task_id, orchestrator_id):
    lock_path = f"artifacts/tasks/{task_id}/.lock.json"
    
    # Check for existing lock
    if os.path.exists(lock_path):
        existing = json.load(open(lock_path))
        
        # Check if stale (heartbeat > TTL)
        if is_heartbeat_stale(existing):
            # Force reclaim
            pass
        else:
            # Another orchestrator holds lock
            return False
    
    # Create new lock
    lock = {
        "owner_id": orchestrator_id,
        "host_id": get_host_id(),
        "pid": os.getpid(),
        "acquired_at": datetime.utcnow().isoformat() + "Z",
        "heartbeat_ts": datetime.utcnow().isoformat() + "Z",
        "ttl_seconds": 300
    }
    
    atomic_write(lock_path, lock)
    return True
```

### Heartbeat

```python
def update_heartbeat(task_id):
    lock_path = f"artifacts/tasks/{task_id}/.lock.json"
    lock = json.load(open(lock_path))
    lock["heartbeat_ts"] = datetime.utcnow().isoformat() + "Z"
    atomic_write(lock_path, lock)
```

### Stale Detection

```python
def is_heartbeat_stale(lock, ttl_seconds=300):
    heartbeat = datetime.fromisoformat(lock["heartbeat_ts"].replace("Z", "+00:00"))
    age = (datetime.utcnow() - heartbeat.replace(tzinfo=None)).total_seconds()
    return age > ttl_seconds
```

---

## Atomic Write Protocol

### Method: Write Temp + Rename

```python
import os
import json
import tempfile

def atomic_write(path, data):
    """Write data atomically to prevent partial writes."""
    dir_path = os.path.dirname(path)
    
    # Write to temp file in same directory
    fd, temp_path = tempfile.mkstemp(dir=dir_path, suffix='.tmp')
    
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())  # Ensure durability
        
        # Atomic rename
        os.rename(temp_path, path)
    except Exception:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise
```

### Backup File (Recommended)

```python
def atomic_write_with_backup(path, data):
    # Create backup of existing file
    if os.path.exists(path):
        backup_path = path + ".bak"
        shutil.copy(path, backup_path)
    
    # Write new file
    atomic_write(path, data)
```

---

## Recovery Algorithm

### On Orchestrator Startup

```python
def startup_recovery():
    """Scan and recover unfinished tasks on startup."""
    
    tasks_dir = "artifacts/tasks"
    recovered = []
    failed = []
    
    for task_id in os.listdir(tasks_dir):
        state_path = f"{tasks_dir}/{task_id}/state.json"
        
        if not os.path.exists(state_path):
            continue
        
        # Load state safely
        state = load_state_safely(task_id)
        if state is None:
            continue
        
        # Check if recoverable
        if state["status"] in RECOVERABLE_STATUSES:
            try:
                recover_task(task_id, state)
                recovered.append(task_id)
            except Exception as e:
                log_event(task_id, "recovery_failed", {"error": str(e)})
                failed.append(task_id)
    
    return {"recovered": recovered, "failed": failed}
```

### Load State Safely

```python
def load_state_safely(task_id):
    """Load state.json with fallback to backup."""
    state_path = f"artifacts/tasks/{task_id}/state.json"
    backup_path = state_path + ".bak"
    
    # Try primary
    try:
        state = json.load(open(state_path))
        # Validate required fields
        validate_state(state)
        return state
    except (json.JSONDecodeError, ValidationError):
        pass
    
    # Try backup
    if os.path.exists(backup_path):
        try:
            state = json.load(open(backup_path))
            validate_state(state)
            log_event(task_id, "state_recovered", {"source": "backup"})
            return state
        except (json.JSONDecodeError, ValidationError):
            pass
    
    # Failed to load
    log_event(task_id, "state_load_failed", {"task_id": task_id})
    return None
```

### Recover Task

```python
def recover_task(task_id, state):
    """Recover a single task."""
    
    # Step 1: Acquire lock
    if not acquire_lock(task_id, get_orchestrator_id()):
        log_event(task_id, "recovery_skipped", {"reason": "lock_held"})
        return
    
    try:
        # Step 2: Verify checkpoint integrity
        if not verify_checkpoints(task_id, state):
            state["status"] = "NEEDS_RECONCILE"
            save_state(task_id, state)
            log_event(task_id, "checkpoint_mismatch", {"status": "NEEDS_RECONCILE"})
            return
        
        # Step 3: Determine resume point
        resume_stage = determine_resume_point(state)
        
        # Step 4: Handle based on stage type
        if is_idempotent_stage(resume_stage):
            # Re-run from checkpoint
            state["status"] = "IN_PROGRESS"
            save_state(task_id, state)
            log_event(task_id, "recovery_started", {"stage": resume_stage})
            # Continue normal execution...
        else:
            # Non-idempotent - check external state
            if verify_external_idempotency(task_id, resume_stage):
                state["status"] = "IN_PROGRESS"
                save_state(task_id, state)
            else:
                state["status"] = "BLOCKED_APPROVAL"
                save_state(task_id, state)
                log_event(task_id, "recovery_blocked", {"reason": "non-idempotent"})
        
    finally:
        release_lock(task_id)
```

---

## Checkpoint Verification

### Durably Complete Stage

A stage is durably complete only if:

1. **Checkpoint entry exists** in `state.json.checkpoints`
2. **Artifact paths are recorded** with SHA256 hashes
3. **Artifacts exist** on filesystem
4. **Hashes match** current artifact content

```python
def verify_checkpoints(task_id, state):
    """Verify all checkpoints are still valid."""
    
    for checkpoint in state.get("checkpoints", []):
        artifact_path = checkpoint["artifact"]
        expected_hash = checkpoint["hash"]
        
        # Check artifact exists
        if not os.path.exists(artifact_path):
            return False
        
        # Check hash matches
        actual_hash = compute_sha256(artifact_path)
        if actual_hash != expected_hash:
            return False
    
    return True
```

---

## NDJSON Tolerant Reader

### Reading Events

```python
def read_events(task_id):
    """Read events.ndjson, tolerating truncated last line."""
    events_path = f"artifacts/tasks/{task_id}/logs/events.ndjson"
    events = []
    
    if not os.path.exists(events_path):
        return events
    
    with open(events_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError truncated/incomplete line
:
                # Skip                pass
    
    return events
```

---

## Event Log Events

### Recovery-Specific Events

| Event Type | Fields | Description |
|------------|--------|-------------|
| `state_recovered` | source: "primary" \| "backup" | State loaded from backup |
| `state_load_failed` | error: string | Both primary and backup failed |
| `lock_recovered` | previous_owner: string | Stale lock force-reclaimed |
| `recovery_started` | stage: string | Recovery begun for task |
| `recovery_blocked` | reason: string | Non-idempotent stage blocked |
| `checkpoint_mismatch` | checkpoint: string | Hash mismatch detected |
| `recovery_skipped` | reason: string | Lock held by another orchestrator |

---

## Related

- See also: `docs/schemas/state.json`
- See also: `docs/CONCURRENCY.md`
- Related issue: Startup Recovery Policy

---

*Last updated: 2026-02-23*
