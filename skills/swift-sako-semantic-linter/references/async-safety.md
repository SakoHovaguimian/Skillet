# Async, Task, and Loading Rules

- Store independently cancellable unstructured work in a named task property.
- Cancel replaceable work before assigning its replacement.
- Cancel every stored task during deinitialization; use `isolated deinit` when required by the type's isolation.
- Snapshot dependencies and required IDs before entering a task so the operation does not race mutable ViewModel configuration or retain the ViewModel unnecessarily.
- Capture the ViewModel weakly in long-lived tasks and perform UI mutation on `@MainActor`.
- Check cancellation before committing results or presenting errors.
- Use `defer` for paired cleanup and loading-state completion. A cancelled operation must still dismiss owned presentation but must not commit results or mark the initial load successful.
- For fetch-backed screens, keep `isLoading`, `hasCompletedInitialLoad`, `hasContent`, and `shouldShowEmptyState` coherent. Gate empty state on completed initial load and non-loading state.
- Use the project's standard loading alert and error-message helpers when available.
