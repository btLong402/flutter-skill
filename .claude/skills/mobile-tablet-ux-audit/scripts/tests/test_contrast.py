#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for contrast.py WCAG contrast calculation and suggestion tool."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Add scripts directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))
import contrast


class TestContrastFunctions(unittest.TestCase):
    """Test core math, color parsing, and logic in contrast.py."""

    def test_parse_hex_valid_formats(self):
        # 3-digit hex
        r, g, b, a = contrast.parse_hex("#fff")
        self.assertEqual((r, g, b, a), (255, 255, 255, 1.0))

        # 4-digit hex with alpha
        r, g, b, a = contrast.parse_hex("#0008")
        self.assertEqual((r, g, b), (0, 0, 0))
        self.assertAlmostEqual(a, 0x88 / 255.0, places=3)

        # 6-digit hex without #
        r, g, b, a = contrast.parse_hex("1C1C1E")
        self.assertEqual((r, g, b, a), (28, 28, 30, 1.0))

        # 8-digit hex with alpha
        r, g, b, a = contrast.parse_hex("#11223380")
        self.assertEqual((r, g, b), (17, 34, 51))
        self.assertAlmostEqual(a, 128 / 255.0, places=3)

    def test_parse_hex_invalid(self):
        invalid_hexes = ["", "#", "#1", "#12", "#12345", "#1234567", "#123456789", "#GGGGGG", "xyz"]
        for val in invalid_hexes:
            with self.assertRaises(ValueError):
                contrast.parse_hex(val)

    def test_composite(self):
        # Opaque foreground retains color
        fg = (255, 0, 0, 1.0)
        bg = (0, 255, 0)
        self.assertEqual(contrast.composite(fg, bg), (255, 0, 0))

        # 50% alpha blending
        fg_half = (255, 255, 255, 0.5)
        bg_black = (0, 0, 0)
        res = contrast.composite(fg_half, bg_black)
        self.assertEqual(res, (128, 128, 128))

        # Transparent foreground gives pure background
        fg_zero = (255, 0, 0, 0.0)
        self.assertEqual(contrast.composite(fg_zero, bg), bg)

    def test_luminance_and_ratio(self):
        # Pure black luminance is 0, pure white is 1
        black = (0, 0, 0)
        white = (255, 255, 255)
        self.assertAlmostEqual(contrast.luminance(black), 0.0, places=4)
        self.assertAlmostEqual(contrast.luminance(white), 1.0, places=4)

        # Black on white ratio is 21.0
        self.assertAlmostEqual(contrast.ratio(black, white), 21.0, places=1)
        # Order should not matter
        self.assertAlmostEqual(contrast.ratio(white, black), 21.0, places=1)
        # Identical colors ratio is 1.0
        self.assertAlmostEqual(contrast.ratio(white, white), 1.0, places=2)

    def test_to_hex(self):
        self.assertEqual(contrast.to_hex((255, 255, 255)), "#FFFFFF")
        self.assertEqual(contrast.to_hex((0, 0, 0)), "#000000")
        self.assertEqual(contrast.to_hex((16, 32, 48)), "#102030")

    def test_required_thresholds(self):
        # Regular text requires 4.5:1
        need, label = contrast.required(kind="text", size=14, bold=False)
        self.assertEqual(need, 4.5)
        self.assertEqual(label, "text thường")

        # Large text (>= 24px) requires 3.0:1
        need, label = contrast.required(kind="text", size=24, bold=False)
        self.assertEqual(need, 3.0)
        self.assertEqual(label, "text lớn")

        # Large bold text (>= 18.66px and bold) requires 3.0:1
        need, label = contrast.required(kind="text", size=18.66, bold=True)
        self.assertEqual(need, 3.0)
        self.assertEqual(label, "text lớn")

        # Bold but small (< 18.66px) requires 4.5:1
        need, label = contrast.required(kind="text", size=16, bold=True)
        self.assertEqual(need, 4.5)
        self.assertEqual(label, "text thường")

        # UI elements require 3.0:1
        need, label = contrast.required(kind="ui", size=16, bold=False)
        self.assertEqual(need, 3.0)
        self.assertEqual(label, "thành phần UI")

    def test_suggest_improves_contrast(self):
        # Failing foreground #8A8A8E on white #FFFFFF
        fg_rgb = (138, 138, 142)
        bg_rgb = (255, 255, 255)
        suggested = contrast.suggest(fg_rgb, bg_rgb, target=4.5)
        self.assertIsNotNone(suggested)
        cand_rgb = contrast.parse_hex(suggested)[:3]
        self.assertGreaterEqual(contrast.ratio(cand_rgb, bg_rgb), 4.5)

        # On dark background, suggestion should move toward white
        dark_bg = (20, 20, 20)
        dark_fg = (60, 60, 60)
        suggested_light = contrast.suggest(dark_fg, dark_bg, target=4.5)
        self.assertIsNotNone(suggested_light)
        cand_light_rgb = contrast.parse_hex(suggested_light)[:3]
        self.assertGreaterEqual(contrast.ratio(cand_light_rgb, dark_bg), 4.5)

    def test_check_pass_and_fail(self):
        # High contrast pair: black on white passes
        pass_res = contrast.check("text", "#000000", "#FFFFFF", 16, False, "text")
        self.assertTrue(pass_res["pass"])
        self.assertEqual(pass_res["ratio"], 21.0)
        self.assertIsNone(pass_res["suggest"])

        # Low contrast pair: light gray on white fails and provides suggestion
        fail_res = contrast.check("caption", "#9A9A9A", "#FFFFFF", 14, False, "text")
        self.assertFalse(fail_res["pass"])
        self.assertLess(fail_res["ratio"], 4.5)
        self.assertIsNotNone(fail_res["suggest"])


