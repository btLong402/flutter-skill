#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for all 20 modular rules integrity and YAML frontmatter."""

import unittest
from pathlib import Path

RULES_DIR = Path(__file__).parent.parent.parent / "templates" / "base" / "rules"


class TestRulesIntegrity(unittest.TestCase):
    def test_all_20_rules_exist(self):
        rule_files = sorted([f.name for f in RULES_DIR.glob("*.md")])
        self.assertEqual(len(rule_files), 20, f"Expected 20 rules, found {len(rule_files)}: {rule_files}")

    def test_rules_frontmatter_and_content(self):
        for rule_file in RULES_DIR.glob("*.md"):
            content = rule_file.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("---"), f"{rule_file.name} must start with YAML frontmatter '---'")
            self.assertIn("description:", content, f"{rule_file.name} must contain 'description:' in frontmatter")
            self.assertIn("# Rule:", content, f"{rule_file.name} must have a '# Rule:' heading")
            self.assertGreater(len(content.splitlines()), 15, f"{rule_file.name} content is suspiciously short")


if __name__ == "__main__":
    unittest.main()
