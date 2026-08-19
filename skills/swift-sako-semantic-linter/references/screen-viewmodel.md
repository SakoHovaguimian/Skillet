# Screen and ViewModel Rules

## Canonical Screen Member Order

Order a screen's populated member sections exactly as follows, with at least one blank line between sections:

1. `@Environment`
2. `@Binding`
3. `@State` and `@StateObject`
4. `@FocusState`
5. other stored properties
6. non-view computed properties
7. initialization and non-view methods
8. view logic: `body`, `navHeader()`, content, sections, rows, cards, overlays, and other `some View` builders

Omit empty sections; do not collapse two populated sections together. Keep a screen's `body` and view-producing helpers in the final view-logic section. Keep `navHeader()` as a focused `some View` helper and call it directly from the header closure:

```swift
AppHeaderScrollView {
    navHeader()
} scrollViewContent: {
    content()
}
```

## ViewModel Contract

- Declare standard screen ViewModels as `final class` and conform to `ViewModel` or a more specialized project ViewModel protocol.
- Include `loggerName`, `loggerEmoji`, `logInit()`, and `logDeinit()` as one lifecycle contract.
- Hold screen-injected navigation services weakly.
- For route-created screens, install every route/context value through `@discardableResult func setup(...) -> Self` before analytics, first appearance, or loading can run.
- Keep `track()` in the final same-type extension in the primary ViewModel file.
- Make `handleFirstAppear()` call `track()` exactly once before applicable subscriber binding.
- Never bind screen publishers from `init`; temporary navigation destination construction must not create live subscriptions.
- Make repeated subscriber binding idempotent by guarding bound/empty state or intentionally replacing the cancel bag before rebinding.

## Screen Ownership and Lifecycle

- Let the screen own its injected ViewModel with `@StateObject` and initialize `_viewModel = StateObject(wrappedValue:)`.
- Let extracted forms and child views observe that same owner with `@ObservedObject`; never create a second owner for the same screen state.
- Use `.onFirstAppear { [weak viewModel] in ... }` for first-appearance wiring.
- Inject navigation before calling `handleFirstAppear()`.
- Never call `viewModel.track()` directly from a standard screen whose ViewModel owns `handleFirstAppear()`.
- Use `.task { [weak viewModel] in ... }` for initial async loading when applicable.
- Forward `.onDisappear { [weak viewModel] ... }` cleanup for capture, realtime, playback, recording, or other active sessions.

## SwiftUI Structure

- Keep `body` declarative and focused on composition, lifecycle hooks, and presentation.
- Extract coherent sections when they have a name, branch independently, repeat, or obscure the top-level flow.
- Prefer `private func section() -> some View` for parameterized sections.
- Add `@ViewBuilder` only when the helper needs conditional or multiple view-producing statements.
- Avoid extraction that merely renames a single modifier chain without improving reuse or comprehension.
- Keep side effects out of view construction. Use the project's established lifecycle and ViewModel entry points.
- Preserve stable identity in `ForEach`; use `\.self` only when values are genuinely stable and unique for the collection lifetime.
- Prefer `.animation(_:value:)` scoped to the state that drives the transition.
- Respect accessibility, Dynamic Type, localization, and reduced-motion behavior in touched UI.

## Analytics

- Track screen views only through `analyticsService.track(screen:)` from the trailing ViewModel `track()` extension.
- Add the matching `ScreenEvent` case and map it to `screen_view`.
- Include applicable context properties such as `workspace_id`, `project_id`, `client_id`, `member_id`, and `invitation_id`; compact nil values before emission.
- Keep intent, success, mutation, and error analytics beside the action that causes them rather than inside screen `track()`.
- Treat root, splash, and other nonstandard lifecycle surfaces as explicit, documented exceptions.
