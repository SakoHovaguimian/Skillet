# Component libraries

Read this only when a component library is selected, alongside [dashboard-contract.md](dashboard-contract.md). Apply the complete baseline to each selected platform unless the user explicitly requests a subset. Expand coverage for supplied library references and requested features. Selecting one platform does not add another platform or an assembled product preview.

## Reference fidelity and catalog layout

When given an existing component-library page as a coverage reference, inspect its category index, full content, variants, state matrices, composed patterns, and visible interactions. Recreate the requested structure and coverage for the selected platform, translating controls by purpose when the reference uses another platform. A visual-inspiration reference alone does not expand the catalog scope. Carry the supplied brand and product directions into the result. Keep reference-specific product names, data, colors, or app tabs only when requested.

Place selected libraries within the shell in [field-guide-experience.md](field-guide-experience.md): clear destinations, accessible category navigation, brief usage notes, specimen surfaces, labeled variants, and visible state comparisons. On narrow viewports, adapt navigation and grids without hiding families or making controls unreadable. When both catalogs are selected, keep them in the same document; changing platform or category must expose real content.

Give each full catalog labeled search, category filters, a matching-group count, and no-results reset. Use semantic disclosures and bulk expand/collapse controls where useful; preserve readable variant and state matrices inside them. A small explicitly requested subset can use simpler navigation. Search disclosed content as well as family names, reveal matching groups, and make direct links expose targets even when collapsed or filtered. Keep each catalog's controls independent from other collections and product demonstrations. Search and collapsed defaults organize the inventory; they never reduce required coverage.

Render selected iOS specimens in a readable gallery outside any phone frame. If a simulator is also selected, reuse those components in its application screens. Keep all catalog families accessible regardless of which application screen is active. A catalog-only request does not require a simulator.

## Baseline coverage

Provide every family below for each selected complete library. For an explicit subset, provide the requested families and their relevant variants and states, and label the scope as a subset. Prefix category ID suffixes with `web-` or `ios-`, such as `web-selection` and `ios-selection`. Keep web categories inside `#web-components` and iOS categories inside `#ios-components`. Use only the selected platform's column; the other column explains equivalent purposes when translation is needed.

| Family and ID suffix | Web specimens | iOS equivalents |
| --- | --- | --- |
| Foundations / Tokens — `foundations` | Semantic color swatches, type hierarchy, spacing scale, radii, shadows, outline icons, motion, focus treatment, and any requested appearance modes | Matching brand roles with mobile type sizes, point spacing, touch targets, radii, icons, and reduced-motion behavior |
| Page Patterns — `patterns` | Page header with breadcrumbs, supporting copy, facts, and actions; split setting section; data panel with search/filter and paging; list rows with trailing status/actions; multi-step progress; app navigation and tabs | Navigation bar with back/title/actions, tab bar, grouped settings sections, searchable record list, detail rows, and step progress adapted for mobile |
| Buttons — `buttons` | Primary, secondary, tertiary/ghost, icon-only, and destructive variants; readable size variants and state matrix | Filled, tinted or bordered, plain, icon/toolbar, and destructive variants; touch sizing and state matrix |
| Inputs — `inputs` | Text field, search, dropdown/select, multiline text, and color control; labeled, filled, validation, disabled, and read-only examples | Text field, search field, picker/menu, text editor, and color selection; mobile focus, validation, disabled, and read-only equivalents |
| Selection Controls — `selection` | Switches, checkboxes, radio groups, and segmented controls with selected/unselected/disabled choices | Switches, checkmark selection rows for single/multiple choice, and segmented controls with equivalent selection behavior |
| Selection Tiles / Chips — `tiles` | Selectable tiles, selected/unselected/disabled states, and chips reflecting current selection with removal where applicable | Touch selection tiles or rows and chips/tags that reflect and update the same choices |
| Cards — `cards` | Section card, actionable section card, compact information card, metric/stat card, status card, and product-specific themed cards | Mobile layouts for each card role with equivalent information and actions |
| Form Sections — `sections` | Titled groups with descriptions, fields, expandable/collapsible sections, read-only summary, and primary/secondary form actions | Grouped form sections, disclosure rows, inline validation, summary rows, and mobile action placement |
| Feedback / System States — `feedback` | Success/info/warning/error messages, dismissible alerts, toast, dialog, sheet, tooltip, popover, loading/progress, and skeleton examples | Inline messages or banners, transient feedback, alert/confirmation, action menu, sheet, contextual information, activity/progress, and skeleton equivalents |
| Empty States — `empty-states` | Standalone section, action-oriented empty state, embedded empty state, and no-results state | Equivalent grouped-list, screen, and inline empty states with mobile actions |
| Table / List Preview — `table` | Responsive table/list composition with realistic records, selection, status, search/filter, row actions, and pagination | Grouped or inset record list with selection, status, search/filter, detail navigation, actions, and suitable loading or paging behavior |

