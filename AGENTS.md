# Repository instructions

Skillet is a portable collection of agent skills for Codex and Claude Code.

## Source of truth

- Treat `skills/` as canonical. Do not edit installed copies under agent home directories.
- Keep one skill per immediate child of `skills/`.
- The skill folder name must exactly match the `name` in `SKILL.md` frontmatter.
- Every skill must include `agents/openai.yaml` with `policy.allow_implicit_invocation: false`.
- Every skill must include `disable-model-invocation: true` in the `SKILL.md` header.
- Treat all skills as explicit-only; do not enable automatic invocation.
- Keep paths portable and relative to the skill directory. Never commit a user's absolute path.

## Skill design

- Keep `SKILL.md` focused on outcomes, routing, non-obvious constraints, and the core workflow.
- Add `references/`, `scripts/`, or `assets/` only when the skill uses them.
- Preserve user intent and authorization boundaries. Do not turn one example into a universal rule.
- Keep names lowercase and hyphenated, with a maximum length of 64 characters.
- When adding, removing, or renaming a skill, update the inventory in `README.md`.
- Keep installation wording in `README.md` synchronized with `INSTALL.md`; `INSTALL.md` is canonical.

## Before handing off changes

Run:

```bash
npx skills@latest add . --list
```

Do not add a package manifest, build system, or dependency merely to maintain Markdown skills.
