# HEARTBEAT.md

## Active heartbeat tasks (overnight autonomous run)

1. Every heartbeat poll, verify the run log is still being updated:
   - File: `docs/plans/2026-02-23-overnight-autonomous-run-log.md`
   - Alert if no new AUTO_LOG/PROGRESS entry for > 20 minutes.

2. Verify cron logger is configured and present:
   - `crontab -l` should contain `push_progress_log.sh`.
   - Alert if missing.

3. Verify overnight work is advancing:
   - Check latest commit timestamp in workspace git.
   - Alert if no new commit for > 90 minutes during the 12h run window.

4. Verify TODO board is being maintained:
   - File: `docs/plans/2026-02-23-overnight-todo.md`
   - Alert if missing, or if no status changes/update entries for > 30 minutes during active run.

5. If all checks pass, return `HEARTBEAT_OK`.
