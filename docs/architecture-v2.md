# Multi-Agent Framework Architecture v2.1

## Design Principles

| Principle | Description |
|-----------|-------------|
| **Modular** | Each component is independent, loosely coupled |
| **Provider-agnostic** | Abstract LLM layer, easy to switch providers |
| **Role-based** | Adding roles = adding config, not code |
| **Robust** | Error handling, fallbacks, observability |
| **SOP-driven** | Follow MetaGPT's Software Company workflow |

---

## Team Structure (MetaGPT-inspired)

```
┌─────────────────────────────────────────────────────────────────┐
│                     Product Manager (PM)                         │
│                  Requirement Analysis & Spec                     │
│                  Workspace: ~/pm-workspace                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    UI/UX Designer                               │
│              User Interface & Experience Design                │
│              Workspace: ~/designer-workspace                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
│   Developer 1     │ │   Developer 2     │ │   Developer N     │
│   (Frontend)      │ │   (Backend)       │ │   (Specialist)    │
│   Provider: X    │ │   Provider: Y    │ │   Provider: Z    │
└───────────────────┘ └───────────────────┘ └───────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        QA Engineer                              │
│                  Testing & Quality Assurance                    │
│                  Workspace: ~/qa-workspace                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌───────────────┐
                    │     Admin     │
                    │  (Coordinator)│
                    └───────────────┘
```

---

## Standard Operating Procedure (SOP)

```
User Request
    │
    ▼
┌─────────────────┐
│      PM        │  ← Input: User requirement
│  Requirement    │
│  Analysis       │
│  + Spec         │
└─────────────────┘
    │ Output: SPEC.md (requirements, user stories)
    ▼
┌─────────────────┐
│   UI/UX        │  ← Input: SPEC.md
│   Designer     │
│  Architecture  │
│  + UI Design   │
└─────────────────┘
    │ Output: design.md (UI mockups, component specs)
    ▼
┌─────────────────┐
│   Developers   │  ← Input: SPEC.md + design.md
│   Implement    │
│   Features    │
└─────────────────┘
    │ Output: code/ (implemented features)
    ▼
┌─────────────────┐
│      QA        │  ← Input: code/ + SPEC.md
│   Testing      │
│   & Review     │
└─────────────────┘
    │ Output: test results + bug reports
    ▼
    Done / Return to PM for revision
```

---

## Provider Flexibility

Each role can use different providers - mix and match:

```yaml
roles:
  pm:
    provider: minimax
    model: MiniMax-M2.5
    workspace: ~/pm-workspace
    
  designer:
    provider: anthropic
    model: claude-sonnet-4-20250514
    workspace: ~/designer-workspace
    
  dev_frontend:
    provider: openai
    model: gpt-5.3-codex
    workspace: ~/dev-frontend-workspace
    
  dev_backend:
    provider: openai
    model: gpt-5.3-codex
    workspace: ~/dev-backend-workspace
    
  qa:
    provider: anthropic
    model: claude-3-5-sonnet
    workspace: ~/qa-workspace
```

---

## Role Definitions

### 1. Product Manager (PM)
- **Responsibility**: Requirement analysis, spec writing, prioritization
- **Input**: User raw requirement
- **Output**: SPEC.md (detailed requirements, user stories)
- **Skills**: brainstorming, requirement analysis

### 2. UI/UX Designer
- **Responsibility**: Interface design, user experience
- **Input**: SPEC.md
- **Output**: design.md (component specs, layout, UX flows)
- **Skills**: UI design knowledge

### 3. Developers (Multiple)
- **Responsibility**: Implementation
- **Input**: SPEC.md + design.md
- **Output**: Working code
- **Types**: Frontend, Backend, Full-stack, Specialist
- **Skills**: coding-agent, language-specific

### 4. QA Engineer
- **Responsibility**: Testing, quality assurance
- **Input**: Implemented code + SPEC.md
- **Output**: Test results, bug reports
- **Skills**: testing frameworks

### 5. Admin (Orchestrator)
- **Responsibility**: Coordinate SOP, route tasks, quality gates
- **Input**: Task from user
- **Output**: Final result to user
- **Skills**: agent-team-orchestration

---

## Task Lifecycle

```
Inbox → Assigned → In Progress → Review → Done | Failed
         │           │            │        │
         ▼           ▼            ▼        ▼
      Task is    Worker is    Worker   Quality
      received   working on   finishes check
                 task         task
```

---

## Handoff Protocol

Each handoff MUST include:

1. **What was done** - Summary of work completed
2. **Where artifacts are** - Exact file paths
3. **How to verify** - Test commands, acceptance criteria
4. **Known issues** - Anything incomplete or risky
5. **What's next** - Clear next action for receiving role

---

## Directory Structure

```
multi-agent-framework/
├── config/
│   ├── providers.yaml      # LLM provider configs
│   ├── roles.yaml         # Role definitions (PM, Designer, Devs, QA)
│   ├── tasks.yaml         # Task templates
│   └── workflow.yaml      # SOP workflow definition
│
├── workspaces/             # Agent workspaces
│   ├── pm-workspace/
│   ├── designer-workspace/
│   ├── dev-frontend-workspace/
│   ├── dev-backend-workspace/
│   ├── qa-workspace/
│   └── admin-workspace/    # My workspace
│
├── artifacts/              # Shared outputs (SOP artifacts)
│   ├── tasks/
│   │   └── {task-id}/
│   │       ├── 01-requirement.md    # PM output
│   │       ├── 02-design.md         # Designer output
│   │       ├── 03-implementation/   # Dev output
│   │       ├── 04-testing.md        # QA output
│   │       └── state.json           # Task state
│   └── shared/              # Shared context (SPEC.md, etc.)
│
├── skills/                # Reusable skills
│   ├── agent-team-orchestration/
│   └── brainstorming/
│
└── logs/                  # Execution logs
    └── {date}/
        └── {task-id}.log
```

---

## Implementation Phases

### Phase 1: Infrastructure & Config (Current)
- [x] Workspaces created
- [ ] Config directory structure
- [ ] providers.yaml
- [ ] roles.yaml (full team)
- [ ] workflow.yaml (SOP)

### Phase 2: Core Framework
- Provider abstraction
- Role registry
- Task lifecycle
- Handoff protocols

### Phase 3: PM + Designer First
- Implement PM role
- Implement Designer role
- Test requirement → spec → design flow

### Phase 4: Developers
- Implement Dev roles (frontend, backend)
- Implement code generation
- Test implementation flow

### Phase 5: QA
- Implement QA role
- Testing workflow
- Full SOP integration

### Phase 6: Robustness
- Error handling
- Fallbacks
- Observability

---

## References

- MetaGPT: https://github.com/FoundationAgents/MetaGPT
- MetaGPT Paper: Code = SOP(Team)
- CrewAI: Role-based agents

---

*Last updated: 2026-02-22*
