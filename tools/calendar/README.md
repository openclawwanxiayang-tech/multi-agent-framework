# Google Calendar Direct API Setup

## One-time setup

1. Google Cloud Console → APIs & Services
2. Enable **Google Calendar API**
3. OAuth consent screen: add your account as a test user
4. Create OAuth Client ID: **Desktop app**
5. Download JSON to:

`tools/calendar/credentials.json`

## First auth run (one-time)

```bash
node tools/calendar/gcal_quick.mjs list \
  --time-min 2026-03-01T00:00:00+08:00 \
  --time-max 2026-03-31T23:59:59+08:00
```

This opens Google consent once and saves token at:

`tools/calendar/token.json`

## Quick usage

Create timed event:

```bash
node tools/calendar/gcal_quick.mjs create \
  --title "TRPG 龙金劫 (Online)" \
  --timezone Australia/Adelaide \
  --start 2026-03-22T17:00:00+10:30 \
  --end 2026-03-22T20:00:00+10:30
```

Create all-day event:

```bash
node tools/calendar/gcal_quick.mjs create \
  --title "Fly: Zhengzhou → Adelaide" \
  --all-day --start-date 2026-03-21 --end-date 2026-03-22
```

Update event:

```bash
node tools/calendar/gcal_quick.mjs update \
  --event-id <EVENT_ID> \
  --start 2026-03-22T10:30:00+10:30 \
  --end 2026-03-22T11:00:00+10:30
```
