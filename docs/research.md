# Multi-Agent Framework Research

## Overview
Research into existing multi-agent orchestration frameworks to inform our approach.

---

## Key Frameworks Analyzed

### 1. MetaGPT
**Philosophy**: "Code = SOP(Team)" — Standard Operating Procedures for AI agent teams

**Core Concepts**:
- **SOP (Standard Operating Procedures)**: Define explicit workflows for agent collaboration
- **Role Assignment**: Assign different roles (PM, Architect, Engineer, QA) to LLMs
- **Shared Context**: Agents share a "memory" / message board
- **Structured Output**: Requirements → Design → Code → Docs

**Architecture**:
```
Requirement → PM → Architect → Project Manager → Engineer → QA
                     ↓              ↓              ↓         ↓
               Spec/PRD        Task Breakdown   Code    Test Results
```

**Strengths**:
- Well-defined workflows
- Proven for software development
- Strong research backing (multiple papers)

---

### 2. CrewAI
**Philosophy**: "Role-playing autonomous agents" — Collaborative intelligence

**Core Concepts**:
- **Agents**: Autonomous entities with roles, goals, backstories
- **Crews**: Teams of agents working together
- **Tasks**: Defined objectives with expected output
- **Tools**: Agents can use tools (similar to OpenClaw skills)
- **Flows**: Event-driven orchestration for enterprise

**Architecture**:
```
Task 1 → Agent A → Output
Task 2 → Agent B → Output
    ↓
Crew (orchestrates agents)
```

**Strengths**:
- Flexible — agents can be any role
- Built-in tool integration
- Enterprise-ready (Flows, monitoring)
- Large community (100k+ developers)

---

### 3. ChatDev (OpenBMB)
**Philosophy**: "Virtual Software Company" — Multi-agent collaboration

**Core Concepts**:
- **Multi-Agent Seminars**: Agents participate in functional meetings
- **Puppeteer Paradigm**: Central orchestrator dynamically activates/sequences agents
- **MacNet**: DAG-based collaboration for 1000+ agents
- **Zero-Code Config**: Define agents/workflows via config

**Variants**:
- ChatDev 1.0: Virtual software company (CEO, CTO, Programmer roles)
- ChatDev 2.0 (DevAll): Zero-code platform for any multi-agent system

**Strengths**:
- Scalable to many agents
- Research-backed (NeurIPS 2025 paper)
- Flexible topology (chain, DAG, etc.)

---

## Common Patterns Across All Frameworks

### 1. Role-Based Agents
Each agent has:
- **Role/Title** (PM, Developer, Reviewer)
- **Goals/Objectives**
- **Backstory/Context** (optional)
- **Tools/Capabilities**

### 2. Explicit Workflows (SOPs)
- Define how agents interact
- Sequential or parallel execution
- Handoff protocols between agents

### 3. Shared Context
- Central memory / message board
- Output from one agent becomes input to next
- Structured data passing

### 4. Task Decomposition
- Break complex tasks into subtasks
- Assign to appropriate agents
- Aggregate results

### 5. Review/Feedback Loops
- Quality checks between stages
- Iterative refinement
- Human oversight points

---

## Best Practices for Our Implementation

### Recommended Patterns

1. **Define Clear Roles**
   - Each sub-agent has specific purpose
   - Document role, goals, constraints

2. **Use SOPs for Workflows**
   - Explicit handoff protocols
   - Input/output formats for each stage

3. **Shared Workspace for Context**
   - Structured files for task state
   - Clear file-based handoffs

4. **Review Points**
   - Admin (me) reviews before moving forward
   - Explicit approval gates

5. **Task Templates**
   - Standard formats for delegating work
   - Expected output structure

### What Works Well

| Pattern | From | Why |
|---------|------|-----|
| SOP-based workflow | MetaGPT | Predictable, repeatable |
| Role + Goals + Tools | CrewAI | Clear agent definition |
| Shared memory board | MetaGPT | Context preservation |
| DAG-based execution | ChatDev | Flexible topology |
| Zero-code config | ChatDev 2.0 | Easy to modify |

---

## Application to Our Use Case

Based on research, here's what I'll implement:

