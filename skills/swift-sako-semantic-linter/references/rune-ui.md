# Rune UI Rules

- Reuse existing app wrappers and Rune components before adding custom UI.
- Discover and use the active environment style authority. In Style-environment projects, prefer `@Environment(\.style)` and `self.style` in production views; reserve `Style.shared` for static defaults or contexts without environment access.
- Treat `ColorSource` as an `AnyShapeStyle`. Pass it directly where supported and use `.source()` only when the called API or local authority requires conversion.
- Use `ImageSource` for Rune-backed system, resource, local, and remote images. Flag raw `Image(systemName:)`, `AsyncImage`, or custom caching when an established `ImageSource` or project wrapper covers the use case; allow drawing/canvas and framework-interoperability exceptions.
- Prefer the project's remote-image wrapper when it already supplies caching, thumbnail, content-mode, and placeholder behavior.
- Never hardcode production typography, spacing, radius, or colors when semantic tokens exist.
- Choose typography tokens by semantic role from nearby authority and sanity-check scale against adjacent screens.
- Use container/section rhythm and active environment spacing.
- Gate heavy content by data readiness and keep conditions local.
- Scope animations with `.animation(_:value:)`; use transitions for meaningful inserted/removed groups and targeted content transitions only where continuity helps.
- Use geometry or compositing groups only when complex animated elements need rendering coherence.
- Keep sheet and overlay triggers in the ViewModel and use project-standard presentation styles.
- Keep mock, preview, navigation, analytics, and first-appearance lifecycle wiring consistent with the feature's current pattern.
- Flag a custom component or raw visual token only when an existing Rune or project primitive clearly covers it. Place a necessary reusable component in the project component area and record the Rune gap.
