# STATUS

## What was built

A local-first Python CLI for healthcare workers to log shift sleep and
fatigue patterns, with CSV export. Built as part of Asdale Dynamics, LLC's
accessible life-admin / healthcare-worker AI aids (education only, never
medical advice). Tone is warm, beginner-friendly, plain English, step by step,
never condescending — matching the Asdale Dynamics brand.

## Files

- `shift_sleep_tracker.py` — CLI module (stdlib only)
- `tests/test_shift_sleep_tracker.py` — 22 unit tests (unittest)
- `LICENSE` — MIT License, copyright Asdale Dynamics, LLC 2026
- `README.md` — usage docs, credits Asdale Dynamics, LLC
- `.gitignore` — ignores Python bytecode and editor files
- `STATUS.md` — this file

## Commands

- `add` — log a shift (date, day/night shift, hours slept, fatigue 1-10, notes)
- `list` — list all logged entries
- `totals` — entry count, total hours slept, average fatigue, date math
  (first/last shift, days between, days since last)
- `edit <id>` — edit an existing entry by id (date, shift, hours, fatigue, notes)
- `delete <id>` — delete an entry by id
- `export --output <file.csv>` — export all entries to CSV
- `disclaimer` — show the education-only disclaimer
- `--data-file <path>` — override the default JSON data file path

The education-only disclaimer prints on every command. Data is stored locally
in `~/.shift_sleep_tracker.json` (JSON) by default. No accounts, no cloud, no
secrets, no personal data collected.

## How to run

```bash
python3 shift_sleep_tracker.py add --date 2026-10-27 --shift night \
    --hours-slept 5 --fatigue 6 --notes "double shift"
python3 shift_sleep_tracker.py totals
python3 shift_sleep_tracker.py list
python3 shift_sleep_tracker.py edit 1 --fatigue 3
python3 shift_sleep_tracker.py delete 1
python3 shift_sleep_tracker.py export --output shift_log.csv
python3 -m unittest discover -s tests -v
```

## Verification results

- `python3 -m unittest discover -s tests -v`: 22 tests, OK
- CLI end-to-end: add, totals, list, edit, delete, export, and `--data-file`
  all ran successfully; CSV export produced correct rows with headers
  `entry_id,date,shift_type,hours_slept,fatigue_rating,notes,created_at`
- Negative "days since last" bug fixed: value is now clamped to 0 for
  future-dated shifts
- `git init`, staged all files, committed as plain messages with no
  co-author trailers, working tree clean. Not pushed, no remote created.

## Known gaps

- No entry bulk-import from CSV (export exists; import does not)
- No graphical or web interface — CLI only, by design for local-first simplicity
- Data file still lives in the user's home directory by default; no config file
  support yet
