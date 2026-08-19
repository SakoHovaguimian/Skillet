# Contributing

Skillet is intentionally simple: each installable skill lives in one folder under
`skills/`, and the repository is the source of truth.

## Add a skill

1. Create `skills/<skill-name>/SKILL.md` following the section spine and rules in
   [docs/SKILL_AUTHORING_STANDARD.md](docs/SKILL_AUTHORING_STANDARD.md).
2. Use lowercase letters, digits, and hyphens for the folder and frontmatter name.
3. Add concise `name` and `description` frontmatter. The description should say
   what the skill does and when an agent should use it.
4. Put only the essential workflow and constraints in `SKILL.md`.
5. Add `agents/openai.yaml` with interface metadata and explicit-only invocation policy.
6. Set `policy.allow_implicit_invocation: false`; all Skillet skills are user-invoked.
7. Set `disable-model-invocation: true` in `SKILL.md` for the same behavior in Claude Code.
8. Add `references/`, `scripts/`, or `assets/` only when the skill uses them.
9. Add the skill to the inventory in `README.md`.

Minimal entry point:

```markdown
---
name: example-skill
description: Does a specific job. Use when an agent should perform that job.
disable-model-invocation: true
---

# Example Skill

Describe the outcome, decision guidance, workflow, and meaningful constraints.
```

Required `agents/openai.yaml` shape:

```yaml
interface:
  display_name: "Example Skill"
  short_description: "Perform the example workflow"
  default_prompt: "Use $example-skill to perform the example workflow."

policy:
  allow_implicit_invocation: false
```

## Import an existing skill

Copy the whole skill directory so its references and helpers stay together. Before
committing:

- remove `__pycache__`, `.pyc`, generated outputs, and local-only files;
- replace absolute machine paths with paths resolved from the skill directory;
- make the folder name match the frontmatter `name`;
- add `agents/openai.yaml` and disable implicit invocation;
- add `disable-model-invocation: true` to the `SKILL.md` frontmatter;
- check that referenced skills and tools will exist for the target agents; and
- confirm the content's provenance and redistribution terms.

## Inspect

Confirm that the installer discovers the collection from the repository root:

```bash
npx skills@latest add . --list
```

Review the printed names and descriptions before publishing.

## Review checklist

- The trigger description is specific enough to avoid unrelated activation.
- Instructions preserve user intent and do not grant extra authority.
- Conditional detail lives in a linked reference rather than bloating `SKILL.md`.
- Scripts are deterministic, portable, and directly support the workflow.
- No credentials, personal paths, caches, or generated artifacts are present.
- `README.md` and `INSTALL.md` still describe the repository accurately.
