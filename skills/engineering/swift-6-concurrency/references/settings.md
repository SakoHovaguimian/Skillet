# Settings and execution semantics

Use the affected target and configuration, not another target's settings. Record the toolchain version, language mode, strict-concurrency level, default actor isolation, relevant upcoming features, and dependency/SDK context. Inspect inherited `.xcconfig` settings and conditional overrides when present.

| Source | Relevant evidence |
| --- | --- |
| Xcode project/configuration | `SWIFT_VERSION`, `SWIFT_STRICT_CONCURRENCY`, `SWIFT_DEFAULT_ACTOR_ISOLATION`, `SWIFT_APPROACHABLE_CONCURRENCY`, `SWIFT_UPCOMING_FEATURE_*`, and explicit compiler flags |
| SwiftPM | Tools version, language modes, target `swiftSettings`, `.defaultIsolation(...)`, and `.enableUpcomingFeature(...)` |
| Existing diagnostics/build log | Actual invocation, imported API annotations, and effective flags when recorded |

A language mode, deployment target, and compiler version are different facts. Do not infer feature enablement from the phrase “Swift 6” or assume an Xcode convenience setting proves every effective flag. Default isolation is per module; it does not rewrite imported declarations. See [SE-0466](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0466-control-default-actor-isolation.md), implemented in Swift 6.2.

## Nonisolated async behavior

| Configuration / declaration | Behavior relevant to diagnosis |
| --- | --- |
| Earlier semantics, without `NonisolatedNonsendingByDefault` | A nonisolated async function switches off an actor to the generic executor. |
| Swift 6.2+ with `NonisolatedNonsendingByDefault` | Nonisolated async functions stay on the caller's actor by default. |
| Explicit `nonisolated(nonsending)` on a supporting compiler | States caller-isolation behavior explicitly. |
| Explicit `@concurrent` on a supporting compiler | Makes async execution switch off the caller's actor; does not create a detached task. |

These spellings and the feature-gated change are described in [SE-0461](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0461-async-function-isolation.md), implemented in Swift 6.2. Do not introduce them into older toolchains. A missing annotation alone is insufficient to infer a hop: inspect inferred isolation and enabled settings.

Keep CPU-heavy synchronous work off a UI actor intentionally. Adding `async` alone does not make work nonblocking. Do not change the whole module's isolation default to repair one call.

## Migration boundaries

Complete checking in Swift 5 mode can reveal migration work before switching language modes. Swift 6 mode enforces complete data-race checking; lowering the strictness selector is not a sound Swift 6 repair. Move one target and its relevant API contracts at a time. Consult the [official migration guide](https://www.swift.org/migration/documentation/swift-6-concurrency-migration-guide/incrementaladoption/) for the actual toolchain and imported SDK boundaries.
