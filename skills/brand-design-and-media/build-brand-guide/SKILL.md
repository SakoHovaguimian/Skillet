---
name: build-brand-guide
description: Create an interactive HTML brand and product field guide with selected identity, component-library, and product-preview modules. Use when asked for a brand dashboard, identity guide, themed web or iOS library, product design exploration, or targeted updates to an existing field guide. Do not use for production app implementation, project scaffolding, or a standalone raster brand board.
disable-model-invocation: true
---

# Build Brand Guide

## Outcome

Turn the user's product and brand direction into one complete, navigable HTML field guide. Connect the identity's meaning to its mark, typography, palette, imagery, and selected product applications. Deliver the requested modules with embedded CSS, JavaScript, SVGs, and supplied images, subject to the asset rules below.

The guide can contain identity, a product guide, web/iOS component libraries, and working product previews. These modules are independently selectable. A brand application demonstrates an identity; a product preview demonstrates behavior. This skill owns the design artifact, not the production app or its configuration.

## Inputs and preconditions

Inspect the supplied brief, assets, existing guide, and relevant product evidence. Reuse known answers. A complete brief authorizes work without another intake confirmation. Ask together only for missing decisions that materially change scope, identity, or demonstrated behavior; continue independent work while waiting.

Establish the product/audience, desired outcome, fixed brand assets and colors, references and their intended role, output destination, and selected modules. Discover product navigation, features, and rules only when the chosen module needs them. An identity-only guide does not need an app's full navigation or business-rule specification.

### Select the scope

| Request | Deliver |
| --- | --- |
| Brand identity guide or brand dashboard | Identity module with relevant illustrative applications; no automatic component catalogs or interactive product simulator |
| Web or iOS component library | The named platform's complete library, or the explicitly requested subset; no automatic second platform or assembled product preview |
| Web product preview or iOS simulator | Working local demonstrations for the requested platform/workflows; no automatic catalog or full identity chapter |
| Product field guide | Product guide plus explicitly requested or clearly implied modules; when no platform work is specified, start with identity and product explanation |
| Full web and iOS field guide | Identity, product guide, both complete libraries, and both product previews |
| Targeted update | Existing module scope and IDs; change only the requested content and genuinely affected dependencies |

Combine named modules as requested. A reference from another platform can supply visual inspiration without adding that platform to the output. If “full guide” leaves consequential platform scope unresolved, ask that focused question; do not assume both platforms. Record the chosen scope briefly in the overview. Do not make the user approve routine design choices or a complete supplied brief.

Preserve supplied identity unless redesign was requested. For a new identity, infer reasonable reversible design choices from the brief and mark consequential product assumptions as proposals. Accept delegated choices without another approval round. If promised assets are essential, wait for them or an explicit instruction to proceed without them; optional assets do not block independent work. Request attachments through a channel that supports them.

## Workflow

1. Establish the selected modules and inspect source material. For an existing HTML guide, inspect structure, tokens, assets, event handlers, and rendered behavior when available. For a library reference, inspect the requested categories, variants, states, and interactions before claiming parity. Separate visual inspiration, exact assets, and product facts.
2. Read [references/dashboard-contract.md](references/dashboard-contract.md) for conditional sections and token ownership, and [references/field-guide-experience.md](references/field-guide-experience.md) for navigation, accessibility, and presentation. Read [references/brand-direction.md](references/brand-direction.md) when creating or changing identity, imagery, or visual direction. Read [references/component-libraries.md](references/component-libraries.md) only when a library is selected. For a targeted edit, load only the relevant guidance and dependencies.
3. Define the brand direction before styling components. Connect audience and product promise to concrete choices in type, color roles, mark, composition, and imagery. Reuse an existing identity; otherwise choose a coherent concept. Keep an organizing metaphor optional. Create canonical assets and tokens before repeating them across applications.
4. For product modules, map supplied features, entities, destinations, rules, and meaningful states. Distinguish current evidence, intended behavior, and proposed demo rules. For selected libraries, enumerate the required families/variants/states before implementation. A requested complete library retains complete coverage for that platform.
5. Establish a representative composition using real copy, the canonical mark, and shared tokens. Inspect its hierarchy, small-size identity, and narrow-screen legibility before extending it. Continue without a checkpoint unless the user requested one or a material decision remains unresolved. Vary layout emphasis while preserving the identity.
6. Build the selected modules and relevant guide controls in one HTML file. Use shared CSS tokens, scoped theme mappings, and separate product data/rule/event logic. Reuse the canonical logo source rather than redrawing it per preview. Keep identity mockups distinguishable from working product demonstrations. Omit unselected chapters, navigation links, exports, and control code.
7. For targeted changes, trace the requested section, asset, or token dependencies. Propagate shared changes to affected selected modules and exports; keep platform-specific changes scoped. Preserve accepted content, geometry, IDs, and behavior elsewhere. Do not expand or remove an existing guide's modules merely to apply new defaults.
8. Reconcile the selected scope against rendered content. Check identity consistency, original assets, relevant logo treatments, requested library coverage, and working preview flows. Exercise applicable navigation, search/filter/disclosures, appearance, copy/download, responsive behavior, keyboard interaction, and print-state restoration. Inspect the browser when available, correct observed defects, and state verification limits precisely.

