#!/usr/bin/env python3
"""Minimal pipeline orchestrator spine (issue #29).

Capabilities:
- init_task: create task folder + task.json/state.json/logs
- append_event: append schema-shaped NDJSON events
- transition: guarded stage transition with lock + validator checks
- run: execute linear pipeline SPEC->DESIGN->IMPLEMENT->REVIEW->QA->RELEASE->DONE
"""

from __future__ import annotations

import argparse
import json
import os
import re
import socket
import subprocess
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = ROOT / "artifacts" / "tasks"
TASK_ID_RE = re.compile(r"^T-\d{4}-(?:\d{2}-\d{2}-\d{3}|MVP-\d{3})$")

STAGES = ["SPEC", "DESIGN", "IMPLEMENT", "REVIEW", "QA", "RELEASE", "DONE"]
ALLOWED_EDGES = {
    "SPEC": ["DESIGN"],
    "DESIGN": ["IMPLEMENT"],
    "IMPLEMENT": ["REVIEW"],
    "REVIEW": ["QA"],
    "QA": ["RELEASE"],
    "RELEASE": ["DONE"],
    "DONE": [],
}
VALIDATOR_BY_STAGE = {
    "SPEC": "validators/spec_validator.py",
    "DESIGN": "validators/design_validator.py",
    "IMPLEMENT": "validators/code_linter.py",
    "QA": "validators/qa_checker.py",
}


def validate_task_id(task_id: str) -> None:
    if "/" in task_id or "\\" in task_id or ".." in task_id:
        raise ValueError(f"Invalid task_id path content: {task_id}")
    if not TASK_ID_RE.fullmatch(task_id):
        raise ValueError(f"Invalid task_id format: {task_id}")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def atomic_write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def append_event(task_dir: Path, event: dict) -> None:
    log = task_dir / "logs" / "events.ndjson"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


@dataclass
class LeaseLock:
    path: Path
    owner_id: str
    ttl_seconds: int = 300

    def _payload(self) -> dict:
        now = utc_now()
        return {
            "$version": "1.0.0",
            "owner_id": self.owner_id,
            "host_id": socket.gethostname(),
            "pid": os.getpid(),
            "acquired_at": now,
            "heartbeat_ts": now,
            "ttl_seconds": self.ttl_seconds,
        }

    def acquire(self) -> None:
        if self.path.exists():
            cur = json.loads(self.path.read_text(encoding="utf-8"))
            hb = cur.get("heartbeat_ts", cur.get("acquired_at"))
            hb_ts = datetime.fromisoformat(hb.replace("Z", "+00:00")).timestamp()
            if time.time() - hb_ts <= int(cur.get("ttl_seconds", 300)):
                raise RuntimeError(f"Lock held by {cur.get('owner_id')}")
            append_event(
                self.path.parent,
                {
                    "$version": "1.0.0",
                    "trace_id": f"{self.path.parent.name}-lock-{int(time.time())}",
                    "task_id": self.path.parent.name,
                    "ts": utc_now(),
                    "agent": self.owner_id,
                    "type": "lock_reclaimed",
                    "details": {
                        "lock_path": str(self.path.relative_to(ROOT)),
                        "prev_owner_id": cur.get("owner_id"),
                        "prev_pid": cur.get("pid"),
                    },
                },
            )
            self.path.unlink(missing_ok=True)
        atomic_write_json(self.path, self._payload())

    def heartbeat(self) -> None:
        if not self.path.exists():
            return
        cur = json.loads(self.path.read_text(encoding="utf-8"))
        cur["heartbeat_ts"] = utc_now()
        atomic_write_json(self.path, cur)

    def release(self) -> None:
        self.path.unlink(missing_ok=True)


