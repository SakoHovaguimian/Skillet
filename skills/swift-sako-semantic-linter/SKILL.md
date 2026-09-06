---
name: swift-sako-semantic-linter
description: Review scoped Swift changes against local Sako, Rune, and Grimoire conventions. Use when explicitly asked for a semantic review or when an authorized implementation workflow requests preflight or verification. Do not apply fixes during review-only or preflight use; route isolation diagnostics to the concurrency skill.
disable-model-invocation: true
---

# Swift Sako Semantic Linter

## Outcome

The requested Swift scope receives a rule preflight, an evidence-backed review, or the smallest coherent authorized repair, according to the requested mode. This skill is the source of truth for Sako, Rune, and Grimoire code rules; implementation skills reference it rather than restating its contract.

## Inputs and preconditions

1. Determine the requested mode: preflight, review-only, or edit. Preflight loads the applicable rule modules and returns constraints for the planned surfaces; it does not scan or edit files. Review-only inspects and reports findings without applying fixes. Edit mode may repair findings only within the user's authorized scope.
2. For preflight, identify the planned surfaces. For review-only or edit mode, identify touched Swift files from the explicit scope or focused diff. Do not absorb unrelated dirty files.
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

Preflight ends after returning the applicable rule contract. The following steps apply only to review-only and edit modes.

1. Inspect the focused diff and enough surrounding code to understand ownership.
2. Run the scanner on touched files using compact output (resolve `<skill-dir>` from the location of this `SKILL.md`):

   ```bash
   python3 <skill-dir>/scripts/scan_swift_style.py --diff-base HEAD --summary <file-or-directory> [...]
   ```

   Omit `--diff-base` only for an intentional full-file audit. Omit `--summary` or use JSON only when exact individual findings are needed.

3. Classify findings:
   - `Mechanical`: safe syntax, spacing, wrapping, access, or token cleanup; repair only in edit mode and in scope.
   - `Semantic`: naming, decomposition, ownership, lifecycle, theme, media, or identity; repair only in edit mode with strong evidence and a focused diff.
   - `Behavioral`: output, state, timing, isolation, navigation, or public API; request authority unless already requested.
   - `Existing`: outside touched lines; leave unchanged unless it blocks the task.
4. In edit mode, apply the smallest coherent authorized patch. In review-only mode, report the proposed patch without changing files.
5. After edits, rerun the affected scan and inspect the final diff. Without edits, do not repeat an unchanged scan unless new evidence requires it.
6. Use a configured formatter/static linter only when safe for focused files; formatting writes require edit mode.

## Constraints

- Resolve conflicts in this order: explicit user/repository instructions; compiler or public contracts; current nearby feature conventions; current Rune/Grimoire conventions; this skill.
- Current local evidence beats legacy formatting. A heuristic never outranks source context.
- Do not run Xcode builds or tests unless explicitly authorized.

## Composition

<interface>
| Invokes | When | Carries in | Expects back | If unavailable |
| --- | --- | --- | --- | --- |
| `$swift-6-concurrency` | A finding involves Swift concurrency isolation, `Sendable`, or actor diagnostics | The requested mode, authorized scope, verification restrictions, diagnostic, touched code, and known project settings | An isolation-correct fix or recommendation | Classify the finding `Behavioral`, flag it for manual review, and do not invent an isolation fix |
</interface>

## Failure handling

- If the requested diff base cannot be resolved, report that diff-scoped verification did not run. Do not silently substitute a full-file audit. Full-file scanning remains appropriate for a confirmed new file or an explicitly requested full-file audit.
- The scanner script fails or is missing: perform the review manually against the loaded rule modules and state that findings were not machine-indexed.
- A formatter or static linter would touch unrelated code: skip it and report why.
- Evidence conflicts with a rule module: local evidence wins; record the conflict in the report.

## Output contract

For preflight, return the applicable rule modules and constraints without a scan or compliance claim. Otherwise return files reviewed/changed, fixes applied, unresolved or out-of-scope findings, verification results, assumptions, conflicts, and limits. If no change is warranted, say so and cite the local evidence.
