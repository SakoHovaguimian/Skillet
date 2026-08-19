# Glossary

- Actor isolation: exclusive access domain for actor state.
- Global actor: shared isolation domain (`@MainActor` or custom global actor).
- Sendable: marker for values safe to cross isolation boundaries.
- @Sendable: closure/function type safe for concurrent execution.
- Suspension point: `await` site where execution can pause and interleave.
- Reentrancy: actor accepts other work while current task is suspended.
- Structured concurrency: parent-child task model (`async let`, `TaskGroup`).
- AsyncSequence: asynchronous stream of values iterated with `for await`.
- AsyncStream: concrete bridge from callbacks/delegates to AsyncSequence.
- Task cancellation: cooperative stop signal for async work.
