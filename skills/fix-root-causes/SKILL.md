---
name: fix-root-causes
description: Debug failures by tracing symptoms to their underlying causes and fixing the pattern at its source. Use when investigating bugs, regressions, recurring failures, or crashes that keep returning after workarounds. Do not use for planned feature work or style cleanups.
disable-model-invocation: true
---

# Fix Root Causes

## Outcome

The failure under investigation is traced to its underlying cause and fixed at that source within the authorized scope, instead of being papered over at the symptom. Symptom fixes accumulate: each workaround makes the system harder to reason about while the real bug remains. Root-cause fixes can take longer upfront, but they reduce total debugging time.

## Inputs and preconditions

A failure report and enough evidence to investigate it. Reproduce through existing evidence or an authorized local execution. Reproduction does not authorize creating tests, contacting production systems, modifying persistent data, or clearing state. When reproduction is unavailable, continue with bounded inspection and label the diagnosis and verification limits.

## Workflow

1. Reproduce the failure when authorized and available; otherwise inspect the existing evidence and state the verification limit.
2. Ask "why" repeatedly until you reach the root cause, not just the nearest guard-able condition.
3. Search for other instances of the demonstrated defect. Repair instances within the authorized scope when the same cause and fix are supported by evidence. Report broader or behaviorally different instances separately.
4. When stuck, instrument the system. Read the actual error instead of guessing.
5. Verify the fix against the original reproduction when authorized and available; otherwise inspect the final diff and report what remains unverified.

### Restart bugs

When something fails after a restart, suspect state before code. Code does not change between runs, but state does.

Inspect persistent state such as configuration files, caches, lock files, and serialized state. If clearing a state file restores behavior, prioritize validating that state and fixing its lifecycle or schema.

## Constraints

- Resist adding guards just to silence a crash. A nil check may hide the defect that produced the nil value.
- If a workaround needs a paragraph-long comment to justify it, fix the code instead.
- Never report a workaround as a root-cause fix.

## Composition

<interface>
| Invokes | When | Carries in | Expects back | If unavailable |
| --- | --- | --- | --- | --- |
| `$unslop` | Once, on the final user-facing diagnosis or remediation plan, only when no parent workflow owns the final artifact | The complete drafted artifact | The prose-improved artifact with technical content intact | Skip the pass and deliver the artifact unchanged |
</interface>

Invoke `$unslop` once on the complete user-facing artifact after its technical content is final, unless a parent workflow owns the final artifact, in which case the outermost workflow makes the single pass. `$unslop` may improve prose but must not change technical meaning: preserve code, paths, symbols, commands, measurements, quoted decisions, evidence anchors, classification labels, and document structure. If `$unslop` is unavailable, deliver the artifact unchanged and note the skipped pass. In this skill, the pass must also not soften evidence, invent a cause, or present a workaround as a root-cause fix.

## Failure handling

- Reproduction impossible: deliver the best-supported hypothesis, labeled as unverified, with the instrumentation that would confirm it.
- Root cause lies outside the editable scope (third-party code, platform bug): document the true cause, apply the least-harmful mitigation only within the authorized scope, and mark it explicitly as a mitigation with a link back to the cause.

## Output contract

Return a diagnosis containing: the observed symptom, the reproduction used, the root cause with supporting evidence, the fix applied or proposed, other instances of the same pattern found, and the verification performed. Label anything unverified.
