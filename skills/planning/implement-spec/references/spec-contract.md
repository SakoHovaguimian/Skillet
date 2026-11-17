# Specification contract

Read this reference before establishing Pattern Lock or producing the final
Implement Spec. Populate it with inspected facts and actual feature decisions;
leave no generic placeholders for settled facts. Keep proposed artifacts and
blocked unknowns explicit. Omit irrelevant detail rather than manufacturing work.

## Pattern lock

Use stable row identifiers and these columns:

| ID | Planned responsibility | Target, layer, files | Artifact: existing or proposed | Applicable rule or contract | Inspected example: path and symbol | Revision and local difference | Pattern status |
| --- | --- | --- | --- | --- | --- | --- | --- |

Use VERIFIED, APPROVED EXCEPTION, or GAP for pattern status. Keep artifact
existence separate: a proposed file can follow a VERIFIED pattern. Record the
approved decision and illustrative design for a new pattern whose representative
implementation does not yet exist; do not pretend it is an inspected example.
Make that representative and its guide update prerequisites for broader reuse.

Cite the source revision and relevant inspected local differences, not just a
branch name or an unverified date. Map every consequential implementation choice
to a row. Verify existing model, endpoint, component, registration, and script
names. Do not use a plausible invented path as evidence.

Record each target's relevant style profile from its own current guides and
configuration: call versus declaration wrapping, thresholds, constructor
signatures and body padding, compact versus expanded blocks, switch/case layout,
section or MARK comments, indentation, naming, member ordering, independent model
placement, and file organization. Identify file-local rules where required and
which conventions need manual review. Shared lineage, including Grimoire and
Obelisk, is not proof of identical rules.

Separate executable lint/format enforcement, manually reviewed conventions, type
checking, compilation, and runtime/device checks. Record verified project commands
and permitted standard diagnostics, such as `git diff --check`, with working
directory, purpose, relevant side effects, and permission status. Inspect command
definitions: a check may generate files, and a type check does not prove formatting.

## Slice and delegation requirements

For each dependency-ordered slice, include:

- Observable workflow and exact behavior; files marked existing or proposed;
  owner, prerequisites, and Pattern Lock row IDs.
- Required schema/model, API, client state, UI, navigation, registrations, copy,
  and live/mock/demo integration, only where applicable. Include failure recovery,
  reconciliation, and a canonical example or maintained-guide update when needed.
- Acceptance criteria as observable behavior or inspectable state, not “works.”
- Permitted commands and manual verification, with a gate before dependent slices:
  inspect the actual changed files against Pattern Lock and the style profile,
  verify integration and ownership, and report evidence. Passing a build alone
  does not satisfy the gate.

Include a delegation section when implementation orchestration is approved. Do
not infer an unknown orchestration choice; ask as specified in the entrypoint.
Define shared contracts and exact file ownership first, one integration owner for
shared contracts/registrations, and serialized overlapping edits or unstable
interfaces. Choose workers by cohesive responsibilities and dependencies, with no
skill-defined cap on total workers or waves. Distinguish that total from actual
concurrent capacity: verify runtime limits, schedule waves or queue work within
them, and report constraints instead of promising unlimited simultaneous agents.

### Worker context package

Give every worker a self-contained assignment before its first edit. Do not rely
on the parent's conversation, inherited context, installed skills, or a vague
instruction to follow repository conventions. Include:

- Feature outcome and workflow context; selected platforms; exact editable roots,
  read-only references, owned files, dependencies, shared interfaces, and integration
  owner. Include relevant domain vocabulary, business rules, permissions, privacy,
  failure/recovery behavior, and live/mock/demo requirements.
- Applicable root and nested AGENTS.md instructions and maintained engineering,
  architecture, language, and style guides. Embed essential rules and supply exact
  accessible paths for the full sources; resolve conflicts before dependent work.
