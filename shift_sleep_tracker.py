#!/usr/bin/env python3
"""Shift Sleep Tracker.

A small, local-first command line tool for healthcare workers to log shift
sleep and fatigue patterns, with CSV export.

Education-only tool. Not medical advice, diagnosis, or treatment.

Copyright (c) 2026 Asdale Dynamics, LLC
"""

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path

DEFAULT_DATA_FILE = Path.home() / ".shift_sleep_tracker.json"
VALID_SHIFT_TYPES = ("day", "night")

DISCLAIMER = """\
================================================================================
EDUCATION-ONLY DISCLAIMER
================================================================================
This tool is for educational purposes only. It is not medical advice, diagnosis,
or treatment. Sleep and fatigue tracking is not a substitute for professional
medical care. If you have concerns about your sleep, fatigue, or health, please
consult a qualified healthcare professional.
================================================================================
"""


@dataclass
class ShiftEntry:
    """A single shift sleep/fatigue log entry."""

    entry_id: str
    date: str  # ISO date, YYYY-MM-DD
    shift_type: str  # "day" or "night"
    hours_slept: float
    fatigue_rating: int  # 1-10
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class ShiftStorage:
    """Local JSON storage for shift entries."""

    def __init__(self, path: Path):
        self.path = Path(path)

    def load(self) -> list[dict]:
        if not self.path.exists():
            return []
        try:
            with self.path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (json.JSONDecodeError, OSError):
            return []
        if not isinstance(data, list):
            return []
        return data

    def save(self, entries: list[dict]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as fh:
            json.dump(entries, fh, indent=2)

    def add(self, entry: ShiftEntry) -> None:
        entries = self.load()
        entries.append(asdict(entry))
        self.save(entries)

    def update(self, entry_id: str, fields: dict) -> bool:
        entries = self.load()
        for item in entries:
            if str(item.get("entry_id")) == str(entry_id):
                item.update(fields)
                self.save(entries)
                return True
        return False

    def delete(self, entry_id: str) -> bool:
        entries = self.load()
        filtered = [e for e in entries if str(e.get("entry_id")) != str(entry_id)]
        if len(filtered) == len(entries):
            return False
        self.save(filtered)
        return True


def next_entry_id(entries: list[dict]) -> str:
    if not entries:
        return "1"
    try:
        return str(max(int(e.get("entry_id", 0)) for e in entries) + 1)
    except (TypeError, ValueError):
        return str(len(entries) + 1)


def validate_date(value: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"invalid date '{value}': expected YYYY-MM-DD"
        ) from exc
    return value


def validate_shift_type(value: str) -> str:
    if value.lower() not in VALID_SHIFT_TYPES:
        raise argparse.ArgumentTypeError(
            f"invalid shift type '{value}': expected one of {VALID_SHIFT_TYPES}"
        )
    return value.lower()


def validate_fatigue(value: str) -> int:
    try:
        rating = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"invalid fatigue rating '{value}': expected an integer"
        ) from exc
    if not 1 <= rating <= 10:
        raise argparse.ArgumentTypeError(
            f"invalid fatigue rating {rating}: expected 1-10"
        )
    return rating


def validate_hours(value: str) -> float:
    try:
        hours = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"invalid hours slept '{value}': expected a number"
        ) from exc
    if hours < 0:
        raise argparse.ArgumentTypeError(
            f"invalid hours slept {hours}: must be zero or greater"
        )
    return hours


def parse_entries(raw: list[dict]) -> list[ShiftEntry]:
    entries = []
    for item in raw:
        entries.append(
            ShiftEntry(
                entry_id=str(item.get("entry_id", "")),
                date=str(item.get("date", "")),
                shift_type=str(item.get("shift_type", "")),
                hours_slept=float(item.get("hours_slept", 0.0)),
                fatigue_rating=int(item.get("fatigue_rating", 0)),
                notes=str(item.get("notes", "")),
                created_at=str(item.get("created_at", "")),
            )
        )
    return entries


def totals(entries: list[ShiftEntry]) -> dict:
    count = len(entries)
    total_hours = sum(e.hours_slept for e in entries)
    average_fatigue = (
        round(sum(e.fatigue_rating for e in entries) / count, 2) if count else 0.0
    )
    return {
        "count": count,
        "total_hours_slept": round(total_hours, 2),
        "average_fatigue": average_fatigue,
    }


def date_math(entries: list[ShiftEntry]) -> dict:
    if not entries:
        return {
            "earliest_date": None,
            "latest_date": None,
            "days_between": 0,
            "days_since_last": None,
        }
    dates = [datetime.strptime(e.date, "%Y-%m-%d").date() for e in entries]
    earliest = min(dates)
    latest = max(dates)
    today = date.today()
    days_since = (today - latest).days
    return {
        "earliest_date": earliest.isoformat(),
        "latest_date": latest.isoformat(),
        "days_between": (latest - earliest).days,
        "days_since_last": max(0, days_since),
    }


def cmd_add(args, storage: ShiftStorage) -> int:
    print(DISCLAIMER)
    entry_date = args.date or date.today().isoformat()
    entry_id = next_entry_id(storage.load())
    entry = ShiftEntry(
        entry_id=entry_id,
        date=entry_date,
        shift_type=args.shift,
        hours_slept=args.hours_slept,
        fatigue_rating=args.fatigue,
        notes=args.notes,
    )
    storage.add(entry)
    print(f"Logged shift #{entry_id}: {entry.date} {entry.shift_type} shift, "
          f"{entry.hours_slept}h slept, fatigue {entry.fatigue_rating}/10")
    return 0


