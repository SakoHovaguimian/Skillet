# Dashboard contract

Read this after the required intake and before building or updating the dashboard.

## Document structure

Deliver a complete HTML document with a doctype, language, viewport metadata, meaningful title, embedded styles, and embedded scripts. Use semantic navigation, main content, headings, and sections. Give the page a composed visual hierarchy that fits the brief rather than imposing a particular palette or layout on every brand.

Give Brand Identity, Web Component Library, iOS Component Library, and Product Previews distinct top-level destinations. Give each library its own category navigation and render its complete catalog at a readable size. Keep the dashboard's inspection navigation separate from the application's requested tabs and navigation.

Keep these IDs stable so later requests can name a specific section:

| ID | Contents |
| --- | --- |
| `brand-identity` | Branding and identity section |
| `brand-logo` | Inline SVG mark and its usage |
| `brand-colors` | Named palette swatches and values |
| `brand-typography` | Header, body, and monospace specimens |
| `brand-guidelines` | Brand voice and visual tone |
| `brand-illustrations` | Two or three inline SVG illustrations or complete generation prompts |
| `product-brief` | Confirmed product directions, navigation, features, and demo rules |
| `component-coverage` | Catalog index linking each component family to web and iOS specimens |
| `web-portal` | Web Portal template section |
| `web-theme` | Readable web token/theme representation |
| `web-components` | Complete rendered web component library with categories and state matrices |
| `web-product-preview` | Working web application shell and feature demonstrations |
| `ios-grimoire` | iOS Grimoire template section |
| `ios-theme` | Rune JSON in a `pre` and `code` block |
| `ios-components` | Complete rendered iOS component library outside the mobile frame |
| `ios-simulator` | Mobile frame with requested app navigation and assembled feature screens |

Use unique IDs for individual component demonstrations and script blocks as needed. Preserve IDs during updates; do not reuse one ID for both an HTML section and a style or script element. Make navigation anchors work without JavaScript.

## Product direction and feature demonstrations

Summarize the confirmed brief in `#product-brief`: requested destinations and ordering, key features and entities, platform differences, and supplied business rules. Label delegated choices and sample rules as proposals. Build from the user's product rather than substituting the domain or navigation of an inspiration site.

Maintain clearly commented product data separately from visual themes and event handlers. Use named structures such as `productBrief`, `navigationModel`, and `demoData`, with explicit local rule functions where needed. Keep rule evaluation separate from rendering so a later request can change an allowed action or validation rule without rewriting the dashboard.

Use these directions throughout the output:

- Turn requested tabs and destinations into working application navigation in `#web-product-preview` and `#ios-simulator`. Render meaningful content for every specified destination. Use platform-appropriate navigation, and make overflow destinations reachable when the mobile tab bar cannot fit them all.
- Turn features into actual examples: forms, detail panels, dashboards, lists, filters, themed cards, and dialogs as appropriate. Use the same representative entities and terminology across components and assembled previews.
- Reflect business rules through available actions, required fields, validation messages, status transitions, role-sensitive controls, and meaningful empty/loading/error/success states. Explain why an action is unavailable when that matters to the workflow.
- Demonstrate a coherent local path through each requested key workflow. A field edit, selection, filter, tab change, or permitted action must update relevant visible state. Keep all examples isolated from real business data and external services.
- Keep the simulator and web preview aligned on product meaning while translating presentation and interactions for each platform. For example, a web table may become a grouped iOS list with a detail screen and action menu.

A feature name in a summary or an inert menu label is not a completed feature demonstration. Reference screenshots supply design evidence; explicit product requirements supply behavior. If behavior is unspecified, use a labeled representative example or ask when the choice materially changes the workflow.

## Branding and identity

- Design a clean, scalable inline SVG logo that relates to the concept. Give it a `viewBox`, a suitable accessible name, and theme-aware fills or strokes. Show the mark at a useful size and demonstrate any essential light/dark or small-size treatment.
- Show the supplied colors with names, actual values, and their intended roles. Preserve fixed brand swatches; derive additional surface, text, border, and status colors as needed for usable components.
- Select appropriate Google Fonts and load them through a Google Fonts stylesheet link in the document head. Define explicit header, body, and monospace stacks with usable local fallbacks, and show real type specimens with weights, sizes, and line heights.
- Write a short, specific account of the brand's voice and visual tone. Include practical guidance on typography, color use, and logo spacing or contrast rather than generic brand adjectives alone.
- Include two or three finished inline SVG illustrations, or two or three precise Midjourney/DALL-E prompts. Prompts must specify subject, composition, palette, style, lighting or texture where relevant, aspect ratio, and exclusions. Label prompts as prompts; do not imply that an image was generated.
- Inspect user reference images before using them. Translate the aspects the user selected into the design; reuse an exact image only when requested. Embed reused user raster images as data URLs and inline reused SVGs so the output does not depend on neighboring files.

Prefer CSS and inline SVG for new visuals. When a stock raster is necessary, use a verified concrete Unsplash image URL with descriptive alternative text; do not invent an image URL. Google Fonts and such Unsplash images may require a network connection. Make any remaining external asset dependency visible in a brief asset note, and retain a readable layout when an asset fails to load.

## Token architecture and surgical updates

### CSS tokens

Use clearly commented groups in `:root` for brand primitives, semantic roles, web styling, and mobile-specific overrides. Define all visual styling tokens there: colors, font stacks, type sizes and weights, line heights, spacing, component dimensions, borders, radii, shadows, and motion timings. Component rules consume `var(...)` rather than hard-coded theme values. Structural keywords, layout mechanics, and media-query conditions may remain literal where CSS requires them.

