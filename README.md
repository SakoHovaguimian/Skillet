# Skillet

<img width="400" height="400" alt="Skillet logo" src="https://github.com/user-attachments/assets/ec40177f-ec05-4be4-81ca-57fd9425fe16" />

Skillet is my personal collection of reusable agent skills for Codex and Claude Code.

These are the workflows I actually use to build software: planning features, pressure-testing decisions, implementing against an existing architecture, debugging root causes, documenting hidden business logic, reviewing code, and cleaning up the garbage AI tends to leave behind.

The goal is simple: **make agents work more like I do.**

Not just generate code, but understand the repository, respect its patterns, ask the right questions, and make deliberate changes.

## How It Works

Every immediate child of [`skills/`](skills/) is its own installable skill.

There is intentionally no application runtime or package manifest. The behavior lives directly inside readable `SKILL.md` files, with deterministic Python helpers, references, and assets added only when they actually make the workflow better.

Skills are also **explicit-only**.

Installing Skillet does not give an agent permission to silently activate these workflows. You invoke the skill you want, when you want it.

## Install Everything

Install the full Skillet globally into both Codex and Claude Code:

```bash
npx skills@latest add sakohovaguimian/skillet --global --agent codex claude-code --skill '*' --yes
```

See [INSTALL.md](INSTALL.md) for single-agent installs, updates, verification, and local development.

## Repository Map

```text
skillet/
├── .github/
│   ├── CODEOWNERS                  Default review ownership
│   ├── pull_request_template.md    Consistent review checklist
│   └── workflows/validate.yml      Automated contract and discovery validation
├── docs/
│   └── SKILL_AUTHORING_STANDARD.md Canonical SKILL.md template and invocation protocol
├── scripts/
│   └── validate_repository.py      Repository-wide authoring and helper validator
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

Every skill requires:

* `SKILL.md`
* `agents/openai.yaml`

Everything else is optional.

If a skill does not genuinely need a script, reference, or asset, it should not have one.

## Included Skills

| Skill                                   | Purpose                                                                                                                       |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `conversational-planning-grill-me`      | Discovers the repository and turns an idea into a decision-complete implementation plan.                                      |
| `dead-code-scanner`                     | Finds unreachable code, dead ends, obsolete resources, unnecessary references, and dependencies that can actually be removed. |
| `fix-root-causes`                       | Debugs the underlying problem instead of patching the symptom.                                                                |
| `grill-me`                              | Pressure-tests a plan until the important decisions are actually resolved.                                                    |
| `grimoire-project-scaffolding-protocol` | Scaffolds iOS projects from the Grimoire template.                                                                            |
| `ios-conversational-planning-grill-me`  | Extends conversational planning with iOS, SwiftUI, Rune, and domain-document discovery.                                       |
| `project-rune-implementation-protocol`  | Implements Rune-first SwiftUI features while preserving the architecture and patterns already in the project.                 |
| `swift-6-concurrency`                   | Helps design, migrate, review, and debug Swift 6 concurrency.                                                                 |
| `swift-sako-semantic-linter`            | Reviews Swift and SwiftUI against my local Sako/Rune conventions instead of generic style rules.                              |
| `ubiquitous-business-logic`             | Pulls hidden rules, edge cases, deeplinks, analytics behavior, and other business logic into explicit documentation.          |
| `ubiquitous-components`                 | Builds and maintains the shared Rune and app UI component catalog.                                                            |
| `ubiquitous-components-fetch`           | Pulls the shared Rune component catalog into a project.                                                                       |
| `ubiquitous-language`                   | Builds a domain glossary from what the codebase actually says and does.                                                       |
| `unslop`                                | Removes the obvious AI writing tells and makes the output sound human again.                                                  |

### Dead Code Means More Than "Unused"

The dead-code scanner intentionally goes further than unused-symbol counts.

Code can technically have references and still be dead.

A reference might come entirely from another dead island. It might exist only to preserve an obsolete feature. A function might still execute even though nobody observes or cares about its result anymore.

The skill traces both **reachability** and **present-day value** before recommending removal.

## Validate a Checkout

From the repository root:

```bash
python3 scripts/validate_repository.py
npx skills@latest add . --list
```

The Python validator checks the contracts Skillet depends on:

* naming
* frontmatter
* invocation policy
* section order
* cross-skill composition
* portable helper paths
* shared verbatim blocks
* local links
* README inventory parity
* helper startup

GitHub Actions runs the same validation on every push and pull request.

The `skills` CLI check verifies that the repository can actually be discovered and installed the same way a user would consume it.

## Design Choices

* Skills stay flat under `skills/`. Discovery should be obvious without building another indexing system around it.
* Every `SKILL.md` follows the structure and invocation contract in [docs/SKILL_AUTHORING_STANDARD.md](docs/SKILL_AUTHORING_STANDARD.md).
* Shared behavior is composed through `$skill-name`, not hidden runtime includes between skill folders.
* Folder names and frontmatter `name` values must match. Installation and invocation should be predictable.
* Every skill is explicit-only. Codex uses `allow_implicit_invocation: false`; Claude Code uses `disable-model-invocation: true`.
* Paths inside skills stay relative so the same skill works regardless of who installs it or which supported agent runs it.
* CI handles the mechanical rules. Humans still own judgment, usefulness, and authorization boundaries.
* Installed copies are outputs. **Change Skillet first, then reinstall or update.**
* There is intentionally no license yet. I want provenance and reuse terms settled before choosing one.