## Constraints

- User requirements and supplied identity outrank inspiration and defaults. Do not impose a warm editorial, dark cinematic, or category-based style on every product.
- Deliver finished content for selected modules. Do not add placeholder chapters, inert product controls, generic fake data, or unrequested platform catalogs to fill a layout. Static identity applications must be identifiable as illustrations.
- Preserve requested completeness. Selecting one platform does not reduce that platform's promised library to a handful of specimens.
- Use one canonical identity and semantic token system. Keep readable explanations in technical sections even when brand presentation panels use sparse text.
- Use CSS/SVG for code-native visuals and the environment's approved tools for raster generation/editing. Follow tool restrictions; do not upload supplied images elsewhere without authorization. Generated raster logo concepts are not editable vector masters.
- Label any unverified framework token mapping as proposed. Use Rune-specific exports only when requested or established by the brief; do not invent native integration or present an HTML/CSS phone preview as a native runtime.
- Keep scope limited to the guide and authorized reference inspection. Do not scaffold projects, modify production app code, run unauthorized builds/tests, publish, or claim trademark availability or measured commercial results.

## Failure handling

- Required scope, identity, or behavior is unresolved: name the concrete choice and pause only dependent work. No reply to an optional preference is not a reason to block the whole guide.
- A reference or exact asset is inaccessible: state the limit and request a replacement if necessary. Continue from supported inputs; never claim fidelity to unseen content. Do not replace a fixed logo with a new design without direction.
- Product rules are incomplete: use labeled representative behavior only where that is within scope; resolve material conflicts before depicting them as established product policy.
- A complete catalog is large: organize it with navigation, disclosures, and state matrices. Preserve selected coverage rather than silently truncating it or adding another platform.
- Raster generation or embedding is unavailable: use permitted code-native artwork when it satisfies the brief, or report the missing asset. Prompts may supplement the guide but cannot stand in for requested finished imagery.
- Fonts are unavailable: retain suitable fallbacks and disclose the external-loading limit without inventing a successful font check.
- A requested native theme schema is unavailable: show a complete proposed mapping and label it; do not claim direct import compatibility.
- Browser preview is unavailable: inspect source/data consistency and mark visual and interaction verification as not performed. Do not claim a checked rendered result.

## Output contract

Deliver one complete `index.html`, or the complete updated file for an existing guide, at the requested destination. Otherwise use a dedicated output location rather than overwriting an unrelated entry point. Include the applicable stable IDs from [references/dashboard-contract.md](references/dashboard-contract.md), selected modules, scope, and brief notes on consequential assumptions, asset dependencies, and verification limits.

When a file is saved, provide a usable file link and a concise account of selected modules and remaining limits. When HTML is requested inline, return the complete raw HTML if rendered directly, or one complete `html` code block. Honor output-only requests. Never substitute a patch, fragment, screenshot of a board, or promise of later content for the requested working guide.
