# Field guide experience

Use this for the selected guide modules. For an existing guide, apply it to requested changes while preserving unrelated design and behavior. Scale the shell and controls to the content; a short identity guide does not need a catalog workspace.

## Presentation and reading rhythm

Choose the visual direction from the brief and [brand-direction.md](brand-direction.md). Keep the guide easy to browse and inspect without imposing a fixed palette, font pairing, or mockup grid.

| Element | Treatment |
| --- | --- |
| Page shell | Use a readable content width, clear alignment, consistent gutters, and a hierarchy appropriate to the brand. A short guide can use a simple top navigation; a long guide benefits from a rail and local indexes. |
| Typography | Give headings, explanations, labels, and specimens distinct roles. Keep technical labels and body text comfortably readable even when brand panels use sparse oversized type. |
| Navigation | Show only selected chapters. If using a rail, keep it scrollable on short displays. Number chapters only when it helps orientation; match labels and order to the content. |
| Toolbar | Include useful guide controls, such as appearance, token downloads, and print, only when applicable. Keep them separate from the product's simulated navigation. |
| Overview | State the product promise and guide scope, then provide direct routes into the material. Use artwork when it supports the identity. Keep the introduction readable on a small laptop. |
| Scope facts | Derive counts from delivered features, families, and destinations. Do not invent usage metrics or add decorative statistics. |
| Sections | Vary emphasis and density with the content. Give the reader pauses between large specimens, practical explanations, and detailed matrices. |
| Content surfaces | Use tables, rows, disclosures, open space, and specimen surfaces where they help comparison. Avoid enclosing every sentence inside another card. |
| Artwork | Reuse the identity's subjects and treatments coherently. Display finished artwork; supplementary generation prompts are text instructions, not finished images. |

Design each supported appearance deliberately. Fixed identity swatches retain their values while semantic surfaces, text, and controls adapt. A brief for one appearance does not automatically require a second one.

## Information architecture

Use real chapter anchors for selected modules and applicable stable IDs from [dashboard-contract.md](dashboard-contract.md). Libraries retain readable galleries and local category indexes. The guide shell organizes the artifact; selected web and phone previews retain the requested application navigation.

For a selected product guide, explain directions in `#product-brief` and organize `#product-features` by meaningful product area. Summaries name the capability and purpose; expanded content explains workflows, relevant rules, and states. Link only to selected specimens and previews that exist. Short feature lists can stay expanded without search. Complex matrices may span the reading area; concise groups may sit side by side on wide screens.

Keep product facts distinct from implementation evidence. A requirement describes intended behavior. A schema establishes entities, fields, and constraints, but does not establish implemented screens, APIs, permissions, or a live service. Label proposals and local demonstrations where they appear.

Add planning or source-exploration content only when it serves the brief. Retain exact technical identifiers and explain their implications. Put lengthy source listings behind disclosures when their inclusion is authorized and useful. Do not add a roadmap, invent a schema, or expose private source material to fill a chapter list.

## Interaction contract

Implement applicable controls with these behaviors. Keep feature-guide, library, and product-demo state independent. Do not add a control whose target module or content is absent.

| Control and scope | Required behavior |
| --- | --- |
| Chapter navigation — guides with multiple sections | Use real fragment links that work without JavaScript. Keep the active link and `aria-current` current while scrolling and navigating. Account for sticky navigation offsets. Honor initial fragments and browser back/forward navigation. |
| Search — full catalogs and large feature inventories | Label each search field. Match case-insensitive query words against names, descriptions, and relevant metadata, including disclosed content. Combine query and category filters, reveal matching groups, and announce matching/total counts in a polite status region. Name the counted unit accurately. |
| Category filters — categorized collections | Provide an All option, selected styling, and `aria-pressed` on filter buttons. Affect only the local collection. Keep every required family reachable. |
| Clear and reset — searchable/filterable collections | Clearing search retains the category and returns focus to the field. No-results feedback includes reset for query and category. Keep counts, selected styling, and visibility synchronized. |
| Disclosures — long grouped content | Prefer `details`/`summary`. Keep all content in the document. When bulk controls help, Expand all / Collapse all affects matching groups, updates after individual toggles, and is disabled when nothing matches. |
| Direct specimen links — linked collections | Reveal collapsed or filtered ancestors so the target is visible. Preserve stable IDs and synchronize affected collection controls. Move focus sensibly, including when closing a mobile drawer. |
| Appearance switch — multiple supported modes | Apply a saved preference before first paint when possible; otherwise follow the system preference where supported. Respect later system changes until the user chooses a mode. Persist a brand-scoped preference when storage is available, tolerate storage failure, and synchronize accessible state and `color-scheme`. |
| Copy — palette values, library tokens, or requested exports | Copy the displayed value or current JSON. Report success only after copying succeeds. Otherwise show selectable text or an equivalent download and report the limit through accessible feedback. |
| Downloads — library mappings or requested exports | Generate only selected mappings from the same data shown. Identify platform, appearance, and proposed/source-backed status. Use a suitable filename and media type; revoke temporary Blob URLs after use. Include source text only when authorized. |
| Print — guides intended for printing or including a print control | Use `window.print()` and a print stylesheet. Include all selected documentation and catalog groups, including filtered or collapsed content. Hide navigation, overlays, and action-only tools; preserve specimens, labels, and logos. Use legible colors, sensible page breaks, and unclipped tables/code. Restore temporary disclosure/filter/visibility changes after printing or cancellation. Label this as the print dialog, not a direct PDF export. |

Appearance changes refresh affected resolved theme objects, displayed JSON, copied values, and downloads. Export both supported appearances or identify the active one explicitly; never silently export stale values. Apply the token architecture in [dashboard-contract.md](dashboard-contract.md).

## Responsive and accessible behavior

If the guide uses a desktop rail, adapt it to a usable narrow-screen navigation. A modal drawer needs labeled open/close buttons, synchronized `aria-expanded` and `aria-controls`, Escape and backdrop dismissal, focus containment, and focus return. Closed controls stay out of the tab order; the background is unavailable while the drawer is modal. Reset modal state when returning to desktop. Preserve ordinary navigation if enhancement fails. A compact guide can use wrapping links without a drawer.

Stack specimen grids and content groups as space narrows. Wrap filters or make their scrolling obvious. Keep wide matrices and source blocks in their own scroll containers so the page does not overflow. Contain any phone frame while letting its screen scroll; a selected iOS catalog remains readable outside the phone.

Provide a skip link when navigation precedes substantial content, meaningful heading order, visible focus, labels, sufficient contrast, and suitable touch targets. Respect reduced motion, including anchor scrolling and transitions. Decorative numbers and icons must not obscure accessible names. Render substantive content and anchors before JavaScript adds search, collapse defaults, or drawer behavior.

## Verification

Inspect desktop and narrow layouts in every supported appearance when a browser is available. Exercise applicable navigation and controls: fragments into hidden content, combined filters, reset, disclosures, keyboard drawer use, copy results, and downloads. Verify appearance changes reach displayed and exported tokens. If printing is included, inspect print preview and confirm the on-screen state returns afterward.

Reconcile selected library inventories and selected product flows separately. If visual inspection or a browser capability is unavailable, inspect the corresponding source/data paths and record that specific limitation. Do not report an unperformed interaction as verified.
