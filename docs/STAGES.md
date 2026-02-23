# Stage Transitions & Failure Semantics

> Version: 1.0.0  
> Last Updated: 2026-02-23

---

## Overview

This document defines the executable state machine for Pipeline mode.

---

## Stage Graph (Pipeline Mode)

```
SPEC → DESIGN → IMPLEMENT → REVIEW → QA → RELEASE → DONE
  │        │          │        │     │        │
  │        │          │        │     │        └──→ DONE
  │        │          │        │     └──────────→ DONE
  │        │          │        └──────────────→ QA
  │        │          └──────────────────────→ REVIEW
  │        └────────────────────────────────→ IMPLEMENT
  └──────────────────────────────────────────→ DESIGN
```

### Allowed Edges

| From | To | Condition |
|------|----|-----------|
| SPEC | DESIGN | Spec approved (validator passes) |
| DESIGN | IMPLEMENT | Design approved |
| IMPLEMENT | REVIEW | Code committed |
| REVIEW | QA | Review approved |
| QA | RELEASE | Tests passed |
| RELEASE | DONE | Deployment complete |

### Back Edges (Retry/Failure)

| From | To | Condition |
|------|----|-----------|
| Any | SPEC | Retry from start (if idempotent) |
| REVIEW | IMPLEMENT | Request changes |
| QA | IMPLEMENT | Fix bugs |
| RELEASE | IMPLEMENT | Rollback |

---

## Stage Definitions

### SPEC (Specification)

- **Purpose**: Create requirements and acceptance criteria
- **Artifacts**: `spec.md`, `acceptance.md`
- **Validator**: spec_validator.py

### DESIGN

- **Purpose**: Create UI/UX and technical design
- **Artifacts**: `design.md`, `wireframes/`
- **Validator**: design_validator.py

### IMPLEMENT

- **Purpose**: Write code
- **Artifacts**: Source files, tests
- **Validator**: code_linter.py

### REVIEW

- **Purpose**: Code review
- **Artifacts**: Review notes, comments
- **Validator**: None (human review)

### QA

- **Purpose**: Testing
- **Artifacts**: Test results, bug reports
- **Validator**: qa_checker.py

### RELEASE

- **Purpose**: Deploy
- **Artifacts**: Deployment notes, changelog
- **Validator**: deployment_checks.py

### DONE

- **Purpose**: Complete
- **Artifacts**: Final summary

---

## Retry Policy

| Stage | Max Retries | Backoff | Escalate After |
|-------|-------------|---------|----------------|
| SPEC | 2 | linear | 2 failures |
| DESIGN | 2 | linear | 2 failures |
| IMPLEMENT | 3 | exponential | 3 failures |
| REVIEW | 1 | none | 1 failure |
| QA | 2 | linear | 2 failures |
| RELEASE | 1 | none | 1 failure |

### Backoff Formula

```
linear:    wait = retry_count * base_wait
exponential: wait = 2^retry_count * base_wait
```

---

## Escalation Triggers

Escalate to human approval when:

1. **Retry limit exceeded** - Agent can't make progress
2. **Risk tier = High/Critical** - Requires human sign-off
3. **Validator failure rate > 20%** - Repeated failures
4. **Tool denied** - Permission issue
5. **Manual override** - Agent or user requests review

---

## Idempotency Rules

| Stage | Re-runnable? | Conditions |
|-------|--------------|------------|
| SPEC | ✅ Yes | If no DESIGN artifact exists |
| DESIGN | ✅ Yes | If no IMPLEMENT artifact exists |
| IMPLEMENT | ✅ Yes | With same artifact hashes (deterministic) |
| REVIEW | ❌ No | Must start fresh (human review) |
| QA | ✅ Yes | With same test suite |
| RELEASE | ❌ No | Must start fresh (deployment) |

### Idempotency Check

```python
def can_rerun_stage(task_id, stage):
    state = read_state(task_id)
    
    if stage == "SPEC":
        # Can rerun if no design yet
        return not Path(f"artifacts/{task_id}/design/design.md").exists()
    
    if stage == "IMPLEMENT":
        # Can rerun if same code hash
        current_hash = compute_hash("impl/")
        return current_hash == state.get('impl_hash')
    
    return False  # Non-idempotent stages
```

---

## State Machine Implementation

```python
from enum import Enum
from typing import Optional

class Stage(Enum):
    SPEC = "SPEC"
    DESIGN = "DESIGN"
    IMPLEMENT = "IMPLEMENT"
    REVIEW = "REVIEW"
    QA = "QA"
    RELEASE = "RELEASE"
    DONE = "DONE"

# Allowed transitions
ALLOWED_EDGES = {
    Stage.SPEC: [Stage.DESIGN],
    Stage.DESIGN: [Stage.IMPLEMENT],
    Stage.IMPLEMENT: [Stage.REVIEW],
    Stage.REVIEW: [Stage.QA],
    Stage.QA: [Stage.RELEASE],
    Stage.RELEASE: [Stage.DONE],
}

# Max retries per stage
MAX_RETRIES = {
    Stage.SPEC: 2,
    Stage.DESIGN: 2,
    Stage.IMPLEMENT: 3,
    Stage.REVIEW: 1,
    Stage.QA: 2,
    Stage.RELEASE: 1,
}

def transition(state, from_stage, to_stage):
    """Execute stage transition with validation."""
    
    # Check allowed edge
    allowed = ALLOWED_EDGES.get(from_stage, [])
    if to_stage not in allowed:
        raise InvalidTransitionError(f"{from_stage} -> {to_stage} not allowed")
    
    # Check retry limit
    retries = state.get('retries', {}).get(to_stage.value, 0)
    if retries >= MAX_RETRIES[to_stage]:
        raise EscalationError(f"Max retries exceeded for {to_stage}")
    
    # Execute transition
    state['stage'] = to_stage.value
    state['status'] = 'IN_PROGRESS'
    state['retries'][to_stage.value] = retries + 1
    
    return state
```

---

## Related

- See also: `docs/schemas/state.json`
- Related issue: #4

---

*Last updated: 2026-02-23*
