#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]
BASE = Path.home() / ".openclaw" / "workspace" / "tools" / "calendar"
TOKEN_PATH = BASE / "token.json"
CREDS_PATH = BASE / "credentials.json"


def get_service():
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDS_PATH.exists():
                raise SystemExit(
                    f"Missing credentials file: {CREDS_PATH}\n"
                    "Download OAuth client JSON from Google Cloud Console and place it there."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_PATH.write_text(creds.to_json())
    return build("calendar", "v3", credentials=creds)


def parse_iso(s: str) -> str:
    # Expect: 2026-03-22T17:00:00+10:30
    return dt.datetime.fromisoformat(s).isoformat()


def cmd_create(args):
    service = get_service()
    event = {
        "summary": args.title,
        "description": args.description or "",
    }
    if args.all_day:
        event["start"] = {"date": args.start_date}
        event["end"] = {"date": args.end_date}
    else:
        event["start"] = {"dateTime": parse_iso(args.start), "timeZone": args.timezone}
        event["end"] = {"dateTime": parse_iso(args.end), "timeZone": args.timezone}

    created = service.events().insert(calendarId=args.calendar, body=event).execute()
    print(json.dumps({"id": created["id"], "htmlLink": created.get("htmlLink")}, ensure_ascii=False))


def cmd_update(args):
    service = get_service()
    event = service.events().get(calendarId=args.calendar, eventId=args.event_id).execute()
    if args.title:
        event["summary"] = args.title
    if args.description is not None:
        event["description"] = args.description
    if args.start and args.end:
        event["start"] = {"dateTime": parse_iso(args.start), "timeZone": args.timezone}
        event["end"] = {"dateTime": parse_iso(args.end), "timeZone": args.timezone}
    updated = service.events().update(calendarId=args.calendar, eventId=args.event_id, body=event).execute()
    print(json.dumps({"id": updated["id"], "htmlLink": updated.get("htmlLink")}, ensure_ascii=False))


def cmd_list(args):
    service = get_service()
    events = (
        service.events()
        .list(
            calendarId=args.calendar,
            timeMin=args.time_min,
            timeMax=args.time_max,
            singleEvents=True,
            orderBy="startTime",
            maxResults=args.limit,
        )
        .execute()
        .get("items", [])
    )
    for e in events:
        start = e.get("start", {}).get("dateTime") or e.get("start", {}).get("date")
        print(f"{e.get('id')}\t{start}\t{e.get('summary','(no title)')}")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(required=True)

    c = sub.add_parser("create")
    c.add_argument("--calendar", default="primary")
    c.add_argument("--title", required=True)
    c.add_argument("--description")
    c.add_argument("--timezone", default="Australia/Adelaide")
    c.add_argument("--start")
    c.add_argument("--end")
    c.add_argument("--all-day", action="store_true")
    c.add_argument("--start-date")
    c.add_argument("--end-date")
    c.set_defaults(func=cmd_create)

    u = sub.add_parser("update")
    u.add_argument("--calendar", default="primary")
    u.add_argument("--event-id", required=True)
    u.add_argument("--title")
    u.add_argument("--description")
    u.add_argument("--timezone", default="Australia/Adelaide")
    u.add_argument("--start")
    u.add_argument("--end")
    u.set_defaults(func=cmd_update)

    l = sub.add_parser("list")
    l.add_argument("--calendar", default="primary")
    l.add_argument("--time-min", required=True)
    l.add_argument("--time-max", required=True)
    l.add_argument("--limit", type=int, default=20)
    l.set_defaults(func=cmd_list)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
