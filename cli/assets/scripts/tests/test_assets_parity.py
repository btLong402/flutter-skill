#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for 100% parity between canonical src/ and cli/assets/."""

import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent
SRC_DIR = ROOT_DIR / "src" / "flutter-pro-max"
CLI_ASSETS_DIR = ROOT_DIR / "cli" / "assets"


class TestAssetsParity(unittest.TestCase):
    def test_csv_data_parity(self):
        src_data = sorted([f.name for f in (SRC_DIR / "data").glob("*.csv")])
        cli_data = sorted([f.name for f in (CLI_ASSETS_DIR / "data").glob("*.csv")])
        self.assertEqual(src_data, cli_data, "CSV datasets between src and cli/assets are not identical!")

        # Compare file sizes / contents
        for filename in src_data:
            src_bytes = (SRC_DIR / "data" / filename).read_bytes()
            cli_bytes = (CLI_ASSETS_DIR / "data" / filename).read_bytes()
            self.assertEqual(src_bytes, cli_bytes, f"Data file {filename} differs between src and cli/assets")

    def test_scripts_parity(self):
        src_scripts = sorted([f.name for f in (SRC_DIR / "scripts").glob("*.py")])
        cli_scripts = sorted([f.name for f in (CLI_ASSETS_DIR / "scripts").glob("*.py")])
        self.assertEqual(src_scripts, cli_scripts, "Python scripts between src and cli/assets are not identical!")

        for filename in src_scripts:
            src_text = (SRC_DIR / "scripts" / filename).read_text(encoding="utf-8")
            cli_text = (CLI_ASSETS_DIR / "scripts" / filename).read_text(encoding="utf-8")
            self.assertEqual(src_text, cli_text, f"Script {filename} differs between src and cli/assets")

    def test_rules_templates_parity(self):
        src_rules = sorted([f.name for f in (SRC_DIR / "templates" / "base" / "rules").glob("*.md")])
        cli_rules = sorted([f.name for f in (CLI_ASSETS_DIR / "templates" / "base" / "rules").glob("*.md")])
        self.assertEqual(src_rules, cli_rules, "Rule templates between src and cli/assets are not identical!")


if __name__ == "__main__":
    unittest.main()
