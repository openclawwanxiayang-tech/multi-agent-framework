# Multi-Agent Collaboration Architecture v2.2

> OpenClaw-Orchestrated Swarm Architecture

**Last Updated**: 2026-02-23

---

## 1. Goals and Non-Goals

### Goals

| Goal | Description |
|------|-------------|
| **SOP-driven** | Standard Operating Procedures for agent collaboration |
| **Auditable** | Full trace of decisions and actions |
| **Replayable** | Checkpoints enable retry/resume |
| **Safe** | Risk tiers, approvals, policy enforcement |
| **Multi-provider** | Support OpenAI/Claude/Minimax without rewriting tool glue |
| **Future-proof** | Clean path to OpenClaw Agent Teams |

### Non-Goals (for v2.2)

| Non-Goal | Reason |
|----------|--------|
| Real-time peer chat between sibling agents | Will emulate with blackboard + queue until Agent Teams lands |
| Fully autonomous production changes without gates | Always require human approval for risky actions |

---

## 2. High-Level System Model

```
┌─────────────────────────────────────────────────────────────────┐
│                      Orchestrator (Admin/Director)              │
│  • Owns workflow graph / state machine                          │
│  • Creates/assigns subtasks                                     │
│  • Enforces policy gates (risk tiers, approvals)               │
│  • Merges outputs + final delivery                              │
│  • Minimal tool execution (routing + verification > heavy use)  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Worker Agents (Specialists)                  │
│  • PM, Designer, Dev, QA, Security, Researcher, Release         │
│  • Narrow tool scopes and budgets                              │
│  • Produce artifacts in standard format                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Blackboard (Shared Workspace)                │
│  • "Team memory": artifacts + decisions + summaries           │
│  • Single source of truth for a task                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Task Queue / State Machine                  │
│  • Tracks status, dependencies, assignments, retries          │
│  • Makes system durable and resumable                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Policy Engine                              │
│  • "Who can do what" + risk-tier gates                        │
│  • Preflight + postflight validation hooks                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Collaboration Modes

### Mode A — Pipeline SOP (Default)

```
PM → Design → Dev → QA → Release
```

**Best for**: Product work where quality matters.

### Mode B — Map-Reduce Swarm

```
Director
   │
   ├──→ Worker 1 (research)
   ├──→ Worker 2 (code spike)
   ├──→ Worker 3 (tests)
   └──→ Worker N ...
         │
         ▼
    Director merges outputs
         │
         ▼
    Verifier confirms
