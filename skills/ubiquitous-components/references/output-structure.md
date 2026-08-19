# Ubiquitous Components Output Structure

Use this structure when generating `docs/UBIQUITOUS_COMPONENTS.md`.

```md
# Ubiquitous Components

_Generated: 2026-03-31T20:00:00-07:00_

## Scope

- **Workspace:** `/absolute/path/to/workspace`
- **Output:** `/absolute/path/to/workspace/docs/UBIQUITOUS_COMPONENTS.md`
- **Global Rune Output:** `/Users/<you>/.codex/shared/ubiquitous-components/rune/UBIQUITOUS_COMPONENTS.md`

### Source Roots
| Source | Kind | Root |
| --- | --- | --- |
| Rune (GlowPro-abc123) | rune | `/.../DerivedData/.../SourcePackages/checkouts/Rune/Sources/Rune` |
| GlowPro | app | `/.../GlowPro/GlowPro` |

### Coverage Summary
| Source | Category | Declarations | APIs | Parameters |
| --- | --- | --- | --- | --- |
| Rune | Components | 42 | 71 | 184 |
| Rune | ViewModifiers | 19 | 33 | 64 |
| Rune | Services | 14 | 27 | 48 |
| Rune | Views | 11 | 15 | 22 |
| Rune | Extensions | 18 | 44 | 57 |
| GlowPro | Components | 9 | 12 | 55 |
| GlowPro | ViewModifiers | 1 | 1 | 3 |
| GlowPro | Services | 27 | 109 | 220 |
| GlowPro | Views | 102 | 198 | 376 |
| GlowPro | Extensions | 8 | 16 | 23 |

### Context Strategy
- This file is intentionally compact: one row per declaration with summarized entry points.
- Private/fileprivate declarations are excluded by default to emphasize offered APIs.
- Use source file references to inspect implementation details only where needed.
- For deep audits, regenerate with a script variant that emits full per-API parameter tables.

### Rune Package Pins
| Package.resolved | Location | Revision | Branch | Version |
| --- | --- | --- | --- | --- |
| `/.../Package.resolved` | `https://github.com/SakoHovaguimian/Rune` | `4363606...` | `main` | `` |

## Category: Components

### Source: Rune

| Symbol | Kind | Access | File | APIs | Params | Entry Points | What |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `CommonButton` | `struct` | `public` | `Components/Button/CommonButton.swift`:10 | 1 | 13 | `init(style:title:titleColor:...)` | Reusable UI component for common button. |
| `CommonButtonStyle` | `struct` | `public` | `Components/Button/CommonButton.swift`:183 | 2 | 0 | `solid`, `outline` | Extension API for common button style. |

## Category: ViewModifiers
... (same pattern)

## Category: Services
... (same pattern)

## Category: Views
... (same pattern)

## Category: Extensions
... (same pattern)

---

## Verification

- Confirmed all discovered `Components`, `ViewModifiers`, `Services`, `Views`/`Screens`, and `Extensions` folders were scanned.
- Confirmed each declaration row includes access, file+line, API counts, parameter counts, and summarized entry points.
- Review rows with `0` APIs to decide whether additional hand-written notes are needed.
```

## Quality Bar

- Keep each category exhaustive for discovered roots.
- Keep declaration rows deterministic and stable between runs.
- Keep `Entry Points` concise while preserving meaningful API coverage.
- Keep `What` factual and implementation-grounded.
- Keep the global Rune artifact in sync for cross-project reuse.
