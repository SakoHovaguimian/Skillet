# Skill authoring standard

This document is the review-time authority for every `SKILL.md` in this repository.
It is never loaded at runtime. Skills share behavior only two ways:

1. **Composition**: a skill invokes another skill with `$skill-name`.
2. **Verbatim blocks**: short shared rules are copied word-for-word from this
   document into each skill that needs them, so drift is detectable with `grep`.

Do not create runtime includes between skill folders. Installed skills must work
when installed alone.

## Frontmatter

```yaml
---
name: <kebab-case, exactly matches the folder name>
description: <see formula below>
disable-model-invocation: true
---
```

Description formula, in order:

1. One sentence stating the capability and the artifact or state change it produces.
2. Trigger cues: `Use when ...` listing the concrete requests that should route here.
3. Negative scope when adjacent skills exist: `Do not use for ...`.

Descriptions are agent-neutral. Never name Codex, Claude, or any specific agent.

## Section spine

Every `SKILL.md` uses these `##` sections, in this order. A section is omitted only
when genuinely empty, never renamed. Skill-specific detail nests as `###` inside
the owning section.

| Section | Contains |
| --- | --- |
| `## Outcome` | The artifact or state change the skill must leave behind, and its authority boundary (what it owns vs. delegates). |
| `## Inputs and preconditions` | Required inputs; how to obtain each missing one (ask vs. discover); the stop rule when an input is unobtainable. Destructive steps declare their confirmation gate here. |
| `## Workflow` | Numbered, deterministic steps. Every conditional names its condition and both branches. |
| `## Constraints` | Non-negotiables only: authority boundaries, prohibited actions, and the conflict-resolution order when sources disagree. |
| `## Composition` | The typed invocation table (below) plus any shared verbatim blocks. |
| `## Failure handling` | Explicit fallback per failure mode. Reporting the limitation is the floor; silent degradation is never acceptable. |
| `## Output contract` | The exact shape of the returned report or written file: path, headings, labels. |

## Style

- H1 is the skill's display name and may use Title Case; all other headings use
  sentence case.
- Imperative voice. No bold-caps shouting (`**CRITICAL:**`), no decorative emphasis,
  no emojis.
- State rules once. If two skills need the same rule, one skill owns it and the
  other references it by `$name`.

## Invocation protocol

- Cross-skill calls always use the `$skill-name` syntax.
- Every call a skill can make is declared in its `## Composition` section using
  this table, one row per callee:

  ```markdown
  <interface>
  | Invokes | When | Carries in | Expects back | If unavailable |
  | --- | --- | --- | --- | --- |
  </interface>
  ```

- `Carries in` names the context the caller must pass (decisions, constraints,
  file lists). `Expects back` names what the caller consumes. `If unavailable`
  is mandatory: a missing callee degrades loudly, never silently.

## Canonical writing-hygiene block

Skills that run a prose pass copy this paragraph verbatim into `## Composition`,
optionally followed by one skill-specific sentence naming what the pass must not
change:

> Invoke `$unslop` once on the complete user-facing artifact after its technical
> content is final, unless a parent workflow owns the final artifact, in which
> case the outermost workflow makes the single pass. `$unslop` may improve prose
> but must not change technical meaning: preserve code, paths, symbols, commands,
> measurements, quoted decisions, evidence anchors, classification labels, and
> document structure. If `$unslop` is unavailable, deliver the artifact unchanged
> and note the skipped pass.

## Script invocation

Reference bundled scripts as:

```bash
python3 <skill-dir>/scripts/<name>.py ...
```

with a note that `<skill-dir>` resolves from the location of the `SKILL.md` being
followed. Never use bare `scripts/...` (ambiguous working directory after
installation) or `/path/to/...` placeholders.

## Shared data exchange

Skills that exchange files across projects resolve the shared root with this
chain, which the bundled scripts implement:

1. `$SKILLET_SHARED_HOME`
2. `$CODEX_HOME`
3. `~/.codex`

Producer and consumer skills must document the same chain.

## Determinism rules

- Number workflow steps; keep one action per step.
- Every user-facing question round states what happens with each answer.
- Destructive or irreversible actions (deleting git history, overwriting files)
  require restating the collected inputs and receiving explicit confirmation
  immediately before execution, even when the inputs were gathered earlier.
- When a skill cannot verify a claim, it labels the claim instead of asserting it.

## Quality checklist

Run before merging a new or edited skill:

```bash
python3 scripts/validate_repository.py
npx skills@latest add . --list
```

- [ ] Folder name, frontmatter `name`, and README inventory row all match.
- [ ] `disable-model-invocation: true` in frontmatter; `allow_implicit_invocation: false` in `agents/openai.yaml`.
- [ ] Description follows the formula and is agent-neutral.
- [ ] Section spine order is respected; headings are sentence case below H1.
- [ ] Every `$skill-name` mentioned in the body appears in the Composition table with a fallback.
- [ ] Every referenced callee exists in `skills/` (or the fallback covers its absence).
- [ ] Script paths use the `<skill-dir>` idiom; no absolute or bare-relative paths.
- [ ] Writing-hygiene block, if present, matches this document verbatim.
- [ ] `npx skills@latest add . --list` discovers the skill with the intended name and description.

The repository validator enforces the machine-checkable items above, verifies
local links, loads each Python helper through `--help`, and checks helper-specific
safety invariants. Reviewers remain responsible for whether a skill makes sound
decisions and preserves user authorization.
