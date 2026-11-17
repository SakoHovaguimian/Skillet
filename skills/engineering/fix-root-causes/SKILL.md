---
name: fix-root-causes
description: Trace a failure to the mechanism that causes it and make a scoped, evidence-backed repair. Use when debugging regressions, intermittent failures, crashes, or bugs that return after workarounds. Do not use for planned feature work or style cleanup.
disable-model-invocation: true
---

# Fix Root Causes

## Outcome

Explain the causal chain from triggering conditions to the observed failure, repair the earliest responsible point within scope, and verify the original failure when permitted. Distinguish a confirmed cause, a supported hypothesis, and a mitigation.

## Inputs and preconditions

Use the failure report, repository, logs, diagnostics, and available reproduction. Establish expected versus actual behavior and the affected version or environment. Discover facts before asking for them; ask only when missing evidence or intended behavior would change the repair.

Honor diagnosis-only requests. Reproduction does not authorize new tests, production access, destructive state resets, persistent-data changes, or unrestricted instrumentation. Use existing evidence when execution is prohibited.

## Workflow

1. Capture the failure precisely: input, relevant state, expected result, actual result, and where the first observable mismatch occurs. Record a known-good case or revision when available. Preserve the failing evidence before changing code or state.
2. Trace backward from the symptom to the earliest violated contract. Follow the actual producer, transformation, owner, and consumer. A stack-frame location is where a failure surfaced, not necessarily where it began.
3. Keep a small hypothesis table when the cause is uncertain: candidate mechanism, supporting evidence, conflicting evidence, and the cheapest observation that distinguishes it from the next plausible explanation. Skip the table for an already-demonstrated cause; never invent alternatives to fill a quota.
4. Run the next permitted discriminating probe. Change one meaningful variable at a time when practical. Prefer existing logs, focused inspection, or bounded instrumentation to speculative patches. Record what would falsify the leading hypothesis; abandon it when evidence contradicts it.
5. State the causal chain before repairing: trigger/state → violated invariant → propagation → symptom. Explain why the proposed change prevents that mechanism. If the chain contains an unsupported link, label it and choose a reversible scoped repair or report the missing evidence.
6. Repair the responsible owner. Preserve valid boundary validation, error recovery, and compatibility. A guard is appropriate when absence is a valid input; it is inadequate when it merely hides corrupted internal state. Search for other instances of the same demonstrated mechanism and repair only those inside the authorized scope.
7. Verify the original failure under equivalent conditions and, when authorized, a neighboring success case or boundary that the fix could break. For intermittent failures, report observed attempts and remaining uncertainty; one success is weak evidence. Use existing checks, not newly created tests unless requested and permitted. Inspect the final diff and remove temporary instrumentation introduced for this investigation unless its retention is intentional and within scope.

### State and timing failures

- A restart changes state, ordering, identity, environment, and caches. Compare these before assuming one cause. Clearing a cache can localize a fault without fixing its writer or invalidation rules.
- For stale or out-of-order results, inspect ownership, cancellation, request identity, and state at completion. A delay or retry can mask a race; require evidence for its placement and bound it.
- For regressions, compare the relevant behavior with known-good code. Use history read-only unless a checkout or other mutation is authorized.

## Constraints

- Do not patch several speculative causes at once or expand into unrelated cleanup.
- Do not remove required defensive checks merely to make a deeper failure visible.
- Keep diagnostic data minimal; do not log secrets or sensitive payloads.
- Never call a mitigation or an unverified hypothesis a confirmed root-cause fix.

## Composition

<interface>
| Invokes | When | Carries in | Expects back | If unavailable |
| --- | --- | --- | --- | --- |
| `$unslop` | Once on the final diagnosis when no parent owns it | Complete diagnosis, evidence, confidence, and verification limits | Clear prose preserving the causal claim and its limits | Deliver unchanged and note the skipped pass |
</interface>

Invoke `$unslop` once on the complete user-facing artifact after its technical content is final, unless a parent workflow owns the final artifact, in which case the outermost workflow makes the single pass. `$unslop` may improve prose but must not change technical meaning: preserve code, paths, symbols, commands, measurements, quoted decisions, evidence anchors, classification labels, and document structure. If `$unslop` is unavailable, deliver the artifact unchanged and note the skipped pass.

## Failure handling

- No reproduction or execution permission: continue bounded inspection and give the best-supported hypothesis with the single next observation that would distinguish it. Do not infer runtime success from a plausible diff.
- Cause outside scope: name the external contract and evidence; apply only an authorized mitigation and record its limitations.
- Probes stop producing useful evidence: stop speculative edits, summarize rejected hypotheses, and identify the missing access or observation. Do not repeat unchanged attempts indefinitely.

## Output contract

Return the symptom and expected behavior, the causal chain with evidence and confidence, the repair or mitigation, related instances found, and verification actually performed. Scale the report to the defect. Include remaining uncertainty and a concrete next check when confirmation was impossible.
