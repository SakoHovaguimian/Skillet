# Feature Integration Parity Rules

- For new ViewModels, keep live DI, mock DI, and preview/mock resolver registration in parity, including actor annotations and constructor shape.
- Build previews with the project's mock resolver, required chainable route setup, shared fixtures, and mock service/style wrapper.
- Pair every new route with its navigation destination; resolve the live ViewModel and install all route context before the screen can track or load.
- Preserve the established route family, tab, sheet, adaptive-sheet, and full-screen-cover patterns.
- When API work applies, update the protocol first and keep live endpoint, mock endpoint, and fixture behavior signature-compatible.
- Locate the repository's actual live and mock endpoint authorities; do not assume mock endpoints live in DI assemblies.
- Use the project's shared request encoding, response decoding, query conversion, and configurable mock error/value helpers.
- Make mock fixtures realistic enough for filtering or pagination behavior the UI depends on.
- Reuse centralized domain permission helpers instead of duplicating role, membership, mutation, or visibility rules in screens or ViewModels.