```

**Best for**: Exploration, research, large refactors.

### Mode C — Incident Mode

```
Triage → Minimal tool permissions → Mandatory human approval
```

**Best for**: Production incidents / risky actions.

---

## 4. Core Components

### 4.1 Orchestrator (Admin/Director)

| Capability | Description |
|------------|-------------|
| Workflow graph | Define task stages and transitions |
| State machine | Track task status through lifecycle |
| Task creation | Spawn subtasks for workers |
| Policy enforcement | Apply risk tiers, approval gates |
| Output merging | Combine worker artifacts |
| Delivery | Return final result to user |

### 4.2 Worker Agents

| Role | Tools | Workspace |
|------|-------|-----------|
| PM | GitHub Issues, Docs | pm-workspace |
| Designer | Figma API, Docs | designer-workspace |
| Dev | Git, Tests, Browser | dev-workspace |
| QA | Tests, Security scans | qa-workspace |
| Security | SAST, dependency scans | security-workspace |
| Release | CI/CD, Deploy | release-workspace |

### 4.3 Blackboard (Shared Task Workspace)

The "team memory" - single source of truth per task.

### 4.4 Task Queue

Tracks status, dependencies, assignments, retries for durability.

### 4.5 Policy Engine

| Function | Description |
|----------|-------------|
| Role permissions | Who can do what |
| Risk tiers | Low/Medium/High/Critical gates |
| Preflight checks | Input validation before execution |
| Postflight checks | Output validation after execution |

---

## 5. Risk Tiers & Permissions

### 5.1 Risk Tiers

| Tier | Description | Permissions |
|------|-------------|-------------|
| **Low** | Read-only, docs, research, code generation in sandbox | Basic tools |
| **Medium** | Code changes + tests + PRs allowed | No secrets changes |
| **High** | Dependency upgrades, infra, deployments | Require human approval |
| **Critical** | Production incidents, credential actions | Multi-approval + incident mode |

### 5.2 Tool Permission Matrix

| Role | Git Write | Run Tests | Web Search | Secrets | Deploy |
|------|-----------|-----------|------------|---------|--------|
| PM | ✗ | ✗ | ✓ | ✗ | ✗ |
| Designer | ✗ | ✗ | ✓ | ✗ | ✗ |
| Dev | ✓ | ✓ | ✓ | ✗ | ✗ |
| QA | ✗ | ✓ | ✓ | ✗ | ✗ |
| Release | ✓ | ✓ | ✓ | ✗ | ✓ (gate) |

---

## 6. Guardrail Hooks

### Preflight (Before Execution)
- Validate input
- Pick collaboration mode
- Set budgets (max_tool_calls, max_tokens)
- Sanitize prompts

### During (Tool Call Policy)
- Deny prohibited calls
- Ask for approval on sensitive calls
- Rate-limit expensive operations

### Postflight (After Execution)
- Artifact validators
- Security checks
- Regression evaluations

---

## 7. Observability

### Required

| Metric | Description |
|--------|-------------|
| **Trace ID** | Per task + per stage |
| **Event log** | Structured NDJSON |
| **Run summary** | What happened, costs, failures, decisions |
| **Checkpoints** | Artifact hashes in state.json |

### Nice-to-Have (v2.3+)
- UI dashboard showing task queue, stage status
- Cost graphs
- "Time travel" re-run from checkpoint

---

## 8. MCP Stance

### v2.2 Recommendation

| Tool Type | Approach |
|-----------|----------|
| Internal tools | Keep native (git, filesystem, tests, local analyzers) |
| External services | Add MCP as optional tool bus (search, ticketing, cloud actions) |

**When MCP pays off**: Multi-provider, many tools, many agents, frequent tool changes.

---

## 9. Upgrade Path to OpenClaw Agent Teams

When Agent Teams is available:

1. Replace "blackboard polling" with team shared state + messaging
2. Keep same artifacts/state/event formats (no workflow rewrite)
3. Add "agent can spawn subtasks" rules via policy engine

---

## 10. Implementation Checklist

- [ ] Finalize schemas: task.json, state.json, envelope schemas
- [ ] Blackboard + queue: directory conventions + stage transitions
- [ ] Validators: spec/design/code/qa minimal checks
- [ ] Event log: NDJSON writer + trace_id propagation
- [ ] Policy engine v1: role permissions + risk tier gates
- [ ] (Optional) MCP gateway for external tools

---

## 11. Directory Structure

```
multi-agent-framework/
├── config/
│   ├── providers.yaml      # LLM provider configs
│   ├── roles.yaml         # Role definitions
│   ├── tasks.yaml         # Task templates
│   ├── workflow.yaml      # SOP workflow
│   └── policy.yaml        # Risk tiers, permissions
│
├── workspaces/            # Agent workspaces
│   ├── pm-workspace/
│   ├── designer-workspace/
│   ├── dev-workspace/
│   ├── qa-workspace/
│   └── admin-workspace/
│
├── artifacts/             # Blackboard (task artifacts)
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
├── schemas/               # JSON schemas
│   ├── task.json
│   ├── state.json
│   └── envelope.json
│
├── validators/            # Stage validators
│   ├── spec_validator.py
│   ├── design_validator.py
│   ├── code_linter.py
│   └── qa_checker.py
│
├── skills/
│   ├── agent-team-orchestration/
│   └── brainstorming/
│
└── logs/                  # Execution logs
    └── {date}/
```

---

## References

- OpenClaw: https://github.com/openclaw/openclaw
- MetaGPT: https://github.com/FoundationAgents/MetaGPT
- CrewAI: https://github.com/crewAIInc/crewAI
- Research: [./research.md](./research.md)

---

*Last updated: 2026-02-23*
