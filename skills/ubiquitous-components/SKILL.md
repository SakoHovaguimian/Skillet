---
name: ubiquitous-components
description: Generate or refresh a source-backed Rune and app UI catalog. Use when asked to create or update the catalog, with shared publication when authorized. Do not use for ordinary UI implementation or to import an existing catalog.
disable-model-invocation: true
---

# Ubiquitous Components

## Outcome

A complete, context-efficient UI inventory at `docs/UBIQUITOUS_COMPONENTS.md`, grounded in source code, not memory, plus a Rune-only global catalog published to shared storage when authorized so other projects can consume it through `$ubiquitous-components-fetch`.

## Inputs and preconditions

A workspace containing Rune source (local checkout, resolved package, or DerivedData checkout) and optionally app-layer UI code. Capture the requested scope from the conversation: full coverage or a scoped subset (for example only Rune, only app views, or only modifiers/services).

## Workflow

1. When the destination exists, inspect it for maintained explanations and custom entries. Plan generation at a separate local candidate path with `--no-global-sync`; merge source-backed changes into the destination only after verifying the candidate. Preserve still-valid maintained content and label unresolved discrepancies. Use direct generation only when no maintained destination exists.

2. Discover source roots, in this priority order:
   - Explicit flags (`--rune-root`, `--app-root`)
   - Local checkouts (`Rune/Sources/Rune`, `.build/checkouts/Rune/Sources/Rune`, `SourcePackages/checkouts/Rune/Sources/Rune`)
   - Xcode DerivedData (`~/Library/Developer/Xcode/DerivedData/*/SourcePackages/checkouts/Rune/Sources/Rune`)
   - `Package.resolved` pins for evidence and revision reporting

3. Run the generator script, using a separate candidate path for an existing destination (resolve `<skill-dir>` from the location of this `SKILL.md`):

   ```bash
   python3 <skill-dir>/scripts/generate_ubiquitous_components.py --workspace <repo-root> --output <candidate-path> --no-global-sync
   ```

   Common variants:

   ```bash
   python3 <skill-dir>/scripts/generate_ubiquitous_components.py --workspace <repo-root> --rune-root <path-to-Rune-or-Sources/Rune> --output <candidate-path> --no-global-sync
   python3 <skill-dir>/scripts/generate_ubiquitous_components.py --workspace <repo-root> --app-root <path-to-app-root> --output <candidate-path> --no-global-sync
   python3 <skill-dir>/scripts/generate_ubiquitous_components.py --workspace <repo-root> --include-private --output <candidate-path> --no-global-sync
   python3 <skill-dir>/scripts/generate_ubiquitous_components.py --workspace <repo-root> --output <local-candidate-path> --global-rune-output <shared-candidate-directory>/UBIQUITOUS_COMPONENTS.md
   ```

   Default behavior excludes `private`/`fileprivate` declarations so the catalog stays focused on offered API. Use `--include-private` for implementation-level audits.

   The helper overwrites its output paths and, without `--no-global-sync`, also writes a Rune-only catalog. Keep `--no-global-sync` for local-only work. For authorized shared publication, use the last variant with a separate local candidate directory, inspect the Rune-only catalog and metadata, update output-path labels to their final destinations, then publish them to the authorized shared destination. Resolve the shared home as `$SKILLET_SHARED_HOME`, else `$CODEX_HOME`, else `~/.codex`:
   - `<shared-home>/shared/ubiquitous-components/rune/UBIQUITOUS_COMPONENTS.md`
   - metadata file: `.../UBIQUITOUS_COMPONENTS.metadata.json`

4. Enforce completeness. Confirm that each discovered category root contributes output:
   - `Components`
   - `ViewModifiers`
   - `Services`
   - `Views` and/or `Screens`
   - `Extensions`

5. Verify extraction quality. Confirm each declaration row includes:
   - Access level
   - File + line
   - API count
   - Parameter count
   - Summarized entry points (`init`/`func` display names)

6. Merge the verified candidate into the destination, preserving still-valid maintained explanations and custom entries and recording the final output path. Patch weak summaries only when needed. If generated `What` descriptions are too generic for key APIs, edit those rows directly in `docs/UBIQUITOUS_COMPONENTS.md` using code evidence from the same files.

## Constraints

- Deliver the final catalog at `docs/UBIQUITOUS_COMPONENTS.md` unless the user asks for a different path. Candidate paths are temporary outputs, not the final artifact.
- Publish the Rune-only shared catalog when the user requested shared publication or an established project instruction authorizes it. A request limited to a local catalog uses `--no-global-sync`. Preserve existing shared content until the replacement has been inspected.
- Keep sections categorical and exhaustive for discovered roots.
- Keep rows compact and deterministic (one declaration per row).
- Keep `Entry Points` concise (top APIs with overflow marker).
- Keep claims implementation-grounded (file path + signature evidence).
- Keep Rune revision traceable through `Package.resolved` when available.

## Composition

<interface>
| Invokes | When | Carries in | Expects back | If unavailable |
| --- | --- | --- | --- | --- |
| `$ubiquitous-components-fetch` | Never invoked by this producer; documented as the consumer of its output | The published shared-catalog location and freshness metadata | A project-local copy of the shared catalog | Consumers use the local `docs/UBIQUITOUS_COMPONENTS.md` directly |
</interface>

Both skills resolve the shared home with the same chain (`$SKILLET_SHARED_HOME`, else `$CODEX_HOME`, else `~/.codex`); changing the chain on one side without the other breaks the exchange.

## Failure handling

- Rune source is not found: fail fast by default. Ask for `--rune-root` or for the user to resolve package dependencies in Xcode. Run with `--allow-missing-rune` only when the user explicitly accepts partial output.
- Shared publication is not requested: complete the local catalog and report that no shared update was made.
- Authorized shared publication fails: preserve the verified local result, report the failure and affected shared paths, and do not claim the shared catalog is current.

## Output contract

Return a concise summary reporting:

- source roots used
- declaration/API/parameter counts
- any missing Rune root or partial-coverage caveat
- context-size caveat when output is still large
- local output path and shared publication status, including the global Rune output path when published

For the expected markdown layout of the generated catalog, use `references/output-structure.md`.
