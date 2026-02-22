# Multi-Agent Collaboration Framework

## Vision
An admin agent (me) coordinates multiple specialized sub-agents, each with specific capabilities and access permissions.

## Core Components

### 1. Admin Agent (Central Coordinator) — THIS AGENT
- **Model**: Minimax M2.5 (default)
- **Workspace**: ~/workspace
- **Role**: Central orchestration, task delegation, quality control
- **Capabilities**: Task decomposition, progress tracking, spawn/manage sub-agents

### 2. Specialized Sub-Agents

| Agent | Model | Workspace | Role |
|-------|-------|-----------|------|
| Codex (Developer) | OpenAI Codex | TBD (e.g., ~/projects/dev) | Code, build, implement features |
| PM Agent | Minimax | TBD (e.g., ~/projects/pm) | Plan, spec, prioritize, manage backlog |
| GitHub Agent | (any) | — | Issues, PRs, CI/CD, repo ops |
| Discord Agent | (any) | — | Channel management, community ops |

### 3. Infrastructure Requirements

#### Model Providers
- OpenAI (GPT-4, GPT-4o, etc.)
- Anthropic (Claude)
- Local/Ollama models
- Minimax (current default)
- Ability to route tasks to optimal provider

#### Local Workspaces
- Multiple project directories
- Isolated or shared access
- Clear separation of concerns

#### Communication
- Inter-agent messaging
- Shared state/context
- Task handoff protocols

## Initial Scope (Phase 1)

1. **GitHub Agent** - Basic operations (issues, PRs, CI status)
2. **Discord Agent** - Extended capabilities (beyond current)
3. **Model Router** - Configure 2-3 providers, ability to switch
4. **Basic Workspace** - One additional workspace directory

## Future Enhancements

- More specialized agents (research, coding, etc.)
- Advanced inter-agent workflows
- Custom skill development
- Monitoring and observability

---

*Last updated: 2026-02-22*
