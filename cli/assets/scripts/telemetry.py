#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flutter Pro Max Telemetry & Knowledge Gap Dispatcher
Zero-dependency telemetry engine using standard Python library.

Captures:
1. Knowledge misses (empty search results & weak BM25 matches)
2. Criteria gaps in UI/UX audit (unrecognized or missing dimensions)
3. Explicit user/AI feedback via --report-gap

Privacy-First & Data Sanitization:
- Default endpoint: https://flutter-pro-max-telemetry.longbt.workers.dev/api/telemetry
- Automatically strips local paths, emails, API keys/tokens, and IP addresses.
- Never collects source code, file contents, or personal credentials.
- Respects DO_NOT_TRACK=1 and FLUTTER_PRO_MAX_TELEMETRY=0.
- Asynchronous daemon thread dispatch with 1.5s network timeout and silent error suppression.
- Local persistence fallback in ~/.flutter-pro-max/gaps.jsonl.
"""

from __future__ import annotations

import json
import os
import platform
import re
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import request, error

# ============ CONFIGURATION ============
VERSION = "2.8.0"
DEFAULT_TIMEOUT_SECONDS = 1.5
DEFAULT_ENDPOINT = "https://flutter-pro-max-telemetry.longbt.workers.dev/api/telemetry"
CONFIG_DIR = Path.home() / ".flutter-pro-max"
LOCAL_GAPS_FILE = CONFIG_DIR / "gaps.jsonl"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Sanitization regex patterns
RE_LOCAL_PATH = re.compile(r"(/[a-zA-Z0-9_.-]+){2,}|[a-zA-Z]:\\[a-zA-Z0-9_.\\]+", re.IGNORECASE)
RE_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
RE_SECRET_TOKEN = re.compile(
    r"(sk-[a-zA-Z0-9_-]{15,}|ghp_[a-zA-Z0-9]{20,}|Bearer\s+[a-zA-Z0-9._-]+|eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}|[0-9a-fA-F]{32,})",
    re.IGNORECASE
)
RE_IP_ADDRESS = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")


def sanitize_text(text: str | None, max_length: int = 200) -> str:
    """Sanitize and anonymize text before transmission."""
    if not text:
        return ""
    s = str(text)
    # Mask secrets & credentials first
    s = RE_SECRET_TOKEN.sub("[SECRET]", s)
    # Mask personal file paths
    s = RE_LOCAL_PATH.sub("[PATH]", s)
    # Mask email addresses
    s = RE_EMAIL.sub("[EMAIL]", s)
    # Mask IP addresses
    s = RE_IP_ADDRESS.sub("[IP]", s)
    # Normalize whitespaces and truncate
    s = " ".join(s.split())
    return s[:max_length]


def is_telemetry_enabled() -> bool:
    """Check if telemetry is enabled based on environment and user config."""
    # Standard opt-out variable
    if os.environ.get("DO_NOT_TRACK") == "1":
        return False

    # Skill-specific opt-out variables
    env_val = os.environ.get("FLUTTER_PRO_MAX_TELEMETRY", "").strip().lower()
    if env_val in ("0", "false", "off", "no", "disable", "disabled"):
        return False

    # Check config file if exists
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                if cfg.get("telemetry") is False:
                    return False
    except Exception:
        pass

    return True


def get_telemetry_endpoint() -> str:
    """Resolve telemetry cloud endpoint from environment, config file, or default."""
    # 1. Environment variable priority
    env_endpoint = (
        os.environ.get("FLUTTER_PRO_MAX_TELEMETRY_ENDPOINT")
        or os.environ.get("FLUTTER_PRO_MAX_CLOUD_URL")
    )
    if env_endpoint and env_endpoint.strip():
        return env_endpoint.strip()

    # 2. Config file fallback
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                ep = cfg.get("endpoint") or cfg.get("telemetry_endpoint")
                if ep and str(ep).strip():
                    return str(ep).strip()
    except Exception:
        pass

    # 3. Default production endpoint
    return DEFAULT_ENDPOINT


def detect_client_ai() -> str:
    """Detect client AI assistant environment from common indicators."""
    cwd = Path.cwd()
    if (cwd / ".claude").exists() or (cwd / "CLAUDE.md").exists():
        return "claude"
    if (cwd / ".cursor").exists() or (cwd / ".cursorrules").exists():
        return "cursor"
    if (cwd / ".agents").exists() or (cwd / "AGENTS.md").exists():
        return "antigravity"
    if (cwd / ".windsurf").exists():
        return "windsurf"
    if (cwd / ".github" / "copilot-instructions.md").exists():
        return "copilot"
    if (cwd / ".gemini").exists():
        return "gemini"
    return "cli"


def build_event_payload(event_type: str, data: dict[str, Any]) -> dict[str, Any]:
    """Construct a clean, anonymized telemetry payload."""
    now_utc = datetime.now(timezone.utc).isoformat()
    payload: dict[str, Any] = {
        "event_type": event_type,
        "timestamp": now_utc,
        "client": {
            "version": VERSION,
            "os": platform.system().lower(),
            "python": f"{sys.version_info.major}.{sys.version_info.minor}",
            "ai_assistant": detect_client_ai(),
        },
    }

    # Sanitize data fields
    sanitized_data: dict[str, Any] = {}
    for k, v in data.items():
        if isinstance(v, str):
            sanitized_data[k] = sanitize_text(v, max_length=300 if k in ("notes", "reason") else 200)
        elif isinstance(v, list) and all(isinstance(item, str) for item in v):
            sanitized_data[k] = [sanitize_text(item, max_length=100) for item in v]
        else:
            sanitized_data[k] = v

    payload.update(sanitized_data)
    return payload


def record_local_gap(payload: dict[str, Any]) -> None:
    """Persist gap event to ~/.flutter-pro-max/gaps.jsonl for local review."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(LOCAL_GAPS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _dispatch_worker(payload: dict[str, Any], endpoint: str | None) -> None:
    """Worker function executed in daemon thread to send telemetry without blocking."""
    # Always persist locally first so no feedback is ever lost
    record_local_gap(payload)

    if not endpoint:
        return

    try:
        data_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = request.Request(
            endpoint,
            data=data_bytes,
            headers={
                "Content-Type": "application/json",
                "User-Agent": f"FlutterProMax-Telemetry/{VERSION}",
            },
            method="POST",
        )
        with request.urlopen(req, timeout=DEFAULT_TIMEOUT_SECONDS) as _:
            pass
    except Exception:
        # Fail silently to guarantee zero interruption to user workflow
        pass


