---
name: grill-me
description: Pressure-test a proposal and return a decision-complete, actionable summary. Use when asked for a challenging interview about requirements, design choices, dependencies, or risks. Do not use for routine clarification or direct implementation.
disable-model-invocation: true
---

# Grill Me

## Outcome

Turn an uncertain proposal into a sufficiently resolved, mutually understood plan before anything is built or changed.

The finished plan should make clear:

- what is being achieved
- how success will be measured
- which decisions were made and why
- which facts are supported by evidence
- which assumptions remain
- what is included and excluded
- which risks are accepted
- what happens when things fail
- what action is authorized next

Grilling is not brainstorming and it is not passive clarification. It is a rigorous interview that exposes ambiguity, dependency gaps, hidden scope, contradictory goals, and unhandled failure modes.

The objective is not to eliminate every possible uncertainty. It is to resolve the decisions that materially affect the next authorized action.

## Inputs and preconditions

A proposal, plan, design, or decision to stress-test, and a user available to answer interview rounds.

Before asking anything, establish ground truth:

1. Reuse evidence passed by the parent or already collected in this task. Read applicable instructions and user-provided artifacts needed to resolve remaining material decisions.
2. Inspect relevant code, documentation, configuration, interfaces, schemas, tests, history, analytics, operational evidence, and existing behavior.
3. Separate what the evidence proves from what it merely suggests.
4. Identify conflicts between code, documentation, current behavior, and stated intent.
5. Ask the user only for intent, preference, authority, prioritization, or facts that cannot be discovered from the environment.

Do not treat existing behavior as inherently correct.

When sources disagree, record:

- the conflicting sources
- what each source implies
- the consequence of choosing either interpretation
- the decision required to resolve the conflict

## Workflow

### Build the decision tree

Represent the proposal as a tree of material decisions.

Each node should contain:

- `Decision` — the choice that must be resolved
- `Why it matters` — what changes based on the answer
- `Prerequisites` — parent decisions or facts required before it can be answered
- `Dependents` — downstream decisions affected by it
- `State` — its current resolution state
- `Resolution` — the evidence, answer, assumption, or deferral that closed it
- `Confidence` — when the resolution is inferred rather than explicit

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

### Decision states

Every tracked material decision must have one state:

- `Unresolved` — known decision that has not been answered
- `Researching` — discoverable fact is being investigated
- `Evidence` — resolved directly from available evidence
- `Decided` — explicitly chosen by the user
- `Assumed` — provisionally chosen, with consequence and confidence
- `Deferred` — intentionally postponed, with an owner or trigger
- `Out of scope` — deliberately excluded
- `Blocked` — cannot progress without missing authority or information

A node is ready for questioning only when all of its prerequisites are settled.

Not every tracked decision must be resolved before the interview ends. Only decisions that materially affect the next authorized action must be sufficiently settled.

### Determine the frontier

The frontier is the set of unresolved decisions that can be answered now without guessing about unresolved prerequisites.

The frontier determines which questions are eligible, not how many must be asked.

For every round:

1. Recalculate the decision tree.
2. Resolve anything discoverable through evidence.
3. Mark decisions waiting on research as `Researching`.
4. Identify user decisions whose prerequisites are settled.
5. Rank eligible decisions by impact, risk, irreversibility, and their ability to unlock downstream decisions.
6. Select the highest-priority 3–5 decisions for the current round.
7. Keep remaining eligible decisions available for subsequent rounds.

Do not ask the entire frontier.

Do not ask downstream questions prematurely.

Do not serialize independent questions unnecessarily, but do not overwhelm the user with every eligible decision.

A round may contain fewer than three questions when only one or two material decisions require attention.

When selecting questions, prefer those that:

- could materially change the design or scope
- address irreversible or high-risk choices
- unlock important downstream branches
- resolve contradictory objectives or requirements
- eliminate large amounts of unnecessary future questioning

Avoid spending interview rounds on low-impact details when higher-impact uncertainty remains.

### Research without blocking the interview

When a question can be settled from the environment, investigate it instead of asking the user.

Examples include:

- existing code behavior
- established naming or architecture conventions
- schema and API contracts
- current configuration
- platform requirements
- test coverage
- documented product rules
- operational limits
- compatibility constraints
- historical implementation decisions

Independent research must not block unrelated user decisions.

When the environment supports parallel research agents, delegate independent investigations to them.

While research is in progress:

