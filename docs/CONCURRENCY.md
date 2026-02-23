# Concurrency & Locking Protocol

> Version: 1.0.0  
> Last Updated: 2026-02-23

---

## Overview

This document defines the concurrency/locking protocol for the repo-native task queue to prevent state corruption during multi-agent execution.

---

## Lock File Format

### Location

```
artifacts/tasks/{task-id}/.lock
```

### Content

```json
{
  "agent_id": "agent-pm-1",
  "started_at": "2026-02-23T10:00:00Z",
  "ttl_seconds": 300,
  "trace_id": "trace-abc123"
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `agent_id` | string | ID of agent holding the lock |
| `started_at` | ISO8601 | When lock was acquired |
| `ttl_seconds` | integer | Time-to-live (default: 300 = 5 min) |
| `trace_id` | string | Trace for debugging |

---

## Atomic Write Method

### Method 1: Write to Temp + Atomic Rename (Recommended)

```python
import os
import json
import tempfile

def atomic_write(path, data):
    """Write data atomically to prevent partial writes."""
    dir_path = os.path.dirname(path)
    
    # Write to temp file in same directory (for atomic rename)
    fd, temp_path = tempfile.mkstemp(dir=dir_path, suffix='.tmp')
    
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Atomic rename
        os.rename(temp_path, path)
    except Exception:
        # Clean up temp file on failure
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise
```

### Method 2: File Lock (flock)

```python
import fcntl

def write_with_lock(path, data):
    with open(path, 'w') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            json.dump(data, f)
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
```

---

## Stale Lock Recovery

### Detection

A lock is stale if:

```python
import time
from datetime import datetime, timedelta

def is_lock_stale(lock_path):
    with open(lock_path) as f:
        lock = json.load(f)
    
    started = datetime.fromisoformat(lock['started_at'].replace('Z', '+00:00'))
    ttl = lock.get('ttl_seconds', 300)
    age = time.time() - started.timestamp()
    
    return age > ttl
```

### Recovery Rules

1. **Check if agent still alive**: Look up `trace_id` in events.ndjson
2. **If confirmed stale**: Force-release lock
3. **If agent active**: Wait or escalate

```python
def recover_stale_lock(lock_path, task_id):
    if not is_lock_stale(lock_path):
        return False  # Lock is valid
    
    # Check if agent is still writing events
    trace_id = get_lock_trace_id(lock_path)
    if agent_has_recent_events(trace_id, seconds=60):
        return False  # Agent still active
    
    # Force release
    os.unlink(lock_path)
    log_event(task_id, "lock_recovery", {"reason": "stale", "trace_id": trace_id})
    return True
```

---

## Concurrency Rules

### Safe Concurrent Operations

| Operation | Safe Concurrent? | Notes |
|-----------|------------------|-------|
| Read state.json | ✅ Yes | Multiple readers OK |
| Read events.ndjson | ✅ Yes | Append-only log |
| Append events.ndjson | ✅ Yes | Single append per event |
| Create new task | ✅ Yes | Unique task IDs |
| Read lock file | ✅ Yes | No modification |

### Operations That Must Be Serialized

| Operation | Reason |
|-----------|--------|
| Update state.json | Prevents race conditions |
| Stage transitions | Only one stage at a time |
| Artifact commits | Prevents merge conflicts |
| Acquire lock | Only one writer per task |

---

## Implementation Example

```python
import os
import json
import time
from pathlib import Path

class TaskLock:
    def __init__(self, task_id, agent_id, trace_id):
        self.task_id = task_id
        self.agent_id = agent_id
        self.trace_id = trace_id
        self.lock_path = Path(f"artifacts/tasks/{task_id}/.lock")
    
    def acquire(self, ttl_seconds=300):
        # Check for existing lock
        if self.lock_path.exists():
            if is_lock_stale(self.lock_path):
                recover_stale_lock(self.lock_path, self.task_id)
            else:
                raise LockException("Task is locked by another agent")
        
        # Create lock file
        lock = {
            "agent_id": self.agent_id,
            "started_at": datetime.utcnow().isoformat() + "Z",
            "ttl_seconds": ttl_seconds,
            "trace_id": self.trace_id
        }
        
        # Atomic write
        atomic_write(self.lock_path, lock)
    
    def release(self):
        if self.lock_path.exists():
            os.unlink(self.lock_path)
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, *args):
        self.release()
```

---

## Usage

```python
# In orchestrator
with TaskLock(task_id, agent_id, trace_id) as lock:
    # Update state
    state = read_state(task_id)
    state['stage'] = 'DESIGN'
    state['status'] = 'IN_PROGRESS'
    atomic_write(state_path, state)
    
    # Do work...
```

---

## Related

- See also: `docs/schemas/state.json`
- Related issue: #3

---

*Last updated: 2026-02-23*
