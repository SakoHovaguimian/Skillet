# Task lifetime and cancellation

Choose sequential awaits for dependent work, `async let` for a fixed set of independent child operations, and a task group for dynamic child work. Bound fan-out to the resource and cancellation contract. A group returns only after its children finish; cancellation cannot force an uncooperative operation to terminate.

`Task {}` starts unstructured work and can inherit the surrounding actor context. It does not automatically become a child whose cancellation follows the caller. Store its handle when an owner must await, replace, or cancel it. Dropping a handle does not stop the task. `Task.detached` loses inherited context and requires explicit lifetime management; it is not the default tool for off-main work. See [SE-0304](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0304-structured-concurrency.md).

## Review the completion path

- Check cancellation before expensive work and before applying a result or presenting an error when cancellation should discard it.
- Keep cancellation out of ordinary failure UI unless the product explicitly treats it as an error.
- For replaceable requests, verify identity as well as cancellation when a stale result or deferred cleanup can overwrite newer state.
- Ensure cleanup releases the resource created by that operation. An old task must not hide a newer HUD or clear its task handle.
- Awaiting an unstructured task's value does not by itself propagate cancellation from the awaiting task.

Cancellation handlers can race with the operation and may run without its actor isolation. Inspect cleanup synchronization and callback contracts before capturing mutable resources. Follow [memory-management guidance](memory-management.md) for long-running work.
