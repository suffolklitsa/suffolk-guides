# suffolk-guides

Plain, current how-to guides for the things every Suffolk Law student has to do, plus two tools: calendar feeds you subscribe to once, and a character & fitness kit for your bar application.

**Status:** guide format, calendar feed and C&F spreadsheet in place. The first guides are being written now (see the issues).

## What's here

| | What it is | Where |
|---|---|---|
| **Guides** | Step-by-step guides: booking rooms, SBA forms, research accounts, registration and more. Each one cites the official source and says when someone last walked through it. | [`guides/`](guides/) |
| **Calendar feeds** | Suffolk Law's academic calendar (classes begin and end, add/drop, exams, commencement) as a feed for Google Calendar, Outlook or Apple Calendar. MPRE dates and LITSA events are next. | [`feeds/`](feeds/) |
| **Character & fitness kit** | A spreadsheet for every address, job, school, legal matter and document your bar application will ask about, with gap checks and a law-school-application check. | [`cf-kit/`](cf-kit/) |

## Subscribe to the academic calendar

Subscribing (rather than downloading) means your calendar updates itself when we update the feed.

- **Google Calendar:** Other calendars → **+** → From URL, and paste the feed link below.
- **Outlook:** Add calendar → Subscribe from web.
- **Apple Calendar:** File → New Calendar Subscription.

Feed link (once published): `https://raw.githubusercontent.com/suffolklitsa/suffolk-guides/main/feeds/academic-calendar.ics`. A shorter link on suffolklitsa.org is coming.

The feed is unofficial. Dates come from Suffolk Law's academic calendar page and are re-checked weekly; the page itself is the authority.

## Unofficial, and how we keep it accurate

These are student-written guides, not university policy. Every guide:

- links the official page each step comes from,
- names who last walked through it and when (`last_checked`), and
- stays marked **draft** until a second person has followed every step on the real system.

Reviewed guides that haven't been rechecked in 180 days fail the automatic check until someone walks through them again. If something's wrong, [open an issue](https://github.com/suffolklitsa/suffolk-guides/issues/new/choose).

## Branches

Pull requests go to `staging`, the default branch. `main` is the released version: maintainers promote `staging` to `main` with a pull request when a batch of changes is ready. Both branches are protected and need a review and passing checks.

## Contributing

Most of this repo needs no code: writing a guide means following a process carefully and writing it down. Start with an issue labeled [`no code needed`](https://github.com/suffolklitsa/suffolk-guides/labels/no%20code%20needed) or [`good first issue`](https://github.com/suffolklitsa/suffolk-guides/labels/good%20first%20issue), copy [`guides/_TEMPLATE.md`](guides/_TEMPLATE.md), and read [CONTRIBUTING.md](CONTRIBUTING.md).

Questions go in the Build topic on the LITSA GroupMe, or comment on the issue.

## Checks

```
python3 scripts/check_guides.py            # front matter, sources, links, staleness
python3 scripts/build_feeds.py --check     # feeds match the data
pip install -r requirements.txt            # only for the cf-kit tests and rebuilding the spreadsheet
python3 -m unittest discover -s tests
```

## Layout

| Path | What's there |
|---|---|
| `guides/` | One Markdown file per guide, plus `_TEMPLATE.md` |
| `data/academic-calendar.json` | Calendar dates, imported from Suffolk's page through the Suffolk assistant's weekly check |
| `feeds/` | Generated `.ics` feeds |
| `cf-kit/` | Spreadsheet generator, layout spec, state notes, and the built file in `dist/` |
| `scripts/` | Guide checker, calendar import, feed builder |

## License

Guides and other written content are CC BY 4.0 ([LICENSE-docs.md](LICENSE-docs.md)). Code is MIT ([LICENSE](LICENSE)).
