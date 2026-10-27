# Shift Sleep Tracker

A friendly, local-first command line tool for healthcare workers to log shift
sleep and fatigue patterns, with CSV export. Built for nurses, aides, techs, and
anyone working shifts who wants a simple way to notice patterns in their sleep
and fatigue over time.

Built by **Asdale Dynamics, LLC** — beginner-friendly AI education, books, and
practical tools (Indiana, formed October 2026). Learn more at
dylanasdale.github.io.

## Education-only disclaimer

This tool is for educational purposes only. It is not medical advice, diagnosis,
or treatment. Sleep and fatigue tracking is not a substitute for professional
medical care. If you have concerns about your sleep, fatigue, or health, please
consult a qualified healthcare professional.

The disclaimer shows every time you run the tool, because your wellbeing matters
more than convenience.

## What it does

- **Log a shift** — date, shift type (day or night), hours slept, fatigue
  rating (1-10), and optional notes
- **List your entries** — see everything you've logged so far
- **View totals** — entry count, total hours slept, average fatigue, plus date
  math (first shift, last shift, days between, days since last)
- **Edit or delete an entry** — fix a mistake or remove a test entry
- **Export to CSV** — open your data in Excel, Google Sheets, or any spreadsheet
- **Local-first storage** — your data lives in a JSON file on your computer
  (`~/.shift_sleep_tracker.json` by default). No accounts, no cloud, no personal
  data collected, nothing phones home.

## Who this is for

Healthcare workers — especially nurses — who work rotating day and night shifts
and want a dead-simple way to track how much sleep they're getting and how
tired they feel. No tech background required. If you can type a command, you
can use this.

## Requirements

Python 3.9 or newer. No external packages — just Python's standard library.

## Install

```bash
git clone <this-repo>
cd shift-sleep-tracker-cli
chmod +x shift_sleep_tracker.py
```

## Usage

Run the tool from the folder you cloned it into:

```bash
python3 shift_sleep_tracker.py <command> [options]
```

### Log a shift

```bash
python3 shift_sleep_tracker.py add --shift night --hours-slept 5 --fatigue 6 \
    --notes "double shift, felt worn out"
```

Options:
- `--shift` — `day` or `night` (required)
- `--hours-slept` — hours slept before the shift (required, can be a decimal)
- `--fatigue` — fatigue rating 1-10 (required)
- `--date` — shift date as YYYY-MM-DD (defaults to today)
- `--notes` — optional notes

### See your entries

```bash
python3 shift_sleep_tracker.py list
```

### View your totals and date math

```bash
python3 shift_sleep_tracker.py totals
```

Shows entry count, total hours slept, average fatigue, first shift date, last
shift date, days between shifts, and days since your last logged shift.

### Fix or remove an entry

```bash
# Change the fatigue rating on entry #1
python3 shift_sleep_tracker.py edit 1 --fatigue 4

# Fix the date on entry #2
python3 shift_sleep_tracker.py edit 2 --date 2026-10-28

# Remove entry #3
python3 shift_sleep_tracker.py delete 3
```

### Export to CSV

```bash
python3 shift_sleep_tracker.py export --output shift_log.csv
```

Open `shift_log.csv` in Excel, Google Sheets, or any spreadsheet app.

### See the disclaimer

```bash
python3 shift_sleep_tracker.py disclaimer
```

### Use a different data file (optional)

By default, data is saved to `~/.shift_sleep_tracker.json`. To use a different
file:

```bash
python3 shift_sleep_tracker.py --data-file ~/my_sleep_data.json add --shift day \
    --hours-slept 7 --fatigue 3
```

## Real-world example

A night-shift nurse logs a few shifts:

```bash
python3 shift_sleep_tracker.py add --date 2026-10-27 --shift night \
    --hours-slept 5 --fatigue 7 --notes "double shift"
python3 shift_sleep_tracker.py add --date 2026-10-28 --shift day \
    --hours-slept 4 --fatigue 8 --notes "hard day after nights"
python3 shift_sleep_tracker.py totals
python3 shift_sleep_tracker.py export --output ~/my_shift_log.csv
```

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
