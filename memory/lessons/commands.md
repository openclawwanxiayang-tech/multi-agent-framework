# Lessons: Commands & Automation

Key commands and automation patterns that work.

## OpenClaw CLI
- `openclaw gateway restart` — Restart gateway
- `openclaw status` — Check system status
- `openclaw config get/set` — Manage config

## Cron Jobs
- `*/15` — progress log
- `*/30` — checkpoint
- `*/10` — watchdog
- `*/5` — session map sync

## Discord
- Enable message content: set `requireMention: false` in guild config
- Channel monitoring via Discord push (no polling needed)

## Session Management
- Session map: `/home/lenovo/.openclaw/ops/longrun/config/channel-map.json`
- Sync script: `sync_session_map.sh`
