# Component libraries

Read this after the required intake, alongside [dashboard-contract.md](dashboard-contract.md). Use it to plan and verify both complete component catalogs. Apply this baseline unless the user explicitly narrows scope; expand it for supplied library references and requested features.

## Reference fidelity and catalog layout

When given an existing component-library page, inspect its category index, full page content, variants, state matrices, composed patterns, and visible interactions. Recreate its library structure and coverage in the generated web catalog, then provide an equivalent iOS catalog. Carry the confirmed brand and product directions into the result. Keep reference-specific product names, data, colors, or app tabs only when the user requests them.

Use a component-library workspace layout: clear platform destinations, persistent or easily accessible category navigation, section headings with brief usage notes, specimen surfaces, labeled variants, and visible state comparisons. On narrow viewports, adapt category navigation and specimen grids without hiding families or making controls unreadable. Build both catalogs in the single document; changing platform or category must expose real content.

Render iOS specimens in a full gallery outside the simulator. Use the simulator to compose those specimens into application screens. Keep all catalog families accessible even when only a subset appears on the selected application screen.

## Baseline coverage

Provide every family below for both platforms. The suffix column defines stable category IDs: prefix it with `web-` or `ios-`, such as `web-selection` and `ios-selection`. Keep all web categories inside `#web-components` and all iOS categories inside `#ios-components`.

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

Supplement the baseline with components implied by the feature set, such as date/time selection, a calendar, media attachments, pricing choices, or a domain-specific workflow control. Describe genuinely platform-specific patterns through their equivalent purpose; do not omit an entire family because its desktop control does not exist on iOS.

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

In each library, show at least three distinct product-specific card compositions in addition to the primitive card specimens. Derive their roles from the user's product and feature set: for example a domain record, an actionable task or next step, and a metric/status summary. These are examples of roles, not fixed business requirements.

Use realistic titles, descriptions, images or inline artwork when appropriate, status, metadata, and actions. Give the cards different information hierarchies and behavior; changing only an accent color or title does not create a distinct composition. Apply the shared theme while translating layout and touch behavior for iOS.

Use the same domain entities and confirmed rules in the libraries, web application preview, and simulator. If a record is unavailable, show its relevant disabled action and reason. If a feature uses a draft/published workflow, show those states and permitted transitions only when established by the user or labeled as sample behavior. Keep all mutations in local demo state.

## Interaction contract

Make segmented controls change selected content or a visible filtered result. Make dropdowns open and update a selection. Make switches, checkboxes, radios, tiles, and removable chips update visible state. Make contextual action menus, expandable sections, tabs, dialogs, and sheets open, navigate, or dismiss as labeled. Make filters and record selection affect the shown sample data and selection summary; make pagination move through actual local sample records.

Give each interaction an understandable local outcome. Keep demo buttons from navigating to missing routes or changing real application data. Use the supplied business rules for validation and availability; isolate illustrative behavior when no real rule was supplied. Keep keyboard focus, labels, Escape dismissal, and modal focus return usable, and provide sufficiently sized touch controls in iOS specimens.

## Coverage index and completion check

Include a compact `#component-coverage` index linking each family to its web and iOS category. Add requested custom families to it. Use it to make the delivered breadth easy to inspect, with any user-approved scope exception stated explicitly.

Before delivery, reconcile the inventory with rendered content, not just headings or data definitions. Verify that every category contains its promised variants and states, every link reaches real specimens, themed cards use the product brief, and each platform has a complete library. Check assembled web and mobile workflows separately. Preserve all required content when organizing long catalogs; use clear navigation and grouping instead of truncating the component set.
