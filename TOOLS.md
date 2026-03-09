# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

### Discord

- multi-agent-framework repo channel: `1478244412508209237`

### Assistant Operating Rules

- Evaluate each task before execution.
- Run a quick brainstorming/clarification pass first to frame scope, assumptions, and success criteria.
- Ask clarifying questions when scope/intent is ambiguous or decisions are user-preference sensitive.
- If scope is clear and the operation is low-risk, execute directly first.
- If configuration/runtime issues are detected, run a doctor-style diagnose+fix pass proactively before escalating.
- If current skills are insufficient for quality execution, find and install a suitable skill, then continue.
- Record user operating preferences implicitly when clearly expressed.
- Keep channel/session boundaries strict: new channel = separate session context (do not route through unrelated DM session).

### Skill Proactivity Policy (Jane preference)

- Default behavior: proactively check whether a specialized skill exists before starting non-trivial tasks.
- If one suitable skill exists, use it directly.
- If multiple candidate skills exist, pick the most specific skill for the task and proceed.
- If no suitable skill is installed, proactively search/fetch/install from ClawHub, then execute.
- Before any new skill installation, run a security scan first (prefer `skill-scan` / `skill-scanner`) and only proceed if scan result is clean or risk is explicitly approved.
- Treat downloaded skills as untrusted until scanned; avoid executing newly installed skill actions before scan completion.
- Do not wait for explicit user instruction to install/enable a missing skill when it clearly improves execution quality.
- After installing a new skill, briefly report: what was installed, scan result, and why.

### Markdown Length & Structure Policy (Jane preference)

- Keep markdown files concise by default.
- Target maximum length: 100 lines per markdown file (especially memory files).
- If a markdown file grows beyond 100 lines, split it into focused subfiles.
- Maintain one index/TOC file per folder to link and organize split files.
- Prefer append-to-right-file over expanding a catch-all long document.


## Codex Session Rules (Jane's preference)

### How to Run
- Use `codex` command (not sessions_spawn) to run in terminal
- Worktree: /mnt/d/aiProjects/workspaces/DndCharacterBuilder-tech-debt
- Branch: feature/tech-debt (for tech debt issues)

### Session Lifecycle
- **One session per issue** - spawn session when starting work on an issue
- **Session stays alive until issue is closed** - not just until task completes
- After PR merges and issue closes, THEN the session can close
- Monitor PR status, address review comments, re-request reviews as needed

### Workflow
1. Create worktree if needed: `git worktree add /path -b feature/xxx`
2. Spawn interactive codex: `codex` (in the worktree directory)
3. Give Codex the issue to work on
4. Monitor until PR is merged
5. Close issue after merge
6. Only THEN close the session
