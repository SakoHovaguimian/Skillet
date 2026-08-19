# iOS plan-readiness lenses

Load this supplemental reference after the stack-neutral planning skill's readiness lenses when an iOS repository-backed plan is confirmed. Apply only the lenses relevant to the task.

## iOS architecture

- Match existing DI, navigation, analytics, service, mock, preview, and lifecycle patterns before proposing new abstractions.
- Identify UIKit and SwiftUI entry points, bridges, target membership, generated resources, previews, extensions, and system callbacks that affect the change.
- Trace state ownership across view models, coordinators, environment objects, delegates, Combine pipelines, and async tasks.

## Grimoire and Rune

- Prefer canonical terms from `UBIQUITOUS_LANGUAGE` and invariants from `UBIQUITOUS_BUSINESS_LOGIC`, while flagging stale documentation.
- Plan Rune-first UI composition and active theme tokens. Identify a Rune gap only when local and shared catalogs cannot satisfy the need.
- Keep new top-level models and other independently owned types in focused files when repository instructions require separation.

## Swift behavior

- Plan Swift concurrency isolation explicitly when async work crosses UI, service, or callback boundaries.
- Cover accessibility, localization, Dynamic Type, reduced motion, and theme behavior where UI is affected.
- Identify the smallest authorized verification that can falsify the risky assumptions. Do not assume an Xcode build or test run is allowed.
