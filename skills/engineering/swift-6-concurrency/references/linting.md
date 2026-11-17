# Concurrency lint findings

An async function without an await may still express a protocol, actor/executor contract, or `@concurrent` CPU operation. Inspect callers and [execution settings](settings.md) before removing async. Preserve required signatures; never add a fake await to silence a lint rule.

Treat lint findings as evidence to investigate, not proof of a concurrency defect. Use a narrow documented suppression when a valid contract requires it. Do not redesign ownership merely to satisfy a heuristic.
