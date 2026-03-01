# Repository Scope Policy

This repository is for the **multi-agent framework product artifacts** only.

## In Scope
- framework architecture, tasks, schemas, and agent definitions
- implementation docs directly tied to the framework

## Out of Scope (must stay in myOpenClaw)
- local runtime logs/state (`.logs/`, `.openclaw/`, `.pi/`)
- personal assistant identity/memory files (`SOUL.md`, `USER.md`, etc.)
- local personal skill/memory bundles (`skills/`, `memory/`)

## Repo Boundary Guard
If `myOpenClaw/` exists as a sibling/nested working folder during local operations, treat it as a separate git repository. Progress/status scripts in this repo must report only `multi-agent-framework` unless explicitly designed for cross-repo reporting.

## Migration Reference
Out-of-scope artifacts were migrated to:
- `openclawwanxiayang-tech/myOpenClaw`
- PR: #2
- Snapshot path: `migrations/multi-agent-framework/2026-03-01/`
