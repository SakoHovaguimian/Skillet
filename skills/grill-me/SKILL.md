---
name: grill-me
description: Relentlessly stress-test a plan, product decision, technical design, or architecture before action. Build a dependency-aware decision tree, investigate discoverable facts, and interview the user in focused rounds that resolve every currently unblocked decision. Use when the user asks to be grilled, challenged, pressure-tested, interviewed, or guided through unresolved requirements, trade-offs, dependencies, risks, and edge cases. Do not act on the resulting plan until the user confirms that shared understanding has been reached.
disable-model-invocation: true
---

# Grill Me

## Outcome

Turn an uncertain proposal into a decision-complete, mutually understood plan before anything is built or changed.

The finished plan should make clear:

* what is being achieved
* how success will be measured
* which decisions were made and why
* which facts are supported by evidence
* which assumptions remain
* what is included and excluded
* which risks are accepted
* what happens when things fail
* what action is authorized next

Grilling is not brainstorming and it is not passive clarification. It is a relentless interview that exposes ambiguity, dependency gaps, hidden scope, contradictory goals, and unhandled failure modes.

## Core Rules

1. Build a decision tree before driving the interview.
2. Ask questions in dependency-aware rounds, not one at a time.
3. In each round, ask the entire currently unblocked frontier.
4. Never ask the user for a fact the available environment can establish.
5. Give a recommended answer for every question.
6. Let each answer reshape the tree and unlock the next frontier.
7. Do not implement, modify, or execute the plan until the user explicitly confirms shared understanding.
8. Stop when the plan is actionable, not when every theoretical detail has been discussed.

## Establish Ground Truth

Before asking questions:

1. Read all applicable instructions and user-provided artifacts.
2. Inspect relevant code, documentation, configuration, interfaces, schemas, tests, history, analytics, operational evidence, and existing behavior.
3. Separate what the evidence proves from what it merely suggests.
4. Identify conflicts between code, documentation, current behavior, and stated intent.
5. Ask the user only for intent, preference, authority, prioritization, or facts that cannot be discovered from the environment.

Do not treat existing behavior as inherently correct.

When sources disagree, record:

* the conflicting sources
* what each source implies
* the consequence of choosing either interpretation
* the decision required to resolve the conflict

## Build the Decision Tree

Represent the proposal as a tree of material decisions.

Each node should contain:

* `Decision` — the choice that must be resolved
* `Why it matters` — what changes based on the answer
* `Prerequisites` — parent decisions or facts required before it can be answered
* `Dependents` — downstream decisions affected by it
* `State` — its current resolution state
* `Resolution` — the evidence, answer, assumption, or deferral that closed it
* `Confidence` — when the resolution is inferred rather than explicit

The tree should capture real dependencies.

For example:

```text
Objective
├── Primary user
│   ├── Permission model
│   ├── Visibility rules
│   └── Success metric
├── Source of truth
│   ├── Conflict behavior
│   ├── Offline behavior
│   └── Migration strategy
└── Delivery model
    ├── Failure recovery
    ├── Observability
    └── Rollout
```

Do not force every topic into a strict hierarchy when dependencies cross branches. Record cross-dependencies explicitly.

## Decision States

Every material decision must have one state:

* `Unresolved` — known decision that has not been answered
* `Researching` — discoverable fact is being investigated
* `Evidence` — resolved directly from available evidence
* `Decided` — explicitly chosen by the user
* `Assumed` — provisionally chosen, with consequence and confidence
* `Deferred` — intentionally postponed, with an owner or trigger
* `Out of scope` — deliberately excluded
* `Blocked` — cannot progress without missing authority or information

A node is ready for questioning only when all of its prerequisites are settled.

## Determine the Frontier

The frontier is the complete set of unresolved decisions that can be answered now without guessing about unresolved prerequisites.

For every round:

1. Recalculate the decision tree.
2. Resolve anything discoverable through evidence.
3. Mark decisions waiting on research as `Researching`.
4. Identify every user decision whose prerequisites are settled.
5. Ask that entire frontier in one round.

Do not ask downstream questions prematurely.

Do not serialize independent questions unnecessarily. If five decisions are ready, ask all five in the same round.

Keep rounds focused enough that the user can answer clearly. When the frontier is unusually large, group it by closely related branches without hiding dependencies.

## Research Without Blocking the Interview

When a question can be settled from the environment, investigate it instead of asking the user.

Examples include:

* existing code behavior
* established naming or architecture conventions
* schema and API contracts
* current configuration
* platform requirements
* test coverage
* documented product rules
* operational limits
* compatibility constraints
* historical implementation decisions

Independent research must not block unrelated user decisions.

When the environment supports parallel research agents, delegate independent investigations to them. While that research is in progress:

* continue asking frontier questions that do not depend on its result
* hold only the downstream branches that require that evidence
* integrate the result into the next tree update
* surface uncertainty when the research is incomplete or conflicting

Never describe unavailable or unfinished research as established fact.

## Start the Interview

Begin by providing:

### Current Understanding

Restate the proposal in one to three sentences without expanding its scope.

### Objective

State the apparent objective and measurable success criteria. Clearly label anything inferred.

### Decision Map

Summarize the major branches of the current decision tree.

### Round 1

Ask every decision on the current frontier.

## Question Format

Each question must resolve one decision.

Use:

```text
1. [Decision-focused question]

Recommended answer: [Clear recommendation and brief rationale.]
Main trade-off: [Only include when it could materially change the choice.]
```

Rules:

