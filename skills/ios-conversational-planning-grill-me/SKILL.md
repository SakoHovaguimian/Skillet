---
name: ios-conversational-planning-grill-me
description: Produce an implementation-ready plan for iOS projects through repository discovery, iOS architecture analysis, and a conversational decision interview. Use before coding when UIKit, SwiftUI, Rune, navigation, lifecycle, concurrency, or ubiquitous-language and business-logic constraints matter. Stop at a final approval gate before implementation.
disable-model-invocation: true
---

# iOS conversational planning + grill me

## Outcome

Use the stack-neutral `$conversational-planning-grill-me` skill as the shared planning, grilling, approval-gate, and handoff engine, then add the iOS-specific evidence and constraints below. Do not duplicate or weaken the shared engine's decision protocol.

## iOS preflight

Before invoking the shared engine, read, in order when present:

1. Applicable `AGENTS.md` files and explicit user constraints.
2. `docs/UBIQUITOUS_LANGUAGE*` and `docs/UBIQUITOUS_BUSINESS_LOGIC*`.
3. `CONTEXT.md`, `CONTEXT-MAP.md`, ADRs, architecture docs, and feature notes.
4. Relevant models and contracts, then services, DI, navigation, state owners, and UI.
5. Tests, fixtures, previews, analytics, flags, migrations, and recent history that clarify intended behavior.
6. Nearby implementation exemplars and formatter or linter configuration.

Use `rg` and targeted reads. Avoid broad repository dumps. Follow imports and call sites only until each planning branch has enough evidence.

Treat domain docs as domain authority, not infallible snapshots. When docs and executable behavior differ, report both with source anchors and make reconciliation an explicit decision.

## iOS-specific planning lenses

- Match existing DI, navigation, analytics, service, mock, preview, and lifecycle patterns before proposing new abstractions.
- Prefer canonical terms from `UBIQUITOUS_LANGUAGE` and invariants from `UBIQUITOUS_BUSINESS_LOGIC`, while flagging stale documentation.
- Plan Rune-first UI composition and active theme tokens. Identify a Rune gap only when local and shared catalogs cannot satisfy the need.
- Keep new top-level models and other independently owned types in focused files when repository instructions require separation.
- Plan Swift concurrency isolation explicitly when async work crosses UI, service, or callback boundaries.
- Account for UIKit and SwiftUI entry points, bridges, target membership, generated resources, previews, and extension or system callback reachability when they affect the change.

Read [references/plan-readiness.md](references/plan-readiness.md) after the shared engine confirms that a repository-backed plan is needed. Apply only the iOS-specific lenses relevant to the task.

## Shared-engine handoff

Invoke `$conversational-planning-grill-me` with the iOS evidence, terminology, constraints, and open decisions. The shared engine owns `$grill-me`, the decision ledger, conflict handling, `$unslop`, the final approval gate, and the implementation handoff. Carry the iOS-specific findings into its final plan.

For approved SwiftUI work, preserve the shared handoff rules and invoke `$project-rune-implementation-protocol` when that skill applies. Invoke `$swift-sako-semantic-linter` after in-scope Rune Swift or SwiftUI edits, and `$swift-6-concurrency` when the approved work materially changes isolation, `Sendable`, tasks, actors, or async control flow.

## Writing hygiene

The shared engine invokes `$unslop` once for the outermost final planning artifact. If this skill produces a separate iOS-specific report outside that engine, invoke `$unslop` on that complete artifact. Preserve paths, symbols, code, evidence anchors, user decisions, and technical meaning. Do not run two unslop passes on the same artifact.