### Admin (Me)
- Orchestrator / Project Manager
- Define SOPs for delegating tasks
- Review outputs, approve next steps

### Sub-Agents
- **Codex (Developer)**: Write code, implement features
- **PM Agent**: Create specs, plan tasks, prioritize

### Workflow
```
Idea → PM Agent (spec) → Admin reviews → Codex (code) → Admin reviews → Done
```

### Tools per Agent
- Developer: GitHub, code execution, file ops
- PM: Documentation, maybe GitHub issues

---

---

## Round 2: Deep Dive on CrewAI Agent Definition

### Agent Attributes (from CrewAI docs)

| Attribute | Parameter | Description |
|-----------|-----------|-------------|
| **Role** | `role` | Agent's function and expertise |
| **Goal** | `goal` | Individual objective guiding decision-making |
| **Backstory** | `backstory` | Context and personality |
| **LLM** | `llm` | Language model (can specify different per agent) |
| **Tools** | `tools` | Capabilities/functions available |
| **Max Iterations** | `max_iter` | Max attempts before final answer |
| **Verbose** | `verbose` | Debug logging |

### Task Attributes

| Attribute | Parameter | Description |
|-----------|-----------|-------------|
| **Description** | `description` | What the task entails |
| **Expected Output** | `expected_output` | What completion looks like |
| **Agent** | `agent` | Which agent performs it |
| **Tools** | `tools` | Tools available for task |

### Process Types

- **Sequential**: Tasks execute in defined order
- **Hierarchical**: Manager agent assigns tasks to agents

---

## Recommended Agent Definitions for Our Setup

Based on research, here are the exact agent configs to use:

### 1. Admin Agent (Me)
```
Role: Project Orchestrator
Goal: Coordinate sub-agents, review outputs, ensure quality
Backstory: Experienced tech lead managing a distributed team
Model: Minimax M2.5
Tools: All (spawn, message, read, write, etc.)
```

### 2. Developer Agent (Codex)
```
Role: Software Developer
Goal: Write clean, working code based on specifications
Backstory: Senior developer who cares about code quality
Model: OpenAI Codex (gpt-5.3-codex)
Workspace: ~/codex-workspace
Tools: File ops, exec, github, browser
```

### 3. PM Agent
```
Role: Product Manager
Goal: Create specs, prioritize backlog, define requirements
Backstory: Experienced PM who bridges business and tech
Model: Minimax M2.5
Workspace: ~/pm-workspace
Tools: File ops, github issues
```

---

## Task Delegation Template

When delegating to a sub-agent, include:

```
## Task: [title]
### Role: [Developer/PM]
### Goal: [specific objective]
### Context: [background info]
### Input: [files/data to work with]
### Expected Output: [what success looks like]
### Constraints: [limitations, deadline, etc.]
```

---

## Round 4: Extensive Framework Research (2026)

### Key Findings from Official Documentation

#### CrewAI Best Practices (from official docs)
- **Agent Definition**: Role + Goal + Backstory + Tools + LLM
- **Task Definition**: Description + Expected Output + Agent + Context
- **Key Parameters**:
  - `max_iter`: Max iterations before final answer (default: 20)
  - `allow_delegation`: Agents can delegate to other agents
  - `verbose`: Debug logging
  - `cache`: Cache tool usage (default: True)
  - `max_retry_limit`: Retries on error (default: 2)
  - `respect_context_window`: Summarize to stay under limit

#### CrewAI Task Features
- **Sequential Process**: Tasks execute in defined order
- **Hierarchical Process**: Manager agent assigns tasks
- **Context**: Task outputs can feed into subsequent tasks
- **Output Formats**: Raw, JSON, Pydantic models
- **Guardrails**: Validate output before proceeding

#### MetaGPT Core Philosophy
- **Code = SOP(Team)** — Standard Operating Procedures for AI teams
- Takes one-line requirement → outputs full software
- Includes PM, Architect, Project Manager, Engineers
- Uses carefully orchestrated SOPs

### OpenClaw-Specific Considerations

Based on our setup (Minimax M2.5 for orchestration), here's how to map these patterns:

