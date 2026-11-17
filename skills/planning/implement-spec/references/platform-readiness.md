# Platform readiness

Read only the sections for selected platforms and relevant boundaries. Use these
as inspection lenses, not new work to add. The target's actual stack and guides
govern; do not introduce a layer, provider, or control merely because it appears
here. Feed findings into the specification's contracts, Pattern Lock, and slices.

## BE/API

Trace the actual route → controller → service → repository → ORM flow and its
registration. Inspect canonical mapping, repository signatures and transaction
client placement, service enrichment such as `getDetailed` where used,
query/filter/sort/pagination semantics, identity/ownership, errors, and cache
invalidation. Preserve business-scoped identity, role distinctions, and private
record access.

Verify schema, enum, independent model, OpenAPI naming, layout, and section-comment
rules. Reuse existing auth, upload, notification, storage, and provider services.
Specify exact schema/contract changes, migration implications, data preservation,
and separate operational permissions. Scope compatibility removals explicitly;
do not invent compatibility systems or alternate storage layers.

## Web

Trace the target's screen/component → query hook → domain service → API client →
authenticated proxy flow where those layers exist, including actual state owners
and invalidation. Reuse shared controls, page/card/modal layouts, theme/motion
tokens, string catalogs, and presentation services. Preserve product vocabulary
and align roles, validation, and recovery with actual backend capability.

Cover affected navigation/history/deep links, focus, drafts, loading/empty/error/
conflict behavior, reconciliation, and responsive/keyboard interaction. Preserve
loaded content and resolved empty states during refresh. Layout or spacing changes
do not authorize replacing approved colors, components, or unrelated behavior.

Where demo mode exists, cover applicable roles, ownership, validation, filtering,
sorting/pagination, mutation persistence, reset, failure simulation, and new
feature states. Keep live versus mock-only capability explicit; demo success does
not establish backend integration.

## iOS

Inspect the owning screen/ViewModel pair, navigation setup, service protocols,
live/mock implementations, and DI registrations, including Factory where used.
Reuse app components and local design-system controls, including Rune where used.
Preserve state ownership, route context, subscriptions, task cancellation,
loading, alerts, presentation, and the target's lifecycle exceptions.

Match local member ordering, `self.` usage, named view-building helpers, spacious
formatting, semantic spacing/font/color tokens, and independent model placement.
Synchronize affected protocols, registrations, live/mock/demo/preview resolution,
route destinations, strings, analytics, and explicit source/resource membership.
Retain loaded content and resolved empty states during refresh. Do not introduce
parallel theme, navigation, auth, or loading systems. Record device/runtime and
Xcode verification as pending unless separately authorized and performed.

## Relevant security boundaries

For protected data or privileged operations, locate actual authentication,
authorization, ownership/tenant enforcement, validation, private storage/cache,
and sensitive logging boundaries. UI visibility alone is not authorization.
Identify server enforcement and applicable live/demo ownership behavior.

For uploads, external calls, and private exports, inspect relevant access checks,
accepted types/limits, signed-URL exposure/expiry, validation, retries, cancellation,
and cleanup contracts. Preserve required privacy controls without adding unrelated
security machinery. Use configuration key names; never copy credentials, tokens,
or private payloads into the specification or telemetry.

Raise unsafe existing examples as conflicts instead of silently copying them.
Do not claim a security certification from this review. If a selected client needs
missing backend behavior, surface the exact gap for an explicit BE-scope,
deferral, or mock-only decision; do not authorize the extra repository yourself.
