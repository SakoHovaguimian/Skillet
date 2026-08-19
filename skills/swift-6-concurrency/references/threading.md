# Threading And Isolation

## Tasks Are Not Threads

Swift schedules tasks on a cooperative thread pool. A task may resume on a different thread after suspension.

## Use Isolation Language, Not Thread Language

- Prefer describing ownership with `@MainActor`, actors, and nonisolated code.
- Avoid reasoning by manually pinning work to queues unless required for interop.

## Suspension Points

Every `await` can allow interleaving work. Re-check assumptions after suspension.

## Swift 6.2 Migration Detail

When `NonisolatedNonsendingByDefault` is enabled, nonisolated async behavior changes. Confirm feature flags before diagnosing runtime hops or Sendable diagnostics.

## Debugging

Use Instruments concurrency templates and isolation-aware reasoning. Avoid relying on `Thread.current` in async contexts under Swift 6 mode.
