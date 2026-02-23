# Multi-Agent Framework Research

> Comprehensive analysis of multi-agent orchestration frameworks, architectures, tools, and best practices.

**Last Updated**: 2026-02-23  
**Research Rounds**: 5 (consolidated from previous disorganized research)

---

## Executive Summary

This research consolidates findings from extensive analysis of multi-agent orchestration frameworks, architectures, and tools. The key insight from Anthropic's research: **multi-agent architecture with lead agent + subagents outperformed single agent by 90.2%**.

### Recommended Architecture for Our Setup

```
User → Admin (Minimax M2.5) → Sequential coordination
         ↓
    ┌────┴────┐
    ↓         ↓
PM Agent  Codex Agent  (parallel when independent)
    ↓         ↓
    └────┬────┘
         ↓
    Review (sequential)
```

---

## Table of Contents

1. [Framework Deep Dives](./research/01-frameworks.md) - MetaGPT, CrewAI, ChatDev
2. [Architecture Patterns](./research/02-architectures.md) - Subagents, Parallel vs Sequential, Handoffs
3. [Tools & SDKs](./research/03-tools-sdks.md) - AutoGen, LangGraph, OpenAI Agents, AutoGPT
4. [Best Practices](./research/04-best-practices.md) - Consolidated recommendations

---

## Research Findings Overview

### Key Frameworks Analyzed

