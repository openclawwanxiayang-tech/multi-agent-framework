# SPEC: Agent Handoff Contract

## Overview
Standardize PM/Designer/Dev/QA handoffs so stage transitions are consistent, auditable, and gateable.

## Handoff Schema

### Required Fields (All Handoffs)
- `task_id`
- `from_role` (`PM|Designer|Dev|QA`)
- `to_role` (`PM|Designer|Dev|QA|Release`)
- `handoff_at` (ISO8601 UTC)
- `version`
- `summary`
- `status` (`ready|blocked|needs-clarification`)
- `artifacts` (list of repository file paths)
- `acceptance_criteria_ref`
- `open_questions` (list; may be empty)
- `risks` (list; may be empty)

### Optional Fields (All Handoffs)
- `assumptions`
- `dependencies`
- `notes`

### Role-Specific Required Fields
- PM -> Designer: `problem_statement`, `requirements`, `acceptance_criteria`, `priority`
- Designer -> Dev: `design_decisions`, `interaction_flows`, `edge_cases`, `traceability_to_requirements`
- Dev -> QA: `implementation_summary`, `changed_files`, `test_evidence`, `known_limitations`
- QA -> Release: `test_results`, `defects_found`, `coverage_summary`, `go_no_go_recommendation`

## Concrete Examples

### PM -> Designer
```yaml
task_id: task-002-agent-handoff-contract
from_role: PM
to_role: Designer
handoff_at: 2026-03-10T03:00:00Z
version: v1
summary: "Spec ready for design"
status: ready
artifacts: [artifacts/tasks/task-002-agent-handoff-contract/requirements.md]
acceptance_criteria_ref: artifacts/tasks/task-002-agent-handoff-contract/SPEC.md
open_questions: []
risks: ["interpretation drift"]
problem_statement: "Inconsistent handoffs cause rework."
requirements: ["REQ-1 define mandatory handoff fields"]
acceptance_criteria: ["AC-1 completeness is machine-checkable"]
priority: P1
```

### Designer -> Dev
```yaml
task_id: task-002-agent-handoff-contract
from_role: Designer
to_role: Dev
handoff_at: 2026-03-10T04:00:00Z
version: v2
summary: "Design ready for implementation"
status: ready
artifacts: [artifacts/tasks/task-002-agent-handoff-contract/design.md]
acceptance_criteria_ref: artifacts/tasks/task-002-agent-handoff-contract/SPEC.md
open_questions: []
risks: ["edge-case expansion"]
design_decisions: ["Use structured YAML handoff records"]
interaction_flows: ["PM -> Designer -> Dev -> QA"]
edge_cases: ["conflicting requirement wording"]
traceability_to_requirements: ["REQ-1 -> DD-1"]
```

### Dev -> QA
```yaml
task_id: task-002-agent-handoff-contract
from_role: Dev
to_role: QA
handoff_at: 2026-03-10T05:00:00Z
version: v3
summary: "Implementation complete for QA"
status: ready
artifacts: [artifacts/tasks/task-002-agent-handoff-contract/implementation-notes.md]
acceptance_criteria_ref: artifacts/tasks/task-002-agent-handoff-contract/SPEC.md
open_questions: []
risks: ["Strict validator rules may require wording fixes"]
implementation_summary: "Implemented handoff schema and checks"
changed_files: ["workspaces/dev-01/handoff_validator.py"]
test_evidence: ["pytest tests/test_handoff_validator.py -> 12 passed"]
known_limitations: ["No auto-repair for malformed records"]
```

### QA -> Release
```yaml
task_id: task-002-agent-handoff-contract
from_role: QA
to_role: Release
handoff_at: 2026-03-10T06:00:00Z
version: v4
summary: "QA complete with release recommendation"
status: ready
artifacts: [artifacts/tasks/task-002-agent-handoff-contract/test-results.md]
acceptance_criteria_ref: artifacts/tasks/task-002-agent-handoff-contract/SPEC.md
open_questions: []
risks: ["Minor doc-only inconsistency"]
test_results: "Pass with minor warnings"
defects_found: ["No blocker defects"]
coverage_summary: "All acceptance criteria verified"
go_no_go_recommendation: go
```

## Validation Rules

### Blocker
- Missing any required common field.
- Missing any required role-specific field.
- `status` is not `ready` at a progression gate.
- Any path in `artifacts` or `acceptance_criteria_ref` does not resolve.
- Acceptance criteria are missing or non-testable.
- QA handoff omits explicit `go_no_go_recommendation`.

### Warning
- Optional fields (`assumptions`, `dependencies`, `notes`) missing.
- Minor formatting inconsistency in non-required text fields.
- `open_questions` empty for complex scope (allowed but flagged).
- Non-critical traceability notes incomplete while core mapping exists.

## File Naming and Location Conventions
- Base location: `artifacts/tasks/{task-id}/`
- Required files: `SPEC.md`, `requirements.md`, `design.md`, `implementation-notes.md`, `test-results.md`
- Recommended handoff records:
  - `handoffs/{timestamp}-{from}-to-{to}.yaml`
  - Example: `handoffs/20260310T060000Z-qa-to-release.yaml`
- Naming rules:
  - Lowercase kebab-case filenames
  - UTC timestamps
  - One handoff record per transition

## Definition of Done by Role
- PM: requirements and acceptance criteria are complete, numbered, and testable.
- Designer: design decisions map to requirements; flows and edge cases documented.
- Dev: implementation summary and changed files documented; test evidence included.
- QA: test outcomes and defects documented; explicit `go/no-go` present.

## Failure Scenarios and Expected Handling
1. Missing PM spec field -> **Blocker**; return to PM with missing-field list.
2. Conflicting PM requirements and Designer output -> **Blocker**; escalate to Admin.
3. Stale design after PM changes -> **Blocker**; require refresh + version bump.
4. Dev handoff includes failing test evidence -> **Blocker**; return to Dev.
5. QA verdict unclear or absent -> **Blocker**; halt release progression.

## Acceptance Criteria
- A standard handoff schema is defined with required/optional fields and role examples.
- Validation rules explicitly separate **Blocker** vs **Warning** outcomes.
- File naming and location conventions are defined under `artifacts/tasks/{task-id}/`.
- Definition of Done is clear for PM, Designer, Dev, and QA.
- Five failure scenarios and expected handling are documented.
- Scope remains process/spec only.

## Out of Scope
- Implementing validator code, CI checks, or orchestration runtime changes.
- Building UI/workflow automation tools.
- Any source-code feature implementation beyond this process specification.
