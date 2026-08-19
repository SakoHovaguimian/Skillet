---
name: swift-sako-semantic-linter
description: Review and repair touched Swift and SwiftUI code against Sako, Rune, Grimoire, and local project semantics. Use after Swift edits or for focused audits of member access, formatting, screen structure, navigation-created ViewModels, lifecycle and analytics, concurrency safety, Rune UI, routes, DI, API, mocks, previews, permissions, and integration parity. Load only the rule modules applicable to the touched surfaces and run repository-aware static checks without builds or tests unless separately authorized.
disable-model-invocation: true
---

# Swift Sako Semantic Linter

## Outcome

Leave the requested Swift diff locally consistent and semantically safe with the smallest coherent change. This skill is the source of truth for Sako, Rune, and Grimoire code rules; implementation skills should reference it rather than restate its contract.

## Establish Scope and Authority

1. Determine whether the user requested edits or review only.
2. Identify touched Swift files from the explicit scope or focused diff. Do not absorb unrelated dirty files.
3. Read applicable `AGENTS.md`, formatter/linter configuration, and 2–3 recent nearby exemplars.
4. Resolve conflicts in this order: explicit user/repository instructions; compiler or public contracts; current nearby feature conventions; current Rune/Grimoire conventions; this skill.

Current local evidence beats legacy formatting. A heuristic never outranks source context.

## Load the Rule Contract

Read [references/core-swift.md](references/core-swift.md) for every run. Then read each applicable module completely:

- [references/screen-viewmodel.md](references/screen-viewmodel.md): screens, sheets, child views, ViewModels, lifecycle, navigation setup, or analytics.
- [references/async-safety.md](references/async-safety.md): `async`, `await`, `Task`, subscriptions, loading, presentation cleanup, or active-session cleanup.
- [references/rune-ui.md](references/rune-ui.md): SwiftUI/Rune composition, style, colors, images, layout, motion, sheets, overlays, or custom components.
- [references/integration-parity.md](references/integration-parity.md): new or changed routes, ViewModels, DI, services, APIs, mocks, fixtures, previews, or permissions.

Load the union for mixed changes. If applicability is uncertain, load the module; context savings never justify skipping a relevant rule.

## Run the Pass

1. Inspect the focused diff and enough surrounding code to understand ownership.
2. Run the scanner on touched files using compact output:

   ```bash
   python3 <skill-dir>/scripts/scan_swift_style.py --diff-base HEAD --summary <file-or-directory> [...]
   ```

   Resolve `<skill-dir>` from this file. Omit `--diff-base` only for an intentional full-file audit. Omit `--summary` or use JSON only when exact individual findings are needed.

3. Classify findings:
   - `Mechanical`: safe syntax, spacing, wrapping, access, or token cleanup; fix in scope.
   - `Semantic`: naming, decomposition, ownership, lifecycle, theme, media, or identity; fix only with strong evidence and a focused diff.
   - `Behavioral`: output, state, timing, isolation, navigation, or public API; request authority unless already requested.
   - `Existing`: outside touched lines; leave unchanged unless it blocks the task.
4. Apply the smallest coherent patch.
5. Re-run the same scan and inspect the final diff for churn or behavior drift.
6. Use a configured formatter/static linter only when safe for focused files.

Do not run Xcode builds or tests unless explicitly authorized. For Swift concurrency diagnostics, invoke `$swift-6-concurrency` rather than inventing isolation fixes.

## Report

Return files reviewed/changed, fixes applied, unresolved or out-of-scope findings, verification results, assumptions, conflicts, and limits. If no change is warranted, say so and cite the local evidence.
