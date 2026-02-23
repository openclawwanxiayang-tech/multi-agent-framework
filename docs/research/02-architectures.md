# Architecture Patterns: Subagents, Parallel vs Sequential, Handoffs

Analysis of different architectural patterns for multi-agent systems, including when to use each.

---

## The 4 Core Architecture Patterns

| Pattern | How it works | Best for |
|---------|-------------|----------|
| **Subagents** | Supervisor coordinates subagents as tools. Results flow back through main agent. | Multiple distinct domains, centralized control |
| **Skills** | Single agent loads specialized prompts on-demand | Single agent with many specializations |
| **Handoffs** | Agent transfers control to another based on context | Sequential workflows, customer support |
| **Router** | Classifies input, dispatches to specialized agents in parallel | Distinct verticals, multi-source queries |

---

## Subagents vs Spawned Separate Agents

### Subagents (Centralized)

```
Main Agent
    │
    ├──→ Subagent A →─┤
    │                 │
    ├──→ Subagent B →─┤→ Results accumulate → Main Agent responds
    │                 │
    └──→ Subagent C →─┘
```

| Aspect | Description |
|--------|-------------|
| **Control** | Centralized (all through main) |
| **Context** | Main agent accumulates all context |
| **Latency** | +1 call overhead per task |
| **Debugging** | Single trace |
| **Failure isolation** | Weaker (crashes main) |

### Spawned Separate Agents (Decentralized)

```
Main Agent
    │
    Spawns → Agent A (独立执行)
    Spawns → Agent B (独立执行)
    Spawns → Agent C (独立执行)
    │
    Collects results → Main Agent responds
```

| Aspect | Description |
|--------|-------------|
| **Control** | Decentralized |
| **Context** | Each has isolated context |
| **Latency** | Direct execution |
| **Debugging** | Multiple traces |
| **Failure isolation** | Stronger |

### When to Use Each

**Use Subagents when:**
- Multiple distinct domains (calendar + email + CRM)
- Need centralized workflow control
- Want strong context accumulation

**Use Spawned Separate Agents when:**
- Need independent execution contexts
- Different model providers per agent
- Want resilience (one failure doesn't crash all)

### Research Finding

> From Anthropic: "Multi-agent architecture with lead agent + subagents outperformed single agent by **90.2%**"

---

## Parallel vs Sequential Execution

### Sequential

```
Task A → Task B → Task C → Done
```

**Use when:**
- Clear dependencies
- Progressive refinement
- Each step builds on previous

**Avoid when:**
- Tasks can run independently
- Speed matters

### Parallel

```
┌─ Task A ─┐
│          ├──→ Results → Aggregate → Done
├─ Task B ─┤
└─ Task C ─┘
```

**Use when:**
- Independent tasks
- Multi-domain queries
- Speed matters

**Avoid when:**
- Tasks have dependencies
- Order matters

### Hybrid

```
        ┌─ Task A (independent) ──┐
        │                          │
Task ───┤─ Task B (independent) ──┼──→ Aggregate → Task D → Done
        │                          │
        └─ Task C (depends on A) ─┘
```

**Use when:**
- Complex real-world systems
- Mix of dependent and independent tasks

---

## Performance Comparison (LangChain Research)

### One-shot Request
(e.g., "buy coffee")

| Approach | Calls |
|----------|-------|
| Subagents | 4 |
| Skills/Handoffs/Router | 3 |

### Repeat Request

| Approach | Calls/turn | Context Savings |
|----------|------------|-----------------|
| Subagents | 4 | - |
| Skills/Handoffs | 2 | 40% |

### Multi-domain Query
(e.g., "compare Python, JS, Rust")

| Approach | Calls | Tokens |
|----------|-------|--------|
| Subagents | 5 | ~9K |
| Skills | 3 | ~15K (context accumulation) |
| Router | 5 | ~9K |

---

## Handoff Patterns

### Explicit Handoff Contract

Each handoff should define:

| Element | Description |
|---------|-------------|
| **Required Input Schema** | What the receiving agent needs |
| **Expected Output Schema** | What the receiving agent produces |
| **Failure/Retry Policy** | What happens if it fails |
| **Context Summary** | Brief of what's been done |

### Handoff Implementation

```
Agent A                          Agent B
   │                                │
   │── Handoff Request (with data) ─→│
   │                                │
   │     Processing...              │
   │                                │
   │←── Output / Completion ────────│
   │                                │
```

### Best Practices

1. **Clean handoff contracts** - Define input/output explicitly
2. **Simple agent boundaries** - Don't over-fragment
3. **State persistence** - Never rely on ephemeral chat only
4. **Error propagation** - Pass failures up the chain

---

## Graph-Based Orchestration

### Why Graph Over Ad-hoc Chains?

| Aspect | Ad-hoc Chains | Graph/DAG |
|--------|---------------|-----------|
| **Flexibility** | Fixed order | Dynamic routing |
| **Parallelism** | Hard to add | Natural support |
| **Error handling** | Manual | Built-in paths |
| **State management** | Scattered | Centralized |

### Graph Components

| Component | Description |
|-----------|-------------|
| **Nodes** | Individual agents or tasks |
| **Edges** | Handoffs / dependencies |
| **State** | Shared context across graph |
| **Checkpoints** | Save/restore execution state |

### From LangGraph: Key Design Signals

- **State graph/DAG execution** - Model workflow as directedDurable execution** graph
- ** - Resume after failure from checkpoint
- **Human-in-the-loop interrupts** - Pause for human approval
- **Memory strategy** - Explicit short-term and long-term memory

---

## Recommended Hybrid Approach

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

### Why This Works

1. **Admin orchestrates** - Sequential control for quality gates
2. **PM + Codex can work in parallel** - On independent tasks
3. **Review is always sequential gate** - Human oversight
4. **Fits our "Admin reviews → spawns subagent" workflow**

### Alternative: DAG-Based

```
        ┌─ Research ─┐
        │            │
User ───┤─ Design ───┼──→ Implement ──→ Test ──→ Done
        │            │
        └─ Plan ─────┘
```

---

## Key Takeaways

1. **Start simple**: Single agent with tools → add agents only when needed
2. **Subagents = centralized control** at cost of +1 call overhead
3. **Parallel = efficiency** for independent tasks
4. **Sequential = quality gates** for dependent workflows
5. **Most production systems use hybrid** - different patterns for different subsystems
6. **Graph over chains** - More flexible, better error handling
7. **Persist state** - Never rely on ephemeral chat only

---

## References

- LangChain Research: Multi-agent architectures
- Anthropic: Multi-agent vs single agent performance
- LangGraph: Graph-based orchestration

---

*Last updated: 2026-02-23*
