---
name: commit-aware-ubiquitous-docs-maintainer
description: Review the last 10 commits, aggregate meaningful domain changes, and decide whether docs/UBIQUITOUS_LANGUAGE.md and docs/UBIQUITOUS_BUSINESS_LOGIC.md need updates. Use when recent implementation work may have changed domain terminology, model relationships, business rules, constraints, workflows, dependencies, or edge-case behavior. Avoid trivial doc churn when recent commits were only refactors, formatting, renames without semantic impact, UI polish, or infrastructure-only changes.
disable-model-invocation: true
---

# Commit-Aware Ubiquitous Docs Maintainer

Review recent repository history, detect meaningful domain changes, and selectively update `docs/UBIQUITOUS_LANGUAGE.md` and `docs/UBIQUITOUS_BUSINESS_LOGIC.md` only when the implementation warrants it.

## Core Principle

Act as a gatekeeper:

- do not update the docs just because files changed
- do update the docs when recent commits materially changed terminology, relationships, business rules, constraints, workflows, dependencies with domain impact, or real behavior
- prefer `No update needed` over low-value doc churn
- trust the code over commit messages

## Workflow

### 1. Read the current docs first

Read these files if present:

- `docs/UBIQUITOUS_LANGUAGE.md`
- `docs/UBIQUITOUS_BUSINESS_LOGIC.md`

Treat them as the current documented baseline.

If the repository contains instruction files that define how those docs should be written, read them too and follow their structure. Common names include:

- `UBIQUITOUS_LANGUAGE.md`
- `UBIQUITOUS_BUSINESS_LOGIC.md`

Merge forward from the existing truth. Do not rewrite the docs from scratch unless the code clearly invalidates the current content.

### 2. Inspect the last 10 commits

Collect enough detail from the last 10 commits to understand:

- commit messages
- touched files
- changed models, entities, services, use cases, controllers, routes, schemas, validators, constants, configs, views, screens, features, migrations, and integrations
- added, removed, or modified relationships, rules, statuses, and terms

Do not treat every commit equally. Some commits are noise; some carry major semantic shifts.

### 3. Aggregate by meaning, not by commit

Collapse the 10 commits into a small set of semantic changes, for example:

- `Order` now belongs to `Account` instead of `Customer`
- eligibility now depends on subscription status
- a consultant escalation path was introduced
- a retry threshold changed from 3 to 5
- a canonical term changed from `Project` to `Workspace`

The goal is to understand domain impact, not to reproduce the commit log.

### 4. Classify each semantic change

For each aggregated change, assign exactly one label:

- `Ignore`: no domain significance, pure refactor, technical-only change
- `Language Update Candidate`: changed canonical term, actor, action, lifecycle wording, ambiguity, alias drift, or bounded-context naming
- `Business Logic Update Candidate`: changed rules, validation, constraints, lifecycle transitions, dependencies with behavior, thresholds, hacks, or edge cases
- `Both`: affects both terminology and behavior

### 5. Investigate only meaningful candidates

For every candidate that is not `Ignore`:

- inspect the relevant code paths directly
- trace primary model and workflow usages
- verify whether behavior actually changed or merely moved
- confirm where terminology or rules are enforced
- ground conclusions in implementation, not commit-message intent

Prioritize searches in:

- `models`, `entities`, `domain`
- `use-cases`, `usecases`, `services`, `repositories`
- `controllers`, `routes`
- `schemas`, `validators`
- `constants`, `config`
- `views`, `screens`, `features`
- migrations when relations or valid states changed

### 6. Compare against the current docs

For each meaningful candidate, ask:

- is this already documented?
- is the current wording still correct?
- is the existing terminology now misleading or incomplete?
- does the current doc omit a new relationship, rule, actor, action, or edge case?
- has previously documented behavior been retired?

Only changes that survive this comparison should lead to doc edits.

### 7. Choose exactly one outcome

- `No update needed`
- `Updated UBIQUITOUS_LANGUAGE only`
- `Updated UBIQUITOUS_BUSINESS_LOGIC only`
- `Updated both docs`

Choose the narrowest valid outcome.

### 8. Make minimal, evidence-grounded edits

When editing:

- preserve still-valid content
- add only the necessary new entries or modifications
- move retired terms or rules only when the code clearly no longer enforces them
- do not churn the docs just to rephrase correct content
- match the structure expected by the docs' owning guidance or existing format

### 9. Re-read before finishing

Before finishing, confirm:

- every new claim is grounded in code
- unchanged docs were truly left untouched
- retired sections only include genuinely retired language or logic
- the docs still match their required structure

## Update Thresholds

### Usually update the language doc when changes affect:

- canonical domain terminology
- bounded contexts
- important actors
- core workflow or lifecycle wording
- model relationships that change how humans talk about the domain
- newly introduced or retired concepts the team should start or stop using

### Usually update the business-logic doc when changes affect:

- validation rules or domain constraints
- hardcoded thresholds, grace periods, or policy values
- business-specific conditionals
- status transitions
- new eligibility or entitlement checks
- domain-facing integration behavior
- hacks, grandfathering, migration rules, or weird exceptions

### Usually ignore changes such as:

- formatting edits
- comment-only changes
- import ordering
- pure refactors that preserve behavior
- file moves with no semantic change
- mechanical renames with no real domain shift
- UI restyling with no wording change
- dependency bumps without domain behavior change
- low-level infrastructure churn with no business consequence

## Recommended Search Pattern

1. Review the last 10 commits.
2. Build a semantic change list.
3. Mark each change as `Ignore`, `Language`, `Logic`, or `Both`.
4. Verify the non-ignored changes in code.
5. Compare them against the current docs.
6. Update only what crosses the meaningful-domain-change threshold.

## Output Format

Return:

## Decision

One of:

- `No update needed`
- `Updated UBIQUITOUS_LANGUAGE only`
- `Updated UBIQUITOUS_BUSINESS_LOGIC only`
- `Updated both docs`

## Commit aggregation summary

Summarize the meaningful semantic changes found across the last 10 commits.

## Update rationale

Explain why the changes were or were not important enough to justify doc updates.

## Files changed

List which docs were updated, if any.

## Critical discrepancies

Call out meaningful mismatches between:

- commit messages and actual implementation
- existing docs and current code
- terminology used by UI, backend, and model layers

## Writing Constraints

- be skeptical of commit messages
- be conservative about doc churn
- preserve still-correct historical context
- separate terminology changes from behavior changes
- when uncertain, do not invent; document only what can be defended
