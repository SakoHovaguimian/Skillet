---
name: conversational-planning-grill-me
description: Produce an implementation-ready plan for a repository or technical/product change through evidence-first discovery and a focused conversational decision interview. Use before coding when requirements, boundaries, risks, or trade-offs need to be resolved. This stack-neutral skill does not depend on iOS, SwiftUI, Rune, or ubiquitous-component catalogs.
disable-model-invocation: true
---

# Conversational planning + grill me

## Outcome

Turn a rough request into a current, evidence-backed implementation plan that another agent can execute without rediscovering product intent or making material design choices.

Compose `$grill-me` as the interview engine. Do not copy or weaken its decision tree, frontier questions, decision ledger, conflict handling, or completion gate.

## Phase 1: Discover before interviewing

Read, in order when present:

1. Applicable `AGENTS.md` files and explicit user constraints.
2. Project context, domain, architecture, product, and decision documents.
3. Relevant models and contracts, then services, integrations, state owners, routing, and UI or other presentation code.
4. Tests, fixtures, examples, generated artifacts, analytics, flags, migrations, and recent history that clarify intended behavior.
5. Nearby implementation exemplars and formatter, linter, or validation configuration.

Use `rg` and targeted reads. Avoid broad repository dumps. Follow imports and call sites only until each planning branch has enough evidence.

Do not require or invent iOS, SwiftUI, Rune, or ubiquitous-component guidance. Read repository-specific conventions when the project actually provides and needs them, but keep this workflow usable for any stack.

## Phase 2: Build the initial planning model

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

Invoke `$grill-me` and follow its interview rules exactly. Let repository evidence settle discoverable facts, ask the user only for intent or authority, and keep the interview open until the decision-complete shared-understanding gate is satisfied.

## Phase 4: Produce the executable plan

Make the final plan proportionate to risk and include:

- objective, success criteria, and non-goals
- chosen approach and rejected alternatives that matter
- exact systems and likely files to create, modify, move, or remove
- data, API, state, lifecycle, concurrency, and failure behavior when applicable
- compatibility, migration, rollout, observability, and rollback when applicable
- accessibility, localization, privacy, security, and performance when applicable
- verification strategy consistent with repository instructions and user authorization
- documentation updates required after implementation
- decision ledger, assumptions, deferrals, and remaining risks

Use paths and symbols as anchors when known. Mark speculative file paths as likely rather than guaranteed.

## Approval gate

Restate the complete current plan once after all material branches close. Then stop and request explicit approval of that exact plan.

Do not treat agreement with an earlier draft, generic enthusiasm, or a request to keep planning as implementation approval. Do not edit implementation files during this skill unless the user explicitly changes the task.

## Writing hygiene

For a standalone invocation, invoke `$unslop` once on the complete user-facing planning artifact after its technical content is final. If a parent workflow owns the final artifact, let the outermost workflow make the single `$unslop` pass instead of running it twice.

Preserve code, paths, symbols, commands, quoted user decisions, evidence anchors, decision-state labels, and plan structure. `$unslop` may improve prose, but it must not change technical meaning, introduce decisions, or weaken the approval gate.

## Implementation handoff

After approval, use the most specific available implementation skill for the repository or execute the approved plan directly. Carry the final plan, decision ledger, constraints, verification limits, and unresolved risks into that handoff.

Never silently reopen an approved product decision during implementation. Surface new contradictory evidence instead.
