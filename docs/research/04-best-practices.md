# Best Practices: Consolidated Recommendations

Cross-framework best practices for building robust multi-agent systems.

---

## 1. Agent Design

### Role-Based Definition

Each agent should have:

| Element | Description | Example |
|---------|-------------|---------|
| **Role** | Function and expertise | "Software Developer" |
| **Goal** | Individual objective | "Write clean, working code" |
| **Backstory** | Context and personality | "Senior dev who cares about quality" |
| **Tools** | Available capabilities | GitHub, file ops, browser |
| **Constraints** | Boundaries | "Never commit to main" |

### Workspace Isolation

```
workspaces/
├── admin-workspace/      # Me - orchestration
├── pm-workspace/        # PM agent
├── designer-workspace/  # Designer agent
├── dev-*-workspace/     # Developer agents
└── qa-workspace/        # QA agent
```

**Principle**: Each agent operates in its own workspace - no crossing boundaries without explicit handoff.

---

## 2. Workflow Design

### SOP-Driven Approach

Follow MetaGPT's "Code = SOP(Team)" philosophy:

```
User Request
    │
    ▼
┌─────────────────┐
│      PM         │ → Spec output
│   Requirements  │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   Designer      │ → Design output
│   UI/UX         │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   Developer     │ → Code output
│   Implementation│
└─────────────────┘
    │
    ▼
┌─────────────────┐
│      QA         │ → Test results
│   Testing       │
└─────────────────┘
    │
    ▼
      Done
```

### Sequential Gates

Each stage should have explicit approval:

| Stage | Gatekeeper | Purpose |
|-------|------------|---------|
| Spec → Design | Admin | Feasibility check |
| Design → Code | Admin + PM | Scope clarity |
| Code → QA | Admin + QA | Quality check |
| QA → Merge | Admin | Final approval |

---

## 3. Task Definition

### Task Template

```markdown
## Task: [title]
### Role: [Developer/PM/Designer/QA]
### Goal: [specific objective]
### Context: [background info]
### Input: [files/data to work with]
### Expected Output: [what success looks like]
### Constraints: [limitations, deadline]
### Tools: [available tools]
```

### Per-Task Artifacts

Each task should produce:

```
artifacts/tasks/{task-id}/
├── 01-requirement.md    # PM output (SPEC.md)
├── 02-design.md         # Designer output
├── 03-implementation/  # Dev output (code)
├── 04-testing.md       # QA output (test results)
└── state.json          # Task state
```

---

## 4. Handoff Protocol

### Required Handoff Elements

Every handoff MUST include:

1. **What was done** - Summary of work completed
2. **Where artifacts are** - Exact file paths
3. **How to verify** - Test commands, acceptance criteria
4. **Known issues** - Anything incomplete or risky
5. **What's next** - Clear next action

### Handoff Contract Schema

```yaml
handoff:
  from: AgentA
  to: AgentB
  input:
    required:
      - artifact_path
      - summary
    optional:
      - context_notes
  output:
    expected_format: markdown
    required_sections:
      - summary
      - artifacts
  failure_policy:
    max_retries: 2
    escalate_to: admin
```

---

## 5. Error Handling & Autonomy Bounds

### Bounded Autonomy

| Parameter | Recommended | Description |
|-----------|-------------|-------------|
| `max_iterations` | 20 | Max attempts before final answer |
| `max_tool_calls` | 50 | Max tool invocations per task |
| `max_retries` | 2 | Retries on error |
| `timeout` | 300s | Task timeout |

### Approval Gates

Always require human approval before:

- Merging code to main
- Deploying changes
- Accessing external services
- Modifying configuration

---

## 6. State Management

### Persistent State

Never rely on ephemeral chat context. Use:

| State Type | Storage | Use Case |
|------------|---------|----------|
| Task state | JSON file | Current progress, artifacts |
| Session state | Markdown | Agent context |
| History | Git log | Traceability |

### Checkpoint Strategy

For long-running tasks:
1. Save state after each stage
2. Enable resume from checkpoint
3. Log failure points for debugging

---

## 7. Observability

### Required Logging

| Log Type | What to Track |
|----------|---------------|
| **Task logs** | Start time, end time, duration |
| **Agent logs** | Which agent, what task, result |
| **Tool logs** | Tool name, inputs, outputs |
| **Error logs** | Error type, stack trace, context |

### Metrics to Track

- Task completion rate
- Average task duration
- Failure rate by agent
- Token usage by agent
- Retry frequency

---

## 8. Git Workflow

### Branch Strategy

```
main (protected)
    │
    ├── feature/{task-id}/spec      → PM spec
    ├── feature/{task-id}/design    → Designer design  
    ├── feature/{task-id}/impl       → Developer code
    └── feature/{task-id}/test       → QA results
```

### PR Requirements

Every PR must:
- [ ] Pass automated checks (tests, lint)
- [ ] Have at least 1 approval
- [ ] Pass review before merge
- [ ] Include descriptive summary
- [ ] Link to task/artifacts

### PR Title Format

```
[Type] Task Name

Examples:
[Spec] User authentication system
[Impl] Add login API endpoint
[Test] Login flow test coverage
```

---

## 9. Quality Gates

### Before Moving to Next Stage

| Stage | Quality Check |
|-------|---------------|
| Spec | Completeness, feasibility, clarity |
| Design | Usability, consistency, completeness |
| Code | Tests pass, lint clean, follows spec |
| Test | Coverage adequate, no critical bugs |

### Review Checklist

```markdown
## Review: [Stage]
### Completeness
- [ ] All requirements addressed
- [ ] All artifacts present

### Quality
- [ ] Follows best practices
- [ ] No critical issues

### Next Steps
- [ ] Ready to proceed / Needs revision
```

---

## 10. Security & Access Control

### Principle of Least Privilege

| Agent | Workspace | Git Access | External Access |
|-------|-----------|------------|-----------------|
| Admin | All | Full | Yes |
| PM | pm-workspace | Read spec repos | Limited |
| Designer | designer-workspace | Read spec repos | Limited |
| Dev | dev-workspace | Feature branches | Build tools |
| QA | qa-workspace | Read + test | Test tools |

### Sensitive Operations

Always require Admin approval for:
- API key changes
- Provider configuration changes
- Workspace boundary crossings
- External service calls

---

## Quick Reference Card

| Do | Don't |
|----|-------|
| ✅ Define clear roles | ❌ Ambiguous agent responsibilities |
| ✅ Use SOPs for workflows | ❌ Ad-hoc execution |
| ✅ Persist state | ❌ Rely on ephemeral context |
| ✅ Set autonomy bounds | ❌ Unlimited tool calls |
| ✅ Human approval gates | ❌ Fully autonomous |
| ✅ Log everything | ❌ No observability |
| ✅ Separate workspaces | ❌ Shared context pollution |
| ✅ Use structured handoffs | ❌ Informal handoffs |

---

*Last updated: 2026-02-23*
