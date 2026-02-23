# Multi-Agent LLM Research Literature Review (2024–2026)

## Executive Summary
This review surveys recent work on LLM-based multi-agent systems (MAS), focusing on coordination mechanisms, scaling behavior, evaluation, and failure analysis. The field is moving from single-agent tool use to structured teams of specialized agents (planner/executor/critic/verifier), with growing evidence that coordination quality—not just base model quality—strongly affects outcomes. At the same time, newer papers show that many gains are fragile and highly dependent on protocol design, role assignment, and verification loops.

Key trend: inference-time orchestration (agent topology + communication protocol + reflection) is becoming a practical alternative to retraining larger base models.

---

## Scope and Method
- Time window: primarily 2024–2026
- Focus: multi-agent LLM systems, not generic MARL unless directly tied to LLM agents
- Priority: peer-reviewed venues + high-impact arXiv preprints
- Sources collected via OpenReview, conference proceedings (ICLR/NeurIPS), and arXiv

---

## Major Themes and Trends

### 1) Structured collaboration beats naive parallelism
Recent systems increasingly use explicit collaboration structures (chain/tree/graph, manager-worker, planner-critic loops). Papers report that topology and communication protocol can materially affect success rates.

### 2) Inference-time scaling laws for agents
Work such as MacNet studies whether adding collaborating agents at inference can yield scaling gains analogous to model-size scaling. Early evidence suggests logistic-like improvement curves, with diminishing returns and topology sensitivity.

### 3) Reflection and verification are central
Reflection mechanisms (self/peer/shared-reflector) and verifier roles improve robustness, but introduce cost/latency. Better credit assignment for “which reflection helped” remains an open area.

### 4) Evaluation is shifting from outcome-only to process-aware
Benchmarks now include milestone-based KPIs, collaboration/competition quality, and failure attribution rather than only final task success.

### 5) Failure analysis has become a first-class research topic
New taxonomies and datasets (e.g., MAST-Data) show many MAS failures stem from system design and inter-agent misalignment rather than base-model inability alone.

---

## Notable Papers (Selected)

| Paper | Venue/Year | Contribution |
|---|---|---|
| AgentBench: Evaluating LLMs as Agents | ICLR 2024 | Foundational benchmark across interactive environments; highlighted gaps in long-horizon reasoning and instruction following. |
| Chain of Agents: LLMs Collaborating on Long-Context Tasks | NeurIPS 2024 | Worker-manager chain for segmented long-context reasoning; reports gains over common long-context baselines. |
| Reflective Multi-Agent Collaboration based on LLMs (COPPER) | NeurIPS 2024 | Reflection-centric MAS with shared reflector + counterfactual reward ideas to improve agent collaboration quality. |
| Scaling LLM-based Multi-Agent Collaboration (MacNet) | ICLR 2025 | Studies large-scale collaborative networks; reports topology effects and collaborative scaling behavior. |
| MultiAgentBench: Evaluating Collaboration and Competition of LLM Agents | arXiv 2025 (reported ACL’25 project release) | Multi-agent benchmark with milestone-based KPIs and protocol/topology comparisons. |
| Why Do Multi-Agent LLM Systems Fail? (MAST/MAST-Data) | arXiv 2025 | Failure taxonomy and annotated traces; categorizes recurring MAS failure modes and diagnosis pipeline. |
| Large Language Model based Multi-Agents: A Survey of Progress and Challenges | arXiv 2024 | Broad survey of domains, communication patterns, and benchmark landscape. |
| Multi-Agent Collaboration Mechanisms: A Survey of LLMs | arXiv 2025 | Collaboration-focused taxonomy (actors, collaboration type, structures, strategies, protocols). |
| FinCon: A Synthesized LLM Multi-Agent System for Financial Decision Making | NeurIPS 2024 | Domain-focused manager/analyst MAS; demonstrates practical hierarchical collaboration in finance tasks. |
| Fine-Tuning LLM with Sequential Cooperative Multi-Agent RL (CORY) | NeurIPS 2024 | Explores cooperative multi-agent RL-style fine-tuning for improved coordinated behavior. |
| Competing LLMs in Multi-Agent Gaming Environments | ICLR 2025 | Competition-centric evaluation of strategic behavior under multi-agent game settings. |
| Reinforce LLM Reasoning through Multi-Agent Reflection | 2025 (OpenReview) | Uses multi-agent reflection with RL-style optimization to improve reasoning outcomes. |