- Its Pattern Lock rows, exact canonical file/symbol examples and direct callers,
  reference revisions and consequential local differences, accepted decisions,
  approved exceptions/new-pattern sketches, and existing/proposed artifact names.
- The target's complete applicable formatting profile: naming, indentation,
  spacing, call/declaration wrapping, constructor/body padding, blocks, switch/case,
  sections/MARK, member order, independent model placement, and file organization.
  Include lint/format configuration paths, verified commands and working
  directories, and conventions requiring manual review. Distinguish formatting,
  lint, type checking, compilation, and runtime evidence.
- Exact affected contracts, integrations and registration points; state ownership,
  lifecycle/concurrency requirements, navigation, caching, persistence, and UI/token
  composition where applicable. Include observable acceptance criteria, permitted
  verification with side effects/permissions, slice gates, and all permanent
  implementation guardrails below, including the missing-pattern stopping rule.

Require each worker to load its assigned instructions, configurations, examples,
and callers and report the loaded paths/symbols and unresolved gaps before editing.
If a required source is inaccessible, stop that assignment; do not guess or weaken
the lock. Pass essential reference content directly when workers lack filesystem
access, and verify that the assignment remains executable in that environment.
Keep packets focused on all applicable requirements, not whole-repository dumps.

Route out-of-ownership work and unresolved architectural decisions to the
integration owner. Require handoffs with changed files/interfaces, lock rows and
examples followed, actual verification, and unresolved gaps. After handoff or
context loss, reload the assignment and focused sources before editing. The
integration owner reviews every worker's actual diff against its lock and style
profile, resolves shared wiring, and verifies the complete workflow before
declaring a slice complete.

Separate requested model/reasoning settings from verified tool capabilities and
actual configuration. Mark future capability checks as prerequisites; do not
claim that a future worker is already configured. Require an explicitly accepted
alternative before using a known unavailable setting.

## Readiness and authorization

State technical readiness, approval, and execution authority independently:

- READY: required evidence and material decisions are resolved for the full scope.
- PARTIAL: enumerate independent ready slices and every blocked dependency.
- BLOCKED: no independent safe starting slice exists; give concrete resolutions
  and targeted questions without an executable start instruction.

Carry source-plan approval evidence for the exact reviewed version. Separate
clarifications, evidence corrections, and material review changes, with approval
status for the latter. Confident draft language or an agent's decision ledger is
not user approval. Keep approved decisions closed unless material new evidence
affects them. Do not hide deferred decisions as assumptions or label mock-only
scope live-ready.

Generating this package never authorizes its reviewer to implement. Preserve
existing explicit permissions. State absent final approval or an implementation
request once; do not demand approval again for an unchanged approved decision.
Submitting the complete package later as a user implementation instruction is the
execution request for its ready scope. Preserve separately restricted operational
permissions; neither technical readiness nor general feature approval grants them.

## Canonical execution package

Start the response with readiness, ready/blocked scope, approval status, the first
eligible slice, and a compact account of review deltas. Then delimit one package
with `Begin Implement Spec` and `End Implement Spec`. Tell the user to copy the
whole package. Do not output a second competing plan or depend on the interview
transcript, this skill, or its references being installed with the implementer.

Use these sections inside that package:

1. **Scope and provenance.** Feature outcome, observable success, non-goals,
   platforms, exact editable and reference-only repositories, source-plan
   identity/version, inspected revisions/local state, and relevant approval
   evidence. Use portable repository-relative source paths with exact target
   roots supplied for this task.
2. **Decision lock.** Settled product and architectural choices, approved
   exceptions, relevant rejected alternatives, review deltas, assumptions, and
   deferred decisions with all blocked dependents. Preserve specific limits,
   mutation semantics, and intentional exceptions from the source plan.
3. **Pattern lock and local profiles.** The lock table, essential per-repository
   conventions, and tooling classifications. Embed critical rules so an agent
   without installed skills can act; cite accessible target guides for detail.
