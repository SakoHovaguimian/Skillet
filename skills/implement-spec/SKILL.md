---
name: implement-spec
description: "Review an existing feature plan against current repository evidence and produce a self-contained implementation specification with readiness gates. Use when asked to check a plan's implementation readiness, add architecture and scope guardrails, or prepare an execution handoff after planning. Do not use for the initial product-planning interview, feature implementation, or review of an implemented diff."
disable-model-invocation: true
---

# Implement Spec

## Outcome

Produce one reviewed implementation specification that another agent can execute
without this conversation or installed skills. Preserve the source plan's concrete
feature detail and settled intent; add current evidence, local conventions,
decision boundaries, and execution gates. Own readiness review and the final
specification. Leave implementation to a later user instruction.

## Inputs and preconditions

Accept a plan from conversational planning or any other source. Inherit supplied
answers before asking questions. Obtain:

- The source plan, its identity/version, decision record, and actual approval
  evidence. Ask for the plan if unavailable; label missing approval evidence
  unknown rather than inferring consent from the plan's wording.
- Selected platforms: BE/API, Web, iOS, in any combination; exact editable
  repositories; reference-only projects; non-goals and deferred decisions.
  Discover readable repository facts and ask only about unresolved scope or
  targets. Confirm ambiguous candidates before treating them as editable.
- Implementation orchestration: inherit an explicit yes/no decision from the
  source plan or user instructions. If unknown, ask whether to use multi-agent
  orchestration for implementation; do not silently choose either mode or ask
  again once settled. Continue independent discovery while awaiting the answer,
  but settle it before the final execution package. If yes, prepare the worker
  handoffs required by the specification contract; if no, retain one implementation
  owner and omit the delegation section.
- Review delegation, off unless expressly authorized; requested model/reasoning
  settings, if any; and existing operational permissions. Keep review delegation
  separate from future implementation orchestration: permission for implementation
  workers does not authorize review workers.

Resolve supporting links relative to the directory containing this installed
`SKILL.md`, not the working directory or original repository checkout. Load the
references at their workflow steps; they are part of this skill's installed bundle.

## Workflow

1. Extract outcomes, workflows, acceptance criteria, accepted decisions, relevant
   rejected alternatives, deferred dependencies, and authorization. Separate
   user-approved choices from draft proposals. Classify review deltas as
   clarification, evidence correction, or material change. A material change
   alters scope, behavior, contracts, architecture, ownership, dependencies, or
   permissions; show the delta and obtain its decision before adopting it. Do not
   seek blanket reapproval of an unchanged approved plan.
2. Reuse still-current discovery. Verify relevant revisions and consequential
   local changes; inspect applicable AGENTS.md files, routed engineering/style/
   business guides, tooling configuration, nearest usable same-layer examples,
   their direct callers, and actual registration. Locate the real guides when an
   entry point is missing or boilerplate. Record exact paths and symbols. Read
   the selected sections of [Platform readiness](references/platform-readiness.md)
   and trace each workflow, including its relevant security boundaries.
3. Read [Specification contract](references/spec-contract.md). Build its Pattern
   Lock and a separate style/tooling profile for each target. Verify named
   artifacts or mark them proposed. Connect consequential implementation choices
   to lock rows. An existing example must actually fit the responsibility and
   current rules; shared template lineage does not establish compliance.
4. Resolve gaps with targeted questions, without restarting the product
   interview. For missing patterns or material contradictions, name affected lock
   rows, searched areas, nearest candidates and why they fail. Propose the
   smallest concrete resolution with files, responsibilities, interfaces, and a
   short illustrative sketch when useful. Ask at most three questions per batch,
   recommend a choice with its tradeoff, pause dependent work, and yield for an
   answer. Complete only independent read-only discovery before yielding; silence
   is not approval. Reopen settled decisions only on material new evidence.
5. Distinguish a new business entity following an established pattern from a new
   ownership, layering, data-flow, lifecycle, registration, caching, persistence,
   or component-composition pattern. Require approval for the latter; outcome
   approval alone does not supply it. For an approved new pattern, schedule one
   representative implementation and an update to the existing maintained guide
   before wider reuse. Keep upstream changes inside authorized repository scope.
6. Preserve sound sequencing and concrete contracts while forming complete
   dependency-ordered slices. Apply the slice, delegation, verification, and
   authorization requirements in the specification contract. When orchestration
   is approved, split work by ownership and dependencies without a fixed total
   worker limit, and give each worker its complete context package before editing.
   Schedule concurrent work within verified runtime limits. Explain material
   reordering. For deferred decisions, mark every dependent slice BLOCKED;
   preserve independent ready work. If a client needs absent backend capability,
   ask whether to include BE work, defer the behavior, or accept expressly
   labelled mock-only scope.
