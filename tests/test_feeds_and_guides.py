import datetime as dt
import tempfile
import unittest
from pathlib import Path

from scripts import build_feeds, check_guides, import_calendar


class Feeds(unittest.TestCase):
    EVENTS = [{"term": "Spring 2027", "event": "classes begin", "date": "2027-01-19"}]

    def test_all_day_event(self):
        ics = build_feeds.calendar("Test", self.EVENTS, "https://example.edu/cal")
        self.assertIn("DTSTART;VALUE=DATE:20270119", ics)
        self.assertIn("DTEND;VALUE=DATE:20270120", ics)
        self.assertIn("SUMMARY:Spring 2027: Classes begin", ics)
        self.assertTrue(ics.startswith("BEGIN:VCALENDAR\r\n"))

    def test_multi_day_event_ends_the_day_after_its_last_day(self):
        ics = build_feeds.calendar("T", [{"term": "Fall 2026", "event": "Thanksgiving recess", "date": "2026-11-25", "end": "2026-11-27"}], "u")
        self.assertIn("DTSTART;VALUE=DATE:20261125", ics)
        self.assertIn("DTEND;VALUE=DATE:20261128", ics)

    def test_same_event_on_two_dates_gets_two_uids(self):
        ev = [{"term": "Spring 2027", "event": "classes follow a Monday schedule", "date": d} for d in ("2027-02-16", "2027-04-21")]
        ics = build_feeds.calendar("T", ev, "u")
        uids = [l for l in ics.split("\r\n") if l.startswith("UID:")]
        self.assertEqual(len(set(uids)), 2)

    def test_extra_dates_are_well_formed(self):
        import json
        extra = json.loads((build_feeds.ROOT / "data" / "academic-calendar-extra.json").read_text())
        for e in extra["events"]:
            start = dt.date.fromisoformat(e["date"])
            self.assertGreaterEqual(dt.date.fromisoformat(e.get("end", e["date"])), start, e)
            self.assertTrue(e["term"] and e["event"], e)

    def test_uid_is_stable(self):
        a = build_feeds.calendar("T", self.EVENTS, "u")
        b = build_feeds.calendar("T", self.EVENTS, "u")
        self.assertEqual(a, b)

    def test_long_lines_fold(self):
        line = "DESCRIPTION:" + "x" * 200
        self.assertTrue(all(len(part.encode()) <= 75 for part in build_feeds.fold(line).split("\r\n")))

    def test_import_normalizes(self):
        data = import_calendar.normalize({"verified_at": "2026-08-21", "entries": [
            {"term": "Fall Law 2026", "event": "classes end", "date": "November 30, 2026"},
            {"term": "Fall Law 2026", "event": "classes begin", "date": "August 24, 2026"}]}, "https://x")
        self.assertEqual([e["date"] for e in data["events"]], ["2026-08-24", "2026-11-30"])
        self.assertEqual(data["events"][0]["term"], "Fall 2026")

    def test_committed_feed_is_current(self):
        stale = [p for p, t in build_feeds.outputs().items() if not p.exists() or p.read_bytes() != t.encode()]
        self.assertEqual(stale, [], "run python3 scripts/build_feeds.py")


GOOD = """---
title: "A guide"
status: draft
owner: "Someone"
last_checked: 2026-10-20
sources:
  - https://www.suffolk.edu/law
---
# A guide
"""


class Guides(unittest.TestCase):
    def check(self, text):
        p = Path(tempfile.mkdtemp()) / "g.md"
        p.write_text(text)
        return self._run(p)

    def _run(self, p):
        root, check_guides.ROOT = check_guides.ROOT, p.parent
        try:
            return check_guides.problems(p, dt.date(2026, 10, 21))
        finally:
            check_guides.ROOT = root

    def test_good_guide(self):
        self.assertEqual(self.check(GOOD), [])

    def test_missing_source(self):
        self.assertTrue(any("sources" in e for e in self.check(GOOD.replace("sources:\n  - https://www.suffolk.edu/law\n", ""))))

    def test_stale_reviewed_guide(self):
        old = GOOD.replace("status: draft", "status: reviewed").replace("2026-10-20", "2025-01-01")
        self.assertTrue(any("ago" in e for e in self.check(old)))

    def test_template_passes(self):
        p = check_guides.GUIDES / "_TEMPLATE.md"
        self.assertEqual([e for e in self._run(p) if "broken link" in e], [])

    def test_http_link_in_body(self):
        bad = GOOD + "\nSee [old page](http://example.com/page).\n"
        errs = self.check(bad)
        self.assertTrue(
            any("http://example.com/page" in e and "should use https" in e for e in errs),
            errs,
        )


if __name__ == "__main__":
    unittest.main()
