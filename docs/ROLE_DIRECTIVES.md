# Role-specific Directives (Execution Templates)

## PM
- Produce only schema-aligned SPEC artifacts: `artifacts/spec/spec.md` and `artifacts/spec/acceptance.md`.
- Own semantic decisions: lock semantics, stage set, and DoD criteria.
- Any policy/schema change must update docs + changelog.

## Designer
- Produce `artifacts/design/design.md` with sections: Architecture, UX assumptions, Error states, Test considerations.
- Follow path contract exactly; do not invent folders.

## Dev
- Implement MVP spine before adding new features.
- Treat schemas as canonical truth.
- Keep runtime deterministic and testable.

## QA
- Add stage-gate failure tests and drift checks.
- Validate lock stale-reclaim and restart/resume behavior.
- Open blocker issues on schema/doc/runtime drift.

## Release
- Maintain CI guardrails (schema + required-files + stage validators).
- Keep one local command for end-to-end golden task validation.
