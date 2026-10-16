#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for Telemetry & Knowledge Gap Feedback Loop."""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from telemetry import (
    is_telemetry_enabled,
    get_telemetry_endpoint,
    build_event_payload,
    send_gap_event,
    send_gap_event_sync,
    sanitize_text,
    DEFAULT_ENDPOINT,
    VERSION,
)
from core import search, search_with_stack


class TestTelemetry(unittest.TestCase):
    def setUp(self):
        # Clean environment before each test
        self.orig_env = os.environ.copy()
        for key in ["DO_NOT_TRACK", "FLUTTER_PRO_MAX_TELEMETRY", "FLUTTER_PRO_MAX_TELEMETRY_ENDPOINT"]:
            if key in os.environ:
                del os.environ[key]

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.orig_env)

    def test_telemetry_default_enabled(self):
        self.assertTrue(is_telemetry_enabled())

    def test_respect_do_not_track(self):
        os.environ["DO_NOT_TRACK"] = "1"
        self.assertFalse(is_telemetry_enabled())

    def test_respect_flutter_telemetry_disabled(self):
        for val in ["0", "false", "off", "no", "disable"]:
            os.environ["FLUTTER_PRO_MAX_TELEMETRY"] = val
            self.assertFalse(is_telemetry_enabled(), f"Failed for val: {val}")

    def test_get_telemetry_endpoint_from_env(self):
        test_url = "https://telemetry.example.com/api/v1/gap"
        os.environ["FLUTTER_PRO_MAX_TELEMETRY_ENDPOINT"] = test_url
        self.assertEqual(get_telemetry_endpoint(), test_url)

    def test_build_event_payload_structure(self):
        payload = build_event_payload("knowledge_gap", {
            "query": "webrtc live streaming",
            "domain": "package",
            "gap_type": "empty_result",
            "result_count": 0,
        })

        self.assertEqual(payload["event_type"], "knowledge_gap")
        self.assertEqual(payload["query"], "webrtc live streaming")
        self.assertEqual(payload["domain"], "package")
        self.assertIn("timestamp", payload)
        self.assertIn("client", payload)
        self.assertEqual(payload["client"]["version"], VERSION)
        self.assertIn("os", payload["client"])
        self.assertIn("ai_assistant", payload["client"])

    @patch("telemetry.record_local_gap")
    def test_send_gap_event_when_disabled(self, mock_record):
        os.environ["DO_NOT_TRACK"] = "1"
        res = send_gap_event("knowledge_gap", {"query": "test"})
        self.assertIsNone(res)
        mock_record.assert_not_called()

    @patch("telemetry.record_local_gap")
    def test_send_gap_event_sync_dispatches(self, mock_record):
        payload = send_gap_event_sync("knowledge_gap", {"query": "test_query", "gap_type": "empty_result"})
        self.assertIsNotNone(payload)
        self.assertEqual(payload["query"], "test_query")
        mock_record.assert_called_once()

    def test_search_detects_empty_gap(self):
        res = search("definitely_nonexistent_flutter_query_xyz_9999", domain="widget")
        self.assertTrue(res.get("gap_detected"))
        self.assertEqual(res.get("gap_type"), "empty_result")
        self.assertEqual(res.get("count"), 0)

    def test_search_detects_weak_match_forced_search(self):
        # shorebird code push in widget domain should be a weak match because widget.csv has no shorebird
        res = search("shorebird code push", domain="widget")
        self.assertTrue(res.get("gap_detected"))
        self.assertEqual(res.get("gap_type"), "weak_match")

    def test_default_endpoint_resolution(self):
        self.assertEqual(get_telemetry_endpoint(), DEFAULT_ENDPOINT)

    def test_sanitize_text_filters_sensitive_data(self):
        # 1. Local path
        self.assertEqual(sanitize_text("Find file in /Users/johndoe/project/secret.dart"), "Find file in [PATH]")
        # 2. Email
        self.assertEqual(sanitize_text("Contact support@company.com now"), "Contact [EMAIL] now")
        # 3. Secret API key / Bearer token
        self.assertEqual(sanitize_text("Use key sk-1234567890abcdef1234567890 for auth"), "Use key [SECRET] for auth")
        self.assertEqual(sanitize_text("Token Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xyz"), "Token [SECRET]")
        # 4. IP address
        self.assertEqual(sanitize_text("Connect to 192.168.1.100 port 8080"), "Connect to [IP] port 8080")
        # 5. Length truncation
        long_str = "normal words text without hex hashes " * 20
        self.assertEqual(len(sanitize_text(long_str, max_length=150)), 150)

    def test_build_event_payload_sanitizes_query_and_notes(self):
        payload = build_event_payload("knowledge_gap", {
            "query": "Fix bug in /Users/developer/app/main.dart with user@domain.com",
            "domain": "widget",
            "notes": "Bearer sk-12345678901234567890",
        })
        self.assertEqual(payload["query"], "Fix bug in [PATH] with [EMAIL]")
        self.assertEqual(payload["notes"], "[SECRET]")

    def test_search_strong_match_no_gap(self):
        res = search("ListView", domain="widget")
        self.assertFalse(res.get("gap_detected"))
        self.assertIsNone(res.get("gap_type"))
        self.assertGreater(res.get("count"), 0)


if __name__ == "__main__":
    unittest.main()

