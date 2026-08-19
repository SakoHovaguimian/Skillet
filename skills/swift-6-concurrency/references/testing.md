# Testing Async And Concurrent Code

## XCTest Patterns

- Mark tests `async` and `throws` as needed.
- Use `await fulfillment(of:timeout:)` for expectations in async tests.
- Avoid blocking waits from async contexts.

## Practical Checks

- Verify cancellation propagation.
- Verify actor-isolated state transitions around suspension points.
- Verify deallocation for long-lived observer tasks.

## Flake Reduction

- Avoid sleep-based assertions when possible.
- Use deterministic synchronization points.
