# Memory Management In Concurrency

## Core Risk

Retain cycles occur when an object stores a `Task` that strongly captures the same object.

## Safe Pattern For Long-Lived Tasks

```swift
final class Poller {
    private var task: Task<Void, Never>?

    func start() {
        task = Task { [weak self] in
            while let self {
                await self.tick()
                try? await Task.sleep(for: .seconds(1))
            }
        }
    }

    deinit { task?.cancel() }
}
```

## AsyncSequence Observation

For never-ending streams, use weak capture and exit when owner is gone, or store and cancel the task explicitly.