_ACTIVE_THREADS: list[threading.Thread] = []


def _flush_telemetry_on_exit() -> None:
    """Allow background dispatch threads a brief grace period to flush before process exit."""
    for t in _ACTIVE_THREADS:
        try:
            if t.is_alive():
                t.join(timeout=1.0)
        except Exception:
            pass


import atexit
atexit.register(_flush_telemetry_on_exit)


def send_gap_event(event_type: str, data: dict[str, Any]) -> dict[str, Any] | None:
    """
    Dispatch a gap event asynchronously via a background thread.
    Returns the payload constructed, or None if telemetry is disabled.
    """
    if not is_telemetry_enabled():
        return None

    payload = build_event_payload(event_type, data)
    endpoint = get_telemetry_endpoint()

    # Dispatch in background thread with atexit grace period
    thread = threading.Thread(
        target=_dispatch_worker,
        args=(payload, endpoint),
        daemon=True,
        name="telemetry-dispatcher",
    )
    _ACTIVE_THREADS.append(thread)
    thread.start()
    return payload


def send_gap_event_sync(event_type: str, data: dict[str, Any]) -> dict[str, Any] | None:
    """Synchronous dispatch helper used primarily for testing."""
    if not is_telemetry_enabled():
        return None

    payload = build_event_payload(event_type, data)
    endpoint = get_telemetry_endpoint()
    _dispatch_worker(payload, endpoint)
    return payload
