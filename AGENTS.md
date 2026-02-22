# AGENTS.md - Agent-Friendly Repository

This repository is designed for AI agents to work with. It follows Anthropic's best practices for agent-friendly repos.

---

## Repository Purpose

Multi-Agent Framework - A virtual software company with PM, Designer, Devs, and QA roles coordinated by Admin.

---

## Tech Stack

- **Orchestration**: OpenClaw
- **LLM Providers**: Minimax, OpenAI, Anthropic
- **Version Control**: GitHub
- **Skills**: agent-team-orchestration, brainstorming

---

## Project Structure

```
multi-agent-framework/
├── config/                 # Configuration files (YAML)
│   ├── providers.yaml     # LLM provider configs
│   ├── roles.yaml        # Role definitions
│   ├── tasks.yaml        # Task templates
│   └── workflow.yaml     # SOP workflow
│
├── workspaces/            # Agent workspaces
│   ├── pm-workspace/     # Product Manager
│   ├── designer-workspace/ # UI/UX Designer
│   ├── dev-*-workspace/  # Developers
│   └── qa-workspace/     # QA Engineer
│
├── artifacts/             # Task outputs
│   └── tasks/           # Each task's deliverables
│
├── skills/               # Reusable skills
│
├── docs/                 # Documentation
│   ├── architecture-v2.md  # Full architecture
│   └── tasks.md          # Task list
│
└── .github/
    └── agents/           # Agent definitions
```

---

## Available Agents (for this repo)

### @pm-agent
- **Role**: Product Manager
- **What it does**: Creates requirements, specs, user stories
- **Writes to**: `artifacts/tasks/{task-id}/`
- **Commands**: None (uses reasoning)
- **Boundaries**:
  - ✅ Write SPEC.md, requirements.md
  - ⚠️ Ask before creating new task directories
  - 🚫 Never write code

### @designer-agent
- **Role**: UI/UX Designer  
- **What it does**: Creates designs, mockups, UX specs
- **Writes to**: `artifacts/tasks/{task-id}/`
- **Commands**: None
- **Boundaries**:
  - ✅ Write design.md, component specs
  - ⚠️ Ask before modifying PM specs
  - 🚫 Never write code

### @dev-agent
- **Role**: Developer
- **What it does**: Implements features, writes code
- **Writes to**: `workspaces/dev-*/`, `artifacts/tasks/{task-id}/`
- **Commands**:
  - `npm install` / `pip install` - Install dependencies
  - `npm run build` - Build project
  - `npm test` - Run tests
- **Boundaries**:
  - ✅ Write code in workspaces/
  - ✅ Write tests in appropriate test dirs
  - 🚫 Never commit directly to main
  - 🚫 Never push secrets

### @qa-agent
- **Role**: QA Engineer
- **What it does**: Tests, validates, reports bugs
- **Writes to**: `artifacts/tasks/{task-id}/`
- **Commands**:
  - `npm test` - Run test suite
  - `npm run lint` - Lint code
- **Boundaries**:
  - ✅ Write test-results.md, bug reports
  - ✅ Add failing tests (never remove)
  - 🚫 Never modify source code

---

## Git Workflow (IMPORTANT)

All agents MUST follow this workflow:

1. **Create branch**: `feature/{task-id}/{type}`
   - Types: spec, design, impl, test
2. **Make changes**
3. **Create PR**: Use proper title format
4. **Wait for review** (Admin reviews)
5. **Merge after approval**

### PR Title Format
```
[{Type}] {Task Name}

Example:
[Spec] User authentication system
[Impl] Add login API endpoint
[Test] Login flow test coverage
```

### Commands Before Commit
```bash
# Always run before committing
npm test
npm run lint
```

---

## Task Workflow

Every task follows SOP:

```
User Request
    │
    ▼
┌─────────────────┐
│      PM         │ → Branch: feature/{id}/spec → PR → Review → Merge
│   SPEC.md       │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   Designer      │ → Branch: feature/{id}/design → PR → Review → Merge
│   design.md     │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│   Developer     │ → Branch: feature/{id}/impl → PR → Review → Merge
│   Code          │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│      QA         │ → Branch: feature/{id}/test → PR → Review → Merge
│   test-results  │
└─────────────────┘
    │
    ▼
      Done
```

---

## Boundaries (All Agents)

| ✅ Always Do | ⚠️ Ask First | 🚫 Never Do |
|-------------|--------------|-------------|
| Write to assigned workspace | Modify other's artifacts | Commit to main |
| Create branches | Change task scope | Push secrets |
| Open PRs | Delete files | Access other workspaces |
| Run tests/lint | Modify config | Bypass PR workflow |

---

## How Agents Should Work Together

1. **PM** creates spec → opens PR → Admin reviews → merges
2. **Designer** reads merged spec → creates design → opens PR → Admin reviews → merges
3. **Dev** reads merged design → implements → opens PR → Admin+QA reviews → merges
4. **QA** tests implementation → reports results → opens PR → Admin reviews → merges

---

*This file makes the repo agent-friendly following GitHub/Anthropic best practices.*
