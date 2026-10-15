#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for score.py UX audit calculation and validation engine."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Add scripts directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))
import score


def get_base_valid_card():
    """Helper returning a minimal valid scorecard dictionary."""
    card = {
        "app": "TestApp",
        "iteration": 1,
        "platforms": ["mobile", "tablet"],
        "scores": {},
        "issues": []
    }
    for dim in score.DIMENSIONS:
        card["scores"][dim] = {
            "mobile": {"score": 3.5, "confidence": "high", "evidence": ["E-mob-1", "E-mob-2"]},
            "tablet": {"score": 3.5, "confidence": "high", "evidence": ["E-tab-1", "E-tab-2"]},
        }
    return card


class TestDimensionConfig(unittest.TestCase):
    """Test configuration constants and definitions."""

    def test_dimensions_count_and_weights(self):
        self.assertEqual(len(score.DIMENSIONS), 10)
        total_weight = sum(weight for _, weight in score.DIMENSIONS.values())
        self.assertEqual(total_weight, 100)

    def test_grade_thresholds(self):
        self.assertEqual(score.grade(95), "Xuất sắc")
        self.assertEqual(score.grade(90), "Xuất sắc")
        self.assertEqual(score.grade(85), "Tốt")
        self.assertEqual(score.grade(80), "Tốt")
        self.assertEqual(score.grade(75), "Đạt")
        self.assertEqual(score.grade(70), "Đạt")
        self.assertEqual(score.grade(65), "Cần cải thiện")
        self.assertEqual(score.grade(60), "Cần cải thiện")
        self.assertEqual(score.grade(59.9), "Kém")
        self.assertEqual(score.grade(0), "Kém")


class TestCardValidation(unittest.TestCase):
    """Test scorecard validation logic and error/warning generation."""

    def test_valid_card_passes_without_errors(self):
        card = get_base_valid_card()
        errors, warnings = score.validate(card)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_invalid_platform_configuration(self):
        card = get_base_valid_card()
        card["platforms"] = ["desktop"]
        errors, _ = score.validate(card)
        self.assertTrue(any("Nền tảng không hợp lệ" in e for e in errors))

        # Both platforms list and scores empty -> cannot detect platforms
        card["platforms"] = []
        card["scores"] = {}
        errors, _ = score.validate(card)
        self.assertTrue(any("Không xác định được nền tảng" in e for e in errors))

    def test_missing_dimension_cell(self):
        card = get_base_valid_card()
        del card["scores"]["accessibility"]["mobile"]
        errors, _ = score.validate(card)
        self.assertTrue(any("accessibility.mobile: thiếu ô điểm" in e for e in errors))

    def test_invalid_score_values(self):
        card = get_base_valid_card()
        # Non-numeric
        card["scores"]["typography"]["mobile"]["score"] = "four"
        errors, _ = score.validate(card)
        self.assertTrue(any("score phải là số" in e for e in errors))

        # Boolean (bool is subclass of int in Python)
        card["scores"]["typography"]["mobile"]["score"] = True
        errors, _ = score.validate(card)
        self.assertTrue(any("score phải là số" in e for e in errors))

        # Out of bounds (< 0 or > 5)
        card["scores"]["typography"]["mobile"]["score"] = 5.5
        errors, _ = score.validate(card)
        self.assertTrue(any("score 5.5 không hợp lệ" in e for e in errors))

        # Invalid step (not multiple of 0.5)
        card["scores"]["typography"]["mobile"]["score"] = 3.3
        errors, _ = score.validate(card)
        self.assertTrue(any("score 3.3 không hợp lệ" in e for e in errors))

    def test_confidence_validation_and_capping_warning(self):
        card = get_base_valid_card()
        # Invalid confidence key
        card["scores"]["typography"]["mobile"]["confidence"] = "ultra"
        errors, _ = score.validate(card)
        self.assertTrue(any("confidence phải là low|medium|high" in e for e in errors))

        # Score exceeds confidence cap -> triggers warning
        card = get_base_valid_card()
        card["scores"]["typography"]["mobile"]["score"] = 4.0
        card["scores"]["typography"]["mobile"]["confidence"] = "low"  # cap is 3.5
        _, warnings = score.validate(card)
        self.assertTrue(any("vượt trần của confidence 'low'" in w for w in warnings))

    def test_evidence_validation_and_count_warning(self):
        card = get_base_valid_card()
        # Missing evidence
        card["scores"]["typography"]["mobile"]["evidence"] = []
        errors, _ = score.validate(card)
        self.assertTrue(any("thiếu evidence" in e for e in errors))

        # Score >= 4 with only 1 evidence -> triggers warning
        card = get_base_valid_card()
        card["scores"]["typography"]["mobile"]["score"] = 4.5
        card["scores"]["typography"]["mobile"]["evidence"] = ["Only 1 evidence"]
        _, warnings = score.validate(card)
        self.assertTrue(any("điểm 4.5 ≥ 4 nhưng chỉ có 1 bằng chứng" in w for w in warnings))

    def test_issue_validation(self):
        card = get_base_valid_card()
        card["issues"] = [
            {
                "id": "ISSUE-1",
                "dimension": "accessibility",
                "platform": "mobile",
                "severity": "major",
                "description": "Missing labels",
                "effort": 2,
                "reach": 2,
                "status": "open",
                "fix": "Add semantics"
            },
            {
                "id": "ISSUE-1",  # duplicate ID
                "dimension": "typography",
                "platform": "tablet",
                "severity": "minor",
                "description": "Small text",
                "effort": 1,
                "reach": 1,
                "status": "open"
            }
        ]
        errors, _ = score.validate(card)
        self.assertTrue(any("ID issue bị trùng" in e for e in errors))

        # Missing fix warning for major/blocker
        card["issues"][1]["id"] = "ISSUE-2"
        card["issues"][0]["fix"] = ""  # major without fix
        _, warnings = score.validate(card)
        self.assertTrue(any("lỗi major nên có đề xuất sửa" in w for w in warnings))

        # Invalid effort / reach
        card["issues"][0]["effort"] = 4
        errors, _ = score.validate(card)
        self.assertTrue(any("effort phải là 1, 2 hoặc 3" in e for e in errors))


