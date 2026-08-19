---
name: conversational-planning-grill-me
description: Produce an implementation-ready plan through repository discovery followed by a conversational, one-question-at-a-time decision interview. Use when planning or pressure-testing a non-trivial feature, refactor, migration, integration, or rollout before coding, especially in Nudge-iOS, Grimoire, or Rune projects with ubiquitous-language, business-logic, architecture, or implementation-protocol constraints. Stop at a final approval gate before implementation.
disable-model-invocation: true
---

# Conversational Planning + Grill Me

## Outcome

Convert a rough request into a current, evidence-backed implementation plan that another agent can execute without rediscovering product intent or making material design choices.

Compose `$grill-me` as the interview engine. Do not copy or weaken its question loop, decision ledger, conflict handling, or completion gate here.

## Phase 1: Discover Before Interviewing

Read, in order when present:

1. Applicable `AGENTS.md` files and explicit user constraints.
2. `docs/UBIQUITOUS_LANGUAGE*` and `docs/UBIQUITOUS_BUSINESS_LOGIC*`.
3. `CONTEXT.md`, `CONTEXT-MAP.md`, ADRs, architecture docs, and feature notes.
4. Relevant models and contracts, then services, DI, navigation, state owners, and UI.
5. Tests, fixtures, previews, analytics, flags, migrations, and recent history that clarify intended behavior.
6. Nearby implementation exemplars and formatter/linter configuration.

Use `rg` and targeted reads. Avoid broad repository dumps. Follow imports and call sites only until each planning branch has enough evidence.

Treat domain docs as domain authority, not infallible snapshots. When docs and executable behavior differ, report both with source anchors and make reconciliation an explicit decision.

## Phase 2: Build the Initial Planning Model

Before the first question, summarize:

- the objective and observable success condition
- confirmed current behavior
- affected bounded context and canonical terminology
- likely change surface
- hard constraints from instructions or contracts
- the highest-leverage unresolved decision

Label claims as `Evidence`, `Inference`, or `Open decision`. Do not present inference as fact.

Read [references/plan-readiness.md](references/plan-readiness.md) once a repository-backed plan is confirmed. Apply only the lenses relevant to the task.

## Phase 3: Run `$grill-me`

Invoke `$grill-me` and follow its one-question loop exactly.

Prioritize product behavior and boundaries before implementation mechanics. Resolve contradictions with evidence, not deference. When a user answer conflicts with an instruction, contract, or invariant, explain the impact and recommend the closest viable alternative.

Compose `$grill-with-docs` only when the user also requests live glossary, context-map, or ADR maintenance. Otherwise keep discovery read-only and list documentation changes in the final plan.

Update the visible plan only when a decision materially changes it. Avoid repeating the full plan after every answer.

## Phase 4: Produce the Executable Plan

Make the final plan proportionate to risk and include:

- objective, success criteria, and non-goals
- chosen approach and rejected alternatives that matter
- exact systems and likely files to create, modify, move, or remove
- data, API, state, lifecycle, concurrency, and failure behavior
- compatibility, migration, rollout, observability, and rollback when applicable
- accessibility, localization, privacy, security, and performance when applicable
- verification strategy consistent with repository instructions and user authorization
- documentation updates required after implementation
- decision ledger, assumptions, deferrals, and remaining risks

Use paths and symbols as anchors when known. Mark speculative file paths as likely rather than guaranteed.

## Approval Gate

Restate the complete current plan once after all material branches close. Then stop and request explicit approval of that exact plan.

Do not treat agreement with an earlier draft, generic enthusiasm, or a request to keep planning as implementation approval. Do not edit implementation files during this skill unless the user explicitly changes the task.

## Implementation Handoff

After approval:

- For a Nudge-iOS, Grimoire, or Rune-backed SwiftUI implementation, invoke `$project-rune-implementation-protocol` with the approved plan and preserve all repository instructions.
- For another stack, use the most specific available implementation skill or execute the approved plan directly.
- Invoke `$swift-sako-semantic-linter` after in-scope Rune Swift/SwiftUI edits.
- Invoke `$swift-6-concurrency` when the approved work materially changes isolation, `Sendable`, tasks, actors, or async control flow.

The handoff must carry the final plan, decision ledger, constraints, verification limits, and unresolved risks. Never silently reopen an approved product decision during implementation; surface new contradictory evidence instead.
