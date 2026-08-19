---
name: ubiquitous-components-fetch
description: Fetch the globally shared Rune components catalog and make it available inside the current project for local context use.
disable-model-invocation: true
---

# Ubiquitous Components Fetch

Fetch the globally shared Rune catalog produced by `$ubiquitous-components` and copy it into the current workspace.

## Workflow

1. Resolve the global source path.
Default source path:
- `$CODEX_HOME/shared/ubiquitous-components/rune/UBIQUITOUS_COMPONENTS.md`
- fallback when `CODEX_HOME` is unset: `~/.codex/shared/ubiquitous-components/rune/UBIQUITOUS_COMPONENTS.md`

2. Validate the global file exists.
If missing, tell the user to run `$ubiquitous-components` in any Rune-capable project first to publish it.

3. Copy into the current workspace.
Use:

```bash
python3 scripts/fetch_global_ubiquitous_components.py --workspace <repo-root>
```

Common variants:

```bash
python3 scripts/fetch_global_ubiquitous_components.py --workspace <repo-root> --output docs/UBIQUITOUS_COMPONENTS_GLOBAL.md
python3 scripts/fetch_global_ubiquitous_components.py --workspace <repo-root> --global-input <absolute-global-path>
python3 scripts/fetch_global_ubiquitous_components.py --workspace <repo-root> --read-only
```

4. Return a concise summary.
Report:
- global source path used
- global `generated_at` timestamp when metadata is present
- local destination path written (if any)
- line/byte size of the fetched file

## Output Requirements

- Default local output path: `docs/UBIQUITOUS_COMPONENTS_GLOBAL.md`.
- In `--read-only` mode, do not write files; only print source path and size.
- Keep behavior deterministic and idempotent.

## Failure Handling

If the global file is missing:
- Fail with a clear error message showing the expected path.
- Recommend running `$ubiquitous-components` to publish the global catalog.
