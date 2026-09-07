#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flutter Pro Max Design System Generator - Aggregates search results and applies reasoning
to generate comprehensive design system recommendations for Flutter apps.

Features:
- Multi-domain search (product, style, color, typography, pattern, architect, landing, motion)
- Closed-grammar reasoning contract for deterministic decision rules
- Design dials: --variance (1-10), --motion (1-10), --density (1-10)
- Dart Code Generator: --export-dart (generates production ThemeData & ThemeExtension)
- Master + Page Overrides persistence pattern

Usage:
    from design_system import generate_design_system
    result = generate_design_system("fintech banking app", "MyApp")
    
    # With dials
    result = generate_design_system("crypto trading", "CryptoApp", variance=8, motion=5, density=9)
    
    # Export Dart theme
    result = generate_design_system("ecommerce shop", "ShopApp", export_dart=True)
    
    # With persistence (Master + Overrides pattern)
    result = generate_design_system("fintech banking app", "MyApp", persist=True)
    result = generate_design_system("fintech banking app", "MyApp", persist=True, page="dashboard")
"""

from __future__ import annotations

import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from core import search, DATA_DIR
from reasoning_contract import parse_decision_rules, apply_decision_rules


# ============ CONFIGURATION ============
REASONING_FILE = "ui-reasoning.csv"
MOTION_FILE = "flutter-motion.csv"

SEARCH_CONFIG = {
    "product": {"max_results": 1},
    "style": {"max_results": 3},
    "color": {"max_results": 2},
    "typography": {"max_results": 2},
    "pattern": {"max_results": 3},
    "architect": {"max_results": 2},
    "landing": {"max_results": 2},
    "motion": {"max_results": 2}
}


# ============ DESIGN DIALS (1-10) ============
DIAL_TIERS = {
    "variance": [
        (1, 3, {"label": "Centered / Minimalist", "style_keywords": ["Minimalism", "Flat Design", "Clean", "Strict Grid"]}),
        (4, 7, {"label": "Balanced / Modern Material 3", "style_keywords": ["Material 3", "Modern Clean", "Soft UI", "Balanced"]}),
        (8, 10, {"label": "Bold / Expressive / Bento", "style_keywords": ["Brutalism", "Bento Grids", "Neumorphism", "Expressive"]}),
    ],
    "motion": [
        (1, 3, {"label": "Subtle", "tier": "Subtle"}),
        (4, 7, {"label": "Standard", "tier": "Standard"}),
        (8, 10, {"label": "Complex", "tier": "Complex"}),
    ],
    "density": [
        (1, 3, {
            "label": "Spacious / Comfortable",
            "visual_density": "VisualDensity.comfortable",
            "spacing": {"xs": 6.0, "sm": 12.0, "md": 24.0, "lg": 36.0, "xl": 48.0, "xxl": 64.0}
        }),
        (4, 7, {
            "label": "Standard Material",
            "visual_density": "VisualDensity.standard",
            "spacing": {"xs": 4.0, "sm": 8.0, "md": 16.0, "lg": 24.0, "xl": 32.0, "xxl": 48.0}
        }),
        (8, 10, {
            "label": "Compact / High-Density Dashboard",
            "visual_density": "VisualDensity.compact",
            "spacing": {"xs": 2.0, "sm": 4.0, "md": 8.0, "lg": 12.0, "xl": 16.0, "xxl": 24.0}
        }),
    ],
}


def _resolve_dial(dial_name: str, value: int | str | None) -> dict[str, Any] | None:
    """Bucket a 1-10 dial value into its tier config. Returns None if value is None."""
    if value is None:
        return None
    try:
        val = max(1, min(10, int(value)))
    except (ValueError, TypeError):
        return None
    for lo, hi, info in DIAL_TIERS[dial_name]:
        if lo <= val <= hi:
            return {**info, "value": val}
    return None


def hex_to_flutter_color(hex_str: str, default: str = "#2563EB") -> str:
    """Convert hex string (#RRGGBB or #RGB) to Flutter Color(0xFFRRGGBB)."""
    clean = (hex_str or default).strip().lstrip("#")
    if len(clean) == 3:
        clean = "".join(c * 2 for c in clean)
    if len(clean) != 6:
        clean = "2563EB"
    return f"Color(0xFF{clean.upper()})"


# ============ DESIGN SYSTEM GENERATOR ============
class DesignSystemGenerator:
    """Generates design system recommendations from aggregated searches with dial control."""

    def __init__(self) -> None:
        self.reasoning_data: list[dict[str, str]] = self._load_reasoning()
        self.motion_data: list[dict[str, str]] = self._load_motions()

    def _load_reasoning(self) -> list[dict[str, str]]:
        """Load reasoning rules from CSV."""
        filepath = DATA_DIR / REASONING_FILE
        if not filepath.exists():
            return []
        with open(filepath, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    def _load_motions(self) -> list[dict[str, str]]:
        """Load flutter motion presets from CSV."""
        filepath = DATA_DIR / MOTION_FILE
        if not filepath.exists():
            return []
        with open(filepath, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    def _multi_domain_search(self, query: str, style_priority: list[str] | None = None) -> dict[str, Any]:
        """Execute searches across multiple domains."""
        results: dict[str, Any] = {}
        for domain, config in SEARCH_CONFIG.items():
            if domain == "style" and style_priority:
                priority_query = " ".join(style_priority[:2]) if style_priority else query
                combined_query = f"{query} {priority_query}"
                results[domain] = search(combined_query, domain, config["max_results"])
            else:
                results[domain] = search(query, domain, config["max_results"])
        return results

    def _find_reasoning_rule(self, category: str) -> dict[str, str]:
        """Find matching reasoning rule for a category."""
        category_lower = category.lower()
        for rule in self.reasoning_data:
            if rule.get("App_Category", "").lower() == category_lower:
                return rule
        for rule in self.reasoning_data:
            app_cat = rule.get("App_Category", "").lower()
            if app_cat in category_lower or category_lower in app_cat:
                return rule
        for rule in self.reasoning_data:
            app_cat = rule.get("App_Category", "").lower()
            keywords = app_cat.replace("/", " ").replace("-", " ").split()
            if any(kw in category_lower for kw in keywords):
                return rule
        return {}

    def _apply_reasoning(self, category: str, query: str) -> dict[str, Any]:
        """Apply reasoning rules using closed grammar contract."""
        rule = self._find_reasoning_rule(category)

        if not rule:
            return {
                "pattern": "Clean Architecture + Feature-First",
                "style_priority": ["Minimalism", "Flat Design"],
                "color_mood": "Professional",
                "typography_mood": "Clean",
                "key_effects": "Subtle animations, smooth transitions",
                "anti_patterns": "",
                "decision_rules": {},
                "activated_rules": [],
                "severity": "MEDIUM",
                "must_have_features": [],
                "conversion_focus": "User engagement and task completion"
            }

        # Parse decision rules with closed grammar reasoning contract
        raw_rules = rule.get("Decision_Rules", "{}")
        parsed_rules: dict[str, list[str]] = {}
        try:
            parsed_rules = parse_decision_rules(raw_rules)
        except Exception:
            try:
                parsed_rules = json.loads(raw_rules)
            except Exception:
                parsed_rules = {}

        # Apply deterministic mutations based on query
        evaluation = apply_decision_rules(parsed_rules, query)

        must_have_features: list[Any] = []
        for key, val in parsed_rules.items():
            if key == "must_have" or key.startswith("must_have"):
                must_have_features.extend(val if isinstance(val, list) else [val])

        conversion_focus = self._determine_conversion_focus(category)

        # Style priority may be overridden by activated style rules
        style_priority = [s.strip() for s in rule.get("Style_Priority", "").split("+") if s.strip()]
        if evaluation["style_ids"]:
            style_priority = evaluation["style_ids"] + style_priority

        pattern_name = evaluation["pattern"] or rule.get("Recommended_Pattern", "Clean Architecture")

        return {
            "pattern": pattern_name,
            "style_priority": style_priority,
            "color_mood": rule.get("Color_Mood", ""),
            "typography_mood": rule.get("Typography_Mood", ""),
            "key_effects": rule.get("Key_Effects", ""),
            "anti_patterns": rule.get("Anti_Patterns", ""),
            "decision_rules": parsed_rules,
            "activated_rules": evaluation["activated"],
            "constraints": evaluation["constraints"],
            "architectures": evaluation["architectures"],
            "states": evaluation["states"],
            "severity": rule.get("Severity", "MEDIUM"),
            "must_have_features": must_have_features,
            "conversion_focus": conversion_focus
        }

    def _determine_conversion_focus(self, category: str) -> str:
        category_lower = category.lower()
        conversion_map: dict[str, str] = {
            "e-commerce": "Purchase conversion, Add to cart, Quick checkout",
            "fintech": "Trust building, Security perception, Transaction completion",
            "banking": "Trust building, Security perception, Transaction completion",
            "health": "Appointment booking, Trust signals, Accessibility",
            "fitness": "Engagement, Progress motivation, Habit formation",
            "social": "Engagement, Retention, Content sharing",
            "education": "Progress tracking, Completion rates, Engagement",
            "productivity": "Task completion, Efficiency, Quick actions",
            "food": "Order conversion, Reorder, Quick checkout",
            "travel": "Booking conversion, Search efficiency, Trust",
            "gaming": "Engagement, Retention, In-app purchases",
        }
        for key, focus in conversion_map.items():
            if key in category_lower:
                return focus
        return "User engagement and task completion"

    def _select_best_match(self, results: list[dict[str, Any]], priority_keywords: list[str]) -> dict[str, Any]:
        if not results:
            return {}
        if not priority_keywords:
            return results[0]

        for priority in priority_keywords:
            priority_lower = priority.lower().strip()
            for result in results:
                style_name = result.get("Style Category", "").lower()
                if priority_lower in style_name or style_name in priority_lower:
                    return result

        scored: list[tuple[int, dict[str, Any]]] = []
        for result in results:
            result_str = str(result).lower()
            score = 0
            for kw in priority_keywords:
                kw_lower = kw.lower().strip()
                if kw_lower in result.get("Style Category", "").lower():
                    score += 10
                elif kw_lower in result.get("Keywords", "").lower():
                    score += 3
                elif kw_lower in result_str:
                    score += 1
            scored.append((score, result))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1] if scored and scored[0][0] > 0 else results[0]

    def _select_motion_preset(self, motion_tier: str | None, query: str) -> dict[str, str]:
        """Find the most appropriate motion preset for given tier and context."""
        if not self.motion_data:
            return {}
        tier = motion_tier or "Standard"
        candidates = [m for m in self.motion_data if m.get("Intensity Tier", "").lower() == tier.lower()]
        if not candidates:
            candidates = self.motion_data

        # Keyword match with query
        query_words = set(re.sub(r'[^\w\s]', ' ', query.lower()).split())
        best_match = candidates[0]
        best_overlap = -1

        for c in candidates:
            kw = set(c.get("Keywords", "").lower().replace(",", " ").split())
            overlap = len(query_words.intersection(kw))
            if overlap > best_overlap:
                best_overlap = overlap
                best_match = c

        return best_match

    def _extract_results(self, search_result: dict[str, Any]) -> list[dict[str, Any]]:
        return search_result.get("results", [])

    def generate(
        self,
        query: str,
        project_name: str | None = None,
        variance: int | None = None,
        motion: int | None = None,
        density: int | None = None
    ) -> dict[str, Any]:
        """Generate complete design system recommendation with dial resolution."""
        # Resolve design dials
        resolved_variance = _resolve_dial("variance", variance)
        resolved_motion = _resolve_dial("motion", motion)
        resolved_density = _resolve_dial("density", density)

        # Step 1: Search product category
        product_result = search(query, "product", 1)
        product_results = product_result.get("results", [])
        category = "General"
        product_info = {}
        if product_results:
            product_info = product_results[0]
            category = product_info.get("Product Type", "General")

        # Step 2: Reasoning rules + closed grammar evaluation
        reasoning = self._apply_reasoning(category, query)
        style_priority = list(reasoning.get("style_priority", []))

        # Dial bias: variance alters style priorities
        if resolved_variance:
            style_priority = resolved_variance["style_keywords"] + style_priority

        # Step 3: Multi-domain search
        search_results = self._multi_domain_search(query, style_priority)
        search_results["product"] = product_result

        # Step 4: Domain match selection
        style_results = self._extract_results(search_results.get("style", {}))
        color_results = self._extract_results(search_results.get("color", {}))
        typography_results = self._extract_results(search_results.get("typography", {}))
        pattern_results = self._extract_results(search_results.get("pattern", {}))
        architect_results = self._extract_results(search_results.get("architect", {}))
        landing_results = self._extract_results(search_results.get("landing", {}))

        best_style = self._select_best_match(style_results, style_priority)
        best_color = color_results[0] if color_results else {}
        best_typography = typography_results[0] if typography_results else {}
        best_landing = landing_results[0] if landing_results else {}

        # Step 5: Motion preset selection
        motion_tier = resolved_motion["tier"] if resolved_motion else "Standard"
        selected_motion = self._select_motion_preset(motion_tier, query)

        # Step 6: Spacing scale from density
        active_density = resolved_density or DIAL_TIERS["density"][1][2]  # default to Standard

        # Combine effects
        style_effects = best_style.get("Effects & Animation", "")
        reasoning_effects = reasoning.get("key_effects", "")
        combined_effects = style_effects if style_effects else reasoning_effects

        # Architecture and state resolution
        pattern_name = reasoning.get("pattern", "Clean Architecture")
        state_management = "Riverpod / BLoC"
        if reasoning.get("states"):
            state_management = ", ".join(reasoning["states"]).title()

        return {
            "project_name": project_name or query.upper(),
            "category": category,
            "dials": {
                "variance": resolved_variance,
                "motion": resolved_motion,
                "density": resolved_density,
            },
            "pattern": {
                "name": pattern_name,
                "architecture": architect_results[0].get("layer", "") if architect_results else "Feature-First",
                "state_management": state_management,
                "recommended_patterns": [p.get("pattern_name", "") for p in pattern_results[:3]]
            },
            "screen_pattern": {
                "name": best_landing.get("Pattern Name", "Hero + Features + CTA"),
                "sections": best_landing.get("Section Order", "Hero > Features > CTA"),
                "cta_placement": best_landing.get("Primary CTA Placement", "Bottom + Sticky"),
                "color_strategy": best_landing.get("Color Strategy", ""),
                "conversion_optimization": best_landing.get("Conversion Optimization", "")
            },
            "style": {
                "name": best_style.get("Style Category", "Minimalism"),
                "type": best_style.get("Type", "General"),
                "effects": style_effects,
                "keywords": best_style.get("Keywords", ""),
                "best_for": best_style.get("Best For", ""),
                "do_not_use": best_style.get("Do Not Use For", "")
            },
            "colors": {
                "primary": best_color.get("Primary (Hex)", "#2563EB"),
                "secondary": best_color.get("Secondary (Hex)", "#3B82F6"),
                "cta": best_color.get("CTA (Hex)", "#F97316"),
                "background": "#FFFFFF",
                "surface": "#F8FAFC",
                "text": "#1E293B",
                "notes": best_color.get("Notes", ""),
                "strategy": best_landing.get("Color Strategy", reasoning.get("color_mood", ""))
            },
            "typography": {
                "heading": best_typography.get("Heading Font", "Inter"),
                "body": best_typography.get("Body Font", "Inter"),
                "mood": best_typography.get("Mood/Style Keywords", reasoning.get("typography_mood", "")),
                "best_for": best_typography.get("Best For", ""),
                "google_fonts_url": best_typography.get("Google Fonts URL", "")
            },
            "motion_preset": selected_motion,
            "spacing_scale": active_density["spacing"],
            "visual_density": active_density.get("visual_density", "VisualDensity.standard"),
            "key_effects": combined_effects,
            "anti_patterns": reasoning.get("anti_patterns", ""),
            "decision_rules": reasoning.get("decision_rules", {}),
            "activated_rules": reasoning.get("activated_rules", []),
            "constraints": reasoning.get("constraints", []),
            "severity": reasoning.get("severity", "MEDIUM"),
            "conversion_focus": reasoning.get("conversion_focus", ""),
            "must_have_features": reasoning.get("must_have_features", [])
        }


# ============ DART THEME GENERATOR ============
def generate_dart_theme(design_system: dict[str, Any]) -> str:
    """Generate production-ready Flutter ThemeData & ThemeExtension in Dart."""
    project = design_system.get("project_name", "App")
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    spacing = design_system.get("spacing_scale", {})
    visual_density = design_system.get("visual_density", "VisualDensity.standard")
    motion = design_system.get("motion_preset", {})

    primary_hex = colors.get("primary", "#2563EB")
    secondary_hex = colors.get("secondary", "#3B82F6")
    cta_hex = colors.get("cta", "#F97316")
    bg_hex = colors.get("background", "#FFFFFF")
    surface_hex = colors.get("surface", "#F8FAFC")
    text_hex = colors.get("text", "#1E293B")

    heading_font = typography.get("heading", "Inter")
    body_font = typography.get("body", "Inter")

    dart_code = f"""// 🐦 Flutter Design System - Generated by Flutter Pro Max
// Project: {project}
// Generated At: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
// Architecture: Clean Architecture + ThemeExtension

import 'package:flutter/material.dart';

/// Layer 1: Primitive Tokens (Colors, Spacing, Radius)
class AppColors {{
  AppColors._();

  static const Color primary = {hex_to_flutter_color(primary_hex)};
  static const Color secondary = {hex_to_flutter_color(secondary_hex)};
  static const Color cta = {hex_to_flutter_color(cta_hex)};
  static const Color background = {hex_to_flutter_color(bg_hex)};
  static const Color surface = {hex_to_flutter_color(surface_hex)};
  static const Color text = {hex_to_flutter_color(text_hex)};
  static const Color textMuted = Color(0xFF64748B);
  static const Color border = Color(0xFFE2E8F0);
  static const Color error = Color(0xFFEF4444);
}}

/// Spacing Scale (Density Tier: {(design_system.get('dials', {}).get('density') or {}).get('label', 'Standard')})
class AppSpacing {{
  AppSpacing._();

  static const double xs = {spacing.get('xs', 4.0)};
  static const double sm = {spacing.get('sm', 8.0)};
  static const double md = {spacing.get('md', 16.0)};
  static const double lg = {spacing.get('lg', 24.0)};
  static const double xl = {spacing.get('xl', 32.0)};
  static const double xxl = {spacing.get('xxl', 48.0)};
}}

/// Border Radius Tokens
class AppRadius {{
  AppRadius._();

  static const Radius sm = Radius.circular(8.0);
  static const Radius md = Radius.circular(12.0);
  static const Radius lg = Radius.circular(16.0);
  static const Radius full = Radius.circular(9999.0);

  static final BorderRadius smBorder = BorderRadius.all(sm);
  static final BorderRadius mdBorder = BorderRadius.all(md);
  static final BorderRadius lgBorder = BorderRadius.all(lg);
  static final BorderRadius fullBorder = BorderRadius.all(full);
}}

/// Layer 2 & 3: Custom Tokens via ThemeExtension
class AppCustomTokens extends ThemeExtension<AppCustomTokens> {{
  final Color ctaColor;
  final double cardRadius;
  final double defaultPadding;

  const AppCustomTokens({{
    required this.ctaColor,
    required this.cardRadius,
    required this.defaultPadding,
  }});

  @override
  AppCustomTokens copyWith({{
    Color? ctaColor,
    double? cardRadius,
    double? defaultPadding,
  }}) {{
    return AppCustomTokens(
      ctaColor: ctaColor ?? this.ctaColor,
      cardRadius: cardRadius ?? this.cardRadius,
      defaultPadding: defaultPadding ?? this.defaultPadding,
    );
  }}

  @override
  AppCustomTokens lerp(ThemeExtension<AppCustomTokens>? other, double t) {{
    if (other is! AppCustomTokens) return this;
    return AppCustomTokens(
      ctaColor: Color.lerp(ctaColor, other.ctaColor, t) ?? ctaColor,
      cardRadius: cardRadius + (other.cardRadius - cardRadius) * t,
      defaultPadding: defaultPadding + (other.defaultPadding - defaultPadding) * t,
    );
  }}
}}

/// Flutter ThemeData Generator
class AppTheme {{
  AppTheme._();

  /// Recommended Motion Pattern:
  /// Category: {motion.get('Category', 'Micro-interaction')} ({motion.get('Intensity Tier', 'Standard')})
  /// Easing: {motion.get('Easing', 'Curves.easeOutCubic')} | Duration: {motion.get('Duration', '200ms')}
  /// Snippet: {motion.get('Flutter Snippet', '// See flutter-motion.csv')}

  static ThemeData get lightTheme {{
    final colorScheme = ColorScheme.fromSeed(
      seedColor: AppColors.primary,
      brightness: Brightness.light,
      primary: AppColors.primary,
      secondary: AppColors.secondary,
      surface: AppColors.surface,
      error: AppColors.error,
    );

    return ThemeData(
      useMaterial3: true,
      visualDensity: {visual_density},
      colorScheme: colorScheme,
      scaffoldBackgroundColor: AppColors.background,
      fontFamily: '{body_font}',
      appBarTheme: const AppBarTheme(
        elevation: 0,
        centerTitle: true,
        backgroundColor: AppColors.surface,
        foregroundColor: AppColors.text,
      ),
      cardTheme: CardTheme(
        color: AppColors.surface,
        elevation: 1,
        shape: RoundedRectangleBorder(borderRadius: AppRadius.mdBorder),
        margin: const EdgeInsets.symmetric(
          horizontal: AppSpacing.sm,
          vertical: AppSpacing.xs,
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.primary,
          foregroundColor: Colors.white,
          minimumSize: const Size(88, 48), // WCAG AA Tap Target >= 48dp
          padding: const EdgeInsets.symmetric(
            horizontal: AppSpacing.md,
            vertical: AppSpacing.sm,
          ),
          shape: RoundedRectangleBorder(borderRadius: AppRadius.smBorder),
          elevation: 0,
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: AppColors.surface,
        contentPadding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.md,
          vertical: AppSpacing.sm,
        ),
        border: OutlineInputBorder(
          borderRadius: AppRadius.smBorder,
          borderSide: const BorderSide(color: AppColors.border),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: AppRadius.smBorder,
          borderSide: const BorderSide(color: AppColors.border),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: AppRadius.smBorder,
          borderSide: const BorderSide(color: AppColors.primary, width: 2),
        ),
      ),
      extensions: const [
        AppCustomTokens(
          ctaColor: AppColors.cta,
          cardRadius: 12.0,
          defaultPadding: AppSpacing.md,
        ),
      ],
    );
  }}

  static ThemeData get darkTheme {{
    final colorScheme = ColorScheme.fromSeed(
      seedColor: AppColors.primary,
      brightness: Brightness.dark,
      primary: AppColors.primary,
      secondary: AppColors.secondary,
      surface: const Color(0xFF1E293B),
      error: AppColors.error,
    );

    return ThemeData(
      useMaterial3: true,
      visualDensity: {visual_density},
      colorScheme: colorScheme,
      scaffoldBackgroundColor: const Color(0xFF0F172A),
      fontFamily: '{body_font}',
      appBarTheme: const AppBarTheme(
        elevation: 0,
        centerTitle: true,
        backgroundColor: Color(0xFF1E293B),
        foregroundColor: Colors.white,
      ),
      cardTheme: CardTheme(
        color: const Color(0xFF1E293B),
        elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: AppRadius.mdBorder),
      ),
      extensions: const [
        AppCustomTokens(
          ctaColor: AppColors.cta,
          cardRadius: 12.0,
          defaultPadding: AppSpacing.md,
        ),
      ],
    );
  }}
}}
"""
    return dart_code


# ============ OUTPUT FORMATTERS ============
BOX_WIDTH = 90


def format_ascii_box(design_system: dict[str, Any]) -> str:
    """Format design system as ASCII box for Flutter apps."""
    project = design_system.get("project_name", "PROJECT")
    pattern = design_system.get("pattern", {})
    screen_pattern = design_system.get("screen_pattern", {})
    style = design_system.get("style", {})
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    effects = design_system.get("key_effects", "")
    anti_patterns = design_system.get("anti_patterns", "")
    dials = design_system.get("dials", {})
    motion = design_system.get("motion_preset", {})
    spacing = design_system.get("spacing_scale", {})

    def wrap_text(text: str, prefix: str, width: int) -> list[str]:
        if not text:
            return []
        words = text.split()
        lines: list[str] = []
        current_line = prefix
        for word in words:
            if len(current_line) + len(word) + 1 <= width - 2:
                current_line += (" " if current_line != prefix else "") + word
            else:
                if current_line != prefix:
                    lines.append(current_line)
                current_line = prefix + word
        if current_line != prefix:
            lines.append(current_line)
        return lines

    lines: list[str] = []
    w = BOX_WIDTH - 1

    lines.append("+" + "-" * w + "+")
    lines.append(f"|  TARGET: {project} - FLUTTER DESIGN SYSTEM".ljust(BOX_WIDTH) + "|")
    lines.append("+" + "-" * w + "+")
    lines.append("|" + " " * BOX_WIDTH + "|")

    # DIALS Section
    if any(dials.values()):
        lines.append("|  DESIGN DIALS:".ljust(BOX_WIDTH) + "|")
        if dials.get("variance"):
            lines.append(f"|     Variance: {dials['variance']['value']}/10 ({dials['variance']['label']})".ljust(BOX_WIDTH) + "|")
        if dials.get("motion"):
            lines.append(f"|     Motion:   {dials['motion']['value']}/10 ({dials['motion']['label']})".ljust(BOX_WIDTH) + "|")
        if dials.get("density"):
            lines.append(f"|     Density:  {dials['density']['value']}/10 ({dials['density']['label']})".ljust(BOX_WIDTH) + "|")
        lines.append("|" + " " * BOX_WIDTH + "|")

    # Screen Pattern section
    if screen_pattern.get("name"):
        lines.append(f"|  SCREEN PATTERN: {screen_pattern.get('name', '')}".ljust(BOX_WIDTH) + "|")
        if screen_pattern.get("sections"):
            sections_str = screen_pattern.get("sections", "")[:65]
            lines.append(f"|     Sections: {sections_str}".ljust(BOX_WIDTH) + "|")
        if screen_pattern.get("cta_placement"):
            lines.append(f"|     CTA: {screen_pattern.get('cta_placement', '')}".ljust(BOX_WIDTH) + "|")
        if screen_pattern.get("conversion_optimization"):
            for line in wrap_text(f"Conversion: {screen_pattern.get('conversion_optimization', '')}", "|     ", BOX_WIDTH):
                lines.append(line.ljust(BOX_WIDTH) + "|")
        lines.append("|" + " " * BOX_WIDTH + "|")

    # Architecture Pattern section
    lines.append(f"|  ARCHITECTURE: {pattern.get('name', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Structure: Feature-First / Clean Architecture".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     State: {pattern.get('state_management', 'Riverpod')}".ljust(BOX_WIDTH) + "|")
    if pattern.get('recommended_patterns'):
        patterns_str = ", ".join(filter(None, pattern.get('recommended_patterns', [])))[:60]
        lines.append(f"|     Patterns: {patterns_str}".ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * BOX_WIDTH + "|")

    # Style section
    lines.append(f"|  UI STYLE: {style.get('name', '')}".ljust(BOX_WIDTH) + "|")
    if style.get("keywords"):
        for line in wrap_text(f"Keywords: {style.get('keywords', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * BOX_WIDTH + "|")

    # Colors section
    lines.append("|  COLOR PALETTE:".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Primary:    {colors.get('primary', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Secondary:  {colors.get('secondary', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     CTA:        {colors.get('cta', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Background: {colors.get('background', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Surface:    {colors.get('surface', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Text:       {colors.get('text', '')}".ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * BOX_WIDTH + "|")

    # Typography section
    lines.append(f"|  TYPOGRAPHY: {typography.get('heading', '')} / {typography.get('body', '')}".ljust(BOX_WIDTH) + "|")
    if typography.get("mood"):
        for line in wrap_text(f"Mood: {typography.get('mood', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * BOX_WIDTH + "|")

    # Motion Preset section
    if motion.get("Category"):
        lines.append(f"|  MOTION INTELLIGENCE: {motion.get('Category', '')} ({motion.get('Intensity Tier', '')})".ljust(BOX_WIDTH) + "|")
        lines.append(f"|     Duration: {motion.get('Duration', '')} | Curve: {motion.get('Easing', '')}".ljust(BOX_WIDTH) + "|")
        snippet = motion.get("Flutter Snippet", "")[:60]
        lines.append(f"|     Snippet:  {snippet}...".ljust(BOX_WIDTH) + "|")
        lines.append("|" + " " * BOX_WIDTH + "|")

    # Spacing & Density
    if spacing:
        lines.append(f"|  SPACING SCALE ({design_system.get('visual_density', 'VisualDensity.standard')}):".ljust(BOX_WIDTH) + "|")
        scale_str = f"xs: {spacing.get('xs')} | sm: {spacing.get('sm')} | md: {spacing.get('md')} | lg: {spacing.get('lg')} | xl: {spacing.get('xl')}"
        lines.append(f"|     {scale_str}".ljust(BOX_WIDTH) + "|")
        lines.append("|" + " " * BOX_WIDTH + "|")

    # Anti-patterns section
    if anti_patterns:
        lines.append("|  AVOID (Anti-patterns):".ljust(BOX_WIDTH) + "|")
        anti_list = [a.strip() for a in anti_patterns.split("+")][:3]
        for anti in anti_list:
            if anti:
                for line in wrap_text(f"• {anti}", "|     ", BOX_WIDTH):
                    lines.append(line.ljust(BOX_WIDTH) + "|")
        lines.append("|" + " " * BOX_WIDTH + "|")

    # Pre-delivery checklist
    lines.append("|  PRE-DELIVERY CHECKLIST:".ljust(BOX_WIDTH) + "|")
    lines.append("|     [ ] const constructors used everywhere possible".ljust(BOX_WIDTH) + "|")
    lines.append("|     [ ] Touch target >= 48x48 dp on mobile".ljust(BOX_WIDTH) + "|")
    lines.append("|     [ ] Semantics widgets added for screen readers".ljust(BOX_WIDTH) + "|")
    lines.append("|     [ ] MediaQuery.disableAnimationsOf respected".ljust(BOX_WIDTH) + "|")
    lines.append("|     [ ] No God Widgets (files < 300 lines)".ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * BOX_WIDTH + "|")
    lines.append("+" + "-" * w + "+")

    return "\n".join(lines)


def format_markdown(design_system: dict[str, Any]) -> str:
    """Format design system as Markdown."""
    project = design_system.get("project_name", "PROJECT")
    pattern = design_system.get("pattern", {})
    screen_pattern = design_system.get("screen_pattern", {})
    style = design_system.get("style", {})
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    effects = design_system.get("key_effects", "")
    anti_patterns = design_system.get("anti_patterns", "")
    dials = design_system.get("dials", {})
    motion = design_system.get("motion_preset", {})
    spacing = design_system.get("spacing_scale", {})

    lines: list[str] = []
    lines.append(f"# Design System: {project}")
    lines.append("")
    lines.append(f"> **Category:** {design_system.get('category', 'General')}")
    lines.append(f"> **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # Dials
    if any(dials.values()):
        lines.append("## Design Dials")
        lines.append("")
        if dials.get("variance"):
            lines.append(f"- **Variance:** `{dials['variance']['value']}/10` — {dials['variance']['label']}")
        if dials.get("motion"):
            lines.append(f"- **Motion Intensity:** `{dials['motion']['value']}/10` — {dials['motion']['label']}")
        if dials.get("density"):
            lines.append(f"- **Visual Density:** `{dials['density']['value']}/10` — {dials['density']['label']} (`{design_system.get('visual_density')}`)")
        lines.append("")

    # Pattern
    lines.append("## Architecture & Patterns")
    lines.append("")
    lines.append(f"- **Pattern:** {pattern.get('name', 'Clean Architecture')}")
    lines.append(f"- **State Management:** {pattern.get('state_management', 'Riverpod')}")
    if screen_pattern.get("name"):
        lines.append(f"- **Screen Structure:** {screen_pattern.get('name')}")
        lines.append(f"- **Section Flow:** {screen_pattern.get('sections')}")
    lines.append("")

    # Colors
    lines.append("## Color Palette")
    lines.append("")
    lines.append(f"| Token | Hex | Flutter Code |")
    lines.append(f"|---|---|---|")
    lines.append(f"| Primary | `{colors.get('primary')}` | `{hex_to_flutter_color(colors.get('primary'))}` |")
    lines.append(f"| Secondary | `{colors.get('secondary')}` | `{hex_to_flutter_color(colors.get('secondary'))}` |")
    lines.append(f"| CTA / Accent | `{colors.get('cta')}` | `{hex_to_flutter_color(colors.get('cta'))}` |")
    lines.append(f"| Background | `{colors.get('background')}` | `{hex_to_flutter_color(colors.get('background'))}` |")
    lines.append(f"| Surface | `{colors.get('surface')}` | `{hex_to_flutter_color(colors.get('surface'))}` |")
    lines.append(f"| Text | `{colors.get('text')}` | `{hex_to_flutter_color(colors.get('text'))}` |")
    lines.append("")

    # Typography
    lines.append("## Typography")
    lines.append("")
    lines.append(f"- **Heading Font:** {typography.get('heading', 'Inter')}")
    lines.append(f"- **Body Font:** {typography.get('body', 'Inter')}")
    lines.append("")

    # Spacing
    if spacing:
        lines.append("## Spacing Tokens")
        lines.append("")
        lines.append("| Token | Value (dp) | Usage |")
        lines.append("|---|---|---|")
        for k, v in spacing.items():
            lines.append(f"| `AppSpacing.{k}` | `{v}` | Responsive padding/gap |")
        lines.append("")

    # Motion Intelligence
    if motion.get("Category"):
        lines.append("## Motion & Micro-interactions")
        lines.append("")
        lines.append(f"**Pattern:** {motion.get('Category')} ({motion.get('Intensity Tier')})")
        lines.append(f"- **Trigger:** {motion.get('Trigger')}")
        lines.append(f"- **Duration & Curve:** {motion.get('Duration')} with `{motion.get('Easing')}`")
        lines.append("")
        lines.append("```dart")
        lines.append(f"// {motion.get('Framework Notes', '')}")
        lines.append(f"{motion.get('Flutter Snippet', '')}")
        lines.append("```")
        lines.append("")

    # Pre-delivery checklist
    lines.append("## Pre-Delivery Checklist")
    lines.append("")
    lines.append("- [ ] `const` constructors used for static subtrees")
    lines.append(r"- [ ] Touch targets $\ge 48\times 48\text{ dp}$")
    lines.append("- [ ] `Semantics` label provided on icon-only buttons")
    lines.append("- [ ] `MediaQuery.disableAnimationsOf(context)` respected")
    lines.append("- [ ] Files under 300 lines (no God Objects)")
    lines.append("")

    return "\n".join(lines)


# ============ PERSISTENCE SYSTEM ============
def safe_slug(text: str) -> str:
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', text).lower()
    return re.sub(r'[\s-]+', '-', slug).strip('-')


def _write_persisted_file(filepath: Path, content: str) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def persist_design_system(
    design_system: dict[str, Any],
    page: str | None = None,
    output_dir: str | None = None,
    query: str = "",
    export_dart: bool = False
) -> None:
    project_slug = safe_slug(design_system.get("project_name", "default"))
    base_dir = Path(output_dir) if output_dir else Path.cwd()
    target_dir = base_dir / "design-system" / project_slug

    master_content = format_markdown(design_system)
    _write_persisted_file(target_dir / "MASTER.md", master_content)

    # Save Dart theme if requested
    if export_dart:
        dart_code = generate_dart_theme(design_system)
        _write_persisted_file(target_dir / "app_theme.dart", dart_code)

    if page:
        page_slug = safe_slug(page)
        overrides_content = format_page_override_md(design_system, page, query)
        _write_persisted_file(target_dir / "pages" / f"{page_slug}.md", overrides_content)


def format_page_override_md(design_system: dict[str, Any], page_name: str, page_query: str | None = None) -> str:
    project = design_system.get("project_name", "PROJECT")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    page_title = page_name.replace("-", " ").replace("_", " ").title()
    page_overrides = _generate_intelligent_overrides(page_name, page_query, design_system)

    lines: list[str] = []
    lines.append(f"# {page_title} Screen Overrides")
    lines.append("")
    lines.append(f"> **PROJECT:** {project} | **Generated:** {timestamp}")
    lines.append(f"> **Screen Type:** {page_overrides.get('page_type', 'General')}")
    lines.append("")
    lines.append("> ⚠️ **IMPORTANT:** Rules in this file override `MASTER.md`.")
    lines.append("")
    lines.append("## Screen Layout & Recommendations")
    lines.append("")
    for rec in page_overrides.get("recommendations", []):
        lines.append(f"- {rec}")
    lines.append("")
    return "\n".join(lines)


def _generate_intelligent_overrides(page_name: str, page_query: str | None, design_system: dict[str, Any]) -> dict[str, Any]:
    page_lower = page_name.lower()
    page_type = _detect_page_type(f"{page_lower} {page_query or ''}")
    recommendations: list[str] = [
        f"Screen pattern optimized for {page_type}",
        "Ensure tap targets >= 48x48 dp for primary actions",
        "Use LayoutBuilder for responsive orientation switches"
    ]
    return {"page_type": page_type, "recommendations": recommendations}


def _detect_page_type(context: str) -> str:
    context_lower = context.lower()
    page_patterns: list[tuple[list[str], str]] = [
        (["dashboard", "analytics", "metrics", "stats"], "Dashboard"),
        (["list", "search", "browse", "filter"], "List / Search"),
        (["detail", "product", "item"], "Detail View"),
        (["form", "edit", "create", "input"], "Form / Input"),
        (["profile", "settings", "account"], "Settings / Profile"),
        (["login", "auth", "signin", "register"], "Authentication"),
        (["home", "landing", "welcome"], "Home / Landing"),
        (["checkout", "payment", "cart"], "Checkout / Payment"),
    ]
    for keywords, page_type in page_patterns:
        if any(kw in context_lower for kw in keywords):
            return page_type
    return "General"


# ============ MAIN ENTRY POINT ============
def generate_design_system(
    query: str,
    project_name: str | None = None,
    output_format: str = "ascii",
    persist: bool = False,
    page: str | None = None,
    output_dir: str | None = None,
    variance: int | None = None,
    motion: int | None = None,
    density: int | None = None,
    export_dart: bool = False
) -> str:
    """Main entry point for design system generation."""
    generator = DesignSystemGenerator()
    design_system = generator.generate(
        query,
        project_name=project_name,
        variance=variance,
        motion=motion,
        density=density
    )

    if persist:
        persist_design_system(
            design_system,
            page=page,
            output_dir=output_dir,
            query=query,
            export_dart=export_dart
        )

    if export_dart:
        return generate_dart_theme(design_system)

    if output_format == "markdown":
        return format_markdown(design_system)
    return format_ascii_box(design_system)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Flutter Design System with Dials and Dart Theme Export")
    parser.add_argument("query", help="Search query (e.g., 'fintech banking app')")
    parser.add_argument("--project-name", "-p", type=str, default=None, help="Project name")
    parser.add_argument("--format", "-f", choices=["ascii", "markdown"], default="ascii", help="Output format")
    parser.add_argument("--variance", type=int, choices=range(1, 11), default=None, help="Variance dial (1-10)")
    parser.add_argument("--motion", type=int, choices=range(1, 11), default=None, help="Motion intensity dial (1-10)")
    parser.add_argument("--density", type=int, choices=range(1, 11), default=None, help="Visual density dial (1-10)")
    parser.add_argument("--export-dart", action="store_true", help="Generate production Dart ThemeData & ThemeExtension code")
    parser.add_argument("--persist", action="store_true", help="Save to design-system/ folder")
    parser.add_argument("--page", type=str, default=None, help="Create page-specific override file")
    parser.add_argument("--output-dir", "-o", type=str, default=None, help="Output directory")

    args = parser.parse_args()

    result = generate_design_system(
        args.query,
        project_name=args.project_name,
        output_format=args.format,
        persist=args.persist,
        page=args.page,
        output_dir=args.output_dir,
        variance=args.variance,
        motion=args.motion,
        density=args.density,
        export_dart=args.export_dart
    )
    print(result)
