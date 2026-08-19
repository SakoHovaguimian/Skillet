# Skillet

Skillet is the source of truth for Sako's reusable agent skills. Each folder under
[`skills/`](skills/) is a self-contained capability that can be installed into
Codex and Claude Code from this repository.

The repository deliberately has no application runtime or package manifest. The
skills are Markdown plus optional supporting files. Installation is handled by
the open `skills` CLI, while the behavior remains visible in each `SKILL.md`.

## Install everything

After this repository is available at `sakohovaguimian/skillet`, install every
skill globally into both Codex and Claude Code:

```bash
npx skills@latest add sakohovaguimian/skillet --global --agent codex claude-code --skill '*' --yes
```

See [INSTALL.md](INSTALL.md) for single-agent commands, updates, verification,
and local development usage.

## Repository map

```text
skillet/
├── .github/
│   ├── CODEOWNERS                  Default review ownership
│   └── pull_request_template.md    Consistent review checklist
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md                Required skill entry point
│       ├── agents/openai.yaml      Required UI metadata and invocation policy
│       ├── references/             Optional, loaded only when needed
│       ├── scripts/                Optional deterministic helpers
│       └── assets/                 Optional output resources
├── .gitignore                      Keeps generated files out of Git
├── AGENTS.md                       Maintenance rules for coding agents
├── CLAUDE.md                       Points Claude Code to the same rules
├── CONTRIBUTING.md                 Human maintenance workflow
├── INSTALL.md                      Canonical installation instructions
└── README.md                       Purpose, inventory, and orientation
```

Every skill requires both `SKILL.md` and `agents/openai.yaml`. References, scripts,
and assets remain optional and should be added only when the skill genuinely uses them.

## Included skills

| Skill | Purpose |
| --- | --- |
| `commit-aware-ubiquitous-docs-maintainer` | Updates domain documentation only when recent commits changed domain meaning. |
| `conversational-planning-grill-me` | Combines stack-neutral repository discovery with a decision-complete planning interview. |
| `fix-root-causes` | Debugs failures by fixing underlying causes instead of symptoms. |
| `grill-me` | Pressure-tests plans and resolves requirements before action. |
| `grimoire-project-scaffolding-protocol` | Scaffolds iOS projects from the Grimoire template. |
| `ios-conversational-planning-grill-me` | Adds iOS, SwiftUI, Rune, and domain-document discovery to conversational planning. |
| `ios-dead-code` | Audits hybrid UIKit/SwiftUI projects for unreachable code and assets. |
| `project-rune-implementation-protocol` | Implements Rune-first SwiftUI features with architecture parity. |
| `swift-6-concurrency` | Guides Swift 6 concurrency design, migration, and debugging. |
| `swift-sako-semantic-linter` | Reviews Swift and SwiftUI changes against local Sako/Rune conventions. |
| `ubiquitous-business-logic` | Documents hidden rules, edge cases, deeplinks, and analytics behavior. |
| `ubiquitous-components` | Builds the shared Rune and app UI component catalog. |
| `ubiquitous-components-fetch` | Imports the shared Rune component catalog into a project. |
| `ubiquitous-language` | Builds and maintains a code-grounded domain glossary. |
| `unslop` | Removes AI writing tells and adds a human voice. |

## Why each top-level file exists

- `README.md` is the front door for people evaluating or maintaining the repo.
- `INSTALL.md` is the one canonical installation contract for humans and agents.
- `CONTRIBUTING.md` explains how a skill moves from idea to reviewed repository content.
- `AGENTS.md` and `CLAUDE.md` keep Codex and Claude Code aligned when they edit this repo.
- `.gitignore` prevents caches, local agent installs, and OS/editor noise from being published.
- `.github/` supplies default review ownership and a lightweight pull-request checklist.
- `skills/` is the only distributable collection; one directory equals one installable skill.

## Design choices

- Skills are flat under `skills/` so discovery is obvious and no custom indexing is needed.
- The folder name and frontmatter `name` must match, making links, installs, and invocation predictable.
- Every skill is explicit-only in both agents: `agents/openai.yaml` sets
  `allow_implicit_invocation: false` for Codex, and `SKILL.md` sets
  `disable-model-invocation: true` for Claude Code.
- Supporting paths inside skills must be relative, so the same skill works for every user and agent.
- Installed copies are outputs. Edit this repository first, then reinstall or update.
- A license is intentionally not included yet. Choose one only after confirming the provenance and
  desired reuse terms for every imported skill.
