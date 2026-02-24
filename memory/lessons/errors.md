# Lessons: Errors & Fixes

Key mistakes and how they were resolved.

## 2026-02-24: Overnight Run Failure
- **Problem**: Only logger cron ran, no actual execution
- **Fix**: Created checkpoint + watchdog scripts + work-cycle engine

## 2026-02-24: Session Not Receiving Channel Messages
- **Problem**: Bot only responded to mentions
- **Fix**: Set `requireMention: false` + enabled Message Content Intent

## 2026-02-24: Polling vs Push
- **Problem**: Relied on polling for channel monitoring
- **Fix**: Enabled Discord streaming mode + real-time message push
