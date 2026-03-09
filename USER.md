# USER.md - About Your Human

_Learn about the person you're helping. Update this as you go._

- **Name:** JaneYang
- **What to call them:** Jane (or whatever you prefer)
- **Pronouns:** _(optional)_
- **Timezone:** Asia/Shanghai
- **Notes:**
  - Prefers GitHub backup to include assistant memory/docs; only sensitive data should be gitignored (credentials, passwords, personal/private info).
  - For issue execution, user expects dependency-aware ordering, not naive latest-first.
  - Current required ordering for deferred-mechanics track: #62 (plan) -> #60 (implementation) -> #63 (engine output surfacing).
  - When multiple issues exist, assistant should explicitly compute and confirm a reasonable order before implementation.
  - User asked this preference to be written down and remembered.
  - Working on: DND Character Builder - a user-friendly, data-driven, extensible character builder tool.
  - For Discord bot setup, user wants new bots (e.g., PR Review Bot) to match existing bot channel access (same channel visibility/permissions), not just minimal baseline.
  - When installing/downloading new skills, run safety scan first (use security scanning skills) before enabling/using them.
  - Keep markdown docs concise; target <=100 lines per file (especially memory docs). Split long markdown into focused files and maintain a TOC/index file.
  - Assistant should run a brainstorming/clarification pass first to frame scope and success criteria, then ask clarifying questions when scope or intent is ambiguous; when scope is clear and action is low-risk, execute directly first and only ask user when blocked by permissions/access/platform limits.
  - If configuration issues are detected, assistant should proactively run diagnosis/fix workflow ("doctor fix") before asking user.
  - For Codex/ACP delegated work, proactively monitor session health (especially ACP/acpx failure patterns), surface blockers early, and recover/retry quickly instead of waiting for user nudges.
  - Keep channel contexts strictly isolated: for different channels, run separate parallel agent/session lanes and never mix task context across channels.

## Context

_(What do they care about? What projects are they working on? What annoys them? What makes them laugh? Build this over time.)_

---

The more you know, the better you can help. But remember — you're learning about a person, not building a dossier. Respect the difference.
