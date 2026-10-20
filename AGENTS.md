# AGENTS.md

Instructions for AI coding agents working in this repo, and for the people using them. Read README.md and CONTRIBUTING.md too.

## What this repo is

Student-written how-to guides for Suffolk systems (`guides/`), subscribable calendar feeds (`feeds/`, built from `data/`), and the character & fitness spreadsheet generator (`cf-kit/`).

## Commands

```
python3 scripts/check_guides.py           # front matter, sources, links
python3 scripts/build_feeds.py            # rebuild feeds; --check is what CI runs
pip install -r requirements.txt           # only for cf-kit
python3 cf-kit/build_cfkit.py             # rebuild the spreadsheet
python3 -m unittest discover -s tests
```

## Rules for this repo

- **Branches:** work from `staging` and open pull requests against it. Never target `main`; maintainers promote `staging` to `main`.
- **An agent can't write a guide on its own.** Guides describe steps a person actually followed on the real system. You can help format, tighten wording or check links, but never invent steps, button names or office details. Leave `status: draft`; only a person who walked through the steps marks a guide `reviewed`.
- **Every guide links its official sources** in front matter.
- **Never edit `feeds/*.ics` by hand;** change `data/` or `scripts/build_feeds.py` and rebuild.
- **cf-kit:** change `build_cfkit.py` and `cf-kit/SPEC.md` together, use only formulas that work in both Excel and Google Sheets, and have a person open the result in Excel to confirm there's no repair prompt before committing. Never put filled-in personal data anywhere.
- **State notes in `cf-kit/states/`** need sources and R&W review before `status = "reviewed"`.

## Rules for every LITSA repo

- **No secrets.** Never write API keys, tokens or passwords into a file, a commit, an issue or a test. Keys come from environment variables. If you find one committed, stop and tell a maintainer.
- **No personal data.** No real names, emails, student records, sign-in sheets or mailing lists in code, tests, fixtures, screenshots or commit messages. Use made-up examples (`jane.doe@example.edu`).
- **No invented law.** Anything stating a rule, statute, case or requirement must come from a source you can link. Never make up a citation. If you can't find the source, say so in the pull request instead of guessing.
- **Small changes.** One issue per pull request. Don't reformat or rename things the issue didn't ask about.
- **Run the checks** listed above before saying the work is done, and report what they printed. If one fails, fix it or say plainly that it fails.
- **Plain writing.** Docs and messages use short, ordinary sentences a first-year law student would follow.
- **Disclose AI use.** The person opening the pull request notes which AI tools helped, in the description. They own every line either way.
