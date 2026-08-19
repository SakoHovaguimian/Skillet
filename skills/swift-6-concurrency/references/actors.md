# Actors

## Core Model

Actors serialize access to mutable actor state.

```swift
actor Counter {
    private var value = 0
    func increment() { value += 1 }
    func current() -> Int { value }
}
```

Cross-actor access requires `await`.

## Global Actors

Use `@MainActor` for UI state and UI-facing view models.

```swift
@MainActor
final class ViewModel: ObservableObject {
    @Published var title = ""
}
```

Create custom global actors for shared, serialized non-UI domains.

## Reentrancy

Assume actor state may change after every `await`.

```swift
actor Account {
    var balance = 0

    func deposit(_ amount: Int) async {
        balance += amount
        await audit()
        // balance may have changed while suspended
    }
}
```

Prefer completing critical state transitions before suspension points.

## nonisolated

Use `nonisolated` only for truly immutable/independent values and protocol requirements that do not touch isolated mutable state.

## Isolation Inheritance Pattern

For `Task` closures that need to work with non-Sendable values in caller isolation, capture `#isolation` explicitly.

```swift
func run(delegate: NonSendableDelegate,
         isolation: isolated (any Actor)? = #isolation) {
    Task {
        _ = isolation
        delegate.doWork()
    }
}
```
