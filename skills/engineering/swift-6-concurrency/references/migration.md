# Migrate Swift concurrency

1. Record the affected target's [settings](settings.md), exact diagnostics, and relevant dependency versions. Separate migration from a local bug fix.
2. Group diagnostics by the first shared ownership or API cause. Repair that cause before adding attributes to every downstream use. Keep existing public behavior and caller contracts explicit.
3. In Swift 5 mode, enable stricter checking within authorized migration scope to expose issues incrementally. Swift 6 already enforces complete checking; do not weaken language mode to hide an unresolved defect.
4. Migrate a coherent target/API boundary at a time. Coordinate protocol witnesses, closures, mocks, and imported APIs. Add async alternatives only when the boundary needs them; do not rewrite Combine or callbacks wholesale.
5. Choose default isolation and upcoming features deliberately. A compiler upgrade does not by itself justify changing target defaults. Record the old/new settings and behavioral effects.
6. Verify the affected diagnostics and ordering/lifetime behavior with authorized checks. Record unresolved dependency limitations and unsafe opt-outs separately from completed work.

Preserve resolved dependency versions unless an authorized migration needs an update. Use the [official incremental-adoption guide](https://www.swift.org/migration/documentation/swift-6-concurrency-migration-guide/incrementaladoption/) for imported APIs and staged checking. Its examples do not override local execution restrictions.
