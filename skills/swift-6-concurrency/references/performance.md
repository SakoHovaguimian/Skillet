# Concurrency Performance

## Measure First

Use Instruments (`Swift Tasks`, `Swift Actors`, and main-thread analysis) before changing architecture.

## Typical Bottlenecks

- Main-actor work doing heavy CPU tasks.
- Actor contention from serialized hot paths.
- Excessive suspension points and unnecessary actor hops.

## Optimization Checklist

- Remove unnecessary `async` helpers.
- Batch actor work to reduce boundary crossings.
- Use `TaskGroup` for truly independent parallel work.
- Verify cancellation and backpressure behavior under load.
- Re-profile after each change.
