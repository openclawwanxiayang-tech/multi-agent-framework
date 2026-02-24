# Model Routing

## Primary Models
- openai-codex (gpt-5.3-codex) — default for coding/reasoning
- minimax-m2.1 — fast, low cost
- minimax-m2.5 — better reasoning
- openai-research — deep research

## Routing
| Task | Model |
|------|-------|
| Code implementation | openai-codex |
| PR review | openai-codex |
| Research | openai-codex |
| Quick Q&A | minimax-m2.1 |
| Complex reasoning | minimax-m2.5 |
| Deep research | openai-research |

See myOpenClaw/config/model-routing.md for full rules.
