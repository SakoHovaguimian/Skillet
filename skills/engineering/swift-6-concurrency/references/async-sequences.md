# Async sequences and callback bridges

Use an async function for one result and an AsyncSequence for multiple values. A callback bridge must define registration, error/completion, buffering, cancellation, and cleanup together.

For streams, choose buffering based on the consumer: latest-state updates may drop older values, while events requiring complete delivery need another policy. Unbounded buffering can grow without limit when production outruns consumption. AsyncStream yield is not a backpressure guarantee.

Set termination cleanup for observer tokens or producer handles. Inspect the termination callback's concurrency requirements and the source API's required isolation; cleanup does not automatically run on the registering actor. Account for termination racing with registration and for repeated cleanup. Do not invent a universal lock or detached task without examining the API.

A continuation-based one-shot bridge must resume exactly once on every terminal path, including cancellation/error, and coordinate callbacks that race. A checked continuation detects some misuse; it does not implement cancellation or make the producer thread-safe.

Keep source-specific examples with the actual source contract; an illustrative `startDownload` function is not a working cancellation implementation.
