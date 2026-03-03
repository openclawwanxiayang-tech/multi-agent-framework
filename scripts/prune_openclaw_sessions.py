#!/usr/bin/env python3
import glob
import os
import shutil
import time
from pathlib import Path

SESS_DIR = Path('/home/lenovo/.openclaw/agents/main/sessions')
ARCHIVE_ROOT = Path('/home/lenovo/.openclaw/agents/main/sessions-archive')
KEEP_NEWEST = 300
MIN_AGE_SECONDS = 2 * 3600  # never touch very recent sessions
PRUNE_AGE_SECONDS = 3 * 24 * 3600  # age-based prune to archive


def main():
    if not SESS_DIR.exists():
        print('sessions dir missing, nothing to do')
        return

    now = time.time()
    files = [Path(p) for p in glob.glob(str(SESS_DIR / '*.jsonl'))]
    files = [f for f in files if f.is_file()]
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    # Keep newest N regardless of age
    protected = set(files[:KEEP_NEWEST])

    to_archive = []
    for f in files:
        st = f.stat()
        age = now - st.st_mtime
        if age < MIN_AGE_SECONDS:
            continue
        if f in protected:
            continue
        if age >= PRUNE_AGE_SECONDS:
            to_archive.append(f)

    stamp = time.strftime('%Y-%m-%d')
    archive_dir = ARCHIVE_ROOT / f'auto-{stamp}'
    archive_dir.mkdir(parents=True, exist_ok=True)

    moved = 0
    for f in to_archive:
        dst = archive_dir / f.name
        # avoid overwrite just in case
        if dst.exists():
            dst = archive_dir / f"{int(f.stat().st_mtime)}-{f.name}"
        shutil.move(str(f), str(dst))
        moved += 1

    print(f'total={len(files)} protected={len(protected)} archived={moved} -> {archive_dir}')


if __name__ == '__main__':
    main()