def cmd_list(args, storage: ShiftStorage) -> int:
    print(DISCLAIMER)
    entries = parse_entries(storage.load())
    if not entries:
        print("No shift entries found.")
        return 0
    for e in entries:
        print(f"#{e.entry_id}  {e.date}  {e.shift_type:5}  "
              f"{e.hours_slept}h slept  fatigue {e.fatigue_rating}/10  {e.notes}")
    return 0


def cmd_totals(args, storage: ShiftStorage) -> int:
    print(DISCLAIMER)
    entries = parse_entries(storage.load())
    t = totals(entries)
    d = date_math(entries)
    print(f"Entries logged:      {t['count']}")
    print(f"Total hours slept:   {t['total_hours_slept']}")
    print(f"Average fatigue:     {t['average_fatigue']}/10")
    if d["earliest_date"]:
        print(f"First shift date:    {d['earliest_date']}")
        print(f"Last shift date:     {d['latest_date']}")
        print(f"Days between shifts: {d['days_between']}")
        print(f"Days since last:     {d['days_since_last']}")
    return 0


def cmd_edit(args, storage: ShiftStorage) -> int:
    print(DISCLAIMER)
    fields = {}
    if args.date is not None:
        fields["date"] = args.date
    if args.shift is not None:
        fields["shift_type"] = args.shift
    if args.hours_slept is not None:
        fields["hours_slept"] = args.hours_slept
    if args.fatigue is not None:
        fields["fatigue_rating"] = args.fatigue
    if args.notes is not None:
        fields["notes"] = args.notes
    if not fields:
        print("Nothing to update. Provide at least one of --date, --shift, "
              "--hours-slept, --fatigue, --notes.")
        return 1
    if storage.update(args.entry_id, fields):
        print(f"Updated shift #{args.entry_id}.")
    else:
        print(f"No shift found with id #{args.entry_id}.")
        return 1
    return 0


def cmd_delete(args, storage: ShiftStorage) -> int:
    print(DISCLAIMER)
    if storage.delete(args.entry_id):
        print(f"Deleted shift #{args.entry_id}.")
    else:
        print(f"No shift found with id #{args.entry_id}.")
        return 1
    return 0


def cmd_export(args, storage: ShiftStorage) -> int:
    print(DISCLAIMER)
    entries = parse_entries(storage.load())
    output = Path(args.output)
    fields = [
        "entry_id", "date", "shift_type", "hours_slept",
        "fatigue_rating", "notes", "created_at",
    ]
    with output.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for item in storage.load():
            writer.writerow({k: item.get(k, "") for k in fields})
    print(f"Exported {len(entries)} entries to {output}")
    return 0


def cmd_disclaimer(args, storage: ShiftStorage) -> int:
    print(DISCLAIMER)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shift_sleep_tracker",
        description="Log shift sleep and fatigue patterns (education only).",
    )
    parser.add_argument("--data-file", default=None,
                        help="Path to the JSON data file. Defaults to "
                             "~/.shift_sleep_tracker.json.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a shift sleep/fatigue log entry")
    p_add.add_argument("--date", type=validate_date, default=None,
                       help="Shift date (YYYY-MM-DD). Defaults to today.")
    p_add.add_argument("--shift", type=validate_shift_type, required=True,
                       help="Shift type: day or night")
    p_add.add_argument("--hours-slept", type=validate_hours, required=True,
                       help="Hours slept before the shift")
    p_add.add_argument("--fatigue", type=validate_fatigue, required=True,
                       help="Fatigue rating 1-10")
    p_add.add_argument("--notes", default="", help="Optional notes")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List all logged shift entries")
    p_list.set_defaults(func=cmd_list)

    p_totals = sub.add_parser("totals", help="Show sleep/fatigue totals and date math")
    p_totals.set_defaults(func=cmd_totals)

    p_export = sub.add_parser("export", help="Export entries to CSV")
    p_export.add_argument("--output", required=True, help="Output CSV file path")
    p_export.set_defaults(func=cmd_export)

    p_disclaimer = sub.add_parser("disclaimer", help="Show the education-only disclaimer")
    p_disclaimer.set_defaults(func=cmd_disclaimer)

    p_edit = sub.add_parser("edit", help="Edit an existing shift entry by id")
    p_edit.add_argument("entry_id", help="Id of the entry to edit")
    p_edit.add_argument("--date", type=validate_date, default=None,
                        help="New shift date (YYYY-MM-DD)")
    p_edit.add_argument("--shift", type=validate_shift_type, default=None,
                        help="New shift type: day or night")
    p_edit.add_argument("--hours-slept", type=validate_hours, default=None,
                        help="New hours slept")
    p_edit.add_argument("--fatigue", type=validate_fatigue, default=None,
                        help="New fatigue rating 1-10")
    p_edit.add_argument("--notes", default=None,
                        help="New notes (use empty string to clear)")
    p_edit.set_defaults(func=cmd_edit)

    p_delete = sub.add_parser("delete", help="Delete a shift entry by id")
    p_delete.add_argument("entry_id", help="Id of the entry to delete")
    p_delete.set_defaults(func=cmd_delete)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    data_file = Path(args.data_file) if args.data_file else DEFAULT_DATA_FILE
    storage = ShiftStorage(data_file)
    return args.func(args, storage)


if __name__ == "__main__":
    sys.exit(main())
