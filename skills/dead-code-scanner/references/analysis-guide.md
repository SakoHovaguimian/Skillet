# Dead code analysis guide

## Mental model

Dead code is code that does not earn its maintenance cost under the system's current contract. Unreachability is the strongest signal, but it is only one kind of deadness.

Model the repository as a graph:

```text
live root -> reachable behavior -> observed result or required side effect
                    |
                    +-> dead end when nothing required observes it
```

A reference creates an edge. It does not prove that either endpoint matters. Trace the edge until it reaches an accepted requirement, an externally supported contract, or an observed effect.

## Establish live roots

Search every root type the repository actually uses:

- application processes, executables, CLIs, servers, workers, scheduled jobs, and serverless handlers
- package or library exports consumed inside or outside the repository
- framework routes, screens, controllers, commands, resolvers, reducers, and dependency-injection registrations
- plugin registries, callbacks, delegates, observers, event consumers, hooks, annotations, and decorators
- schemas, serializers, deserializers, reflection, runtime lookup, and string-addressed symbols
- database migrations, seeders, operational scripts, build plugins, code generators, and generated-code inputs
- configuration, feature flags, environment-selected implementations, templates, resources, localization, and assets
- test-only entry points only when the repository treats the tested behavior as a current supported contract

Read manifests and build files before assuming the conventional `main`, `index`, or application file is the only root. A monorepo can contain several independent graphs.

## Trace reachability

Follow more than imports and direct calls:

1. Control flow: calls, handlers, callbacks, commands, and lifecycle hooks.
2. Data flow: values produced, transformed, persisted, emitted, or returned.
3. Registration: routes, dependency injection, plugins, event subscriptions, reflection, and framework discovery.
4. Configuration: flags, environment selection, manifests, build settings, and deployment descriptors.
5. External entry: public API consumers, scripts, webhooks, jobs, database records, serialized names, and other repositories.

When a candidate is referenced only by another candidate, keep tracing. Classify the connected set as a possible dead island rather than marking each node live.

## Run the value audit

For every candidate and every reference that appears to keep it alive, answer:

- Which current requirement or accepted contract does this serve?
- Is the referring consumer itself reachable from a live root?
- Is the result consumed, persisted, rendered, transmitted, or otherwise observed?
- Is the side effect intentional and still required?
- Does another implementation already own the same behavior?
- Is the reference only a test, preview, fixture, example, benchmark, compatibility shim, or generated artifact?
- Is the abstraction kept for a hypothetical future consumer rather than a current requirement?
- What concrete behavior would fail if the complete removal group disappeared?

If no concrete answer survives this chain, the reference may be unnecessary even though it is real.

## Common dead ends

Look for reachable code whose work goes nowhere:

- return values that callers discard when the call has no required side effect
- state written but never read by a live consumer
- events emitted with no live subscriber, or subscribers whose results are ignored
- adapters that translate into a format no active boundary consumes
- caches that are populated but never queried, invalidated, or measured
- logging, analytics, or error translation for retired flows
- feature-flag branches whose flag can no longer select them
- retry, migration, or compatibility paths whose supported window has ended
- duplicate validators, mappers, services, routes, and UI paths shadowed by a canonical implementation

Do not remove an apparently ignored call until exceptions, timing, synchronization, mutation, I/O, accounting, telemetry, and security effects are checked.

## Support-only references

Tests can preserve an obsolete design. Treat a test reference as evidence that someone described the behavior, then ask whether the behavior remains required.

Use the same rule for:

- fixtures and snapshots
- examples and sample applications
- previews and stories
- benchmarks
- migration-only harnesses
- comments and documentation

When production behavior is retired, the supporting artifacts usually belong to the same removal group.

## Dynamic and external risks

Keep a candidate in `Review required` until these surfaces are searched or ruled out:

- public or exported package APIs
- reflection and annotation-driven discovery
- string-based class, function, route, resource, or template lookup
- serialization names, schema bindings, and database-stored identifiers
- native selectors, delegates, runtime registration, and framework lifecycle callbacks
- dependency injection and plugin registries
- generated source and the templates or schemas that produce it
- build scripts, linker settings, code-signing inputs, and deployment hooks
- other repositories, clients, automation, or operators invoking the symbol directly

Absence of an in-repository reference cannot disprove an external consumer.

## Resources, configuration, and dependencies

Trace non-code artifacts back to owning behavior:

- Assets and localization: search direct names, generated wrappers, naming conventions, templates, and runtime construction.
- Configuration and flags: confirm all environments, deployments, tenants, and rollback paths before calling a branch obsolete.
- Dependencies: inspect imports, plugins, build steps, generated code, transitive requirements, runtime loading, and use limited to dead islands.
- Migrations: confirm every supported installation has crossed the migration and that rollback or disaster recovery no longer requires it.
- Generated files: remove or change the source template/schema first when generation would recreate the candidate.

## Confidence and reporting

Use `Safe to remove` only when the report can state:

1. the live roots searched
2. the dynamic and external surfaces ruled out
3. the complete removal group
4. the current requirement analysis
5. the expected behavioral impact
6. the verification that would catch a mistake

Otherwise use `Potentially removable` or `Review required` and name the missing evidence. Estimated line, binary, dependency, or complexity savings are optional; do not invent a number.
