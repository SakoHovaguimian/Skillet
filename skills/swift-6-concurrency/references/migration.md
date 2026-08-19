# Migration To Swift 6

## Strategy

1. Confirm current settings (`SWIFT_VERSION`, strict concurrency, default isolation, upcoming features).
2. Update dependencies first.
3. Add async alternatives before replacing closure APIs.
4. Raise strict-concurrency level incrementally: minimal -> targeted -> complete.
5. Keep PRs small and scoped to concurrency behavior.
6. Flip to Swift 6 mode after diagnostics are under control.

## Rules Of Thumb

- Do not blanket-apply `@MainActor`.
- Prefer fixing boundary ownership over suppressing warnings.
- Use `@preconcurrency` only as temporary debt.
- Record explicit follow-up cleanup tasks for every escape hatch.

## Combine/Rx Migration

- Replace pipeline-only use cases with direct async flow where possible.
- Use AsyncAlgorithms for debounce/throttle/merge/combineLatest patterns.
- Prefer `NotificationCenter.notifications(...)` async streams over Combine sinks for actor-safe observation.
