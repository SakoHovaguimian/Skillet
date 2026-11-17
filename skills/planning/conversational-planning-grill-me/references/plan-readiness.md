# Plan readiness lenses

Load this reference for repository-backed feature, refactor, integration, or migration planning. Apply only relevant lenses. Absence is not a reason to invent scope.

## Product contract

- Identify the actor, trigger, expected outcome, and observable success.
- Define included states and explicit non-goals.
- Resolve canonical terms and ownership boundaries.
- Convert vague quality claims into observable acceptance criteria.

## System contract

- Identify the source of truth and every writer and reader affected.
- Define inputs, outputs, invariants, identity, ordering, and compatibility.
- Trace state transitions, cancellation, retries, duplicate delivery, partial success, and recovery.
- Distinguish client-owned behavior from server-owned behavior.

## Delivery risk

- Check migration, backfill, feature flags, phased rollout, and rollback only when existing data or users are affected.
- Identify analytics, logs, metrics, or diagnostics needed to distinguish success from silent failure.
- State performance budgets or privacy, security, or compliance constraints when the change can materially affect them.
- Name external owners, credentials, approvals, or release dependencies.

## User experience

- Cover loading, empty, partial, offline, permission-denied, error, and recovery states that can occur.
- Preserve accessibility, localization, keyboard or assistive technology behavior, and theme behavior where UI is affected.
- Define navigation, dismissal, interruption, and state restoration behavior where relevant.

## Verification

- Choose the smallest verification that can falsify the risky assumptions.
- Separate required checks from checks prohibited or unavailable in repository instructions.
- Define manual or static alternatives when builds or tests are not authorized.
- Include documentation reconciliation after behavior changes, not before evidence exists.

## Final plan quality bar

The plan is ready only when an implementer can answer:

1. What outcome must change, and how will success be observed?
2. What is the source of truth and who owns each transition?
3. Which contracts, files, and systems change?
4. What happens on failure, interruption, duplication, and rollback?
5. What is deliberately excluded or deferred?
6. Which verification is authorized and sufficient for the risk?
