# Conflict Resolution Rules

> How to handle disagreements in map-reduce outputs.

## Conflict Types

| Type | Description | Resolution |
|------|-------------|------------|
| Score ties | Equal aggregate scores | Prefer correctness → earlier → human |
| Quality gap | One output clearly superior | Select best |
| Partial failure | Some mappers failed | Exclude failed, continue |
| All failed | No outputs viable | Escalate to human |

## Escalation Triggers

Escalate to human when:
- All mappers failed
- Score difference < 5% but different approaches
- Verifier cannot decide
- Policy requires human approval

## Escalation Payload

```json
{
  "$version": "1.0.0",
  "event": "ESCALATE",
  "task_id": "T-2026-MVP-001",
  "reason": "all_mappers_failed|score_tie|policy_required",
  "context": {
    "attempted_mappers": 3,
    "failed": 3,
    "scores": [...]
  },
  "requires_approval": true,
  "escalated_at": "2026-03-02T12:10:00Z"
}
```

## Logging

All conflicts logged to events.ndjson with:
- `trace_id`
- `conflict_type`
- `resolution_applied`
- `human_escalated`