| Framework | Philosophy | Best For | Reference |
|-----------|------------|----------|-----------|
| **MetaGPT** | Code = SOP(Team) | Software development | [GitHub](https://github.com/FoundationAgents/MetaGPT) |
| **CrewAI** | Role-playing agents | Enterprise applications | [GitHub](https://github.com/crewAIInc/crewAI) |
| **ChatDev** | Virtual Software Company | Scalable systems (1000+ agents) | [GitHub](https://github.com/OpenBMB/ChatDev) |

### Core Architecture Patterns

| Pattern | When to Use | Avoid When |
|---------|-------------|-------------|
| **Subagents** | Multiple distinct domains, centralized control | Need independent contexts |
| **Spawned Agents** | Different providers per agent, resilience | Simple single-domain tasks |
| **Parallel** | Independent tasks, multi-domain queries | Tasks with dependencies |
| **Sequential** | Clear dependencies, quality gates | Tasks can run independently |

### Tools & SDKs Analyzed

| Tool | Strength | Use Case |
|------|----------|----------|
| **AutoGen** | Enterprise, human-in-loop | Complex business applications |
| **LangGraph** | State persistence, DAG execution | Long-running workflows |
| **OpenAI Agents SDK** | Simple routing | Production Swarm replacements |
| **AutoGPT Platform** | Visual workflow, ops | Managed deployments |

---

## Key Principles (From All Research)

### 1. Use Explicit Handoff Contracts

```yaml
handoff:
  from: AgentA
  to: AgentB
  input:
    required: [artifact_path, summary]
  output:
    expected_format: markdown
  failure_policy:
    max_retries: 2
    escalate_to: admin
```

### 2. Persist State Between Agents

- Task state file + checkpointing
- Never rely on ephemeral chat only
- Use structured artifact files

### 3. Bound Autonomy

| Parameter | Recommended |
|-----------|-------------|
| `max_iterations` | 20 |
| `max_tool_calls` | 50 |
| `max_retries` | 2 |
| `timeout` | 300s |

### 4. Human-in-the-Loop at Key Gates

- After PM spec (feasibility check)
- Before merge/deploy (quality check)
- For sensitive operations (API changes)

### 5. Graph Over Ad-hoc Chains

- Model workflow as DAG (including parallel branches)
- Add explicit rollback/error paths
- LangGraph-style checkpoint persistence

### 6. Observability First

- Per-agent logs
- Task IDs and traceability
- Runtime metrics (latency, retries, failure reasons)

### 7. Role Isolation

- Separate workspace per agent
- Principle-of-least-privilege tools/access
- No crossing boundaries without explicit handoff

---

## Recommended Agent Definitions

### Admin (Me - Orchestrator)

```yaml
Role: Project Orchestrator
Goal: Coordinate sub-agents, review outputs, ensure quality
Backstory: Experienced tech lead managing a distributed team
Model: Minimax M2.5
Tools: sessions_spawn, message, read, write, exec
Workspace: ~/admin-workspace
Constraints: Reviews all outputs before proceeding
```

### PM Agent

```yaml
Role: Product Manager
Goal: Create specs, prioritize backlog, define requirements
Backstory: Experienced PM who bridges business and tech
Model: Minimax M2.5
Workspace: ~/pm-workspace
Tools: File ops, github issues
```

### Developer Agent

```yaml
Role: Software Developer
Goal: Write clean, working code based on specifications
Backstory: Senior developer who cares about code quality
Model: OpenAI Codex (gpt-5.3-codex)
Workspace: ~/codex-workspace
Tools: File ops, exec, github, browser
```

### QA Agent

```yaml
Role: QA Engineer
Goal: Test implementation, report bugs, ensure quality
Backstory: Thorough tester with attention to detail
Model: Minimax M2.5 or Claude
Workspace: ~/qa-workspace
Tools: File ops, exec, testing frameworks
```

---

## Workflow Implementation

### Standard Operating Procedure (SOP)

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

### Per-Task Artifacts

```
artifacts/tasks/{task-id}/
├── brief.md           # Original request
├── 01-spec.md         # PM output
├── 02-design.md       # Designer output
├── 03-implementation/ # Dev output
├── 04-testing.md      # QA output
└── state.json         # Task state
```

---

## Directory Structure

```
multi-agent-framework/
├── config/
│   ├── providers.yaml     # LLM provider configs
│   ├── roles.yaml         # Role definitions
│   ├── tasks.yaml         # Task templates
│   └── workflow.yaml      # SOP workflow
│
├── workspaces/
│   ├── admin-workspace/
│   ├── pm-workspace/
│   ├── designer-workspace/
│   ├── dev-*-workspace/
│   └── qa-workspace/
│
├── artifacts/
│   └── tasks/
│       └── {task-id}/
│
├── docs/
│   ├── research/
│   │   ├── 01-frameworks.md
│   │   ├── 02-architectures.md
│   │   ├── 03-tools-sdks.md
│   │   └── 04-best-practices.md
│   ├── architecture-v2.md
│   └── tasks.md
│
└── skills/
    ├── agent-team-orchestration/
    └── brainstorming/
```

---

## MCP & External Tools Integration

### MCP Decision: Not Needed for Native Capabilities

**Decision**: MCP is not required when agents already have built-in capabilities.

| Tool | Agent Has It? | Need MCP? |
|------|---------------|-----------|
| GitHub | Codex has Git ✅ | ❌ No |
| File ops | Codex has it ✅ | ❌ No |
| Browser | OpenClaw browser tool ✅ | ❌ No |
| Web search | Codex has it ✅ | ❌ No |

**When MCP makes sense**:
- Agent lacks capability (need Brave Search, but no web search)
- Standardization across multiple agents
- Custom/third-party APIs not built into any agent

### Communication Tools Integration

**Decision**: Agents need separate accounts for Discord/Telegram/Feishu to communicate directly.

#### Why Separate Accounts?

| Benefit | Example |
|---------|---------|
| **@mentionable** | "@pm-agent review this spec" |
| **Clear attribution** | "Dev Agent completed PR #123" |
| **Targeted routing** | Messages to specific agents |
| **Independent presence** | Agents online/away status |

#### Architecture Options

**Option A: Hub-and-Spoke (Recommended for Start)**
```
OpenClaw (me) monitors Discord
    │
    ├── Detect @pm-agent → Spawn PM sub-agent → Reply
    ├── Detect @dev-agent → Spawn Dev sub-agent → Reply
    └── Detect @codex → Route to Codex → Reply
```

**Option B: Independent Agents (Future)**
```
@pm-agent (dedicated bot) → Own Discord account → Always online
@dev-agent (dedicated bot) → Own Discord account → Always online
```

#### Tools to Integrate

| Tool | Use Case | Status |
|------|----------|--------|
| **Discord** | Team communication | ✅ Available |
| **Telegram** | Personal chat | Available |
| **Feishu** | China workspace | Have skills |
| **Jira** | Task tracking | To evaluate |

#### Required Automation

| Automation | Purpose |
|------------|---------|
| Account setup | Create bot accounts, get tokens |
| Session management | Keep agents logged in |
| Mention detection | Filter messages for @agent |
| Context passing | Forward to correct workspace |
| Response routing | Send replies back to channel |

---

## Action Items

- [ ] Review consolidated research documents
- [ ] Configure sub-agent workspaces
- [ ] Test sessions_spawn with role definitions
- [ ] Implement SOP workflow with artifact templates
- [ ] Set up Git branch protection rules
- [ ] Add observability logging
- [ ] Test Discord agent communication (hub-and-spoke)
- [ ] Evaluate Feishu integration for China workflow
- [ ] Consider Jira for task management

---

## References

### Frameworks
- MetaGPT: https://github.com/FoundationAgents/MetaGPT
- CrewAI: https://github.com/crewAIInc/crewAI
- ChatDev: https://github.com/OpenBMB/ChatDev

### Tools & SDKs
- AutoGen: https://github.com/microsoft/autogen
- LangGraph: https://github.com/langchain-ai/langgraph
- OpenAI Agents SDK: https://openai.github.io/openai-agents-python/

### Documentation
- CrewAI Agents: https://docs.crewai.com/concepts/agents
- CrewAI Tasks: https://docs.crewai.com/concepts/tasks

---

*Research completed: 2026-02-23*