class TestCalculationsAndCaps(unittest.TestCase):
    """Test effective score calculation, platform scoring, and cap rules."""

    def test_effective_score_with_confidence_caps(self):
        # High confidence allows full score up to 5.0
        self.assertEqual(score.effective({"score": 5.0, "confidence": "high"}), 5.0)
        # Medium confidence caps at 4.0
        self.assertEqual(score.effective({"score": 4.5, "confidence": "medium"}), 4.0)
        self.assertEqual(score.effective({"score": 3.5, "confidence": "medium"}), 3.5)
        # Low confidence caps at 3.5
        self.assertEqual(score.effective({"score": 4.5, "confidence": "low"}), 3.5)
        self.assertEqual(score.effective({"score": 3.0, "confidence": "low"}), 3.0)

    def test_perfect_score_yields_100(self):
        card = get_base_valid_card()
        for dim in score.DIMENSIONS:
            for p in ["mobile", "tablet"]:
                card["scores"][dim][p] = {"score": 5.0, "confidence": "high", "evidence": ["E1", "E2"]}
        res = score.platform_result(card, "mobile")
        self.assertEqual(res["raw"], 100.0)
        self.assertEqual(res["final"], 100.0)
        self.assertEqual(res["grade"], "Xuất sắc")

    def test_blocker_issue_caps_at_59(self):
        card = get_base_valid_card()
        for dim in score.DIMENSIONS:
            card["scores"][dim]["mobile"] = {"score": 5.0, "confidence": "high", "evidence": ["E1", "E2"]}
        card["issues"] = [{
            "id": "BLK-01",
            "dimension": "visual_hierarchy_layout",
            "platform": "mobile",
            "severity": "blocker",
            "description": "App crashes on launch",
            "status": "open",
            "fix": "Fix crash"
        }]
        res = score.platform_result(card, "mobile")
        self.assertEqual(res["raw"], 100.0)
        self.assertEqual(res["final"], 59.0)
        self.assertTrue(any("có lỗi blocker còn mở" in cap[0] for cap in res["caps"]))

        # Fixed blocker does NOT trigger cap
        card["issues"][0]["status"] = "fixed"
        res_fixed = score.platform_result(card, "mobile")
        self.assertEqual(res_fixed["final"], 100.0)

    def test_dimension_under_1_5_caps_at_69(self):
        card = get_base_valid_card()
        for dim in score.DIMENSIONS:
            card["scores"][dim]["mobile"] = {"score": 4.5, "confidence": "high", "evidence": ["E1", "E2"]}
        # Set one dimension to 1.5
        card["scores"]["typography"]["mobile"]["score"] = 1.5
        res = score.platform_result(card, "mobile")
        self.assertLess(res["final"], res["raw"])
        self.assertEqual(res["final"], 69.0)
        self.assertTrue(any("tiêu chí ≤ 1.5" in cap[0] for cap in res["caps"]))

    def test_accessibility_under_3_caps_at_79(self):
        card = get_base_valid_card()
        for dim in score.DIMENSIONS:
            card["scores"][dim]["mobile"] = {"score": 4.5, "confidence": "high", "evidence": ["E1", "E2"]}
        # Set accessibility to 2.5
        card["scores"]["accessibility"]["mobile"]["score"] = 2.5
        res = score.platform_result(card, "mobile")
        self.assertLess(res["final"], res["raw"])
        self.assertEqual(res["final"], 79.0)
        self.assertTrue(any("accessibility < 3" in cap[0] for cap in res["caps"]))


