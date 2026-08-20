---
name: project-rune-implementation-protocol
description: Implement SwiftUI features with architecture parity and Rune-first composition. Use when building screens, navigation-created ViewModels, flows, services, APIs, DI, routes, analytics, mocks, previews, or batch features in projects that follow the Rune/Grimoire patterns. Do not restate coding rules here; all Swift, screen, lifecycle, concurrency, Rune, and parity rules belong to `$swift-sako-semantic-linter`.
disable-model-invocation: true
---

# Project Rune Implementation Protocol

## Outcome

The requested vertical feature is delivered with current-project architecture and Rune parity.

- This protocol owns discovery, Pattern Lock, planning, implementation order, and final integration accounting.
- `$swift-sako-semantic-linter` owns all coding and enforcement rules. It is invoked before coding to load the applicable rule modules and after coding to scan touched Swift files.
- Do not duplicate linter rules here. If the contracts conflict, explicit user/repository instructions win; otherwise the linter is authoritative.

## Inputs and preconditions

A feature request (single or batch) and a project that follows the Rune/Grimoire patterns. Locate the primary `.xcodeproj` and actual app source root before anything else; if none exists, stop and report that this protocol does not apply.

## Workflow

### 1. Resolve project authority

1. Read applicable `AGENTS.md` and project documentation.
2. Invoke `$ubiquitous-components-fetch` to import the shared Rune catalog.
3. Inspect only authorities applicable to the request:
   - 2–3 recent nearby screens, ViewModels, and components
   - global imports and active style/theme authority
   - navigation service, route family, destinations, sheets, and covers
   - ViewModel/Trackable protocols and analytics `ScreenEvent`
   - live/mock DI, mock resolver, and preview conventions
   - service/API protocols, live/mock endpoints, and fixtures
   - centralized domain permission helpers
4. Invoke `$swift-sako-semantic-linter` as a preflight and load the rule-module union for the planned surfaces.

Use targeted catalog search for the needed UI category; do not load the entire Rune catalog when a focused query is sufficient.

### 2. Lock patterns before editing

Return a compact Pattern Lock table covering only applicable surfaces: local exemplar, route/setup, lifecycle/analytics, DI/mock/preview, service/API, Rune components/style/media, async/loading, and file placement. Record exceptions instead of silently inventing a new pattern.

For multiple features, create one batch plan, identify shared infrastructure, and implement dependency-first. For each feature map:

- files to create or update
- models and ownership boundaries
- route, destination, and ViewModel setup
- lifecycle and analytics
- live/mock DI and preview resolver
- protocol/live/mock API and fixtures when applicable
- Rune components, active style, images, and custom-component gaps

### 3. Implement the vertical slice

1. Add or update focused models and contracts.
2. Implement services/API and realistic mocks when required.
3. Wire live DI, mock DI, and mock resolution.
4. Implement the ViewModel and route/context setup.
5. Add analytics and lifecycle behavior.
6. Implement the Rune-first screen and extracted views.
7. Wire routes/destinations and previews.
8. Check project membership, filenames, headers, and ownership.

Match recent local architecture and formatter output. Reuse project wrappers before lower-level Rune primitives. Add a custom reusable component only when the catalog and nearby code show a real gap; place it in the project component area and record a concise Rune Gap Justification.

### 4. Enforce and verify

Invoke `$swift-sako-semantic-linter` on every touched Swift file with its compact diff-scoped scan. Apply all applicable linter modules and resolve every error or documented semantic exception. Use exact output only to investigate grouped findings.

Mark applicable integration surfaces `YES`, `NO`, or `N/A`:

- Pattern Lock and relevant Rune catalog search completed
- models/files have correct ownership and project membership
- route, destination, setup, lifecycle, and analytics are complete
- live DI, mock DI, resolver, preview, and fixtures remain compatible
- protocol, live API, and mock API remain compatible
- Rune components, active style, media, layout, and custom gaps are accounted for
- async work, loading, cancellation, and cleanup satisfy the linter contract
- compact semantic scan completed with no unresolved errors

## Constraints

- Do not expand the requested behavior.
- Do not run Xcode builds or tests unless explicitly authorized.
- After requested work, report existing files that merit splitting as optional follow-up; do not absorb them automatically.
- If the linter is unavailable, do not claim semantic compliance.

## Composition

<interface>
| Invokes | When | Carries in | Expects back | If unavailable |
| --- | --- | --- | --- | --- |
| `$swift-sako-semantic-linter` | Preflight (step 1) to load rule modules; post-implementation (step 4) on touched files | Planned surfaces, then the touched-file list and diff scope | The applicable rule contract, then the semantic scan report | Preserve local patterns, skip the compliance claim, and report the limitation |
| `$ubiquitous-components-fetch` | Step 1, before Pattern Lock | The workspace root | The shared Rune catalog available locally | Use local component docs and report the limitation |
</interface>

## Failure handling

- No `.xcodeproj` or recognizable Rune/Grimoire structure: stop and report that the protocol does not apply rather than forcing its patterns.
- A required pattern authority (navigation service, DI container, analytics protocol) cannot be found: record the gap in the Pattern Lock as an exception and match the closest local exemplar instead of inventing a pattern.
- Linter findings conflict with local evidence: current local evidence wins; record the conflict in the report.

## Output contract

Provide the Pattern Lock, implementation plan, files created/modified, Rune Gap Justifications, semantic-linter summary, integration checklist, exceptions, and verification limits.
