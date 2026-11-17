# AsyncAlgorithms

Use an existing AsyncAlgorithms dependency when its operators match the required stream semantics. Adding it is a dependency decision within the user's scope, not an automatic concurrency fix.

Verify names and signatures against the resolved version and [official package documentation](https://github.com/apple/swift-async-algorithms). Do not copy Combine operators into an AsyncSequence chain without checking availability.

Choose debounce for an inactivity window, throttle for bounded emission frequency, merge for interleaving, combineLatest for current values, and zip for positional pairing. Define error, cancellation, buffering, and completion behavior before replacing an existing pipeline. Timing changes are behavior changes.

Use AsyncChannel or AsyncThrowingChannel only when their producer/consumer contract fits. Inspect whether senders can remain suspended after consumer termination and who finishes or cancels them.
