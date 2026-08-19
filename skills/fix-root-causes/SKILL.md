---
name: fix-root-causes
description: Debug failures by tracing symptoms to their underlying causes and fixing the pattern at its source. Use when investigating bugs, regressions, or recurring failures.
disable-model-invocation: true
---

# Fix Root Causes

When debugging, do not paper over symptoms. Trace every problem to its root cause and fix it there.

Symptom fixes accumulate. Each workaround makes the system harder to reason about while the real bug remains. Root-cause fixes can take longer upfront, but they reduce total debugging time.

## Process

- Reproduce first. If you cannot reproduce the problem, you cannot verify the fix.
- Ask "why" until you reach the root cause.
- Resist adding guards just to silence a crash. A nil check may hide the defect that produced the nil value.
- If a workaround needs a paragraph-long comment to justify it, fix the code instead.
- Check for the pattern, not just the instance. Search for the same pattern and fix all relevant instances.
- When stuck, instrument the system. Read the actual error instead of guessing.

## Restart bugs

When something fails after a restart, suspect state before code. Code does not change between runs, but state does.

Inspect persistent state such as configuration files, caches, lock files, and serialized state. If clearing a state file restores behavior, prioritize validating that state and fixing its lifecycle or schema.

## Writing hygiene

When returning a diagnosis, root-cause explanation, remediation plan, or other user-facing technical artifact, invoke `$unslop` once after the technical content is complete. Preserve error messages, stack traces, code, paths, symbols, commands, measurements, causal links, and uncertainty. `$unslop` may improve the prose, but it must not soften evidence, invent a cause, or turn a workaround into a root-cause fix. If a parent workflow owns the final artifact, let that outermost workflow make the single pass instead of running it twice.