4. **Contract map.** Applicable models/schema changes, routes and methods,
   request/response fields, validation, identity/roles/ownership, errors,
   conflicts/recovery, filters/sorting/pagination, client mapping, live/mock/demo
   behavior, and migration/data implications. State current versus approved
   intended contracts. Do not replace specifics with “wire it up.”
5. **Ordered vertical slices.** Apply the slice requirements above. Include
   concrete edits, integrations, acceptance criteria, gates, and only necessary
   canonical-example/documentation work. Retain blocked work in view.
6. **Ownership and delegation.** Include only when requested; apply the ownership,
   worker context packages, dependencies, configuration, and handoff requirements
   above. Record the settled orchestration choice, worker responsibilities, total
   assignments, verified concurrency, and scheduling; include each worker package
   in the copy-ready specification so the implementer can dispatch it without
   reconstructing context. For a single owner, record that choice in the decision
   lock and omit this section.
7. **Verification and operational permissions.** Exact commands, directories,
   purposes, side effects, permission status, and manual checks. Separate discovery
   already performed from future lint/format/type/compile/runtime/device checks.
   Separate editing migration files from applying migrations, live provider work,
   or deployment. Record pending evidence honestly and cover every requested
   workflow, with approved exclusions or blockers labelled.
8. **Execution instruction.** A proposed user instruction containing the permanent
   guardrails below, the ready/blocked boundary, ownership, and first ready slice.
   Direct the implementer to follow the full package's decision lock, contracts,
   local rules, and dependency order. Do not copy review-only prohibitions that
   would prevent authorized implementation. Omit the executable start instruction
   entirely for a BLOCKED result.

## Permanent implementation guardrails

Carry the following rules into the package's execution instruction, including
feature-specific approved decisions and permissions. These rules govern future
implementation as well as delegated workers:

- Do not write, extend, modify, or delete automated tests or delegate that work.
  Run existing tests only when explicitly authorized, using verified commands.
- Do not create worktrees or run Xcode builds unless explicitly requested.
  Preserve user changes. Do not infer permission to create branches, commit, push,
  deploy, apply migrations, reset data, or perform external provider writes;
  retain any explicit authorization already supplied for those operations.
- Work only within specified editable repositories, platforms, and ready scope.
  Keep reference-only projects read-only. A dependency does not expand scope.
- Before editing, confirm the checkout, relevant references, and contracts still
  match the specification. Preserve local edits; never reset a repository to make
  it match. Reopen only decisions affected by material changes, not the whole
  review for unrelated differences. Reload focused rules and examples after
  handoff or context loss.
- Preserve approved behavior, decisions, architecture, ownership, async semantics,
  and unrelated visual choices. Follow each target's actual naming, spacing,
  formatting, file organization, and semantic conventions.
- Reuse models, components, helpers, services, middleware, tokens, strings, and
  presentation behavior. Add abstractions only for a demonstrated current
  responsibility or reuse. Split independent types into focused files near their
  owner under the target's rules; do not extract every private detail into a file.
- Stop affected work on a new GAP, material contract contradiction, unapproved
  departure from a locked pattern, or required scope expansion. Show the evidence
  and smallest concrete resolution, ask, and wait. Continue only independent ready
  work; outcome approval does not authorize unspecified architecture. Do not ask
  again for an architectural decision explicitly approved in the specification.
- Complete each vertical slice and its actual-diff Pattern Lock/style/integration
  gate before dependent slices. Do not weaken checks, suppress failures, or claim
  unperformed verification. Keep secrets and private payloads out of output and
  telemetry; refer to configuration keys without exposing values.
- Use the most specific applicable implementation workflow when available while
  preserving these boundaries. The complete specification remains executable
  without that workflow or any installed skill.
- Report completed and blocked work, changed-file evidence, approved deviations,
  actual commands/results, and pending verification. Do not call the whole feature
  complete while an included workflow remains unfinished.
