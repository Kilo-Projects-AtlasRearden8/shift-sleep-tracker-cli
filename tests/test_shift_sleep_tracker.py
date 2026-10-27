"""Tests for the Shift Sleep Tracker CLI.

Covers totals calculation, date math, entry persistence, and CSV export.
"""

import argparse
import csv
import json
import os
import tempfile
import unittest
from datetime import date, timedelta

import shift_sleep_tracker as sst


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.path = os.path.join(self.tmpdir, "data.json")
        self.storage = sst.ShiftStorage(self.path)

    def test_save_and_load_roundtrip(self):
        entry = sst.ShiftEntry(
            entry_id="1",
            date="2026-10-01",
            shift_type="night",
            hours_slept=6.5,
            fatigue_rating=7,
            notes="felt tired",
        )
        self.storage.add(entry)
        raw = self.storage.load()
        self.assertEqual(len(raw), 1)
        self.assertEqual(raw[0]["entry_id"], "1")
        self.assertEqual(raw[0]["hours_slept"], 6.5)

    def test_missing_file_returns_empty(self):
        self.assertEqual(self.storage.load(), [])

    def test_corrupt_file_returns_empty(self):
        with open(self.path, "w", encoding="utf-8") as fh:
            fh.write("{not valid json")
        self.assertEqual(self.storage.load(), [])


class TestNextEntryId(unittest.TestCase):
    def test_empty_list_starts_at_one(self):
        self.assertEqual(sst.next_entry_id([]), "1")

    def test_increments_past_max(self):
        entries = [
            {"entry_id": "3"},
            {"entry_id": "1"},
            {"entry_id": "10"},
        ]
        self.assertEqual(sst.next_entry_id(entries), "11")


class TestTotals(unittest.TestCase):
    def test_totals_empty(self):
        self.assertEqual(
            sst.totals([]),
            {"count": 0, "total_hours_slept": 0.0, "average_fatigue": 0.0},
        )

    def test_totals_nonempty(self):
        entries = [
            sst.ShiftEntry("1", "2026-10-01", "night", 6.0, 8),
            sst.ShiftEntry("2", "2026-10-02", "day", 4.0, 4),
            sst.ShiftEntry("3", "2026-10-03", "night", 5.0, 6),
        ]
        result = sst.totals(entries)
        self.assertEqual(result["count"], 3)
        self.assertEqual(result["total_hours_slept"], 15.0)
        self.assertEqual(result["average_fatigue"], 6.0)

    def test_totals_rounds_average(self):
        entries = [
            sst.ShiftEntry("1", "2026-10-01", "night", 6.0, 5),
            sst.ShiftEntry("2", "2026-10-02", "day", 4.0, 4),
        ]
        self.assertEqual(sst.totals(entries)["average_fatigue"], 4.5)


class TestDateMath(unittest.TestCase):
    def test_date_math_empty(self):
        self.assertEqual(
            sst.date_math([]),
            {
                "earliest_date": None,
                "latest_date": None,
                "days_between": 0,
                "days_since_last": None,
            },
        )

    def test_date_math_range(self):
        entries = [
            sst.ShiftEntry("1", "2026-10-01", "night", 6.0, 8),
            sst.ShiftEntry("2", "2026-10-05", "day", 4.0, 4),
            sst.ShiftEntry("3", "2026-10-03", "night", 5.0, 6),
        ]
        result = sst.date_math(entries)
        self.assertEqual(result["earliest_date"], "2026-10-01")
        self.assertEqual(result["latest_date"], "2026-10-05")
        self.assertEqual(result["days_between"], 4)

    def test_days_since_last_relative_to_today(self):
        yesterday = date.today() - timedelta(days=1)
        entries = [
            sst.ShiftEntry("1", yesterday.isoformat(), "night", 6.0, 8),
        ]
        result = sst.date_math(entries)
        self.assertEqual(result["days_since_last"], 1)


class TestParseEntries(unittest.TestCase):
    def test_parse_entries(self):
        raw = [
            {
                "entry_id": "1",
                "date": "2026-10-01",
                "shift_type": "night",
                "hours_slept": 6.0,
                "fatigue_rating": 8,
                "notes": "",
                "created_at": "2026-10-01T00:00:00",
            }
        ]
        entries = sst.parse_entries(raw)
        self.assertEqual(len(entries), 1)
        self.assertIsInstance(entries[0], sst.ShiftEntry)
        self.assertEqual(entries[0].fatigue_rating, 8)


class TestCliExport(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.data_path = os.path.join(self.tmpdir, "data.json")
        self.storage = sst.ShiftStorage(self.data_path)
        self.storage.add(
            sst.ShiftEntry("1", "2026-10-01", "night", 6.0, 8, "notes here")
        )

    def test_export_writes_csv(self):
        out_path = os.path.join(self.tmpdir, "out.csv")
        args = type("A", (), {"output": out_path})()
        sst.cmd_export(args, self.storage)
        with open(out_path, newline="", encoding="utf-8") as fh:
            reader = list(csv.DictReader(fh))
        self.assertEqual(len(reader), 1)
        self.assertEqual(reader[0]["date"], "2026-10-01")
        self.assertEqual(reader[0]["shift_type"], "night")


class TestValidation(unittest.TestCase):
    def test_validate_fatigue_out_of_range(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            sst.validate_fatigue("11")
        with self.assertRaises(argparse.ArgumentTypeError):
            sst.validate_fatigue("0")

    def test_validate_shift_type(self):
        self.assertEqual(sst.validate_shift_type("DAY"), "day")
        self.assertEqual(sst.validate_shift_type("Night"), "night")
        with self.assertRaises(argparse.ArgumentTypeError):
            sst.validate_shift_type("midnight")


if __name__ == "__main__":
    unittest.main()