Use semantic names such as `--color-brand-primary`, `--color-surface`, `--color-text`, `--color-border`, `--color-focus-ring`, `--font-heading`, `--space-4`, and `--radius-control`. Make derived values traceable to the brand primitives. Define distinct hover, active, disabled, error, and focus treatments using the same token system.

Keep mobile overrides separately named, for example `--ios-control-height` or `--ios-radius-card`, so a Web Portal-only update does not accidentally restyle the mobile preview. Shared brand changes should still reach both platforms.

### Theme objects and scripts

Treat CSS `:root` as the source of truth for shared and web styling. In clearly named and commented theme-data script blocks, construct a `portalTheme` object and a `runeTheme` object from resolved CSS tokens. Keep iOS-specific mapping and intentional differences explicit. Do not maintain unrelated hand-edited copies of the same colors or let initialization overwrite a user's CSS token edit with stale JavaScript values.

Render the readable web theme and Rune JSON from these objects. Serialize Rune tokens with `JSON.stringify(runeTheme, null, 2)` into the code element's `textContent`, keeping the displayed JSON valid and aligned with the actual preview.

Keep theme data, product data, rule functions, and event handling in clearly commented blocks. Use a separate interaction script for catalog navigation, application navigation, demo state, dialogs, and any copy controls. Scope handlers to their relevant section, with intentional synchronization only where the same example shares state. Escape user-supplied strings when placing them in HTML or scripts; do not interpolate reference content as executable markup.

On a surgical update, trace the target ID or token group, change only the necessary source values and dependent mappings, and recheck the affected previews and displayed token data. Preserve unrelated content and theme groups. Return the complete updated file.

## Web Portal template

Build the complete library specified in [component-libraries.md](component-libraries.md). Match the supplied reference's library structure and breadth: application shell, category navigation, foundation specimens, component families, named variants, explicit state matrices, page patterns, and realistic composed examples. Apply the confirmed brand instead of inheriting the reference's palette or product copy.

Render all required specimens in `#web-components`, with linked category IDs and a useful token/theme overview in `#web-theme`. Build the product's web shell and meaningful feature demonstrations separately in `#web-product-preview`, reusing the catalog's styles and components.

Use native semantic controls where possible. Make buttons, selection controls, menus, and modal demonstrations behave as their labels imply. Dialogs need working open and close controls, Escape dismissal, and sensible focus management. Keep form actions local to the demonstration without adding production services or a framework.

Maintain readable contrast, visible keyboard focus, and clear active and disabled states. If a supplied brand color cannot serve as readable text or a control foreground, preserve its swatch and use a suitable accessible role or derived color in the UI.

## iOS Grimoire template

### Component library

Build the complete iOS catalog specified in [component-libraries.md](component-libraries.md) in `#ios-components`, independently of `#ios-simulator`. Match the web library's family and scenario coverage while showing iOS-appropriate controls, navigation, grouped lists, menus, alerts, sheets, card layouts, and touch states. Show named variants and states at a readable scale outside a phone frame. Make the mobile equivalents easy to compare with their web counterparts through the coverage index.

### Rune theme

Print a complete Rune theme JSON object in `#ios-theme` inside `pre > code`. Include at least:

- Semantic colors with stable camelCase names and concrete color values.
- Font roles with family, numeric point size, and SwiftUI-style weight names.
- Numeric padding and spacing values expressed in points.
- Corner radii and control dimensions needed by the shown mobile components.

Keep units and color encodings unambiguous. Do not put CSS `var(...)` strings, unresolved aliases, comments, functions, or trailing commas in the printed JSON. Use actual source-backed Rune keys when supplied project documentation establishes them. Otherwise label the object as a proposed mapping and avoid claiming it can be imported unchanged. Note any custom-font bundling requirement within this section.

### Simulator preview

Build a CSS mobile frame with plausible iPhone proportions, safe-area spacing, a status area, and a home indicator. Assemble the iOS catalog components into the requested app destinations and key feature flows. Keep all specified tabs or navigation destinations reachable, render their representative content, and demonstrate the confirmed local rules and states. Adapt density, control sizing, typography, and navigation for touch while retaining the shared identity. Allow the phone content to scroll without clipping controls or forcing horizontal page overflow.

Label the simulator as an HTML/CSS preview. It demonstrates the design translation and does not require an iOS project, native execution, or an Xcode build.

## Verification before delivery

- Reconcile every baseline category, supplied reference category, requested custom component, and important variant/state against the actual rendered web and iOS catalogs. Confirm the coverage index links to real specimens, including the full iOS library outside the simulator.
- Confirm every required section, ID, logo, type specimen, guideline, illustration or prompt, and theme object is present and finished.
- Visit every requested application destination in both product previews. Exercise the key feature flows and verify supplied rules affect validation, available actions, transitions, and feedback. Check product-specific cards use realistic domain content.
- Check that displayed theme data reflects the CSS tokens, and that the Rune block parses as JSON with concrete values and consistent units.
- Inspect a desktop layout and a narrow viewport when browser tools are available. Check text wrapping, phone containment, overflow, image loading, and readability.
- Exercise category navigation, segmented controls, dropdowns, chips, form demos, dialog/sheet open and close behavior, and keyboard focus in both catalogs. Check for JavaScript errors when browser tools expose them.
- Verify all requested references were either used as directed or explicitly identified as inaccessible. Keep any material assumptions or verification limits visible within the relevant dashboard section.
- Deliver one complete file with embedded CSS and JavaScript, without unfinished content, omitted code, framework dependencies, or companion assets.
