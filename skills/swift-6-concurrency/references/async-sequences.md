# Async Sequences And Streams

## When To Use

- Use `AsyncSequence` for asynchronous iteration over multiple values.
- Use `AsyncStream` to bridge callback/delegate APIs.
- Use regular `async` functions for single-value request/response.

## AsyncStream Bridging Pattern

```swift
func download(_ url: URL) -> AsyncThrowingStream<Event, Error> {
    AsyncThrowingStream { continuation in
        startDownload(url,
            progress: { continuation.yield(.progress($0)) },
            completion: { result in
                continuation.yield(with: result.map(Event.completed))
                continuation.finish()
            }
        )
    }
}
```

## Lifecycle

Set `continuation.onTermination` for cleanup and observer removal.

## Buffer Policy

- `.unbounded`: keep all buffered values.
- `.bufferingNewest(n)`: drop older values.
- `.bufferingOldest(n)`: preserve earliest values.