class TestContrastCLI(unittest.TestCase):
    """Test command-line execution and exit codes of contrast.py."""

    def setUp(self):
        self.script_path = str(Path(__file__).parent.parent / "contrast.py")

    def test_cli_pass_exit_code_zero(self):
        cmd = [sys.executable, self.script_path, "#000000", "#FFFFFF"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("[PASS]", res.stdout)

    def test_cli_fail_exit_code_one(self):
        cmd = [sys.executable, self.script_path, "#8A8A8E", "#FFFFFF", "--size", "14"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 1)
        self.assertIn("[FAIL]", res.stdout)
        self.assertIn("gợi ý fg:", res.stdout)

    def test_cli_invalid_input_exit_code_two(self):
        cmd = [sys.executable, self.script_path, "not-a-color", "#FFFFFF"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 2)
        self.assertIn("Lỗi:", res.stderr)

    def test_cli_json_flag(self):
        cmd = [sys.executable, self.script_path, "#000000", "#FFFFFF", "--json"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertTrue(data[0]["pass"])

    def test_cli_pairs_json_file(self):
        pairs_data = [
            {"name": "header", "fg": "#000000", "bg": "#FFFFFF", "size": 20, "bold": True, "kind": "text"},
            {"name": "body", "fg": "#333333", "bg": "#FFFFFF", "size": 16, "bold": False, "kind": "text"},
            {"name": "failing_icon", "fg": "#EEEEEE", "bg": "#FFFFFF", "size": 16, "kind": "ui"},
        ]
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(pairs_data, f)
            temp_path = f.name

        try:
            cmd = [sys.executable, self.script_path, "--pairs", temp_path, "--json"]
            res = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(res.returncode, 1)  # failing_icon failed
            data = json.loads(res.stdout)
            self.assertEqual(len(data), 3)
            self.assertTrue(data[0]["pass"])
            self.assertTrue(data[1]["pass"])
            self.assertFalse(data[2]["pass"])
        finally:
            Path(temp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
