# Schema Documentation

JSON schemas for the Multi-Agent Framework v2.2.

---

## Overview

| Schema | File | Purpose |
|--------|------|---------|
| **Task** | `task.json` | Task identity and contract |
| **TaskState** | `state.json` | Durable execution state machine |
| **Envelope** | `envelope.json` | Structured handoff between agents |
| **Event** | `event.json` | Append-only event log entry |

---

## task.json

Task identity and contract. Created at task initialization.

```json
{
  "task_id": "T-2026-02-23-001",
  "title": "Add durable task queue + blackboard spec",
  "created_at": "2026-02-23T10:00:00Z",
  "mode": "pipeline",
  "risk_tier": "medium",
  "definition_of_done": [
    "Spec approved",
    "Design approved",
    "Implementation merged",
    "QA passed"
  ],
  "budgets": {
    "max_tool_calls": 120,
    "max_total_tokens": 400000
  }
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `task_id` | string | Unique ID (format: T-YYYY-MM-XXX) |
| `title` | string | Human-readable title |
| `created_at` | datetime | ISO 8601 timestamp |
| `mode` | enum | pipeline, map_reduce, incident |
| `risk_tier` | enum | low, medium, high, critical |
| `definition_of_done` | array | Completion criteria |
| `budgets` | object | Execution limits |

---

## state.json

Durable execution state machine. Updated at each stage transition.

```json
{
  "task_id": "T-2026-02-23-001",
  "stage": "DESIGN",
  "status": "IN_PROGRESS",
  "assigned": [
    {"role": "designer", "agent_id": "agent-designer-1"},
    {"role": "pm", "agent_id": "agent-pm-1"}
  ],
  "dependencies": [],
  "checkpoints": [
    {"stage": "SPEC", "artifact": "artifacts/spec/spec.md", "hash": "sha256:..."}
  ],
  "retries": {"DESIGN": 1},
  "next": ["MERGE_SPEC_DESIGN"]
}
```

### Stage Values

```
SPEC → MERGE_SPEC_DESIGN → IMPLEMENT → REVIEW → QA → RELEASE → DONE
```

### Status Values

- `PENDING` - Not yet started
- `IN_PROGRESS` - Currently executing
- `BLOCKED` - Waiting on dependencies
- `WAITING_APPROVAL` - Needs human approval
- `COMPLETED` - Stage finished successfully
- `FAILED` - Stage failed

---

## envelope.json

Structured handoff between agents. Replaces free-form chat.

```json
{
  "task_id": "T-2026-02-23-001",
  "from_role": "pm",
  "to_role": "director",
  "stage": "SPEC",
  "outputs": {
    "spec_path": "artifacts/spec/spec.md",
    "acceptance_path": "artifacts/spec/acceptance.md"
  },
  "claims": {
    "scope_locked": true,
    "open_questions": ["Do we adopt MCP in v2.2 or v2.3?"]
  }
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `from_role` | string | Sending role |
| `to_role` | string | Receiving role |
| `outputs` | object | Artifact paths produced |
| `claims` | object | Scope status, open questions |

---

## event.json

Append-only event log entry. Stored as NDJSON.

```json
{
  "ts": "2026-02-23T10:05:00Z",
  "trace_id": "trace-001",
  "task_id": "T-2026-02-23-001",
  "agent": "pm-1",
  "role": "pm",
  "type": "artifact_write",
  "path": "artifacts/spec/spec.md",
  "hash": "sha256:abc123...",
  "result": "success",
  "level": "info"
}
```

### Event Types

| Type | Description |
|------|-------------|
| `artifact_write` | File written to blackboard |
| `artifact_read` | File read from blackboard |
| `tool_call` | Tool executed |
| `validator` | Validation check ran |
| `stage_transition` | Moved to next stage |
| `approval` | Human approval granted |
| `error` | Error occurred |

---

## Usage

### Validation

```bash
# Validate a task
cat task.json | jq -s

# Validate with JSON Schema
ajv validate -s schemas/task.json -d task.json
```

### Python (Pydantic)

```python
from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    task_id: str
    title: str
    created_at: datetime
    mode: str  # pipeline, map_reduce, incident
    risk_tier: str  # low, medium, high, critical
    definition_of_done: List[str]
    budgets: Optional[dict] = None
```

---

*Last updated: 2026-02-23*
