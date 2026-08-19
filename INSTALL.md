# Install Skillet

This is the canonical installation guide for `sakohovaguimian/skillet`.

## Prerequisites

- Node.js with `npx`
- Git access to `github.com/sakohovaguimian/skillet`
- Codex, Claude Code, or both

The GitHub repository must exist before the owner/repository commands below can
download it.

## Install all skills into Codex and Claude Code

Run once from any terminal:

```bash
npx skills@latest add sakohovaguimian/skillet --global --agent codex claude-code --skill '*' --yes
```

This installs at user scope (`--global`), targets both agents, selects every skill,
and skips interactive confirmation. Installed skills remain ordinary inspectable
files managed by the `skills` CLI.

All Skillet skills are explicit-only. Invoke one with `$skill-name` in Codex or
`/skill-name` in Claude Code; neither agent should select these skills automatically.

## Install into one agent

Codex only:

```bash
npx skills@latest add sakohovaguimian/skillet --global --agent codex --skill '*' --yes
```

Claude Code only:

```bash
npx skills@latest add sakohovaguimian/skillet --global --agent claude-code --skill '*' --yes
```

## Verify

```bash
npx skills@latest list --global
```

## Update

Update the installed set from its recorded sources:

```bash
npx skills@latest update --global --yes
```

If the repository has gained a brand-new skill, rerun the install command so the
new skill is selected too.

## Inspect this checkout without installing

From the repository root:

```bash
npx skills@latest add . --list
```

This prints the skills discovered in the checkout and does not install them.

## For Codex or Claude acting on an install request

When the user asks to install all Skillet skills, run the combined install command
above. Do not manually copy individual folders unless the `skills` CLI is unavailable
or the user explicitly requests a manual installation.
