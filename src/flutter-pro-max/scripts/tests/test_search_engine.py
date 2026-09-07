#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for core search engine and multi-domain queries."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core import search, search_with_stack, CSV_CONFIG, DATA_DIR


class TestSearchEngine(unittest.TestCase):
    def test_search_all_18_domains_callable(self):
        for domain in CSV_CONFIG.keys():
            res = search("flutter", domain=domain, max_results=2)
            self.assertIsInstance(res, dict)
            self.assertIn("results", res)
            self.assertEqual(res["domain"], domain)

    def test_search_widget_domain(self):
        res = search("ListView pagination", domain="widget", max_results=3)
        self.assertIn("results", res)
        self.assertGreater(len(res["results"]), 0)
        top_res = res["results"][0]
        self.assertIn("_score", top_res)
        self.assertIn("Widget Name", top_res)
        self.assertEqual(top_res["Widget Name"], "ListView")

    def test_search_motion_domain(self):
        res = search("hero transition", domain="motion", max_results=3)
        self.assertIn("results", res)
        self.assertGreater(len(res["results"]), 0)
        top_res = res["results"][0]
        self.assertIn("Category", top_res)
        self.assertIn("Hero Shared Element", top_res["Category"])
        self.assertIn("Flutter Snippet", top_res)

    def test_search_with_stack_filtering(self):
        res = search_with_stack("state management", stack="riverpod", max_results=5)
        self.assertIsInstance(res, dict)
        self.assertIn("results", res)


if __name__ == "__main__":
    unittest.main()