def init_task(task_id: str, title: str) -> Path:
    validate_task_id(task_id)
    task_dir = TASKS_DIR / task_id
    (task_dir / "artifacts" / "spec").mkdir(parents=True, exist_ok=True)
    (task_dir / "artifacts" / "design").mkdir(parents=True, exist_ok=True)
    (task_dir / "artifacts" / "impl").mkdir(parents=True, exist_ok=True)
    (task_dir / "artifacts" / "qa").mkdir(parents=True, exist_ok=True)
    (task_dir / "artifacts" / "release").mkdir(parents=True, exist_ok=True)
    (task_dir / "logs").mkdir(parents=True, exist_ok=True)

    task = {
        "$version": "1.0.0",
        "task_id": task_id,
        "title": title,
        "created_at": utc_now(),
        "mode": "pipeline",
        "risk_tier": "low",
        "definition_of_done": ["Spec approved", "Design approved", "Implementation merged", "Tests passing"],
        "budgets": {"max_tool_calls": 50, "max_total_tokens": 100000},
    }
    state = {
        "$version": "1.0.0",
        "task_id": task_id,
        "stage": "SPEC",
        "status": "PENDING",
        "assigned": [],
        "retries": {},
        "next": ["DESIGN"],
        "checkpoints": [],
    }
    atomic_write_json(task_dir / "task.json", task)
    atomic_write_json(task_dir / "state.json", state)
    append_event(task_dir, {
        "$version": "1.0.0", "trace_id": f"{task_id}-001", "task_id": task_id,
        "ts": utc_now(), "stage": "SPEC", "type": "stage_transition", "agent": "system",
        "details": {"from": None, "to": "SPEC", "event": "TASK_CREATED", "mode": "pipeline", "risk_tier": "low"},
    })
    return task_dir


def transition(task_id: str, to_stage: str, owner_id: str = "orchestrator") -> None:
    validate_task_id(task_id)
    task_dir = TASKS_DIR / task_id
    state_path = task_dir / "state.json"

    lock = LeaseLock(task_dir / ".lock", owner_id=owner_id)
    lock.acquire()
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
        from_stage = state["stage"]
        if to_stage not in ALLOWED_EDGES.get(from_stage, []):
            raise RuntimeError(f"Invalid transition: {from_stage} -> {to_stage}")

        validator = VALIDATOR_BY_STAGE.get(from_stage)
        if validator:
            cmd = ["python3", str(ROOT / validator), str(task_dir)]
            result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Validator failed for stage {from_stage}: {result.stderr.strip()}")

        state["stage"] = to_stage
        state["status"] = "COMPLETED" if to_stage == "DONE" else "IN_PROGRESS"
        state["next"] = ALLOWED_EDGES.get(to_stage, [])
        atomic_write_json(state_path, state)

        append_event(task_dir, {
            "$version": "1.0.0", "trace_id": f"{task_id}-{int(time.time())}", "task_id": task_id,
            "ts": utc_now(), "stage": to_stage, "type": "stage_transition",
            "agent": owner_id,
            "details": {
                "from": from_stage,
                "to": to_stage,
                "event": "TASK_COMPLETED" if to_stage == "DONE" else "STAGE_TRANSITION",
            },
        })
    finally:
        lock.release()


def run_pipeline(task_id: str, owner_id: str = "orchestrator") -> None:
    validate_task_id(task_id)
    for to_stage in STAGES[1:]:
        transition(task_id, to_stage, owner_id)


def main() -> None:
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)

    init_p = sp.add_parser("init_task")
    init_p.add_argument("task_id")
    init_p.add_argument("--title", default="Untitled task")

    tr_p = sp.add_parser("transition")
    tr_p.add_argument("task_id")
    tr_p.add_argument("to_stage", choices=STAGES)
    tr_p.add_argument("--owner-id", default="orchestrator")

    run_p = sp.add_parser("run")
    run_p.add_argument("task_id")
    run_p.add_argument("--owner-id", default="orchestrator")

    a = p.parse_args()
    if a.cmd == "init_task":
        init_task(a.task_id, a.title)
    elif a.cmd == "transition":
        transition(a.task_id, a.to_stage, a.owner_id)
    elif a.cmd == "run":
        run_pipeline(a.task_id, a.owner_id)


if __name__ == "__main__":
    main()