| Pattern | CrewAI | MetaGPT | OpenClaw Implementation |
|---------|--------|---------|------------------------|
| Agent Definition | YAML + Code | Role-based | sessions_spawn with role description |
| Task Definition | YAML + Code | SOP-based | Structured brief → spec → review |
| Handoff | allow_delegation | Explicit SOP | Admin reviews → spawns next |
| State | Memory + Context | Shared message board | File-based (workspace) |
| Output | Pydantic/JSON | Structured docs | Markdown files |

### Skills That Would Help

1. **coding-agent skill** (already available): For spawning Codex/Claude Code agents
2. **github skill** (already available): For GitHub operations
3. **gh-issues skill** (already available): For issue management

**Missing/Needed**:
- A skill to manage multiple sub-agents with proper workspace isolation
- A skill to define and persist SOPs for common workflows
- A skill to visualize agent execution flow

### Recommended Architecture for OpenClaw

```
User → Admin (Minimax M2.5) → Spawns sub-agents → Reviews → Responds

Sub-agent workspaces:
- ~/codex-workspace (for Codex/Claude Code)
- ~/pm-workspace (for PM agent)
- ~/research-workspace (for research tasks)
```

### Action Items

1. [ ] Configure Brave Search API for better research
2. [ ] Create sub-agent workspace directories
3. [ ] Test sessions_spawn with different agent configs
4. [ ] Define standard task templates
5. [ ] Set up review/approval workflow

---

## Round 5: Architecture Research - Parallel vs Subagents (2026-02-22)

### Key Question: How to arrange agents - parallel or sequential? Subagents or spawned?

#### Research Findings from LangChain, Microsoft, Google, Anthropic

### The 4 Core Architecture Patterns

| Pattern | How it works | Best for |
|---------|-------------|----------|
| **Subagents** | Supervisor coordinates subagents as tools. Results flow back through main agent. | Multiple distinct domains, centralized control |
| **Skills** | Single agent loads specialized prompts on-demand | Single agent with many specializations |
| **Handoffs** | Agent transfers control to another based on context | Sequential workflows, customer support |
| **Router** | Classifies input, dispatches to specialized agents in parallel | Distinct verticals, multi-source queries |

### Subagents vs Spawned (Separate) Agents

| Aspect | Subagents | Spawned Separate Agents |
|-------|-----------|------------------------|
| **Control** | Centralized (all through main) | Decentralized |
| **Context** | Main agent accumulates | Each has isolated context |
| **Latency** | +1 call overhead per task | Direct execution |
| **Debugging** | Single trace | Multiple traces |
| **Failure isolation** | Weaker (crashes main) | Stronger |

**From Anthropic**: "Multi-agent architecture with lead agent + subagents outperformed single agent by **90.2%**"

### Parallel vs Sequential

| Pattern | Use when | Avoid when |
|---------|----------|------------|
| **Parallel** | Independent tasks, multi-domain queries, research | Tasks have dependencies |
| **Sequential** | Clear dependencies, progressive refinement | Tasks can run independently |
| **Hybrid** | Complex real-world systems | Simple single-domain tasks |

### Performance Comparison (LangChain Research)

**One-shot request** (e.g., "buy coffee"):
- Subagents: 4 calls
- Skills/Handoffs/Router: 3 calls

**Repeat request**:
- Subagents: 4 calls/turn
- Skills/Handoffs: 2 calls/turn (40% savings from context)

**Multi-domain query** (e.g., "compare Python, JS, Rust"):
- Subagents: 5 calls, ~9K tokens
- Skills: 3 calls, ~15K tokens (context accumulation)
- Router: 5 calls, ~9K tokens

### When to Use Each

**Use Subagents when:**
- Multiple distinct domains (calendar + email + CRM)
- Need centralized workflow control
- Want strong context isolation per subagent

