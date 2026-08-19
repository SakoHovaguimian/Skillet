# Core Data And Concurrency

## Safe Transfer Pattern

Pass `NSManagedObjectID` across isolation boundaries, not live `NSManagedObject` instances.

## Context Ownership

- Keep each `NSManagedObjectContext` inside its owning isolation domain.
- Perform context work within that domain, then transfer IDs or value snapshots.

## Migration Guidance

When strict concurrency emits Core Data Sendable warnings, first remove cross-boundary object sharing before considering suppression attributes.
