# iOS Dead Code Analysis Guide

## Reachability Anchors

Search these anchors first:

- `@main`, `@UIApplicationMain`, `UIApplicationMain`, `main.swift`
- `AppDelegate`, `SceneDelegate`, `application(_:didFinishLaunchingWithOptions:)`, `scene(_:willConnectTo:)`
- `WindowGroup`, `UIApplicationDelegateAdaptor`, `UISceneDelegate`
- `Info.plist` keys: `UIMainStoryboardFile`, `UIApplicationSceneManifest`, URL schemes, background modes
- `Main.storyboard`, `LaunchScreen.storyboard`, active target membership clues in `.pbxproj`
- Extension entry points for widgets, intents, notifications, share extensions, and app clips

## UIKit and SwiftUI Bridge Patterns

Treat these as bridge boundaries that need explicit tracing:

- `UIHostingController(rootView: SomeView(...))`
- `class FooHostingController: UIHostingController<SomeView>`
- `UIViewRepresentable` and `UIViewControllerRepresentable`
- `makeUIView`, `updateUIView`, `makeUIViewController`, `updateUIViewController`
- `Coordinator` nested inside a representable
- UIKit routers/coordinators that push, present, or embed hosting controllers
- SwiftUI views that wrap legacy UIKit components but are absent from active `body` trees

If the SwiftUI wrapper is unreachable, the wrapper, coordinator, and wrapped UIKit type usually belong to one removal group.

## Dynamic Invocation Risks

Keep these in Review Required until searched:

- `@objc`, `dynamic`, `#selector`, target/action, gesture recognizers, notification selectors
- `NSClassFromString`, `NSSelectorFromString`, KVC/KVO, `perform(_:)`
- Storyboard identifiers, restoration identifiers, segue identifiers, nib names
- URL schemes, universal links, deep-link route strings, remote config flags
- Codable/Decodable DTOs and API response models
- Asset or localization names assembled from strings
- Public/open symbols used by another module or package product

## Asset and String Search

Search asset names in:

- Swift and Objective-C source: `Image("...")`, `UIImage(named:)`, `Color("...")`, generated resource wrappers
- Storyboards, XIBs, plists, asset catalogs, SwiftGen/R.swift outputs
- Tests and snapshots only after determining whether those tests describe live behavior

Search localization keys in:

- `Text("key")`, `String(localized:)`, `NSLocalizedString`, generated localization wrappers
- Storyboards, XIBs, plists, and server-driven UI mappings

Dynamic naming should downgrade to Review Required unless the naming scheme can be fully enumerated.

## Dependency Search

For Swift packages, pods, and linked frameworks:

1. Extract package/product names from `Package.swift`, `Package.resolved`, `.pbxproj`, `Podfile`, and lock files.
2. Search `import ModuleName`, generated wrappers, build scripts, linker flags, and plugin references.
3. Check whether dependency usage lives only in tests, previews, or dead islands.
4. Classify as Potentially Unused unless the target membership and import graph clearly show no app target usage.

## Reporting Heuristics

Use removal groups when files depend on each other inside the same dead island. Example:

- `LegacyCheckoutCoordinator`
- `CheckoutHostingController`
- `LegacyCheckoutRepresentable`
- `LegacyCheckoutViewController`
- `CheckoutLegacyViewModel`
- `Assets.xcassets/checkout_old_logo.imageset`

Estimate savings only when easy: lines from candidate files plus image file sizes. If uncertain, say `not estimated`.

When the audit is partial, state the search scope clearly. Avoid implying whole-app certainty after scanning only a feature folder.
