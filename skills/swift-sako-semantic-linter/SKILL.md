---
name: swift-sako-semantic-linter
description: Review and repair touched Swift and SwiftUI code against Sako, Rune, Grimoire, and local project semantics. Use when Swift edits need a follow-up pass or a focused audit of member access, formatting, screen structure, navigation-created ViewModels, lifecycle and analytics, concurrency safety, Rune UI, routes, DI, API, mocks, previews, permissions, or integration parity. Do not use for Swift 6 isolation diagnostics; those route to `$swift-6-concurrency`.
disable-model-invocation: true
---

# Swift Sako Semantic Linter

## Outcome

The requested Swift diff is left locally consistent and semantically safe with the smallest coherent change. This skill is the source of truth for Sako, Rune, and Grimoire code rules; implementation skills reference it rather than restating its contract.

## Inputs and preconditions

1. Determine whether the user requested edits or review only.
2. Identify touched Swift files from the explicit scope or focused diff. Do not absorb unrelated dirty files.
3. Read applicable `AGENTS.md`, formatter/linter configuration, and 2–3 recent nearby exemplars.

## Workflow

### 1. Load the rule contract

Read [references/core-swift.md](references/core-swift.md) for every run. Then read each applicable module completely:

- [references/screen-viewmodel.md](references/screen-viewmodel.md): screens, sheets, child views, ViewModels, lifecycle, navigation setup, or analytics.
- [references/async-safety.md](references/async-safety.md): `async`, `await`, `Task`, subscriptions, loading, presentation cleanup, or active-session cleanup.
- [references/rune-ui.md](references/rune-ui.md): SwiftUI/Rune composition, style, colors, images, layout, motion, sheets, overlays, or custom components.
- [references/integration-parity.md](references/integration-parity.md): new or changed routes, ViewModels, DI, services, APIs, mocks, fixtures, previews, or permissions.

Load the union for mixed changes. If applicability is uncertain, load the module; context savings never justify skipping a relevant rule.

### 2. Run the pass

1. Inspect the focused diff and enough surrounding code to understand ownership.
2. Run the scanner on touched files using compact output (resolve `<skill-dir>` from the location of this `SKILL.md`):

   ```bash
   python3 <skill-dir>/scripts/scan_swift_style.py --diff-base HEAD --summary <file-or-directory> [...]
   ```

   Omit `--diff-base` only for an intentional full-file audit. Omit `--summary` or use JSON only when exact individual findings are needed.

3. Classify findings:
   - `Mechanical`: safe syntax, spacing, wrapping, access, or token cleanup; fix in scope.
   - `Semantic`: naming, decomposition, ownership, lifecycle, theme, media, or identity; fix only with strong evidence and a focused diff.
   - `Behavioral`: output, state, timing, isolation, navigation, or public API; request authority unless already requested.
   - `Existing`: outside touched lines; leave unchanged unless it blocks the task.
4. Apply the smallest coherent patch.
5. Re-run the same scan and inspect the final diff for churn or behavior drift.
6. Use a configured formatter/static linter only when safe for focused files.

## Constraints

- Resolve conflicts in this order: explicit user/repository instructions; compiler or public contracts; current nearby feature conventions; current Rune/Grimoire conventions; this skill.
- Current local evidence beats legacy formatting. A heuristic never outranks source context.
- Do not run Xcode builds or tests unless explicitly authorized.

## Composition

<interface>
| Invokes | When | Carries in | Expects back | If unavailable |
| --- | --- | --- | --- | --- |
| `$swift-6-concurrency` | A finding involves Swift concurrency isolation, `Sendable`, or actor diagnostics | The diagnostic, the touched code, and known project settings | An isolation-correct fix or recommendation | Classify the finding `Behavioral`, flag it for manual review, and do not invent an isolation fix |
</interface>

## Failure handling

- The scanner script fails or is missing: perform the review manually against the loaded rule modules and state that findings were not machine-indexed.
- A formatter or static linter would touch unrelated code: skip it and report why.
- Evidence conflicts with a rule module: local evidence wins; record the conflict in the report.

## Output contract

Return files reviewed/changed, fixes applied, unresolved or out-of-scope findings, verification results, assumptions, conflicts, and limits. If no change is warranted, say so and cite the local evidence.