Supplement the selected scope with components needed by requested features, such as date/time selection, media attachments, or a domain-specific workflow control. Describe platform-specific patterns through their equivalent purpose; do not omit an entire promised family because its desktop control does not exist on iOS. Do not add product capabilities merely to populate a specimen.

## Variants and state matrices

Show several named specimens per family rather than one example standing in for a library. Make the relevant states inspectable side by side or through a clear state selector:

- Buttons: default, hover for pointer use, keyboard focus, pressed, disabled, and loading across the main variants. Give icon-only controls accessible names and distinguish disabled from loading.
- Fields: empty/default, filled, focused, invalid with a useful message, disabled, and read-only. Include helper text and required-field treatment when product rules need them.
- Selection: selected, unselected, disabled, and keyboard focus where applicable. Show at least a multi-option segmented control, a single-choice group, a multi-choice group, and a switch.
- Cards: actual section, information, metric, and status treatments, plus themed compositions with different purposes. Show selected, actionable, unavailable, or loading states where the card's function warrants them.
- Navigation and overlays: selected destination, back navigation, open/closed, dismissal, and available/unavailable actions. Use iOS pressed and selection states for touch rather than treating hover as a native requirement.
- Data and feedback: representative populated, empty/no-results, loading, validation/error, and success cases. Provide controls to reach transient states instead of displaying permanent loading animations as completed demos.

Label specimen states explicitly. A staged hover/focus specimen helps comparison but does not replace working pointer and keyboard behavior on interactive examples. Keep loading examples controllable and respect reduced-motion preferences.

## Themed cards and product examples

For a complete library, include composed examples grounded in the supplied product, alongside primitive card specimens. Choose distinct roles the product supports, such as a domain record, a next action, or a status summary. Show enough to demonstrate how primitives combine; do not invent features to meet a card quota. For a domain-neutral library, use clearly labeled illustrative content without implying a product specification. For an explicit subset, add compositions only where they help explain the requested components.

Use realistic titles, descriptions, images or inline artwork when appropriate, status, metadata, and actions. Give the cards different information hierarchies and behavior; changing only an accent color or title does not create a distinct composition. Apply the shared theme while translating layout and touch behavior for iOS.

Use the same domain entities and supplied rules across selected libraries and previews. If a record is unavailable, show its relevant disabled action and reason. Show workflow transitions only when established by the user or labeled as sample behavior. Keep all mutations in local demo state.

## Interaction contract

Make segmented controls change selected content or a visible filtered result. Make dropdowns open and update a selection. Make switches, checkboxes, radios, tiles, and removable chips update visible state. Make contextual action menus, expandable sections, tabs, dialogs, and sheets open, navigate, or dismiss as labeled. Make filters and record selection affect the shown sample data and selection summary; make pagination move through actual local sample records.

Give each interaction an understandable local outcome. Keep demo buttons from navigating to missing routes or changing real application data. Use the supplied business rules for validation and availability; isolate illustrative behavior when no real rule was supplied. Keep keyboard focus, labels, Escape dismissal, and modal focus return usable, and provide sufficiently sized touch controls in iOS specimens.

## Coverage index and completion check

Include a compact `#component-coverage` index linking promised families to real categories. Show columns only for selected platforms and add requested custom families. State any explicitly requested subset or exception; do not display an unselected platform as missing work. When both platforms are selected, connect equivalent purposes without pretending their controls are identical.

Before delivery, reconcile the selected inventory with rendered content, not just headings or data definitions. Verify promised variants and states, real link targets, meaningful composed examples, and complete coverage for every selected full library. Check selected assembled previews separately; the catalog does not stand in for a requested product flow. Preserve required content when organizing long catalogs instead of truncating the component set.
