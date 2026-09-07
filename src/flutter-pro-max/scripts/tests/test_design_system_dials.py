#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for design system dials and Dart theme generator."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from design_system import DesignSystemGenerator, generate_design_system, generate_dart_theme


class TestDesignSystemDials(unittest.TestCase):
    def setUp(self):
        self.generator = DesignSystemGenerator()

    def test_dials_resolution(self):
        ds = self.generator.generate(
            "crypto wallet",
            project_name="CryptoTest",
            variance=8,
            motion=5,
            density=9
        )
        self.assertIsNotNone(ds["dials"]["variance"])
        self.assertEqual(ds["dials"]["variance"]["value"], 8)
        self.assertIn("Bold", ds["dials"]["variance"]["label"])

        self.assertIsNotNone(ds["dials"]["motion"])
        self.assertEqual(ds["dials"]["motion"]["value"], 5)
        self.assertEqual(ds["dials"]["motion"]["label"], "Standard")

        self.assertIsNotNone(ds["dials"]["density"])
        self.assertEqual(ds["dials"]["density"]["value"], 9)
        self.assertEqual(ds["visual_density"], "VisualDensity.compact")

    def test_motion_preset_attached(self):
        ds = self.generator.generate("banking app", motion=2)
        motion = ds.get("motion_preset", {})
        self.assertTrue(bool(motion.get("Category")))
        self.assertIn("Subtle", motion.get("Intensity Tier", ""))

    def test_dart_theme_export(self):
        ds = self.generator.generate("fashion shop", density=3)
        dart_code = generate_dart_theme(ds)
        self.assertIn("class AppColors", dart_code)
        self.assertIn("class AppSpacing", dart_code)
        self.assertIn("class AppTheme", dart_code)
        self.assertIn("ThemeExtension<AppCustomTokens>", dart_code)
        self.assertIn("useMaterial3: true", dart_code)


if __name__ == "__main__":
    unittest.main()
