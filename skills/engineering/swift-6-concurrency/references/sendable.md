# Sendable and ownership transfer

`Sendable` describes safe sharing across concurrency domains; it does not make an arbitrary mutable object safe. Inspect every stored property and mutation path before adding conformance. Immutable value snapshots often avoid sending an entire service or model owner.

A nonisolated final class with immutable Sendable stored properties can support checked conformance. A lock-backed mutable class generally needs a separately justified unchecked conformance; “uses a lock” is not compiler proof that every access follows it. Global-actor-isolated types have a different isolation contract.

`@Sendable` closures constrain captured state. Capture a needed immutable value rather than mutable `self` when that matches ownership, but remember a capture list copies a reference, not the referenced object. Isolation still governs access to that object.

## One-way transfer

On supporting compilers, region-based isolation and `sending` parameters/results allow certain disconnected non-Sendable values to transfer safely. This does not make the type universally Sendable, and conflicting access after transfer is invalid. Inspect aliases and later uses; do not add `sending` just to move an error to a caller. See [SE-0430](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0430-transferring-parameters-and-results.md).

## Opt-outs

For `@unchecked Sendable`, `nonisolated(unsafe)`, or a migration use of `@preconcurrency`, record the exact invariant, enforcing owner, affected boundary, and follow-up condition. The attribute does not add synchronization. Check a safe ownership or API adaptation first. Verification follows repository restrictions; no attribute justifies inventing tests or claiming runtime safety from inspection.
