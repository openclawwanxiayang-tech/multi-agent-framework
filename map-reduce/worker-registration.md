# Map-Reduce Worker Registration

> Defines how workers publish outputs to the blackboard in Map-Reduce mode.

## Worker Contract

Each map-reduce worker must:

1. **Register** on startup with orchestrator
2. **Accept** map tasks via queue
3. **Publish** outputs to blackboard with:
   - `worker_id`: unique identifier
   - `task_id`: parent task
   - `output_path`: artifact location
   - `criteria_scores`: scores against acceptance criteria
   - `metadata`: timing, tokens, etc.

## Worker Types

| Type | Role | Output |
|------|------|--------|
| `mapper` | Process subtask | Partial artifact |
| `reducer` | Merge/select | Final artifact |
| `verifier` | Validate outputs | Verification report |

## Registration API

```json
{
  "$version": "1.0.0",
  "worker_id": "worker-dev-001",
  "type": "mapper|reducer|verifier",
  "capabilities": ["python", "go", "javascript"],
  "status": "idle|busy|offline",
  "registered_at": "2026-03-02T12:00:00Z"
}
```

## Output Publishing

Workers publish to blackboard:

```json
{
  "$version": "1.0.0",
  "output_id": "out-001",
  "worker_id": "worker-dev-001",
  "task_id": "T-2026-MVP-001",
  "stage": "MAP",
  "output_path": "artifacts/tasks/T-2026-MVP-001/outputs/mapper-001/solution.py",
  "criteria_scores": {
    "correctness": 0.9,
    "efficiency": 0.85,
    "readability": 0.95
  },
  "metadata": {
    "duration_ms": 45000,
    "tokens_used": 12000
  },
  "published_at": "2026-03-02T12:01:00Z"
}
```

## Heartbeat

Workers must send heartbeat every 60s to remain active.
