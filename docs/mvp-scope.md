# v2.2 MVP Scope (Frozen)

This document defines exactly what "v2.2 MVP" includes. All other features are explicitly deferred.

---

## MVP Includes (Locked)

| Feature | Status |
|---------|--------|
| **Pipeline mode only** | ✅ Default and only mode for MVP |
| **Repo-native queue** | ✅ `artifacts/tasks/*/state.json` file-based |
| **events.ndjson logging** | ✅ Structured event log with `trace_id` |
| **Policy engine v1** | ✅ Enforced allow/deny/require-approval checks |
| **E2E vertical slice** | ✅ One end-to-end run proving the loop |
| **Schemas frozen + versioned** | ✅ `task.json/state.json/envelope.json/event.json` are the contract |
| **Stage machine semantics defined** | ✅ Allowed transitions + retry/escalation + checkpoint/resume rules |
| **Concurrency protocol** | ✅ File-lock + atomic write + stale lock recovery for repo-native queue |
| **Startup recovery policy** | ✅ Automatic resume on crash/restart with checkpoint verification |

### Notes on "Policy engine v1"

Policy engine v1 is considered "done" only if it is **enforced** (not just stubs):
- Evaluated **inside the orchestrator runner** before any tool call / stage transition.
- Default behavior: **deny** when a role/tool is not explicitly allowed.
- High/Critical actions must be **blocked** unless an approval record exists and is referenced in the task logs.

---

## MVP Acceptance Criteria (Must Pass)

The MVP is complete only when all of the following pass:

1. **Task bootstrap works**
   - Creating a new task produces: `task.json`, `state.json`, `blackboard.md`, and `logs/events.ndjson`.

2. **Pipeline E2E run succeeds**
   - At minimum: **PM → Dev → QA** run end-to-end.
   - Artifacts are created under `artifacts/spec/`, `artifacts/impl/`, `artifacts/qa/`.

3. **Validators gate transitions (minimum viable)**
   - A stage cannot advance if its validator fails.
   - Validator results are written to `events.ndjson`.

4. **Policy enforcement is real**
   - A deliberately forbidden tool action is **blocked**.
   - The denial is recorded in `events.ndjson` with role/tool/risk tier context.

5. **Durability / resume works**
   - Kill the run mid-stage → resume from checkpoint → finish successfully.
   - Artifact hashes referenced in state checkpoints remain consistent (or changes are explicitly recorded as a new checkpoint).

6. **Startup recovery works**
   - Orchestrator crashes → restarts → automatically scans and recovers unfinished tasks.
   - Crash/restart demo test passes: start pipeline → kill orchestrator mid-stage → restart → resumes and completes.
   - Policy blocks a high-risk action without approval.

---

## Explicitly Deferred (Not in v2.2 MVP)

| Feature | Reason |
|---------|--------|
| Map-reduce mechanics | Deferred to v2.3 |
| MCP integration | Optional; external tools only; deferred to v2.3 |
| Incident mode | Deferred to v2.3 (depends on stronger policy + approvals UX) |
| Dashboards / exports | Nice-to-have; deferred |
| LangSmith/ELK export | Optional; deferred |
| Chat platforms (Discord/Telegram/Feishu) | Deferred to v2.4+ (scope expansion risk) |

---

## Why Freeze Scope?

Prevents thrash and scope creep. Get a working Pipeline E2E loop first:
- durable lifecycle
- enforced policy
- auditable logs
- resumable execution
