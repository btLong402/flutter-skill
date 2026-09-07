#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for reasoning_contract.py."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from reasoning_contract import parse_decision_rules, apply_decision_rules


class TestReasoningContract(unittest.TestCase):
    def test_parse_empty(self):
        self.assertEqual(parse_decision_rules(None), {})
        self.assertEqual(parse_decision_rules(""), {})
        self.assertEqual(parse_decision_rules("{}"), {})

    def test_parse_standard_actions(self):
        raw = '{"if_booking": ["pattern:calendar-view", "style:minimalism"]}'
        rules = parse_decision_rules(raw)
        self.assertIn("if_booking", rules)
        self.assertEqual(rules["if_booking"], ["pattern:calendar-view", "style:minimalism"])

    def test_parse_legacy_actions_fallback(self):
        raw = '{"if_luxury": "use-premium-colors", "must_have": ["quick-cart"]}'
        rules = parse_decision_rules(raw)
        self.assertIn("if_luxury", rules)
        self.assertEqual(rules["if_luxury"], ["constraint:use-premium-colors"])
        self.assertEqual(rules["must_have"], ["constraint:quick-cart"])

    def test_apply_decision_rules_matching(self):
        rules = {
            "if_booking": ["pattern:booking-flow", "style:clean-grid"],
            "if_offline_first": ["architecture:drift-cache"],
            "must_have": ["constraint:biometric-auth"]
        }
        res = apply_decision_rules(rules, "build an appointment booking app with offline sync")
        self.assertEqual(res["pattern"], "booking-flow")
        self.assertIn("clean-grid", res["style_ids"])
        self.assertIn("drift-cache", res["architectures"])
        self.assertIn("biometric-auth", res["constraints"])


if __name__ == "__main__":
    unittest.main()
