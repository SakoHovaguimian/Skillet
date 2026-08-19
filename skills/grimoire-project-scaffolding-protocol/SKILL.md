---
name: grimoire-project-scaffolding-protocol
description: Execute the initial scaffolding of a new iOS project from the Grimoire base template. Mandates strict requirement gathering via user prompting prior to execution to prevent hallucinations. Handles project-wide renaming, git resets, entry-point routing, and configuration while strictly maintaining existing architecture and formatting patterns.
disable-model-invocation: true
---

# Grimoire Project Scaffolding Protocol

## Phase 1: Mandatory Requirement Gathering (No Hallucination)

**CRITICAL:** Do not hallucinate, assume project details, or begin file modifications. Before executing any code changes or scaffolding, prompt the user for the following information. Present these questions clearly and stop to wait for the user's response:

1. **Project Name:** What is the new project name?
2. **Entry Flow:** Do you need Welcome / Login / Signup required as intro screens, or should the app just go directly to the main screen?
3. **Bundle ID:** What should the bundle ID be?
4. **Git Repository:** What remote git repo URL should the project point to? (The current git repo must be removed immediately regardless).
5. **Firebase Configuration:** If using Firebase, do you have a Firebase JSON file (or `GoogleService-Info.plist`) to replace the existing one in the exact same location?

## Phase 2: Enforce Non-Negotiables

- Treat existing Grimoire architecture as authoritative: match patterns, do not invent alternatives.
- Spacing, naming, and formatting should be followed to a T, matching the original code patterns exactly.
- Do not introduce architecture drift during scaffolding.

## Phase 3: Global Renaming & Header Standardization

Once the user provides the **Project Name**, execute a comprehensive replacement strategy:

1. **Project-Wide Renaming:** Rename the physical folder structure of the app.
   Rename Xcode targets, schemes, and build settings.
   Replace any string, variable, or configuration that references the original project name (`Grimoire` OR `GlowPro`) with the new project name.
2. **File Header Overwrites:** Search and replace top-of-file Xcode code comments.
   Replace the original project name reference with the new project name.
   Replace all existing file creation timestamps with today's date.

## Phase 4: Git & Config Scaffolding

1. **Git Reset:** Immediately remove the existing git repository tracking (`rm -rf .git`), initialize a fresh repository (`git init`), and point it to the user-provided git repo URL (`git remote add origin <url>`).
2. **Bundle ID:** Update the `.pbxproj`, `Info.plist`, and Target Build Settings to strictly reflect the user-provided Bundle ID.
3. **Firebase Swap:** If the user indicated Firebase usage and provided the configuration file, overwrite the existing file at the identical path. Ensure it remains correctly linked in the Xcode project hierarchy.

## Phase 5: Initial Routing Configuration

Modify the app's entry point based on the **Entry Flow** response:

- **If Intro Screens Required:** Wire the `AppRootView` and `NavigationService` to default to the unauthenticated state (Welcome -> Signup/Login -> Main App flow). Keep existing auth UI patterns intact. (This is how it comes by default so do nothing)
- **If Main Screen Only:** Bypass the auth/intro flow entirely. Set the initial route directly to the Main App (TabBar or Home screen). Strip out or disable the intro flow presentation logic from the default launch path. (In `MainViewModel`, hardcode the bools accordingly for `shouldShowWelcomeScreen` or `showShouldHomeScreen`.)

## Phase 6: Verify Before Finalizing

Validate all applicable items:

- User was explicitly prompted for all 5 scaffolding questions before generation started.
- Global rename from `Grimoire` or `GlowPro` to the new Project Name is complete across folders, targets, and build settings.
- All file headers updated (New Project Name + Today's Date).
- `.git` directory destroyed and new remote origin added.
- Bundle ID updated globally.
- Initial route logic matches the requested Entry Flow.
- Firebase config replaced (if applicable).
- Exact spacing, naming, and formatting parity achieved.

## Return Final Output In This Shape

- Scaffolding Execution Report
- Global Rename Summary (Targets, Folders, Headers)
- Git & Config Status
- Routing Setup Summary
- Integration Checklist with YES or NO per item
