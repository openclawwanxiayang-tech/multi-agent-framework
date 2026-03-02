#!/usr/bin/env python3
"""
generate_summary.py - Generate run summary from events.ndjson

Creates a summary.md for a task showing:
- Timeline of events
- Stage transitions
- Agent actions
- Duration metrics
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def generate_summary(task_path: Path) -> str:
    """Generate summary.md from events.ndjson."""
    events_path = task_path / "logs" / "events.ndjson"
    
    if not events_path.exists():
        return "# No events found\n"
    
    events = []
    with open(events_path) as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))
    
    if not events:
        return "# No events found\n"
    
    # Get task info
    task_id = events[0].get("task_id", "unknown")
    
    # Build timeline
    timeline = []
    stage_times = {}
    prev_time = None
    
    for e in events:
        ts = e.get("timestamp", "")
        stage = e.get("stage", "")
        event_type = e.get("event", "")
        actor = e.get("actor", "system")
        
        timeline.append(f"- **{ts}** [{stage}] {event_type} by {actor}")
        
        if event_type == "STAGE_STARTED":
            stage_times[stage] = {"start": ts}
        elif event_type == "STAGE_COMPLETED" and stage in stage_times:
            stage_times[stage]["end"] = ts
    
    # Calculate durations
    duration_lines = ["## Durations", ""]
    for stage, times in stage_times.items():
        if "start" in times and "end" in times:
            try:
                start = datetime.fromisoformat(times["start"].replace("Z", "+00:00"))
                end = datetime.fromisoformat(times["end"].replace("Z", "+00:00"))
                dur = (end - start).total_seconds()
                duration_lines.append(f"- {stage}: {dur:.1f}s")
            except:
                pass
    
    # Generate summary
    summary = f"""# Run Summary: {task_id}

## Timeline

"""
    summary += "\n".join(timeline)
    summary += "\n\n"
    summary += "\n".join(duration_lines)
    summary += "\n\n## Summary\n"
    summary += f"- Total events: {len(events)}\n"
    summary += f"- Stages: {len(stage_times)}\n"
    
    return summary


def main():
    if len(sys.argv) < 2:
        print("Usage: generate_summary.py <task-path>")
        sys.exit(1)
    
    task_path = Path(sys.argv[1])
    summary = generate_summary(task_path)
    print(summary)
    
    # Optionally write to logs/summary.md
    summary_path = task_path / "logs" / "summary.md"
    summary_path.write_text(summary)
    print(f"\n[Wrote to {summary_path}]")


if __name__ == "__main__":
    main()