**Use Spawned Separate Agents when:**
- Need independent execution contexts
- Different model providers per agent
- Want resilience (one failure doesn't crash all)

**Use Parallel Execution when:**
- Tasks are independent
- Multi-domain research
- Speed matters

**Use Sequential when:**
- Clear dependencies (spec → code → review)
- Progressive refinement workflows
- Each step builds on previous

### Recommended Hybrid Approach for Our Setup

Based on research, use **hierarchical + parallel hybrid**:

```
User → Admin (sequential coordination)
         ↓
    ┌────┴────┐
    ↓         ↓
PM Agent  Codex Agent  (parallel when independent)
    ↓         ↓
    └────┬────┘
         ↓
    Review (sequential)
```

**Why:**
- Admin orchestrates (sequential control)
- PM + Codex can work in parallel on independent tasks
- Review is always sequential gate
- Fits our "Admin reviews → spawns subagent" workflow

### Key Takeaways

1. **Start simple**: Single agent with tools → add agents only when needed
2. **Subagents = centralized control** at cost of +1 call overhead
3. **Parallel = efficiency** for independent tasks
4. **Sequential = quality gates** for dependent workflows
5. **Most production systems use hybrid** - different patterns for different subsystems
- MetaGPT: https://github.com/FoundationAgents/MetaGPT
- CrewAI: https://github.com/crewAIInc/crewAI
- ChatDev: https://github.com/OpenBMB/ChatDev
- CrewAI Agents: https://docs.crewai.com/concepts/agents
- CrewAI Tasks: https://docs.crewai.com/concepts/tasks

---

## Round 3: Additional Framework Scan (OpenAI ecosystem + orchestration-first stacks)

### 1) Microsoft AutoGen
- Positioning: framework for autonomous or human-in-the-loop multi-agent applications.
- Key design signals:
  - explicit multi-agent orchestration
  - tool/MCP integration
  - configurable max tool iterations
  - warning emphasis on trusted tool servers
- Practical takeaway: use bounded tool loops + trust boundaries for external tools.

### 2) LangGraph
- Positioning: low-level graph orchestration for long-running, stateful agents.
- Key design signals:
  - state graph/DAG execution
  - durable execution + resume after failure
  - human-in-the-loop interrupts
  - explicit short-term and long-term memory strategy
- Practical takeaway: represent orchestration as a graph with persisted state and checkpoints.

### 3) OpenAI Swarm (and successor Agents SDK)
- Swarm is educational/experimental; OpenAI recommends Agents SDK for production.
- Core primitive ideas remain valuable:
  - **Agents** + **Handoffs** as first-class building blocks
  - lightweight, controllable routing
- Practical takeaway: design clean handoff contracts and keep agent boundaries simple.

### 4) AutoGPT Platform
- Positioning: platformized agent workflows with deployment and management layer.
- Key design signals:
  - workflow builder mindset (blocks)
  - lifecycle management (test → deploy)
  - ops concerns (hosting, environment requirements)
- Practical takeaway: treat orchestration as product/ops, not just prompts.

---

## Consolidated Best Practices (cross-framework)

1. **Use explicit handoff contracts**
   - Required input schema
   - Expected output schema
   - Failure/retry policy

2. **Persist state between agents**
   - Task state file + checkpointing
   - Never rely on ephemeral chat only

3. **Bound autonomy**
   - Max iterations/tool calls
   - Approval gates before risky actions

4. **Human-in-the-loop at key gates**
   - After PM spec
   - Before merge/deploy

5. **Graph over ad-hoc chains**
   - Model workflow as DAG (including parallel branches)
   - Add explicit rollback/error paths

6. **Observability first**
   - Per-agent logs
   - Task IDs and traceability
   - Runtime metrics (latency, retries, failure reasons)

7. **Role isolation**
   - Separate workspace per agent
   - Principle-of-least-privilege tools/access

---

## Proposed "Correct-first" Architecture for Your Setup

- **Admin (Minimax)**: orchestrator, approvals, task routing
- **PM Agent (Minimax)**: requirements/spec/backlog
- **Dev Agent (OpenAI Codex)**: implementation in dedicated workspace

### Workflow (v1)
1. Admin creates Task ID + brief
2. PM agent outputs spec in structured template
3. Admin approval gate
4. Dev agent implements + test evidence
5. Admin review + integration decision
6. Optional GitHub agent for PR/CI loop

### Required artifacts per task
- `/orchestration/tasks/<task-id>/brief.md`
- `/orchestration/tasks/<task-id>/spec.md`
- `/orchestration/tasks/<task-id>/implementation.md`
- `/orchestration/tasks/<task-id>/review.md`

---

*Research completed: 2026-02-22 (Round 3)*
