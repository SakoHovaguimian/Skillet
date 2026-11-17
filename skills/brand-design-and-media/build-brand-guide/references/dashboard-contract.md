# Dashboard contract

Read this after selecting scope and before building the guide. Requirements below apply only to selected modules. A targeted update preserves existing scope unless the user changes it.

## Document structure and module boundaries

Deliver a complete HTML document with a doctype, language, viewport metadata, meaningful title, embedded styles, and any needed embedded scripts. Use semantic navigation, main content, headings, and sections. Apply [field-guide-experience.md](field-guide-experience.md) to the guide shell and [brand-direction.md](brand-direction.md) to new or changed visual direction.

Give each selected module a distinct destination. Keep guide navigation separate from application navigation. A library is an inspectable catalog; a product preview assembles working flows; an identity application illustrates visual usage. Selecting one does not require the others. Share styles and assets when modules coexist.

Use the following stable IDs for applicable content. Omit unselected sections and their links rather than adding empty chapters. Preserve existing IDs on updates. The legacy IDs `web-portal` and `ios-grimoire` identify platform sections; they do not require those frameworks.

| ID | Required when | Contents |
| --- | --- | --- |
| `dashboard-overview` | Always | Product introduction, selected scope, and relevant assumptions |
| `brand-identity` | Identity selected | Identity and relevant illustrative applications |
| `brand-logo` | Identity selected | Supplied or authorized new mark, variants, and practical usage |
| `brand-colors` | Identity selected | Named palette, values, and roles |
| `brand-typography` | Identity selected | Specimens for the type roles actually used |
| `brand-guidelines` | Identity selected | Specific voice, visual tone, and usage guidance |
| `brand-illustrations` | Imagery is part of the identity deliverable | Finished artwork and imagery direction |
| `product-brief` | Product guide selected | Product directions, entities, navigation, and rules |
| `product-features` | Product guide selected | Feature groups, rules, and states; links to any selected demonstrations |
| `component-coverage` | Any library selected | Index of the selected catalog families |
| `web-portal` | Any web module selected | Container for the selected web content |
| `web-theme` | Web library or web token export selected | Readable web tokens and mapping status |
| `web-components` | Web library selected | Catalog with categories, variants, and state matrices |
| `web-product-preview` | Web preview selected | Working local application shell and feature flows |
| `ios-grimoire` | Any iOS module selected | Container for the selected iOS content |
| `ios-theme` | iOS library or iOS token export selected | Concrete semantic iOS mapping, with schema status |
| `ios-components` | iOS library selected | Readable catalog outside any phone frame |
| `ios-simulator` | iOS preview selected | Phone frame with working local navigation and feature flows |

Use unique IDs for individual demonstrations and script blocks. Do not reuse a section ID for a style or script element. Make navigation anchors work without JavaScript. A preview-only guide can summarize its assumptions in the overview without acquiring a full product-guide chapter.

## Product guide and working previews

For a selected product guide, summarize supplied directions in `#product-brief`: entities, requested destinations and ordering, features, platform differences, and business rules. Build `#product-features` as readable groups explaining workflows, relevant rules, and states. Link only to demonstrations that exist. Use search and disclosures when the inventory warrants them. Derive counts from the actual inventory. Separate source-backed facts, intended behavior, and proposed additions.

For selected product previews, keep product data separate from visual themes and event handlers. Use named structures such as `productBrief`, `featureInventory`, `navigationModel`, and `demoData` where needed. Keep rule evaluation separate from rendering so a later rule change does not require rewriting the guide.

- Make requested destinations reachable, with meaningful content and platform-appropriate navigation. Handle overflow destinations when mobile tabs cannot fit them all.
- Demonstrate a coherent local path through each requested key workflow. Actions update visible state; fields validate; filters affect records; transitions produce feedback.
- Reflect supplied rules through required fields, available actions, status transitions, and relevant empty/loading/error/success states. Explain unavailable actions where the reason matters.
- Reuse representative entities and terminology across selected modules. When both previews are selected, preserve product meaning while translating presentation, such as a web table becoming a grouped iOS list.
- Keep all changes in local demo state, isolated from business data and external services.

A feature label or inert menu is not a completed preview. Screenshots establish appearance, not behavior. Label representative demo rules when permitted by the brief; resolve material conflicts before depicting them as policy. Static identity mockups follow the labeling rules in [brand-direction.md](brand-direction.md) and do not promise working workflows.

## Identity and asset handling

Follow the brand-direction reference for strategy, canonical logo reuse, variants, visual rhythm, and relevant applications. Preserve supplied identity unless redesign is authorized. Show exact color values and roles, readable type specimens, and practical guidance. Add finished imagery when it serves the brief; there is no illustration quota. Generation prompts can supplement requested artwork but cannot replace it.

Inspect references before using them. Translate the aspects the user selected; reuse exact assets only as authorized. Embed reused raster images as data URLs and SVGs inline so the file does not depend on neighboring assets. Preserve the original logo source and supported treatments. Use CSS/SVG for code-native visuals and approved tools for raster generation or editing.

