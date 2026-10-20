#!/usr/bin/env python3
"""Build subscribable calendar feeds (.ics) from data/.

    python3 scripts/build_feeds.py           # writes feeds/*.ics
    python3 scripts/build_feeds.py --check   # fail if feeds/ is out of date (CI)

Each date becomes an all-day event. Event UIDs are stable, so a calendar app that subscribed
updates events in place instead of duplicating them.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODID = "-//LITSA//suffolk-guides//EN"


def esc(text: str) -> str:
    return text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def fold(line: str) -> str:
    """RFC 5545 lines are at most 75 octets; longer ones continue on the next line after a space."""
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return line
    parts, cur = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        if len(cur) + len(b) > (75 if not parts else 74):
            parts.append(cur.decode("utf-8"))
            cur = b""
        cur += b
    parts.append(cur.decode("utf-8"))
    return "\r\n ".join(parts)


def calendar(name: str, events: list[dict], source_url: str) -> str:
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", f"PRODID:{PRODID}", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
             f"X-WR-CALNAME:{esc(name)}", "X-WR-TIMEZONE:America/New_York"]
    for e in sorted(events, key=lambda e: (e["date"], e["event"])):
        day = dt.date.fromisoformat(e["date"])
        last = dt.date.fromisoformat(e.get("end") or e["date"])
        summary = f"{e['term']}: {e['event'][:1].upper()}{e['event'][1:]}"
        uid = hashlib.sha256(f"{e['term']}|{e['event']}|{e['date']}".encode()).hexdigest()[:20] + "@suffolk-guides.litsa"
        lines += ["BEGIN:VEVENT", f"UID:{uid}", "DTSTAMP:20260101T000000Z",
                  f"DTSTART;VALUE=DATE:{day:%Y%m%d}", f"DTEND;VALUE=DATE:{last + dt.timedelta(days=1):%Y%m%d}",
                  f"SUMMARY:{esc(summary)}", "TRANSP:TRANSPARENT",
                  f"DESCRIPTION:{esc('From Suffolk Law academic calendar: ' + source_url + '. Unofficial; check the source.')}",
                  "END:VEVENT"]
    lines.append("END:VCALENDAR")
    return "\r\n".join(fold(l) for l in lines) + "\r\n"


def outputs() -> dict[Path, str]:
    data = json.loads((ROOT / "data" / "academic-calendar.json").read_text(encoding="utf-8"))
    events = list(data["events"])
    # Holidays, recesses, schedule swaps and make-up days, transcribed from the same calendar.
    extra = ROOT / "data" / "academic-calendar-extra.json"
    if extra.exists():
        events += json.loads(extra.read_text(encoding="utf-8"))["events"]
    return {ROOT / "feeds" / "academic-calendar.ics": calendar("Suffolk Law academic calendar (unofficial)", events, data["source"]["url"])}


def main(argv: list[str]) -> int:
    files = outputs()
    if "--check" in argv:
        stale = [p for p, t in files.items() if not p.exists() or p.read_bytes() != t.encode("utf-8")]
        for p in stale:
            print(f"out of date: {p.relative_to(ROOT)}; run python3 scripts/build_feeds.py")
        return 1 if stale else 0
    for p, t in files.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(t.encode("utf-8"))
        print(f"wrote {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
