#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for developer utility tool templates (Makefile, Fastlane, Gitignore)."""

import unittest
import sys
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates" / "tools"


class TestToolsTemplates(unittest.TestCase):
    def test_makefile_template_completeness(self):
        makefile_path = TEMPLATES_DIR / "Makefile.template"
        self.assertTrue(makefile_path.exists(), "Makefile.template missing")
        content = makefile_path.read_text(encoding="utf-8")
        
        required_targets = [
            "help:", "setup:", "clean:", "get:", "build-runner:", "watch:",
            "format:", "analyze:", "test:", "coverage:",
            "build-apk-dev:", "build-apk-prod:", "build-appbundle-prod:",
            "build-ios-prod:"
        ]
        for target in required_targets:
            self.assertIn(target, content, f"Missing target: {target}")

    def test_gitignore_template(self):
        gitignore_path = TEMPLATES_DIR / "gitignore.template"
        self.assertTrue(gitignore_path.exists(), "gitignore.template missing")
        content = gitignore_path.read_text(encoding="utf-8")
        
        self.assertIn(".shared/", content)
        self.assertIn("design-system/pages/", content)
        self.assertIn("__pycache__/", content)

    def test_fastlane_templates(self):
        fastlane_dir = TEMPLATES_DIR / "fastlane"
        self.assertTrue(fastlane_dir.exists(), "fastlane templates directory missing")
        
        # Android
        android_appfile = fastlane_dir / "android" / "Appfile"
        android_fastfile = fastlane_dir / "android" / "Fastfile"
        self.assertTrue(android_appfile.exists())
        self.assertTrue(android_fastfile.exists())
        android_content = android_fastfile.read_text(encoding="utf-8")
        self.assertIn("default_platform(:android)", android_content)
        self.assertIn("lane :build_prod", android_content)
        self.assertIn("lane :deploy_play_store", android_content)

        # iOS
        ios_appfile = fastlane_dir / "ios" / "Appfile"
        ios_fastfile = fastlane_dir / "ios" / "Fastfile"
        self.assertTrue(ios_appfile.exists())
        self.assertTrue(ios_fastfile.exists())
        ios_content = ios_fastfile.read_text(encoding="utf-8")
        self.assertIn("default_platform(:ios)", ios_content)
        self.assertIn("lane :certificates", ios_content)
        self.assertIn("lane :beta_testflight", ios_content)
        self.assertIn("lane :deploy_app_store", ios_content)

        # Env example
        env_example = fastlane_dir / "env.example"
        self.assertTrue(env_example.exists())


if __name__ == "__main__":
    unittest.main()
