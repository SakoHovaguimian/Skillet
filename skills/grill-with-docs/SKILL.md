---
name: grill-with-docs
description: Stress-test plans against the repository's domain model, code, and decision history while running a one-question-at-a-time planning interview. Use when a user wants to challenge a design or implementation plan against existing domain language, CONTEXT.md, CONTEXT-MAP.md, and ADRs, and wants terminology resolved with immediate glossary updates.
disable-model-invocation: true
---

# Grill With Docs

## Goal
Drive a live planning interview that resolves design decisions branch by branch and keeps project documentation aligned as decisions crystallize.

## Operating Order
1. Read existing documentation first.
2. Inspect relevant code when code can answer the question.
3. Identify existing domain language.
4. Compare the user's plan against that language.
5. Ask one unresolved question at a time.
6. Provide a recommended answer with each question.
7. Update `CONTEXT.md` immediately when terminology is resolved.
8. Offer an ADR only when ADR criteria are met.

Never ask the user a question that can be answered from the repository.
Never batch resolved glossary updates.
Never put implementation details in `CONTEXT.md`.
Never create documentation files before there is concrete content to write.

## Codebase Exploration
When exploring, check documentation before implementation code.

### Single-Context Repository
Treat the repository as single-context when root `CONTEXT.md` exists and root `CONTEXT-MAP.md` does not.

### Multi-Context Repository
Treat the repository as multi-context when root `CONTEXT-MAP.md` exists.
Use the map to identify the relevant context path, then check:
- system-wide ADRs in `docs/adr/`
- context-specific ADRs near each context

If context ownership of the current topic is unclear, ask one question to resolve the owning context before making documentation edits.

### Lazy File Creation
Create files only when there is concrete content:
- Create `CONTEXT.md` only after the first domain term is resolved.
- Create `docs/adr/` only when the first qualifying ADR is needed.
- Never create placeholders.

## Question Loop
Run this loop until decisions are clear:
1. Pick the highest-leverage unresolved branch.
2. Explore local docs/code if the branch is discoverable.
3. If evidence resolves it, state the conclusion and continue.
4. If user input is still required, ask exactly one question in this format:
   - `Question:` single concrete question.
   - `Recommended answer:` one recommended choice with short rationale.
5. Wait for the user's answer before the next question.

## Domain Language Discipline
Call out terminology conflicts immediately.
When the user uses overloaded or fuzzy words, propose one canonical term and explicitly list terms to avoid.

When discussing relationships, stress-test with concrete edge-case scenarios that force boundary clarity.

When user claims contradict code behavior, surface the contradiction plainly and ask which rule is intended.

## `CONTEXT.md` Rules
Keep `CONTEXT.md` as a glossary only.
Do not use it as implementation spec, decision log, scratchpad, or task list.

Before adding a term, ask whether it is project-specific domain language rather than a generic programming concept.

Use this structure:

```md
# {Context Name}
{One or two sentence context description.}

## Language
**Term**:
Short definition in one or two sentences.
_Avoid_: synonym-a, synonym-b

## Flagged Ambiguities
**Ambiguous Term**:
Conflict summary and canonical resolution.

## Example Dialogue
Dev: ...
Domain Expert: ...
```

Definition rules:
- Be opinionated.
- Keep each definition tight.
- Define what the concept is, not implementation behavior.
- Show relationships and cardinality where obvious.

## `CONTEXT-MAP.md` Rules
When multiple contexts exist, maintain a concise map with:
- context links
- one-line context responsibilities
- directional relationship bullets with event or reference contracts

## ADR Rules
Store ADRs in `docs/adr/` and use sequential numeric filenames:
- `0001-slug.md`
- `0002-slug.md`

Before creating one, scan existing ADRs and increment the highest number.

Use short ADRs by default:

```md
# {Decision Title}
{One to three sentences covering context, decision, and why.}
```

Offer or create an ADR only if all are true:
1. The decision is hard to reverse.
2. The decision is surprising without context.
3. The decision reflects a real trade-off.

Do not create ADRs for obvious, temporary, easy-to-reverse, or low-impact implementation choices.
