# Source of Truth & Versioning Policy

> Version: 1.0.0  
> Last Updated: 2026-03-02

## Hierarchy (highest to lowest)

1. **Schemas** (`docs/schemas/*.json`)
2. **Validators** (`validators/*.py`) for enforceable checks
3. **Orchestrator runtime behavior** (`scripts/run_pipeline.py` and related code)
4. **Normative docs** (`docs/*.md`)
5. **Agent prompts/instructions** (`.github/agents/*.md`)
6. **Example artifacts/fixtures** (`artifacts/tasks/**`)

If conflict exists, resolve upward in this order.

## Versioning

- All contracts include `$version`.
- Current contract major: `1.x`.

### Compatibility rules

- **Patch** (`1.0.0 -> 1.0.1`): typo/docs fixes, no schema shape change.
- **Minor** (`1.0.0 -> 1.1.0`): backward-compatible optional fields, tighter docs.
- **Major** (`1.x -> 2.0.0`): breaking schema change (field rename/removal/type change).

### Change process

Any schema or policy change must include:
1. schema update
2. validator/runtime update (if applicable)
3. docs update
4. changelog entry (`CHANGELOG.md`)

## Runtime acceptance

A task artifact is accepted only when:
- JSON validates against schema for its `$version`
- stage validators pass
- state transition is allowed by `docs/STAGES.md`
