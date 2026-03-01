# Multi-Agent Framework - Task List v2.2 (Revised)

> Aligned with architecture-v2.2 and research.md v2.2
> Revision goals: remove duplicate logging tasks, move minimum governance earlier, add E2E vertical slice, make concurrency + map-reduce implementable.

---

## Architecture Reference

| Document | Description |
|----------|-------------|
| [`docs/architecture-v2.md`](./architecture-v2.md) | Full v2.2 architecture spec |
| [`docs/research.md`](./research.md) | Research findings and rationale |
| [`docs/decider.md`](./decider.md) | Mode selection rubric (pipeline vs map-reduce vs incident) |
| [`docs/schemas/`](./schemas/README.md) | JSON schemas for tasks, state, events |

---

## v2.2 MVP Scope (Frozen)

This section defines exactly what "v2.2 MVP" includes. All other features are explicitly deferred.

### MVP Includes (Locked)

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

### Explicitly Deferred (Not in MVP)

| Feature | Reason |
|---------|--------|
| Map-reduce mechanics | Deferred to v2.3 |
| MCP integration | Optional; external tools only; deferred to v2.3 |
| Incident mode | Deferred to v2.3 (depends on stronger policy + approvals UX) |
| Dashboards / exports | Nice-to-have; deferred |
| LangSmith/ELK export | Optional; deferred |
| Chat platforms (Discord/Telegram/Feishu) | Deferred to v2.4+ (scope expansion risk) |

### Why Freeze Scope?

Prevents thrash and scope creep. Get a working Pipeline E2E loop first.

---

## v2.2 System Overview (Conceptual)

**Orchestration loop**:
User → Orchestrator → (Policy checks) → Workers → (Artifacts + Logs) → Orchestrator

**Shared stores**:
- Blackboard = shared task content & decisions & artifacts
- Queue/State = workflow control & assignments & transitions

---

## Team Roles

| Role | Purpose | Tools | Workspace |
|------|---------|-------|-----------|
| **Orchestrator** (Admin) | Coordination, gates, merging | All | admin-workspace |
| **PM** | Requirements → Spec | Docs, GitHub Issues | pm-workspace |
| **Designer** | Spec → Design | Docs, Figma API | designer-workspace |
| **Dev** | Implementation | Git, Tests, Browser | dev-workspace |
| **QA** | Testing → Quality | Tests, Security | qa-workspace |
| **Release** | Deployment | CI/CD | release-workspace |

---

## Collaboration Modes

| Mode | When to Use |
|------|-------------|
| **Pipeline** (default) | PM → Design → Dev → QA → Release |
| **Map-Reduce** | Parallel workers → reduce/merge → verify |
| **Incident** | Triage → minimal tools → human approval |

---

## Risk Tiers

| Tier | What | Approval |
|------|------|----------|
| **Low** | Read-only, docs, research | Auto |
| **Medium** | Code + tests + PRs | Auto |
| **High** | Dep upgrades, infra, deploy | Human |
| **Critical** | Production incidents, secrets | Multi-approval |

---

## GitHub Workflow (Per Deliverable)

| Stage | Branch | Action |
|-------|--------|--------|
| Spec | `feature/{id}/spec` | Create → PR → Review → Merge |
| Design | `feature/{id}/design` | Create → PR → Review → Merge |
| Implementation | `feature/{id}/impl` | Create → PR → Review → Merge |
| Test | `feature/{id}/test` | Create → PR → Review → Merge |

**Rule**: No direct commits to main. Every change goes through PR review.

> Note (practical): consider a "low-risk fast lane" later (still PR-based) for tiny doc-only changes to avoid 4-PR overhead.

---

## Implementation Roadmap

### Milestone 1: Schema & Logging Foundations (Plumbing)

