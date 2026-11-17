# Skillet

<img width="400" height="400" alt="Skillet logo" src="https://github.com/user-attachments/assets/ec40177f-ec05-4be4-81ca-57fd9425fe16" />

Skillet is my personal collection of reusable agent skills for Codex and Claude Code.

The collection covers software engineering, product, planning, writing, brand design, and marketing. Each skill gives the agent a workflow I want to reuse, with a specific result and enough guidance to check it.

The goal is to **make agents work more like I do.**

## How It Works

Each installable skill lives at `skills/<section>/<skill-name>/`. Browse the [section folders](skills/) and invoke a skill by its name.

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
│   └── <section>/
│       └── <skill-name>/
│           ├── SKILL.md            Required skill entry point
│           ├── agents/openai.yaml  Required UI metadata and invocation policy
│           ├── references/         Optional, loaded only when needed
│           ├── scripts/            Optional deterministic helpers
│           └── assets/             Optional output resources
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

### Engineering

| Skill | Purpose |
| --- | --- |
| `backport` | Compares template evolution against a project's creation-date baseline and produces a detailed, prioritized adoption report. |
| `dead-code-scanner` | Finds unreachable code, dead ends, obsolete resources, unnecessary references, and dependencies that can actually be removed. |
| `diff-simplifier` | Simplifies recently modified code without changing its behavior or the codebase's existing architecture. |
| `fix-root-causes` | Distinguishes failure hypotheses, traces the causal mechanism, and repairs its responsible owner. |
| `opinionated-linter` | Reviews Swift and SwiftUI against my local Sako/Rune conventions instead of generic style rules. |
| `review-changes` | Independently reviews scoped code changes for bugs, regressions, and missed requirements, with optional implementation and fixes when requested. |
| `swift-6-concurrency` | Helps design, migrate, review, and debug Swift 6 concurrency. |

Use `diff-simplifier` to make a recent change easier to maintain while preserving behavior. Use `review-changes` for independent findings about correctness and scope. When requesting both, simplify first so the reviewer sees the resulting diff.

### Product

| Skill | Purpose |
| --- | --- |
| `ubiquitous-business-logic` | Pulls hidden rules, edge cases, deeplinks, analytics behavior, and other business logic into explicit documentation. |

### Planning

| Skill | Purpose |
| --- | --- |
| `conversational-planning-grill-me` | Discovers the repository and turns an idea into a decision-complete implementation plan. |
| `grill-me` | Pressure-tests a plan until the important decisions are actually resolved. |
| `implement-spec` | Reviews an existing plan against repository evidence and produces a guarded, self-contained implementation specification. |
| `ios-conversational-planning-grill-me` | Extends conversational planning with iOS, SwiftUI, Rune, and domain-document discovery. |
| `summarize-thread` | Turns a requirements discussion and supporting material into a concise technical specification, preserving rules and open decisions. |

### Writing and Communication

| Skill | Purpose |
| --- | --- |
| `help-me-senpai` | Explains how something works in plain English using a small example and, when available, a walkthrough of the actual case. |
| `how-to-use` | Writes a short guide to setting up, using, and checking a product feature. |
| `unslop` | Clarifies prose while preserving the author’s voice, evidence, and technical meaning. |

### Brand Design and Media

| Skill | Purpose |
| --- | --- |
| `build-brand-guide` | Creates HTML brand/product field guides with selectable identity, web/iOS libraries, and working previews tied to a coherent visual system. |

### Marketing and Growth

| Skill | Purpose |
| --- | --- |
| `app-store-screenshots` | Creates cohesive App Store screenshot campaigns with clear copy, faithful product imagery, connected layouts, and individual exports. |
| `pitch-it` | Explains a product or feature to a specific audience with a one-line pitch and short description. |
| `plan-a-launch` | Plans a product or feature launch across brand direction, marketing channels, social content, and measurement. |
| `whats-new-app-store` | Turns changes since the most recent GitHub release tag into short, emoji-prefixed App Store update notes. |

### Template-owned workflows

Grimoire owns new-project setup, feature implementation, and domain terminology through its root `AGENTS.md` and local documentation. Its `docs/NEW_PROJECT_CHECKLIST.md`, `docs/FEATURE_IMPLEMENTATION.md`, and `docs/FEATURE_DOCUMENTATION.md` travel with the template. Feature documents and the shared glossary evolve alongside the app. These workflows no longer require installed Skillet skills.

The component-catalog generation and fetch skills have been removed. Use project-local documentation and resolved Rune source for component discovery. Existing generated catalogs can remain lookup aids; verify them against the current dependency.

Removing a skill here does not uninstall a previously installed copy. See [installation maintenance](INSTALL.md) when updating an existing installation.

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

* Section folders group workflows by purpose. Each skill name is unique across the library.
* Every `SKILL.md` follows the structure and invocation contract in [docs/SKILL_AUTHORING_STANDARD.md](docs/SKILL_AUTHORING_STANDARD.md).
* Shared behavior is composed through `$skill-name`, not hidden runtime includes between skill folders.
* Folder names and frontmatter `name` values must match. Installation and invocation should be predictable.
* Every skill is explicit-only. Codex uses `allow_implicit_invocation: false`; Claude Code uses `disable-model-invocation: true`.
* Paths inside skills stay relative so the same skill works regardless of who installs it or which supported agent runs it.
* CI handles the mechanical rules. Humans still own judgment, usefulness, and authorization boundaries.
* Installed copies are outputs. **Change Skillet first, then reinstall or update.**
* There is intentionally no license yet. I want provenance and reuse terms settled before choosing one.