- continue asking selected high-priority questions that do not depend on its result
- hold only downstream branches that require that evidence
- integrate the result into the next tree update
- surface uncertainty when research is incomplete or conflicting

Never describe unavailable or unfinished research as established fact.

### Start the interview

Begin by providing:

1. **Current understanding.** Restate the proposal in one to three sentences without expanding its scope.
2. **Objective.** State the apparent objective and measurable success criteria. Clearly label anything inferred.
3. **Decision map.** Summarize the major branches of the current decision tree.
4. **Round 1.** Ask the highest-priority 3–5 eligible questions.

Do not dump the entire decision tree or question queue unless the user requests it.

### Question format

Each question must resolve one decision.

Use:

```text
1. [Decision-focused question]

Recommended answer: [Clear recommendation and brief rationale.]
Main trade-off: [Only include when it could materially change the choice.]
```

Rules:

- Ask concrete questions the user can directly answer.
- Include mutually exclusive options when useful.
- Do not combine separate decisions into one question.
- Do not ask abstract questions such as "What do you want?" when concrete choices can be named.
- Do not repeat questions already answered by evidence or prior responses.
- Recommend one answer rather than neutrally listing possibilities.
- Prefer the smallest option that satisfies the objective while preserving future change.
- Let strong repository or product evidence outweigh generic convention.
- State uncertainty instead of inventing precision.
- Use a scenario or counterexample when vague language hides an edge case.

Recommendations should be defensible, not designed merely to obtain agreement.

When a significant counterargument exists, explain it briefly.

### Process each round

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
10. Evaluate whether the actionability stopping condition has been met.
11. If more questioning is necessary, select the next highest-priority 3–5 eligible decisions.

Show only meaningful changes between rounds:

- decisions closed
- branches added or removed
- conflicts discovered
- assumptions introduced
- research findings that changed the plan
- the next selected questions

Do not repeat the entire ledger after every response.

Do not continue asking questions merely because unresolved branches still exist.

### Challenge weak answers

Do not silently accept answers that fail to resolve a decision that materially affects the next action.

Challenge answers that are:

- vague
- internally inconsistent
- incompatible with the stated objective
- dependent on an undefined term
- impossible under known constraints
- missing ownership
- missing failure behavior
- based on an unsupported assumption
- broader or narrower than the claimed scope

State:

1. what remains unresolved
2. why it matters
3. the closest viable interpretation
4. the decision needed from the user

When appropriate, offer a recommended correction rather than merely pointing out the problem.

Do not prolong the interview to challenge ambiguity that has no material effect on the next authorized action.

### Detect hidden conflicts

Surface conflicts as soon as they become visible.

Look specifically for:

- incompatible goals or success metrics
- unclear users, actors, or ownership boundaries
- terminology that changes meaning across branches
- authorization and permission gaps
- contract or schema ambiguity
- missing state transitions or lifecycle behavior
- unclear source of truth
- concurrency and conflict-resolution gaps
- missing cancellation, retry, timeout, idempotency, or recovery behavior
- destructive operations without safeguards
- privacy, security, accessibility, performance, or compliance risks
- migration and backward-compatibility omissions
- rollout without observability or rollback
- edge cases that contradict the happy path
- scope claims that understate the dependency footprint

For each material conflict, provide:

```text
Conflict: [What is inconsistent.]
Evidence: [What exposed it.]
Consequence: [What breaks or remains ambiguous.]
Recommended resolution: [Closest viable answer.]
```

### Decision priority

Prioritize branches in this order when constructing the tree, selecting questions, and making recommendations:

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

Use this order as guidance, not a rigid sorting algorithm. A lower-ranked decision may take priority when it blocks the next authorized action.

### Maintain the decision ledger

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

During the interview, show only meaningful ledger changes.

At completion, group relevant decisions into:

- evidence-backed facts
- explicit decisions
- accepted assumptions
- deferred decisions
- out-of-scope branches
- remaining risks
- unresolved decisions, if any

Unresolved decisions must not silently disappear from the final summary.

### Actionability stopping condition

Do not treat the interview as complete merely because the user has answered a certain number of questions.

Do not require the entire decision tree to be resolved.

The interview is complete when remaining uncertainty does not materially affect the next authorized action.

Before stopping:

