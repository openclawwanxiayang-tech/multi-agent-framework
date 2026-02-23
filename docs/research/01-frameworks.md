# Framework Deep Dives: MetaGPT, CrewAI, ChatDev

Detailed analysis of the three main multi-agent frameworks that inform our architecture.

---

## MetaGPT

**Philosophy**: "Code = SOP(Team)" — Standard Operating Procedures for AI agent teams

### Core Concepts

| Concept | Description |
|---------|-------------|
| **SOP** | Standard Operating Procedures define explicit workflows for agent collaboration |
| **Role Assignment** | Assign different roles (PM, Architect, Engineer, QA) to LLMs |
| **Shared Context** | Agents share a "memory" / message board |
| **Structured Output** | Requirements → Design → Code → Docs in sequence |

### Architecture

```
Requirement → PM → Architect → Project Manager → Engineer → QA
                     ↓              ↓              ↓         ↓
               Spec/PRD        Task Breakdown   Code    Test Results
```

### Strengths
- Well-defined workflows
- Proven for software development
- Strong research backing (multiple papers)
- Takes one-line requirement → outputs full software

### Weaknesses
- Rigid sequential structure
- Less flexible than CrewAI for non-development tasks

### References
- GitHub: https://github.com/FoundationAgents/MetaGPT
- Paper: "MetaGPT: Meta Programming for Multi-Agent Collaboration"

---

## CrewAI

**Philosophy**: "Role-playing autonomous agents" — Collaborative intelligence

### Core Concepts

| Concept | Description |
|---------|-------------|
| **Agents** | Autonomous entities with roles, goals, backstories |
| **Crews** | Teams of agents working together |
| **Tasks** | Defined objectives with expected output |
| **Tools** | Agents can use tools (similar to OpenClaw skills) |
| **Flows** | Event-driven orchestration for enterprise |

### Agent Attributes

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

| Process | Description |
|---------|-------------|
| **Sequential** | Tasks execute in defined order |
| **Hierarchical** | Manager agent assigns tasks to agents |

### Task Features
- **Context**: Task outputs can feed into subsequent tasks
- **Output Formats**: Raw, JSON, Pydantic models
- **Guardrails**: Validate output before proceeding

### Key Parameters
- `max_iter`: Max iterations before final answer (default: 20)
- `allow_delegation`: Agents can delegate to other agents
- `cache`: Cache tool usage (default: True)
- `max_retry_limit`: Retries on error (default: 2)
- `respect_context_window`: Summarize to stay under limit

### Strengths
- Flexible — agents can be any role
- Built-in tool integration
- Enterprise-ready (Flows, monitoring)
- Large community (100k+ developers)

### References
- GitHub: https://github.com/crewAIInc/crewAI
- Docs: https://docs.crewai.com/concepts/agents

---

## ChatDev (OpenBMB)

**Philosophy**: "Virtual Software Company" — Multi-agent collaboration

### Core Concepts

| Concept | Description |
|---------|-------------|
| **Multi-Agent Seminars** | Agents participate in functional meetings |
| **Puppeteer Paradigm** | Central orchestrator dynamically activates/sequences agents |
| **MacNet** | DAG-based collaboration for 1000+ agents |
| **Zero-Code Config** | Define agents/workflows via config |

### Variants

| Version | Description |
|---------|-------------|
| **ChatDev 1.0** | Virtual software company (CEO, CTO, Programmer roles) |
| **ChatDev 2.0 (DevAll)** | Zero-code platform for any multi-agent system |

### Architecture Patterns
- Chain-based: Sequential handoffs
- DAG-based: Parallel branches with dependencies
- Hierarchical: Manager → Workers

### Strengths
- Scalable to many agents (MacNet supports 1000+)
- Research-backed (NeurIPS 2025 paper)
- Flexible topology (chain, DAG, etc.)
- Zero-code configuration

### References
- GitHub: https://github.com/OpenBMB/ChatDev

---

## Comparison Matrix

| Aspect | MetaGPT | CrewAI | ChatDev |
|--------|---------|--------|---------|
| **Philosophy** | SOP-driven | Role-playing | Virtual Company |
| **Workflow** | Fixed sequential | Flexible sequential/hierarchical | Configurable (chain/DAG) |
| **Scalability** | Medium | Medium | High (1000+ agents) |
| **Tool Integration** | Basic | Extensive | Moderate |
| **Config Style** | Code | Code + YAML | Zero-code JSON |
| **Community** | Growing | Large (100k+) | Research-focused |
| **Best For** | Software dev | Enterprise apps | Scalable systems |

---

## Application to Our Framework

Based on these frameworks, our implementation should:

### From MetaGPT
- Use SOPs for predictable, repeatable workflows
- Implement role-based specialization
- Structure outputs (SPEC.md → design.md → code)

### From CrewAI
- Define agents with Role + Goal + Backstory + Tools
- Use hierarchical process for task assignment
- Build tool integration (GitHub, file ops, etc.)

### From ChatDev
- Support DAG-based execution for parallel tasks
- Allow zero-code workflow configuration
- Scale to multiple developers

### Hybrid Approach

```
User → Admin (Minimax) → Sequential coordination
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

*Last updated: 2026-02-23*
