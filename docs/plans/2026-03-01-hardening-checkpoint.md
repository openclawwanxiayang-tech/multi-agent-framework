# 2026-03-01 Hardening Checkpoint

## Scope
Security hardening and verification for local OpenClaw host/runtime.

## Baseline (before changes)
- `openclaw security audit --deep`: **1 critical · 3 warn · 1 info**
- Critical finding: Discord `groupPolicy="open"` with elevated tools enabled.
- Warnings: missing `gateway.trustedProxies`, ineffective `gateway.nodes.denyCommands` entries, and permissive credentials directory permissions.

## Changes applied
1. Tightened credentials directory permissions:
   - `chmod 700 ~/.openclaw/credentials`
2. Updated OpenClaw runtime config (`~/.openclaw/openclaw.json`):
   - `channels.discord.groupPolicy: "open" -> "allowlist"`
   - Cleared ineffective `gateway.nodes.denyCommands` values (set to `[]`)
3. Restarted gateway and re-ran verification checks.

## Verification (after changes)
- `openclaw security audit --deep`: **0 critical · 1 warn · 1 info**
- Remaining warning: `gateway.trustedProxies` unset.
  - Acceptable when Control UI remains loopback/local-only.
  - Must be configured if deploying behind reverse proxy.

## Current status summary
- Critical risks addressed.
- Gateway healthy and reachable.
- OpenClaw update available (`2026.2.26`) pending separate approval/execution.

## Commands executed (audit trail)
- `uname -a`
- `cat /etc/os-release`
- `id`
- `whoami`
- `ss -ltnup`
- `(ufw|firewalld|nft) status checks`
- `openclaw status --deep`
- `openclaw security audit --deep`
- `openclaw update status`
- `chmod 700 ~/.openclaw/credentials`
- Gateway config edits in `~/.openclaw/openclaw.json`
- `openclaw gateway restart`
- Post-change re-checks: `openclaw security audit --deep`, `openclaw status --deep`