---

## Methodological Taxonomy

### A. Organization and Topology
- **Star/manager-worker**: strong control, easier governance, possible bottleneck
- **Chain**: simple and interpretable, vulnerable to error propagation
- **Tree/graph**: high expressivity and parallel depth, harder to debug

### B. Role Design
- Planner, researcher, executor, critic, verifier
- Homogeneous swarms vs heterogeneous specialists

### C. Communication Protocol
- Round-based discussion
- Milestone/contract-driven handoffs
- Shared memory (blackboard) vs pairwise messaging

### D. Learning Regime
- Prompt-orchestrated (no training)
- Trained reflection/coordination modules
- RL-style credit assignment for agent contributions

### E. Interaction Pattern
- Cooperation
- Competition
- Coopetition (mixed incentives)

---

## Benchmarks and Metrics

### Common benchmarks
- **AgentBench** (interactive agent capabilities)
- **MultiAgentBench** (collaboration + competition dynamics)
- Long-context task suites used in CoA-style evaluations

### Common metrics
- Task success / accuracy
- Milestone completion rates
- Collaboration quality indicators (agreement/helpfulness/coordination quality)
- Robustness across seeds/tasks/models
- Cost and latency (often underreported but deployment-critical)

---

## Open Challenges
1. **Cost-latency-quality tradeoff**: better coordination can be expensive at inference.
2. **Coordination fragility**: prompt and role design changes can cause unstable outcomes.
3. **Verification reliability**: verifier agents still fail on subtle errors/hallucinations.
4. **Benchmark realism**: many setups are still less messy than production workflows.
5. **Reproducibility**: framework versions and orchestration details heavily influence results.
6. **Safety/alignment in groups**: collusion, deception, and hidden-channel behavior need stronger controls.

---

## Practical Recommendations for This Repo (multi-agent-framework)
1. Start with a minimal reliable team: **PM → Dev → Critic → QA/Verifier**.
2. Use explicit handoff contracts (input schema, output schema, done criteria).
3. Add verifier checkpoints before task closure (artifact-level acceptance criteria).
4. Log failure modes using a lightweight taxonomy (design, alignment, verification).
5. Track per-role token/latency budgets to prevent orchestration bloat.
6. Prefer deterministic protocols first; add adaptive collaboration only when needed.

---

## References
- AgentBench (ICLR 2024, OpenReview): https://openreview.net/forum?id=zAdUB0aCTQ
- Chain of Agents (OpenReview): https://openreview.net/forum?id=LuCLf4BJsr
- Chain of Agents (arXiv): https://arxiv.org/abs/2406.02818
- Reflective Multi-Agent Collaboration / COPPER (OpenReview): https://openreview.net/forum?id=wWiAR5mqXq
- Reflective Multi-Agent Collaboration (NeurIPS proceedings): https://proceedings.neurips.cc/paper_files/paper/2024/hash/fa54b0edce5eef0bb07654e8ee800cb4-Abstract-Conference.html
- Scaling LLM-based Multi-Agent Collaboration / MacNet (OpenReview): https://openreview.net/forum?id=K3n5jPkrU6
- MultiAgentBench (arXiv): https://arxiv.org/abs/2503.01935
- Why Do Multi-Agent LLM Systems Fail? (arXiv): https://arxiv.org/abs/2503.13657
- LLM-based Multi-Agents Survey (arXiv 2024): https://arxiv.org/abs/2402.01680
- Multi-Agent Collaboration Mechanisms Survey (arXiv 2025): https://arxiv.org/abs/2501.06322
- FinCon (NeurIPS abstract): https://proceedings.neurips.cc//paper_files/paper/2024/hash/f7ae4fe91d96f50abc2211f09b6a7e49-Abstract-Conference.html
- Fine-Tuning LLM with Sequential Cooperative Multi-Agent RL (NeurIPS PDF): https://papers.nips.cc/paper_files/paper/2024/file/1c2b1c8f7d317719a9ce32dd7386ba35-Paper-Conference.pdf

---

## Notes on Evidence Strength
- Peer-reviewed conference papers were prioritized where possible.
- Several 2025 items are currently arXiv/OpenReview and may evolve before final archival publication.
- Comparative claims should be interpreted with benchmark/protocol differences in mind.
