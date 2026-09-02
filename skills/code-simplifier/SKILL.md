---
name: code-simplifier
description: Simplify recently modified code while preserving its behavior and the codebase's existing architecture. Use when asked to reduce a recent diff, remove unnecessary abstractions or configurability, reuse established solutions, or make changed code easier to understand. Do not use for broad repository cleanup, architectural redesign, or behavior changes.
disable-model-invocation: true
---

# Code Simplifier

## Outcome

Recently modified code contains the least code necessary to solve the actual problem while preserving required behavior, validation, security, error handling, edge cases, and architectural boundaries.

Simple means explicit and readable, not clever. Leave code unchanged when it is already as simple as the existing system allows.

## Inputs and preconditions

A repository and an identifiable set of recently modified code. Use the user's explicit scope when provided. Otherwise, derive the scope from the current task's touched files and the working-tree or staged diff. If no reliable recent-change boundary exists, ask for the intended files or diff before editing.

Read applicable repository instructions, including `AGENTS.md`, `CLAUDE.md`, and local documentation, before changing code. Inspect enough nearby code to understand the architecture, ownership boundaries, conventions, and established patterns that govern the scoped changes.

## Workflow

1. Establish the recent-change boundary. If the user supplied a scope, use it; otherwise use the current task's touched files and version-control diff. Do not expand into unrelated cleanup.
2. Identify the behavior the scoped code must preserve, including validation, security, error handling, side effects, and required edge cases.
3. Inspect nearby code for existing helpers, services, repositories, types, dependencies, language features, standard-library facilities, native APIs, and conventions that already solve the same problem.
4. Review each changed construct in this order:
   1. Remove it if the required behavior does not need it.
   2. Replace it with an established codebase solution if one exists.
   3. Replace custom machinery with a suitable platform or already-installed dependency when that is consistent with local patterns.
   4. Reduce nesting, indirection, duplication, boilerplate, temporary variables, unnecessary comments, and speculative flexibility when readability improves.
   5. Keep it when further reduction would obscure intent, combine responsibilities, weaken a boundary, or introduce a new pattern.
5. Apply the smallest clear diff that completely preserves the required behavior. Do not retain edits merely to demonstrate that simplification occurred.
6. Review the resulting diff against the surrounding architecture and revert any simplification that bypasses an established ownership, service, repository, or dependency boundary.
7. Run proportionate, repository-authorized verification for the affected behavior. If verification is unavailable or prohibited, inspect the final diff and report the limitation instead of claiming success.

## Constraints

- Preserve existing behavior unless the user explicitly requests a change.
- Resolve conflicts in this order: explicit user requirements, repository instructions, established architecture and local conventions, then reduction in code size.
- Work only on recently modified code unless the user explicitly broadens the scope.
- Prefer explicit, readable code over dense one-liners, nested ternaries, or clever control flow.
- Do not invent an architectural direction that is cleaner only in isolation.
- Do not create abstractions, extension points, configuration, or flexibility for a single speculative future use.
- Do not bypass established service, repository, dependency, or ownership boundaries for convenience.
- Do not combine unrelated responsibilities merely to reduce line count.
- Keep abstractions that clarify intent, enforce architecture, or serve demonstrated reuse.
- Never simplify away validation, security, error handling, or required edge cases.
- Do not add dependencies when the language, platform, standard library, or existing dependencies already suffice.

## Failure handling

- The recent-change boundary is unclear: stop before editing and request the intended scope.
- Required behavior is undocumented or ambiguous: preserve observed behavior and label the uncertainty; ask before making a behavioral choice.
- Nearby code contains competing patterns: prefer the pattern used by the closest recent equivalent and report the ambiguity.
- A smaller implementation would cross an architectural boundary or weaken a guardrail: keep the existing structure and explain why no simplification was made.
- Verification cannot run: report the checks performed and the unverified behavior.

## Output contract

Return only meaningful information:

- the files simplified and the unnecessary code or indirection removed
- any scoped code deliberately left unchanged because it already fits the architecture
- the verification performed and any remaining limits

Do not narrate mechanical edits. If no safe simplification is warranted, say that the scoped code was left unchanged and why.
