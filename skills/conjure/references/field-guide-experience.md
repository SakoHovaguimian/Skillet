# Field guide experience

Read this after intake for every new Conjure dashboard. For an existing dashboard, apply it to the requested changes while preserving unrelated design and behavior. This reference captures the reusable presentation and interaction patterns inspected in GentlePath.html; the original file is not a runtime dependency.

## Visual direction

Present a polished editorial field guide that readers can browse, search, inspect, and print. Use these defaults when the confirmed brief leaves design choices open; explicit brand requirements and requested references take precedence.

| Element | Default treatment |
| --- | --- |
| Page shell | A quiet paper-like canvas, a slightly distinct sidebar, thin dividers, and a centered reading area with generous side gutters. Use a deep brand accent for emphasis and muted supporting color fields. |
| Typography | Pair expressive editorial headings with a clear sans serif for body text and controls. Lora with DM Sans is one suitable starting point; choose alternatives when the brand calls for them. Reserve italic emphasis for a short phrase. Keep catalog labels and explanations comfortably readable instead of copying tiny reference annotations. |
| Sidebar | A fixed desktop rail, approximately 220–250px wide, with a small mark, wordmark, guide label, numbered chapter links, a soft active highlight, and a restrained footer. Allow the rail itself to scroll on short displays. |
| Toolbar | A sticky top bar containing a compact brand/guide breadcrumb and appearance, download, and Print / PDF controls. Keep it distinct from the simulated product's navigation. |
| Overview | A short eyebrow, a concise product promise in large type, supporting copy, primary and secondary chapter links, and a substantial illustration with a small caption. Keep the hero readable on a small laptop; stack its copy and artwork on phones. |
| Scope and pillars | A slim, divided strip of facts derived from the delivered guide, followed by a few concise product-value statements with small illustrations. Count actual features, families, or destinations; do not invent usage metrics or copy the reference's model counts. Reuse appropriate identity artwork. |
| Chapters | Generous vertical spacing, a small eyebrow, a distinct heading, a short introduction, and a quiet decorative chapter number. Use a consistent numbering sequence that matches the sidebar. |
| Content surfaces | Rounded disclosure groups, simple tables and rows, readable specimen surfaces, and occasional tinted callouts. Approximately 20px card radii and 12px control radii are starting points, with fine borders and restrained shadows. Avoid putting every sentence or specimen inside another card. |
| Artwork | Prefer a coherent hero and supporting illustration language grounded in the user's concept. GentlePath's paths, leaves, and sunlight suit that brand; use subjects appropriate to the new product. Use finished embedded artwork or inline SVG for the visible hero. Generation prompts can supplement the identity section, but do not display them as finished images. |

For a warm brief without fixed colors, oat and paper surfaces, a forest-like primary, sage support, and a restrained lilac or clay accent are useful starting points. Translate these roles through the confirmed palette instead of making those hues universal. Provide a separately designed dark palette with readable semantic roles; do not invert the page or recolor fixed identity swatches.

## Information architecture

Use real, numbered chapter anchors with these default destinations: Overview, Product guide, Brand identity, Web library, iOS library, and Product previews. Chapters may be reordered or supplemented to suit the brief. Preserve the required IDs in [dashboard-contract.md](dashboard-contract.md), with separate readable web and iOS galleries and local category indexes. The field-guide shell organizes the full artifact; the web application and phone preview retain the user's requested app navigation.

Build `#dashboard-overview` around the product promise, scope facts, and value pillars. Summarize confirmed directions in `#product-brief`, with `#product-features` containing a browsable feature guide. Group features by meaningful product area. Each disclosure summary names the capability or group, explains its purpose, and shows a useful count or status. Expanded content explains the workflow, relevant rules and states, and links to its web and iOS demonstrations. Use a two-column layout for concise groups on wide displays and one column on narrow displays; allow complex specimen matrices to span the reading area.

Keep product facts distinct from implementation evidence. A supplied requirement describes intended behavior. A schema can establish entities, fields, and constraints, but does not establish implemented screens, APIs, permissions, or a live service. Label source-backed foundations, intended behavior, and proposed additions where they appear. Keep local demonstrations identifiable as demonstrations.

When the brief calls for planning or source exploration, add useful chapters such as proposed next steps, entity relationships, or AI concepts. Derive entity groups and counts from supplied sources, retain exact technical identifiers, and explain user-facing implications in plain language. Put long source listings behind disclosures with copy/download tools only when their inclusion is requested or useful to the brief. Keep proposals separate from current capabilities. Do not invent a schema, add an AI roadmap, or expose private source material merely to reproduce the reference's chapter list.

## Interaction contract

Implement these guide controls in addition to the component and product demonstrations. Share helpers where useful, but keep feature-guide, web-catalog, and iOS-catalog state scoped independently.

