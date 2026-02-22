# Multi-Agent Framework - Task List

## Design Principles

| Principle | Description |
|-----------|-------------|
| **Modular** | Each component is independent, loosely coupled |
| **Provider-agnostic** | Abstract LLM layer, easy to switch providers |
| **Role-based** | Adding roles = adding config, not code |
| **Robust** | Error handling, fallbacks, observability |

---

## Architecture: See `docs/architecture-v2.md`

---

## Phase 1: Infrastructure & Config

### 1.1 Workspaces (DONE ✅)
- [x] Create ~/codex-workspace
- [x] Create ~/pm-workspace

### 1.2 Configuration System
- [ ] Create `config/` directory structure
- [ ] Create `config/providers.yaml` - LLM provider configs
- [ ] Create `config/roles.yaml` - Role definitions
- [ ] Create `config/tasks.yaml` - Task templates
- [ ] Create `config/workflow.yaml` - Workflow definitions

### 1.3 Shared Artifacts
- [ ] Create `artifacts/tasks/` - Task outputs
- [ ] Create `artifacts/state.json` - Global state
- [ ] Create `logs/` - Execution logs

---

## Phase 2: Core Framework

### 2.1 Provider Abstraction
- [ ] Build provider config loader
- [ ] Implement fallback chain
- [ ] Test provider switching

### 2.2 Role Registry
- [ ] Build role config loader
- [ ] Implement workspace isolation
- [ ] Add role validation

### 2.3 Task Lifecycle Manager
- [ ] Implement task states (Inbox → Review → Done)
- [ ] Add state transitions with timestamps
- [ ] Create artifact tracking

### 2.4 Handoff Protocol
- [ ] Define handoff message format
- [ ] Implement artifact path tracking
- [ ] Add verification steps

---

## Phase 3: Agent Implementation

### 3.1 PM Agent
- [ ] Configure PM role in roles.yaml
- [ ] Test spawning PM agent
- [ ] Test spec generation

### 3.2 Developer Agent
- [ ] Configure Dev role in roles.yaml
- [ ] Test spawning Dev agent
- [ ] Test code generation

### 3.3 Reviewer Agent
- [ ] Configure Reviewer role
- [ ] Implement review workflow

### 3.4 Inter-Agent Communication
- [ ] Test PM → Dev handoff
- [ ] Test Dev → Reviewer handoff
- [ ] Test full pipeline

---

## Phase 4: Robustness

### 4.1 Error Handling
- [ ] Add timeout handling
- [ ] Implement retry logic
- [ ] Add graceful degradation

### 4.2 Fallbacks
- [ ] Provider fallback chain
- [ ] Model fallback
- [ ] Workspace fallback

### 4.3 Observability
- [ ] Add structured logging
- [ ] Create execution traces
- [ ] Build monitoring

---

## Phase 5: Extension

### 5.1 New Roles
- [ ] Add Researcher role (easy - just config)
- [ ] Add any custom roles as needed

### 5.2 Custom Skills
- [ ] Build reusable skills
- [ ] Add skill registry

### 5.3 Visualization
- [ ] Task flow visualization
- [ ] Agent status dashboard

---

## Key Files

| File | Purpose |
|------|---------|
| `config/providers.yaml` | LLM provider configs |
| `config/roles.yaml` | Role definitions |
| `artifacts/tasks/{id}/` | Task outputs |
| `skills/` | Reusable skills |

---

*Status: Ready for Phase 1.2* - *Start: Config System*
