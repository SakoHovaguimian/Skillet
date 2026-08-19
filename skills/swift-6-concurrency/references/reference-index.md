# Swift Concurrency Reference Index

## Fundamentals

| File | Description |
|---|---|
| `async-await-basics.md` | Core async/await syntax, call patterns, `async let` |
| `tasks.md` | Task lifecycle, cancellation, priorities, task groups |
| `glossary.md` | Quick term definitions |

## Thread Safety And Isolation

| File | Description |
|---|---|
| `actors.md` | Actor isolation, global actors, reentrancy |
| `sendable.md` | Sendable rules, closure captures, escape hatches |
| `threading.md` | Tasks vs threads, suspension points, isolation domains |

## Advanced Patterns

| File | Description |
|---|---|
| `async-sequences.md` | AsyncSequence and AsyncStream usage and bridging |
| `async-algorithms.md` | Debounce/throttle/merge/combineLatest/channel patterns |
| `memory-management.md` | Retain-cycle and task lifetime patterns |
| `performance.md` | Instruments workflow and optimization checklist |

## Integration And Migration

| File | Description |
|---|---|
| `core-data.md` | Core Data-safe concurrency integration patterns |
| `migration.md` | Swift 6 migration plan with minimal blast radius |
| `testing.md` | XCTest and Swift Testing async patterns |
| `linting.md` | Concurrency-related lint guidance |

## Quick Problem Mapping

- Non-Sendable diagnostic: `sendable.md`
- Main actor-isolated diagnostic: `actors.md`, `threading.md`
- async_without_await: `linting.md`
- Core Data warning: `core-data.md`
- XCTest async issue: `testing.md`
- Combine migration: `async-algorithms.md`, `migration.md`