7. Assign READY, PARTIAL, or BLOCKED using the specification contract. Report
   approval and execution authorization separately. Resolve open material
   questions before an unconditional package; deliberate deferral permits only a
   bounded PARTIAL package. Missing overall approval alone is an authorization
   status, not proof that technical discovery failed.
8. Assemble the single canonical package defined in the specification contract,
   then apply the composition prose pass. Include concrete source-plan detail;
   do not substitute generic guardrails for models, routes, limits, mutation
   semantics, file changes, recovery, or observable acceptance criteria. Stop
   after delivering the review and proposed execution package.

## Constraints

- Keep this review read-only: do not edit application code or instructions, add
  dependencies, start servers, run builds/tests/migrations, create branches or
  worktrees, commit, push, or deploy. Output in chat; create no audits, scratch
  exports, source/history copies, or specification files unless requested.
- Use each source for its responsibility. User requirements and approved
  exceptions define intended outcomes. Target instructions define conventions;
  code establishes current behavior and wiring. The canonical backend establishes
  current API, identity, authorization, validation, and errors. Design references
  define scoped appearance/interaction. Templates and siblings are reference-only.
  Surface material conflicts rather than choosing a convenient source. Describe
  both current and intended contracts for approved changes.
- Preserve repository boundaries and deliberate local differences. Do not expand
  scope for a discovered dependency, copy a template's rules into a descendant,
  or assume the implementer has a referenced skill. Carry the permanent guardrails
  from the specification contract into the execution package; keep this review's
  read-only restrictions out of that implementation instruction.
- Scale inspection and output to the feature. Do not invent frameworks, flags,
  fallback layers, migrations, background machinery, or documentation to fill
  the format. Never weaken checks, expose secrets or private payloads, invent
  evidence, or claim successful verification that this review did not perform.

## Composition

Treat conversational planning as an upstream producer, not a workflow to rerun.
Do not invoke an implementation workflow during this review. Keep this skill
usable when installed alone.

<interface>
| Invokes | When | Carries in | Expects back | If unavailable |
| --- | --- | --- | --- | --- |
| `$unslop` | Once the complete review artifact is technically final and this workflow owns the final prose pass | The full artifact, decisions, evidence anchors, readiness labels, and authorization boundaries | Clearer prose with technical meaning and structure preserved | Deliver unchanged and note the skipped pass |
</interface>

Invoke `$unslop` once on the complete user-facing artifact after its technical
content is final, unless a parent workflow owns the final artifact, in which
case the outermost workflow makes the single pass. `$unslop` may improve prose
but must not change technical meaning: preserve code, paths, symbols, commands,
measurements, quoted decisions, evidence anchors, classification labels, and
document structure. If `$unslop` is unavailable, deliver the artifact unchanged
and note the skipped pass.

Preserve readiness, approval evidence, blocked dependencies, and every execution
guardrail through that pass.

## Failure handling

- If the plan, target, or a required reference is inaccessible, name what is
  missing and block affected work; ask for the minimum source or decision needed.
  Do not fabricate a plan or plausible reference.
- If a bundled supporting file is missing, identify the resolved installed path
  and request a complete skill reinstall. Do not substitute the original checkout
  silently or continue without its readiness requirements.
- If a command's behavior or permission is uncertain, inspect its definition and
  classify it for later verification instead of running it during review.
- If delegated implementation settings cannot be verified in the review runtime,
  record them as execution prerequisites. If settings are known unavailable,
  report the limitation and require an acceptable alternative before delegation;
  never silently substitute or claim configuration that did not occur.
- If revisions or contracts materially change, reopen affected lock rows and
  decisions only. Do not discard user changes, reset the checkout, or repeat the
  whole review for harmless unrelated differences.

## Output contract

Return a short readiness statement and classified material deltas, followed by
one self-contained, clearly delimited Implement Spec using
[Specification contract](references/spec-contract.md). Identify ready and blocked
scope, approval evidence/status, and the first eligible slice. For a BLOCKED
result, return the concrete blockers and decisions without an executable start
instruction. Keep questions targeted and stop for answers when required. Do not
claim compilation, runtime correctness, visual parity, production readiness, or
security certification from a read-only readiness review.
