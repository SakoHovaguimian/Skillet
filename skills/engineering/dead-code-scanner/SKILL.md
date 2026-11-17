---
name: dead-code-scanner
description: Audit a repository for unreachable, unnecessary, obsolete, or low-value code, resources, configuration, and dependencies, producing an evidence-backed removal report. Use when asked to find dead code, trace dead ends, evaluate whether referenced code still earns its place, or identify safe cleanup candidates across any platform or language. Do not use to delete candidates; removal requires separate authorization.
disable-model-invocation: true
---

# Dead Code Scanner

## Outcome

An evidence-backed audit that separates code which is unreachable from code which is reachable but no longer valuable. The report covers source, resources, configuration, dependencies, generated integration points, and internally connected dead islands without deleting anything.

A reference is evidence of use, not evidence of necessity. Trace what the reference contributes to current required behavior before deciding that it keeps a candidate alive.

## Inputs and preconditions

A repository or scoped source root and enough access to inspect its entry points, manifests, build configuration, runtime registration, tests, and history. Read applicable repository instructions before scanning.

If the root does not exist, is unreadable, or contains no discoverable source files, stop with a clear error. If the user requests only a subdirectory, report that conclusions apply only to that scope.

## Workflow

1. Establish the current contract. Identify required product behavior, supported public APIs, active platforms, compatibility promises, operational jobs, and migration obligations. Do not assume that existing behavior is still required.
2. Run the bundled indexer for language-neutral lexical evidence, resolving `<skill-dir>` from this `SKILL.md`:

   ```bash
   python3 <skill-dir>/scripts/dead_code_scanner.py <repo-root> --include-assets --include-dependencies
   ```

   Use `--focus <relative-path>` for a partial audit and `--json` when structured output helps. The helper reports signals, not deletion verdicts.
3. Identify every live root that can create behavior: application and library entry points, exported APIs, routes, command handlers, jobs, migrations, plugins, dependency-injection registration, reflection, serialization, build steps, generated-code inputs, resources, and externally invoked scripts.
4. Build a reachability graph from those roots. Follow control flow, data flow, registration, configuration, imports, callbacks, events, and string-addressed lookup across package and process boundaries. References originating only from another candidate do not prove that either node is live.
5. Audit value for every candidate, including referenced candidates. Ask what current requirement the reference satisfies, whether its consumer is reachable, whether its result or side effect is observed, whether another path already owns the behavior, and what concrete failure removal would cause.
6. Classify findings using the confidence rules below. Group internally connected candidates into removal units so the report does not preserve an island merely because its files reference one another.
7. Inspect assets, configuration, flags, migrations, generated inputs, tests, examples, and dependencies after source reachability. A test or example can document an obsolete feature; it does not automatically make production code necessary.
8. Produce the report without deleting or rewriting candidates. Recommend a verification or removal order when evidence is strong enough.

### Candidate classes

- `Unreachable`: no path from a live root.
- `Support-only`: referenced only by tests, fixtures, previews, examples, benchmarks, or documentation that does not represent a supported contract.
- `Dead end`: executed, but its output, mutation, event, or side effect is never observed or needed.
- `Redundant`: reachable behavior is duplicated by the current canonical path.
- `Obsolete`: retained for an expired feature, migration, compatibility promise, flag, or integration.
- `Speculative`: abstraction, extension point, or configuration with no current consumer or accepted requirement.
- `Orphaned`: resource, configuration, dependency, generated input, or adapter whose owning behavior is gone.

### Confidence classes

- `Safe to remove`: no dynamic or external invocation risk, no required behavior depends on it, and the complete removal unit and verification path are known.
- `Potentially removable`: evidence points to removal, but one named contract, consumer, or runtime path still needs confirmation.
- `Review required`: public APIs, reflection, serialization, generated code, external consumers, build tooling, migrations, string-addressed resources, or incomplete repository access prevent a safe conclusion.

## Constraints

- Never equate reference count with value. A reachable caller can itself be unnecessary, and a zero-reference symbol can still be invoked dynamically or externally.
- Do not classify public APIs, plugins, callbacks, serialized types, migrations, build hooks, generated-code inputs, or string-addressed resources as safe until their external and dynamic surfaces are ruled out.
- Distinguish production requirements from tests that merely preserve old behavior.
- Preserve user scope. This skill audits and reports; deletion requires a separate request and review of the proposed removal group.
- Label inferences and incomplete reachability instead of upgrading them to facts.

## Composition

<interface>
| Invokes | When | Carries in | Expects back | If unavailable |
| --- | --- | --- | --- | --- |
| `$unslop` | Once, on the complete audit report, only when no parent workflow owns the final report | The complete drafted report | The prose-improved report with evidence and classifications intact | Skip the pass and deliver the report unchanged |
</interface>

Invoke `$unslop` once on the complete user-facing artifact after its technical content is final, unless a parent workflow owns the final artifact, in which case the outermost workflow makes the single pass. `$unslop` may improve prose but must not change technical meaning: preserve code, paths, symbols, commands, measurements, quoted decisions, evidence anchors, classification labels, and document structure. If `$unslop` is unavailable, deliver the artifact unchanged and note the skipped pass. In this skill, the pass must also not change a finding, remove a caveat, or promote a candidate to a safer confidence class.

## Failure handling

- The helper fails or does not support a repository construct: continue with targeted repository search, name the unsupported construct, and mark affected conclusions as manually derived.
- No trustworthy live roots can be established: report the roots searched and stop before assigning `Safe to remove`.
- A reference crosses an unavailable package, service, generated boundary, or external consumer: classify the candidate `Review required` and name the evidence needed.
- Required behavior is disputed or undocumented: separate current execution evidence from product intent and request a decision before recommending removal.

## Output contract

Return a report with these sections:

1. Scope and current contract
2. Live roots and dynamic surfaces inspected
3. Summary by confidence class and candidate class
4. Safe to remove
5. Potentially removable
6. Review required
7. Removal groups and dependency order
8. Verification needed before deletion
9. Limits, assumptions, and unresolved contracts

For each finding, include a path and line when available, the references found, why those references do or do not establish value, the reachability or value failure, the proposed removal group, confidence, and the verification that would falsify the finding.

Read [references/analysis-guide.md](references/analysis-guide.md) for deeper reachability, value, dynamic-invocation, resource, dependency, and reporting guidance.
