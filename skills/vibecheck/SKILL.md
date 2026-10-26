---
name: vibecheck
description: Implement a task and refine the diff through independent fresh-context code reviews using a chosen reviewer model. Use when asked for VibeCheck, an implement-review-fix loop, or a second agent to check correctness, overengineering, and repository conventions. Do not use for a standalone review or broad codebase cleanup.
disable-model-invocation: true
---

# VibeCheck

## Outcome

Deliver the requested implementation, independently reviewed against the task and the actual codebase. Fix supported findings within scope and report remaining concerns. The implementer owns edits and the final report; each reviewer inspects without editing.

## Inputs and preconditions

Start by collecting the task and reviewer model before implementation. Ask for missing inputs together in one short intake:

> What task should I implement, and which model should independently review it? You can also choose the reviewer's reasoning effort; otherwise I'll use high if supported.

Use answers already supplied in the request or current conversation; do not ask the user to repeat them. If the user delegates model selection, choose an available model different from the implementer's when possible and disclose the choice. Never invent model availability or silently replace a named model.

Use the requested reviewer effort. Otherwise default to high when supported; if high is unavailable, use the closest supported effort and state it. Prefer an effort different from the implementer's when compatible with the user's choices. Default to at most three review rounds unless the user specifies another finite limit.

Require repository access, an identifiable task scope, and a way to start an independent reviewer without inherited conversation history. Discover repository instructions, conventions, and permitted verification from the repository. If the repository or requested reviewer configuration cannot be obtained, report the missing prerequisite before beginning implementation.

## Workflow

1. Complete the intake. Identify the repository and inspect applicable instructions, lint and formatting configuration, and nearby implementations. Record the starting revision and existing working-tree changes so the task's diff can be separated from unrelated user work.
2. Implement the task within the established architecture and naming conventions. Run proportionate checks allowed by the user and repository. Verification never overrides restrictions on tests, builds, or other commands.
3. Prepare the complete task diff against the recorded starting state, including task-owned new files and subsequent fixes. Exclude unrelated pre-existing changes. Give the reviewer repository access and enough revision or snapshot information to inspect the same state as the diff. Keep that state stable while the reviewer works.
4. Spawn a new reviewer with the selected model and reasoning effort and no inherited chat history. Where supported, set `fork_turns="none"` explicitly. Supply only the original task with accepted scope clarifications and restrictions, the task diff, and repository location/access. Let the reviewer discover applicable instructions and conventions directly. Do not provide the implementer's reasoning, self-assessment, prior review findings, or proposed answers.
5. Instruct the reviewer to perform the review described below and return its findings to the implementer. Wait for completion before editing. Record the actual model and effort used when exposed by the environment; label unverified settings rather than claiming they were confirmed.
6. Assess each finding against the task and repository evidence. Fix supported issues within scope. Explain any rejected finding or deferred change; ask only when resolution requires a material scope or behavior decision the task does not answer. Do not add speculative abstractions or unrelated cleanup to satisfy a preference.
7. After fixes, run the affected permitted checks and repeat from step 3 with a fresh reviewer. Stop when a completed review finds no actionable issues, the round limit is reached, or a prerequisite or unresolved decision blocks progress. If the last round triggers edits, report that those final edits have not received a further independent review. A failed or incomplete review never counts as clean.
8. Report the outcome using the output contract.

### Reviewer brief

Review the original task and diff with access to the repository. Read applicable instructions and inspect surrounding code and configuration before deciding that a convention has been followed or violated. Check:

- Correctness, regressions, edge cases, and whether the task is fully satisfied.
- Overengineering: unnecessary abstractions, indirection, configurability, dependencies, or speculative future-proofing. Suggest the simplest solution that preserves required behavior and architectural boundaries.
- Compliance with actual architecture, ownership boundaries, naming, file organization, formatting, lint rules, and repository instructions.
- Unrelated changes or avoidable churn in the task diff.

Remain read-only. Do not modify files or run auto-fix commands. Run only repository-authorized checks that do not change the reviewed files, and report exactly what ran and its result. If a check cannot run, say so; inspection alone does not establish that lint or a build passes.

For each finding, provide severity, a file and line reference, the violated requirement or concrete failure scenario, the impact, and the smallest appropriate fix. Cite the local convention or configuration when alleging a standards violation. Separate confirmed issues from questions and optional preferences. Report no actionable findings when that is the result; do not manufacture issues to fill a review.

## Constraints

- Resolve conflicts in this order: explicit user requirements, applicable repository instructions, established local conventions, then reviewer preferences.
- Preserve unrelated user changes. If the task diff cannot be isolated reliably, resolve that boundary before reviewing or editing it further.
- Keep reviewers independent and read-only. Every review round uses a new reviewer with no inherited conversation context.
- Honor the requested model and supported effort. Do not substitute a same-context self-review for the independent review.
- Keep the loop bounded. Clean means no actionable findings in the reviewed state, not a guarantee that the implementation is defect-free.
- Stay within the task's authorization. This workflow does not itself authorize commits, pushes, merges, deployments, destructive operations, or worktrees.

## Failure handling

- Required intake is missing: ask only for the missing task or reviewer selection and wait before implementation.
- The environment cannot select the requested model or start a fresh-context reviewer: explain the limitation and request an available configuration or a user-run independent review. Do not present the workflow as completed.
- Repository access or conventions are incomplete or conflicting: state what could be verified, follow the closest applicable authoritative pattern, and identify any decision requiring the user.
- Verification is unavailable or prohibited: report the checks actually performed and the specific behavior or standards left unverified.
- A review fails, stalls, or cannot inspect the diff: report an incomplete review and stop; do not retry indefinitely or claim a clean result.
- Findings require broader changes or the round limit is reached: stop, report remaining issues and any unreviewed edits, and leave the scope or continuation decision to the user.

## Output contract

Return a concise report with:

- Implementation: what changed and whether the original task is satisfied.
- Review: reviewer model, effort, completed rounds, and status (clean, findings remain, or incomplete).
- Findings: meaningful issues fixed, rejected with reasons, or still unresolved, with file references where useful. Keep optional preferences separate.
- Verification: checks actually run, their results, and material limitations, including edits made after the final review.

Do not claim compliance, successful checks, or independent review without evidence.