| Task | Status | Description |
|------|--------|-------------|
| 1.1 | [ ] | Finalize task.json schema |
| 1.2 | [ ] | Finalize state.json schema |
| 1.3 | [ ] | Finalize envelope.json schema |
| 1.4 | [ ] | Finalize event log format (NDJSON) + event.json schema |
| 1.5 | [ ] | Implement trace_id generation + propagation |
| 1.6 | [ ] | Implement NDJSON event logger (append-only) |
| 1.7 | [ ] | Define + implement redaction rules for logs (no secrets) |
| 1.8 | [ ] | Add basic guardrail checks (budget caps, max retries, timeout defaults) |

**Deliverable**: JSON schemas in `docs/schemas/` + working `events.ndjson` writer + trace propagation.

---

### Milestone 2: Durable Lifecycle MVP (Blackboard + Queue + Minimum Governance)

| Task | Status | Description |
|------|--------|-------------|
| 2.1 | [ ] | Define directory structure for artifacts (canonical layout) |
| 2.2 | [ ] | Create blackboard.md + decisions.md per task |
| 2.3 | [ ] | Implement task.json creation (new task bootstrap) |
| 2.4 | [ ] | Implement state.json transitions (stage/status/assigned/retries/next) |
| 2.5 | [ ] | MVP task queue: repo-native (`artifacts/tasks/*/state.json`) |
| 2.6 | [ ] | Concurrency protocol: file-lock acquisition, atomic write, stale lock recovery |
| 2.7 | [ ] | Define stage transitions formally (allowed edges + fail/retry/escalate) |
| 2.8 | [ ] | Implement orchestrator runner: create task folder, update state.json, append events.ndjson |
| 2.9 | [ ] | Implement resume-from-checkpoint: restart stage using artifact hashes + idempotency rules |
| 2.10 | [ ] | Policy engine v1 (minimum): role permissions + tool allow/deny + require-approval hooks |
| 2.11 | [ ] | Risk tier gates v1: low/medium auto; high/critical block unless approved |
| 2.12 | [ ] | Implement Mode Router v1 (uses `docs/decider.md` rubric) |
| 2.13 | [ ] | **E2E vertical slice demo**: run Pipeline end-to-end on a tiny task and produce artifacts+logs |

**Deliverable**: Working task lifecycle (repo-native), resumable stages, minimum enforcement, and an E2E run proving the loop.

---

### Milestone 3: Map-Reduce + Stage Validators (Quality & Parallelism)

#### 3A — Map-Reduce Mechanics

| Task | Status | Description |
|------|--------|-------------|
| 3.1 | [ ] | Map-Reduce worker registration: how workers publish outputs to blackboard |
| 3.2 | [ ] | Reduce strategy v1: merge policy (best-of-n / vote / verifier) |
| 3.3 | [ ] | Verifier role + criteria for map-reduce outputs |
| 3.4 | [ ] | Conflict resolution rules (disagreement handling + escalation to human) |

#### 3B — Validators

| Task | Status | Description |
|------|--------|-------------|
| 3.5 | [ ] | spec_validator.py - validate SPEC.md + acceptance criteria |
| 3.6 | [ ] | design_validator.py - validate design.md covers requirements + states |
| 3.7 | [ ] | code_linter.py - validate code formatting/static checks |
| 3.8 | [ ] | qa_checker.py - validate test results + required evidence |
| 3.9 | [ ] | Integrate validators into CI (PR checks) |
| 3.10 | [ ] | Add regression test harness (golden tasks + expected artifacts) |

**Deliverable**: Parallel mode is real (reduce+verify exists) and stage gates are enforced.

---

### Milestone 4: Observability & Governance (Upgrades, not Plumbing)

| Task | Status | Description |
|------|--------|-------------|
| 4.1 | [ ] | Implement run summary generation (logs/summary.md) |
| 4.2 | [ ] | Add audit views: per-task timeline + per-agent actions (from events.ndjson) |
| 4.3 | [ ] | Expand policy engine: richer constraints (file/path restrictions, branch rules, rate limits) |
| 4.4 | [ ] | Human approval workflow UX (how approvals are recorded + referenced) |
| 4.5 | [ ] | (Optional) Export to LangSmith/ELK |
| 4.6 | [ ] | Threat model + red-team tests (prompt injection, tool abuse, artifact poisoning) |

