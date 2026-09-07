#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for data integrity and catalog metadata."""

import unittest
import sys
import json
import csv
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core import DATA_DIR, CSV_CONFIG


class TestDataIntegrity(unittest.TestCase):
    def test_catalog_summary_exists(self):
        summary_path = DATA_DIR / "catalog-summary.json"
        self.assertTrue(summary_path.exists())
        with open(summary_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertIn("counts", data)
        self.assertIn("snapshots", data)

    def test_all_configured_csvs_exist_and_non_empty(self):
        for domain, config in CSV_CONFIG.items():
            filename = config["file"]
            csv_path = DATA_DIR / filename
            self.assertTrue(csv_path.exists(), f"CSV for domain '{domain}' does not exist: {filename}")
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                self.assertIsNotNone(header, f"CSV {filename} is empty")
                rows = list(reader)
                self.assertGreater(len(rows), 0, f"CSV {filename} has no data rows")


if __name__ == "__main__":
    unittest.main()
