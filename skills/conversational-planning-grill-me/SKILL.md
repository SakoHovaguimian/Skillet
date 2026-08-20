---
name: conversational-planning-grill-me
description: Produce an implementation-ready plan for a repository or technical/product change through evidence-first discovery and a focused conversational decision interview. Use when requirements, boundaries, risks, or trade-offs need to be resolved before coding. Do not use for iOS-specific planning when `$ios-conversational-planning-grill-me` applies; this stack-neutral skill does not depend on iOS, SwiftUI, Rune, or ubiquitous-component catalogs.
disable-model-invocation: true
---

# Conversational Planning + Grill Me

## Outcome

Turn a rough request into a current, evidence-backed implementation plan that another agent can execute without rediscovering product intent or making material design choices.

This skill owns discovery, the planning model, the executable plan, and the approval gate. It composes `$grill-me` as the interview engine and must not copy or weaken that engine's decision tree, frontier questions, decision ledger, conflict handling, or completion gate.

## Inputs and preconditions

A change request and access to the repository or artifacts it concerns. If the request names no repository and none is available, plan from the provided artifacts and label every unverifiable claim as an assumption.

## Workflow

### 1. Discover before interviewing

Read, in order when present:

1. Applicable `AGENTS.md` files and explicit user constraints.
2. Project context, domain, architecture, product, and decision documents.
3. Relevant models and contracts, then services, integrations, state owners, routing, and UI or other presentation code.
4. Tests, fixtures, examples, generated artifacts, analytics, flags, migrations, and recent history that clarify intended behavior.
5. Nearby implementation exemplars and formatter, linter, or validation configuration.

Use `rg` and targeted reads. Avoid broad repository dumps. Follow imports and call sites only until each planning branch has enough evidence.

Do not require or invent iOS, SwiftUI, Rune, or ubiquitous-component guidance. Read repository-specific conventions when the project actually provides and needs them, but keep this workflow usable for any stack.

### 2. Build the initial planning model

Before the first question, summarize:

- the objective and observable success condition
- confirmed current behavior
- affected bounded context and canonical terminology
- likely change surface
- hard constraints from instructions or contracts
- the highest-leverage unresolved decision

Label claims as `Evidence`, `Inference`, or `Open decision`. Do not present inference as fact.

Read [references/plan-readiness.md](references/plan-readiness.md) once a repository-backed plan is confirmed. Apply only the lenses relevant to the task.

### 3. Run the interview

Invoke `$grill-me` and follow its interview rules exactly. Let repository evidence settle discoverable facts, ask the user only for intent or authority, and keep the interview open until the decision-complete shared-understanding gate is satisfied.

### 4. Produce the executable plan

Make the final plan proportionate to risk, using the output contract below. Use paths and symbols as anchors when known. Mark speculative file paths as likely rather than guaranteed.

### 5. Approval gate

Restate the complete current plan once after all material branches close. Then stop and request explicit approval of that exact plan.

### 6. Implementation handoff

After approval, use the most specific available implementation skill for the repository or execute the approved plan directly. Carry the final plan, decision ledger, constraints, verification limits, and unresolved risks into that handoff.

Never silently reopen an approved product decision during implementation. Surface new contradictory evidence instead.

## Constraints

- Do not treat agreement with an earlier draft, generic enthusiasm, or a request to keep planning as implementation approval.
- Do not edit implementation files during this skill unless the user explicitly changes the task.
- Do not present inference as fact; every claim keeps its `Evidence`, `Inference`, or `Open decision` label until resolved.

## Composition

<interface>
| Invokes | When | Carries in | Expects back | If unavailable |
| --- | --- | --- | --- | --- |
| `$grill-me` | Step 3, after the initial planning model exists | The planning model, evidence anchors, constraints, and open decisions | A decision-complete ledger and confirmed shared understanding | Run a reduced interview inline, state that the full engine was unavailable, and keep the approval gate |
| `$unslop` | Once, on the complete planning artifact, only when no parent workflow owns the final artifact | The complete drafted plan | The prose-improved plan with structure intact | Skip the pass and deliver the plan unchanged |
| Repository implementation skill (most specific available) | After explicit approval, at handoff | Final plan, decision ledger, constraints, verification limits, unresolved risks | Implementation consistent with the approved plan | Execute the approved plan directly |
</interface>

Invoke `$unslop` once on the complete user-facing artifact after its technical content is final, unless a parent workflow owns the final artifact, in which case the outermost workflow makes the single pass. `$unslop` may improve prose but must not change technical meaning: preserve code, paths, symbols, commands, measurements, quoted decisions, evidence anchors, classification labels, and document structure. If `$unslop` is unavailable, deliver the artifact unchanged and note the skipped pass. In this skill, the pass must also not introduce decisions or weaken the approval gate.

## Failure handling

- Evidence contradicts the user's stated intent: surface the conflict as a `$grill-me` conflict record; never silently prefer either side.
- Discovery cannot reach needed code or documents: mark the affected plan branches as assumption-based and say what access would resolve them.
- The user requests implementation before the gate: restate the gate, present what remains unresolved, and proceed only on explicit approval of the current plan.

## Output contract

The final plan includes, proportionate to risk:

- objective, success criteria, and non-goals
- chosen approach and rejected alternatives that matter
- exact systems and likely files to create, modify, move, or remove
- data, API, state, lifecycle, concurrency, and failure behavior when applicable
- compatibility, migration, rollout, observability, and rollback when applicable
- accessibility, localization, privacy, security, and performance when applicable
- verification strategy consistent with repository instructions and user authorization
- documentation updates required after implementation
- decision ledger, assumptions, deferrals, and remaining risks
