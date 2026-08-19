# Sendable

## Purpose

`Sendable` marks types that are safe to transfer across isolation boundaries.

## Value Types

- Prefer structs/enums for easier Sendable adoption.
- Ensure all stored properties are Sendable.
- Add explicit conformance for public API types.

## Reference Types

A class can conform safely when:

- It is `final`.
- Stored state is immutable or otherwise safely synchronized.
- All stored properties are Sendable.

Use actor isolation instead of locks when possible.

## @Sendable Closures

Closure captures used across concurrency boundaries must be Sendable-safe.

```swift
var query = "swift"
let block: @Sendable () -> Void = { [query] in
    print(query)
}
```

## Escape Hatches

- `@unchecked Sendable`: use only with documented invariants and strong tests.
- `@preconcurrency`: temporary suppression for older dependencies; track removal.
- `nonisolated(unsafe)`: last resort with strict ownership controls.