| Control | Required behavior |
| --- | --- |
| Chapter navigation | Use real fragment links that work without JavaScript. Update the active link and `aria-current` while scrolling and navigating. Account for the sticky bar in anchor offsets. Honor initial fragments and browser back/forward navigation. |
| Catalog and feature search | Give each browsable collection a labeled search field. Match case-insensitive query words against names, descriptions, and relevant metadata, including disclosed content. Combine query and category filters, reveal matching groups, and announce the number of matching groups out of the total in a polite status region. Label the unit accurately. |
| Category filters | Provide an All option, clear selected styling, and `aria-pressed` on filter buttons. Filters affect actual local content without modifying another collection's state. Keep every baseline family reachable. |
| Clear and reset | Clearing search retains the category and returns focus to the search field. A no-results message includes a reset action that clears query and category. Keep result counts, filter styling, and empty-state visibility synchronized. |
| Disclosure groups | Prefer semantic `details`/`summary`. Begin with a small useful selection open. Expand all / Collapse all affects currently matching groups, updates its label after individual toggles, and is disabled when nothing matches. Keep all content present in the document. |
| Direct specimen links | Reveal any collapsed or filtered ancestors needed to expose the target. Preserve the destination's stable ID, update its collection's controls consistently, and move focus sensibly when navigation closes a mobile drawer. |
| Appearance switch | Apply the saved light/dark preference before first paint when possible; otherwise follow `prefers-color-scheme`. Respect later system changes until an explicit preference is saved. Persist a brand-scoped preference when local storage is available, tolerate storage failure, and keep the switch's accessible state and `color-scheme` synchronized. |
| Copy tools | Copy displayed color values and the current web/Rune token JSON. Report success only after copying succeeds. If the clipboard is unavailable, show selectable text or offer the equivalent download and report the limit without false success feedback. Use an accessible status/toast region. |
| Downloads | Offer a clearly named local download of the web and proposed/source-backed Rune token mappings, with appearance and mapping status identified. Generate it from the same data shown in the guide, using a data URL or Blob and an appropriate filename and media type. Revoke temporary Blob URLs after use. Download source text only when authorized for inclusion. |
| Print / PDF | Invoke the browser print dialog with `window.print()` and a dedicated print stylesheet. Print all documentation and catalog groups, including currently filtered or collapsed ones. Hide guide navigation, overlays, and action-only tools while preserving visual specimens and labels. Use a legible light print palette, sensible page breaks, and unclipped tables/code. Restore temporary disclosure, filter, and visibility changes after printing or cancellation. This control opens the print dialog; do not claim it directly exports a PDF. |

Light/dark switching must refresh resolved theme objects, readable token JSON, and subsequent downloads across the guide, web preview, and iOS preview. Keep brand primitive swatches stable and label appearance-specific semantic swatches. Include both appearance mappings in exports, or identify the active appearance explicitly; never silently export stale values from another appearance. Apply [dashboard-contract.md](dashboard-contract.md)'s shared token architecture to both appearances.

## Responsive and accessible behavior

At a content-driven breakpoint near tablet width, replace the fixed rail with a menu drawer and overlay. Provide labeled open and close buttons, synchronized `aria-expanded`/`aria-controls`, Escape and overlay dismissal, focus containment while open, and focus return on dismissal. Keep closed drawer controls out of the tab order and prevent background interaction while it acts as a modal. Reset modal state when returning to desktop. Preserve ordinary usable navigation if enhancement fails.

Stack hero, feature groups, specimen grids, and scope facts as space narrows. Wrap filters or provide an obvious scroll affordance. Keep source blocks and genuinely wide matrices in their own scroll containers so the page itself does not overflow. Keep the phone frame contained while allowing its screen to scroll. Do not shrink the complete iOS library into the phone to fit the page.

Provide a skip link, meaningful heading order, visible focus, labels, sufficient contrast in both appearances, and touch targets suitable for the shown platform. Respect reduced-motion preferences, including anchor scrolling and disclosure transitions. Decorative numbering and icons must not obscure accessible names. Render substantive content and anchors before JavaScript adds search, collapse defaults, or drawer behavior.

## Verification

When a browser is available, inspect desktop and phone-width layouts in both appearances. Exercise a chapter link, scroll tracking, a fragment into a collapsed or filtered specimen, combined search and category filtering, no-results reset, individual and bulk disclosures, the mobile drawer by keyboard, a real copy result, and a token download. Confirm appearance changes update the displayed and downloaded tokens. Inspect print preview and verify the on-screen state returns after leaving it.

Reconcile the full web and iOS inventory and product flows separately, following the other two references. If visual inspection or an individual browser capability is unavailable, check the corresponding source/data paths and record that specific limitation in the artifact; do not report an unperformed interaction as verified.
