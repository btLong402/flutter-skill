---
description: Run comprehensive Flutter UI/UX, accessibility, and layout review on a screen or widget file
---

Run a complete 6-phase Flutter design review on `$ARGUMENTS`.

Invoke the `flutter-design-review` agent to inspect the specified file or screen:
1. Scan for `RenderFlex overflow` hazards and missing `Expanded` / `SafeArea`
2. Validate touch targets (minimum 48x48 dp)
3. Check accessibility, `Semantics`, and font scaling resilience
4. Verify token usage and `ThemeData` compliance (no hardcoded colors)
5. Review animation curves, disposal, and `MediaQuery.disableAnimationsOf`
6. Audit widget rebuild scope and `const` usage

Return a ranked report with actionable code solutions.
