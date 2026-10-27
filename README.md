# Shift Sleep Tracker

A small, local-first command line tool for healthcare workers to log shift
sleep and fatigue patterns, with CSV export.

Built by **Asdale Dynamics, LLC** — beginner-friendly AI education, books, and
practical tools (Indiana, formed October 2026). Learn more at
dylanasdale.github.io.

## Education-only disclaimer

This tool is for educational purposes only. It is not medical advice, diagnosis,
or treatment. Sleep and fatigue tracking is not a substitute for professional
medical care. If you have concerns about your sleep, fatigue, or health, please
consult a qualified healthcare professional.

## What it does

- Log a shift with date, shift type (day/night), hours slept, fatigue rating
  (1-10), and optional notes
- List all logged entries
- View totals: entry count, total hours slept, average fatigue, plus date math
  (first/last shift date, days between, days since last)
- Export all entries to CSV
- Data is stored locally as JSON (no accounts, no cloud, no personal data
  collected)

## Requirements

Python 3.9+. No external packages — only the standard library.

## Install

```bash
git clone <this-repo>
cd shift-sleep-tracker-cli
chmod +x shift_sleep_tracker.py
```

## Usage

Run from the folder:

```bash
python3 shift_sleep_tracker.py add --shift night --hours-slept 6.5 --fatigue 7 --notes "felt tired"
python3 shift_sleep_tracker.py add --shift day --hours-slept 4 --fatigue 4
python3 shift_sleep_tracker.py list
python3 shift_sleep_tracker.py totals
python3 shift_sleep_tracker.py export --output shift_log.csv
python3 shift_sleep_tracker.py disclaimer
```

Examples:

```bash
# Log a night shift worked after sleeping 5 hours, fatigue rating 6
python3 shift_sleep_tracker.py add --date 2026-10-27 --shift night \
    --hours-slept 5 --fatigue 6 --notes "double shift"

# See your totals and date math
python3 shift_sleep_tracker.py totals

# Export everything to CSV
python3 shift_sleep_tracker.py export --output ~/shift_sleep_export.csv
```

Data is saved to `~/.shift_sleep_tracker.json` by default.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

## Credit

Created and maintained by Asdale Dynamics, LLC — Dylan Asdale, registered
nurse turned AI author and founder. Books and plain-English AI guides at
dylanasdale.github.io.