class TestBacklogAndPrioritization(unittest.TestCase):
    """Test prioritization formula and backlog ranking."""

    def test_backlog_priority_formula(self):
        # Priority = (severity * reach * weight) / effort
        # Accessibility weight = 14
        # Blocker (8) * reach (3) * 14 / effort (1) = 336.0
        card = get_base_valid_card()
        card["issues"] = [
            {
                "id": "AC-01",
                "dimension": "accessibility",
                "platform": "both",
                "severity": "blocker",
                "reach": 3,
                "effort": 1,
                "description": "Screen reader unusable",
                "status": "open"
            },
            {
                "id": "TY-01",
                "dimension": "typography",  # weight 8
                "platform": "mobile",
                "severity": "minor",        # severity 2
                "reach": 1,
                "effort": 2,
                "description": "Font size 12 too small",
                "status": "open"
            },
            {
                "id": "FIXED-01",
                "dimension": "accessibility",
                "platform": "both",
                "severity": "blocker",
                "status": "fixed",
                "description": "Already fixed"
            }
        ]
        b = score.backlog(card, ["mobile", "tablet"])
        self.assertEqual(len(b), 2)  # FIXED-01 excluded
        self.assertEqual(b[0]["id"], "AC-01")
        self.assertEqual(b[0]["priority"], 336.0)
        # TY-01: (2 * 1 * 8) / 2 = 8.0
        self.assertEqual(b[1]["id"], "TY-01")
        self.assertEqual(b[1]["priority"], 8.0)


