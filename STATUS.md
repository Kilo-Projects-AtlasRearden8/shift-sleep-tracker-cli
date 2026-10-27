# STATUS

## What was built

A local-first Python CLI for healthcare workers to log shift sleep and
fatigue patterns, with CSV export. Built as part of Asdale Dynamics, LLC's
accessible life-admin / healthcare-worker AI aids (education only, never
medical advice).

## Files

- `shift_sleep_tracker.py` — CLI module (stdlib only)
- `tests/test_shift_sleep_tracker.py` — 15 unit tests (unittest)
- `LICENSE` — MIT License, copyright Asdale Dynamics, LLC 2026
- `README.md` — usage docs, credits Asdale Dynamics, LLC
- `.gitignore` — ignores Python bytecode and editor files
- `STATUS.md` — this file

## Commands

- `add` — log a shift (date, day/night shift, hours slept, fatigue 1-10, notes)
- `list` — list all logged entries
- `totals` — entry count, total hours slept, average fatigue, date math
  (first/last shift, days between, days since last)
- `export --output <file.csv>` — export all entries to CSV
- `disclaimer` — show the education-only disclaimer

The education-only disclaimer prints on every command. Data is stored locally
in `~/.shift_sleep_tracker.json` (JSON). No accounts, no cloud, no secrets, no
personal data collected.

## How to run

```bash
python3 shift_sleep_tracker.py add --date 2026-10-27 --shift night \
    --hours-slept 5 --fatigue 6 --notes "double shift"
python3 shift_sleep_tracker.py totals
python3 shift_sleep_tracker.py export --output shift_log.csv
python3 -m unittest discover -s tests -v
```

## Verification results

- `python3 -m unittest discover -s tests -v`: 15 tests, OK
- CLI end-to-end: add, list, totals, export all ran successfully; CSV export
  produced correct rows with headers `entry_id,date,shift_type,hours_slept,
  fatigue_rating,notes,created_at`
- `git init`, staged all files, committed as `b642fd1` (plain message, no
  co-author trailers), working tree clean. Not pushed, no remote created.

## Known gaps

- Data file path defaults to `~/.shift_sleep_tracker.json`; override requires
  editing code (no `--data-file` flag yet)
- "Days since last" can be negative if a logged shift date is after today
- No entry edit/delete commands
- No test for the `list` command output formatting
