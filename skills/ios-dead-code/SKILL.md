---
name: ios-dead-code
description: Identify unused code, isolated code islands, orphaned UIKit/SwiftUI bridges, unused assets, stale localization keys, and unreached dependencies in hybrid UIKit/SwiftUI iOS projects. Use for an iOS dead-code audit, finding safe-to-remove Swift code, tracing reachability from @main/AppDelegate/SceneDelegate/storyboards/root SwiftUI views, reviewing UIHostingController or UIViewRepresentable bridges, inspecting unused Assets.xcassets or Localizable.strings entries, or reporting dependency cleanup candidates. Do not use to delete code; it produces an evidence-backed report.
disable-model-invocation: true
---

# iOS Dead Code

## Outcome

An evidence-backed audit report classifying unused code, assets, strings, and dependencies by removal confidence. Only classify code as safe to remove after tracing it back to a live entry point. A type, function, asset, or dependency is dead when it has no reachable lineage from one of these roots:

- `@main` SwiftUI `App`, `UIApplicationDelegate`, `AppDelegate`, `SceneDelegate`, `main.swift`, `UIApplicationMain`, or `@UIApplicationMain`
- `Info.plist` main storyboard, XIB/storyboard instantiation, segues, restoration identifiers, and target/action connections
- SwiftUI root views, navigation destinations, sheet/fullScreenCover/popover builders, tab builders, environment injections, and preview-excluded app composition
- System callbacks such as notification observers, app intents, widgets, extensions, URL schemes, push/deep links, background tasks, delegates, data sources, and `@objc` selectors

Treat internal references inside an unreachable cluster as a code island, not proof that the cluster is alive.

## Inputs and preconditions

An iOS project root containing an `.xcodeproj`, `.xcworkspace`, or `Package.swift`. If the user scopes the audit to a feature folder or to bridges, honor that scope with the script flags below.

## Workflow

1. Start with repository shape. Find `.xcodeproj`, `.xcworkspace`, `Package.swift`, `Podfile`, app targets, extension targets, asset catalogs, storyboards, XIBs, and localization files.
2. Run the helper scanner for a first-pass index (resolve `<skill-dir>` from the location of this `SKILL.md`):

   ```bash
   python3 <skill-dir>/scripts/ios_dead_code_scan.py <project-root> --include-assets --include-dependencies
   ```

   Use `--focus <path>` for a feature folder and `--focus-bridging` when the user asks for bridge-specific analysis. The script is an indexer, not a verdict engine.

3. Build a reachability map from entry points outward. Follow UIKit routing, SwiftUI view composition, dependency injection, coordinators, notifications, selectors, storyboards, XIBs, and app extension entry points.
4. Trace each candidate backward to a root. If it only reaches other candidates, classify the whole cluster as a potential code island.
5. Cross framework boundaries deliberately:
   - `UIHostingController(rootView:)`, `UIHostingController` subclasses, and UIKit coordinators pushing SwiftUI flows
   - `UIViewRepresentable` and `UIViewControllerRepresentable` wrappers around UIKit views/controllers
   - `Coordinator` objects used by representables
   - Environment objects, observable objects, Combine subjects, and delegate bridges shared between UIKit and SwiftUI
6. Inspect assets, strings, and dependencies after code reachability. Search code, storyboards, XIBs, plist files, package manifests, build settings, and generated resources before marking them unused.
7. Produce the report with confidence categories and removal groupings, using the output contract below.

### Detection checklist

Prioritize these categories:

- Bridging orphans: SwiftUI representables whose wrapped UIKit type is only reachable through the unused representable.
- Ghost coordinators and routers: UIKit coordinators that still instantiate removed or replaced SwiftUI flows.
- Orphaned view models/controllers: referenced by tests, previews, or dead classes but never instantiated in live UI.
- Protocol conformance islands: a conforming type implements required methods but the conforming type itself is never used.
- Dead Combine state: `@Published`, `PassthroughSubject`, `CurrentValueSubject`, or `.sink` pipelines left behind after a UIKit or SwiftUI consumer was removed.
- Interface Builder disconnects: `@IBOutlet` and `@IBAction` members not connected in active XIB/storyboard files.
- Unused imports and over-linked dependencies: imports, Swift packages, pods, or linked frameworks with no live usage.
- Dead assets and strings: image sets or localization keys not referenced by Swift, Objective-C, storyboards, XIBs, plists, or generated code.

## Constraints

Use the confidence categories strictly:

- Safe to Remove: private/internal code, assets, strings, or bridges with no dynamic invocation risk and no path from live entry points. Include the surrounding island if removal must be grouped.
- Potentially Unused: internally referenced clusters with no visible root path, or items that look stale but require one project-specific confirmation.
- Review Required: `public`/`open` APIs, `@objc`, selectors, reflection, `NSClassFromString`, dynamic asset names, Codable/Decodable DTOs, notification names, URL/deep-link handlers, app extensions, generated code, and cross-module entry points.

Never put `@objc` methods, public UI components, `Decodable` models, or string-addressed resources directly in Safe to Remove unless the dynamic call surface has been searched and ruled out.

## Composition

<interface>
| Invokes | When | Carries in | Expects back | If unavailable |
| --- | --- | --- | --- | --- |
| `$unslop` | Once, on the complete audit report, only when no parent workflow owns the final report | The complete drafted report | The prose-improved report with findings intact | Skip the pass and deliver the report unchanged |
</interface>

Invoke `$unslop` once on the complete user-facing artifact after its technical content is final, unless a parent workflow owns the final artifact, in which case the outermost workflow makes the single pass. `$unslop` may improve prose but must not change technical meaning: preserve code, paths, symbols, commands, measurements, quoted decisions, evidence anchors, classification labels, and document structure. If `$unslop` is unavailable, deliver the artifact unchanged and note the skipped pass. In this skill, the pass must also not change a finding, remove a caveat, or promote a candidate to a safer confidence category.

## Failure handling

- The scanner script fails or is missing: build the index manually with `rg` and project-file inspection, and note in the report that the first pass was manual.
- Dynamic usage cannot be ruled out for a candidate: classify it Review Required with the specific verification needed; never guess it into a safer category.
- The project layout is non-standard (no discoverable entry points): report which roots were searched and stop rather than inventing reachability.

## Output contract

Use this structure:

```markdown
# iOS Dead Code Detection Report

## Summary
- Total unused items:
- Safe to remove:
- Potentially unused:
- Review required:
- Estimated savings:

## Safe to Remove
### Bridging Orphans & Unreached Classes
- `path/file.swift:line`
  Reason: ...
  Removal group: ...

### Dead Combine Properties
- `path/file.swift:line`
  Reason: ...

### Unused Functions & Extensions
- `path/file.swift:line`
  Reason: ...

### Unused Assets & Strings
- `Assets.xcassets/name.imageset`
  Reason: ...

## Potentially Unused
- `path/file.swift:line`
  Reason: ...
  What would make it live: ...

## Review Required
- `path/file.swift:line`
  Risk: ...
  Verification: ...

## Dependencies
- `PackageOrFramework`
  Finding: ...

## Recommendations
- Immediate actions:
- Review steps:
- Suggested deletion order:
```

Include file paths and line numbers where possible. Explain the reachability failure, not just the reference count.

### Resources

- `scripts/ios_dead_code_scan.py`: static first-pass scan for Swift declarations, bridge patterns, likely unreferenced types, assets, localization keys, imports, packages, and pods.
- `references/analysis-guide.md`: load when doing a deeper audit or when candidates involve dynamic UIKit/SwiftUI reachability.
