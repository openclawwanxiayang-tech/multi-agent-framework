# Lessons: Decisions & Rationale

Important choices and why.

## Operations Boundary
- Keep runtime automation outside product repo
- Location: `/home/lenovo/.openclaw/ops/longrun/`

## Push Policy
- Push only when checks pass
- WIP commit on failure, no push

## Session Map Strategy
- Poll-based sync every 5 minutes
- Manual trigger after session actions

## Memory System
- Use OpenClaw native markdown-first memory

## Documentation Discipline
- Every material change updates docs + issues + PRs

## Review Gate Policy (2026-03-01)
- For delivered work, always push to remote and open an MR/PR for review and approval.
- Treat this as default workflow unless explicitly told otherwise.
