# Verifier Role

> Criteria and process for verifying map-reduce outputs.

## Verifier Responsibilities

1. **Fetch** all candidate outputs from blackboard
2. **Evaluate** each against acceptance criteria
3. **Score** using defined rubrics
4. **Report** findings with evidence

## Evaluation Rubric

| Criterion | Score Range | Description |
|-----------|-------------|-------------|
| Correctness | 0.0-1.0 | Does it solve the problem? |
| Efficiency | 0.0-1.0 | Time/space complexity |
| Robustness | 0.0-1.0 | Error handling, edge cases |
| Readability | 0.0-1.0 | Code clarity, docs |

## Verification Output

```json
{
  "$version": "1.0.0",
  "verifier_id": "verifier-001",
  "task_id": "T-2026-MVP-001",
  "outputs_verified": [
    {
      "output_id": "out-001",
      "worker_id": "worker-dev-001",
      "scores": {
        "correctness": 0.95,
        "efficiency": 0.85,
        "robustness": 0.80,
        "readability": 0.90
      },
      "aggregate": 0.875,
      "passed": true,
      "evidence": "All test cases pass..."
    }
  ],
  "recommended_output": "out-001",
  "verified_at": "2026-03-02T12:05:00Z"
}
```

## Conflict Resolution

If outputs have similar scores:
1. Prefer higher correctness
2. If tied, prefer earlier submission
3. If still tied, escalate to human
