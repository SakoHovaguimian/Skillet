---
name: ubiquitous-components
description: Build or refresh a compact UI API catalog for Rune and app-layer UI code by scanning Components, ViewModifiers, Services, Views/Screens, and Extensions, then writing `docs/UBIQUITOUS_COMPONENTS.md` and publishing a Rune-only shared catalog. Use when an authoritative, context-efficient inventory is needed for reusable UI building blocks, design-system audits, or UI implementation planning. Do not use to import an existing catalog into a project; use `$ubiquitous-components-fetch` for that.
disable-model-invocation: true
---

# Ubiquitous Components

## Outcome

A complete, context-efficient UI inventory at `docs/UBIQUITOUS_COMPONENTS.md`, grounded in source code, not memory, plus a Rune-only global catalog published to shared storage so other projects can consume it through `$ubiquitous-components-fetch`.

## Inputs and preconditions

A workspace containing Rune source (local checkout, resolved package, or DerivedData checkout) and optionally app-layer UI code. Capture the requested scope from the conversation: full coverage or a scoped subset (for example only Rune, only app views, or only modifiers/services).

## Workflow

1. Read existing `docs/UBIQUITOUS_COMPONENTS.md` when present. Merge forward: preserve still-valid entries and regenerate stale sections from code.

2. Discover source roots, in this priority order:
   - Explicit flags (`--rune-root`, `--app-root`)
   - Local checkouts (`Rune/Sources/Rune`, `.build/checkouts/Rune/Sources/Rune`, `SourcePackages/checkouts/Rune/Sources/Rune`)
   - Xcode DerivedData (`~/Library/Developer/Xcode/DerivedData/*/SourcePackages/checkouts/Rune/Sources/Rune`)
   - `Package.resolved` pins for evidence and revision reporting

3. Run the generator script (resolve `<skill-dir>` from the location of this `SKILL.md`):

   ```bash
   python3 <skill-dir>/scripts/generate_ubiquitous_components.py --workspace <repo-root>
   ```

   Common variants:

   ```bash
   python3 <skill-dir>/scripts/generate_ubiquitous_components.py --workspace <repo-root> --output docs/UBIQUITOUS_COMPONENTS.md
   python3 <skill-dir>/scripts/generate_ubiquitous_components.py --workspace <repo-root> --rune-root <path-to-Rune-or-Sources/Rune>
   python3 <skill-dir>/scripts/generate_ubiquitous_components.py --workspace <repo-root> --app-root <path-to-app-root>
   python3 <skill-dir>/scripts/generate_ubiquitous_components.py --workspace <repo-root> --include-private
   python3 <skill-dir>/scripts/generate_ubiquitous_components.py --workspace <repo-root> --no-global-sync
   python3 <skill-dir>/scripts/generate_ubiquitous_components.py --workspace <repo-root> --global-rune-output <absolute-global-path>
   ```

   Default behavior excludes `private`/`fileprivate` declarations so the catalog stays focused on offered API. Use `--include-private` for implementation-level audits.

   Default behavior also syncs a Rune-only copy to the shared home, resolved as `$SKILLET_SHARED_HOME`, else `$CODEX_HOME`, else `~/.codex`:
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

6. Patch weak summaries only when needed. If generated `What` descriptions are too generic for key APIs, edit those rows directly in `docs/UBIQUITOUS_COMPONENTS.md` using code evidence from the same files.

## Constraints

- Write the file strictly as `docs/UBIQUITOUS_COMPONENTS.md` unless the user asks for a different path.
- Also write/sync the Rune-only global artifact unless the user explicitly disables it.
- Keep sections categorical and exhaustive for discovered roots.
- Keep rows compact and deterministic (one declaration per row).
- Keep `Entry Points` concise (top APIs with overflow marker).
- Keep claims implementation-grounded (file path + signature evidence).
- Keep Rune revision traceable through `Package.resolved` when available.

## Composition

<interface>
| Invokes | When | Carries in | Expects back | If unavailable |
| --- | --- | --- | --- | --- |
| `$ubiquitous-components-fetch` (consumer side) | Never invoked by this skill; consumers run it to import the global catalog this skill publishes | — | — | Consumers use the local `docs/UBIQUITOUS_COMPONENTS.md` directly |
</interface>

Both skills resolve the shared home with the same chain (`$SKILLET_SHARED_HOME`, else `$CODEX_HOME`, else `~/.codex`); changing the chain on one side without the other breaks the exchange.

## Failure handling

- Rune source is not found: fail fast by default. Ask for `--rune-root` or for the user to resolve package dependencies in Xcode. Run with `--allow-missing-rune` only when the user explicitly accepts partial output.
- Global sync is disabled or fails: still write the local catalog, and report that consumers of `$ubiquitous-components-fetch` will see a stale or missing global copy.

## Output contract

Return a concise summary reporting:

- source roots used
- declaration/API/parameter counts
- any missing Rune root or partial-coverage caveat
- context-size caveat when output is still large
- local output path and global Rune output path

For the expected markdown layout of the generated catalog, use `references/output-structure.md`.
