#!/usr/bin/env bash
set -euo pipefail

OWNER="WanxiaJaneYang"
REPO="WanxiaJaneYang/DndCharacterBuilder"
PROJECT_NUMBER="3"
WORKDIR="/home/lenovo/.openclaw/workspace"
LOG_DIR="$WORKDIR/logs"
LOG_FILE="$LOG_DIR/project-issue-sync.log"
mkdir -p "$LOG_DIR"

GH_BIN="${GH_BIN:-}"
if [[ -z "$GH_BIN" ]]; then
  GH_BIN="$(command -v gh 2>/dev/null || true)"
fi
if [[ -z "$GH_BIN" && -x "/home/linuxbrew/.linuxbrew/bin/gh" ]]; then
  GH_BIN="/home/linuxbrew/.linuxbrew/bin/gh"
fi
if [[ -z "$GH_BIN" ]]; then
  echo "[$(date '+%F %T')] ERROR: gh not found" >> "$LOG_FILE"
  exit 0
fi

"$GH_BIN" issue list --repo "$REPO" --state open --limit 500 --json number >/tmp/open_issues.$$ 2>/dev/null || {
  echo "[$(date '+%F %T')] WARN: unable to list open issues" >> "$LOG_FILE"
  rm -f /tmp/open_issues.$$
  exit 0
}

"$GH_BIN" api graphql -f query='query($owner:String!,$number:Int!,$cursor:String){ user(login:$owner){ projectV2(number:$number){ items(first:100,after:$cursor){ pageInfo{hasNextPage endCursor} nodes{ content{ __typename ... on Issue { number repository { nameWithOwner } } } } } } } }' -F owner="$OWNER" -F number="$PROJECT_NUMBER" >/tmp/project_items_page1.$$ 2>/dev/null || {
  echo "[$(date '+%F %T')] WARN: unable to read project items" >> "$LOG_FILE"
  rm -f /tmp/open_issues.$$ /tmp/project_items_page1.$$
  exit 0
}

python3 - "$REPO" /tmp/open_issues.$$ /tmp/project_items_page1.$$ "$GH_BIN" "$OWNER" "$PROJECT_NUMBER" "$LOG_FILE" <<'PY'
import json, subprocess, sys
repo, open_file, page1_file, gh_bin, owner, project_num, log_file = sys.argv[1:]

with open(open_file, 'r', encoding='utf-8') as f:
    open_issues = json.load(f)
open_nums = {i['number'] for i in open_issues}

with open(page1_file, 'r', encoding='utf-8') as f:
    page = json.load(f)

proj_nums = set()

def absorb(nodes):
    for n in nodes:
        c = n.get('content')
        if c and c.get('__typename') == 'Issue' and c.get('repository', {}).get('nameWithOwner') == repo:
            proj_nums.add(c['number'])

items = page['data']['user']['projectV2']['items']
absorb(items['nodes'])
while items['pageInfo']['hasNextPage']:
    cursor = items['pageInfo']['endCursor']
    out = subprocess.check_output([
        gh_bin, 'api', 'graphql',
        '-f', 'query=query($owner:String!,$number:Int!,$cursor:String){ user(login:$owner){ projectV2(number:$number){ items(first:100,after:$cursor){ pageInfo{hasNextPage endCursor} nodes{ content{ __typename ... on Issue { number repository { nameWithOwner } } } } } } } }',
        '-F', f'owner={owner}',
        '-F', f'number={project_num}',
        '-F', f'cursor={cursor}',
    ], stderr=subprocess.DEVNULL)
    page = json.loads(out.decode('utf-8'))
    items = page['data']['user']['projectV2']['items']
    absorb(items['nodes'])

missing = sorted(open_nums - proj_nums)
extra = sorted(proj_nums - open_nums)

from datetime import datetime
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
with open(log_file, 'a', encoding='utf-8') as f:
    if missing or extra:
        f.write(f'[{now}] REMINDER: issue/project mismatch missing={missing} extra={extra}\n')
    else:
        f.write(f'[{now}] OK: issue/project sync open={len(open_nums)} project_items={len(proj_nums)}\n')
PY

rm -f /tmp/open_issues.$$ /tmp/project_items_page1.$$
exit 0