**Deliverable**: Clear audits + stronger governance + optional external observability.

---

### Milestone 5: MCP Integration (Optional, External Tools)

| Task | Status | Description |
|------|--------|-------------|
| 5.1 | [ ] | Evaluate MCP server options |
| 5.2 | [ ] | Deploy FastMCP with curated external tools (search/tickets/docs/etc.) |
| 5.3 | [ ] | Add MCP auth (scoped tokens) |
| 5.4 | [ ] | Add MCP to tool permission matrix (policy enforcement) |
| 5.5 | [ ] | Audit MCP tool call security (allowlist servers, logging, redaction) |

**Deliverable**: MCP gateway for external tools without breaking core repo-native workflow.

---

### Milestone 6: Agent Accounts (Discord/Telegram/Feishu) (Post-MVP)

| Task | Status | Description |
|------|--------|-------------|
| 6.1 | [ ] | Hub-and-spoke: monitor mentions |
| 6.2 | [ ] | Spawn sub-agents on mention (bounded) |
| 6.3 | [ ] | Route responses back to channel |
| 6.4 | [ ] | (Future) Separate bot accounts |
| 6.5 | [ ] | Feishu integration |
| 6.6 | [ ] | Jira integration |

**Deliverable**: Agents respond in chat platforms (after the core system is stable).

---

## Directory Structure (Target)

```
multi-agent-framework/
├── config/
│   ├── providers.yaml
│   ├── roles.yaml
│   ├── tasks.yaml
│   ├── workflow.yaml
│   └── policy.yaml # Risk tiers, permissions, approval rules
│
├── workspaces/
│   ├── admin-workspace/
│   ├── pm-workspace/
│   ├── designer-workspace/
│   ├── dev-workspace/
│   ├── qa-workspace/
│   └── release-workspace/
│
├── artifacts/
│   └── tasks/
│       └── {task-id}/
│           ├── task.json
│           ├── state.json
│           ├── blackboard.md
│           ├── decisions.md
│           ├── artifacts/
│           │   ├── spec/
│           │   ├── design/
│           │   ├── impl/
│           │   ├── qa/
│           │   └── release/
│           └── logs/
│               ├── events.ndjson
│               └── summary.md
│
├── schemas/
│   ├── task.json
│   ├── state.json
│   ├── envelope.json
│   └── event.json
│
├── validators/
│   ├── spec_validator.py
│   ├── design_validator.py
│   ├── code_linter.py
│   └── qa_checker.py
│
├── skills/
│   ├── agent-team-orchestration/
│   └── brainstorming/
│
└── logs/
```

---

## Agent Profiles

Each agent defined in `.github/agents/`:

| Agent | File | Status |
|-------|------|--------|
| PM | pm-agent.md | ✅ Existing |
| Dev | dev-agent.md | ✅ Existing |
| QA | qa-agent.md | ✅ Existing |
| Designer | designer-agent.md | [ ] To create |
| Release | release-agent.md | [ ] To create |

Each agent has:
- Role and responsibilities
- Tool permissions (per risk tier)
- Workspace boundaries
- Commands they can run
- What to NEVER do

---

## Quick Start Checklist

- [ ] Review architecture-v2.md
- [ ] Review schemas in docs/schemas/
- [ ] Set up workspaces (or use existing)
- [ ] Run Pipeline mode end-to-end (Milestone 2.13)
- [ ] Enable CI validators (Milestone 3)
- [ ] Add map-reduce reducer + verifier (Milestone 3A)

---

*Last updated: 2026-02-23*
*Version: 2.2 (Revised)*
