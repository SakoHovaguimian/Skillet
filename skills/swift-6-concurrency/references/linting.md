# Linting For Concurrency

## async_without_await

Prefer removing `async` when no suspension is required.

If `async` is required by protocol/override/conformance shape, avoid fake awaits; use narrow suppression with rationale.

## General Rule

Treat lint warnings as design signals. Prefer architectural fixes over annotation-only silencing.