* Ask concrete questions the user can directly answer.
* Include mutually exclusive options when useful.
* Do not combine separate decisions into one question.
* Do not ask abstract questions such as “What do you want?” when concrete choices can be named.
* Do not repeat questions already answered by evidence or prior responses.
* Recommend one answer rather than neutrally listing possibilities.
* Prefer the smallest option that satisfies the objective while preserving future change.
* Let strong repository or product evidence outweigh generic convention.
* State uncertainty instead of inventing precision.
* Use a scenario or counterexample when vague language hides an edge case.

## Process Each Round

After the user responds:

1. Map every answer to the relevant decision node.
2. Record explicit choices as `Decided`.
3. Separate firm decisions from tentative preferences.
4. Detect answers that are vague, contradictory, incomplete, or non-actionable.
5. Update affected downstream branches.
6. Remove branches made irrelevant by earlier answers.
7. Add newly exposed decisions, risks, and dependencies.
8. Incorporate completed research.
9. Recalculate the frontier.
10. Ask the next full round.

Show only meaningful changes between rounds:

* decisions closed
* branches added or removed
* conflicts discovered
* assumptions introduced
* research findings that changed the plan
* the next frontier

Do not repeat the entire ledger after every response.

## Challenge Weak Answers

Do not silently accept answers that fail to resolve the decision.

Challenge answers that are:

* vague
* internally inconsistent
* incompatible with the stated objective
* dependent on an undefined term
* impossible under known constraints
* missing ownership
* missing failure behavior
* based on an unsupported assumption
* broader or narrower than the claimed scope

State:

1. what remains unresolved
2. why it matters
3. the closest viable interpretation
4. the decision needed from the user

When appropriate, offer a recommended correction rather than merely pointing out the problem.

## Detect Hidden Conflicts

Surface conflicts as soon as they become visible.

Look specifically for:

* incompatible goals or success metrics
* unclear users, actors, or ownership boundaries
* terminology that changes meaning across branches
* authorization and permission gaps
* contract or schema ambiguity
* missing state transitions or lifecycle behavior
* unclear source of truth
* concurrency and conflict-resolution gaps
* missing cancellation, retry, timeout, idempotency, or recovery behavior
* destructive operations without safeguards
* privacy, security, accessibility, performance, or compliance risks
* migration and backward-compatibility omissions
* rollout without observability or rollback
* edge cases that contradict the happy path
* scope claims that understate the dependency footprint

For each conflict, provide:

```text
Conflict: [What is inconsistent.]
Evidence: [What exposed it.]
Consequence: [What breaks or remains ambiguous.]
Recommended resolution: [Closest viable answer.]
```

## Decision Priority

Prioritize branches in this order when constructing the tree and recommendations:

1. Objective and measurable success
2. Primary users, actors, and authority
3. Irreversible or high-blast-radius decisions
4. Security, privacy, data loss, and migration
5. Parent decisions that collapse downstream branches
6. External contracts and ownership boundaries
7. State, lifecycle, and failure behavior
8. Rollout, observability, verification, and recovery
9. Reversible implementation choices
10. Cosmetic preferences

Skip categories that do not materially apply.

## Maintain the Decision Ledger

Keep a compact internal ledger throughout the interview.

Each entry should include:

```text
Decision:
State:
Resolution:
Source or owner:
Consequence:
Dependents:
```

During the interview, show only ledger changes.

At completion, show the full material ledger grouped into:

* evidence-backed facts
* explicit decisions
* accepted assumptions
* deferred decisions
* out-of-scope branches
* remaining risks

## Shared-Understanding Gate

Do not treat the interview as complete merely because all questions have answers.

Before requesting confirmation:

1. Check that every material branch is resolved.
2. Verify that no `Blocked` decision prevents action.
3. Confirm that terms are used consistently.
4. Confirm that the success criteria match the chosen design.
5. Confirm that included scope, exclusions, risks, and recovery behavior are explicit.
6. Confirm that no answer relies on an unresolved prerequisite.
7. Confirm that the proposed next action matches the authority the user has granted.

Then present a shared-understanding summary.

## Final Shared-Understanding Summary

Return:

### Objective and Success

The intended outcome and measurable success criteria.

### Final Design

A concise explanation of how the chosen plan works.

### Decisions and Evidence

Every material decision, its resolution, and the supporting evidence or user answer.

### Assumptions

Every remaining assumption, its consequence, and confidence.

### Scope

What is included.

### Non-Goals

What is deliberately excluded.

### Deferred Decisions

What remains postponed, who owns it, and what triggers reconsideration.

### Risks and Recovery

Remaining risks, detection methods, rollback, retry, migration, or recovery paths.

### Next Action

The first concrete action that would follow confirmation.

### Confirmation

Ask:

> Does this accurately represent our shared understanding, or is any decision, assumption, scope boundary, or risk still wrong or incomplete?

## Writing hygiene

When this skill is used standalone, invoke `$unslop` once after each complete user-facing interview artifact is drafted, including a round, conflict record, ledger update, or final shared-understanding summary. If a parent workflow owns the final artifact, let that outermost workflow make the single `$unslop` pass instead of running it twice.

Preserve decision-state labels, code, paths, symbols, commands, quoted user answers, evidence anchors, and the decision structure. `$unslop` may improve prose, but it must not change the decision, introduce scope, or weaken the authorization gate.

## Authorization Gate

Do not implement, edit files, generate production artifacts, execute commands, create tickets, or otherwise act on the plan until the user explicitly confirms the shared understanding.

Confirmation of the plan authorizes only the next action when:

* the user already requested implementation as part of the original task, or
* the user explicitly authorizes implementation after reviewing the summary

Otherwise, return the decision-complete plan without implying that execution has been approved.
