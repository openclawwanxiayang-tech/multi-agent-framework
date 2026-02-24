# Lessons: Errors & Fixes

Key mistakes and how they were resolved.

## 2026-02-24: Overnight Run Failure
- **Problem**: Only logger cron ran, no actual execution
- **Root cause**: Missing autonomous executor + watchdog escalation
- **Fix**: Created checkpoint + watchdog scripts + work-cycle engine

## 2026-02-24: Session Not Receiving Channel Messages
- **Problem**: Bot only responded to mentions
- **Root cause**: `requireMention: true` in Discord guild config + Message Content Intent not enabled
- **Fix**: Set `requireMention: false` + enabled Message Content Intent in Discord Dev Portal

## 2026-02-24: Polling vs Push
- **Problem**: Relied on polling for channel monitoring
- **Fix**: Enabled Discord streaming mode + real-time message push

## 2026-02-24: Watchdog False Positives
- **Problem**: Alerted on "no commit >90m" during healthy longrun
- **Fix**: Need to correlate commit staleness with work-cycle output (future improvement)