class TestComputeAndComparison(unittest.TestCase):
    """Test overall score calculation, delta comparison, and verdict logic."""

    def test_compute_weighting(self):
        card = get_base_valid_card()
        # Set mobile to 80 and tablet to 60
        for dim in score.DIMENSIONS:
            card["scores"][dim]["mobile"] = {"score": 4.0, "confidence": "high", "evidence": ["E1", "E2"]}
            card["scores"][dim]["tablet"] = {"score": 3.0, "confidence": "high", "evidence": ["E1", "E2"]}

        # 50/50 weighting: (80 + 60) / 2 = 70.0
        res_50 = score.compute(card, tablet_weight=0.5)
        self.assertAlmostEqual(res_50["overall"], 70.0)

        # 30% tablet weighting: 0.7 * 80 + 0.3 * 60 = 74.0
        res_30 = score.compute(card, tablet_weight=0.3)
        self.assertAlmostEqual(res_30["overall"], 74.0)

    def test_compare_and_regressions(self):
        prev_card = get_base_valid_card()
        cur_card = copy.deepcopy(prev_card)

        # Introduce a regression of >= 1.0 on mobile typography
        prev_card["scores"]["typography"]["mobile"]["score"] = 4.5
        cur_card["scores"]["typography"]["mobile"]["score"] = 3.0  # delta = -1.5

        # Improvement on tablet touch_interaction
        prev_card["scores"]["touch_interaction"]["tablet"]["score"] = 2.0
        cur_card["scores"]["touch_interaction"]["tablet"]["score"] = 3.5  # delta = +1.5

        prev_sum = score.compute(prev_card, tablet_weight=0.5)
        cur_sum = score.compute(cur_card, tablet_weight=0.5)

        cmp = score.compare(cur_sum, prev_sum)
        self.assertEqual(len(cmp["regressions"]), 1)
        self.assertEqual(cmp["regressions"][0][:2], ("mobile", "typography"))
        self.assertEqual(len(cmp["improvements"]), 1)
        self.assertEqual(cmp["improvements"][0][:2], ("tablet", "touch_interaction"))

    def test_verdict_states(self):
        base_dims = {d: {"effective": 3.5} for d in score.DIMENSIONS}
        # Case 1: Regression triggers REVERT_RECOMMENDED
        summary = {"platforms": ["mobile"], "results": {"mobile": {"final": 75.0, "dims": base_dims}}, "overall": 75.0, "backlog": []}
        cmp_reg = {"overall_delta": 2.0, "regressions": [("mobile", "typography", -1.5)], "improvements": []}
        v, notes = score.verdict(summary, cmp_reg, target=85.0)
        self.assertEqual(v, "REVERT_RECOMMENDED")

        # Case 2: Overall drop triggers REVERT_RECOMMENDED
        cmp_drop = {"overall_delta": -1.0, "regressions": [], "improvements": []}
        v, notes = score.verdict(summary, cmp_drop, target=85.0)
        self.assertEqual(v, "REVERT_RECOMMENDED")

        # Case 3: Passing condition: overall >= 85, no blockers, min dim >= 3.5
        summary_pass = {
            "platforms": ["mobile"],
            "overall": 88.0,
            "results": {
                "mobile": {
                    "final": 88.0,
                    "dims": {d: {"effective": 4.0} for d in score.DIMENSIONS}
                }
            },
            "backlog": []
        }
        v, notes = score.verdict(summary_pass, None, target=85.0)
        self.assertEqual(v, "PASS")


class TestScoreCLI(unittest.TestCase):
    """Test CLI execution and outputs of score.py."""

    def setUp(self):
        self.script_path = str(Path(__file__).parent.parent / "score.py")
        self.example_card = str(Path(__file__).parent.parent.parent / "assets" / "example-scorecard.json")

    def test_cli_runs_example_scorecard_successfully(self):
        cmd = [sys.executable, self.script_path, self.example_card]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("Báo cáo UI/UX", res.stdout)
        self.assertIn("Điểm tổng:", res.stdout)

    def test_cli_markdown_and_json_export(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as out_md, \
             tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as out_json:
            md_path = out_md.name
            json_path = out_json.name

        try:
            cmd = [
                sys.executable, self.script_path, self.example_card,
                "--out", md_path,
                "--json-out", json_path,
                "--top", "3"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0)

            # Verify markdown file exists and has content
            self.assertTrue(Path(md_path).exists())
            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()
            self.assertIn("# Báo cáo UI/UX", md_content)

            # Verify JSON file structure
            self.assertTrue(Path(json_path).exists())
            with open(json_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)
            self.assertIn("overall", json_data)
            self.assertIn("platforms", json_data)
            self.assertIn("backlog", json_data)
        finally:
            Path(md_path).unlink(missing_ok=True)
            Path(json_path).unlink(missing_ok=True)

    def test_cli_invalid_scorecard_fails(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write('{"invalid": true}')
            bad_path = f.name

        try:
            cmd = [sys.executable, self.script_path, bad_path]
            res = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(res.returncode, 2)
            self.assertIn("Scorecard không hợp lệ", res.stderr)
        finally:
            Path(bad_path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
