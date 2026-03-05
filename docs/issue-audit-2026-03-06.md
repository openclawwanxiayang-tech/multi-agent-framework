# Issue Audit Report - 2026-03-06

## Executive Summary
- **Total Open Issues**: 41
- **Bucket Classification**:
  - A) Keep (still valid): ~25
  - B) Reframe (needs rewriting): ~8
  - C) Merge (duplicates): ~3
  - D) Close (done/wrong direction): ~5

## Classification Table

| # | Title | Bucket | Action | Notes |
|---|-------|--------|--------|-------|
| 156 | DataPack: Expand skill synergy | B | Reframe | Align with modifier pipeline P0 |
| 155 | Engine: Formalize skill misc breakdown | B | Reframe | Part of P0-2 modifier pipeline |
| 154 | Engine/DataPack: Pre-index modifiers | B | Reframe | Part of P0-2 modifier pipeline |
| 151 | Split App.tsx | A | Keep | Tech debt, valid |
| 149 | Split locale files | A | Keep | Tech debt, valid |
| 148 | Localize feats | A | Keep | Part of Epic #145 |
| 147 | Localize skills | A | Keep | Done, can close |
| 145 | Epic: Localization | A | Keep | Valid epic |
| 142 | Expand unresolved-rules fixtures | A | Keep | Valid |
| 141 | Expand SRD equipment | A | Keep | Valid |
| 139 | ACP handling for Ride | B | Reframe | Part of P0-2 modifier pipeline |
| 135 | Craft/Profession catalog | A | Keep | Valid long-term |
| 133 | Group specialized skills | A | Keep | Valid |
| 132 | Specialized skill rollout | B | Reframe | Overlaps with 133, 135 |
| 131 | Review sheet 0-rank skills | A | Keep | User-facing bug |
| 126 | Epic: Persistence UX | A | Keep | Valid epic |
| 125 | Epic: Wizard Reliability | B | Reframe | Must be UI-only |
| 124 | Epic: Rules/Data Integrity | A | Keep | Valid epic |
| 123 | E2E: Race step | D | Downgrade | E2E → temp only, add note |
| 122 | Generalize skill budget | B | Merge | Into #95 (done) |
| 115 | Racial bonus in sheetViewModel | A | Keep | Valid |
| 114 | AC labels localization | A | Keep | Valid |
| 111 | Reshape attacks/damage | A | Keep | Valid |
| 110 | schemaVersion for sheetViewModel | B | Reframe | Core P0-1 |
| 96 | Contract tests: skill budget | B | Reframe | Part of P0-3 |
| 92 | Sheet Spec compliance | A | Keep | Valid |
| 91 | Expand skill dataset | B | Reframe | Done in #70 |
| 90 | Never render raw IDs | A | Keep | Valid |
| 89 | Localization layer | A | Keep | Valid |
| 88 | Epic: Flow-driven wizard | B | Reframe | Must be UI-only |
| 86 | Contract snapshot for Sheet | B | Reframe | Part of P0-3 |
| 85 | Feat text rendering | A | Keep | Valid |
| 84 | Epic: Unresolved Rules | A | Keep | Valid epic |
| 83 | Epic: Skills | A | Keep | Valid epic |
| 82 | Minimal equipment model | A | Keep | Valid |
| 79 | Export/import UX | A | Keep | Valid |
| 78 | Pack tooling | A | Keep | Valid |
| 77 | Feat legality | A | Keep | Valid |
| 76 | Unresolved rules UX | A | Keep | Valid |
| 74 | Refactor engine modules | B | Reframe | Align with P0-1 engine API |

## New P0 Issues to Create

### P0-1: Engine API - compute(CharacterSpec, Rulepack) -> SheetViewModel + Validation + Unresolved
