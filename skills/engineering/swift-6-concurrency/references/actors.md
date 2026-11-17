# Actors and reentrancy

Actors protect isolated mutable state. Cross-isolation access can require suspension; access already inside the same isolation domain does not automatically need another `await`. Global actors such as `MainActor` express a shared isolation domain. Match the actual UI/service contract rather than annotating every type alike.

## State across suspension

Serialization does not make an async operation atomic. At a suspension point, another operation may change actor state. Identify the invariant that must hold when work resumes. Re-read or validate state, use a request generation/identity when appropriate, or reserve/update state before suspension with a defined failure recovery path. Do not hold a blocking lock across `await`.

For two loads A then B, actor isolation alone does not stop A from completing last and overwriting B. Cancellation plus an identity check may be necessary when canceled work can still complete or when several producers share an owner.

See [SE-0306](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0306-actors.md) for actor isolation and reentrancy.

## Nonisolated APIs and conformances

Use `nonisolated` when a declaration's contract permits access without that actor's protection. It cannot safely expose isolated mutable state. For async behavior, use the [settings reference](settings.md); do not assume every nonisolated async call leaves the actor.

For a protocol mismatch, inspect the requirement, witness, conformance isolation, and actual callers before moving the entire type onto or off an actor. Check compiler support for version-sensitive conformance features.

An `isolated` actor parameter can express an operation on the supplied actor. Use it when the API needs that contract, not as a routine capture trick. Do not copy a `#isolation` pattern without proving how the closure receives its isolation.
