# Concurrency Performance

## Measure First

When profiling is authorized and available, use Instruments (`Swift Tasks`, `Swift Actors`, and main-thread analysis) to identify the bottleneck before changing architecture. Otherwise state the source-based hypothesis and the measurement still needed.

## Typical Bottlenecks

- Main-actor work doing heavy CPU tasks.
- Actor contention from serialized hot paths.
- Excessive suspension points and unnecessary actor hops.

## Optimization Checklist

- Inspect callers and execution semantics before removing `async`; a signature can encode an isolation or protocol contract.
- Batch actor work to reduce boundary crossings.
- Use `TaskGroup` for truly independent parallel work.
- Verify cancellation and backpressure behavior under load.
- Re-profile after each change.
