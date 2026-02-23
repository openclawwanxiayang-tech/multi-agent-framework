# Stage Transitions & Failure Semantics (Pipeline MVP)

## Pipeline State Machine
Stages:
`SPEC -> DESIGN -> IMPLEMENT -> REVIEW -> QA -> RELEASE -> DONE`

## Allowed Edges
| From | To | Condition |
|---|---|---|
| SPEC | DESIGN | Spec approved |
| DESIGN | IMPLEMENT | Design approved |
| IMPLEMENT | REVIEW | Code committed |
| REVIEW | QA | Review approved |
| QA | RELEASE | Tests passed |
| RELEASE | DONE | Deployment complete |

No backward edges in MVP; retries re-run the same stage.

## Retry Policy
| Stage | Max Retries | Backoff |
|---|---:|---|
| SPEC | 2 | linear |
| DESIGN | 2 | linear |
| IMPLEMENT | 3 | exponential |
| REVIEW | 1 | none |
| QA | 2 | linear |
| RELEASE | 1 | none |

Suggested defaults:
- linear: 30s, 60s, ...
- exponential: 30s, 60s, 120s

## Escalation Policy
Escalate to human approval when any condition is true:
1. Retry limit exceeded
2. Risk tier = `high` or `critical`
3. Validator failure rate > 20% in current stage window

Escalation event shape (example):
```json
{"type":"escalation.required","task_id":"T-123","stage":"QA","reason":"retry_limit_exceeded","trace_id":"..."}
```

## Idempotency Rules
| Stage | Re-runnable? | Conditions |
|---|---|---|
| SPEC | Yes | No DESIGN artifact committed yet |
| DESIGN | Yes | No IMPLEMENT artifact committed yet |
| IMPLEMENT | Yes | Same input spec hash + deterministic build context |
| REVIEW | No | Must open a fresh review cycle |
| QA | Yes | Same build + same test plan |
| RELEASE | No | Must initiate fresh release transaction |

## Failure Semantics
- Any failed stage attempt emits `stage.failed` event.
- Retry attempts emit `stage.retry_scheduled` with backoff metadata.
- Escalations emit `escalation.required` and transition task to `BLOCKED` until approval.
- Terminal failure emits `task.failed` when escalation is declined or unresolved.

## Implementation Hooks
- Config source of truth: `workflow.yaml` (to be added/updated)
- Orchestrator responsibilities:
  - enforce allowed edges
  - enforce retry/backoff policy
  - enforce escalation trigger evaluation
  - persist all transition/failure events to `events.ndjson`
