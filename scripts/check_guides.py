#!/usr/bin/env python3
"""Check every guide's front matter and relative links. Runs in CI.

Each guide needs: title, status (draft or reviewed), owner, last_checked (YYYY-MM-DD), and at
least one source URL. Reviewed guides more than 180 days past last_checked are flagged as stale.
"""
from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDES = ROOT / "guides"
STALE_DAYS = 180


def front_matter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    data, key = {}, None
    for line in m.group(1).splitlines():
        line = re.sub(r"\s+#.*$", "", line).rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") and key:
            data.setdefault(key, []).append(line[4:].strip().strip('"'))
        elif ":" in line:
            key, value = line.split(":", 1)
            key, value = key.strip(), value.strip().strip('"')
            data[key] = value if value else []
    return data


def problems(path: Path, today: dt.date) -> list[str]:
    text = path.read_text(encoding="utf-8")
    fm = front_matter(text)
    name = path.relative_to(ROOT)
    out = []
    for key in ("title", "status", "owner", "last_checked", "sources"):
        if not fm.get(key):
            out.append(f"{name}: front matter needs {key}")
    if fm.get("status") and fm["status"] not in ("draft", "reviewed"):
        out.append(f"{name}: status must be draft or reviewed")
    try:
        checked = dt.date.fromisoformat(fm.get("last_checked", ""))
        if fm.get("status") == "reviewed" and (today - checked).days > STALE_DAYS:
            out.append(f"{name}: last checked {checked}, more than {STALE_DAYS} days ago; walk through it again")
    except ValueError:
        out.append(f"{name}: last_checked must be YYYY-MM-DD")
    for src in fm.get("sources", []) if isinstance(fm.get("sources"), list) else []:
        if not src.startswith("https://"):
            out.append(f"{name}: source {src!r} should be an https link")
    body = text
    fm_match = re.match(r"^---\n.*?\n---\n", text, re.S)
    if fm_match:
        body = text[fm_match.end() :]
    for url in re.findall(r"\]\((http://[^)]+)\)", body):
        out.append(f"{name}: link {url!r} should use https")
    for target in re.findall(r"\]\((?!https?://|mailto:|#)([^)]+)\)", text):
        if not (path.parent / target.split("#")[0]).exists():
            out.append(f"{name}: broken link {target}")
    return out


def main() -> int:
    today = dt.date.today()
    found = [p for p in sorted(GUIDES.rglob("*.md")) if not p.name.startswith("_") and p.name != "README.md"]
    errors = [e for p in found for e in problems(p, today)]
    for e in errors:
        print(e)
    print(f"{len(found)} guides checked: {'ok' if not errors else f'{len(errors)} problems'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
