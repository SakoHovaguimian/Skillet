# Tasks, threads, and isolation

Reason about actor ownership and executor behavior before inspecting thread identity. Tasks can suspend and resume; an async call is not proof of a background thread, a new task, or simultaneous execution. A thread observation alone does not establish the compiler's isolation contract.

Read [settings and execution semantics](settings.md) before diagnosing nonisolated async hops. Default isolation and upcoming features vary by module and configuration.

Every potential suspension deserves a check of assumptions about mutable state. Actor serialization prevents simultaneous isolated access; it does not prevent other operations from changing state while the current operation is suspended.

Use authorized profiling for responsiveness and contention. If it cannot run, explain the suspected blocking or serialization mechanism without inventing a measured performance result.
