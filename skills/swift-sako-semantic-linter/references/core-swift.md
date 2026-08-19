# Core Swift Rules

## Member Access

- Use `self.` for all instance properties and references through instance properties, including bindings, state, environment values, dependencies, and closure properties.
- Omit `self.` for method calls unless the compiler requires it for capture, disambiguation, or escaping-closure semantics.
- Do not mistake a callable property for a method. Factory registrations such as `self.analyticsService()` may be property access through `callAsFunction` and must follow local framework authority.
- Keep compiler-required explicit capture or disambiguation, including escaping-closure cases.
- Do not rewrite static/global references as instance access.

## Whitespace and Braces

- Use `var body: some View`, never `var body : some View`.
- Do not add blank lines merely to pad braces.
- Keep short guards, branches, closures, and accessors compact when current local style does.
- Use a blank line between logical phases in longer bodies: validation, mutation, effects, and return/render.
- Preserve a deliberate legacy brace rhythm only when it is the active convention in the touched feature.
- Remove trailing whitespace and malformed member tokens such as `. leading`.

## Parameters and Closures

- Keep a declaration's first parameter on the declaration line when readable; place subsequent parameters one per aligned line.
- Apply the same rule to constructors and Swift initializers. In Sako-style repositories, keep the first parameter on the `init` line and align subsequent parameters beneath it. Do not introduce a bare `init(` line unless current local authority explicitly requires it.
- Keep a call on one line when readable. For a multiline call, place arguments one per line and the closing parenthesis on its own line.
- Do not force an argument onto the opening line when that reduces scanability or conflicts with the local formatter.
- Prefer trailing closures when they clarify the primary action; avoid multiple trailing closures when labels communicate intent better.
- Use `() -> Void`, not `() -> ()`.

## Naming and Ownership

- Use canonical domain language from project docs and nearby models.
- Avoid vague abbreviations, generic `data`/`item` names, and type names that hide lifecycle or ownership.
- Keep new independently owned top-level models and types in focused files when project instructions require separation.
- Place independently owned domain models in the project's top-level `Models` area when that is the established repository structure.
- Keep screens, ViewModels, and feature-only views in the feature area; place genuinely reusable components in the project component area.
- Synchronize filenames and file headers when the owned primary type is renamed.
- Use `// MARK: -` only when it improves navigation; do not create one-item ceremony.

## Safety Boundaries

- Do not change API shape, isolation, task ownership, state timing, navigation behavior, or other behavior under the label of linting.
- Do not apply a repository-wide format pass unless explicitly requested.
- Do not run builds or tests without authorization.
- Prefer a precise unresolved finding over a speculative automatic fix.
