#!/usr/bin/env python3
"""Clear stale cron locks before gateway starts.

This script removes runningAtMs from jobs.json to prevent
stale cron locks from persisting across gateway restarts.

Usage:
  python3 clear_cron_locks.py
"""
import json
import pathlib

def main():
    p = pathlib.Path.home() / ".openclaw/cron/jobs.json"
    if not p.exists():
        print("No jobs.json found")
        return
    
    data = json.loads(p.read_text())
    jobs = data.get("jobs", [])
    
    cleared = 0
    for j in jobs:
        if "runningAtMs" in j:
            del j["runningAtMs"]
            cleared += 1
    
    if cleared:
        p.write_text(json.dumps(data, indent=2))
        print(f"Cleared {cleared} stale locks")
    else:
        print("No stale locks found")

if __name__ == "__main__":
    main()
