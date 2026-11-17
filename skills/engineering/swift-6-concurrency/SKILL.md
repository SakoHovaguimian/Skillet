---
name: swift-6-concurrency
description: Diagnose Swift concurrency failures and make scoped repairs using the target's actual isolation and task-lifetime rules. Use when resolving actor or Sendable diagnostics, stale async results, cancellation bugs, hangs, or concurrency migrations. Do not use for general Swift style or merely because unchanged code contains async or await.
disable-model-invocation: true
---

# Swift 6 Concurrency

## Outcome

Identify the responsible isolation boundary or task-lifetime failure, choose the smallest correct repair, and explain the behavior still requiring verification. Support diagnosis, review-only, implementation, and migration according to the user's requested scope.

## Inputs and preconditions

Reuse exact diagnostics, reproduction, affected targets, and settings already established. Read repository restrictions before running commands. Discover compiler/toolchain version separately from Swift language mode; a Swift 6 toolchain can compile a target in Swift 5 mode.

When settings affect the answer, read [settings and execution semantics](references/settings.md). Inspect the affected target/configuration's `Package.swift`, `.pbxproj`, referenced `.xcconfig` files, or existing build logs for language mode, strict concurrency, default isolation, upcoming features, and dependency versions. Do not launch a build to discover settings unless authorized. Record unknown effective settings rather than treating a missing key as a known default.

## Workflow

1. Classify the problem: compiler isolation/transfer diagnostic, runtime ordering/lifetime defect, responsiveness problem, or migration. Read the exact diagnostic and notes; for a runtime bug, capture the expected state and observed sequence.
2. Map only the relevant owners: caller isolation, callee isolation, values or closures crossing between them, task owner, and completion/cancellation path. Mark inferred isolation separately from an explicit annotation. For an ordering bug, identify the state read before suspension and the condition that must remain true before writing a result.
3. Load the relevant references below. Use the current toolchain's official documentation or Swift Evolution proposal when behavior is version-sensitive or not covered here. Match implemented status and feature settings; do not treat a newly published proposal as an available feature.
4. Choose the smallest repair that restores the contract. Consider keeping operations in one isolation domain, transferring an immutable value snapshot, changing ownership/lifetime, or a supported one-way transfer. Do not add `Sendable` until the type's semantics justify it. A cancellation or stale-result bug may need request identity rather than another actor annotation.
5. In review-only mode, report the repair without editing. Otherwise apply it within scope and inspect callers, protocols, conformances, live/mock implementations, and captures affected by the changed contract. Keep project-wide setting changes separate from a local diagnostic fix unless migration was requested.
6. Verify the actual risk with authorized checks. Inspect cancellation, stale completions, state after suspension, and lifetime even when compilation passes. When execution is unavailable, state exactly what inspection supports and what still requires compiler/runtime confirmation.

### Reference routing

| Problem | Read |
| --- | --- |
| Swift version, default isolation, unexpected executor behavior | [Settings](references/settings.md), [threading](references/threading.md) |
| Actor access, reentrancy, protocol isolation | [Actors](references/actors.md) |
| Non-Sendable value, closure capture, ownership transfer | [Sendable](references/sendable.md) |
| Cancellation, task groups, stale results | [Tasks](references/tasks.md) |
| Retained ViewModel, polling, observers | [Memory management](references/memory-management.md) |
| Callback bridging, buffering, termination | [Async sequences](references/async-sequences.md) |
| Core Data | [Core Data](references/core-data.md) |
| Migration | [Migration](references/migration.md) |
| Other focused topics | [Reference index](references/reference-index.md) |

## Constraints

- Preserve requested mode and scope. Do not blanket-apply `@MainActor`, disable checking, or use `Task.detached` merely to silence a diagnostic.
- Async syntax does not establish off-main execution or automatic cancellation. Keep data-race safety, ordering correctness, and responsiveness separate.
- Unsafe opt-outs require a concrete safety invariant, its enforcement owner, why a safe alternative is insufficient, and a condition for removal or re-evaluation. Do not invent verification to justify them.
- Honor restrictions on builds, tests, profiling, dependencies, and production access. Reference checklists do not authorize those operations.

## Failure handling

- Effective settings are unknown: provide conditional guidance only where the answer differs and identify the file/log or authorized check that would settle it.
- A diagnostic cannot be reproduced: inspect the provided code and name the missing evidence. Do not invent an isolation explanation from a paraphrase.
- A dependency owns the incompatible API: explain the boundary and scoped adapter or mitigation; update the dependency only when authorized.
- Compiler success is unavailable: report source inspection, not a compiled or runtime-verified fix.

## Output contract

Report the relevant settings, diagnostic or failure, owner/boundary, chosen repair and rationale, and verification actually performed. Include any unsafe invariant and remaining uncertainty. Use a short explanation for one diagnostic; use a boundary table only when several owners make it useful.