Use suitable font stacks with local fallbacks. Google Fonts may load through a stylesheet link, or embed available licensed font files with required notices. If external stock imagery is appropriate, use a verified concrete source URL, never an invented URL. Disclose external font/image dependencies and preserve a readable layout if they fail. Do not send supplied assets to an external service without authorization. Include alternative text for meaningful images; hide purely decorative artwork from assistive technology.

## Token architecture and scoped updates

### CSS tokens

Use commented groups in `:root` for brand primitives, semantic roles, and selected platform styling. Define theme values there: colors, font stacks, type scales, spacing, component dimensions, borders, radii, shadows, and motion timings. Components consume `var(...)`; structural keywords, layout mechanics, and media-query conditions may remain literal. Keep exact fixed identity assets separate from UI appearance overrides.

Use semantic names such as `--color-brand-primary`, `--color-surface`, `--color-text`, `--color-border`, `--color-focus-ring`, `--font-heading`, `--space-4`, and `--radius-control`. Make derived values traceable to brand primitives. Define applicable hover, active, disabled, error, and focus treatments through the same system.

Name platform overrides separately, such as `--ios-control-height` and `--ios-radius-card`. Shared brand changes reach all affected selected modules; platform-specific changes stay scoped. Add appearance overrides only for supported modes.

### Theme mappings and scripts

Treat CSS tokens as the visual source of truth. For selected libraries or requested exports, construct mapping objects from resolved tokens. Use `portalTheme` for web and an appropriate semantic iOS object; use `runeTheme` only when Rune is requested or established by the brief. A preview alone does not require an export or theme chapter.

Render displayed JSON with `JSON.stringify(object, null, 2)` into `textContent`. Keep displayed, copied, and downloaded data derived from the same objects. Re-resolve appearance-dependent values after a mode change. Do not keep stale hand-edited copies or let initialization overwrite CSS edits with old JavaScript data. Identify appearance and mapping status; metadata wrappers belong outside any framework object with a fixed schema.

Separate theme data, product data, rule functions, and event handling into clearly commented blocks as needed. Keep guide state separate from product demo state. Scope handlers locally, synchronizing only shared examples deliberately. Escape supplied strings for their HTML or script context; never interpolate reference content as executable markup.

For a targeted update, trace the requested section or token group, update its affected mappings and applications, and recheck them. Preserve unrelated content, IDs, modules, and behavior. Return the complete updated file.

## Web modules

For a selected web library, build the catalog in [component-libraries.md](component-libraries.md) within `#web-components`, with category links and a token overview in `#web-theme`. Preserve requested reference coverage while applying the chosen identity. For a selected web preview, build the product shell and flows in `#web-product-preview`. Reuse catalog components when both modules exist; a preview alone needs only its own components.

Use native semantic controls where possible. Menus and dialogs need working open/close behavior, keyboard handling, Escape dismissal where appropriate, and sensible focus management. Keep form actions local. If an exact brand color is unsuitable as a foreground, preserve its swatch and use a readable semantic role or derived color for the control.

## iOS modules

### Component library and mapping

For a selected iOS library, build [component-libraries.md](component-libraries.md)'s catalog in `#ios-components` at a readable scale outside any phone frame. Adapt navigation, grouped lists, menus, alerts, sheets, card layouts, and touch states to iOS. When both libraries are selected, make their equivalent purposes easy to compare in the coverage index.

For an iOS library or requested export, show concrete semantic tokens in `#ios-theme` inside `pre > code`: colors, font roles with family/size/weight, spacing, radii, and relevant control dimensions. State units and color encodings. Use numeric points for proposed native sizes and explain any conversion from CSS. Do not include CSS `var(...)` strings, unresolved aliases, comments, functions, or trailing commas in JSON. Note custom-font bundling requirements.

When Rune or another native schema is requested, use inspected source-backed keys and units. If the schema is unavailable, label the mapping as proposed and do not claim direct import compatibility. Selecting iOS alone does not imply Rune, Grimoire, or an existing native project.

### Simulator preview

For a selected iOS preview, build a CSS phone frame with plausible proportions, safe-area spacing, a status area, and a home indicator. Implement requested navigation, screens, rules, and flows. Adapt density, typography, and controls for touch. Allow screen content to scroll without clipping controls or forcing horizontal page overflow.

Label this as an HTML/CSS preview. It demonstrates design and local behavior, not native execution. It does not require an iOS project or Xcode build.

## Verification before delivery

- Reconcile selected modules and applicable stable IDs with finished content. Omitted modules must not leave dead links, placeholder chapters, unused exports, or inert guide controls.
- For changed identity, run the visual checks in [brand-direction.md](brand-direction.md), including canonical assets and relevant logo treatments.
- For selected libraries, reconcile required families, variants, states, and links using [component-libraries.md](component-libraries.md). A requested complete library remains complete.
- For selected previews, visit every requested destination and exercise key flows, validation, transitions, and feedback. Verify rules against the supplied brief.
- For selected mappings, check concrete values, units, JSON parsing, and agreement with CSS and previews. Check copy/download data after any appearance change.
- Inspect desktop and narrow layouts when a browser is available. Check text, overflow, asset loading, focus, and applicable guide controls from [field-guide-experience.md](field-guide-experience.md). Check JavaScript errors when available.
- Record inaccessible references and unperformed checks precisely. Deliver one complete file without unfinished content, framework dependencies, or companion asset requirements; disclose permitted external asset links.
