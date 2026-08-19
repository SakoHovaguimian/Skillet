---
name: swift-6-concurrency
description: Expert guidance for Swift 6 concurrency design, implementation, migration, and debugging. Use when working with async/await, Task/TaskGroup, actors, @MainActor, Sendable, AsyncSequence, AsyncAlgorithms, strict concurrency diagnostics, Swift 6 migration strategy, concurrency testing, performance profiling, or linter warnings such as async_without_await. Do not use for general Swift style; use `$swift-sako-semantic-linter` for that.
disable-model-invocation: true
---

# Swift 6 Concurrency

## Outcome

Practical, production-focused guidance or fixes for concurrency-safe Swift code: the correct isolation boundary identified, the smallest safe fix chosen, and verification steps named.

## Inputs and preconditions

A concurrency question, diagnostic, or migration task, plus the project settings that alter diagnostics and runtime behavior:

- Swift language mode (`Swift 5.x` vs `Swift 6`)
- Strict concurrency level (`minimal`, `targeted`, `complete`)
- Default actor isolation (`@MainActor` vs `nonisolated`)
- Upcoming features, especially `NonisolatedNonsendingByDefault`

Read these files first:

- SwiftPM: `Package.swift`
- Xcode: `*.pbxproj` for
  - `SWIFT_STRICT_CONCURRENCY`
  - `SWIFT_DEFAULT_ACTOR_ISOLATION`
  - `SWIFT_UPCOMING_FEATURE_`

If settings are unknown and matter to the decision, ask for them before final recommendations.

## Workflow

### Triage flow

1. Read the diagnostic text exactly.
2. Mark the crossing point where data or execution crosses isolation.
3. Pick the smallest safe fix in this order:
   - Move code into the correct isolation domain.
   - Make data `Sendable`.
   - Refactor ownership/lifetime.
   - Use escape hatches only with explicit safety notes.
4. Add verification steps (tests, compile checks, profiler checks if performance-related).

### Error to reference mapping

- `non-Sendable type` diagnostics -> `references/sendable.md`, `references/threading.md`
- `Main actor-isolated` diagnostics -> `references/actors.md`, `references/threading.md`
- `async_without_await` and lint warnings -> `references/linting.md`
- XCTest/Swift Testing async failures -> `references/testing.md`
- Core Data concurrency warnings -> `references/core-data.md`
- Migration planning -> `references/migration.md`

### Tool selection rules

- Use `async/await` for single request-response async work.
- Use `async let` for a fixed number of parallel operations.
- Use `TaskGroup` for dynamic fan-out work.
- Use actors for shared mutable async state.
- Use `@MainActor` for UI state and UI-facing view models.
- Use AsyncAlgorithms for debounce/throttle/stream composition.
- Use `AsyncStream` for callback/delegate bridging.

## Constraints

1. Inspect project settings before giving migration-sensitive advice.
2. Identify the isolation boundary before proposing a fix.
3. Avoid blanket `@MainActor` fixes; justify each main-actor choice.
4. Prefer structured concurrency (`async let`, `TaskGroup`) over unstructured tasks.
5. Use `Task.detached` only when work must be independent from caller context.
6. If recommending `@preconcurrency`, `@unchecked Sendable`, or `nonisolated(unsafe)`, document a safety invariant and require follow-up cleanup.
7. Keep migration changes small and reviewable.

## Failure handling

- Settings cannot be determined and materially change the answer: present the fix per plausible setting and say which file would confirm it, instead of guessing one.
- A diagnostic cannot be reproduced from the provided context: state what is missing; do not invent an isolation story around a paraphrased error.

## Output contract

Every recommendation names: the diagnostic (verbatim when available), the isolation crossing point, the chosen fix and why smaller fixes were insufficient, any escape-hatch safety invariant, and this verification checklist applied to the change:

- Build passes with current concurrency settings.
- Concurrency diagnostics do not regress.
- Cancellation paths are covered for long-running tasks.
- Retain-cycle risks are reviewed (`Task` captures, stream observers).
- Tests updated or added for behavior changes.
- Performance-sensitive changes are measured with Instruments when relevant.

### Reference files

Use `references/reference-index.md` for navigation, then load only needed files:

- `references/async-await-basics.md`
- `references/tasks.md`
- `references/actors.md`
- `references/sendable.md`
- `references/threading.md`
- `references/async-sequences.md`
- `references/async-algorithms.md`
- `references/memory-management.md`
- `references/migration.md`
- `references/performance.md`
- `references/testing.md`
- `references/core-data.md`
- `references/linting.md`
- `references/glossary.md`
