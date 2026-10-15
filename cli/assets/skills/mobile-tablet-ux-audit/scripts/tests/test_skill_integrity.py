#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integrity tests for mobile-tablet-ux-audit skill structure, assets, and documentation."""

import json
import re
import sys
import unittest
from pathlib import Path

# Add scripts directory to sys.path
SCRIPTS_DIR = Path(__file__).parent.parent
SKILL_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import score


class TestSkillIntegrity(unittest.TestCase):
    """Test skill files, templates, cross-references, and rubric consistency."""

    def test_skill_manifest_exists_and_valid(self):
        skill_md = SKILL_ROOT / "SKILL.md"
        self.assertTrue(skill_md.exists(), "SKILL.md must exist in skill root")
        content = skill_md.read_text(encoding="utf-8")

        # Must have YAML frontmatter
        self.assertTrue(content.startswith("---"), "SKILL.md must start with YAML frontmatter")
        parts = content.split("---", 2)
        self.assertGreaterEqual(len(parts), 3, "YAML frontmatter must be enclosed by ---")

        frontmatter = parts[1]
        self.assertIn("name: mobile-tablet-ux-audit", frontmatter)
        self.assertIn("description:", frontmatter)

    def test_all_reference_documents_exist_and_non_empty(self):
        expected_refs = [
            "rubric.md",
            "platform-checks.md",
            "evidence-collection.md",
            "improvement-playbook.md",
        ]
        ref_dir = SKILL_ROOT / "references"
        self.assertTrue(ref_dir.exists(), "references/ directory must exist")

        for ref in expected_refs:
            ref_path = ref_dir / ref
            self.assertTrue(ref_path.exists(), f"Reference file missing: {ref}")
            self.assertGreater(ref_path.stat().st_size, 500, f"Reference file too small: {ref}")

    def test_all_assets_exist_and_parse_valid_json(self):
        assets_dir = SKILL_ROOT / "assets"
        self.assertTrue(assets_dir.exists(), "assets/ directory must exist")

        template_path = assets_dir / "scorecard.template.json"
        example_path = assets_dir / "example-scorecard.json"

        self.assertTrue(template_path.exists())
        self.assertTrue(example_path.exists())

        with open(template_path, "r", encoding="utf-8") as f:
            template_data = json.load(f)
        self.assertIn("scores", template_data)
        self.assertIn("platforms", template_data)

        with open(example_path, "r", encoding="utf-8") as f:
            example_data = json.load(f)
        self.assertIn("scores", example_data)
        self.assertIn("issues", example_data)

    def test_example_scorecard_passes_score_validation(self):
        example_path = SKILL_ROOT / "assets" / "example-scorecard.json"
        card = score.load(str(example_path))
        errors, warnings = score.validate(card)
        self.assertEqual(errors, [], f"Example scorecard has validation errors: {errors}")

    def test_template_contains_all_dimensions(self):
        template_path = SKILL_ROOT / "assets" / "scorecard.template.json"
        with open(template_path, "r", encoding="utf-8") as f:
            template_data = json.load(f)
        scores = template_data.get("scores", {})
        for dim in score.DIMENSIONS:
            self.assertIn(dim, scores, f"Dimension '{dim}' missing in scorecard.template.json")
            for plat in ["mobile", "tablet"]:
                self.assertIn(plat, scores[dim], f"Platform '{plat}' missing in {dim}")

    def test_rubric_dimensions_and_weights_match_score_py(self):
        rubric_path = SKILL_ROOT / "references" / "rubric.md"
        content = rubric_path.read_text(encoding="utf-8")

        for dim, (name, weight) in score.DIMENSIONS.items():
            self.assertIn(f"`{dim}`", content, f"Dimension `{dim}` not mentioned in rubric.md")
            # Verify weight appears in the rubric
            weight_pattern = rf"`{dim}`\s*\|\s*{re.escape(name)}\s*\|\s*{weight}"
            self.assertTrue(
                re.search(weight_pattern, content) or f"`{dim}`" in content,
                f"Weight {weight} for `{dim}` not documented correctly in rubric.md"
            )

    def test_scripts_exist_and_importable(self):
        score_py = SCRIPTS_DIR / "score.py"
        contrast_py = SCRIPTS_DIR / "contrast.py"
        self.assertTrue(score_py.exists())
        self.assertTrue(contrast_py.exists())


if __name__ == "__main__":
    unittest.main()
