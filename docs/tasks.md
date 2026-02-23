# Multi-Agent Framework - Task List v2.2

> Aligned with architecture-v2.2 and research.md v2.2

---

## Architecture Reference

| Document | Description |
|----------|-------------|
| [`docs/architecture-v2.md`](./architecture-v2.md) | Full v2.2 architecture spec |
| [`docs/research.md`](./research.md) | Research findings and rationale |
| [`docs/decider.md`](./decider.md) | Mode selection rubric (pipeline vs map-reduce vs incident) |
| [`docs/schemas/`](./schemas/README.md) | JSON schemas for tasks, state, events |

---

## v2.2 System Overview

```
User → Orchestrator → Workers → Blackboard → Queue → Policy Engine
```

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
| **Map-Reduce** | Parallel workers → merge → verify |
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

---

## Implementation Roadmap

### Milestone 1: Schema & Logging Foundations

| Task | Status | Description |
|------|--------|-------------|
| 1.1 | [ ] | Finalize task.json schema |
| 1.2 | [ ] | Finalize state.json schema |
| 1.3 | [ ] | Finalize envelope.json schema |
| 1.4 | [ ] | Define event log format (NDJSON) |
| 1.5 | [ ] | Implement trace_id generation |
| 1.6 | [ ] | Add basic guardrail checks |

**Deliverable**: JSON schemas in `docs/schemas/`

---

### Milestone 2: Blackboard & Queue

| Task | Status | Description |
|------|--------|-------------|
| 2.1 | [ ] | Define directory structure for artifacts |
| 2.2 | [ ] | Create blackboard.md per task |
| 2.3 | [ ] | Implement task.json creation |
| 2.4 | [ ] | Implement state.json transitions |
| 2.5 | [ ] | MVP task queue: repo-native (`artifacts/tasks/*/state.json`) + file-locking for concurrency |
| 2.6 | [ ] | Define stage transitions |
| 2.7 | [ ] | Implement orchestrator runner: create task folder, update state.json, append events.ndjson |
| 2.8 | [ ] | Implement resume-from-checkpoint: restart a stage using artifact hashes |

**Deliverable**: Working task lifecycle (repo-native). Later: optional GitHub Issues/DB-backed queue once MVP is stable.

---

### Milestone 3: Stage Validators

| Task | Status | Description |
|------|--------|-------------|
| 3.1 | [ ] | spec_validator.py - validate SPEC.md |
| 3.2 | [ ] | design_validator.py - validate design.md |
| 3.3 | [ ] | code_linter.py - validate code |
| 3.4 | [ ] | qa_checker.py - validate test results |
| 3.5 | [ ] | Integrate validators into CI |
| 3.6 | [ ] | Add regression test harness |

**Deliverable**: Automated validation at each stage

---

### Milestone 4: Observability & Governance

| Task | Status | Description |
|------|--------|-------------|
| 4.1 | [ ] | Set up NDJSON event logger |
| 4.2 | [ ] | Add trace_id to all agent actions |
| 4.3 | [ ] | Implement run summary generation |
| 4.4 | [ ] | Policy engine v1: role permissions |
| 4.5 | [ ] | Risk tier gates implementation |
| 4.6 | [ ] | (Optional) Export to LangSmith/ELK |

**Deliverable**: Full observability + basic policy enforcement

---

### Milestone 5: MCP Integration (Optional)

| Task | Status | Description |
|------|--------|-------------|
| 5.1 | [ ] | Evaluate MCP server options |
| 5.2 | [ ] | Deploy FastMCP with curated tools |
| 5.3 | [ ] | Add MCP auth (scoped tokens) |
| 5.4 | [ ] | Add MCP to tool permission matrix |
| 5.5 | [ ] | Audit tool call security |

**Deliverable**: MCP gateway for external tools

---

### Milestone 6: Agent Accounts (Discord/Telegram/Feishu)

| Task | Status | Description |
|------|--------|-------------|
| 6.1 | [ ] | Hub-and-spoke: monitor mentions |
| 6.2 | [ ] | Spawn sub-agents on mention |
| 6.3 | [ ] | Route responses back to channel |
| 6.4 | [ ] | (Future) Separate bot accounts |
| 6.5 | [ ] | Feishu integration |
| 6.6 | [ ] | Jira integration |

**Deliverable**: Agents respond in chat platforms

---

## Directory Structure (Target)

```
multi-agent-framework/
├── config/
│   ├── providers.yaml
│   ├── roles.yaml
│   ├── tasks.yaml
│   ├── workflow.yaml
│   └── policy.yaml          # NEW: Risk tiers, permissions
│
├── workspaces/
│   ├── admin-workspace/
│   ├── pm-workspace/
│   ├── designer-workspace/
│   ├── dev-workspace/
│   ├── qa-workspace/
│   └── release-workspace/   # NEW
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
├── schemas/                 # DONE
│   ├── task.json
│   ├── state.json
│   ├── envelope.json
│   └── event.json
│
├── validators/
│   ├── spec_validator.py    # TODO
│   ├── design_validator.py  # TODO
│   ├── code_linter.py       # TODO
│   └── qa_checker.py       # TODO
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
- [ ] Create first task with task.json
- [ ] Run through pipeline mode
- [ ] Test validators at each stage

---

## Related Documents

| Document | Description |
|----------|-------------|
| [`AGENTS.md`](./AGENTS.md) | Agent-friendly repository guide |
| [`.github/agents/`](.github/agents/) | Agent profile definitions |
| [`docs/research.md`](./research.md) | Full research and rationale |

---

*Last updated: 2026-02-23*
*Version: 2.2*
