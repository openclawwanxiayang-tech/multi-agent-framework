# Multi-Agent Framework Research v2.2

> Comprehensive analysis of multi-agent orchestration frameworks, architectures, tools, and best practices.

**Last Updated**: 2026-02-23  
**Version**: 2.2 (enhanced with community practices, gaps analysis, and roadmap)

---

## Executive Summary

This document builds on existing research and outlines an enhanced multi-agent collaboration architecture. We review the current repo's design (roles-as-agents, branch-based workflows, SOPs) and survey emerging 2024–2026 practices (OpenClaw's agent teams, ClawSwarm, LangChain's Open Agent Platform, LangGraph, MetaGPT, AutoGen, etc.).

We identify gaps in governance, observability, persistence, and standardisation (e.g., need for guardrails, tracing, shared memory/blackboard, task queue) and propose concrete v2 additions: a clear system model, task lifecycle, message/artefact schemas, blackboard spec, log format, validators, MCP stance, and "swarm modes".

The key insight from Anthropic's research: **multi-agent architecture with lead agent + subagents outperformed single agent by 90.2%**.

---

## Table of Contents

1. [Existing Documentation Summary](#existing-documentation-summary)
2. [Recent Community Practices (2024–2026)](#recent-community-practices-20242026)
3. [Gaps vs Best Practices](#gaps-vs-best-practices)
4. [Proposed v2 Architecture & Processes](#proposed-v2-architecture--processes)
5. [Swarm Modes](#swarm-modes)
6. [Implementation Roadmap](#implementation-roadmap)
7. [Repos/Tools Comparison](#repostools-comparison)
8. [Recommended Next Steps](#recommended-next-steps)
9. [Schema Definitions](./schemas/README.md) - JSON schemas for tasks, state, events
10. [MCP & External Tools Integration](#mcp--external-tools-integration)
10. [Communication Tools Integration](#communication-tools-integration)

---

## Existing Documentation Summary

The `docs/` folder already describes a **structured SOP-driven workflow**: each role (PM, designer, developer, QA, admin) is defined as an "agent" with its own workspace and responsibilities.

**Design Principles:**
- Modularity
- Provider-agnosticism
- Role-based
- SOP-driven

**Example Architecture:**
```
Admin → parallel PM & Designer → Review → Dev → QA
```

**Current Files:**
- `architecture-v2.md` - Design principles and team structure
- `tasks.md` - Deliverables and PR-based pipeline
- `research.md` - Framework surveys (MetaGPT, CrewAI, etc.)

**Current Gap:** The docs capture an **assembly-line approach**: a lead Admin agent delegates to specialist agents, which exchange documents via a version-controlled backlog. They do **not yet specify**:
- Message schemas
- Blackboard structure
- Detailed observability/logging schemes

---

## Recent Community Practices (2024–2026)

### OpenClaw Agent Teams
OpenClaw's latest RFC (Feb 2026) calls for **Agent Teams** – a coordinated multi-agent mode enabling parallel execution with shared state and inter-agent messaging. This contrasts the old "sessions_spawn" (isolated subagents) model and matches our need for sibling communication.

### ClawSwarm
A lightweight multi-agent system (director + workers) built on Swarms framework. It uses a **hierarchical swarm**: a single director agent receives each task, emits a structured plan (SwarmSpec) to specialist workers, then collates their outputs. Workers have narrow roles (e.g., search, code, summarization) and the director does *not* execute tools itself. ClawSwarm also persists conversation memory with RAG to handle long histories.

### LangChain / LangGraph / Open Agent Platform
LangChain's ecosystem emphasizes multi-agent orchestration:
- **Open Agent Platform (OAP)**: No-code UI for building agents with first-class support for Retrieval (LangConnect RAG) and MCP tool integration, plus an "Agent Supervisor" to orchestrate agents together
- **LangGraph**: Designed for *stateful, hierarchical multi-actor workflows* – supports single-, multi-agent and hierarchical flows in one framework, with built-in long-term memory, "time-travel" state management, and human-in-the-loop controls

These tools emphasise **observability and durability** (traces, metrics, undo/roll-back, background jobs) and strict typing (memory schema, tool interfaces).

### MetaGPT
An example of SOP-driven agent workflows. MetaGPT encodes Standard Operating Procedures into prompt pipelines, creating an "assembly line" of role-based agents. Each agent has a specialist role (requirements, coding, testing, etc.) and agents verify each other's outputs to reduce errors. The workflow is iterative: agents handle subtasks in parallel and feed results back to lead agents.

### AutoGen (Microsoft)
A popular open-source multi-agent framework (Python) designed for research/collaboration. It allows agents to chat and self-reflect in loops. AutoGen supports agent-to-agent communication patterns and "self-reflection" but lacks built-in enterprise features (no RBAC, audit, etc.).

### Governance & Safety
Recent guidance stresses:
- Built-in guardrails
- Logging
- Human oversight
- Pre-flight checks ("input guardrails")
- Tracing for observability
- Centralized policy enforcement
- Eval-driven metrics loops
- CitationAgent for sources in research
- Memory of plans to avoid hallucination

---

## Gaps vs Best Practices

| Gap Area | Current State | Best Practice | Proposed v2 Addition |
|----------|---------------|---------------|---------------------|
| **Coordination Patterns** | Spawn-and-return flow | Sibling communication, dynamic task creation | Support parallel workflows, nested agents |
| **Governance & Security** | "What NOT to do" lists | Formal policy enforcement, RBAC, audit logs | Security policies, pre-flight schemas |
| **Observability & Logging** | No structured logging | Full observability (trace IDs, event logs) | Trace/event log format |
| **Durability & Memory** | Local file per workspace | Persistent blackboard/memory | Shared blackboard, task queue |
| **Task Lifecycle** | Implicit workflow | Formal task queue with state machine | Task queue specification |
| **Standardisation** | Ad-hoc tools | MCP for tool discovery | MCP stance (stateless tools only) |
| **Evaluation** | None defined | Eval-driven design | Stage validators, regression tests |
| **Permissioning** | Not mentioned | Least-privilege, scoped tokens | Agent permission scopes |

---

## Proposed v2 Architecture & Processes

### System Model and Workflow

We propose a **flow-based orchestrator** (inspired by CrewAI) with a central *Admin/Orchestrator agent* defining the task flow.

```
User Request
     │
     ▼
┌─────────────────┐
│ Admin/Coordinator│
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
PM Agent   Designer Agent
    │         │
    └────┬────┘
         │
         ▼
┌─────────────────┐
│  Merge Docs     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Developer Agent │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Reviewer Agent  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   QA Agent      │
└────────┬────────┘
         │
         ▼
  Completed
```

**Roles:**
- **Admin/Coordinator**: Parses user input, creates Task object, orchestrates phases, sets guardrails
- **PM & Designer (Parallel)**: In phase 1, both analyze requirements; outputs merge into common workspace
- **Developer**: Writes code/artifacts based on merged outputs
- **Reviewer**: Conducts peer-review of dev output
- **QA**: Runs tests and final approval

### Task Lifecycle (Pipeline)

```
New Request
     │
     ▼
Analysis/Planning
     │
     ▼
┌─────────────────────┐
│  Parallel?          │
│  (Yes/No branch)    │
└─────────┬───────────┘
          │
    ┌─────┴─────┐
    ▼           ▼
Parallel    Sequential
Execution   Execution
    │           │
    └─────┬─────┘
          │
          ▼
   Merge Outputs
          │
          ▼
Development & Tools
          │
          ▼
Validation/Testing
          │
          ▼
    Completion
```

**States:** New → Planning → InProgress → Review → Done

**States:** New → Planning → InProgress → Review → Done

### Message / Artifact Schema

All inter-agent messages and artefacts should follow **typed schemas**:

```json
{
  "task_id": "T1234",
  "stage": "spec",
  "sender": "PM-Agent",
  "payload": {
    "spec_title": "Feature X Requirements",
    "sections": [
      {"heading": "Overview", "content": "..."},
      {"heading": "Acceptance Criteria", "content": "..."}
    ]
  },
  "metadata": {"timestamp": "...", "version": 1}
}
```

All agents validate incoming envelopes against JSON schemas (e.g., using Pydantic).

### Shared Blackboard & Task Queue

We introduce a **blackboard** (GitHub repository or database) where agents post and retrieve artifacts and context.

**Blackboard Fields:**
- `task_id`
- `phase`
- `document_refs`
- `agent_outputs`

**Task Queue Fields:**
- `task_id`
- `status`
- `assigned_agents[]`
- `dependencies[]`
- `history[]`

**State Transitions:** New → Planning → InProgress → Review → Done

### Trace/Event Log Format

All agent actions must be logged in an append-only **trace log**:

```json
{
  "timestamp": "2026-02-23T18:34:00Z",
  "task_id": "T1234",
  "agent": "Dev-Agent",
  "action": "tool_call",
  "tool": "run_tests",
  "input": {"files": 2},
  "output": {"passed": 10, "failed": 0},
  "result": "success"
}
```

This log can be ingested by observability tools (Elastic, LangSmith) for replay/debugging.

### Stage Validators

| Stage | Validator | Checks |
|-------|-----------|--------|
| **Spec** | spec_validator.py | Required sections, no empty fields |
| **Design** | design_validator.py | Completeness, wireframes included |
| **Code** | code_linter.py | Style, security, tests |
| **QA** | compliance_checker.py | Forbidden content, security issues |

---

## Swarm Modes

We should support multiple modes of collaboration:

| Mode | Description | Use Case |
|------|-------------|----------|
| **Manager-Orchestrator** | One lead agent issues tasks | Our default (Admin → sub-agents) |
| **Decentralized** | Agents call each other peer-to-peer | Brainstorming |
| **Pipeline** | Linear handoff | No parallelism needed |
| **Parallel Team** | Lead spawns many sub-agents in parallel | Research, multi-domain queries |

The system should be flexible to switch modes per Task (config flag).

---

## Implementation Roadmap

| Milestone | Effort | Description |
|-----------|--------|-------------|
| **1. Schema & Logging** | Low | Define JSON schemas, trace log format, basic guardrails |
| **2. Blackboard & Queue** | Medium | Set up shared workspace, implement Task Queue |
| **3. Validators & Evals** | Medium | Write validation scripts, integrate into CI |
| **4. Observability & Governance** | High | Logging/tracing system, RBAC, policy engine |
| **5. MCP Integration** | High | Deploy MCP server with curated tools (if needed) |
| **6. Documentation** | Low | Update docs with new model, diagrams |

**Effort Estimates:**
- Low ≈ 1–2 engineers × 1 month
- Medium ≈ 2–3 engineers × 2–3 months
- High ≈ 3+ engineers × 3–6 months

---

## Repos/Tools Comparison

| Repository/Tool | Purpose | Maturity | License | Relevance |
|-----------------|---------|----------|---------|-----------|
| **openclaw/openclaw** | Multi-agent assistant | Production | Apache-2.0 | Base orchestrator |
| **The-Swarm-Corporation/ClawSwarm** | Hierarchical multi-agent bot | Prototype | Apache-2.0 | Lightweight alternative |
| **LangChain/langchain** | LLM agent framework | Production | MIT | Industry-standard |
| **langchain-ai/langgraph** | Graph-based orchestration | Beta | MIT | Stateful workflows |
| **langchain-ai/open-agent-platform** | No-code + supervisor | Alpha | MIT | Agent-supervisor pattern |
| **FoundationAgents/MetaGPT** | SOP-driven framework | Research | MIT | Assembly-line roles |
| **microsoft/autogen** | Multi-agent orchestration | Active | MIT | Agent loops |
| **modelcontextprotocol** | Protocol for tools | Emerging | Apache-2.0 | Tool standard |
| **fastmcp/fastmcp** | MCP server framework | Emerging | MIT | Host MCP tools |

---

## Recommended Next Steps

1. **PR: Define Blackboard & Task-Queue**
   - Create `blackboard.md` describing shared workspace model
   - Add JSON schema for Task and envelopes
   - Implement Task Queue service

2. **PR: Add Logging & Traceability**
   - Introduce trace logger and event JSON schema
   - Update each agent to log actions
   - Demonstrate trace for completed task

3. **PR: Validator Scripts and SOP Update**
   - Add validator tools (spec_validator.py, code_linter.py)
   - Include in CI (GitHub Actions)
   - Update SOP docs to reference checks

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

### MCP Security Stance

If adopting MCP:
- Host tools on trusted MCP server
- Ensure **tool permissioning**: scoped tokens, network restrictions
- **Stateful tools** (databases, vector stores) remain "native"
- Enforce **cryptographic authenticity**: sign tool metadata
- Maintain **security review checklist** for each new tool

---

## Communication Tools Integration

**Decision**: Agents need separate accounts for Discord/Telegram/Feishu to communicate directly.

### Why Separate Accounts?

| Benefit | Example |
|---------|---------|
| **@mentionable** | "@pm-agent review this spec" |
| **Clear attribution** | "Dev Agent completed PR #123" |
| **Targeted routing** | Messages to specific agents |
| **Independent presence** | Agents online/away status |

### Architecture Options

**Option A: Hub-and-Spoke (Recommended)**
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

### Tools to Integrate

| Tool | Use Case | Status |
|------|----------|--------|
| **Discord** | Team communication | ✅ Available |
| **Telegram** | Personal chat | Available |
| **Feishu** | China workspace | Have skills |
| **Jira** | Task tracking | To evaluate |

### Required Automation

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
- [ ] Define message/artifact JSON schemas
- [ ] Set up shared blackboard (tasks/ repo or DB)
- [ ] Implement Task Queue service
- [ ] Define trace/event log format
- [ ] Add stage validators (spec, design, code, QA)
- [ ] Set up observability logging
- [ ] Set up Git branch protection rules
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
- ClawSwarm: https://github.com/The-Swarm-Corporation/ClawSwarm

### Documentation
- CrewAI Agents: https://docs.crewai.com/concepts/agents
- CrewAI Tasks: https://docs.crewai.com/concepts/tasks

---

*Research completed: 2026-02-23*
