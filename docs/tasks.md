# Multi-Agent Framework - Task List

## Architecture Decision: Hierarchical Hybrid

```
User → Admin (sequential coordination)
         ↓
    ┌────┴────┐
    ↓         ↓
PM Agent  Codex Agent  (parallel when independent)
    ↓         ↓
    └────┬────┘
         ↓
    Review (sequential gate)
```

---

## Phase 1: Infrastructure Setup

### Task 1.1: Create Workspaces
- [ ] Create developer workspace (~/codex-workspace or similar)
- [ ] Create PM workspace (~/pm-workspace or similar)
- [ ] Test file operations in each

### Task 1.2: Configure Sub-agent Profiles
- [ ] Define Codex developer agent config (model: openai-codex, workspace)
- [ ] Define PM agent config (model: minimax-m2.5, workspace)
- [ ] Document agent profiles in docs/

---

## Phase 2: Sub-agent Framework

### Task 2.1: Spawn Sub-agents
- [ ] Test spawning Codex agent with specific workspace
- [ ] Test spawning PM agent with specific workspace
- [ ] Verify each uses correct model

### Task 2.2: Task Templates
- [ ] Create delegation templates (how to assign work)
- [ ] Define output formats for sub-agent results
- [ ] Set up review/approval workflow

---

## Phase 3: Integration

### Task 3.1: GitHub Integration
- [ ] Verify `gh` CLI auth
- [ ] Test issues/PRs operations
- [ ] Document in skills

### Task 3.2: Discord Integration
- [ ] Review/enhance Discord capabilities

---

## Phase 4: Advanced

### Task 4.1: Custom Skills
- [ ] Build reusable skills for common tasks

### Task 4.2: Monitoring
- [ ] Track sub-agent activity
- [ ] Set up reporting

---

## Key References

- Installed skill: `agent-team-orchestration` - for roles, task states, handoffs
- Installed skill: `brainstorming` - for creative phase before implementation

---

*Status: Ready to start Phase 1*
