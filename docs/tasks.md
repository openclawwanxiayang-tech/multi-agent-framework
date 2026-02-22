# Multi-Agent Framework - Task List

## Design Principles

| Principle | Description |
|-----------|-------------|
| **Modular** | Each component is independent, loosely coupled |
| **Provider-agnostic** | Abstract LLM layer, easy to switch providers |
| **Role-based** | Adding roles = adding config, not code |
| **SOP-driven** | Follow MetaGPT's Software Company workflow |

---

## Architecture: See `docs/architecture-v2.md`

---

## Team (MetaGPT-inspired)

| Role | Purpose | Workspace |
|------|---------|-----------|
| **PM** | Requirements → Spec | ~/pm-workspace |
| **UI/UX Designer** | Spec → Design | ~/designer-workspace |
| **Developers** (N) | Implementation | ~/dev-*-workspace |
| **QA** | Testing → Quality | ~/qa-workspace |
| **Admin** | Coordination + Quality Gates | ~/workspace |

---

## GitHub Workflow (Per Deliverable)

Every deliverable follows PR workflow:

| Stage | Branch | Action |
|-------|--------|--------|
| Spec | `feature/{id}/spec` | Create → PR → Review → Merge |
| Design | `feature/{id}/design` | Create → PR → Review → Merge |
| Implementation | `feature/{id}/impl` | Create → PR → Review → Merge |
| Test | `feature/{id}/test` | Create → PR → Review → Merge |

**Rule**: No direct commits to main. Every change goes through PR review.

---

## Agent-Friendly Repository

Created:
- `AGENTS.md` - Main agent guide (Anthropic best practices)
- `.github/agents/pm-agent.md` - PM agent definition
- `.github/agents/dev-agent.md` - Developer agent definition
- `.github/agents/qa-agent.md` - QA agent definition

Each agent has:
- Clear role and responsibilities
- Workspace boundaries
- Commands they can run
- Git workflow they must follow
- What to NEVER do

---

## Phase 1: Infrastructure & Config

### 1.1 Workspaces (DONE ✅)
- [x] ~/codex-workspace
- [x] ~/pm-workspace
- [ ] ~/designer-workspace
- [ ] ~/dev-frontend-workspace
- [ ] ~/dev-backend-workspace
- [ ] ~/qa-workspace

### 1.2 Configuration System
- [ ] Create `config/` directory
- [ ] `config/providers.yaml` - LLM providers
- [ ] `config/roles.yaml` - Full team roles
- [ ] `config/workflow.yaml` - SOP definition
- [ ] `artifacts/` - Shared outputs
- [ ] `logs/` - Execution logs

---

## Phase 2: Core Framework

- [ ] Provider abstraction layer
- [ ] Role registry system
- [ ] Task lifecycle manager
- [ ] Handoff protocols

---

## Phase 3: PM + Designer (SOP Part 1)

- [ ] PM role implementation
- [ ] Designer role implementation
- [ ] Test: requirement → spec → design

---

## Phase 4: Developers (SOP Part 2)

- [ ] Dev role(s) implementation
- [ ] Frontend specialist
- [ ] Backend specialist
- [ ] Test: design → implementation

---

## Phase 5: QA (SOP Part 3)

- [ ] QA role implementation
- [ ] Testing workflow
- [ ] Full SOP integration

---

## Phase 6: Robustness

- [ ] Error handling
- [ ] Fallbacks (provider switching)
- [ ] Observability

---

*Status: Phase 1.2 - Config System*

*Provider-agnostic team: PM (Minimax), Designer (Anthropic), Devs (OpenAI), QA (Anthropic)*
