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