1. Identify the next concrete action.
2. Verify that its necessary prerequisites and decisions are sufficiently resolved.
3. Confirm that no unresolved authority, safety, security, data-loss, or other critical constraint blocks that action.
4. Verify that the objective and success criteria are sufficiently clear to guide the action.
5. Confirm that scope and non-goals are clear enough to prevent material implementation ambiguity.
6. Record remaining assumptions with their consequences and confidence.
7. Record deferred decisions with an owner or trigger for reconsideration.
8. Record remaining risks and appropriate detection, mitigation, or recovery expectations.
9. Verify that unresolved downstream decisions can safely wait without forcing a material redesign of the next action.

A decision may remain unresolved when:

- it does not affect the next action
- it can be addressed safely during a later phase
- its resolution is reversible and low-risk
- it is intentionally deferred with a clear trigger
- the next action is explicitly intended to gather evidence needed to resolve it

Do not classify a decision as harmless merely to finish the interview. If resolving it could materially alter scope, architecture, safety, cost, or the next action, continue questioning or mark the action blocked.

Once the stopping condition is satisfied, stop asking questions and produce the final shared-understanding summary.

The goal is an actionable plan with transparent uncertainty, not exhaustive certainty about every theoretical branch.

### Shared-understanding gate

Before requesting confirmation:

1. Verify that the actionability stopping condition is satisfied.
2. Confirm that terms are used consistently where they affect the next action.
3. Confirm that success criteria match the chosen approach.
4. Confirm that material scope boundaries, risks, and recovery expectations are explicit.
5. Confirm that assumptions and deferrals are visible rather than silently treated as facts.
6. Confirm that the proposed next action matches the authority the user has granted.

Then return the final summary to the parent workflow, or present it for confirmation when used standalone.

## Constraints

1. Build a decision tree before driving the interview.
2. Ask questions in bounded, dependency-aware rounds.
3. Ask the highest-priority 3–5 eligible decisions per round, not the entire frontier.
4. Never ask the user for a fact the available environment can establish.
5. Give a recommended answer for every question.
6. Let each answer reshape the tree and unlock downstream decisions.
7. Do not implement, modify, or execute the plan until the user explicitly confirms shared understanding.
8. Stop when remaining uncertainty cannot materially affect the next authorized action.
9. Record unresolved assumptions, deferrals, and material risks rather than forcing unnecessary decisions.
10. Never substitute assumptions for missing authority or critical safety requirements.

### Authorization gate

Read-only investigation needed to resolve the proposal may proceed before confirmation, subject to the user's scope and repository restrictions.

Do not implement the plan, modify project files, create external artifacts, or perform external writes before the required confirmation.

When invoked by a parent planning workflow, return the actionable decision ledger to that parent. The parent owns the single final confirmation.

When used standalone, present the final summary and request confirmation.

Confirmation authorizes implementation only when the user has requested implementation. It does not authorize external messages, deployment, destructive operations, or production access beyond the scope explicitly granted.

## Failure handling

- **Blocked decision:** Pause only actions dependent on that decision. Continue independent investigation and questioning. If the blocked decision prevents the next action, do not declare the plan actionable.
- **Incomplete or conflicting research:** Present the conflict record and mark the affected branches. Do not present unfinished research as established fact.
- **User stops responding:** Deliver the current ledger with every material open decision labeled, so the interview can resume without loss.
- **Remaining non-blocking uncertainty:** Record it as an assumption, deferral, or risk. Do not continue interviewing solely to eliminate uncertainty that cannot materially affect the next authorized action.
- **No useful questions remain but an action is blocked:** Return the blocker and the information or authority required. Do not manufacture a resolution.

## Output contract

The final shared-understanding summary contains, in order:

1. **Objective and success.** The intended outcome and measurable success criteria.
2. **Final design.** A concise explanation of how the chosen plan works.
3. **Decisions and evidence.** Material decisions needed for the next action, their resolutions, and supporting evidence or user answers.
4. **Assumptions.** Remaining assumptions, their consequences, and confidence.
5. **Scope.** What is included.
6. **Non-goals.** What is deliberately excluded.
7. **Deferred decisions.** What remains postponed, who owns it, and what triggers reconsideration.
8. **Risks and recovery.** Remaining risks, detection methods, rollback, retry, migration, or recovery paths where applicable.
9. **Next action.** The first concrete action that would follow confirmation, including any remaining conditions.
10. **Confirmation.** When standalone, request confirmation. When composed, return the summary to the parent for its single final confirmation.

When standalone, ask:

> Does this accurately represent our shared understanding for the next action, or is any material decision, assumption, scope boundary, or risk still wrong or incomplete?
