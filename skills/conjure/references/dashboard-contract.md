# Dashboard contract

Read this after the required intake and before building or updating the dashboard.

## Document structure

Deliver a complete HTML document with a doctype, language, viewport metadata, meaningful title, embedded styles, and embedded scripts. Use semantic navigation, main content, headings, and sections. Give the page a composed visual hierarchy that fits the brief rather than imposing a particular palette or layout on every brand.

Keep these IDs stable so later requests can name a specific section:

| ID | Contents |
| --- | --- |
| `brand-identity` | Branding and identity section |
| `brand-logo` | Inline SVG mark and its usage |
| `brand-colors` | Named palette swatches and values |
| `brand-typography` | Header, body, and monospace specimens |
| `brand-guidelines` | Brand voice and visual tone |
| `brand-illustrations` | Two or three inline SVG illustrations or complete generation prompts |
| `web-portal` | Web Portal template section |
| `web-theme` | Readable web token/theme representation |
| `web-components` | Rendered web component showcase |
| `ios-grimoire` | iOS Grimoire template section |
| `ios-theme` | Rune JSON in a `pre` and `code` block |
| `ios-simulator` | Mobile frame and component variants |

Use unique IDs for individual component demonstrations and script blocks as needed. Preserve IDs during updates; do not reuse one ID for both an HTML section and a style or script element. Make navigation anchors work without JavaScript.

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

Keep theme data and mapping separate from DOM initialization and event handling. Use a separate, clearly commented interaction script for navigation enhancements, demo state, dialogs, and any copy controls. Scope handlers to their relevant section. Escape user-supplied strings when placing them in HTML or scripts; do not interpolate reference content as executable markup.

On a surgical update, trace the target ID or token group, change only the necessary source values and dependent mappings, and recheck the affected previews and displayed token data. Preserve unrelated content and theme groups. Return the complete updated file.

## Web Portal template

Display a useful token/theme overview and a rendered component showcase. Include at least:

- Primary, secondary, destructive, and disabled buttons, with visible hover/focus behavior.
- Labeled text inputs and a relevant selection control, with help text and an error example.
- Cards containing actual concept-specific content and an action.
- A navigation bar with a clearly selected item.
- A modal with working open and close controls, Escape dismissal, and sensible focus management.

Use native semantic controls where possible. Make buttons, selection controls, and modal demonstrations behave as their labels imply. Keep form actions local to the demonstration. Show enough states to assess how the theme works without adding production services or a framework.

Maintain readable contrast, visible keyboard focus, and clear active and disabled states. If a supplied brand color cannot serve as readable text or a control foreground, preserve its swatch and use a suitable accessible role or derived color in the UI.

## iOS Grimoire template

Print a complete Rune theme JSON object in `#ios-theme` inside `pre > code`. Include at least:

- Semantic colors with stable camelCase names and concrete color values.
- Font roles with family, numeric point size, and SwiftUI-style weight names.
- Numeric padding and spacing values expressed in points.
- Corner radii and control dimensions needed by the shown mobile components.

Keep units and color encodings unambiguous. Do not put CSS `var(...)` strings, unresolved aliases, comments, functions, or trailing commas in the printed JSON. Use actual source-backed Rune keys when supplied project documentation establishes them. Otherwise label the object as a proposed mapping and avoid claiming it can be imported unchanged. Note any custom-font bundling requirement within this section.

Build a CSS mobile frame with plausible iPhone proportions, safe-area spacing, a status area, and a home indicator. Render mobile variants of the same buttons, inputs, cards, navigation, and modal or sheet. Adapt density, control sizing, typography, and navigation for touch while retaining the shared identity. Allow the phone content to scroll without clipping controls or forcing horizontal page overflow.

Label the simulator as an HTML/CSS preview. It demonstrates the design translation and does not require an iOS project, native execution, or an Xcode build.

## Verification before delivery

- Confirm every required section, ID, logo, type specimen, guideline, illustration or prompt, component, and theme object is present and finished.
- Check that displayed theme data reflects the CSS tokens, and that the Rune block parses as JSON with concrete values and consistent units.
- Inspect a desktop layout and a narrow viewport when browser tools are available. Check text wrapping, phone containment, overflow, image loading, and readability.
- Exercise navigation anchors, form demos, dialog open/close behavior, and keyboard focus. Check for JavaScript errors when browser tools expose them.
- Verify all requested references were either used as directed or explicitly identified as inaccessible. Keep any material assumptions or verification limits visible within the relevant dashboard section.
- Deliver one complete file with embedded CSS and JavaScript, without unfinished content, omitted code, framework dependencies, or companion assets.
