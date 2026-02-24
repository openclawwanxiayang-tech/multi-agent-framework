# Lessons: Decisions & Rationale

Important choices and why they were made.

## 2026-02-24: Operations Boundary
- **Decision**: Keep runtime automation outside product repo
- **Rationale**: Product repo should focus on reusable framework, not host-specific ops
- **Location**: `/home/lenovo/.openclaw/ops/longrun/`

## 2026-02-24: Push Policy
- **Decision**: Push only when checks pass; WIP commit on failure
- **Rationale**: Safety first, no broken builds pushed

## 2026-02-24: Session Map Strategy
- **Decision**: Poll-based sync every 5 minutes (not real-time trigger)
- **Rationale**: OpenClaw doesn't emit session-create events; polling is reliable fallback
- **Manual trigger**: After session actions, run sync script

## 2026-02-24: Memory System
- **Decision**: Use OpenClaw native memory (markdown-first, hybrid retrieval)
- **Rationale**: Already built-in, inspectable, git-friendly, no external deps

## 2026-02-24: Documentation Discipline
- **Decision**: Every material change updates docs + issues + PRs
- **Rationale**: Maintain traceability, avoid silent drift
