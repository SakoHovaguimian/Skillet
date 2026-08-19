---
name: ubiquitous-components
description: Build or refresh a compact UI API catalog for Rune and app-layer UI code by scanning Components, ViewModifiers, Services, Views/Screens, and Extensions, then writing `docs/UBIQUITOUS_COMPONENTS.md`. Use when Codex needs an authoritative but context-efficient inventory for reusable UI building blocks, design-system audits, or UI implementation planning.
disable-model-invocation: true
---

# Ubiquitous Components

Generate and maintain a complete, context-efficient UI inventory grounded in source code, not memory.

This skill also publishes a Rune-only global catalog so other projects can consume a shared artifact.
For consumers, use `$ubiquitous-components-fetch` to import the global file into any workspace.

## Workflow

1. Scan the conversation for requested scope.
Capture whether the user wants full coverage or a scoped subset (for example only Rune, only app views, or only modifiers/services).

2. Read existing `docs/UBIQUITOUS_COMPONENTS.md` when present.
Merge forward. Preserve still-valid entries and regenerate stale sections from code.

3. Discover source roots.
Prioritize this order:
- Explicit flags (`--rune-root`, `--app-root`)
- Local checkouts (`Rune/Sources/Rune`, `.build/checkouts/Rune/Sources/Rune`, `SourcePackages/checkouts/Rune/Sources/Rune`)
- Xcode DerivedData (`~/Library/Developer/Xcode/DerivedData/*/SourcePackages/checkouts/Rune/Sources/Rune`)
- `Package.resolved` pins for evidence and revision reporting

4. Run the generator script.
Use:

```bash
python3 scripts/generate_ubiquitous_components.py --workspace <repo-root>
```

Common variants:

```bash
python3 scripts/generate_ubiquitous_components.py --workspace <repo-root> --output docs/UBIQUITOUS_COMPONENTS.md
python3 scripts/generate_ubiquitous_components.py --workspace <repo-root> --rune-root <path-to-Rune-or-Sources/Rune>
python3 scripts/generate_ubiquitous_components.py --workspace <repo-root> --app-root <path-to-app-root>
python3 scripts/generate_ubiquitous_components.py --workspace <repo-root> --include-private
python3 scripts/generate_ubiquitous_components.py --workspace <repo-root> --no-global-sync
python3 scripts/generate_ubiquitous_components.py --workspace <repo-root> --global-rune-output <absolute-global-path>
```

Default behavior excludes `private`/`fileprivate` declarations so the catalog stays focused on offered surface area. Use `--include-private` for implementation-level audits.

Default behavior also syncs a Rune-only copy to:
- `$CODEX_HOME/shared/ubiquitous-components/rune/UBIQUITOUS_COMPONENTS.md`
- fallback when `CODEX_HOME` is unset: `~/.codex/shared/ubiquitous-components/rune/UBIQUITOUS_COMPONENTS.md`
- metadata file: `.../UBIQUITOUS_COMPONENTS.metadata.json`

5. Enforce completeness.
Confirm that each discovered category root contributes output:
- `Components`
- `ViewModifiers`
- `Services`
- `Views` and/or `Screens`
- `Extensions`

6. Verify extraction quality.
Confirm each declaration row includes:
- Access level
- File + line
- API count
- Parameter count
- Summarized entry points (`init`/`func` display names)

7. Patch weak summaries only when needed.
If generated `What` descriptions are too generic for key APIs, edit those rows directly in `docs/UBIQUITOUS_COMPONENTS.md` using code evidence from the same files.

8. Return a concise summary.
Report:
- source roots used
- declaration/API/parameter counts
- any missing Rune root or partial-coverage caveat
- context-size caveat when output is still large
- local output path and global Rune output path

## Output Requirements

- Write the file strictly as `docs/UBIQUITOUS_COMPONENTS.md` unless the user asks for a different path.
- Also write/sync the Rune-only global artifact unless the user explicitly disables it.
- Keep sections categorical and exhaustive for discovered roots.
- Keep rows compact and deterministic (one declaration per row).
- Keep `Entry Points` concise (top APIs with overflow marker).
- Keep claims implementation-grounded (file path + signature evidence).
- Keep Rune revision traceable through `Package.resolved` when available.

## Failure Handling

If Rune source is not found:
- Fail fast by default.
- Ask for `--rune-root` or for the user to resolve package dependencies in Xcode.
- Optionally run with `--allow-missing-rune` only when the user explicitly accepts partial output.

## Reference

For the expected markdown layout, use:
- `references/output-structure.md`
