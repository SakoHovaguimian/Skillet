---
name: code-simplifier
description: Simplify recently modified code while preserving its behavior and the codebase's existing architecture. Use when asked to reduce a recent diff, remove unnecessary abstractions or configurability, reuse established solutions, or make changed code easier to understand. Do not use for broad repository cleanup, architectural redesign, or behavior changes.
disable-model-invocation: true
---

# Code Simplifier

## Outcome

Recently modified code contains the least code necessary to solve the actual problem while preserving required behavior and the codebase's existing architecture. The result is easier to understand than what it replaced, not merely shorter.

Simple does not mean clever. Fewer lines do not automatically mean better code. Leave code unchanged when it is already as simple as it should be.

## Inputs and preconditions

Require a repository and an identifiable set of recently modified code. Use the user's explicit scope when provided. Otherwise, derive the scope from the current task's touched files and the working-tree or staged diff. If no reliable recent-change boundary exists, ask for the intended files or diff before editing.

Read applicable repository instructions, including `AGENTS.md`, `CLAUDE.md`, and local documentation. Inspect enough nearby code to understand the structure, boundaries, patterns, ownership, and conventions that govern the scoped changes.

## Workflow

1. Establish the recent-change boundary. If the user supplied a scope, use it; otherwise use the current task's touched files and version-control diff. Do not expand into unrelated cleanup.
2. Identify the behavior the scoped code must preserve, including validation, security, error handling, side effects, and required edge cases.
3. Remove speculative code, premature abstractions, unnecessary configurability, and unused flexibility when the required behavior does not need them.
4. Reuse existing helpers, services, types, abstractions, and patterns when the codebase already solves the problem; otherwise keep the local solution under review.
5. Replace custom machinery with native language features, standard libraries, platform APIs, or existing dependencies when they solve the problem and fit local patterns; otherwise preserve the established implementation.
6. Reduce unnecessary nesting, indirection, duplication, boilerplate, temporary state, and obvious comments when the change improves readability; otherwise leave the code alone.
7. Apply the smallest clear diff that completely solves the problem without sacrificing readability.
8. Review the result against the surrounding architecture. If a simplification fights the system around it, revert that simplification; otherwise keep it.
9. Run proportionate, repository-authorized verification for the affected behavior. If verification is unavailable or prohibited, inspect the final diff and report the limitation instead of claiming success.

## Constraints

- Treat the current codebase architecture as the bedrock. Fit all changes within its existing structure, boundaries, patterns, ownership, and conventions.
- Resolve conflicts in this order: explicit user requirements, repository instructions, established architecture and local conventions, then reduction in code size.
- Preserve existing behavior unless explicitly asked to change it.
- Work only on recently modified code unless explicitly asked otherwise.
- Choose clarity over brevity. Prefer explicit, readable code over dense one-liners or clever control flow.
- Avoid nested ternaries when simple `if/else` or `switch` logic is clearer.
- Do not create abstractions for speculative future use.
- Do not introduce a new pattern when the codebase already has one.
- Do not bypass established service, repository, dependency, or ownership boundaries for convenience.
- Do not combine unrelated responsibilities just to reduce line count.
- Keep abstractions that genuinely improve clarity or enforce architecture.
- Never simplify away validation, security, error handling, or required edge cases.

## Failure handling

- The recent-change boundary is unclear: stop before editing and request the intended scope.
- Required behavior is undocumented or ambiguous: preserve observed behavior, label the uncertainty, and ask before making a behavioral choice.
- Nearby code contains competing patterns: prefer the closest recent equivalent and report the ambiguity.
- A smaller implementation would cross an architectural boundary or weaken a guardrail: keep the existing structure and explain why no simplification was made.
- Verification cannot run: report the checks performed and the unverified behavior.

## Output contract

Report only meaningful changes, the verification performed, and any remaining limits. Mention scoped code left unchanged only when the reason clarifies an architectural or behavioral constraint. Do not narrate mechanical edits.

If no safe simplification is warranted, state that the scoped code was left unchanged and why.
