---
name: review-changes
description: Independently review a scoped code change for bugs, regressions, and missed requirements, and fix supported findings when edits are in scope. Use when asked for a fresh review of a diff or an implement-review-fix pass. Do not use for a behavior-preserving simplification pass or broad codebase cleanup.
disable-model-invocation: true
---

# Review Changes

## Outcome

Deliver the scoped change with an independent review and a clear account of the exact state reviewed. Spend review effort on concrete failure risks, unnecessary complexity, and actual repository conventions. The implementation owner makes edits; the reviewer stays read-only.

## Inputs and preconditions

Reuse the task, repository, diff scope, and restrictions already supplied. For an implementation request, implement then review. For an existing-diff request, review that diff. Ask for missing scope only when it cannot be established reliably.

Reviewer selection is optional intake. Honor an explicitly selected model and effort. Otherwise use an available fresh-context reviewer without asking the user to select a model; use its default effort for a small bounded diff and higher effort when supported for substantial behavior, state, concurrency, or contract changes. A different available model may help but is not required. Do not invent availability or silently substitute for a named configuration.

Default to one review and, if its repairs warrant it, one follow-up review. Honor a different finite round limit supplied by the user. Resolve reviewer availability before making changes that depend on a required review gate; independent implementation already authorized may continue if review is unavailable, with that limitation explicit.

## Workflow

1. Inspect applicable instructions, nearby patterns, and permitted verification. Record the starting revision, staged/unstaged changes, and untracked task files. Separate pre-existing user work from this task; HEAD alone is not a reliable task baseline in a dirty tree.
2. Implement the requested behavior when implementation is in scope. Run proportionate authorized checks. For an existing diff, skip implementation and establish the review boundary directly.
3. Prepare the full task change, including new files and subsequent fixes, against the starting state. Give the reviewer repository access and enough baseline/current content or revision information to reconstruct it. Include relevant pre-existing context without claiming it as task-owned. Freeze task edits during review and record the reviewed state using available revisions, diff content, or content fingerprints; a worktree or commit is not required.
4. Start a reviewer without inherited conversation history. Where supported, use `fork_turns="none"`. Supply only the original task with accepted clarifications, scope and execution restrictions, task diff, repository access, and the reviewer brief below. Do not supply the implementer's reasoning, claimed success, or previous findings. Wait before editing.
5. Assess returned findings against source evidence. For review-only requests, report confirmed issues. When edits are authorized, fix confirmed issues within scope. Reject incorrect findings with a reason and keep optional preferences separate.
6. Verify repairs with the affected permitted checks. Use a fresh follow-up review for correctness, contract, ownership, or concurrency repairs when the round budget allows. A mechanical correction may finish after focused verification; disclose that the final edit lacks independent review. Follow-up reviewers inspect the complete current task diff, without prior verdicts or implementer explanations.
7. Stop after a completed review with no actionable findings, the finite budget, or a concrete blocker. If source changed during review, treat affected findings as stale and reconcile before claiming a reviewed result. Do not spend rounds seeking stylistic unanimity.

### Reviewer brief

Read repository instructions and the closest applicable implementation. Review the original task and full scoped diff for:

- Missing behavior, regressions, edge cases, data loss, invalid state transitions, and broken contracts.
- Unnecessary abstractions, configurability, dependencies, or unrelated churn.
- Violations of evidenced local architecture, ownership, naming, formatting, and integration conventions.

Stay read-only. Run only permitted checks that do not mutate reviewed files. Each actionable finding needs severity, path and line, a concrete failure scenario or violated requirement, impact, and the smallest appropriate correction. Cite local authority for convention findings. Separate confirmed issues from questions and optional preferences. Return no actionable findings when supported; do not manufacture issues or claim checks ran without evidence.

## Constraints

- User requirements and repository instructions outrank reviewer preferences.
- Preserve unrelated changes. Resolve an ambiguous edit boundary before repairing it.
- A same-context self-review does not count as independent review. A clean review applies only to the reviewed state and is not a guarantee of correctness.
- This workflow authorizes no commits, staging, pushes, deployments, destructive operations, or worktrees beyond the user's request.
- Respect restrictions on tests, builds, and external services throughout implementation and review.

## Failure handling

- No independent reviewer or requested configuration is available: report the review as unavailable. Complete separately authorized implementation when useful; do not claim the full workflow completed. Ask for a substitute only if independent review is required to proceed.
- A reviewer cannot inspect the full diff or fails: report incomplete review. Correct a concrete access problem if possible; do not retry unchanged failures indefinitely.
- Budget reached with findings or final edits: report remaining findings and which edits have not received independent review. Do not silently restart the budget.
- A finding needs a material scope or behavior decision: present the concrete choice and continue only independent authorized work.

## Output contract

Briefly report the implementation or diff reviewed, actual reviewer configuration when exposed, completed rounds, findings fixed/rejected/remaining, and checks actually run. State whether the final changed state received independent review. Distinguish no actionable findings, findings remain, incomplete, and unavailable; never report an unsuccessful review as clean.
