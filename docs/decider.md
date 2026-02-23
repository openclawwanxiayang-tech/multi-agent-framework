# Collaboration Mode Decider (v2.2)

This rubric decides whether a task should run as **Pipeline SOP**, **Map-Reduce Swarm**, or **Incident Mode**.

---

## Modes

### 1) Pipeline SOP (PM → Design → Dev → QA → Release)

Use when:
- Requirements are ambiguous or stakeholder-facing
- Output quality and traceability matter
- You need clear stage gates and ownership
- Work touches multiple layers (UX + backend + docs)

Signals:
- Many unknowns or decisions to lock early
- A "definition of done" requires multiple validations (spec/design/tests)

### 2) Map-Reduce Swarm (Parallel workers → merge → verifier)

Use when:
- You need breadth: research, options, spikes, comparisons
- The task can be decomposed into independent chunks
- You benefit from "multiple tries" and synthesis

Signals:
- You can split into 3–10 independent subtasks (e.g., compare frameworks, draft variants, generate test cases)
- Merging can be verified objectively (lint/tests/checklists)

Recommended pattern:
1. Director splits into subtasks with typed envelopes
2. Workers produce artifacts + short summaries
3. Director merges into one artifact
4. Verifier validates against acceptance criteria

### 3) Incident Mode (Triage → minimal permissions → mandatory approvals)

Use when:
- Risk is high (production, credentials, infra)
- Time matters, but safety matters more
- You need tight control of tool permissions

Signals:
- Risk tier = High/Critical
- Any action could affect customers or security posture

Rules:
- Mandatory human approvals for deploy/secret/infrastructure operations
- Short feedback loops, aggressive logging, explicit rollback plans

---

## Quick Decision Table

| Question | If YES | Mode |
|---|---|---|
| Is the task High/Critical risk? | Yes | Incident |
| Can it be split into parallel independent subtasks? | Yes | Map-Reduce |
| Does it require stage gates (spec/design/qa/release)? | Yes | Pipeline |
| Is it small + low risk + single owner? | Yes | Pipeline (fast lane) |

---

## Examples

| Task | Mode |
|------|------|
| "Compare 5 repos/frameworks and extract best practices" | **Map-Reduce** |
| "Implement durable task queue + validators" | **Pipeline** |
| "Rotate production credentials / hotfix incident" | **Incident** |

---

*Last updated: 2026-02-23*
