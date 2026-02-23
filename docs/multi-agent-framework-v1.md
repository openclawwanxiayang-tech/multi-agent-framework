# Multi-Agent Framework - Project Documentation

> **DEPRECATED**: This document is kept for historical context. Use `docs/architecture-v2.md`, `docs/research.md`, and `docs/tasks.md` as the source of truth.

## Vision
Build an AI agent orchestration system where an Admin agent (me) coordinates specialized sub-agents for collaborative task execution.

## Research Summary

### Architecture Patterns (LangChain, Microsoft, Anthropic, Google)

| Pattern | Use When |
|---------|----------|
| **Subagents** | Multiple distinct domains, centralized control needed |
| **Skills** | Single agent with many specializations |
| **Handoffs** | Sequential workflows, customer support flows |
| **Router** | Multi-source queries, distinct verticals |

### Key Findings

1. **Subagents vs Spawned Agents**
   - Subagents: Centralized control, +1 call overhead, context flows through main
   - Spawned: Decentralized, isolated contexts, more resilient

2. **Anthropic Research**: Lead agent + subagents = **90.2% better performance** than single agent

3. **Parallel vs Sequential**
   - Parallel: For independent tasks (faster)
   - Sequential: For dependent tasks with quality gates

4. **Most production systems use hybrid approaches**

## Decision: Hierarchical Hybrid Architecture

```
User → Admin (Minimax M2.5)
         ↓
    ┌────┴────┐
    ↓         ↓
PM Agent  Codex Agent  (parallel when independent)
    ↓         ↓
    └────┬────┘
         ↓
    Review (sequential gate)
```

### Why This Architecture
- **Admin**: Sequential coordination, quality gates, human approval
- **PM Agent**: Specs, requirements, planning
- **Codex Agent**: Code implementation
- **Review**: Always sequential gate before output

## Installed Skills

1. **agent-team-orchestration** - Multi-agent team orchestration with roles, task lifecycles, handoff protocols
2. **brainstorming** - Creative exploration before implementation

## Phase 1: Infrastructure Setup (Current)

- [ ] Create workspace directories for sub-agents
- [ ] Configure sub-agent profiles
- [ ] Test spawning agents

## Phase 2: Framework Setup

- [ ] Define task templates
- [ ] Set up review/approval workflow
- [ ] Configure GitHub integration

## Phase 3: Integration

- [ ] GitHub operations (issues, PRs)
- [ ] Discord operations

## Phase 4: Advanced

- [ ] Custom skills
- [ ] Monitoring

## References

- LangChain Multi-Agent: https://docs.langchain.com/oss/python/langchain/multi-agent
- Microsoft Azure Patterns: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- Anthropic Multi-Agent Research: https://www.anthropic.com/engineering/multi-agent-research-system
- MetaGPT: https://github.com/FoundationAgents/MetaGPT
- CrewAI: https://docs.crewai.com/

---

*Last updated: 2026-02-22*
