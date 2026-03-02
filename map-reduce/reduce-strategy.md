# Reduce Strategy v1

> How to merge/select outputs from multiple mappers.

## Strategies

### 1. Best-of-N

Select the output with highest aggregate score.

```
aggregate = Σ(criteria_scores[key] * weight[key])
```

**Use case**: When quality is paramount, run N mappers in parallel.

### 2. Vote

Each mapper votes on each criterion. Select output with most votes.

**Use case**: When there's a clear right/wrong answer.

### 3. Verifier

Run outputs through a verifier agent that scores each.

**Use case**: Complex tasks requiring judgment.

## Configuration

```json
{
  "$version": "1.0.0",
  "task_id": "T-2026-MVP-001",
  "reduce_strategy": "best-of-n|vote|verifier",
  "weights": {
    "correctness": 0.4,
    "efficiency": 0.3,
    "readability": 0.3
  },
  "min_mappers": 2,
  "max_mappers": 5
}
```

## Process

1. **Collect** all mapper outputs within timeout
2. **Score** each against criteria
3. **Apply** selected strategy
4. **Publish** final artifact to blackboard
5. **Log** reduce event with trace_id
