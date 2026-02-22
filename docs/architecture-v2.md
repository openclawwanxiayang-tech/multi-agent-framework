# Multi-Agent Framework Architecture v2

## Design Principles

| Principle | Description |
|-----------|-------------|
| **Modular** | Each component is independent, loosely coupled |
| **Provider-agnostic** | Abstract LLM layer, easy to switch providers |
| **Role-based** | Adding roles = adding config, not code |
| **Robust** | Error handling, fallbacks, observability |
| **Observable** | Logs, metrics, traceability |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Admin (Orchestrator)                      │
│                    (Minimax M2.5 - default)                     │
│                                                                  │
│  - Task routing & coordination                                   │
│  - Quality gates & approval                                     │
│  - Provider selection                                           │
└─────────────────────────────────────────────────────────────────┘
         │                    │                     │
         ▼                    ▼                     ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   Role: PM      │  │  Role: Dev      │  │  Role: [NEW]    │
│   Provider: X   │  │  Provider: Y    │  │  Provider: Z    │
│   Workspace: ~/ │  │  Workspace: ~/ │  │  Workspace: ~/  │
│     pm-workspace│  │  codex-workspace│  │    custom-ws    │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                    │                     │
         └────────────────────┴─────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Shared Context   │
                    │  (Artifacts,     │
                    │   State, Memory) │
                    └──────────────────┘
```

---

## Core Components

### 1. Provider Abstraction Layer

```yaml
# config/providers.yaml
providers:
  openai:
    enabled: true
    default_model: gpt-5.3-codex
    fallback: gpt-4o
    
  anthropic:
    enabled: true
    default_model: claude-sonnet-4-20250514
    fallback: claude-3-5-sonnet
    
  minimax:
    enabled: true
    default_model: MiniMax-M2.5
    fallback: MiniMax-M2.1
    
  ollama:
    enabled: false
    default_model: qwen2.5-coder
```

**Why**: Switch providers without changing agent code

---

### 2. Role Registry

```yaml
# config/roles.yaml
roles:
  pm:
    name: Product Manager
    description: Creates specs, plans tasks, defines requirements
    default_provider: minimax
    default_model: MiniMax-M2.5
    workspace: ~/pm-workspace
    tools:
      - file_read
      - file_write
      - github_issues
    skills:
      - brainstorming
    
  dev:
    name: Developer
    description: Writes code, implements features
    default_provider: openai
    default_model: gpt-5.3-codex
    workspace: ~/codex-workspace
    tools:
      - file_read
      - file_write
      - exec
      - github
      - browser
    skills:
      - coding-agent
      
  reviewer:
    name: Code Reviewer
    description: Reviews code, validates quality
    default_provider: anthropic
    default_model: claude-sonnet-4-20250514
    workspace: ~/reviewer-workspace
    tools:
      - file_read
      - github_pr
    skills: []

  # Adding new role = just add config
  researcher:
    name: Researcher
    description: Conducts research, gathers information
    default_provider: minimax
    default_model: MiniMax-M2.5
    workspace: ~/research-workspace
    tools:
      - web_search
      - web_fetch
    skills: []
```

---

### 3. Task Lifecycle (from agent-team-orchestration)

```
Inbox → Assigned → In Progress → Review → Done | Failed
```

Each transition includes:
- Timestamp
- Actor (who)
- Artifact path
- Notes

---

### 4. Handoff Protocol

Every handoff includes:

1. **What was done** - summary
2. **Where artifacts are** - exact paths
3. **How to verify** - test commands, acceptance criteria
4. **Known issues** - anything incomplete/risky
5. **What's next** - clear next action

---

## Directory Structure

```
multi-agent-framework/
├── config/
│   ├── providers.yaml      # LLM provider configs
│   ├── roles.yaml         # Role definitions
│   ├── tasks.yaml         # Task templates
│   └── workflow.yaml      # Workflow definitions
│
├── workspaces/             # Agent workspaces
│   ├── pm-workspace/
│   ├── codex-workspace/
│   ├── reviewer-workspace/
│   └── [new-role]-workspace/
│
├── artifacts/              # Shared outputs
│   ├── tasks/
│   │   └── {task-id}/
│   │       ├── brief.md
│   │       ├── spec.md
│   │       ├── implementation.md
│   │       └── review.md
│   └── state.json         # Global state
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

## Key Features

### Provider Switching
```yaml
# To switch provider for a role:
roles:
  dev:
    provider: anthropic   # Change from openai to anthropic
    model: claude-sonnet-4-20250514
```

### Adding New Role
```yaml
# Just add to roles.yaml:
roles:
  new_role:
    name: My New Role
    workspace: ~/new-workspace
    # ... rest of config
```

### Fallback机制
```yaml
# If primary provider fails, auto-fallback
providers:
  openai:
    fallback: anthropic  # Chain fallback
```

---

## Implementation Phases

### Phase 1: Infrastructure (Current)
- [x] Create workspaces
- [x] Document agent profiles
- [ ] Create config directory structure
- [ ] Define providers.yaml
- [ ] Define roles.yaml

### Phase 2: Core Framework
- [ ] Build provider abstraction
- [ ] Implement role registry
- [ ] Create task lifecycle manager
- [ ] Set up handoff protocols

### Phase 3: Agent Implementation
- [ ] Implement PM agent
- [ ] Implement Dev agent
- [ ] Implement Reviewer
- [ ] Test inter-agent communication

### Phase 4: Robustness
- [ ] Add error handling
- [ ] Implement fallbacks
- [ ] Add logging/observability
- [ ] Create monitoring dashboard

### Phase 5: Extension
- [ ] Add more roles
- [ ] Create custom skills
- [ ] Build visualization

---

## References

- LangGraph: Graph-based orchestration
- VoltAgent: Modular, pluggable architecture
- Databricks: Modular engineering for AI agents
- Google ADK: Provider abstraction patterns

---

*Last updated: 2026-02-22*
