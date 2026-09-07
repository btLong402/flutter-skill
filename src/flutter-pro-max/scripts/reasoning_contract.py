#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Closed, non-executable grammar for design-system decision rules in Flutter Pro Max."""

from __future__ import annotations

import json
import re
from typing import Any

CONDITION_SIGNALS: dict[str, tuple[str, ...]] = {
    "if_booking": ("booking", "appointment", "calendar"),
    "if_boutique": ("boutique",),
    "if_casual": ("casual", "playful"),
    "if_checkout": ("checkout", "payment", "purchase"),
    "if_children": ("child", "children", "kids"),
    "if_collaboration": ("collaboration", "multiplayer", "co-edit"),
    "if_competitive": ("competitive", "leaderboard"),
    "if_content_focused": ("content", "article", "reading", "documentation"),
    "if_conversion_focused": ("conversion", "sales", "signup", "purchase"),
    "if_creative_field": ("creative", "artist", "portfolio"),
    "if_crop_focused": ("crop", "farm", "agriculture"),
    "if_dashboard": ("dashboard", "operations", "monitoring"),
    "if_data_heavy": ("data heavy", "data-heavy", "analytics", "large dataset"),
    "if_delivery": ("delivery", "courier", "shipping"),
    "if_discovery_focused": ("discover", "discovery", "browse", "directory"),
    "if_engagement_metric": ("engagement", "retention", "contribution"),
    "if_experience_focused": ("experience", "immersive", "journey"),
    "if_gamification": ("gamification", "badges", "streak"),
    "if_health": ("health", "medical", "patient"),
    "if_hero_needed": ("hero", "showcase", "launch"),
    "if_large_dataset": ("large dataset", "thousands", "millions"),
    "if_light_mode_needed": ("light mode", "light theme"),
    "if_low_performance": ("low performance", "low-end", "slow device"),
    "if_luxury": ("luxury", "premium", "high-end"),
    "if_medication": ("medication", "medicine", "prescription"),
    "if_meditation": ("meditation", "breathing", "mindfulness"),
    "if_minimal_portfolio": ("minimal portfolio", "simple portfolio"),
    "if_mobile": ("mobile", "phone", "tablet", "ios", "android"),
    "if_personalized": ("personalized", "personalised", "recommendation"),
    "if_pre_launch": ("pre-launch", "prelaunch", "coming soon", "waitlist"),
    "if_salary_focused": ("salary", "compensation", "pay range"),
    "if_team_collaboration": ("team collaboration", "team workspace"),
    "if_trust_needed": ("trust", "secure", "verified", "authority"),
    "if_ux_focused": ("ux", "usability", "accessibility", "accessible"),
    "if_video_ready": ("video ready", "product video", "demo video"),
    # Flutter & Mobile Specific Signals
    "if_offline_first": ("offline", "cache", "local-first", "sync", "sqlite"),
    "if_tablet_adaptive": ("tablet", "ipad", "foldable", "desktop", "adaptive", "responsive"),
    "if_cupertino": ("ios", "apple", "cupertino", "iphone"),
    "if_material3": ("android", "material", "material3", "m3"),
    "if_cross_platform": ("cross-platform", "multiplatform", "web and mobile"),
}

ALLOWED_CONDITIONS = {"must_have", *CONDITION_SIGNALS}
ACTION_PREFIXES = {"constraint", "style", "pattern", "mode", "architecture", "state"}
TOKEN_ACTION_PREFIXES = {"constraint", "style", "architecture", "state"}
TOKEN_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CONDITION_PATTERNS = {
    condition: tuple(
        re.compile(r"(?<!\w)" + re.escape(signal) + r"(?!\w)")
        for signal in signals
    )
    for condition, signals in CONDITION_SIGNALS.items()
}


def _object_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate decision-rule key: {key}")
        result[key] = value
    return result


def _validate_action(action: str) -> None:
    if not isinstance(action, str) or ":" not in action:
        raise ValueError(f"action must use a known prefix: {action}")
    prefix, value = action.split(":", 1)
    if prefix not in ACTION_PREFIXES:
        raise ValueError(f"unknown decision-rule action: {action}")
    if prefix in TOKEN_ACTION_PREFIXES and not TOKEN_RE.fullmatch(value):
        raise ValueError(f"invalid {prefix} action value: {value}")
    if prefix == "pattern" and not value.strip():
        raise ValueError("pattern action must name a pattern")
    if prefix == "mode" and value not in {"dark", "light"}:
        raise ValueError("mode action must be dark or light")


def parse_decision_rules(raw: str | None) -> dict[str, list[str]]:
    """Parse the condition -> action-array representation with backward compatibility."""
    if not raw or not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    
    normalized_rules: dict[str, list[str]] = {}
    for condition, raw_actions in data.items():
        cond_key = str(condition).strip()
        # Normalize actions to list of strings with prefix
        action_list: list[str] = []
        raw_items = raw_actions if isinstance(raw_actions, list) else [raw_actions]
        for item in raw_items:
            action_str = str(item).strip()
            if not action_str:
                continue
            if ":" not in action_str:
                # Default prefix for untagged action tokens
                action_str = f"constraint:{action_str}"
            action_list.append(action_str)
        
        if action_list:
            normalized_rules[cond_key] = action_list
            
    return normalized_rules


def apply_decision_rules(rules: dict[str, list[str]], query: str) -> dict[str, Any]:
    """Return deterministic mutations and an audit trail; never execute untrusted data."""
    normalized = str(query or "").casefold()
    result: dict[str, Any] = {
        "activated": [],
        "style_ids": [],
        "constraints": [],
        "architectures": [],
        "states": [],
        "pattern": None,
        "mode": None,
    }
    for condition, actions in rules.items():
        active = condition.startswith("must_have") or any(
            pattern.search(normalized)
            for pattern in CONDITION_PATTERNS.get(condition, ())
        )
        if not active:
            continue
        result["activated"].append({"condition": condition, "actions": list(actions)})
        for action in actions:
            if ":" in action:
                prefix, value = action.split(":", 1)
            else:
                prefix, value = "constraint", action

            if prefix == "style" and value not in result["style_ids"]:
                result["style_ids"].append(value)
            elif prefix == "constraint" and value not in result["constraints"]:
                result["constraints"].append(value)
            elif prefix == "architecture" and value not in result["architectures"]:
                result["architectures"].append(value)
            elif prefix == "state" and value not in result["states"]:
                result["states"].append(value)
            elif prefix == "pattern":
                result["pattern"] = value
            elif prefix == "mode":
                result["mode"] = value
    return result

