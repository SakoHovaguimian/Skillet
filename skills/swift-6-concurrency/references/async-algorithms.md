# AsyncAlgorithms

Use AsyncAlgorithms when stream composition is required beyond standard library features.

## High-Value Operators

- `debounce`: emit after inactivity window
- `throttle`: limit emit frequency
- `merge`: interleave independent streams
- `combineLatest`: react with newest values from multiple streams
- `zip`: pair values by order

## Example

```swift
import AsyncAlgorithms

for await query in searchQueries
    .debounce(for: .milliseconds(400))
    .removeDuplicates()
{
    await search(query)
}
```

## Multi-Producer Patterns

Use `AsyncChannel` or `AsyncThrowingChannel` for coordinated producer-consumer flows with backpressure.
